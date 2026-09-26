const menuToggle = document.querySelector('.menu-toggle');
const siteMenu = document.querySelector('#site-menu');

if (menuToggle && siteMenu) {
  menuToggle.addEventListener('click', () => {
    const open = menuToggle.getAttribute('aria-expanded') === 'true';
    menuToggle.setAttribute('aria-expanded', String(!open));
    siteMenu.classList.toggle('is-open', !open);
    menuToggle.textContent = open ? 'Menu' : 'Close';
  });

  siteMenu.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      menuToggle.setAttribute('aria-expanded', 'false');
      siteMenu.classList.remove('is-open');
      menuToggle.textContent = 'Menu';
    });
  });
}
