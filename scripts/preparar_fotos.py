#!/usr/bin/env python3
"""Prepara fotos para os posts: coloque as originais em media/entrada/ e rode

  python scripts/preparar_fotos.py

Para cada foto (jpg, png, heic):
  - converte HEIC para JPEG (com o `sips` do macOS);
  - corrige a rotação e reduz para no máximo 2000 px no lado maior;
  - salva em media/fotos/<nome-em-minusculas>.jpg SEM metadados (EXIF, GPS,
    modelo do celular), e acrescenta uma linha em media/fotos/CATALOGO.md.

media/entrada/ está no .gitignore: os originais nunca vão para o GitHub.
Rode localmente (precisa de Pillow: pip install -r requirements-dev.txt).
"""
from __future__ import annotations

import re
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "media" / "entrada"
OUT = ROOT / "media" / "fotos"
CATALOG = OUT / "CATALOGO.md"
MAX_SIDE = 2000
EXTS = {".jpg", ".jpeg", ".png", ".heic", ".heif"}


def slugify(name: str) -> str:
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s or "foto"


def open_image(path: Path, tmp: Path) -> Image.Image:
    if path.suffix.lower() in {".heic", ".heif"}:
        jpg = tmp / (path.stem + ".jpg")
        subprocess.run(["sips", "-s", "format", "jpeg", str(path), "--out", str(jpg)],
                       check=True, capture_output=True)
        path = jpg
    return Image.open(path)


def prepare(path: Path, tmp: Path) -> Path:
    img = ImageOps.exif_transpose(open_image(path, tmp))  # aplica a rotação antes de perder o EXIF
    img = img.convert("RGB")
    img.thumbnail((MAX_SIDE, MAX_SIDE))
    dest = OUT / f"{slugify(path.stem)}.jpg"
    n = 2
    while dest.exists():
        dest = OUT / f"{slugify(path.stem)}-{n}.jpg"
        n += 1
    # Salvar sem passar exif= descarta todos os metadados.
    img.save(dest, "JPEG", quality=85, optimize=True, progressive=True)
    return dest


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    photos = sorted(p for p in INBOX.iterdir() if p.suffix.lower() in EXTS) if INBOX.exists() else []
    if not photos:
        sys.exit(f"Nenhuma foto em {INBOX.relative_to(ROOT)}/ (jpg, png ou heic).")
    if not CATALOG.exists():
        CATALOG.write_text("# Catálogo de fotos\n\nDescreva cada foto em uma linha (opcional, "
                           "mas ajuda a rotina a escolher). A rotina escreve o texto alternativo.\n\n"
                           "| arquivo | descrição |\n| --- | --- |\n", encoding="utf-8")
    with tempfile.TemporaryDirectory() as tmp:
        for src in photos:
            dest = prepare(src, Path(tmp))
            kb = dest.stat().st_size // 1024
            with open(CATALOG, "a", encoding="utf-8") as fh:
                fh.write(f"| {dest.name} | |\n")
            print(f"{src.name} -> {dest.relative_to(ROOT)} ({kb} KB, sem metadados)")
    print("\nConfira as fotos, apague os originais de media/entrada/ se quiser, "
          "e commite media/fotos/.")


if __name__ == "__main__":
    main()
