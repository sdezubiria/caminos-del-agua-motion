"""Builds prototipo/index.html from index.src.html, and js/siete-raices.js from the Cargo card snippet.

Each section is laid out on the 1920 px Figma frame (file "Caminos del Agua", frames Final 49 to Final 63).
`pl()` places one Figma vector or image at its frame coordinates; CSS scales the frame with the page width.
On narrow screens the line art (class "deco") is hidden and the sections reflow (see css/site.css)."""
import hashlib, json, math, pathlib, re

here = pathlib.Path(__file__).resolve().parent
root = here.parent
SVG = 'img/svg/'
# Final domain is not decided yet: canonical, Open Graph, JSON-LD, robots.txt and sitemap.xml use this
SITE = 'https://www.caminosdelagua.co'


def num(v):
    return f'{v:.2f}'.rstrip('0').rstrip('.')


def box(x, y, w, h):
    return f'--x:{num(x)};--y:{num(y)};--w:{num(w)};--h:{num(h)}'


def parse_inset(inset, w, h):
    """CSS inset shorthand (Figma's image bleed) -> image rect inside a w × h box."""
    v = inset.split()
    v = v * 4 if len(v) == 1 else v * 2 if len(v) == 2 else v + [v[1]] if len(v) == 3 else v
    def px(s, ref):
        return float(s[:-1]) / 100 * ref if s.endswith('%') else float(s.replace('px', ''))
    t, r, b, l = px(v[0], h), px(v[1], w), px(v[2], h), px(v[3], w)
    return l, t, w - l - r, h - t - b


def pl(src, x, y, w, h, inset='0', tf=None, inner=None, cls='deco'):
    """A Figma node: outer box (x, y, w, h); optional rotated inner box `inner` (w, h) centred in it."""
    iw, ih = inner or (w, h)
    ix, iy = x + (w - iw) / 2, y + (h - ih) / 2
    l, t, ww, hh = parse_inset(inset, iw, ih)
    img = f'<img class="pl" src="{src if "/" in src else SVG + src}" alt="" loading="lazy" decoding="async" style="{{}}">'
    if tf:
        return f'<div class="pl {cls}" style="{box(ix, iy, iw, ih)};transform:{tf}">{img.format(box(l, t, ww, hh))}</div>'
    return img.replace('class="pl"', f'class="pl {cls}"').format(box(ix + l, iy + t, ww, hh))


def vline(src, x, y, length, inset='-13px 0', rot='rotate(-90deg)'):
    """A Figma line drawn horizontally then turned upright (box is 0 wide)."""
    return pl(src, x, y, 0, length, inset, rot, (length, 0))


def hline(src, x, y, length, inset='-13px 0', rot=None):
    return pl(src, x, y, length, 0, inset, rot)


S = {}

S['trae'] = [
    pl('icon-aliado.svg', 1414, 264, 128.164, 136, '0 -5.05% -3.68% -5.05%'),
    pl('icon-casas.svg', 872, 187, 215, 96, '0 0 -5.21% 0'),
    pl('icon-lupa.svg', 912, 462, 135.169, 78.179, '0 0 -5.32% -0.24%'),
]

