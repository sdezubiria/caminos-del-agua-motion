/* Caminos del Agua · prototipo: section menu and the contact form dialog */
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
})();
