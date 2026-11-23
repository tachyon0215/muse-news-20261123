#!/usr/bin/env python3
"""Render entry.png (1024x1024): the world news of Monday 23 Nov 2026 in one image.

Original drawing code using only Pillow shapes and system Noto Sans fonts.
No external images, no network. Deterministic output.
"""
from PIL import Image, ImageDraw, ImageFont
import math

W = H = 1024
FONT_DIR = "/usr/share/fonts/truetype/noto/"
BG = (247, 243, 232)
INK = (17, 17, 17)
WHITE = (255, 255, 255)
SUB = (55, 55, 55)
BOLD = "NotoSans-Bold.ttf"
BLACK = "NotoSans-Black.ttf"
COND_BOLD = "NotoSans-CondensedBold.ttf"
REG = "NotoSans-Regular.ttf"

def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)

def fit(draw, text, name, max_size, min_size, max_width):
    size = max_size
    while size > min_size:
        f = font(name, size)
        if draw.textlength(text, font=f) <= max_width:
            return f
        size -= 2
    return font(name, min_size)

def center(draw, cx, y, text, f, fill):
    w = draw.textlength(text, font=f)
    draw.text((cx - w / 2, y), text, font=f, fill=fill)
    return y + f.size

def star(d, cx, cy, r, fill, outline=None):
    pts = []
    for i in range(16):
        ang = math.pi * i / 8
        rad = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    d.polygon(pts, fill=fill, outline=outline)

# ---------------------------------------------------------------- icons

def icon_climate(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(224, 242, 241))
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 + 6
    r = min(x1 - x0, y1 - y0) * 0.30
    # globe
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(37, 99, 235), outline=INK, width=4)
    # continents (simple blobs)
    d.ellipse([cx - r*0.62, cy - r*0.55, cx - r*0.05, cy - r*0.05], fill=(34, 197, 94))
    d.ellipse([cx + r*0.08, cy + r*0.02, cx + r*0.62, cy + r*0.55], fill=(34, 197, 94))
    d.ellipse([cx - r*0.15, cy + r*0.28, cx + r*0.28, cy + r*0.72], fill=(34, 197, 94))
    # thermometer on right
    tx = x1 - 34
    d.rounded_rectangle([tx - 10, y0 + 22, tx + 10, y1 - 52], radius=9, fill=WHITE, outline=INK, width=4)
    d.rectangle([tx - 5, y0 + 70, tx + 5, y1 - 58], fill=(220, 38, 38))
    d.ellipse([tx - 17, y1 - 62, tx + 17, y1 - 28], fill=(220, 38, 38), outline=INK, width=4)
    # broken handshake / X over a document at bottom left: no deal
    dx, dy = x0 + 16, y1 - 58
    d.rectangle([dx, dy, dx + 62, dy + 42], fill=WHITE, outline=INK, width=3)
    d.line([dx + 6, dy + 6, dx + 56, dy + 36], fill=(220, 38, 38), width=6)
    d.line([dx + 56, dy + 6, dx + 6, dy + 36], fill=(220, 38, 38), width=6)

def icon_tanker(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(219, 234, 254))
    sea_y = y0 + (y1 - y0) * 0.62
    d.rectangle([x0, sea_y, x1, y1], fill=(37, 99, 235))
    for i in range(3):
        wy = sea_y + 12 + i * 18
        for wx in range(int(x0 + 10), int(x1 - 28), 50):
            d.line([wx, wy, wx + 22, wy], fill=(147, 197, 253), width=4)
    # tanker hull
    hx0, hx1 = x0 + 14, x1 - 14
    hy = sea_y - 26
    d.polygon([(hx0, hy), (hx1, hy), (hx1 - 18, hy + 26), (hx0 + 18, hy + 26)], fill=(31, 41, 55))
    d.rectangle([hx0 + 6, hy - 16, hx1 - 6, hy], fill=(185, 28, 28))
    # bridge tower
    d.rectangle([hx1 - 52, hy - 44, hx1 - 22, hy - 16], fill=WHITE, outline=INK, width=3)
    # explosion / hit on hull side
    star(d, (hx0 + hx1) / 2, hy + 4, 26, (245, 158, 11), (185, 28, 28))
    # mine circles in water
    for mx in (x0 + 42, x1 - 48):
        d.ellipse([mx - 11, sea_y + 30, mx + 11, sea_y + 52], fill=INK)
        d.line([mx, sea_y + 30, mx, sea_y + 22], fill=INK, width=4)

