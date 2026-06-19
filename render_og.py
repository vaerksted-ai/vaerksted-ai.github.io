"""Render the Open Graph social-preview image for vaerksted.ai.

Output: og-image.png (1200x630, the standard size for Facebook/Twitter/LinkedIn).
"""
from PIL import Image, ImageDraw, ImageFont

# ─── Canvas ─────────────────────────────────────────
W, H = 1200, 630
OUT = "/home/user/vaerksted-ai.github.io"
VOID = (11, 13, 17)        # #0B0D11
FROST = (237, 239, 243)    # #EDEFF3
MIST = (139, 147, 159)     # #8B939F
SIGNAL = (108, 140, 255)   # #6C8CFF

img = Image.new("RGB", (W, H), VOID)
draw = ImageDraw.Draw(img, "RGBA")

# ─── Blueprint grid (fades out toward the bottom) ───
grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(grid)
step = 72
for x in range(0, W + 1, step):
    gd.line((x, 0, x, H), fill=(FROST[0], FROST[1], FROST[2], 18), width=1)
for y in range(0, H + 1, step):
    gd.line((0, y, W, y), fill=(FROST[0], FROST[1], FROST[2], 18), width=1)
# Vertical alpha fade mask: opaque at top, transparent toward bottom
fade = Image.new("L", (W, H), 0)
fd = ImageDraw.Draw(fade)
for y in range(H):
    a = max(0, int(255 * (1 - y / (H * 0.7))))
    fd.line((0, y, W, y), fill=a)
grid.putalpha(Image.composite(grid.getchannel("A"), Image.new("L", (W, H), 0), fade))
img = Image.alpha_composite(img.convert("RGBA"), grid).convert("RGB")
draw = ImageDraw.Draw(img, "RGBA")

# ─── Signal glow (soft radial highlights) ───────────
overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
od = ImageDraw.Draw(overlay)
for r in range(620, 0, -16):
    a = int(34 * (1 - r / 620))
    od.ellipse((240 - r, 20 - r, 240 + r, 20 + r),
               fill=(SIGNAL[0], SIGNAL[1], SIGNAL[2], a))
for r in range(480, 0, -16):
    a = int(18 * (1 - r / 480))
    od.ellipse((1140 - r, 60 - r, 1140 + r, 60 + r),
               fill=(SIGNAL[0], SIGNAL[1], SIGNAL[2], a))
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


# ─── Eyebrow ────────────────────────────────────────
EYEBROW_Y = 90
draw.line((80, EYEBROW_Y, 112, EYEBROW_Y), fill=SIGNAL, width=2)
draw_tracked((128, EYEBROW_Y - 11), "A WORKSHOP OF BUILDERS", eyebrow_font, SIGNAL, 3)

# ─── Wordmark: V æ rksted ───────────────────────────
WORDMARK_Y = 150
x = 74

draw.text((x, WORDMARK_Y), "V", fill=FROST, font=wordmark_font)
v_bbox = wordmark_font.getbbox("V")
x += (v_bbox[2] - v_bbox[0]) - 6

draw.text((x, WORDMARK_Y), "æ", fill=SIGNAL, font=wordmark_font)
ae_bbox = wordmark_font.getbbox("æ")
x += (ae_bbox[2] - ae_bbox[0]) - 6

draw.text((x, WORDMARK_Y), "rksted", fill=FROST, font=wordmark_font)

# ─── Tagline ────────────────────────────────────────
draw.text((80, 446), "We build AI-native apps. On principle.", fill=FROST, font=tagline_font)

# ─── Footer rule + meta ─────────────────────────────
draw.line((80, 540, 1120, 540), fill=(FROST[0], FROST[1], FROST[2], 30), width=1)
draw_tracked((80, 570), "VAERKSTED.AI  ·  KØBENHAVN  ·  EST. MMXXVI", footer_font, MIST, 2)

# ─── Save ───────────────────────────────────────────
img.save(f"{OUT}/og-image.png", "PNG", optimize=True)
print("OG image saved: 1200x630")
