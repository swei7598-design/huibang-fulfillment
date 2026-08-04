from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from PIL import Image
import math

files = ["hba_globe", "hbb_orbit", "hbc_network"]
size = 512
for name in files:
    d = svg2rlg(f"{name}.svg")
    renderPM.drawToFile(d, f"{name}_raw.png", fmt="PNG")
    im = Image.open(f"{name}_raw.png").convert("RGBA")
    im = im.resize((size, size), Image.LANCZOS)
    w, h = im.size
    cx, cy = w/2, h/2
    r = min(w, h)/2 - 2
    px = im.load()
    for y in range(h):
        for x in range(w):
            if math.hypot(x-cx, y-cy) > r:
                px[x, y] = (0, 0, 0, 0)
    im.save(f"{name}.png")
    print(name, im.size, im.mode)
