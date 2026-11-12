# Caminos del Agua · Prototipo web

One-page HTML prototype of the site, built from the Figma file *Caminos del Agua* (frames Final 49 to Final 63). It uses the animated Corriente logo and the Siete Raíces cards from the motion lab.

## Files

- `index.html`: the page. It's generated, so don't edit it by hand.
- `index.src.html`: the page source with the text, sections and SEO tags. Edit this one.
- `build.py`: writes `index.html` and `js/siete-raices.js`. Run `python3 build.py` after any change.
- `css/site.css`: styles. On desktop each section is its 1920 px Figma frame, scaled to the window. Under 900 px it becomes one column.
- `js/site.js`: section menu and contact form.
- `js/siete-raices.js`: the Siete Raíces cards, built from `../cargo/siete-raices.src.html` and `../assets/cards-data.js`.
- `img/`: photos as WebP, Figma line art in `img/svg/`, `og-image.jpg` for link previews. `img/raw/` keeps the original PNG exports.
- `llms.txt`, `robots.txt`, `sitemap.xml`: for search engines and AI assistants.

## Before going live

- **Domain.** `SITE` in `build.py` is set to `https://www.caminosdelagua.co` as a placeholder. Change it, along with the URLs in `robots.txt` and `sitemap.xml`, then rebuild.
- **Font.** The design uses Aktiv Grotesk (Adobe Fonts). Hanken Grotesk stands in for now. Add the Adobe Fonts kit to `<head>` and Aktiv Grotesk takes over automatically.
- **Form.** "Formulario", "¡Únete a nuestro proyecto!" and the three "¿Qué te trae por aquí?" buttons open the form, but it doesn't send anything yet.
- **Placeholders.** Team and ally tiles have no photos yet. The allies are still "John Doe" as in the template.

## Viewing it

Open `index.html` through a local server so the CSS and scripts load, for example `python3 -m http.server` in this folder.
