"""Builds prototipo/index.html from index.src.html, and js/siete-raices.js from the Cargo card snippet.

Each section is laid out on the 1920 px Figma frame (file "Caminos del Agua", frames Final 49 to Final 63).
`pl()` places one Figma vector or image at its frame coordinates; CSS scales the frame with the page width.
On narrow screens the line art (class "deco") is hidden and the sections reflow (see css/site.css)."""
import hashlib, json, pathlib, re

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


# The lime line that runs down the left of several sections (Figma "Ellipse 1167")
def lime(x_left, top):
    return pl('green-bar.svg', x_left - 13, top, 149.999, 2876)


S = {}

S['intro'] = [
    pl('river-line.svg', 977, 52, 319, 1704, '0 -4.08%'),
    pl('river-dot.svg', 964, 39, 26, 26),
]

S['trae'] = [
    pl('icon-aliado.svg', 1414, 264, 128.164, 136, '0 -5.05% -3.68% -5.05%'),
    pl('trae-lines.svg', 559, -1137, 748.671, 1998, '0 0 -0.65% 0'),
    pl('icon-casas.svg', 878, 187, 215, 96, '0 0 -5.21% 0'),
    pl('icon-lupa.svg', 906, 462, 135.169, 78.179, '0 0 -5.32% -0.24%'),
]

d = 'donde-'
S['donde'] = [lime(93, -0.44)] + [
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

S['ha'] = [lime(93, -2006.44)]

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
    lime(101, -2538),
]

S['porque'] = [
    pl('water-curve.svg', 673, -2444, 149.999, 2876),
    pl('water-curve-end.svg', 822.9, 419, 136.7, 137.1, '0 0 -9.52% -9.49%', 'rotate(-90deg) scale(-1,1)'),
]


