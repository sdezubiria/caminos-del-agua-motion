# Caminos del Agua · Prototipo web

One-page HTML prototype of the site, built from the Figma file *Caminos del Agua* (frames Final 49 to Final 63). It uses the animated Corriente logo and the Siete Raíces cards from the motion lab.

## Files

- `index.html`: the page. It's generated, so don't edit it by hand.
- `index.src.html`: the page source with the text, sections and SEO tags. Edit this one.
- `build.py`: writes `index.html` and `js/siete-raices.js`. Run `python3 build.py` after any change. It also builds the river (see below).
- `css/site.css`: styles. On desktop each section is its 1920 px Figma frame, scaled to the window. Under 900 px it becomes one column.
- `js/site.js`: section menu, contact form and the river drawing on scroll.
- `js/siete-raices.js`: the Siete Raíces cards, built from `../cargo/siete-raices.src.html` and `../assets/cards-data.js`.
- `img/`: photos as WebP, Figma line art in `img/svg/`, `og-image.jpg` for link previews. `img/raw/` keeps the original PNG exports.
- `img/<name>-800.webp`: lighter versions of the photos for phones. `build.py` adds `srcset` and `sizes` to every photo that has one. If you replace a photo, make its 800 px version again (for example with Pillow: resize to 800 wide, WebP quality 78).
- `llms.txt`, `robots.txt`, `sitemap.xml`: for search engines and AI assistants. `llms.txt` is generated from `llms.src.txt`.
- `HIDE` in `build.py`: sections left out for now. "¿Quién está detrás?" and "Nuestros aliados" are hidden until the client sends their content; remove them from `HIDE` and rebuild to bring them back.

## The river

One line runs from the g of the logo down to the bottom of the page, and draws as you scroll, with round caps. It starts in ink, as the logo, and takes a palette colour in each section (`COLORS` in `build.py`), blending into the next colour across each section boundary.

- `build.py` defines it as orthogonal polylines with rounded corners (radius 80) in page coordinates: on desktop the page is one 1920-wide frame, and each section starts at the sum of the heights above it (`SECTIONS`). Side branches (the pills in "¿Qué te trae por aquí?", the team groups, the form, the allies) leave the line tangentially.
- Each section gets the pieces of line that cross it in an `<svg class="river">` placed above its photos and below its text and pills. `ON_PHOTO` can give the line a light edge over photos; it is empty since the client asked to drop the white edge (Nov 18).
- `js/site.js` sets `--rl` (length drawn) from the scroll position. Under `prefers-reduced-motion` the line is drawn in full.
- Over the walk photo the line makes the two loops of the phone frame 12 (`LOOP_R`), and in "¿Cómo se vive?" strokes leave it along the top of each card (Figma Final 64).

## Phones (under 900 px)

The phone layout follows the Figma frames "iPhone 16 & 17 Pro" 11 to 27 (402 px wide; `--m` is one of their pixels).

- Inicio, the walk photo, "¿Qué te trae por aquí?", "¿Dónde estamos?", the render and the two water photos are fixed 402 × 874 frames scaled to the screen width. The other sections reflow.
- The render and the two water photos scroll sideways, with a bar under them (`.hs`, `.hs-bar`).
- The river is drawn per piece in phone units: `MOBILE` in `build.py` (SVG pieces and straight runs along reflowing text). Each piece draws as it crosses the same point on screen. The arrows over the water photos are `M_ARROWS`.

## Privacy

The form has a required consent box that links to the Política de privacidad (Ley 1581 de 2012), a dialog at the end of `index.src.html` (`#privacidad`), also linked from the footer.
- If you change a section's height or move a pill, change `SECTIONS` or the route in `build.py` too. The build checks that each section's `--h` matches.

## Before going live

- **Domain.** `SITE` in `build.py` is set to `https://www.caminosdelagua.co` as a placeholder. Change it, along with the URLs in `robots.txt` and `sitemap.xml`, then rebuild.
- **Font.** The design uses Aktiv Grotesk (Adobe Fonts). Hanken Grotesk stands in for now. Add the Adobe Fonts kit to `<head>` and Aktiv Grotesk takes over automatically.
- **Form.** "Formulario", "¡Únete a nuestro proyecto!" and the three "¿Qué te trae por aquí?" buttons open the form, but it doesn't send anything yet.
- **Placeholders.** Team and ally tiles have no photos yet. The allies are still "John Doe" as in the template.

## Viewing it

Open `index.html` through a local server so the CSS and scripts load, for example `python3 -m http.server` in this folder.
