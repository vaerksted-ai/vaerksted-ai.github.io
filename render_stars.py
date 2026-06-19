"""Generate stars.svg — a cosmic starfield backdrop (Asgard floats in the void)."""
import random

W, H = 1600, 1000
random.seed(42)  # deterministic field

stars = []
# Faint white dust
for _ in range(260):
    x = round(random.uniform(0, W), 1)
    y = round(random.uniform(0, H), 1)
    r = round(random.uniform(0.4, 1.3), 2)
    o = round(random.uniform(0.18, 0.7), 2)
    stars.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#EDEFF3" opacity="{o}"/>')
# A few brighter, larger stars
for _ in range(26):
    x = round(random.uniform(0, W), 1)
    y = round(random.uniform(0, H), 1)
    r = round(random.uniform(1.3, 2.1), 2)
    o = round(random.uniform(0.55, 0.95), 2)
    stars.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFFFFF" opacity="{o}"/>')
# Scattered Asgardian gold embers
for _ in range(22):
    x = round(random.uniform(0, W), 1)
    y = round(random.uniform(0, H * 0.7), 1)
    r = round(random.uniform(0.8, 1.6), 2)
    o = round(random.uniform(0.3, 0.7), 2)
    stars.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#E8C879" opacity="{o}"/>')

svg = (
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
    f'width="{W}" height="{H}" preserveAspectRatio="xMidYMin slice">\n'
    + "\n".join(stars)
    + "\n</svg>\n"
)
with open("/home/user/vaerksted-ai.github.io/stars.svg", "w") as f:
    f.write(svg)
print(f"stars.svg written: {len(stars)} stars")
