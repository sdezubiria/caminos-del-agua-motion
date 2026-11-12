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

/* The river: one ink line from the g of the logo to the footer (built by build.py, styled in css/site.css).
   --rl is the length drawn so far. Its tip follows a point 62% down the window. Where the line runs sideways
   or up, the tip still moves on at least A page px per px of line, so horizontal runs draw over some scroll
   instead of all at once. On phones a thin line down the left edge draws instead (--mp, 0 to 1). */
const page = document.querySelector('.page');
const main = document.getElementById('contenido');
const ref = document.querySelector('.river-ref path');
const total = parseFloat(page.style.getPropertyValue('--rt'));
const narrow = matchMedia('(max-width: 899px)');
const still = matchMedia('(prefers-reduced-motion: reduce)');
const A = .35, STEP = 6, AT = .62;
const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
let map = null;

function measure() {
  // Sample the line once: L = length, Y = the scroll target (page px) at which the tip reaches it
  const k = ref.getTotalLength() / total;
  const L = [], Y = [];
  for (let l = 0; ; l = Math.min(l + STEP, total)) {
    const y = ref.getPointAtLength(l * k).y;
    Y.push(L.length ? Math.max(Y[Y.length - 1] + A * (l - L[L.length - 1]), y) : y);
    L.push(l);
    if (l >= total) break;
  }
  map = { L, Y, k };
}
function lengthAt(t) {
  const { L, Y } = map;
  if (t <= Y[0]) return 0;
  if (t >= Y[Y.length - 1]) return total;
  let lo = 0, hi = Y.length - 1;
  while (hi - lo > 1) { const m = (lo + hi) >> 1; (Y[m] <= t ? lo = m : hi = m); }
  return L[lo] + (L[hi] - L[lo]) * (t - Y[lo]) / ((Y[hi] - Y[lo]) || 1);
}
function setVars(vars) { for (const k in vars) page.style.setProperty(k, vars[k]); }

let ticking = false;
function update() {
  ticking = false;
  const rest = document.documentElement.scrollHeight - innerHeight - scrollY;
  // Near the bottom the target slides down to the window's lower edge, so the river reaches the end
  const at = AT + (1 - AT) * clamp(1 - rest / innerHeight);
  if (narrow.matches) {
    const r = main.getBoundingClientRect();
    setVars({ '--mp': still.matches || rest < 2 ? 1 : clamp((innerHeight * at - r.top) / r.height).toFixed(4) });
    return;
  }
  if (still.matches) return setVars({ '--rl': total, '--tv': 0 });
  if (!map) measure();
  const u = page.clientWidth / 1920;
  const rl = rest < 2 ? total : lengthAt((innerHeight * at - page.getBoundingClientRect().top) / u);
  const p = ref.getPointAtLength(rl * map.k);
  setVars({ '--rl': rl.toFixed(1), '--tx': p.x.toFixed(1), '--ty': p.y.toFixed(1), '--tv': rl > 0 && rl < total ? 1 : 0 });
}
const queue = () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } };
addEventListener('scroll', queue, { passive: true });
addEventListener('resize', queue);
narrow.addEventListener('change', queue);
still.addEventListener('change', queue);
update();
})();