d = 'donde-'
S['donde'] = [
    pl(d + '7b1a4.svg', 1048.5, 770.24, 74, 18.258),
    vline(d + '54039.svg', 1094.65, 526.24, 252, '-2px 0 0 0'),
    vline(d + '31129.svg', 1048.65, 699.24, 92, '-2px 0 0 0'),
    vline(d + '2846b.svg', 1123, 694, 91, '-2px 0 0 0'),
    vline(d + 'b5c96.svg', 1297.65, 539.24, 269, '-2px 0 0 0'),
    pl(d + '7900a.svg', 1017.65, 786.24, 282.5, 22.5, '-2.22% -0.18%'),
    pl(d + '56613.svg', 1087, 519, 13, 13),
    pl(d + '56613.svg', 1087, 765, 13, 13),
    pl(d + 'eab9f.svg', 1292.65, 803.24, 10, 10),
    *[pl(d + '22aaf.svg', x, y, 11, 11) for x, y in [(1042, 783), (1116, 783), (1042, 688), (1116, 688), (1291, 539)]],
    pl(d + '4d716.svg', 1005, 788.5, 14, 0.5, '-0.5px 0', 'rotate(2.05deg)', (14.009, 0)),
    pl(d + 'a7532.svg', 1398.5, 709.5, 560, 31.519, '-1.59% 0'),
    pl(d + 'ab265.svg', 208, 671.5, 1269, 282.5, '-0.37% 0 -0.18% 0'),
    pl(d + 'dd4d7.svg', 963.5, 827, 770.5, 264.5, '-0.33% 0 -0.32% 0'),
    pl(d + '5fdea.svg', -4, 804.59, 224.5, 48.406, '-1.03% 0 -1.01% 0'),
    pl(d + 'd7071.svg', 1009.5, 826.5, 805, 266.5, '-0.37% 0 -0.35% 0'),
]

u = 'usos-'
S['usos'] = [
    vline(u + '8c29e.svg', 698, 232, 529, '-2px -0.76% -8px -0.76%'),
    pl(u + '0dc51.svg', 423, 501, 1, 229, '-100% -1.75% -900.01% -1.75%', 'rotate(-90deg)', (229, 1)),
    vline(u + '857e3.svg', 729, 405, 356, '-2px -1.12% -8px -1.12%'),
    vline(u + '08949.svg', 1260, 410.5, 406.5, '-1px -0.98% -9px -0.98%'),
    pl(u + '54e6a.svg', 1209, 315, 1, 205, '-104.66% -1.95% -900.01% -1.95%', 'rotate(-90deg)', (205, 1)),
    vline(u + 'eb26a.svg', 1417, 264, 276, '-2px -1.45% -8px -1.45%'),
    vline(u + '35f05.svg', 1605.95, 419, 307.875, '-2px -1.3% -8px -1.3%'),
    pl(u + '1f29a.svg', 540.5, 448.38, 858, 33.422, '-6% -0.3% -5.98% -0.32%'),
    pl(u + '51d93.png', 1154.95, 489.88, 129.766, 124.883, '0 0 -4.2% -4.03%', 'rotate(-177.18deg) scale(1,-1)', (124.068, 118.927)),
    pl(u + '97a74.png', 832.61, 631.54, 161.402, 161.402, '0 0 -4.03% -4.03%', 'rotate(-158.02deg) scale(1,-1)', (124, 124)),
    pl(u + 'fad28.png', 994.01, 562.98, 161.402, 161.402, '0 0 -4.03% -4.03%', 'rotate(21.98deg) scale(1,-1)', (124, 124)),
    pl(u + '6a680.png', 698, 733, 136.798, 136.798, '0 0 -4.03% -4.03%', 'rotate(6.27deg) scale(1,-1)', (124, 124)),
    pl(u + 'e0da7.svg', 1468, 471.16, 453, 39.344, '-2.52% -0.24% -2.71% -0.29%'),
    *[pl(u + '56b36.svg', x, y, 14, 14) for x, y in [(416, 495), (690, 226), (721, 401), (1202, 311), (1254, 398), (1409, 257), (1598, 413)]],
    pl(u + 'a6fca.svg', 1, 490.5, 474.5, 46.5, '-3.04% -0.3% -2.15% -0.24%'),
]


