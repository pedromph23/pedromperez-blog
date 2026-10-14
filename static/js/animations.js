/* =====================================================
 * GSAP animations — pedromperez-blog
 * Requiere: gsap.min.js + ScrollTrigger.min.js
 * ===================================================== */

document.addEventListener("DOMContentLoaded", () => {
  if (typeof gsap === "undefined") {
    console.warn("[GSAP] No se cargó la librería. Verifica el CDN.");
    return;
  }

  gsap.registerPlugin(ScrollTrigger);

  // ---------- 1. Hero (home, blog, proyectos, sobre-mi, contacto) -----
  const heroTl = gsap.timeline({ defaults: { ease: "power3.out" } });

  if (document.querySelector(".hero-kicker")) {
    heroTl.from(".hero-kicker", { y: 20, opacity: 0, duration: 0.6 });
  }
  if (document.querySelector(".hero-title")) {
    heroTl.from(".hero-title", { y: 40, opacity: 0, duration: 0.9 }, "-=0.3");
  }
  if (document.querySelector(".hero-subtitle")) {
    heroTl.from(".hero-subtitle", { y: 30, opacity: 0, duration: 0.7 }, "-=0.5");
  }
  if (document.querySelector(".hero-actions")) {
    heroTl.from(".hero-actions > *", { y: 20, opacity: 0, duration: 0.5, stagger: 0.12 }, "-=0.4");
  }

  // ---------- 2. Tarjetas (posts, proyectos, formularios) -------------
  const cards = gsap.utils.toArray(".animate-card");
  cards.forEach((card, i) => {
    gsap.from(card, {
      scrollTrigger: {
        trigger: card,
        start: "top 88%",
        toggleActions: "play none none none",
      },
      y: 30,
      opacity: 0,
      duration: 0.7,
      delay: (i % 3) * 0.08,
      ease: "power2.out",
    });
  });

  // ---------- 3. Títulos de sección -----------------------------------
  gsap.utils.toArray(".section-title").forEach((title) => {
    gsap.from(title, {
      scrollTrigger: { trigger: title, start: "top 90%" },
      x: -20,
      opacity: 0,
      duration: 0.6,
      ease: "power2.out",
    });
  });

  // ---------- 4. Logo del sidebar -------------------------------------
  const logo = document.querySelector("aside a[href='/']");
  if (logo) {
    gsap.from(logo, { x: -30, opacity: 0, duration: 0.6, delay: 0.1, ease: "power2.out" });
  }

  
  // ---------- 6. Avatar con anillo animado ----------
  const avatarSet = [
    { ring: ".avatar-ring",       circle: ".avatar-ring-circle",       img: ".avatar-img" },
    { ring: ".avatar-ring-hero",  circle: ".avatar-ring-hero-circle",  img: ".avatar-img-hero" },
    { ring: ".avatar-ring-about", circle: ".avatar-ring-about-circle", img: ".avatar-img-about" },
  ];

  avatarSet.forEach(({ ring, circle, img }) => {
    const ringEl = document.querySelector(ring);
    const circleEl = document.querySelector(circle);
    const imgEl = document.querySelector(img);
    if (!ringEl || !circleEl || !imgEl) return;

    const tl = gsap.timeline({ defaults: { ease: "power2.out" } });
    tl.from(imgEl, { scale: 0.7, opacity: 0, duration: 0.8 })
      .to(circleEl, { strokeDashoffset: 0, duration: 1.6, ease: "power2.inOut" }, "-=0.4");

    gsap.to(ringEl, {
      scale: 1.06, duration: 2.4, repeat: -1, yoyo: true,
      ease: "sine.inOut", transformOrigin: "50% 50%", delay: 1.8,
    });
  });

  console.log("[GSAP] Avatar anillo configurado.");

  console.log("[GSAP] Animaciones cargadas correctamente.");
});
