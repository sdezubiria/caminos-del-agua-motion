"""Builds cargo/siete-raices-cards.html: the Siete Raíces cards as one Cargo page snippet, with the card data inlined
and the photos + roots background pointing at the copies uploaded to the Cargo page."""
import json, pathlib, re

root = pathlib.Path(__file__).resolve().parent.parent
FREIGHT = 'https://freight.cargo.site/t/original/i/'
IMG = {
    'raiz-1': FREIGHT + 'D3202116609913391403731144748282/cda-raiz-1.jpg',
    'raiz-2': FREIGHT + 'R3202116609931838147804854299898/cda-raiz-2.jpg',
    'raiz-3': FREIGHT + 'Z3202116609950284891878563851514/cda-raiz-3.jpg',
    'raiz-4': FREIGHT + 'B3202116609968731635952273403130/cda-raiz-4.jpg',
    'raiz-5': FREIGHT + 'X3202116609987178380025982954746/cda-raiz-5.jpg',
    'raiz-6': FREIGHT + 'F3202116610005625124099692506362/cda-raiz-6.jpg',
    'raiz-7': FREIGHT + 'S3202116610024071868173402057978/cda-raiz-7.jpg',
    'siete-raices-bg': FREIGHT + 'W3202116610042518612247111609594/cda-siete-raices-bg.svg',
}
data = (root / 'assets/cards-data.js').read_text().replace('window.CARDS =', 'const CARDS =')
src = (root / 'cargo/siete-raices.src.html').read_text()
out = src.replace('/*@IMG@*/', json.dumps(IMG)).replace('/*@CARDS@*/', data.strip())
assert '</script' not in data
# Cargo's editor turns runs of spaces into non-breaking spaces, which CSS doesn't read as whitespace
# (the first declaration on every indented line gets dropped). Strip indentation and collapse runs of spaces.
out = '\n'.join(re.sub(r' {2,}', ' ', line.strip()) for line in out.splitlines())
(root / 'cargo/siete-raices-cards.html').write_text(out)
print(len(out))