def arrows():
    """Arrows over the two water photos, from the Figma frame Final 56. The centre divider and its two stubs
    are now part of the river, so they are left out here."""
    rows = [
        *[('25069', x, y, 0, 205, 0, 205, '-1.22% -18.41px', '') for x, y in [(152.5, 110), (340, 267), (533, 110), (747, 267)]],
        *[('12af0', x, y, 0, 72, 0, 72, '-3.47% -18.41px', '') for x, y in [(139, 658), (326, 716), (411, 622), (523, 663)]],
        ('79f5a', 225, 860, 172.5, 97.476, 172.5, 97.476, '-2.05% -6.33% -2.05% -1.16%', ''),
        ('96fb4', 475, 767, 103, 58, 103, 58, '-3.45% -10.59% -3.45% -1.94%', ''),
        ('96fb4', 359, 806, 103, 58, 103, 58, '-3.45% -10.59% -3.45% -1.94%', ''),
        ('d5a9c', 866, 599, 0, 72, 0, 72, '-3.47% -18.41px', 'rotate(180deg) scale(1,-1)'),
        *[('f770d', x, y, 0, 47, 0, 47, '-3.19% -11.05px', '') for x, y in [
            (1234, 341), (1605, 263), (1549, 356), (1739, 280), (1722, 534), (1631, 716), (1701, 778),
            (1584, 552), (1479, 487), (1813, 658), (1183, 433), (1120, 565), (1214, 681), (1293, 388)]],
        ('d5a9c', 918, 663, 0, 72, 0, 72, '-3.47% -18.41px', 'rotate(180deg) scale(1,-1)'),
        ('3713b', 765, 1099, 172.5, 97.476, 172.5, 97.476, '-2.05% -6.33% -2.05% -1.16%', 'rotate(180deg) scale(1,-1)'),
        ('79f5a', 1061, 516, 172.5, 97.476, 172.5, 97.476, '-2.05% -6.33% -2.05% -1.16%', ''),
        ('96fb4', 1282, 287, 103, 58, 103, 58, '-3.45% -10.59% -3.45% -1.94%', ''),
        ('c4034', 1080, 338.67, 103, 55.332, 103, 55.332, '-3.61% -6.33% -3.62% -1.94%', ''),
        ('3713b', 1572, 619, 172.5, 97.476, 172.5, 97.476, '-2.05% -6.33% -2.05% -1.16%', 'rotate(180deg) scale(1,-1)'),
        ('516eb', 1616, 370, 135, 97, 135, 97, '-2.06% -8.72% -2.06% -1.48%', 'rotate(180deg) scale(1,-1)'),
        ('dcb82', 760, 713, 103, 58, 103, 58, '-3.45% -10.59% -3.45% -1.94%', 'rotate(180deg) scale(1,-1)'),
        ('7b915', 680, 844, 25, 63.5, 25, 63.5, '-3.15% -8% -3.15% -25.46%', ''),
        ('86714', 636, 934, 60.259, 62.995, 15.225, 71.979, '-2.78% -27.83% -2.78% -41.81%', 'rotate(-136.95deg) scale(1,-1)'),
        ('b35a9', 691, 751, 48.677, 70.152, 15.225, 71.979, '-2.08% -9.85% -2.08% -31.36%', 'rotate(-150.52deg) scale(1,-1)'),
        ('6cd44', 1327, 518, 20, 81, 20, 81, '-2.47% -10% -2.47% -31.83%', 'rotate(180deg) scale(1,-1)'),
        ('2f699', 1414, 728, 60.259, 62.995, 15.225, 71.979, '-2.78% -27.83% -2.78% -41.81%', 'rotate(-43.05deg)'),
        ('2e839', 1564.45, 976.54, 112.418, 80.643, 24.585, 116.227, '-2.15% -10.17% -2.15% -32.37%', 'rotate(-59.19deg)'),
        ('a1747', 1350, 421, 65.973, 56.488, 15.225, 71.979, '-2.08% -9.85% -2.08% -31.36%', 'rotate(-128.21deg) scale(1,-1)'),
        ('e4122', 1410.05, 335.37, 35.663, 52.521, 12.92, 52.476, '-2.86% -12.99% -2.86% -36.96%', 'rotate(-152.54deg) scale(1,-1)'),
    ]
    return [pl(f'arrow-{k}.svg', x, y, w, h, ins, tf or None, (iw, ih)) for k, x, y, w, h, iw, ih, ins, tf in rows]


