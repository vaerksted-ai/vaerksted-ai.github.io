"""Render the Open Graph social-preview image for vaerksted.ai.

Output: og-image.png (1200x630, the standard size for Facebook/Twitter/LinkedIn).
Asgardian theme: cosmos + gold + the Bifröst.
"""
import random
from PIL import Image, ImageDraw, ImageFont

# ─── Canvas ─────────────────────────────────────────
W, H = 1200, 630
OUT = "/home/user/vaerksted-ai.github.io"
VOID = (7, 8, 13)          # #07080D
FROST = (237, 239, 243)    # #EDEFF3
MIST = (139, 147, 159)     # #8B939F
GOLD = (232, 200, 121)     # #E8C879

# Bifröst — the rainbow bridge Heimdal guards (one hue per app).
BIFROST = [
    (0.00, (242, 109, 109)),  # red
    (0.22, (242, 163, 60)),   # amber
    (0.44, (79, 208, 138)),   # green
    (0.64, (56, 197, 224)),   # cyan
    (0.82, (91, 141, 239)),   # blue
    (1.00, (176, 124, 246)),  # violet
]
# Polished Asgardian gold (vertical sheen).
GOLD_METAL = [
    (0.00, (247, 231, 176)),
    (0.38, (230, 197, 111)),
    (0.52, (184, 137, 58)),
    (0.72, (235, 208, 131)),
    (1.00, (247, 231, 176)),
]


def _sample(stops, t):
    t = max(0.0, min(1.0, t))
    for i in range(len(stops) - 1):
        t0, c0 = stops[i]
        t1, c1 = stops[i + 1]
        if t0 <= t <= t1:
            f = (t - t0) / (t1 - t0)
            return tuple(round(c0[k] + (c1[k] - c0[k]) * f) for k in range(3))
    return stops[-1][1]


def bifrost_color(t):
    return _sample(BIFROST, t)


def bifrost_span(x0, x1):
    """Full-canvas image whose rainbow runs across [x0, x1] horizontally."""
    grad = Image.new("RGB", (W, H))
    px = grad.load()
    for x in range(W):
        col = bifrost_color((x - x0) / max(1.0, (x1 - x0)))
        for y in range(H):
            px[x, y] = col
    return grad


def gold_vspan(y0, y1):
    """Full-canvas image with a vertical gold sheen across [y0, y1]."""
    grad = Image.new("RGB", (W, H))
    px = grad.load()
    for y in range(H):
        col = _sample(GOLD_METAL, (y - y0) / max(1.0, (y1 - y0)))
        for x in range(W):
            px[x, y] = col
    return grad


# ─── Cosmic backdrop (indigo glow over the void) ────
img = Image.new("RGB", (W, H), VOID)
draw = ImageDraw.Draw(img, "RGBA")
cosmos = Image.new("RGBA", (W, H), (0, 0, 0, 0))
cd = ImageDraw.Draw(cosmos)
for r in range(820, 0, -10):
    a = int(60 * (1 - r / 820))
    cd.ellipse((600 - r, -120 - r, 600 + r, -120 + r), fill=(26, 23, 51, a))  # #1A1733
img = Image.alpha_composite(img.convert("RGBA"), cosmos).convert("RGB")
draw = ImageDraw.Draw(img, "RGBA")

# ─── Starfield ──────────────────────────────────────
random.seed(42)
for _ in range(150):
    sx, sy = random.uniform(0, W), random.uniform(0, H)
    rad = random.uniform(0.5, 1.6)
    a = int(random.uniform(45, 200))
    draw.ellipse((sx - rad, sy - rad, sx + rad, sy + rad), fill=(*FROST, a))
for _ in range(28):  # gold embers
    sx, sy = random.uniform(0, W), random.uniform(0, H * 0.7)
    rad = random.uniform(0.8, 1.7)
    a = int(random.uniform(70, 190))
    draw.ellipse((sx - rad, sy - rad, sx + rad, sy + rad), fill=(*GOLD, a))

# ─── Faint etched grid (fades toward the bottom) ────
grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(grid)
step = 72
for x in range(0, W + 1, step):
    gd.line((x, 0, x, H), fill=(*GOLD, 12), width=1)
for y in range(0, H + 1, step):
    gd.line((0, y, W, y), fill=(*GOLD, 12), width=1)
fade = Image.new("L", (W, H), 0)
fd = ImageDraw.Draw(fade)
for y in range(H):
    fd.line((0, y, W, y), fill=max(0, int(255 * (1 - y / (H * 0.7)))))
