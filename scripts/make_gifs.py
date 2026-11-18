#!/usr/bin/env python3
"""Erzeugt authentische 90er-Jahre-Web-GIFs nach public/gifs/.

Ausfuehren:  python3 scripts/make_gifs.py
Benötigt Pillow.  Alle GIFs loopen ewig (loop=0).
"""
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent.parent / "public" / "gifs"
OUT.mkdir(parents=True, exist_ok=True)

FONT_BOLD = None
for cand in (
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
):
    if Path(cand).exists():
        FONT_BOLD = cand
        break


def font(size):
    if FONT_BOLD:
        return ImageFont.truetype(FONT_BOLD, size)
    return ImageFont.load_default(size)


def save(frames, name, duration=140, colors=64):
    """frames: Liste von RGB-Images -> animiertes GIF."""
    pal = [
        f.quantize(colors=colors, method=Image.MEDIANCUT, dither=Image.NONE)
        for f in frames
    ]
    pal[0].save(OUT / name, save_all=True, append_images=pal[1:],
                duration=duration, loop=0, disposal=1, optimize=True)
    print("  ✓", name, f"({len(frames)} frames)")


# ---------------------------------------------------------------- rainbow bar
def rainbow():
    colors = [(255, 0, 0), (255, 128, 0), (255, 255, 0),
              (0, 200, 0), (0, 80, 255), (160, 0, 255)]
    w, h = 96, 12
    frames = []
    for shift in range(6):
        img = Image.new("RGB", (w, h))
        d = ImageDraw.Draw(img)
        row = 0
        i = shift
        while row < h:
            c = colors[i % 6]
            band = 2
            d.rectangle([0, row, w, row + band], fill=c)
            row += band
            i += 1
        frames.append(img)
    save(frames, "rainbow.gif", duration=160, colors=16)


# ------------------------------------------------------------- starfield tile
def stars():
    rng = random.Random(1996)
    size = 160
    n = 42
    starlist = []
    for _ in range(n):
        starlist.append({
            "x": rng.randint(0, size - 1), "y": rng.randint(0, size - 1),
            "c": rng.choice([(255, 255, 255), (255, 255, 120), (120, 255, 255),
                             (255, 120, 255), (140, 255, 140), (255, 190, 120)]),
            "phase": rng.randint(0, 3),
            "big": rng.random() < 0.22,
        })

    def draw_star(d, x, y, c, r):
        # plus-form mit diagonaler Verstaerkung
        d.point((x, y), fill=c)
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            px, py = x + dx, y + dy
            if r >= 1:
                d.point((px, py), fill=c)
            if r >= 2:
                d.point((x + 2 * dx, y + 2 * dy), fill=c)
                d.point((x + dx, y + dy + 1), fill=c)
                d.point((x + dx, y + dy - 1), fill=c)
        if r >= 2:
            for dx, dy in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
                d.point((x + dx, y + dy), fill=c)

    frames = []
    for f in range(4):
        img = Image.new("RGB", (size, size), (5, 3, 16))
        d = ImageDraw.Draw(img)
        for s in starlist:
            bright = (s["phase"] + f) % 4 != 3
            r = (2 if s["big"] else 1) if bright else 0
            if bright:
                # wrap-around zeichnen, damit der Tile nahtlos kachelt
                for ox in (-size, 0, size):
                    for oy in (-size, 0, size):
                        draw_star(d, s["x"] + ox, s["y"] + oy, s["c"], r)
        frames.append(img)
    save(frames, "stars.gif", duration=280, colors=32)


