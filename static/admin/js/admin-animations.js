document.addEventListener('DOMContentLoaded', () => {
  gsap.from("#header", { x: -50, opacity: 0, duration: 0.5, ease: "power2.out" });
  gsap.from("#container > header", { y: -20, opacity: 0, duration: 0.5, delay: 0.1, ease: "power2.out" });
  gsap.from(".module", { y: 20, opacity: 0, duration: 0.4, stagger: 0.1, ease: "power1.out", delay: 0.2 });
  gsap.from("#result_list tbody tr", { x: -10, opacity: 0, duration: 0.3, stagger: 0.02, ease: "power1.out", delay: 0.3 });
});
