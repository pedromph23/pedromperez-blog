document.addEventListener('DOMContentLoaded', () => {
  gsap.from('.module', {
    duration: 0.6, y: 30, opacity: 0, stagger: 0.1, ease: 'power2.out'
  });
  gsap.from('#result_list tbody tr', {
    duration: 0.4, y: 15, opacity: 0, stagger: 0.05, ease: 'power1.out'
  });
});