def arrows():
    """Arrows over the two water photos, from the Figma frame Final 56 (notes in s7-arrows.txt format)."""
    rows = [
        ('b20d0', 960, 964, 0, 618, 0, 618, '0 -13px', ''),
        ('1b375', 765, 1056, 101, 0, 0, 101, '0 -13px', 'rotate(90deg)'),
        ('3d8a2', 1061, 874, 59, 0, 0, 59, '0 -13px', 'rotate(90deg)'),
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


S['agua'] = [
    pl('divider-a.svg', 948, -679, 113, 1566.06),
    pl('divider-b.svg', 865.9, -413, 94.1, 1461.6, '0 0 -0.88% -13.83%', 'scale(-1,1)'),
] + arrows()

# ¿Cómo se vive? Figma "Final 64" sits 213 px down inside "Final 57"
V = 213
v = 'vive-'
band =lambda src, x, top, tf, w=1014: pl(v + src, x, top + V, w, 132, '0 0 -1.28% -9.85%', tf, (132, w))
S['vive-lines'] = [
    pl(v + 'ad93b.svg', 844, 2027 + V, 257.5, 136.62, '0', 'rotate(-180deg) scale(-1,1)'),
]
S['vive-lines-2'] = [
    pl(v + '73613.svg', 213, 2390 + V, 615, 0, '0 -13px', 'rotate(90deg)', (0, 615)),
    pl(v + '99f88.svg', 831.9, 1418 + V, 257.5, 136.62, '0', 'rotate(180deg)'),
    pl(v + 'ad93b.svg', 844, 850 + V, 257.5, 136.62, '0', 'rotate(-180deg) scale(-1,1)'),
    pl(v + '99f88.svg', 812.9, 216 + V, 257.5, 136.62, '0', 'rotate(180deg)'),
    pl(v + '17ba7.svg', 828.1, 1575 + V, 131.9, 814.4, '0 0 -1.6% -9.85%', 'scale(-1,1)'),
]
S['vive-lines-3'] = [
    band('6db94.svg', 954, 860, 'rotate(90deg)', 1002),
    band('c65df.svg', -54, 1423, 'rotate(-90deg) scale(-1,1)'),
]
S['vive-lines-4'] = [
    band('c65df.svg', -54, 228, 'rotate(-90deg) scale(-1,1)'),
    band('6db94.svg', 960, 2032, 'rotate(90deg)'),
    band('4e7af.svg', -54, 2356, 'rotate(-90deg)'),
    pl(v + '4f413.svg', 960, V, 0, 2356, '0 -13px'),
    pl('river-black.svg', 105, 2488 + V, 319, 1065, '0 -4.08%', 'scale(-1,1)'),
]

e = 'equipo-'
corner = lambda src, x, y, tf, s=126: pl(e + src, x, y, s, s, '0 0 -10.32% -10.32%', tf)
S['equipo'] = [
    hline(e + '3b459.svg', 760, 771, 78.5),
    vline(e + 'ae12f.svg', 1540, 361, 456),
    corner('da9d0.svg', 1540, 468, 'rotate(90deg) scale(-1,1)'),
    corner('da9d0.svg', 1540, 618, 'rotate(90deg) scale(-1,1)'),
    corner('a3e9a.svg', 1414.1, 816, 'scale(-1,1)'),
    corner('4308e.svg', 1417, 233, 'rotate(-89.21deg) scale(-1,1)', 127.73),
    corner('4308e.svg', 889.9, 233, 'rotate(-89.21deg) scale(-1,1)', 127.73),
    pl(e + '20f4d.svg', 145.9, 107, 126.1, 126.1, '0 0 -10.32% -10.32%'),
    hline(e + 'dd966.svg', 272, 233, 1147, '-13px 0', 'rotate(180deg)'),
    vline(e + '2069f.svg', 146, -30, 137, rot='rotate(90deg)'),
    pl('tree-left.svg', 268, 212, 252, 511, '0 0 -2.54% 0'),
    corner('da9d0.svg', 1016.1, 607, 'rotate(90deg) scale(-1,1)'),
    corner('32a61.svg', 889.9, 664, 'rotate(-90deg)'),
    corner('4b630.svg', 1414, 430, 'rotate(-90deg)'),
    vline(e + '54cd3.svg', 1016, 373, 302),
]

S['contacto'] = [
    pl('contacto-20f4d.svg', 130, 179, 126, 126, '0 0 -10.32% -10.32%'),
    hline('contacto-ddee5.svg', 256, 305, 1178, '-13px 0', 'rotate(180deg)'),
    vline('contacto-dd320.svg', 130, 0, 179, rot='rotate(90deg)'),
    vline('contacto-715c2.svg', 130, 180, 399, rot='rotate(90deg)'),
]

a = 'aliados-'
S['aliados'] = [
    pl(a + '20f4d.svg', 130, 98, 126, 126, '0 0 -10.32% -10.32%'),
    hline(a + 'ddee5.svg', 256, 224, 1178, '-13px 0', 'rotate(180deg)'),
    vline(a + '9a835.svg', 1558, 351, 389),
    vline(a + 'dd320.svg', 130, -81, 179, rot='rotate(90deg)'),
    *[pl(a + '4308e.svg', x, 224, 127.73, 127.73, '0 0 -10.32% -10.32%', 'rotate(-89.21deg) scale(-1,1)')
      for x in (1431.9, 1103, 899.9, 697, 494, 292)],
]

S['footer'] = [
    pl('footer-dde77.svg', 139, 244, 58, 0, '-4px 0'),
]


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
(here / 'js/siete-raices.js').write_text(cards_js())
# Version the CSS and JS links by content, so a new build is never served from a stale cache
for asset in ('css/site.css', 'js/site.js', 'js/siete-raices.js'):
    v = hashlib.sha1((here / asset).read_bytes()).hexdigest()[:8]
    html = html.replace(f'"{asset}"', f'"{asset}?v={v}"')
left = re.findall(r'<!--@[^>]*@-->', html)
assert not left, left
(here / 'index.html').write_text(html)
print('index.html', len(html), 'bytes')