def icon_kyiv(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(254, 226, 226))
    # apartment building
    bx0, by0, bx1, by1 = x0 + 18, y0 + 52, x0 + 118, y1 - 14
    d.rectangle([bx0, by0, bx1, by1], fill=(209, 213, 219), outline=INK, width=4)
    for r in range(4):
        for c in range(2):
            wx = bx0 + 14 + c * 42
            wy = by0 + 14 + r * 34
            col = (251, 191, 36) if (r + c) % 2 == 0 else (147, 197, 253)
            d.rectangle([wx, wy, wx + 26, wy + 20], fill=col, outline=INK, width=2)
    # damage hole
    star(d, bx1 - 8, by0 + 52, 24, (245, 158, 11), (185, 28, 28))
    d.ellipse([bx1 - 30, by0 + 34, bx1 + 6, by0 + 70], fill=(75, 85, 99))
    # drone upper right
    cx, cy = x1 - 62, y0 + 44
    for sx in (-1, 1):
        rx = cx + sx * 40
        d.line([cx, cy, rx, cy - 4], fill=INK, width=6)
        d.ellipse([rx - 20, cy - 12, rx + 20, cy + 2], outline=INK, width=5)
    d.rounded_rectangle([cx - 22, cy - 9, cx + 22, cy + 10], radius=8, fill=INK)
    d.line([cx, cy + 10, cx - 28, by0 + 40], fill=(220, 38, 38), width=4)

def icon_factory(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(255, 237, 213))
    base = y1 - 18
    # factory silhouette
    d.rectangle([x0 + 14, base - 62, x1 - 58, base], fill=(75, 85, 99), outline=INK, width=3)
    d.polygon([(x0 + 14, base - 62), (x0 + 66, base - 92), (x1 - 58, base - 62)], fill=(55, 65, 81), outline=INK)
    # chimneys
    for chx in (x1 - 46, x1 - 26):
        d.rectangle([chx, base - 104, chx + 12, base], fill=(75, 85, 99), outline=INK, width=2)
    # flames
    for fx, fh in ((x0 + 52, 58), (x0 + 92, 76), (x0 + 132, 52)):
        fy = base - 62
        d.polygon([(fx - 18, fy), (fx, fy - fh), (fx + 18, fy)], fill=(249, 115, 22), outline=(185, 28, 28))
        d.polygon([(fx - 9, fy), (fx, fy - fh * 0.55), (fx + 9, fy)], fill=(251, 191, 36))
    # smoke
    for sx, sy, sr in ((x1 - 58, y0 + 26, 16), (x1 - 34, y0 + 16, 12)):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(156, 163, 175))

def icon_quake(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(237, 233, 254))
    base = y1 - 16
    # Andes mountains
    d.polygon([(x0 + 8, base), (x0 + 62, y0 + 34), (x0 + 116, base)], fill=(120, 113, 108), outline=INK, width=3)
    d.polygon([(x0 + 84, base), (x1 - 52, y0 + 20), (x1 - 8, base)], fill=(168, 162, 158), outline=INK, width=3)
    d.polygon([(x0 + 48, y0 + 52), (x0 + 62, y0 + 34), (x0 + 78, y0 + 52)], fill=WHITE)
    d.polygon([(x1 - 66, y0 + 40), (x1 - 52, y0 + 20), (x1 - 38, y0 + 40)], fill=WHITE)
    # crack in ground
    mid = (x0 + x1) / 2
    pts = [(mid - 50, base), (mid - 22, base - 10), (mid - 30, base - 20), (mid, base - 14), (mid - 4, base - 26), (mid + 28, base - 18), (mid + 52, base - 26)]
    # draw crack as zigzag line near base
    crack = [(x0 + 20, base - 4), (x0 + 58, base - 14), (x0 + 84, base - 4), (x0 + 118, base - 16), (x0 + 148, base - 6), (x1 - 24, base - 14)]
    d.line(crack, fill=(185, 28, 28), width=5)
    # seismic waves top right
    for rr in (14, 26, 38):
        d.arc([x1 - 62 - rr, y0 + 8 - rr + 20, x1 - 62 + rr, y0 + 8 + rr + 20], start=300, end=60, fill=(124, 58, 237), width=5)

