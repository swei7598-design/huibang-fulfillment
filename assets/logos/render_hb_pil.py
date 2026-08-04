from PIL import Image, ImageDraw
import math

S = 512
CX = CY = S // 2
NAVY = (10, 14, 26, 255)
NAVY2 = (27, 42, 74, 255)
GOLD = (245, 185, 66, 255)
GOLDL = (255, 206, 106, 255)
GOLD_DIM = (245, 185, 66, 110)

def new_canvas():
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([6, 6, S-6, S-6], fill=NAVY)
    d.ellipse([16, 16, S-16, S-16], fill=NAVY2)
    d.ellipse([16, 16, S-16, S-16], outline=GOLD, width=5)
    return im, d

def globe_grid(d, strong=GOLD_DIM):
    # longitude + latitude ellipses + equator
    d.ellipse([CX-84, 14, CX+84, S-14], outline=strong, width=2)
    d.ellipse([CX-174, 14, CX+174, S-14], outline=strong, width=2)
    d.line([14, CY, S-14, CY], fill=strong, width=2)
    d.ellipse([14, CY-84, S-14, CY+84], outline=strong, width=2)
    d.ellipse([14, CY-174, S-14, CY+174], outline=strong, width=2)

def hb_letters(d, w=20):
    g = GOLDL
    # H
    d.rectangle([180, 196, 200, 316], fill=g)
    d.rectangle([218, 196, 238, 316], fill=g)
    d.rectangle([180, 248, 238, 268], fill=g)
    # B stem + two right-half disks
    d.rectangle([258, 196, 278, 316], fill=g)
    d.pieslice([216, 196, 320, 268], 270, 90, fill=g)   # top bowl
    d.pieslice([216, 244, 320, 316], 270, 90, fill=g)   # bottom bowl

def nodes(d, pts, r=5, color=GOLDL):
    for (x, y) in pts:
        d.ellipse([x-r, y-r, x+r, y+r], fill=color)

def bezier(p0, p1, p2, n=40):
    pts = []
    for i in range(n+1):
        t = i / n
        x = (1-t)**2*p0[0] + 2*(1-t)*t*p1[0] + t*t*p2[0]
        y = (1-t)**2*p0[1] + 2*(1-t)*t*p1[1] + t*t*p2[1]
        pts.append((x, y))
    return pts

# ---------- A: 经纬地球 ----------
im, d = new_canvas()
globe_grid(d)
hb_letters(d)
nodes(d, [(CX, 70), (S-70, CY), (CX, S-70), (70, CY),
          (140, 140), (372, 140), (372, 372), (140, 372)], r=5)
im.save("hba_globe.png")

# ---------- B: 轨道环绕 ----------
im, d = new_canvas()
# globe inner
d.ellipse([CX-92, CY-92, CX+92, CY+92], fill=NAVY, outline=GOLD, width=4)
d.ellipse([CX-32, CY-90, CX+32, CY+90], outline=GOLD_DIM, width=2)
d.ellipse([CX-64, CY-90, CX+64, CY+90], outline=GOLD_DIM, width=2)
d.line([CX-92, CY, CX+92, CY], fill=GOLD_DIM, width=2)
d.ellipse([CX-92, CY-30, CX+92, CY+30], outline=GOLD_DIM, width=2)
d.ellipse([CX-92, CY-62, CX+92, CY+62], outline=GOLD_DIM, width=2)
# orbit ring (rotated) on separate layer
orb = Image.new("RGBA", (S, S), (0, 0, 0, 0))
od = ImageDraw.Draw(orb)
od.ellipse([40, CY-56, S-40, CY+56], outline=GOLD, width=3)
od.ellipse([S-40-9, CY-9, S-40+9, CY+9], fill=GOLDL)  # globe dot at east
orb = orb.rotate(-24, center=(CX, CY), resample=Image.BICUBIC)
im = Image.alpha_composite(im, orb)
d = ImageDraw.Draw(im)
hb_letters(d, w=15)
nodes(d, [(CX, 104), (S-104, CY), (CX, S-104), (104, CY)], r=4)
im.save("hbb_orbit.png")

# ---------- C: 全球网络 ----------
im, d = new_canvas()
globe_grid(d)
# network arcs
arcs = [
    ((CX, 80), (340, 140), (300, 330)),
    ((300, 330), (200, 380), (110, 330)),
    ((110, 330), (70, 160), (CX, 80)),
    ((110, 330), (60, 210), (CX, 80)),
    ((300, 330), (350, 210), (CX, 80)),
]
for p0, p1, p2 in arcs:
    d.line(bezier(p0, p1, p2), fill=GOLDL, width=3)
hb_letters(d)
nodes(d, [(CX, 80), (300, 330), (110, 330), (CX, 70), (S-70, CY), (70, CY)], r=5)
im.save("hbc_network.png")

# circular alpha mask so outside badge is transparent
for name in ["hba_globe", "hbb_orbit", "hbc_network"]:
    im = Image.open(f"{name}.png").convert("RGBA")
    px = im.load()
    r = S//2 - 3
    for y in range(S):
        for x in range(S):
            if math.hypot(x-CX, y-CY) > r:
                px[x, y] = (0, 0, 0, 0)
    im.save(f"{name}.png")
    print(name, im.size, im.mode)
print("ALL DONE")
