/* Caminos del Agua on Cargo: the prototype's js/site.js adapted to live inside a Cargo page.
   Built into cargo/web.html by cargo/build-web.py. Differences from site.js:
   - everything is looked up inside .cda-web, and .page is .cda-page (Cargo uses .page for its own pages);
   - links to #ids inside the page scroll there instead of going through Cargo's router;
   - the form sends through Cargo's contact form endpoint (recipient: Publish Settings > Contact Form);
   - the Siete Raíces script is fetched from jsDelivr with its image paths made absolute.
   Cargo saves the live page in the editor, so this script only sets attributes and listeners, never adds
   elements to the page. VERSION guards against running twice after an Update in the editor. */
(() => {
const VERSION = '@VERSION@';
const BASE = '@BASE@';
const web = document.querySelector('.cda-web');
if (!web || web.dataset.ran === VERSION) return;
web.dataset.ran = VERSION;
web.classList.add('js');

const SITE_ID = 3758984;
const ENDPOINT = 'https://cargo.site/dispatch/notifications/sendContactMessage';
const MAIL = 'eliana.caicedo@infinitourbano.com';
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

// In-page links: scroll to the target ourselves, before Cargo's router sees the click
const still = matchMedia('(prefers-reduced-motion: reduce)');
addEventListener('click', e => {
  const a = e.target.closest && e.target.closest('.cda-web a[href^="#"]');
  if (!a) return;
  const el = document.getElementById(a.getAttribute('href').slice(1));
  if (!el || !web.contains(el)) return;
  e.preventDefault();
  e.stopPropagation();
  if (el.matches('dialog')) { if (!el.open) el.showModal(); return; }   // #privacidad
  // stopPropagation keeps the click from the menu's own listener, so close the menu here
  if (menu.contains(a) && !menu.hidden) setMenu(false);
  el.scrollIntoView({ behavior: still.matches ? 'auto' : 'smooth', block: 'start' });
  if (el.matches('main')) { el.setAttribute('tabindex', '-1'); el.focus({ preventScroll: true }); }
}, true);

const burger = web.querySelector('.burger');
const menu = web.querySelector('#menu');
const closeBtn = menu.querySelector('.menu-close');
/* Cargo sets `contain: layout` on its page wrappers, so a position: fixed menu would cover the whole page
   instead of the window. The menu opens as a popover (popover="manual", added by build-web.py), which puts it
   in the browser's top layer, above the containment, without moving it in the page. */
function setMenu(open) {
  menu.hidden = !open;
  if (menu.showPopover) { try { open ? menu.showPopover() : menu.hidePopover(); } catch (err) {} }
  burger.setAttribute('aria-expanded', open);
  document.documentElement.style.overflow = open ? 'hidden' : '';
  (open ? menu.querySelector('a') : burger).focus({ preventScroll: true });
}
burger.addEventListener('click', () => setMenu(menu.hidden));
closeBtn.addEventListener('click', () => setMenu(false));
menu.addEventListener('click', e => { if (e.target.closest('a')) setMenu(false); });
addEventListener('keydown', e => { if (e.key === 'Escape' && !menu.hidden) setMenu(false); });

// Every button with data-interes opens the form, with that interest already chosen
const dlg = web.querySelector('#formulario');
const form = dlg.querySelector('form');
const ok = form.querySelector('.form-ok');
const enviar = form.querySelector('button[value="enviar"]');
function say(text, error) {
  ok.textContent = text;
  ok.hidden = !text;
  ok.classList.toggle('error', !!error);
}
web.querySelectorAll('[data-interes]').forEach(btn => btn.addEventListener('click', () => {
  say('');
  form.interes.value = btn.dataset.interes;
  dlg.showModal();
}));
form.addEventListener('submit', async e => {
  if (e.submitter && e.submitter.value === 'cerrar') return;
  e.preventDefault();
  const f = form.elements;
  const nombre = f.nombre.value.trim();
  const correo = f.correo.value.trim();
  if (!nombre) { say('Escribe tu nombre.', true); f.nombre.focus(); return; }
  if (!EMAIL_RE.test(correo)) { say('Escribe un correo válido.', true); f.correo.focus(); return; }
  if (!f.autorizo.checked) { say('Para enviar, autoriza el tratamiento de tus datos.', true); f.autorizo.focus(); return; }
  const message = [
    'Mensaje desde el formulario de Caminos del Agua',
    '',
    'Nombre: ' + nombre,
    'Correo: ' + correo,
    'Teléfono: ' + (f.telefono.value.trim() || '—'),
    '¿Qué te trae por aquí?: ' + (f.interes.value || '—'),
    '',
    'Mensaje:',
    f.mensaje.value.trim() || '—',
    '',
    'Autorizó el tratamiento de sus datos según la Política de privacidad (Ley 1581 de 2012): sí'
  ].join('\n');
  enviar.disabled = true;
  enviar.textContent = 'Enviando…';
  say('');
  try {
    const res = await fetch(ENDPOINT, { method: 'POST', headers: { 'Content-Type': 'application/json; charset=UTF-8' },
      body: JSON.stringify({ from: correo, site_id: SITE_ID, message }) });
    if (!res.ok) throw new Error(res.status);
    form.reset();
    say('Gracias, recibimos tu mensaje. Te contactaremos pronto.');
  } catch (err) {
    say('No pudimos enviar el mensaje. Inténtalo de nuevo o escríbenos a ' + MAIL + '.', true);
  } finally {
    enviar.disabled = false;
    enviar.textContent = 'Enviar';
  }
});
dlg.addEventListener('click', e => { if (e.target === dlg) dlg.close(); });
// Política de privacidad (opened by the in-page link listener above)
const priv = web.querySelector('#privacidad');
priv.addEventListener('click', e => { if (e.target === priv) priv.close(); });

// Siete Raíces: the prototype's script, with its relative image paths pointed at jsDelivr
fetch(BASE + 'js/siete-raices.js').then(r => r.text()).then(code => {
  const s = document.createElement('script');
  s.textContent = code.replaceAll('"img/', '"' + BASE + 'img/');
  document.head.appendChild(s);
});

/* The river, as in site.js: --rl is the length drawn so far, from the (length, scroll target) pairs in
   #river-map. On phones the pieces that follow the phone frames (.mr) each draw from their place on screen (--p). */
const page = web.querySelector('.cda-page');
const total = parseFloat(page.style.getPropertyValue('--rt'));
const narrow = matchMedia('(max-width: 899px)');
const AT = .62;
const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
const pairs = JSON.parse(web.querySelector('#river-map').textContent);
const L = pairs.filter((_, i) => i % 2 === 0), Y = pairs.filter((_, i) => i % 2 === 1);
function lengthAt(t) {
  if (t <= Y[0]) return 0;
  if (t >= Y[Y.length - 1]) return total;
  let lo = 0, hi = Y.length - 1;
  while (hi - lo > 1) { const m = (lo + hi) >> 1; (Y[m] <= t ? lo = m : hi = m); }
  return L[lo] + (L[hi] - L[lo]) * (t - Y[lo]) / ((Y[hi] - Y[lo]) || 1);
}
function setVars(vars) { for (const k in vars) page.style.setProperty(k, vars[k]); }
const pieces = page.querySelectorAll('.mr');
function mobileRiver(y, all) {
  pieces.forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.height) el.style.setProperty('--p', all ? 1 : clamp((y - r.top) / r.height).toFixed(3));
  });
}
// Sideways scrollers on phones (render, water): the bar under each shows how far along you are
web.querySelectorAll('.hs').forEach(hs => {
  const bar = hs.parentElement.querySelector('.hs-bar');
  if (!bar) return;
  const set = () => {
    const max = hs.scrollWidth - hs.clientWidth;
    bar.style.setProperty('--hw', hs.scrollWidth ? (hs.clientWidth / hs.scrollWidth).toFixed(3) : 1);
    bar.style.setProperty('--hp', max > 0 ? (hs.scrollLeft / max).toFixed(3) : 0);
  };
  hs.addEventListener('scroll', set, { passive: true });
  addEventListener('resize', set);
  set();
});
let ticking = false;
function update() {
  ticking = false;
  const rest = document.documentElement.scrollHeight - innerHeight - scrollY;
  const at = AT + (1 - AT) * clamp(1 - rest / innerHeight);
  if (narrow.matches) return mobileRiver(innerHeight * at, still.matches || rest < 2);
  if (still.matches) return setVars({ '--rl': total });
  const u = page.clientWidth / 1920;
  const rl = rest < 2 ? total : lengthAt((innerHeight * at - page.getBoundingClientRect().top) / u);
  setVars({ '--rl': rl.toFixed(1) });
}
const queue = () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } };
addEventListener('scroll', queue, { passive: true });
addEventListener('resize', queue);
narrow.addEventListener('change', queue);
still.addEventListener('change', queue);
new ResizeObserver(queue).observe(page);
update();

})();