S['agua'] = arrows()

S['footer'] = [
    pl('footer-dde77.svg', 337, 244, 58, 0, '-4px 0'),
]


# ---------- El río: one line from the g of the logo to the footer ----------
# The whole desktop page is one coordinate system 1920 wide: a section starts at the sum of the heights above it.
# The line is built from orthogonal polylines with rounded corners (radius R, as the Figma curves), so an S-bend
# is two corners 2R apart. Each section gets the pieces of line that cross it, in an <svg class="river"> whose
# viewBox is that slice of the page. CSS draws every piece from --rl, the length of river drawn so far (js/site.js).
SECTIONS = [('hero', 1080), ('intro', 1080), ('trae', 1080), ('donde', 1080), ('ha', 540), ('usos', 1080),
            ('porque', 540), ('agua', 1250), ('vive', 2680), ('vision', 2377), ('equipo', 1080), ('valla', 1080),
            ('contacto', 420), ('aliados', 800), ('footer', 291)]
TOP, y0 = {}, 0
for key, h in SECTIONS:
    TOP[key] = y0
    y0 += h
R = 80
RAIL = 131      # the left rail: the lime roots trunk in siete-raices-bg.svg is centred here
MID = 960       # the centre line through "¿Por qué el agua?", the water photos and "¿Cómo se vive?"
# The line takes a colour from the palette in each section, chosen to read on that section's ground, and blends
# into the next one over BLEND page px either side of the boundary. It starts in ink, as the logo.
COLORS = {
    'hero': '#2A2222',      # tinta, as the logo
    'intro': '#5571D1',     # azul
    'trae': '#5571D1',      # azul, as the pills it feeds
    'donde': '#DBF174',     # lima, on the dark aerial photo
    'ha': '#2D4545',        # pino, as "40 ha"
    'usos': '#DBF174',      # lima, on the render
    'porque': '#5571D1',    # azul, as the heading
    'agua': '#9ECFEB',      # cielo, between the two water photos
    'vive': '#3A5930',      # bosque, as the zone text
    'vision': '#2E3E76',    # noche, as "Nuestra Visión"
    'equipo': '#5571D1',    # azul
    'valla': '#5571D1',
    'contacto': '#5571D1',
    'aliados': '#5571D1',
    'footer': '#5571D1',
}
BLEND = 160
ON_PHOTO = {'intro', 'valla'}   # a dark line over a photo gets a light edge
BRANCH_K = 2.5  # side branches draw this many times faster than the river, so they finish while still in view


def P(sec, x, y):
    """A point given in section coordinates, as a page point."""
    return (x, TOP[sec] + y)


