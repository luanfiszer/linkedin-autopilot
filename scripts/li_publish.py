#!/usr/bin/env python3
"""Publica no LinkedIn os posts aprovados cujo horário já chegou.

Só lê queue/approved/, que só recebe arquivos por merge na main: o merge é a
aprovação. Publica no máximo 1 post por execução, o mais antigo primeiro.

Idempotência, em três camadas:
  1. Arquivo com `posted_urn` nunca é publicado de novo. Se ele ainda estiver
     em approved/ (a execução anterior publicou mas não terminou de mover), o
     script só termina a movimentação.
  2. Antes do POST o script grava `publish_attempted_at` no arquivo. Se a
     resposta for ambígua (timeout, erro 5xx), o marcador fica e o arquivo
     não é tentado de novo até alguém conferir no LinkedIn (sai com código 4).
  3. Em erro definitivo (4xx), o marcador é removido: nada foi criado.

Uso
  python scripts/li_publish.py                 # publica o próximo post vencido
  python scripts/li_publish.py --dry-run       # mostra o que faria, sem API
  python scripts/li_publish.py --file queue/approved/X.md   # publica X agora

Códigos de saída
  0  ok (publicou ou não havia nada a publicar)
  1  erro de publicação (tentará de novo na próxima execução)
  3  token expirado ou inválido
  4  publicação incerta: confira no LinkedIn antes de qualquer coisa
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
import queue_lib as q  # noqa: E402

API = "https://api.linkedin.com"
# Posts API versionada (YYYYMM). 202609 é a versão atual na Microsoft Learn
# (set/2026). Cada versão vale ~1 ano; sobrescreva com LINKEDIN_VERSION.
DEFAULT_VERSION = "202609"
TIMEOUT = 30

EXIT_OK, EXIT_FAIL, EXIT_TOKEN, EXIT_UNCERTAIN = 0, 1, 3, 4
TOKEN_MSG = ("Token do LinkedIn expirado ou inválido. Rode `python scripts/get_token.py` "
             "localmente e atualize o secret LINKEDIN_ACCESS_TOKEN no GitHub.")


class TokenError(RuntimeError):
    pass


class PublishError(RuntimeError):
    """Falha definitiva: o LinkedIn recusou, nada foi criado."""


class UncertainError(RuntimeError):
    """Não dá pra saber se o post foi criado (timeout, 5xx)."""


# --- little text --------------------------------------------------------------
# O campo `commentary` da Posts API usa o formato "little". Estes caracteres são
# reservados e precisam de barra invertida, senão o texto é cortado ou recusado:
LITTLE_RESERVED = set("\\|{}@[]()<>#*_~")
# Hashtag: '#' no começo do texto ou depois de algo que não é letra/dígito,
# seguido de letras e dígitos (acentos inclusos, pelo menos uma letra: "#1" é
# texto). Vira o HashtagTemplate da documentação, que funciona também com
# #TransformaçãoDigital.
HASHTAG_RE = re.compile(r"(?<![\w#])#([^\W_]*[^\W\d_][^\W_]*)")


def _escape_plain(text: str) -> str:
    return "".join("\\" + c if c in LITTLE_RESERVED else c for c in text)


def escape_little_text(text: str) -> str:
    """Escapa texto puro para o formato little, mantendo hashtags clicáveis."""
    out, pos = [], 0
    for m in HASHTAG_RE.finditer(text):
        out.append(_escape_plain(text[pos:m.start()]))
        out.append("{hashtag|\\#|" + m.group(1) + "}")
        pos = m.end()
    out.append(_escape_plain(text[pos:]))
    return "".join(out)


# --- API ----------------------------------------------------------------------
def _headers(token: str, version: str | None = None) -> dict:
    h = {
        "Authorization": f"Bearer {token}",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json",
    }
    if version:
        h["LinkedIn-Version"] = version
    return h


def _post(url, headers, body):
    try:
        return requests.post(url, headers=headers, json=body, timeout=TIMEOUT)
    except requests.ConnectTimeout as exc:
        # Nem conectou: com certeza nada foi criado.
        raise PublishError(f"sem conexão com o LinkedIn: {exc}") from exc
    except requests.ConnectionError as exc:
        msg = str(exc)
        if any(s in msg for s in ("NewConnectionError", "NameResolutionError", "Failed to resolve")):
            raise PublishError(f"sem conexão com o LinkedIn: {exc}") from exc
        raise UncertainError(f"conexão caiu durante o envio: {exc}") from exc
    except requests.Timeout as exc:
        raise UncertainError(f"timeout de {TIMEOUT}s esperando o LinkedIn") from exc


def _check(resp, endpoint):
    if resp.status_code == 401:
        raise TokenError(f"{endpoint}: 401 {resp.text[:300]}")
    if resp.status_code >= 500:
        raise UncertainError(f"{endpoint}: {resp.status_code} {resp.text[:300]}")
    if resp.status_code not in (200, 201):
        raise PublishError(f"{endpoint}: {resp.status_code} {resp.text[:300]}")


def _urn_from(resp) -> str:
    urn = resp.headers.get("x-restli-id") or resp.headers.get("X-RestLi-Id")
    if not urn:
        try:
            urn = resp.json().get("id")
        except ValueError:
            urn = None
    if not urn:
        raise UncertainError(f"LinkedIn respondeu {resp.status_code} sem o URN do post")
    return urn


def publish_rest(text, visibility, token, author, version):
    body = {
        "author": author,
        "commentary": escape_little_text(text),
        "visibility": visibility,
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": [],
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
    }
    resp = _post(f"{API}/rest/posts", _headers(token, version), body)
    _check(resp, "rest/posts")
    return _urn_from(resp)


def publish_ugc(text, visibility, token, author):
    """Fallback: API legada v2/ugcPosts. Texto puro, sem little text."""
    body = {
        "author": author,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": text},
                "shareMediaCategory": "NONE",
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": visibility},
    }
    resp = _post(f"{API}/v2/ugcPosts", _headers(token), body)
    _check(resp, "v2/ugcPosts")
    return _urn_from(resp)


def publish(text, visibility, token, author, version):
    """Tenta rest/posts; se ele recusar o token self-serve (403, versão), tenta
    v2/ugcPosts. Devolve (urn, endpoint usado)."""
    try:
        return publish_rest(text, visibility, token, author, version), "rest/posts"
    except PublishError as exc:
        first = str(exc)
        code = re.search(r": (\d{3}) ", first)
        if not code or code.group(1) not in {"403", "404", "426"}:
            raise
        print(f"  rest/posts recusou ({first[:120]}). Tentando v2/ugcPosts.", file=sys.stderr)
    try:
        return publish_ugc(text, visibility, token, author), "v2/ugcPosts"
    except PublishError as exc:
        if ": 403 " in str(exc):
            raise TokenError(f"403 nos dois endpoints. rest/posts: {first}; ugcPosts: {exc}") from exc
        raise


# --- fila ---------------------------------------------------------------------
def now_local():
    return datetime.now(q.TZ).replace(microsecond=0)


def append_log(post: q.Post, log_path: Path) -> None:
    def cell(s):
        return str(s).replace("|", "\\|").replace("\n", " ").strip()

    when = q.parse_datetime(post.meta["posted_at"]).strftime("%Y-%m-%d %H:%M")
    row = (f"| {when} | {cell(post.meta.get('type', ''))} | {cell(post.meta.get('hook', ''))} "
           f"| {cell(post.first_line)[:120]} | {cell(post.posted_urn)} |\n")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    existing = log_path.read_text(encoding="utf-8") if log_path.exists() else ""
    if post.posted_urn and post.posted_urn in existing:
        return  # já registrado
    if existing and not existing.endswith("\n"):
        existing += "\n"
    log_path.write_text(existing + row, encoding="utf-8")


def finalize(post: q.Post, published_dir: Path, log_path: Path) -> Path:
    """Move para published/ e registra no log. Seguro para repetir."""
    published_dir.mkdir(parents=True, exist_ok=True)
    dest = published_dir / post.path.name
    if post.path.resolve() != dest.resolve():
        shutil.move(str(post.path), dest)
        post.path = dest
    append_log(post, log_path)
    return dest


def select(paths, now, recover):
    """Separa (vencidos por ordem de horário, já publicados a recuperar, avisos)."""
    due, done, warnings = [], [], []
    for path in paths:
        try:
            post = q.load(path)
        except q.QueueError as exc:
            warnings.append(str(exc))
            continue
        if post.posted_urn:
            done.append(post)
            continue
        if post.attempted:
            warnings.append(f"{path.name}: publicação incerta em {post.meta['publish_attempted_at']}. "
                            "Confira no LinkedIn. Se saiu, adicione posted_urn; se não, apague "
                            "a linha publish_attempted_at.")
            continue
        errs = q.schema_errors(post)
        if errs:
            warnings.append(f"{path.name}: " + "; ".join(errs))
            continue
        if recover or post.scheduled_at <= now:
            due.append(post)
    due.sort(key=lambda p: (p.scheduled_at, p.path.name))
    return due, done, warnings


def run(argv=None, *, now=None, approved_dir=None, published_dir=None, log_path=None) -> int:
    ap = argparse.ArgumentParser(description="Publica no LinkedIn o próximo post aprovado.")
    ap.add_argument("--dry-run", action="store_true", help="mostra o que seria publicado, sem API")
    ap.add_argument("--file", help="publica este arquivo agora, ignorando scheduled_at")
    args = ap.parse_args(argv)

    approved_dir = Path(approved_dir or q.APPROVED)
    published_dir = Path(published_dir or q.PUBLISHED)
    log_path = Path(log_path or q.LOG)
    now = now or now_local()

    if args.file:
        paths = [Path(args.file)]
        if not paths[0].exists():
            print(f"Arquivo não encontrado: {args.file}", file=sys.stderr)
            return EXIT_FAIL
    else:
        paths = q.approved_posts(approved_dir)

    due, done, warnings = select(paths, now, recover=bool(args.file))
    for w in warnings:
        print(f"AVISO: {w}", file=sys.stderr)

    # Recuperação: publicado numa execução anterior mas ainda em approved/.
    for post in done:
        if post.path.parent.resolve() == published_dir.resolve():
            print(f"{post.path.name} já foi publicado ({post.posted_urn}). Nada a fazer.")
            continue
        if args.dry_run:
            print(f"[dry-run] {post.path.name} já tem posted_urn; seria só movido para published/.")
            continue
        dest = finalize(post, published_dir, log_path)
        print(f"{post.path.name} já tinha posted_urn ({post.posted_urn}). Movido para {dest}.")

    if not due:
        print(f"Nada a publicar agora ({now.isoformat()}).")
        return EXIT_OK

    post = due[0]  # no máximo 1 por execução
    pending = len(due) - 1
    print(f"Próximo: {post.path.name}  [{post.meta['type']}] {post.meta['visibility']} "
          f"agendado para {post.scheduled_at.isoformat()}")
    if pending:
        print(f"(mais {pending} vencido(s) na fila; sai 1 por execução)")

    if args.dry_run:
        print("\n[dry-run] commentary que seria enviado para rest/posts:\n")
        print(escape_little_text(post.body))
        print(f"\n[dry-run] {len(post.body)} caracteres. Nada foi enviado.")
        return EXIT_OK

    token = os.environ.get("LINKEDIN_ACCESS_TOKEN", "").strip()
    author = os.environ.get("LINKEDIN_PERSON_URN", "").strip()
    version = os.environ.get("LINKEDIN_VERSION", "").strip() or DEFAULT_VERSION
    if not token:
        print(f"LINKEDIN_ACCESS_TOKEN não definido. {TOKEN_MSG}", file=sys.stderr)
        return EXIT_TOKEN
    if not author.startswith("urn:li:person:"):
        print("LINKEDIN_PERSON_URN ausente ou inválido (esperado urn:li:person:...). "
              "Rode scripts/get_token.py.", file=sys.stderr)
        return EXIT_FAIL

    q.set_fields(post, publish_attempted_at=now.isoformat())
    try:
        urn, endpoint = publish(post.body, post.meta["visibility"], token, author, version)
    except TokenError as exc:
        q.set_fields(post, publish_attempted_at=None)
        print(f"ERRO: {TOKEN_MSG}\n  detalhe: {exc}", file=sys.stderr)
        return EXIT_TOKEN
    except PublishError as exc:
        q.set_fields(post, publish_attempted_at=None)
        print(f"ERRO ao publicar {post.path.name}: {exc}", file=sys.stderr)
        return EXIT_FAIL
    except UncertainError as exc:
        print(f"PUBLICAÇÃO INCERTA de {post.path.name}: {exc}\n"
              "Confira o seu perfil no LinkedIn. O arquivo ficou marcado com "
              "publish_attempted_at e não será tentado de novo sozinho.", file=sys.stderr)
        return EXIT_UNCERTAIN

    posted_at = datetime.now(q.TZ).replace(microsecond=0).isoformat()
    q.set_fields(post, publish_attempted_at=None, posted_urn=urn, posted_at=posted_at,
                 posted_via=endpoint)
    dest = finalize(post, published_dir, log_path)
    print(f"PUBLICADO via {endpoint}: {urn}\n  https://www.linkedin.com/feed/update/{urn}/\n"
          f"  arquivo: {dest}")
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as fh:
            fh.write(f"published_slug={post.slug}\n")
    return EXIT_OK


def main():
    try:
        from dotenv import load_dotenv
        load_dotenv(q.ROOT / ".env")
    except ImportError:
        pass
    sys.exit(run())


if __name__ == "__main__":
    main()
