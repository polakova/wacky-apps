#!/usr/bin/env python3
"""Generate a launcher icon for one Wacky App.

Usage: make_icon.py <slug> <emoji> <fallback_label> <res_dir>

Draws the app's emoji on a colored rounded tile. If the color-emoji font
isn't available (or rendering fails), falls back to a bold label on the tile —
either way every app gets a distinct icon. Writes ic_launcher.png +
ic_launcher_round.png into all mipmap density folders.
"""
import sys, os
from PIL import Image, ImageDraw, ImageFont

slug, emoji, fallback, res_dir = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]

PALETTE = ["#ff5da2", "#7b2ff7", "#16e0bd", "#ffd23f", "#ff7a45", "#3a86ff", "#1a1623"]
def stable(s):  # deterministic (unlike hash())
    return sum(ord(c) * (i + 1) for i, c in enumerate(s))
bg = PALETTE[stable(slug) % len(PALETTE)]

M = 432  # master size (xxxhdpi-ish, downscaled to other densities)
img = Image.new("RGBA", (M, M), (0, 0, 0, 0))
d = ImageDraw.Draw(img)
# rounded tile + chunky outline (matches the site's neo-retro look)
d.rounded_rectangle([16, 16, M - 16, M - 16], radius=92, fill=bg, outline="#1a1623", width=14)

EMOJI_FONTS = [
    "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf",
    "/System/Library/Fonts/Apple Color Emoji.ttc",
]

def draw_emoji():
    path = next((p for p in EMOJI_FONTS if os.path.exists(p)), None)
    if not path:
        return False
    font = ImageFont.truetype(path, 109)  # NotoColorEmoji ships a 109px bitmap strike
    layer = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.text((100, 100), emoji, font=font, embedded_color=True, anchor="mm")
    bbox = layer.getbbox()
    if not bbox:
        return False
    g = layer.crop(bbox)
    scale = 248 / max(g.width, g.height)
    g = g.resize((max(1, int(g.width * scale)), max(1, int(g.height * scale))), Image.LANCZOS)
    img.alpha_composite(g, ((M - g.width) // 2, (M - g.height) // 2))
    return True

ok = False
try:
    ok = draw_emoji()
except Exception as e:
    sys.stderr.write("emoji render failed (%s); using label fallback\n" % e)

if not ok:
    # fallback: bold short label centered
    txt = (fallback or slug[:2]).upper()[:4]
    size = 200 if len(txt) <= 2 else 150
    try:
        f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
    except Exception:
        f = ImageFont.load_default()
    d.text((M / 2, M / 2), txt, font=f, fill="#ffffff", anchor="mm")

DENSITIES = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}
for dens, px in DENSITIES.items():
    out = os.path.join(res_dir, "mipmap-" + dens)
    os.makedirs(out, exist_ok=True)
    scaled = img.resize((px, px), Image.LANCZOS)
    scaled.save(os.path.join(out, "ic_launcher.png"))
    scaled.save(os.path.join(out, "ic_launcher_round.png"))

print("icon: %s (%s) %s" % (slug, emoji, "emoji" if ok else "label"))