class Line:
    """A path of straight segments and circular arcs, with the length at each segment."""
    def __init__(self, x, y):
        self.x, self.y, self.segs, self.len = x, y, [], 0.0

    def _add(self, kind, end, length, bbox, extra=None):
        self.segs.append(dict(kind=kind, a=(self.x, self.y), b=end, at=self.len, len=length, bbox=bbox, extra=extra))
        self.len += length
        self.x, self.y = end

    def line(self, x, y):
        if abs(x - self.x) + abs(y - self.y) < 1e-6:
            return self
        bbox = (min(self.x, x), min(self.y, y), max(self.x, x), max(self.y, y))
        self._add('L', (x, y), math.hypot(x - self.x, y - self.y), bbox)
        return self

    def arc(self, r, sweep, x, y, angle, cx, cy):
        """Arc of radius r around (cx, cy) turning `angle` radians to (x, y). sweep=1 turns clockwise on screen."""
        bbox = (cx - r, cy - r, cx + r, cy + r) if angle > math.pi / 2 + 1e-6 else \
            (min(self.x, x), min(self.y, y), max(self.x, x), max(self.y, y))
        a0 = math.atan2(self.y - cy, self.x - cx)
        self._add('A', (x, y), r * angle, bbox, (r, int(angle > math.pi), sweep, cx, cy, a0))
        return self

    def to(self, *pts, r=R):
        """Orthogonal polyline from the current point through pts, with a corner of radius r at every inner point."""
        pts = [(self.x, self.y)] + [tuple(map(float, p)) for p in pts]
        unit = lambda a, b: ((b[0] - a[0]) / math.dist(a, b), (b[1] - a[1]) / math.dist(a, b))
        for i in range(1, len(pts)):
            a, b = pts[i - 1], pts[i]
            ux, uy = unit(a, b)
            cut_a = r if i > 1 else 0
            cut_b = r if i < len(pts) - 1 else 0
            assert math.dist(a, b) >= cut_a + cut_b - 0.01, ('segment too short for its corners', a, b)
            self.line(b[0] - ux * cut_b, b[1] - uy * cut_b)
            if cut_b:
                vx, vy = unit(b, pts[i + 1])
                assert abs(ux * vx + uy * vy) < 1e-6, ('corners must be square', a, b, pts[i + 1])
                cross = ux * vy - uy * vx
                ex, ey = b[0] + vx * r, b[1] + vy * r
                self.arc(r, 1 if cross > 0 else 0, ex, ey, math.pi / 2, b[0] - ux * r + vx * r, b[1] - uy * r + vy * r)
        return self

    def length_at(self, p):
        """Length along the line to a point that lies on one of its straight segments."""
        for s in self.segs:
            if s['kind'] != 'L':
                continue
            (ax, ay), (bx, by) = s['a'], s['b']
            if abs(math.dist(s['a'], p) + math.dist(p, s['b']) - s['len']) < 0.01:
                return s['at'] + math.dist(s['a'], p)
        raise ValueError(f'{p} is not on a straight part of the line')

    def point_at(self, length):
        """The point at a given length along the line."""
        for s in self.segs:
            if length <= s['at'] + s['len'] or s is self.segs[-1]:
                t = min(max(length - s['at'], 0), s['len'])
                if s['kind'] == 'L':
                    (ax, ay), (bx, by) = s['a'], s['b']
                    return ax + (bx - ax) * t / s['len'], ay + (by - ay) * t / s['len']
                r, _, sweep, cx, cy, a0 = s['extra']
                a = a0 + (t / r if sweep else -t / r)   # sweep=1 is clockwise on screen: the angle grows
                return cx + r * math.cos(a), cy + r * math.sin(a)

    def d(self, segs):
        out = [f'M{num(segs[0]["a"][0])} {num(segs[0]["a"][1])}']
        for s in segs:
            x, y = map(num, s['b'])
            if s['kind'] == 'L':
                out.append(f'L{x} {y}')
            else:
                r, large, sweep = s['extra'][:3]
                out.append(f'A{num(r)} {num(r)} 0 {large} {sweep} {x} {y}')
        return ''.join(out)


class Branch(Line):
    """A side line that leaves its parent tangentially at `start` and draws BRANCH_K times faster."""
    def __init__(self, parent, start, k=BRANCH_K):
        super().__init__(*start)
        if isinstance(parent, Branch):
            self.from_main = parent.from_main + parent.length_at(start) / parent.k
        else:
            self.from_main = parent.length_at(start)
        self.k = k


