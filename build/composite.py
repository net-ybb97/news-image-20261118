#!/usr/bin/env python3
"""Composite the six panel illustrations into the final 1024x1024 entry image.

Layout: bold header (date + title) on top, then a 2x3 grid of panels.
Each panel is a cover-cropped illustration with a caption bar beneath it.
All text is drawn here with PIL -- the generated art contains no text.

Run:  python3 build/composite.py
Out:  assets/day.png  (1024x1024, <= 1 MiB)
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
PANELS_DIR = ROOT / "build" / "panels"
OUT = ROOT / "assets" / "day.png"

FONT_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
FONT_DISPLAY = "/usr/share/fonts/truetype/noto/NotoSansDisplay-Bold.ttf"

W = H = 1024
BG = (10, 22, 38)            # deep navy
PANEL_BG = (16, 34, 56)      # caption bar
ACCENT = (255, 176, 32)      # amber
WHITE = (245, 247, 250)
MUTED = (168, 190, 214)

MARGIN = 16
GAP = 12
HEADER_H = 168
COLS, ROWS = 2, 3

# (panel file, caption) -- captions name what happened, 3-8 words each.
STORIES = [
    ("bridge.png",  "Ukraine strikes Crimean Bridge"),
    ("radar.png",   "Iran hits Bahrain radar; US strikes back"),
    ("crash.png",   "Russian plane crash in Siberia kills 19"),
    ("quad.png",    "Quad leaders gather in Manila"),
    ("nvidia.png",  "Nvidia beats estimates, bars Huang return"),
    ("measles.png", "US loses measles-free status"),
]

CAPTION_H = 66


def cover_crop(img: Image.Image, tw: int, th: int) -> Image.Image:
    """Resize + center-crop img to exactly tw x th (cover behaviour)."""
    scale = max(tw / img.width, th / img.height)
    nw, nh = round(img.width * scale), round(img.height * scale)
    img = img.resize((nw, nh), Image.LANCZOS)
    x = (nw - tw) // 2
    y = (nh - th) // 2
    return img.crop((x, y, x + tw, y + th))


def fit_font(draw: ImageDraw.ImageDraw, text: str, path: str,
             start: int, max_width: int) -> ImageFont.FreeTypeFont:
    size = start
    while size > 12:
        font = ImageFont.truetype(path, size)
        if draw.textlength(text, font=font) <= max_width:
            return font
        size -= 2
    return ImageFont.truetype(path, size)


def wrap(draw: ImageDraw.ImageDraw, text: str, font, max_width: int):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=font) <= max_width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def main() -> None:
    canvas = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(canvas)

    # ---- header ------------------------------------------------------
    date_font = ImageFont.truetype(FONT_DISPLAY, 74)
    title_font = ImageFont.truetype(FONT_BOLD, 30)
    sub_font = ImageFont.truetype(FONT_BOLD, 20)

    date_text = "18 NOVEMBER 2026"
    tw = draw.textlength(date_text, font=date_font)
    draw.text(((W - tw) / 2, 12), date_text, font=date_font, fill=WHITE)

    title_text = "THE WORLD ON 18 NOVEMBER 2026"
    tw = draw.textlength(title_text, font=title_font)
    draw.text(((W - tw) / 2, 98), title_text, font=title_font, fill=ACCENT)

    sub_text = "THE DAY IN SIX STORIES"
    tw = draw.textlength(sub_text, font=sub_font)
    draw.text(((W - tw) / 2, 134), sub_text, font=sub_font, fill=MUTED)

    draw.line([(MARGIN, HEADER_H - 2), (W - MARGIN, HEADER_H - 2)],
              fill=ACCENT, width=3)

    # ---- grid --------------------------------------------------------
    grid_top = HEADER_H + 8
    cell_w = (W - 2 * MARGIN - (COLS - 1) * GAP) // COLS
    cell_h = (H - grid_top - MARGIN - (ROWS - 1) * GAP) // ROWS
    img_h = cell_h - CAPTION_H

    for i, (fname, caption) in enumerate(STORIES):
        r, c = divmod(i, COLS)
        x = MARGIN + c * (cell_w + GAP)
        y = grid_top + r * (cell_h + GAP)

        art = Image.open(PANELS_DIR / fname).convert("RGB")
        art = cover_crop(art, cell_w, img_h)
        canvas.paste(art, (x, y))

        bar_y = y + img_h
        draw.rectangle([x, bar_y, x + cell_w, bar_y + CAPTION_H],
                       fill=PANEL_BG)
        font = fit_font(draw, caption, FONT_BOLD, 30, cell_w - 20)
        lines = wrap(draw, caption, font, cell_w - 20)
        line_h = font.size + 4
        total_h = line_h * len(lines) - 4
        ty = bar_y + (CAPTION_H - total_h) // 2
        for line in lines:
            lw = draw.textlength(line, font=font)
            draw.text((x + (cell_w - lw) / 2, ty), line,
                      font=font, fill=WHITE)
            ty += line_h

    OUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(OUT, format="PNG", optimize=True)
    size = OUT.stat().st_size
    print(f"saved {OUT}  {canvas.size}  {size} bytes")

    if size > 1_048_576:
        q = canvas.quantize(colors=256, method=Image.MEDIANCUT)
        q.save(OUT, format="PNG", optimize=True)
        size = OUT.stat().st_size
        print(f"quantized -> {size} bytes")
    assert size <= 1_048_576, f"still too big: {size}"


if __name__ == "__main__":
    main()
