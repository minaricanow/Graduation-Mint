import math, base64, io, json, os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PAL = {'K':'#2b2140','Y':'#e0ab20','O':'#bd7a18','B':'#5a3516','D':'#32200c','G':'#3d8043','g':'#2b5f33',
       'S':'#fbe3d3','P':'#f7a3b0','W':'#ffffff','R':'#f7b6c6','E':'#7a5bc0','H':'#ff8fa3','Z':'#ffd84d',
       'w':'#8d7660','x':'#6e5a49','r':'#5e2a47','q':'#753556','Q':'#45203a','c':'#4a3040','C':'#63455a',
       'f':'#3f2a1e','l':'#ffd36b','m':'#fff0a8','d':'#6b3f24','n':'#1c120d','e':'#7d7468',
       'M':'#ece8c4','N':'#cbc59a','u':'#1f2955','v':'#2a366b',
       'A':'#c8323c','J':'#f2d878','j':'#d9b955','T':'#f1e2b4','t':'#d8c590','k':'#1d1d2b','h':'#47476b','p':'#3a3f66','a':'#5a4636','z':'#e8b9a4'}
BRIGHT = {'Y':'#ffe45c','O':'#f5a524','B':'#7a4a1f','D':'#43260f','G':'#52a056','g':'#397a3f'}

PAL.update({'Y':'#ffd23f','O':'#f0a020','B':'#6b4220','D':'#3f2610','G':'#4fa04f','g':'#37783a',
            'w':'#d8bc98','x':'#b59c80','r':'#b8506a','q':'#d06a85','Q':'#7f3350','c':'#8c6474','C':'#aa8394',
            'f':'#6a4a38','l':'#a9d6f0','m':'#e6f6ff','d':'#8c5732','n':'#2a1b14','e':'#a39a8c','u':'#ffffff','v':'#dcebf7'})
BRIGHT = {'Y':'#ffe66d','O':'#ffb02e','B':'#7a4a1f','D':'#43260f','G':'#5fb85f','g':'#43893f'}

class Grid:
    def __init__(s, w, h): s.w, s.h = w, h; s.p = [['.'] * w for _ in range(h)]
    def set(s, x, y, c):
        x, y = int(round(x)), int(round(y))
        if 0 <= x < s.w and 0 <= y < s.h: s.p[y][x] = c
    def get(s, x, y): return s.p[y][x] if 0 <= x < s.w and 0 <= y < s.h else '.'
    def ell(s, cx, cy, rx, ry, c):
        for y in range(s.h):
            for x in range(s.w):
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1: s.p[y][x] = c
    def img(s, over=None):
        pal = dict(PAL); pal.update(over or {})
        im = Image.new('RGBA', (s.w, s.h), (0, 0, 0, 0))
        for y in range(s.h):
            for x in range(s.w):
                c = s.p[y][x]
                if c in pal:
                    h = pal[c].lstrip('#'); im.putpixel((x, y), tuple(int(h[i:i+2], 16) for i in (0, 2, 4)) + (255,))
        return im

def sheet(frames, over=None):
    w, h = frames[0].w, frames[0].h
    im = Image.new('RGBA', (w * len(frames), h), (0, 0, 0, 0))
    for i, f in enumerate(frames): im.paste(f.img(over), (i * w, 0))
    return im