# ------------------------------------------------------------- spinning globe
def globe():
    size = 64
    cx = cy = 32
    r = 28
    ocean = (20, 80, 220)
    land = (30, 180, 70)
    line = (140, 210, 255)
    frames = []
    steps = 12
    for i in range(steps):
        t = i / steps * math.pi
        img = Image.new("RGB", (size, size), (0, 0, 0, 255))
        d = ImageDraw.Draw(img)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=ocean)
        # Kontinente (klecksige Pixel-Welt)
        rng = random.Random(7)
        for _ in range(9):
            bx, by = rng.randint(cx - 18, cx + 10), rng.randint(cy - 16, cy + 12)
            s = rng.randint(4, 9)
            d.ellipse([bx, by, bx + s, by + s - 2], fill=land)
        # Rotations-Ellipsen (Meridiane)
        for k in (0.25, 0.6, 0.92):
            rx = r * abs(math.cos(t + k * math.pi))
            d.ellipse([cx - rx, cy - r, cx + rx, cy + r], outline=line)
        # Breitengrade
        for yy in (cy - 14, cy, cy + 14):
            dy = abs(cy - yy)
            rx = math.sqrt(max(r * r - dy * dy, 1))
            d.line([cx - rx, yy, cx + rx, yy], fill=line)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255))
        d.point((cx - 14, cy - 16), fill=(255, 255, 255))
        d.point((cx - 13, cy - 17), fill=(255, 255, 255))
        frames.append(img)
    save(frames, "globe.gif", duration=110, colors=32)


