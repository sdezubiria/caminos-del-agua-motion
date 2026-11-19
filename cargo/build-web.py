#!/usr/bin/env python3
"""Build cargo/web.html: the HTML prototype (prototipo/index.html) as one Cargo page.

Paste web.html into the page's HTML code view in Cargo and click Update. It holds:
- the prototype's page markup, minified, inside <div class="cda-web">. Real HTML, so search engines and AI
  crawlers read the text without running scripts;
- prototipo/css/site.css scoped to .cda-web (selectors prefixed, :root/body moved onto .cda-web, .page
  renamed .cda-page because Cargo uses .page for its own pages);
- cargo/web.src.js, the Cargo version of prototipo/js/site.js.
Images and the Siete Raíces script load from jsDelivr, which serves the GitHub repo at a pinned commit (BASE).
Rebuild after `python3 prototipo/build.py`, and push the prototype first if images changed.

Cargo saves the page's live HTML and turns runs of spaces into non-breaking spaces, so the output has no
indentation and no double spaces outside <pre>. Run: python3 cargo/build-web.py [commit] [--site ID]
--site builds the same page for another Cargo site: the form sends with that site's id (Cargo mails it to the
recipient set in that site's Publish Settings > Contact Form) and the output is web-ID.html.
"""
import hashlib
import html as html_lib
import json
import re
import subprocess
import sys
from pathlib import Path

here = Path(__file__).resolve().parent
root = here.parent
proto = root / 'prototipo'

DEFAULT_SITE = 3758984   # 449156.cargo.site
args = sys.argv[1:]
site_id = DEFAULT_SITE
if '--site' in args:
    i = args.index('--site')
    site_id = int(args[i + 1])
    del args[i:i + 2]
commit = args[0] if args else subprocess.run(
    ['git', '-C', str(root), 'rev-parse', 'origin/prototipo-web'], capture_output=True, text=True, check=True).stdout.strip()
BASE = f'https://cdn.jsdelivr.net/gh/sdezubiria/caminos-del-agua-motion@{commit}/prototipo/'

html = (proto / 'index.html').read_text()
head = html[:html.index('<body>')]
body = html[html.index('<body>') + len('<body>'):html.index('</body>')]

# ---------- Markup ----------
body = re.sub(r'<script src="[^"]*"[^>]*></script>\s*', '', body)
body = re.sub(r'<!--.*?-->', '', body, flags=re.S)
body = body.replace('<div class="page"', '<div class="cda-page"', 1)
# The menu opens as a popover, in the top layer: Cargo's `contain: layout` would trap a fixed element (web.src.js)
body = body.replace('<nav class="menu" id="menu"', '<nav class="menu" id="menu" popover="manual"', 1)
assert 'popover="manual"' in body
# Cargo's published HTML cuts attributes that hold escaped quotes (data-river-colors arrives as "{"), so the
# river colours move into a JSON script tag, which Cargo leaves alone (like #river-map)
m = re.search(r' data-river-colors="([^"]*)"', body)
colors = html_lib.unescape(m.group(1))
json.loads(colors)
body = body[:m.start()] + body[m.end():]
body = body.replace('<main id="contenido">', '<script type="application/json" id="river-colors">' + colors + '</script>\n<main id="contenido">', 1)
assert 'id="river-colors"' in body and '&quot;' not in body
assert '<div class="cda-page"' in body


def absolute(url):
    return url if re.match(r'^(https?:|data:|#|mailto:|tel:)', url) else BASE + re.sub(r'\?v=[0-9a-f]+$', '', url)


body = re.sub(r'(\s(?:src|href)=")([^"]+)(")', lambda m: m.group(1) + absolute(m.group(2)) + m.group(3), body)
body = re.sub(r'(\ssrcset=")([^"]+)(")', lambda m: m.group(1) + ', '.join(
    ' '.join([absolute(p.split()[0])] + p.split()[1:]) for p in m.group(2).split(',')) + m.group(3), body)

# The form sends for real on Cargo: drop the prototype's notice and placeholder thank-you text
body = re.sub(r'<p class="form-note">.*?</p>\s*', '', body, flags=re.S)
body = re.sub(r'(<p class="form-ok" role="status" hidden>).*?(</p>)', r'\1\2', body, flags=re.S)
assert 'form-note' not in body and 'Prototipo' not in body

# Google Fonts, as in the prototype's <head>
fonts = re.search(r'<link rel="stylesheet" href="(https://fonts\.googleapis\.com/[^"]+)"', head).group(1)

# Structured data from the prototype's <head>, pointed at the Cargo address (files at jsDelivr)
PROTO_SITE = re.search(r"^SITE = '([^']+)'", (proto / 'build.py').read_text(), re.M).group(1)
CARGO_SITE = 'https://www.caminosdelagua.com.co'   # the client's domain; connect it in Cargo > Settings > Domain
ld = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', head, re.S).group(1))
ld = json.loads(json.dumps(ld, ensure_ascii=False)
                .replace(PROTO_SITE + '/favicon.svg', BASE + 'favicon.svg')
                .replace(PROTO_SITE + '/img/', BASE + 'img/')
                .replace(PROTO_SITE, CARGO_SITE))
