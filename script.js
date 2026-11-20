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
