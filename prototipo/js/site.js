/* Caminos del Agua · prototipo: section menu, contact form dialog and the river that draws as you scroll */
(() => {
const burger = document.querySelector('.burger');
const menu = document.getElementById('menu');
const closeBtn = menu.querySelector('.menu-close');

function setMenu(open) {
  menu.hidden = !open;
  burger.setAttribute('aria-expanded', open);
  document.documentElement.style.overflow = open ? 'hidden' : '';
  (open ? menu.querySelector('a') : burger).focus();
}
burger.addEventListener('click', () => setMenu(menu.hidden));
closeBtn.addEventListener('click', () => setMenu(false));
menu.addEventListener('click', e => { if (e.target.closest('a')) setMenu(false); });
addEventListener('keydown', e => { if (e.key === 'Escape' && !menu.hidden) setMenu(false); });

// Every button with data-interes opens the form, with that interest already chosen
const dlg = document.getElementById('formulario');
const form = dlg.querySelector('form');
const ok = form.querySelector('.form-ok');
document.querySelectorAll('[data-interes]').forEach(btn => btn.addEventListener('click', () => {
  ok.hidden = true;
  form.interes.value = btn.dataset.interes;
  dlg.showModal();
}));
form.addEventListener('submit', e => {
  if (e.submitter && e.submitter.value === 'cerrar') return;
  e.preventDefault();   // prototype: nothing is sent yet
  ok.hidden = false;
  form.reset();
});
dlg.addEventListener('click', e => { if (e.target === dlg) dlg.close(); });

// Política de privacidad: a dialog, from the consent box in the form and from the footer
const priv = document.getElementById('privacidad');
document.querySelectorAll('.priv-link').forEach(a => a.addEventListener('click', e => { e.preventDefault(); priv.showModal(); }));
priv.addEventListener('click', e => { if (e.target === priv) priv.close(); });

/* The river: one line from the g of the logo to the bottom of the page (built by build.py, styled in
   css/site.css). --rl is the length drawn so far. Its end follows a point 62% down the window, through a
   table of (length, scroll target) pairs that build.py computes from the line's geometry (#river-map), so
   the browser measures nothing. On phones the line follows the phone frames instead: each piece (.mr, built by
   build.py) draws as it crosses the same point on screen (--p, 0 to 1). */
const page = document.querySelector('.page');
const total = parseFloat(page.style.getPropertyValue('--rt'));
const narrow = matchMedia('(max-width: 899px)');
const still = matchMedia('(prefers-reduced-motion: reduce)');
const AT = .62;
const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
const pairs = JSON.parse(document.getElementById('river-map').textContent);
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
document.querySelectorAll('.hs').forEach(hs => {
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
  // Near the bottom the target slides down to the window's lower edge, so the river reaches the end
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
update();
})();