# The g of the logo: viewBox 170 85 475 425 drawn 770 wide at (656, 244). The river channel in the g (mask
# cdaMaskRio in cargo/logo-corriente.html) ends in a straight cut from (320.44, 472.48) to (306.15, 481.75).
# The line starts flush on that cut, as wide as the channel and square to it, then curls left and down.
LS = 770 / 475
CUT = ((320.44, 472.48), (306.15, 481.75))
cut_w = math.dist(*CUT)                                            # 17.03 logo units: the channel width
gx = 656 + ((CUT[0][0] + CUT[1][0]) / 2 - 170) * LS
gy = 244 + ((CUT[0][1] + CUT[1][1]) / 2 - 85) * LS
tx, ty = (CUT[0][1] - CUT[1][1]) / cut_w, (CUT[1][0] - CUT[0][0]) / cut_w   # square to the cut, out of the g
assert tx < 0 and ty < 0
STROKE = cut_w * LS                                                # 27.6 px: the river is as wide as the g's channel
CURL = 40
ccx, ccy = gx + ty * CURL, gy - tx * CURL                          # centre of a left turn
turn = (math.atan2(ty, tx) - math.pi / 2) % (2 * math.pi)          # from the tail's heading round to straight down
G_X = ccx - CURL

river = Line(gx, gy).arc(CURL, 0, G_X, ccy, turn, ccx, ccy)
A, B, C = G_X, G_X + 209, 1228       # intro S-bends, ending on the trunk of "¿Qué te trae por aquí?"
ib = lambda y: P('intro', 0, y)[1]
river.to(
    (A, ib(132)), (B, ib(132)), (B, ib(292)), (A, ib(292)), (A, ib(452)), (B, ib(452)), (B, ib(292)), (C, ib(292)),
    P('trae', C, 860.5), P('trae', RAIL, 860.5),                    # trunk, then left behind "Explora el proyecto"
    P('porque', RAIL, 80), P('porque', MID, 80),                    # down the rail, across "¿Por qué el agua?"
    P('vision', MID, 80), P('vision', RAIL, 80),                    # down the centre of the water and the four zones
    P('footer', RAIL, 291 + 40),                                    # the rail, past the roots, the team and the allies,
)                                                                   # and off the bottom of the page
TOTAL = river.len

branches = []


def branch(parent, start, *pts, k=BRANCH_K):
    b = Branch(parent, start, k).to(*pts)
    branches.append(b)
    return b


# ¿Qué te trae por aquí?: the trunk feeds the three pills; "Quiero conocer" also feeds "Contáctanos"
branch(river, P('trae', C, 269.5), P('trae', C, 349.5), P('trae', 1123, 349.5))
branch(river, P('trae', C, 390.5), P('trae', C, 470.5), P('trae', 1335, 470.5))
branch(river, P('trae', C, 526.5), P('trae', C, 606.5), P('trae', 657, 606.5))

# ¿Quién está detrás?: a line from the rail through the three group pills, one stem per group between its tiles
EQ_BUS, EQ_GX, EQ_W = 270, (230, 786.5, 1343), 347
stems = [gx + EQ_W / 2 for gx in EQ_GX]
stem_end = (771, 670, 890)
bus = branch(river, P('equipo', RAIL, EQ_BUS - R), P('equipo', RAIL, EQ_BUS), P('equipo', stems[2], EQ_BUS),
             P('equipo', stems[2], stem_end[2]))
for sx, end in zip(stems[:2], stem_end[:2]):
    branch(bus, P('equipo', sx - R, EQ_BUS), P('equipo', sx, EQ_BUS), P('equipo', sx, end))

# Contáctenos: a branch to the form
CT_BUS = 270
branch(river, P('contacto', RAIL, CT_BUS - R), P('contacto', RAIL, CT_BUS), P('contacto', 1373, CT_BUS))

# Nuestros aliados: a line along the six tiles, the last stem runs on to "¡Únete a nuestro proyecto!"
AL_BUS, AL_TILES = 224, [230 + i * 262 + 75 for i in range(6)]
al = branch(river, P('aliados', RAIL, AL_BUS - R), P('aliados', RAIL, AL_BUS), P('aliados', AL_TILES[-1], AL_BUS),
            P('aliados', AL_TILES[-1], 690))
for cx in AL_TILES[:-1]:
    branch(al, P('aliados', cx - R, AL_BUS), P('aliados', cx, AL_BUS), P('aliados', cx, 452))