grid.putalpha(Image.composite(grid.getchannel("A"), Image.new("L", (W, H), 0), fade))
img = Image.alpha_composite(img.convert("RGBA"), grid).convert("RGB")
draw = ImageDraw.Draw(img, "RGBA")

# ─── Aurora glow (gold horizon + Bifröst tints) ─────
overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
od = ImageDraw.Draw(overlay)
GLOWS = [
    (600, -20, 560, 30, GOLD),             # gold horizon, centre
    (264, 10, 600, 26, (91, 141, 239)),    # blue
    (1020, 30, 500, 22, (176, 124, 246)),  # violet
]
for cx, cy, rmax, amax, col in GLOWS:
    for r in range(rmax, 0, -16):
        a = int(amax * (1 - r / rmax))
        od.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(col[0], col[1], col[2], a))
img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
draw = ImageDraw.Draw(img, "RGBA")

# ─── Fonts (DejaVu stand-ins; web page uses Space Grotesk + JetBrains Mono) ──
DISPLAY = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
DISPLAY_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
MONO_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

# Size the wordmark so "Værksted" fits the left/right margins (80px each).
WORDMARK = "Værksted"
MAX_W = W - 160
wm_size = 220
while wm_size > 60:
    f = ImageFont.truetype(DISPLAY, wm_size)
    bb = f.getbbox(WORDMARK)
    if (bb[2] - bb[0]) <= MAX_W:
        break
    wm_size -= 2
wordmark_font = ImageFont.truetype(DISPLAY, wm_size)
tagline_font = ImageFont.truetype(DISPLAY_REG, 44)
eyebrow_font = ImageFont.truetype(MONO_REG, 16)
footer_font = ImageFont.truetype(MONO_REG, 14)


def draw_tracked(xy, text, font, fill, track):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, fill=fill, font=font)
        bbox = font.getbbox(ch)
        x += (bbox[2] - bbox[0]) + track
    return x


# ─── Eyebrow (gold text, Bifröst rule) ──────────────
EYEBROW_Y = 90
for i in range(32):
    draw.line((80 + i, EYEBROW_Y - 1, 80 + i, EYEBROW_Y + 1), fill=bifrost_color(i / 31), width=1)
draw_tracked((128, EYEBROW_Y - 11), "A WORKSHOP OF BUILDERS", eyebrow_font, GOLD, 3)

# ─── Wordmark: V æ rksted ───────────────────────────
WORDMARK_Y = 150
y_top, y_bottom = WORDMARK_Y + wm_size * 0.12, WORDMARK_Y + wm_size * 0.92
gold_img = gold_vspan(y_top, y_bottom)
x = 74

# "V" — gold
v_bbox = wordmark_font.getbbox("V")
v_mask = Image.new("L", (W, H), 0)
ImageDraw.Draw(v_mask).text((x, WORDMARK_Y), "V", fill=255, font=wordmark_font)
img.paste(gold_img, (0, 0), v_mask)
x += (v_bbox[2] - v_bbox[0]) - 6

# "æ" — Bifröst rainbow
ae_bbox = wordmark_font.getbbox("æ")
ae_mask = Image.new("L", (W, H), 0)
ImageDraw.Draw(ae_mask).text((x, WORDMARK_Y), "æ", fill=255, font=wordmark_font)
img.paste(bifrost_span(x + ae_bbox[0], x + ae_bbox[2]), (0, 0), ae_mask)
x += (ae_bbox[2] - ae_bbox[0]) - 6

# "rksted" — gold
rk_mask = Image.new("L", (W, H), 0)
ImageDraw.Draw(rk_mask).text((x, WORDMARK_Y), "rksted", fill=255, font=wordmark_font)
img.paste(gold_img, (0, 0), rk_mask)

draw = ImageDraw.Draw(img, "RGBA")

# ─── Tagline ────────────────────────────────────────
draw.text((80, 446), "We build AI-native apps. On principle.", fill=FROST, font=tagline_font)

# ─── Footer rule + meta ─────────────────────────────
draw.line((80, 540, 1120, 540), fill=(*GOLD, 50), width=1)
draw_tracked((80, 570), "VAERKSTED.AI  ·  KØBENHAVN  ·  EST. MMXXVI", footer_font, MIST, 2)

# ─── Save ───────────────────────────────────────────
img.save(f"{OUT}/og-image.png", "PNG", optimize=True)
print("OG image saved: 1200x630")
