"""Builds cargo/logo-corriente.html: the Corriente logo animation as a Cargo page snippet (SVG + CSS, no JS)."""
import json, pathlib, re

root = pathlib.Path(__file__).resolve().parent.parent
src = (root / 'assets/logo-data.js').read_text()
L = json.loads(re.search(r'=\s*(\{.*\})\s*;', src, re.S).group(1))

ORDER = ['c', 'a1', 'big', 'i', 'dot', 'n', 'o', 'tri', 'del', 'a3l', 'u', 'a3r']
def piece(k, a=''):
    return f'<polygon points="{L["tri"]}"{a}/>' if k == 'tri' else f'<path d="{L[k]}"{a}/>'
# Centre line of the river inside the logo: right leg of the "m" -> S -> stem and tail of the "g"
ROUTE = 'M596.8 168 L596.8 214 Q596.8 249.6 556 249.6 L444.7 249.6 A21.6 21.6 0 0 0 444.7 292.6 L484.5 292.6 A21.6 21.6 0 0 1 484.5 335.8 L412 335.8 Q390.2 335.8 390.2 360 L390.2 452 Q390.2 494 352 498 Q324 500 309 482'
ink = ''.join(piece(k) for k in ORDER)
mask = piece('big', ' fill="#fff"') + piece('tri', ' fill="#fff"')
flows = ''.join(f'<path class="cda-flow cda-f{i}" d="{ROUTE}"/>' for i in (1, 2))

html = f'''<div class="cda-logo"><svg viewBox="170 85 475 425" role="img" aria-label="Caminos del Agua"><defs><mask id="cdaMaskRio" maskUnits="userSpaceOnUse" x="150" y="60" width="520" height="480">{mask}</mask></defs><g class="cda-ink">{ink}</g><g mask="url(#cdaMaskRio)">{flows}</g></svg></div>
<style>
/* Corriente: the river inside the logo flows on a loop at 1.8x (4.4s / 1.8) */
.cda-logo {{ position: absolute; left: 0; right: 0; top: 0; height: var(--viewport-height, 100svh); display: grid; place-items: center; pointer-events: none; z-index: 1; }}
.cda-logo svg {{ width: min(84vw, calc(52vh * 475 / 425)); height: auto; overflow: visible; }}
.cda-logo .cda-ink {{ fill: #2A2222; }}
.cda-flow {{ fill: none; stroke-width: 36; stroke-linecap: round; stroke-linejoin: round; animation: 2.444s linear infinite; }}
.cda-f1 {{ stroke: #5571D1; stroke-dasharray: 150 170; animation-name: cdaFlowA; }}
.cda-f2 {{ stroke: #9ECFEB; stroke-dasharray: 60 260; animation-name: cdaFlowB; }}
@keyframes cdaFlowA {{ from {{ stroke-dashoffset: 0; }} to {{ stroke-dashoffset: -320; }} }}
@keyframes cdaFlowB {{ from {{ stroke-dashoffset: -60; }} to {{ stroke-dashoffset: -380; }} }}
@media (prefers-reduced-motion: reduce) {{ .cda-flow {{ animation-play-state: paused; }} }}
</style>'''
(root / 'cargo/logo-corriente.html').write_text(html)
print(len(html))