def river_svg(sec):
    """The pieces of river that cross a section, as an inline SVG over that slice of the page."""
    top, h = TOP[sec], dict(SECTIONS)[sec]
    lo, hi = top - 30, top + h + 30
    hits = lambda s: s['bbox'][1] <= hi and s['bbox'][3] >= lo
    paths = []

    def pieces(line, at0, k):
        run = []
        for s in line.segs + [None]:
            if s and hits(s):
                run.append(s)
                continue
            if run:
                length = sum(x['len'] for x in run)
                style = f'--a:{num(at0 + run[0]["at"] / k)};--l:{num(length)}' + (f';--k:{k}' if k != 1 else '')
                paths.append(f'<path d="{line.d(run)}" pathLength="{num(length)}" style="{style}"/>')
                run = []

    pieces(river, 0, 1)
    for b in branches:
        pieces(b, b.from_main, b.k)
    if sec in ON_PHOTO:
        # Over photos the line gets a light edge, drawn with it, so it reads on dark ground too
        paths[:0] = [p.replace('<path ', '<path class="rv-case" ') for p in paths]
    if sec == 'vision':
        # The lime roots trunk in siete-raices-bg.svg starts at the top edge; hide the stub above the river's corner
        paths.insert(0, f'<rect x="117" y="{top}" width="28" height="{R * 2}" fill="#9ECFEB"/>')
    return (f'<svg class="river deco" viewBox="0 {top} 1920 {h}" preserveAspectRatio="none" aria-hidden="true" focusable="false">'
            + ''.join(paths) + '</svg>')