STORIES = [
    {"tag": "CLIMATE", "accent": (15, 118, 110), "icon": icon_climate,
     "headline": ["COP31 ENDS WITH", "NO CLIMATE DEAL"],
     "sub": ["Antalya talks run past deadline;", "EU refuses to endorse draft"]},
    {"tag": "MIDDLE EAST", "accent": (185, 28, 28), "icon": icon_tanker,
     "headline": ["TANKERS HIT IN", "HORMUZ STRAIT"],
     "sub": ["Two oil tankers struck amid", "Iran-US tensions at sea"]},
    {"tag": "WAR", "accent": (0, 91, 187), "icon": icon_kyiv,
     "headline": ["DRONE HITS KYIV", "REGION BUILDING"],
     "sub": ["14 missing after Russian strike,", "Zelenskiy says"]},
    {"tag": "ASIA", "accent": (194, 65, 12), "icon": icon_factory,
     "headline": ["FACTORY FIRE IN", "INDONESIA"],
     "sub": ["3 dead, 36 missing at Banten", "candy factory; search goes on"]},
    {"tag": "EARTHQUAKE", "accent": (124, 58, 237), "icon": icon_quake,
     "headline": ["MAGNITUDE 6.7 QUAKE SHAKES PERU"],
     "sub": ["Andes tremor felt in Lima; no casualties reported at first"]},
]

def panel(d, box, story, icon_w):
    x0, y0, x1, y1 = box
    accent = story["accent"]
    d.rounded_rectangle(box, radius=14, fill=WHITE, outline=accent, width=4)
    pad = 12
    ibox = [x0 + pad, y0 + pad, x0 + pad + icon_w, y1 - pad]
    tmp = Image.new("RGB", (int(ibox[2] - ibox[0]), int(ibox[3] - ibox[1])), WHITE)
    td = ImageDraw.Draw(tmp)
    story["icon"](td, [0, 0, tmp.width, tmp.height])
    return tmp, ibox

def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 148], fill=INK)
    d.rectangle([0, 148, W, 156], fill=(245, 158, 11))
    f_title = fit(d, "MONDAY 23 NOVEMBER 2026", BLACK, 58, 30, W - 40)
    center(d, W / 2, 16, "MONDAY 23 NOVEMBER 2026", f_title, WHITE)
    f_sub = font(COND_BOLD, 30)
    center(d, W / 2, 92, "T H E   W O R L D   I N   O N E   I M A G E", f_sub, (245, 158, 11))
    margin, gap = 20, 14
    top = 172
    footer_h = 30
    area_bottom = H - margin - footer_h
    row_h = [(area_bottom - top - gap * 2) // 3] * 3
    row_h[2] += (area_bottom - top - gap * 2) - sum(row_h)
    col_w = (W - margin * 2 - gap) // 2
    positions = []
    y = top
    for r in range(3):
        if r < 2:
            positions.append([margin, y, margin + col_w, y + row_h[r]])
            positions.append([margin + col_w + gap, y, W - margin, y + row_h[r]])
        else:
            positions.append([margin, y, W - margin, y + row_h[r]])
        y += row_h[r] + gap
    for story, box in zip(STORIES, positions):
        x0, y0, x1, y1 = box
        accent = story["accent"]
        wide = (x1 - x0) > col_w + 10
        icon_w = 300 if wide else 168
        tmp, ibox = panel(d, box, story, icon_w)
        img.paste(tmp, (int(ibox[0]), int(ibox[1])))
        d.rounded_rectangle(ibox, radius=10, outline=accent, width=2)
        tx = ibox[2] + 18
        tw = x1 - tx - 14
        f_tag = font(COND_BOLD, 21)
        tag_w = d.textlength(story["tag"], font=f_tag) + 22
        d.rounded_rectangle([tx, y0 + 14, tx + tag_w, y0 + 46], radius=8, fill=accent)
        d.text((tx + 11, y0 + 18), story["tag"], font=f_tag, fill=WHITE)
        hy = y0 + 56
        max_head = 46 if not wide else 54
        for line in story["headline"]:
            f_h = fit(d, line, BLACK, max_head, 24, tw)
            d.text((tx, hy), line, font=f_h, fill=INK)
            hy += f_h.size + 6
        f_s = font(REG, 24 if not wide else 27)
        sy = hy + 6
        for line in story["sub"]:
            f_line = fit(d, line, REG, f_s.size, 16, tw)
            d.text((tx, sy), line, font=f_line, fill=SUB)
            sy += f_line.size + 5
    f_f = font(COND_BOLD, 20)
    center(d, W / 2, H - margin - footer_h + 4,
           "SOURCES: MANILA TIMES - EDEXLIVE - JAGRAN JOSH - NDTV - TIMES NOW",
           f_f, (100, 100, 100))
    img.save("entry.png", format="PNG")
    print("saved entry.png", img.size)

if __name__ == "__main__":
    main()
