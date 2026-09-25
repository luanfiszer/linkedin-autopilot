#!/usr/bin/env python3
"""Gera imagens-ilustração para os posts: cartão de código e diagrama simples.

As imagens têm cara de ilustração técnica, não de foto nem de print real.
Nunca use isto para simular um print (terminal, tela, resultado de teste):
print falso é enganoso. Print de verdade, só o Luan manda.

Uso
  python scripts/gerar_imagem.py codigo exemplo.cs --lang csharp \\
      --titulo "OutboxWorker.cs" -o media/fotos/gerado-outbox-codigo.png
  python scripts/gerar_imagem.py diagrama fluxo.yml -o media/fotos/gerado-outbox-fluxo.png

Formato do diagrama (YAML):
  titulo: Outbox Pattern
  caixas: [API grava dados + evento, Tabela outbox, Worker em background, RabbitMQ]
  setas: [mesma transação, lê pendentes, publica]   # opcional, uma a menos que caixas
  destaque: 1          # opcional: índice da caixa em destaque (0 = primeira)
  nota: O evento só sai da tabela depois de publicado.   # opcional

Dependências: pillow, pygments (requirements-images.txt). Fontes: usa DejaVu
(Linux), Menlo/SF (macOS) ou as que vêm com o matplotlib, se instalado.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent

MONO_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "/usr/share/fonts/dejavu/DejaVuSansMono.ttf",
    "/System/Library/Fonts/Menlo.ttc",
]
SANS_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/dejavu/DejaVuSans.ttf",
    "/System/Library/Fonts/SFNS.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
]
SANS_BOLD_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
    "/System/Library/Fonts/SFNS.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
]

# Paleta sóbria (fundo escuro, um acento). Nada de gradiente "de IA".
BG = (22, 27, 34)
CARD = (13, 17, 23)
BORDER = (48, 54, 61)
TEXT = (230, 237, 243)
MUTED = (139, 148, 158)
ACCENT = (88, 166, 255)
BOX = (33, 38, 45)


def _font(candidates, mpl_name, size):
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    try:
        import matplotlib
        p = Path(matplotlib.get_data_path()) / "fonts" / "ttf" / mpl_name
        if p.exists():
            return ImageFont.truetype(str(p), size)
    except ImportError:
        pass
    sys.exit("Nenhuma fonte TrueType encontrada. Instale o pacote fonts-dejavu "
             "ou `pip install matplotlib` (que traz a DejaVu).")


def mono(size):
    return _font(MONO_CANDIDATES, "DejaVuSansMono.ttf", size)


def sans(size, bold=False):
    if bold:
        return _font(SANS_BOLD_CANDIDATES, "DejaVuSans-Bold.ttf", size)
    return _font(SANS_CANDIDATES, "DejaVuSans.ttf", size)


# --- cartão de código ---------------------------------------------------------
def render_code(code: str, lang: str, title: str | None, out: Path) -> Path:
    from pygments import lex
    from pygments.lexers import get_lexer_by_name
    from pygments.styles import get_style_by_name

    style = get_style_by_name("github-dark")
    lexer = get_lexer_by_name(lang)
    code = code.expandtabs(4).rstrip("\n")
    lines = code.split("\n")
    if len(lines) > 30:
        sys.exit(f"Código com {len(lines)} linhas; máximo 30. Corte até o essencial.")

    f = mono(30)
    ascent, descent = f.getmetrics()
    line_h = int((ascent + descent) * 1.45)
    char_w = f.getlength("M")
    gutter = char_w * (len(str(len(lines))) + 2)
    code_w = max(f.getlength(l) for l in lines) if lines else 0

    pad, bar_h = 56, 64
    card_w = int(max(1000, gutter + code_w + pad * 2))
    card_h = int(bar_h + pad * 0.6 + line_h * len(lines) + pad)
    margin = 64
    W, H = card_w + margin * 2, card_h + margin * 2

    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    x0, y0 = margin, margin
    d.rounded_rectangle([x0, y0, x0 + card_w, y0 + card_h], radius=18, fill=CARD, outline=BORDER, width=2)
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        cx, cy = x0 + 32 + i * 30, y0 + bar_h // 2
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=c)
    if title:
        tf = sans(24)
        d.text((x0 + card_w / 2, y0 + bar_h / 2), title, font=tf, fill=MUTED, anchor="mm")
    d.line([x0, y0 + bar_h, x0 + card_w, y0 + bar_h], fill=BORDER, width=2)

    def color(ttype):
        while ttype is not None:
            s = style.style_for_token(ttype)
            if s["color"]:
                h = s["color"]
                return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
            ttype = ttype.parent
        return TEXT

    y = y0 + bar_h + pad * 0.6
    tokens = list(lex(code + "\n", lexer))
    x = x0 + pad + gutter
    lineno = 1
    d.text((x0 + pad, y), f"{lineno:>{len(str(len(lines)))}}", font=f, fill=BORDER)
    for ttype, value in tokens:
        parts = value.split("\n")
        for j, part in enumerate(parts):
            if j > 0:
                y += line_h
                x = x0 + pad + gutter
                lineno += 1
                if lineno <= len(lines):
                    d.text((x0 + pad, y), f"{lineno:>{len(str(len(lines)))}}", font=f, fill=BORDER)
            if part:
                d.text((x, y), part, font=f, fill=color(ttype))
                x += f.getlength(part)
    return _save(img, out)


# --- diagrama -----------------------------------------------------------------
def _wrap(d, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if d.textlength(test, font=font) <= max_w or not cur:
            cur = test
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def render_diagram(spec: dict, out: Path) -> Path:
    boxes = [str(b) for b in spec.get("caixas", [])]
    if not 2 <= len(boxes) <= 5:
        sys.exit("O diagrama precisa de 2 a 5 caixas.")
    arrows = [str(a) for a in spec.get("setas", [])]
    if arrows and len(arrows) != len(boxes) - 1:
        sys.exit("setas precisa ter uma a menos que caixas.")
    hi = spec.get("destaque")

    W, H = 1600, 900
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    tf, af, nf = sans(52, bold=True), sans(24), sans(28)

    if spec.get("titulo"):
        d.text((W / 2, 110), str(spec["titulo"]), font=tf, fill=TEXT, anchor="mm")

    n = len(boxes)
    gap = 110
    box_w = (W - 160 - gap * (n - 1)) / n
    box_h = 260
    top = (H - box_h) / 2 + 20
    for i, label in enumerate(boxes):
        x = 80 + i * (box_w + gap)
        outline = ACCENT if hi == i else BORDER
        d.rounded_rectangle([x, top, x + box_w, top + box_h], radius=22, fill=BOX,
                            outline=outline, width=4 if hi == i else 2)
        size = 32
        while True:  # diminui a fonte até a palavra mais longa caber na caixa
            bf = sans(size)
            lines = _wrap(d, label, bf, box_w - 40)
            if max(d.textlength(ln, font=bf) for ln in lines) <= box_w - 30 or size <= 18:
                break
            size -= 2
        lh = int(size * 1.4)
        y = top + box_h / 2 - (len(lines) - 1) * lh / 2
        for ln in lines:
            d.text((x + box_w / 2, y), ln, font=bf, fill=TEXT, anchor="mm")
            y += lh
        if i < n - 1:
            ax0, ax1, ay = x + box_w + 14, x + box_w + gap - 14, top + box_h / 2
            d.line([ax0, ay, ax1 - 10, ay], fill=ACCENT, width=5)
            d.polygon([(ax1, ay), (ax1 - 22, ay - 13), (ax1 - 22, ay + 13)], fill=ACCENT)
            if arrows:
                alines = _wrap(d, arrows[i], af, gap + box_w * 0.6)
                yy = top - 34 - (len(alines) - 1) * 30
                for ln in alines:
                    d.text(((ax0 + ax1) / 2, yy), ln, font=af, fill=MUTED, anchor="mm")
                    yy += 30
    if spec.get("nota"):
        d.text((W / 2, H - 110), str(spec["nota"]), font=nf, fill=MUTED, anchor="mm")
    return _save(img, out)


def _save(img: Image.Image, out: Path) -> Path:
    out = Path(out)
    if not out.name.startswith("gerado-"):
        out = out.with_name("gerado-" + out.name)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG", optimize=True)  # PNG do Pillow não leva EXIF
    return out


def main():
    ap = argparse.ArgumentParser(description="Gera cartão de código ou diagrama para post.")
    sub = ap.add_subparsers(dest="modo", required=True)
    c = sub.add_parser("codigo", help="cartão de código (código genérico, escrito do zero)")
    c.add_argument("arquivo", help="arquivo com o código, ou - para stdin")
    c.add_argument("--lang", required=True, help="linguagem do Pygments: csharp, python, sql, json...")
    c.add_argument("--titulo", help="texto da barra do cartão, ex.: OutboxWorker.cs")
    c.add_argument("-o", "--out", required=True)
    g = sub.add_parser("diagrama", help="diagrama de 2 a 5 caixas a partir de um YAML")
    g.add_argument("arquivo", help="arquivo YAML, ou - para stdin")
    g.add_argument("-o", "--out", required=True)
    args = ap.parse_args()

    src = sys.stdin.read() if args.arquivo == "-" else Path(args.arquivo).read_text(encoding="utf-8")
    if args.modo == "codigo":
        path = render_code(src, args.lang, args.titulo, args.out)
    else:
        path = render_diagram(yaml.safe_load(src) or {}, args.out)
    w, h = Image.open(path).size
    print(f"{path} ({w}x{h}, {path.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