def scroll_map(lag=.35, step=4, tol=.5):
    """For js/site.js: pairs (length, scroll target) telling how much river to draw for a scroll position.
    The scroll target is the page y the reader has reached. Going down, the line is drawn to where the reader is.
    Where the line runs sideways or up, the target still moves on `lag` page px per px of line, so a horizontal
    run draws over some scroll instead of all at once. Collinear samples are dropped (within `tol` px)."""
    pts, yt = [], None
    n = int(TOTAL // step)
    for i in range(n + 2):
        length = min(i * step, TOTAL)
        y = river.point_at(length)[1]
        yt = y if yt is None else max(yt + lag * (length - pts[-1][0]), y)
        pts.append((length, yt))
    keep = [pts[0]]
    j0 = 0
    for j in range(2, len(pts)):
        (l0, v0), (l1, v1) = pts[j0], pts[j]
        if any(abs(v0 + (v1 - v0) * (pts[k][0] - l0) / (l1 - l0) - pts[k][1]) > tol for k in range(j0 + 1, j)):
            keep.append(pts[j - 1])
            j0 = j - 1
    keep.append(pts[-1])
    return '[' + ','.join(f'{num(l)},{num(v)}' for l, v in keep) + ']'


def river_ref():
    """The colour gradient every river piece strokes with, and the scroll map for js/site.js. The gradient is in
    page coordinates, so it runs on unbroken from one section's SVG to the next."""
    stops = [(0, COLORS[SECTIONS[0][0]])]
    for (a, _), (b, _) in zip(SECTIONS, SECTIONS[1:]):
        stops += [(TOP[b] - BLEND, COLORS[a]), (TOP[b] + BLEND, COLORS[b])]
    stops.append((y0, COLORS[SECTIONS[-1][0]]))
    stops = ''.join(f'<stop offset="{y / y0:.5f}" stop-color="{c}"/>' for y, c in stops)
    return (f'<svg class="river-ref" width="0" height="0" aria-hidden="true" focusable="false">'
            f'<defs><linearGradient id="rv-color" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="{y0}">'
            f'{stops}</linearGradient></defs></svg>'
            f'<script type="application/json" id="river-map">{scroll_map()}</script>')


def logo_svg():
    """The Corriente logo (SVG + CSS animation) from the Cargo snippet, without its Cargo wrapper."""
    src = (root / 'cargo/logo-corriente.html').read_text()
    svg = re.search(r'<svg.*?</svg>', src, re.S).group(0)
    return svg.replace(' role="img" aria-label="Caminos del Agua"', ' aria-hidden="true" focusable="false"')


def cards_js():
    IMG = {f'raiz-{n}': f'img/cards/{n}.webp' for n in range(1, 8)}
    IMG['siete-raices-bg'] = 'img/siete-raices-bg.svg'
    data = (root / 'assets/cards-data.js').read_text().replace('window.CARDS =', 'const CARDS =')
    src = (root / 'cargo/siete-raices.src.html').read_text()
    js = re.search(r'<script>\n(.*)</script>', src, re.S).group(1)
    js = js.replace('/*@IMG@*/', json.dumps(IMG)).replace('/*@CARDS@*/', data.strip())
    return '/* Generated by build.py from cargo/siete-raices.src.html and assets/cards-data.js */\n' + js


html = (here / 'index.src.html').read_text()
for key, parts in S.items():
    html = html.replace(f'<!--@pl:{key}@-->', '\n'.join(parts))
html = html.replace('<!--@logo@-->', logo_svg()).replace('@SITE@', SITE)


def add_srcset(html):
    """Photos that have a lighter img/<name>-800.webp version get srcset and sizes, so phones download that one.
    sizes: full width under 900 px; on desktop, the image's width on the 1920 frame (--w) as a share of the window."""
    def one(m):
        tag, name = m.group(0), m.group(1)
        small = here / f'img/{name}-800.webp'
        if not small.exists() or 'srcset=' in tag:
            return tag
        full_w = int(re.search(r'width="(\d+)"', tag).group(1))
        w = float(re.search(r'--w:([\d.]+)', tag).group(1))
        sizes = f'(max-width: 899px) 100vw, {round(w / 19.2)}vw'
        srcset = f'img/{name}-800.webp 800w, img/{name}.webp {full_w}w'
        return tag.replace(f'src="img/{name}.webp"', f'src="img/{name}.webp" srcset="{srcset}" sizes="{sizes}"')
    return re.sub(r'<img [^>]*src="img/([a-z0-9-]+)\.webp"[^>]*>', one, html)


html = add_srcset(html)
# The first photo (largest paint on load) is preloaded: the preload must offer the same choice of files
m = re.search(r'src="img/walk-photo\.webp" srcset="([^"]+)" sizes="([^"]+)"', html)
html = html.replace('href="img/walk-photo.webp" fetchpriority="high"><!--@srcset-preload@-->',
                    f'href="img/walk-photo.webp" imagesrcset="{m.group(1)}" imagesizes="{m.group(2)}" fetchpriority="high">')
for key, h in SECTIONS:
    html = html.replace(f'<!--@river:{key}@-->', river_svg(key))
    if key != 'vision':   # the Siete Raíces cards keep their own 1920:2377 frame
        assert re.search(rf'data-river="{key}"[^>]*--h:{h}"', html), f'section {key} should be {h} tall'
html = html.replace('@RIVER_COLORS@', json.dumps(COLORS).replace('"', '&quot;'))
html = html.replace('<!--@river-ref@-->', river_ref()).replace('@RIVER_TOTAL@', num(TOTAL)).replace('@RIVER_W@', num(STROKE))
(here / 'js/siete-raices.js').write_text(cards_js())
# Version the CSS and JS links by content, so a new build is never served from a stale cache
for asset in ('css/site.css', 'js/site.js', 'js/siete-raices.js', 'favicon.svg'):
    v = hashlib.sha1((here / asset).read_bytes()).hexdigest()[:8]
    html = html.replace(f'"{asset}"', f'"{asset}?v={v}"')
left = re.findall(r'<!--@[^>]*@-->', html)
assert not left, left
(here / 'index.html').write_text(html)
print('index.html', len(html), 'bytes')
