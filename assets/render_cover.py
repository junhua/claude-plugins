"""Render the marketplace catalogue frontispiece.

Shares the Orbital Cadence visual language with super-ralph's teaser but
reframes the composition as a library frontispiece rather than a single
instrument. One plate, centered, with catalogue apparatus around it.
"""
from PIL import Image, ImageDraw, ImageFont
import math
import os

W, H = 1280, 640
CX, CY = 640, 320

PAPER = (244, 241, 234)
INK = (14, 26, 43)
ACCENT = (200, 85, 61)

FONT_DIR = (
    "/Users/junhua/.claude/plugins/cache/anthropic-agent-skills/"
    "document-skills/12ab35c2eb56/skills/canvas-design/canvas-fonts"
)
DISPLAY = os.path.join(FONT_DIR, "BigShoulders-Bold.ttf")
MONO = os.path.join(FONT_DIR, "IBMPlexMono-Regular.ttf")
MONO_BOLD = os.path.join(FONT_DIR, "IBMPlexMono-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "IBMPlexSerif-Regular.ttf")

PLATE_LEFT = 340
PLATE_RIGHT = 940
PLATE_TOP = 110
PLATE_BOTTOM = 540

DIAL_CX = 440
DIAL_CY = 320
DIAL_RINGS = [44, 78, 112, 142]

ENTRIES = [
    ("I",   "super-ralph",   "autonomous dev workflow",   "active"),
    ("II",  "—",             "reserved",                  "vacant"),
    ("III", "—",             "reserved",                  "vacant"),
    ("IV",  "—",             "reserved",                  "vacant"),
]


def polar(cx: float, cy: float, r: float, a: float) -> tuple[float, float]:
    return cx + r * math.cos(a), cy + r * math.sin(a)


def paste_rotated_text(
    base: Image.Image,
    text: str,
    font: ImageFont.FreeTypeFont,
    cx: float, cy: float,
    rotation_deg: float,
    color: tuple = INK,
) -> None:
    tmp_draw = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    bbox = tmp_draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pad = 10
    layer = Image.new("RGBA", (tw + pad * 2, th + pad * 2), (0, 0, 0, 0))
    ldraw = ImageDraw.Draw(layer)
    ldraw.text((pad - bbox[0], pad - bbox[1]), text, font=font, fill=color + (255,))
    rotated = layer.rotate(-rotation_deg, expand=True, resample=Image.BICUBIC)
    px = int(cx - rotated.width / 2)
    py = int(cy - rotated.height / 2)
    base.paste(rotated, (px, py), rotated)


def draw_frame(draw: ImageDraw.ImageDraw) -> None:
    draw.line([60, 40, W - 60, 40], fill=INK, width=1)
    draw.line([60, H - 40, W - 60, H - 40], fill=INK, width=1)
    draw.line([60, 40, 60, H - 40], fill=INK, width=1)
    draw.line([W - 60, 40, W - 60, H - 40], fill=INK, width=1)
    draw.line([80, 60, W - 80, 60], fill=INK, width=1)
    draw.line([80, H - 60, W - 80, H - 60], fill=INK, width=1)


def draw_plate(draw: ImageDraw.ImageDraw) -> None:
    draw.line([PLATE_LEFT, PLATE_TOP, PLATE_RIGHT, PLATE_TOP], fill=INK, width=2)
    draw.line([PLATE_LEFT, PLATE_BOTTOM, PLATE_RIGHT, PLATE_BOTTOM], fill=INK, width=2)
    draw.line([PLATE_LEFT, PLATE_TOP, PLATE_LEFT, PLATE_BOTTOM], fill=INK, width=2)
    draw.line([PLATE_RIGHT, PLATE_TOP, PLATE_RIGHT, PLATE_BOTTOM], fill=INK, width=2)
    draw.line([PLATE_LEFT + 10, PLATE_TOP + 10, PLATE_RIGHT - 10, PLATE_TOP + 10],
              fill=INK, width=1)
    draw.line([PLATE_LEFT + 10, PLATE_BOTTOM - 10, PLATE_RIGHT - 10, PLATE_BOTTOM - 10],
              fill=INK, width=1)


def draw_dial(draw: ImageDraw.ImageDraw) -> None:
    for r in DIAL_RINGS:
        draw.ellipse([DIAL_CX - r, DIAL_CY - r, DIAL_CX + r, DIAL_CY + r],
                     outline=INK, width=1)
    for i in range(24):
        a = -math.pi / 2 + i * (2 * math.pi / 24)
        x1, y1 = polar(DIAL_CX, DIAL_CY, DIAL_RINGS[2], a)
        r2 = DIAL_RINGS[3] if (i % 6 == 0) else (DIAL_RINGS[2] + 8)
        x2, y2 = polar(DIAL_CX, DIAL_CY, r2, a)
        draw.line([x1, y1, x2, y2], fill=INK, width=2 if (i % 6 == 0) else 1)

    a_build = -math.pi / 2 + 2 * (2 * math.pi / 8)
    x1, y1 = polar(DIAL_CX, DIAL_CY, DIAL_RINGS[2], a_build)
    x2, y2 = polar(DIAL_CX, DIAL_CY, DIAL_RINGS[3] + 10, a_build)
    draw.line([x1, y1, x2, y2], fill=ACCENT, width=2)
    mx, my = polar(DIAL_CX, DIAL_CY, DIAL_RINGS[3] + 18, a_build)
    draw.ellipse([mx - 4, my - 4, mx + 4, my + 4], fill=ACCENT)


def draw_index(base: Image.Image) -> None:
    d = ImageDraw.Draw(base)
    mono = ImageFont.truetype(MONO, 12)
    mono_bold = ImageFont.truetype(MONO_BOLD, 12)

    col_x = 600
    row_y = 170
    row_h = 42

    header_y = row_y - 26
    d.text((col_x, header_y), "no.", font=mono_bold, fill=INK)
    d.text((col_x + 50, header_y), "instrument", font=mono_bold, fill=INK)
    d.text((col_x + 200, header_y), "status", font=mono_bold, fill=INK)
    d.line([col_x, header_y + 18, PLATE_RIGHT - 30, header_y + 18], fill=INK, width=1)

    for i, (numeral, name, desc, status) in enumerate(ENTRIES):
        y = row_y + i * row_h
        d.text((col_x, y), numeral, font=mono_bold, fill=INK)
        d.text((col_x + 50, y), name, font=mono, fill=INK)
        d.text((col_x + 50, y + 16), desc, font=ImageFont.truetype(MONO, 10), fill=INK)
        if status == "active":
            d.ellipse([col_x + 200, y + 4, col_x + 208, y + 12], fill=ACCENT)
            d.text((col_x + 216, y), status, font=mono, fill=INK)
        else:
            d.text((col_x + 200, y), status, font=ImageFont.truetype(MONO, 11), fill=INK)
        if i < len(ENTRIES) - 1:
            d.line([col_x, y + row_h - 4, PLATE_RIGHT - 30, y + row_h - 4],
                   fill=INK, width=1)


def draw_corner_plate(base: Image.Image) -> None:
    d = ImageDraw.Draw(base)
    mono = ImageFont.truetype(MONO, 11)
    mono_bold = ImageFont.truetype(MONO_BOLD, 10)
    d.line([80, 88, 220, 88], fill=INK, width=1)
    d.text((80, 70), "CATALOGUE  NO. I", font=mono_bold, fill=INK)
    d.text((80, 94), "junhua  /  plugins", font=mono, fill=INK)

    right_label = "A  MARKETPLACE  OF  INSTRUMENTS"
    bbox = d.textbbox((0, 0), right_label, font=mono_bold)
    rw = bbox[2] - bbox[0]
    d.text((W - 80 - rw, 76), right_label, font=mono_bold, fill=INK)
    d.line([W - 80 - rw, 94, W - 80, 94], fill=INK, width=1)


def draw_display_word(base: Image.Image) -> None:
    d = ImageDraw.Draw(base)
    font = ImageFont.truetype(DISPLAY, 58)
    text = "JUNHUA · PLUGINS"
    bbox = d.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = (W - tw) / 2
    ty = H - 128

    pad_x, pad_y = 30, 14
    well = [
        tx - pad_x, ty - pad_y,
        tx + tw + pad_x, ty + th + pad_y,
    ]
    d.rectangle(well, fill=PAPER)
    d.line([well[0], well[1], well[2], well[1]], fill=INK, width=1)
    d.line([well[0], well[3], well[2], well[3]], fill=INK, width=1)
    d.text((tx - bbox[0], ty - bbox[1]), text, font=font, fill=INK)

    sub_font = ImageFont.truetype(MONO, 12)
    subtitle = "A   CLAUDE   CODE   MARKETPLACE"
    sb = d.textbbox((0, 0), subtitle, font=sub_font)
    sw = sb[2] - sb[0]
    d.text(((W - sw) / 2, H - 82), subtitle, font=sub_font, fill=INK)


def render() -> None:
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    draw_frame(draw)
    draw_plate(draw)
    draw_dial(draw)
    draw_index(img)
    draw_corner_plate(img)
    draw_display_word(img)

    out = "/Users/junhua/Workspace/claude-plugins/assets/teaser.png"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out} ({W}x{H})")


if __name__ == "__main__":
    render()