# --------------------------------------------------------- under construction
def construction():
    w, h = 150, 96
    yellow = (255, 210, 0)
    black = (0, 0, 0)
    orange = (255, 120, 0)
    frames = []
    for f in range(4):
        img = Image.new("RGB", (w, h), black)
        d = ImageDraw.Draw(img)
        # gestreifte Balken oben/unten (versetzt pro Frame = laeuft)
        for bar_y in (0, h - 10):
            for x in range(-10, w + 10, 10):
                off = (x + f * 2) % 20
                if off < 10:
                    d.polygon([(x, bar_y), (x + 10, bar_y),
                               (x + 10 - 10, bar_y + 10), (x - 10, bar_y + 10)],
                              fill=yellow)
        # Blinklampe
        if f % 2 == 0:
            d.ellipse([w // 2 - 5, 12, w // 2 + 5, 22], fill=orange,
                      outline=(255, 255, 255))
        else:
            d.ellipse([w // 2 - 5, 12, w // 2 + 5, 22], outline=orange)
        fnt = font(13)
        txt1, txt2 = "UNDER", "CONSTRUCTION"
        for txt, yy, col in ((txt1, 34, yellow), (txt2, 52, yellow)):
            if f % 4 == 3:
                col = (255, 255, 255)
            bb = d.textbbox((0, 0), txt, font=fnt)
            d.text(((w - bb[2] + bb[0]) / 2, yy), txt, fill=col, font=fnt)
        frames.append(img)
    save(frames, "construction.gif", duration=420, colors=16)


# ------------------------------------------------------------------ NEW! sign
def new_badge():
    fnt = font(13)
    frames = []
    for f in range(2):
        img = Image.new("RGB", (52, 26), (255, 40, 40) if f == 0 else (255, 230, 0))
        d = ImageDraw.Draw(img)
        # Zacken-Stern
        cx, cy, r1, r2 = 26, 13, 12, 5.5
        pts = []
        for i in range(16):
            ang = math.pi * 2 * i / 16 - math.pi / 2
            rr = r1 if i % 2 == 0 else r2
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
        col = (255, 230, 0) if f == 0 else (255, 40, 40)
        d.polygon(pts, fill=col)
        d.text((26, 12), "NEW!", fill=(0, 0, 0) if f == 0 else (255, 255, 255),
               font=fnt, anchor="mm")
        frames.append(img)
    save(frames, "new.gif", duration=400, colors=8)


# ------------------------------------------------------------ sparkle divider
def sparkle():
    w, h = 300, 22
    cols = [(255, 255, 255), (120, 255, 255), (255, 120, 255),
            (255, 255, 120), (140, 255, 140)]
    pos = [30, 80, 130, 180, 230, 275]
    frames = []
    for f in range(6):
        img = Image.new("RGB", (w, h), (10, 6, 24))
        d = ImageDraw.Draw(img)
        for i, x in enumerate(pos):
            phase = (f + i) % 6
            r = [0, 1, 2, 3, 2, 1][phase]
            if r == 0:
                continue
            c = cols[i % len(cols)]
            y = h // 2
            d.line([x - r, y, x + r, y], fill=c)
            d.line([x, y - r, x, y + r], fill=c)
            if r >= 2:
                d.point((x - 1, y - 1), fill=c)
                d.point((x + 1, y + 1), fill=c)
        frames.append(img)
    save(frames, "sparkle.gif", duration=150, colors=16)


# ------------------------------------------------------------ bouncing arrow
def arrow():
    frames = []
    for f in range(4):
        dy = [0, 3, 6, 3][f]
        img = Image.new("RGB", (40, 44), (0, 0, 0))
        d = ImageDraw.Draw(img)
        col = (255, 230, 0)
        d.polygon([(20, 34 + dy), (6, 18 + dy), (14, 18 + dy), (14, 6 + dy),
                   (26, 6 + dy), (26, 18 + dy), (34, 18 + dy)], fill=col)
        frames.append(img)
    save(frames, "arrow.gif", duration=160, colors=8)


# ---------------------------------------------------------------- pixel heart
def heart():
    frames = []
    for f, (col, grow) in enumerate([((255, 30, 60), 0), ((255, 130, 160), 1)]):
        img = Image.new("RGB", (22, 22), (0, 0, 0))
        d = ImageDraw.Draw(img)
        d.ellipse([2 - grow, 4 - grow, 11 + grow, 13 + grow], fill=col)
        d.ellipse([11 - grow, 4 - grow, 20 + grow, 13 + grow], fill=col)
        d.polygon([(2 - grow, 9), (20 + grow, 9), (11, 20 + grow)], fill=col)
        d.ellipse([4, 5, 8, 9], fill=(255, 170, 190))
        frames.append(img)
    save(frames, "heart.gif", duration=450, colors=8)


# --------------------------------------------------------------- "you got mail"
def envelope():
    frames = []
    for f in range(2):
        img = Image.new("RGB", (44, 30), (0, 0, 0))
        d = ImageDraw.Draw(img)
        d.rectangle([3, 6, 41, 26], fill=(250, 250, 220), outline=(60, 60, 60))
        d.line([3, 6, 22, 18], fill=(60, 60, 60))
        d.line([41, 6, 22, 18], fill=(60, 60, 60))
        if f == 1:
            d.polygon([(38, 6), (38, 1), (32, 6)], fill=(255, 40, 40))
        frames.append(img)
    save(frames, "mail.gif", duration=500, colors=8)


# ------------------------------------------------------------------- flames
def flames():
    rng = random.Random(88)
    frames = []
    for _ in range(6):
        img = Image.new("RGB", (36, 52), (0, 0, 0))
        d = ImageDraw.Draw(img)
        base = 50
        pts = [(4, base), (32, base)]
        for x in range(6, 32, 3):
            pts.append((x, base - rng.randint(8, 34)))
        pts.append((32, base))
        d.polygon(pts, fill=(255, 80, 0))
        pts2 = [(9, base), (27, base)]
        for x in range(11, 28, 3):
            pts2.append((x, base - rng.randint(6, 26)))
        pts2.append((27, base))
        d.polygon(pts2, fill=(255, 190, 0))
        d.polygon([(14, base), (22, base), (18, base - rng.randint(6, 16))],
                  fill=(255, 255, 120))
        frames.append(img)
    save(frames, "flame.gif", duration=140, colors=16)


# ------------------------------------------------------------- robot head
def robot():
    silver = (176, 184, 200)
    dark = (60, 66, 80)
    cyan = (125, 249, 255)
    red = (255, 60, 60)
    frames = []
    for f in range(4):
        img = Image.new("RGB", (32, 36), (0, 0, 0))
        d = ImageDraw.Draw(img)
        # Antenne mit Blinklicht
        d.line([15, 3, 15, 8], fill=dark)
        d.ellipse([12, 0, 18, 5], fill=red if f % 2 == 0 else dark)
        # Kopf mit Stirnband
        d.rectangle([4, 8, 27, 30], fill=silver, outline=dark)
        d.rectangle([4, 8, 27, 13], fill=(140, 148, 164))
        # Ohren
        d.rectangle([1, 14, 4, 22], fill=dark)
        d.rectangle([27, 14, 30, 22], fill=dark)
        # Augen (blinken in Frame 2)
        eye = cyan if f != 2 else dark
        d.rectangle([9, 16, 13, 20], fill=eye, outline=dark)
        d.rectangle([18, 16, 22, 20], fill=eye, outline=dark)
        # Mundgitter
        for x in range(10, 22, 4):
            d.rectangle([x, 24, x + 1, 28], fill=dark)
        frames.append(img)
    save(frames, "robot.gif", duration=350, colors=16)


# ------------------------------------------------------ construction worker
def worker():
    yellow = (255, 210, 63)
    skin = (242, 196, 155)
    orange = (255, 123, 0)
    stripe = (255, 236, 77)
    blue = (52, 68, 128)
    dark = (40, 40, 40)
    grey = (150, 150, 150)
    brown = (122, 84, 48)
    frames = []
    for f in range(4):
        img = Image.new("RGB", (42, 54), (5, 3, 15))
        d = ImageDraw.Draw(img)
        # Boden
        d.rectangle([0, 47, 41, 49], fill=grey)
        # Schutzhelm
        d.rectangle([10, 1, 24, 5], fill=yellow)
        d.rectangle([8, 5, 26, 7], fill=yellow)
        # Gesicht
        d.rectangle([11, 8, 23, 14], fill=skin)
        d.rectangle([13, 10, 14, 11], fill=dark)
        d.rectangle([19, 10, 20, 11], fill=dark)
        # Warnweste mit Reflexionsstreifen
        d.rectangle([9, 15, 25, 31], fill=orange)
        d.rectangle([9, 22, 25, 24], fill=stripe)
        # Arme
        d.rectangle([6, 16, 9, 26], fill=skin)
        d.rectangle([25, 16, 28, 26], fill=skin)
        # Beine + Stiefel
        d.rectangle([12, 32, 16, 46], fill=blue)
        d.rectangle([18, 32, 22, 46], fill=blue)
        d.rectangle([11, 46, 17, 48], fill=dark)
        d.rectangle([17, 46, 23, 48], fill=dark)
        # Schaufel gräbt (Blatt-Tiefe pro Frame)
        by = 36 + f * 2
        d.line([26 + f, 18 + f, 33, by], fill=grey)
        d.rectangle([31, by, 38, by + 6], fill=grey)
        # Erdbrocken fliegen beim Aushub
        if f in (1, 2):
            d.rectangle([30 + f, 30 - f * 4, 31 + f, 31 - f * 4], fill=brown)
            d.rectangle([34 - f, 26 + f * 2, 35 - f, 27 + f * 2], fill=brown)
        # Haufen
        d.ellipse([26, 42, 41, 49], fill=brown)
        frames.append(img)
    save(frames, "worker.gif", duration=320, colors=16)


# -------------------------------------------------------------- skull (punk!)
def skull():
    frames = []
    glow = [(255, 40, 40), (255, 120, 0), (120, 255, 120), (120, 220, 255)]
    for f in range(4):
        img = Image.new("RGB", (30, 30), (0, 0, 0))
        d = ImageDraw.Draw(img)
        c = glow[f]
        # Gluehen
        d.ellipse([1, 1, 28, 28], outline=c)
        d.ellipse([3, 3, 26, 26], outline=c)
        # Schaedel
        d.ellipse([5, 4, 24, 21], fill=(240, 240, 240))
        d.rectangle([9, 20, 20, 26], fill=(240, 240, 240))
        d.rectangle([11, 22, 12, 26], fill=(0, 0, 0))
        d.rectangle([14, 22, 15, 26], fill=(0, 0, 0))
        d.rectangle([17, 22, 18, 26], fill=(0, 0, 0))
        d.ellipse([8, 10, 13, 16], fill=c)
        d.ellipse([16, 10, 21, 16], fill=c)
        d.polygon([(14, 15), (16, 15), (15, 18)], fill=(0, 0, 0))
        frames.append(img)
    save(frames, "skull.gif", duration=300, colors=16)


# ------------------------------------------------------------- 88x31 badges
def badge(name, line1, line2, bg, fg, accent):
    w, h = 88, 31
    fnt = font(10)
    frames = []
    for f in range(2):
        img = Image.new("RGB", (w, h), bg)
        d = ImageDraw.Draw(img)
        d.rectangle([0, 0, w - 1, h - 1], outline=accent if f else fg)
        d.text((w / 2, 9), line1, fill=fg, font=fnt, anchor="mm")
        d.text((w / 2, 21), line2, fill=accent if f else fg, font=fnt, anchor="mm")
        frames.append(img)
    save(frames, f"badge-{name}.gif", duration=600, colors=8)


def badges():
    badge("netscape", "BEST VIEWED IN", "NETSCAPE 4.0", (0, 0, 90), (255, 255, 255), (255, 220, 0))
    badge("y2k", "100%", "Y2K READY", (0, 0, 0), (0, 220, 80), (180, 255, 60))
    badge("html", "POWERED BY", "HTML 3.2", (90, 0, 0), (255, 255, 255), (255, 150, 0))
    badge("notepad", "MADE WITH", "NOTEPAD", (200, 200, 200), (0, 0, 0), (120, 120, 220))
    badge("modem", "OPTIMIZED FOR", "56k MODEM", (30, 0, 60), (255, 255, 255), (255, 80, 255))
    badge("ie", "ALSO WORKS IN", "IE 5.5 (?!) ", (0, 40, 90), (255, 255, 255), (60, 200, 255))


# ------------------------------------------------------------------ wax seal
def seal():
    size = 76
    cx = cy = 38
    dark = (150, 20, 20)
    red = (200, 30, 30)
    light = (255, 90, 90)
    gold = (255, 215, 0)
    frames = []
    for f in range(4):
        img = Image.new("RGB", (size, size), (10, 6, 24))
        d = ImageDraw.Draw(img)
        # gezackter Wachsrund
        for i in range(24):
            ang = math.pi * 2 * i / 24
            px = cx + 34 * math.cos(ang)
            py = cy + 34 * math.sin(ang)
            d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=dark)
        d.ellipse([cx - 32, cy - 32, cx + 32, cy + 32], fill=red)
        # Glanz, wandert langsam
        gx = cx - 18 + f * 4
        d.ellipse([gx, cy - 26, gx + 12, cy - 12], fill=light)
        # goldener Innenring (doppelt)
        d.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], outline=gold)
        d.ellipse([cx - 23, cy - 23, cx + 23, cy + 23], outline=gold)
        d.text((cx, cy), "GEPRÜFT", fill=(255, 255, 255), font=font(8), anchor="mm")
        frames.append(img)
    save(frames, "seal.gif", duration=500, colors=16)


if __name__ == "__main__":
    print("Generiere 90er-GIFs nach", OUT)
    rainbow()
    stars()
    globe()
    construction()
    new_badge()
    sparkle()
    arrow()
    heart()
    envelope()
    flames()
    skull()
    robot()
    worker()
    badges()
    seal()
    print("Fertig!")