jsonld = '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False, separators=(',', ':')) + '</script>'


def squeeze(s):
    """No indentation and no runs of spaces (Cargo would turn them into non-breaking spaces)."""
    s = re.sub(r'[ \t]*\n[ \t\n]*', '\n', s)
    return re.sub(r' {2,}', ' ', s).strip()


def no_space_before_breaks(s):
    """Cargo also turns a space just before a tag into a non-breaking space. Before <br> (and before the
    arrows, which sit outside the text flow) that space is invisible in the prototype, but as a
    non-breaking space it takes width and can push a label onto another line. Drop it."""
    return re.sub(r' +(<br\b|<span aria-hidden="true")', r'\1', s)


# ---------- CSS ----------
css = (proto / 'css/site.css').read_text()
css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
css = css.replace(':root {', '.cda-web {', 1)
css = re.sub(r'\nhtml \{[^}]*\}', '', css)                      # scroll-behavior: the script scrolls smoothly itself
css = re.sub(r'(@media[^{]*\{\s*)html \{[^}]*\}', r'\1', css)
css = css.replace('\nbody {', '\n.cda-web {', 1)
css = re.sub(r'\.js \.page\b', '.cda-web.js .cda-page', css)
css = re.sub(r'\.page\b', '.cda-page', css)


def prefix(sel):
    sel = sel.strip()
    if sel.startswith('.cda-web'):
        return sel
    return '.cda-web ' + sel


def scope(block):
    """Prefix every selector with .cda-web, recursing into @media / @container / @supports."""
    out, i = [], 0
    while i < len(block):
        j = block.find('{', i)
        if j < 0:
            out.append(block[i:])
            break
        sel = block[i:j].strip()
        depth, k = 1, j + 1
        while depth:
            depth += {'{': 1, '}': -1}.get(block[k], 0)
            k += 1
        inner = block[j + 1:k - 1]
        if sel.startswith(('@media', '@container', '@supports')):
            out.append(f'{sel}{{{scope(inner)}}}')
        elif sel.startswith('@'):
            out.append(f'{sel}{{{inner}}}')
        else:
            out.append(','.join(prefix(s) for s in sel.split(',')) + '{' + inner + '}')
        i = k
    return '\n'.join(o.strip() for o in out if o.strip())


css = scope(css)
# Cargo sizes every element in a page with `bodycopy * { font-size: calc(var(--font-scale) * var(--font-size)) }`.
# Inside the wrapper, elements inherit as in a plain page; the prototype's own rules (.cda-web .x) still win.
css += '''
.cda-web{margin:0;line-height:normal;font-size:16px;text-align:left}
.cda-web *{font-size:inherit}
.cda-web .form-ok.error{background:#fff;color:#9b1c1c}
.cda-web .menu[popover]{margin:0;width:auto;height:auto;max-width:none;max-height:none;border:0;color:inherit}
'''
css = squeeze(css)

# ---------- Script ----------
js = (here / 'web.src.js').read_text()
js = re.sub(r'^/\*.*?\*/\n', '', js, flags=re.S)

# The CSS goes in through a script at the top of the page, not a <style> element: on the published site Cargo
# HTML-escapes quotes and > inside <style> (' becomes &#x27;), which breaks the CSS. Script text is left alone.
# It runs before the markup below is parsed, so nothing shows unstyled. In the editor it only touches <head>,
# which Cargo doesn't save.
css_loader = ('<script>(function(){var s=document.getElementById("cda-web-css")||document.createElement("style");'
              's.id="cda-web-css";s.textContent=' + json.dumps(css, ensure_ascii=False) + ';'
              'if(!s.parentNode)document.head.appendChild(s);})();</script>')
assert '</' not in css
page = f'<link rel="stylesheet" href="{fonts}">\n{jsonld}\n{css_loader}\n<div class="cda-web">\n{no_space_before_breaks(squeeze(body))}\n</div>'
assert 'const SITE_ID = 3758984;' in js
js = js.replace('const SITE_ID = 3758984;', f'const SITE_ID = {site_id};')
version = hashlib.sha1((page + js + BASE).encode()).hexdigest()[:10]
js = js.replace('@VERSION@', version).replace('@BASE@', BASE)
assert '  ' not in page and '\t' not in page, 'double spaces left in the markup'
out = f'{page}\n<script>\n{squeeze(js)}\n</script>\n'
name = 'web.html' if site_id == DEFAULT_SITE else f'web-{site_id}.html'
(here / name).write_text(out)
print(f'{name} {len(out.encode())} bytes · site {site_id} · version {version} · {BASE}')
