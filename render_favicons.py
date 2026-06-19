"""Render the favicon family: apple-touch-icon.png (180x180) and favicon.ico (multi-size)."""
from PIL import Image, ImageDraw, ImageFont

OUT = "/home/user/vaerksted-ai.github.io"
PANEL = (17, 20, 26)      # #11141A
SIGNAL = (108, 140, 255)  # #6C8CFF
# Geometric grotesk stand-in for Space Grotesk (the web page uses the real face).
DISPLAY = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def render_ae(size: int, corner_radius_ratio: float = 0.18) -> Image.Image:
    """Render a square Æ favicon at the given size."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Rounded panel background
    radius = int(size * corner_radius_ratio)
    draw.rounded_rectangle((0, 0, size - 1, size - 1), radius=radius, fill=PANEL)

    # æ centered, sized to fit, in signal blue
    font_size = int(size * 0.64)
    font = ImageFont.truetype(DISPLAY, font_size)
    bbox = font.getbbox("æ")
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    # Center using the bbox offset
    x = (size - text_w) / 2 - bbox[0]
    y = (size - text_h) / 2 - bbox[1] - size * 0.03  # slight optical lift
    draw.text((x, y), "æ", fill=SIGNAL, font=font)

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
