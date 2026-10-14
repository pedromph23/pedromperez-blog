/* =====================================================
 * navigation.js — menú móvil
 * - Abre/cierra drawer
 * - Overlay click cierra
 * - Escape cierra
 * - Bloquea scroll del body
 * - ARIA correcto
 * - Foco al primer link al abrir, al botón al cerrar
 * ===================================================== */

(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', () => {
    const toggle  = document.getElementById('mobile-menu-toggle');
    const close   = document.getElementById('mobile-menu-close');
    const drawer  = document.getElementById('mobile-drawer');
    const overlay = document.getElementById('mobile-overlay');

    if (!toggle || !drawer || !overlay) return;

    let open = false;

    function openMenu() {
      open = true;
      drawer.classList.remove('-translate-x-full');
      overlay.classList.remove('opacity-0', 'pointer-events-none');
      overlay.classList.add('opacity-100');
      toggle.setAttribute('aria-expanded', 'true');
      document.body.style.overflow = 'hidden';
      // Foco al primer enlace
      const firstLink = drawer.querySelector('a');
      if (firstLink) firstLink.focus({ preventScroll: true });
    }

    function closeMenu() {
      open = false;
      drawer.classList.add('-translate-x-full');
      overlay.classList.add('opacity-0', 'pointer-events-none');
      overlay.classList.remove('opacity-100');
      toggle.setAttribute('aria-expanded', 'false');
      document.body.style.overflow = '';
      toggle.focus({ preventScroll: true });
    }

    toggle.addEventListener('click', () => (open ? closeMenu() : openMenu()));
    if (close) close.addEventListener('click', closeMenu);
    overlay.addEventListener('click', closeMenu);

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && open) closeMenu();
    });

    // Cerrar al hacer click en cualquier link del drawer
    drawer.querySelectorAll('a').forEach((a) =>
      a.addEventListener('click', () => closeMenu())
    );

    // Cerrar si pasamos a desktop
    const mq = window.matchMedia('(min-width: 1024px)');
    mq.addEventListener('change', (e) => { if (e.matches && open) closeMenu(); });
  });
})();
