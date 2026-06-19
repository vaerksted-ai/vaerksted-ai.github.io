"""Render the favicon family: apple-touch-icon.png (180x180) and favicon.ico (multi-size)."""
from PIL import Image, ImageDraw, ImageFont

OUT = "/home/user/vaerksted-ai.github.io"
PANEL = (17, 20, 26)      # #11141A
# Geometric grotesk stand-in for Space Grotesk (the web page uses the real face).
DISPLAY = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# Bifröst — the rainbow bridge Heimdal guards (one hue per app).
BIFROST = [
    (0.00, (242, 109, 109)),  # red
    (0.22, (242, 163, 60)),   # amber
    (0.44, (79, 208, 138)),   # green
    (0.64, (56, 197, 224)),   # cyan
    (0.82, (91, 141, 239)),   # blue
    (1.00, (176, 124, 246)),  # violet
]


def bifrost_color(t: float):
    """Sample the Bifröst gradient at t in [0, 1]."""
    t = max(0.0, min(1.0, t))
    for i in range(len(BIFROST) - 1):
        t0, c0 = BIFROST[i]
        t1, c1 = BIFROST[i + 1]
        if t0 <= t <= t1:
            f = (t - t0) / (t1 - t0)
            return tuple(round(c0[k] + (c1[k] - c0[k]) * f) for k in range(3))
    return BIFROST[-1][1]


def bifrost_gradient(w: int, h: int, x0: float = None, x1: float = None) -> Image.Image:
    """Rainbow gradient image, w×h, running across [x0, x1] (defaults to full width)."""
    if x0 is None:
        x0, x1 = 0, w - 1
    grad = Image.new("RGB", (w, h))
    px = grad.load()
    for x in range(w):
        col = bifrost_color((x - x0) / max(1.0, (x1 - x0)))
        for y in range(h):
            px[x, y] = col
    return grad


def render_ae(size: int, corner_radius_ratio: float = 0.18) -> Image.Image:
    """Render a square Æ favicon at the given size."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Rounded panel background
    radius = int(size * corner_radius_ratio)
    draw.rounded_rectangle((0, 0, size - 1, size - 1), radius=radius, fill=PANEL)

    # æ centered, sized to fit, painted with the Bifröst gradient
    font_size = int(size * 0.64)
    font = ImageFont.truetype(DISPLAY, font_size)
    bbox = font.getbbox("æ")
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x = (size - text_w) / 2 - bbox[0]
    y = (size - text_h) / 2 - bbox[1] - size * 0.03  # slight optical lift

    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).text((x, y), "æ", fill=255, font=font)
    # Span the rainbow across the glyph itself so the full red→violet shows.
    grad = bifrost_gradient(size, size, x + bbox[0], x + bbox[2]).convert("RGBA")
    img.paste(grad, (0, 0), mask)

    return img


# Apple touch icon (180x180, used by iOS for home-screen bookmarks)
apple = render_ae(180)
apple.convert("RGB").save(f"{OUT}/apple-touch-icon.png", "PNG", optimize=True)

# Standard favicon.ico — multi-size embedded
sizes = [16, 32, 48, 64]
images = [render_ae(s) for s in sizes]
images[0].save(
    f"{OUT}/favicon.ico",
    format="ICO",
    sizes=[(s, s) for s in sizes],
    append_images=images[1:],
)

# PNG variants people sometimes link explicitly
render_ae(192).convert("RGB").save(f"{OUT}/icon-192.png", "PNG", optimize=True)
render_ae(512).convert("RGB").save(f"{OUT}/icon-512.png", "PNG", optimize=True)

print("Favicons rendered: apple-touch-icon.png, favicon.ico, icon-192.png, icon-512.png")