def flower(big, dx):
    if big: W, Hh, hx, hy, sx, rs, rp, lobes, amp, inner = 13, 18, 6 + dx, 5, 6, 2.4, 4.0, 6, 1.0, 3.5
    else:   W, Hh, hx, hy, sx, rs, rp, lobes, amp, inner = 11, 12, 5 + dx, 4, 5, 1.5, 3.2, 4, .6, 2.6
    g = Grid(W, Hh)
    base, ctrl, tip = (sx, Hh - 1), (sx + dx * .3, Hh * .65), (hx, hy + (3 if big else 2))
    pts = []
    for i in range(41):
        t = i / 40
        x = (1-t)**2*base[0] + 2*t*(1-t)*ctrl[0] + t*t*tip[0]
        y = (1-t)**2*base[1] + 2*t*(1-t)*ctrl[1] + t*t*tip[1]
        pts.append((x, y)); g.set(x, y, 'G')
        if big: g.set(x + 1, y, 'g')
    if big:
        for idx, side in ((18, -1), (26, 1)):
            px, py = [round(v) for v in pts[idx]]
            sx0 = px - 1 if side < 0 else px + 2
            for k, oy in enumerate((0, 0, -1)): g.set(sx0 + side * k, py + oy, 'G' if k < 2 else 'g')
    else:
        px, py = [round(v) for v in pts[22]]
        g.set(px + 1, py, 'G'); g.set(px + 2, py - 1, 'g')
    for y in range(Hh):
        for x in range(W):
            r = math.hypot(x - hx, y - hy); th = math.atan2(y - hy, x - hx)
            R = rp + amp * abs(math.cos(lobes * th)) * (1 if big else .6)
            if r <= rs: g.set(x, y, 'D' if (big and (x + y * 2) % 4 == 0) else 'B')
            elif r <= R: g.set(x, y, 'O' if r <= inner else 'Y')
    return g

def hero(f, capped=True):
    g = Grid(13, 22)
    g.ell(6, 6, 6.4, 6.2, 'J')
    for y in range(7, 10):
        for x in (0, 1, 11, 12): g.set(x, y, 'J')
    for y, (a, b) in {13: (3, 9), 14: (2, 10), 15: (1, 11), 16: (1, 11), 17: (1, 11), 18: (1, 11)}.items():
        for x in range(a, b + 1): g.set(x, y, 'k')
    for x in range(1, 12): g.set(x, 18, 'h')
    for x, y in [(3, 15), (3, 16), (3, 17), (9, 15), (9, 16), (9, 17)]: g.set(x, y, 'h')
    for y in range(13, 18):
        for x in (4, 8): g.set(x, y, 'Z')
    for x in (5, 6, 7): g.set(x, 12, 'S'); g.set(x, 13, 'W')
    g.ell(6, 7.5, 4.6, 4.4, 'S')
    for x in range(2, 11):
        d = 5 if capped else (4 if abs(x - 6) >= 3 else 5)
        for y in range(1, d + 1):
            if g.get(x, y) == 'S': g.set(x, y, 'J')
    for x, y in [(4, 3), (8, 2), (6, 4), (3, 5)]: g.set(x, y, 'j')
    for ex in (4, 8):
        if f != 3: g.set(ex, 7, 'K')
        g.set(ex, 8, 'K')
    g.set(3, 9, 'P'); g.set(9, 9, 'P'); g.set(6, 10, 'H')
    if capped:
        for x in range(3, 10): g.set(x, 0, 'h')
        for x in range(0, 13): g.set(x, 1, 'k')
        for x in range(1, 12): g.set(x, 2, 'k')
        for x in range(3, 10): g.set(x, 3, 'k'); g.set(x, 4, 'k')
        for x in (0, 12): g.set(x, 1, 'h')
        for x in range(6, 12): g.set(x, 1, 'Z')
        for y in range(1, 6): g.set(12, y, 'Z')
    def leg(x0, up):
        for y in ((19,) if up else (19, 20)): g.set(x0, y, 'p'); g.set(x0 + 1, y, 'p')
        sy = 20 if up else 21
        for x in (x0 - 1, x0, x0 + 1): g.set(x, sy, 'W')
    leg(4, f == 1); leg(7, f == 2)
    return g

