const navToggle = document.querySelector('.nav-toggle');
const navLinks = document.querySelector('.nav-links');
const year = document.getElementById('year');
const specialMessage = document.getElementById('special-message');

if (navToggle && navLinks) {
  navToggle.addEventListener('click', () => {
    navLinks.classList.toggle('open');
  });

  navLinks.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      navLinks.classList.remove('open');
    });
  });
}

if (year) {
  year.textContent = new Date().getFullYear();
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
