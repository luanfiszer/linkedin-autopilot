"""Leitura e escrita dos arquivos da fila (queue/approved e queue/published).

Cada post é um .md com frontmatter YAML entre linhas '---' e o texto do post
logo abaixo, exatamente como deve ser publicado.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import yaml

ROOT = Path(__file__).resolve().parent.parent
APPROVED = ROOT / "queue" / "approved"
PUBLISHED = ROOT / "queue" / "published"
LOG = ROOT / "linkedin" / "log.md"
TZ = ZoneInfo("America/Sao_Paulo")

VISIBILITIES = {"PUBLIC", "CONNECTIONS"}
TYPES = {"PROOF", "OPINION", "TEACH", "STORY", "OFFER"}
REQUIRED = ("scheduled_at", "visibility", "type", "hook")
FILENAME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-\d{4}-[a-z0-9][a-z0-9-]*\.md$")
FRONT_RE = re.compile(r"\A---[ \t]*\n(.*?)\n---[ \t]*\n?(.*)\Z", re.DOTALL)


class QueueError(ValueError):
    """Arquivo da fila malformado."""


@dataclass
class Post:
    path: Path
    meta: dict
    body: str
    raw_front: str
    errors: list[str] = field(default_factory=list)

    @property
    def slug(self) -> str:
        return self.path.stem

    @property
    def scheduled_at(self) -> datetime | None:
        return parse_datetime(self.meta.get("scheduled_at"))

    @property
    def posted_urn(self) -> str | None:
        return self.meta.get("posted_urn") or None

    @property
    def attempted(self) -> bool:
        return bool(self.meta.get("publish_attempted_at"))

    @property
    def first_line(self) -> str:
        for line in self.body.splitlines():
            if line.strip():
                return line.strip()
        return ""


def parse_datetime(value) -> datetime | None:
    """Aceita datetime (o YAML converte sozinho) ou string ISO 8601."""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    try:
        return datetime.fromisoformat(str(value).strip())
    except ValueError:
        return None


def load(path: Path) -> Post:
    text = Path(path).read_text(encoding="utf-8")
    m = FRONT_RE.match(text)
    if not m:
        raise QueueError(f"{path.name}: frontmatter ausente (o arquivo tem que começar com '---')")
    raw_front, body = m.group(1), m.group(2)
    try:
        meta = yaml.safe_load(raw_front) or {}
    except yaml.YAMLError as exc:
        raise QueueError(f"{path.name}: YAML inválido no frontmatter: {exc}") from exc
    if not isinstance(meta, dict):
        raise QueueError(f"{path.name}: frontmatter precisa ser um mapa chave: valor")
    return Post(path=Path(path), meta=meta, body=body.strip("\n"), raw_front=raw_front)


def schema_errors(post: Post) -> list[str]:
    """Erros de estrutura (não inclui regras de agenda, tamanho ou nota)."""
    errs = []
    for key in REQUIRED:
        if post.meta.get(key) in (None, ""):
            errs.append(f"campo obrigatório ausente: {key}")
    sched = post.meta.get("scheduled_at")
    dt = parse_datetime(sched)
    if sched is not None and dt is None:
        errs.append(f"scheduled_at não é uma data ISO 8601: {sched!r}")
    elif dt is not None and dt.tzinfo is None:
        errs.append("scheduled_at sem fuso horário (use por exemplo 2026-09-29T08:15:00-03:00)")
    vis = post.meta.get("visibility")
    if vis is not None and vis not in VISIBILITIES:
        errs.append(f"visibility inválida: {vis!r} (use PUBLIC ou CONNECTIONS)")
    typ = post.meta.get("type")
    if typ is not None and typ not in TYPES:
        errs.append(f"type inválido: {typ!r} (use {' | '.join(sorted(TYPES))})")
    score = post.meta.get("human_score")
    if score is not None and not isinstance(score, (int, float)):
        errs.append(f"human_score precisa ser número: {score!r}")
    if not post.body.strip():
        errs.append("texto do post vazio")
    return errs


def _yaml_scalar(value: str) -> str:
    return '"' + str(value).replace("\\", "\\\\").replace('"', '\\"') + '"'


def set_fields(post: Post, **fields) -> None:
    """Grava ou remove campos no frontmatter preservando o resto do arquivo.

    Não reserializa o YAML inteiro: mantém comentários e a ordem que o
    usuário escreveu. None remove o campo.
    """
    lines = post.raw_front.splitlines()
    for key, value in fields.items():
        lines = [ln for ln in lines if not re.match(rf"^{re.escape(key)}\s*:", ln)]
        if value is not None:
            lines.append(f"{key}: {_yaml_scalar(value)}")
        post.meta.pop(key, None)
        if value is not None:
            post.meta[key] = value
    post.raw_front = "\n".join(lines)
    post.path.write_text(f"---\n{post.raw_front}\n---\n{post.body}\n", encoding="utf-8")


def approved_posts(directory: Path = APPROVED) -> list[Path]:
    return sorted(p for p in Path(directory).glob("*.md"))


def local_date(dt: datetime):
    return dt.astimezone(TZ).date()
