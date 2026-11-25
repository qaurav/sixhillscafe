// ---------------------------------------------------------------------------
// Special opening hours / closures notice.
// To show a banner on every page: set enabled to true, write the message and
// (optionally) an "until" date so it hides itself afterwards (YYYY-MM-DD).
// ---------------------------------------------------------------------------
const SITE_NOTICE = {
  enabled: false,
  message: 'Christmas opening hours: please call us on 01773 772554 to check.',
  until: '' // e.g. '2026-12-31'
};

(function showNotice() {
  if (!SITE_NOTICE.enabled || !SITE_NOTICE.message) return;
  if (SITE_NOTICE.until && new Date() > new Date(SITE_NOTICE.until + 'T23:59:59')) return;
  try {
    if (sessionStorage.getItem('sixhills-notice') === SITE_NOTICE.message) return;
  } catch (error) { /* storage unavailable */ }
  const bar = document.createElement('div');
  bar.className = 'site-notice';
  bar.setAttribute('role', 'status');
  const text = document.createElement('span');
  text.textContent = SITE_NOTICE.message;
  const close = document.createElement('button');
  close.type = 'button';
  close.setAttribute('aria-label', 'Dismiss notice');
  close.textContent = '\u00d7';
  close.addEventListener('click', () => {
    bar.remove();
    try { sessionStorage.setItem('sixhills-notice', SITE_NOTICE.message); } catch (error) { /* ignore */ }
  });
  bar.append(text, close);
  const skip = document.querySelector('.skip-link');
  if (skip) skip.after(bar); else document.body.prepend(bar);
})();

const navToggle = document.querySelector('.nav-toggle');
const navLinks = document.querySelector('.nav-links');
const year = document.getElementById('year');
const specialMessage = document.getElementById('special-message');

if (navToggle && navLinks) {
  const setMenu = (open) => {
    navLinks.classList.toggle('open', open);
    navToggle.setAttribute('aria-expanded', String(open));
  };

  navToggle.addEventListener('click', () => {
    setMenu(!navLinks.classList.contains('open'));
  });

  navLinks.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => setMenu(false));
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && navLinks.classList.contains('open')) {
      setMenu(false);
      navToggle.focus();
    }
  });

  document.addEventListener('click', (event) => {
    if (
      navLinks.classList.contains('open') &&
      !navLinks.contains(event.target) &&
      !navToggle.contains(event.target)
    ) {
      setMenu(false);
    }
  });
}

if (year) {
  year.textContent = new Date().getFullYear();
}

// Google Maps only loads after the visitor chooses to (see privacy.html#maps)
const mapBox = document.getElementById('map-consent');
const loadMapButton = document.getElementById('load-map');

if (mapBox && loadMapButton) {
  const loadMap = () => {
    const frame = document.createElement('iframe');
    frame.src = mapBox.dataset.src;
    frame.title = 'Map to Six Hills Cafe';
    frame.className = 'map-frame';
    frame.loading = 'lazy';
    frame.referrerPolicy = 'no-referrer-when-downgrade';
    mapBox.replaceWith(frame);
    try {
      localStorage.setItem('sixhills-map-consent', '1');
    } catch (error) {
      /* storage unavailable: the choice just won't be remembered */
    }
  };

  loadMapButton.addEventListener('click', loadMap);

  try {
    if (localStorage.getItem('sixhills-map-consent') === '1') {
      loadMap();
    }
  } catch (error) {
    /* ignore */
  }
}

if (specialMessage) {
  const specials = [
    'Cinnamon oat latte with a house-made cookie.',
    'Honey lavender tea with warm brioche.',
    'Iced maple cold brew and a buttery croissant.'
  ];

  let index = 0;
  setInterval(() => {
    index = (index + 1) % specials.length;
    specialMessage.textContent = specials[index];
  }, 4000);
}
