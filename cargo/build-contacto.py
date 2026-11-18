"""Builds the Contáctenos/aliados Cargo snippets from contacto.src.html, one per page (they differ only in data-cda):
contacto.html (desktop page 13), aliados.html (desktop page 14), movil.html (mobile page 15),
enlaces.html (appended to page 3, desktop and mobile, so its #formulario links work)."""
import hashlib, pathlib, re

here = pathlib.Path(__file__).resolve().parent
src = (here / 'contacto.src.html').read_text()
# Cargo's editor turns runs of spaces into non-breaking spaces; strip indentation and collapse runs of spaces.
src = '\n'.join(re.sub(r' {2,}', ' ', line.strip()) for line in src.splitlines())
src = src.replace('@VERSION@', hashlib.sha1(src.encode()).hexdigest()[:10], 1)
for name in ('contacto', 'aliados', 'movil', 'enlaces'):
    out = src.replace('@SECTION@', name, 1)
    (here / f'{name}.html').write_text(out)
    print(name, len(out))
