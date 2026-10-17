document.addEventListener('DOMContentLoaded', () => {
  // Sidebar entra desde la izquierda
  gsap.from("#header", { x: -260, opacity: 0, duration: 0.8, ease: "power3.out" });
  
  // Contenido principal aparece
  gsap.from("#container", { opacity: 0, duration: 1, delay: 0.2, ease: "power2.out" });

  // Tarjetas (módulos) entran escalonadas
  gsap.from(".module", {
    y: 40, opacity: 0, duration: 0.6, stagger: 0.1, ease: "back.out(1.7)", delay: 0.3
  });

  // Filas de tablas
  gsap.from("#result_list tbody tr", {
    x: -20, opacity: 0, duration: 0.4, stagger: 0.05, ease: "power1.out", delay: 0.4
  });
});