def cap(f):
    g = Grid(15, 9); ry = [1.2, 2.6, 3.8, 2.6][f]; cy = 4; ins = set()
    for y in range(9):
        for x in range(15):
            if abs(x - 7) / 7 + abs(y - cy) / ry <= 1: ins.add((x, y))
    for (x, y) in ins:
        edge = any((x + a, y + b) not in ins for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        g.set(x, y, 'h' if edge else 'k')
    g.set(7, cy, 'Z')
    for x in range(8, 13): g.set(x, cy, 'Z')
    for y in range(cy + 1, cy + 4): g.set(12, y, 'Z')
    return g

def house(open_, flick):
    g = Grid(36, 30)
    for y in range(11, 30):
        for x in range(3, 33): g.set(x, y, 'x' if y >= 28 else 'w')
    for y in range(0, 12):
        half = int(y * 1.5) + 1
        for x in range(max(0, 17 - half), min(35, 18 + half) + 1):
            g.set(x, y, 'q' if y % 3 == 0 else 'r')
        g.set(max(0, 17 - half), y, 'Q'); g.set(min(35, 18 + half), y, 'Q')
    for x in range(0, 36): g.set(x, 11, 'Q')
    for y in range(1, 8):
        for x in range(26, 30): g.set(x, y, 'c')
    for x in range(25, 31): g.set(x, 0, 'C')
    glass = 'm' if flick else 'l'
    for wx in (7, 23):
        for y in range(15, 21):
            for x in range(wx, wx + 6):
                edge = x in (wx, wx + 5) or y in (15, 20) or x in (wx + 2, wx + 3) or y == 17
                g.set(x, y, 'f' if edge else glass)
    for y in range(19, 30):
        for x in range(15, 21): g.set(x, y, 'f' if (x in (15, 20) or y == 19) else ('n' if open_ else 'd'))
    if open_:
        for y in range(20, 30):
            for x in (17, 18): g.set(x, y, 'Z')
        for y in range(20, 30): g.set(14, y, 'd')
    else:
        g.set(19, 25, 'Z')
        for y in range(21, 28): g.set(17, y, 'f')
    for x in range(14, 22): g.set(x, 29, 'e')
    return g

def moon():
    g = Grid(11, 11); g.ell(5, 5, 5.3, 5.3, 'M')
    for x, y in [(3, 3), (4, 3), (7, 6), (4, 7), (6, 2), (8, 4)]: g.set(x, y, 'N')
    return g

def sun():
    g = Grid(13, 13); g.ell(6, 6, 5.6, 5.6, 'O'); g.ell(6, 6, 5.0, 5.0, 'Z')
    return g

def cloud():
    g = Grid(20, 6)
    for cx, cy, rx, ry in [(5, 4, 4.5, 2.2), (10, 3, 5, 2.8), (15, 4, 4.5, 2.2)]: g.ell(cx, cy, rx, ry, 'u')
    for x in range(20): g.set(x, 5, '.')
    for x in range(20):
        if g.get(x, 4) == 'u': g.set(x, 4, 'v')
    return g

out = {}
def add(name, frames, over=None):
    im = sheet(frames, over)
    os.makedirs(os.path.join(HERE, '..', 'sprites'), exist_ok=True); im.save(os.path.join(HERE, '..', 'sprites', name + '.png'))
    buf = io.BytesIO(); im.save(buf, 'PNG', optimize=True)
    out[name] = {'src': 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode(), 'w': frames[0].w, 'h': frames[0].h, 'n': len(frames)}

add('sunL',  [flower(True, d) for d in (-1, 0, 1)])
add('sunLb', [flower(True, d) for d in (-1, 0, 1)], BRIGHT)
add('sunS',  [flower(False, d) for d in (-1, 0, 1)])
add('sunSb', [flower(False, d) for d in (-1, 0, 1)], BRIGHT)
add('hero',  [hero(i, True) for i in range(4)] + [hero(i, False) for i in range(4)])
add('cap',   [cap(i) for i in range(4)])
add('sun',   [sun()])
add('cloud', [cloud()])
tpl = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
open(os.path.join(HERE, '..', 'index.html'), 'w', encoding='utf-8').write(tpl.replace('__SPRITES__', json.dumps(out)))
print('ok', {k: (v['w'], v['h'], v['n']) for k, v in out.items()})
