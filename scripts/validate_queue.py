#!/usr/bin/env python3
"""Valida os posts novos em queue/approved/ antes do merge do PR.

Checa, para cada arquivo:
  - nome no formato AAAA-MM-DD-HHMM-slug.md
  - frontmatter válido (campos, visibility, type)
  - scheduled_at no futuro e com fuso
  - texto entre 400 e 3.000 caracteres
  - nenhum placeholder {{...}} sobrando
  - detect.py --lang pt com nota >= 70
  - no máximo 1 post por dia (contando approved/ e published/, no fuso de SP)

Uso
  python scripts/validate_queue.py                        # todos os pendentes em approved/
  python scripts/validate_queue.py --base origin/main     # só os novos/alterados vs. a base
  python scripts/validate_queue.py queue/approved/X.md    # arquivos específicos
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / ".claude" / "skills" / "li-human"))
import detect  # noqa: E402
import queue_lib as q  # noqa: E402

MIN_CHARS, MAX_CHARS = 400, 3000
MIN_SCORE = 70
PLACEHOLDER_RE = re.compile(r"\{\{.*?\}\}", re.DOTALL)


def changed_files(base: str) -> list[Path]:
    out = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=AMR", f"{base}...HEAD", "--", "queue/approved/"],
        cwd=q.ROOT, capture_output=True, text=True, check=True).stdout
    return [q.ROOT / line for line in out.splitlines() if line.endswith(".md")]


def validate_post(post: q.Post, now: datetime, lex) -> list[str]:
    errs = []
    if not q.FILENAME_RE.match(post.path.name):
        errs.append("nome fora do padrão AAAA-MM-DD-HHMM-slug.md (slug em minúsculas, sem acento)")
    errs += q.schema_errors(post)
    if post.posted_urn:
        errs.append("arquivo novo não pode ter posted_urn (isso marca post já publicado)")
    dt = post.scheduled_at
    if dt is not None and dt.tzinfo is not None:
        # O nome do arquivo é só organização: quem manda é o scheduled_at.
        if dt <= now:
            errs.append(f"scheduled_at já passou: {dt.isoformat()}")
    n = len(post.body)
    if not MIN_CHARS <= n <= MAX_CHARS:
        errs.append(f"texto com {n} caracteres (precisa estar entre {MIN_CHARS} e {MAX_CHARS})")
    placeholders = PLACEHOLDER_RE.findall(post.body + "\n" + post.raw_front)
    if placeholders:
        errs.append("placeholder sem preencher: " + ", ".join(sorted(set(placeholders))))
    _, score, verdict = detect.run(post.body, lex, "pt")
    if score < MIN_SCORE:
        errs.append(f"detect.py --lang pt deu {score:.1f} ({verdict}); mínimo {MIN_SCORE}")
    return errs


def day_conflicts(targets: list[q.Post], approved_dir: Path, published_dir: Path) -> dict[Path, str]:
    """Mais de 1 post no mesmo dia (fuso de SP) em toda a fila."""
    by_day = defaultdict(list)
    seen = set()
    for directory in (approved_dir, published_dir):
        for path in sorted(Path(directory).glob("*.md")):
            try:
                post = q.load(path)
            except q.QueueError:
                continue
            dt = post.scheduled_at
            if dt is None or dt.tzinfo is None:
                continue
            by_day[q.local_date(dt)].append(path.name)
            seen.add(path.resolve())
    for post in targets:  # arquivos passados fora da pasta da fila também contam
        dt = post.scheduled_at
        if post.path.resolve() not in seen and dt is not None and dt.tzinfo is not None:
            by_day[q.local_date(dt)].append(post.path.name)
    out = {}
    for post in targets:
        dt = post.scheduled_at
        if dt is None or dt.tzinfo is None:
            continue
        names = by_day[q.local_date(dt)]
        if len(names) > 1:
            others = [n for n in names if n != post.path.name]
            out[post.path] = f"mais de 1 post em {q.local_date(dt)}: também {', '.join(others)}"
    return out


def run(argv=None, *, now=None, approved_dir=None, published_dir=None) -> int:
    ap = argparse.ArgumentParser(description="Valida os posts de queue/approved/.")
    ap.add_argument("files", nargs="*", help="arquivos a validar (padrão: todos os pendentes)")
    ap.add_argument("--base", help="valida só o que mudou em relação a este ref git")
    args = ap.parse_args(argv)

    approved_dir = Path(approved_dir or q.APPROVED)
    published_dir = Path(published_dir or q.PUBLISHED)
    now = now or datetime.now(q.TZ)
    lex = detect.load_lexicon("pt")

    if args.files:
        paths = [Path(f) for f in args.files]
    elif args.base:
        paths = [p for p in changed_files(args.base) if p.exists()]
    else:
        paths = q.approved_posts(approved_dir)

    if not paths:
        print("Nenhum post novo em queue/approved/ para validar.")
        return 0

    errors: dict[Path, list[str]] = {}
    posts = []
    for path in paths:
        try:
            post = q.load(path)
        except q.QueueError as exc:
            errors[path] = [str(exc)]
            continue
        if not args.files and not args.base and post.posted_urn:
            continue  # já publicado, aguardando a movimentação
        posts.append(post)
        errors[path] = validate_post(post, now, lex)
    for path, msg in day_conflicts(posts, approved_dir, published_dir).items():
        errors[path].append(msg)

    failed = 0
    gha = bool(os.environ.get("GITHUB_ACTIONS"))
    for path, errs in errors.items():
        rel = path.resolve().relative_to(q.ROOT) if path.resolve().is_relative_to(q.ROOT) else path
        if errs:
            failed += 1
            print(f"FALHOU  {rel}")
            for e in errs:
                print(f"   - {e}")
                if gha:
                    print(f"::error file={rel}::{e}")
        else:
            print(f"OK      {rel}")
    print(f"\n{len(errors) - failed} ok, {failed} com problema.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(run())
