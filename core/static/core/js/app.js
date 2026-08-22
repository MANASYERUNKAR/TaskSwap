/* Quiet Utility reminder: motion is brief, respectful, and only clarifies a typography-first interface. */
(function () {
    "use strict";
    document.documentElement.classList.add("is-motion-ready");
    const revealItems = document.querySelectorAll(".reveal");
    if ("IntersectionObserver" in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => { if (entry.isIntersecting) { entry.target.classList.add("is-visible"); observer.unobserve(entry.target); } });
        }, { threshold: 0.12 });
        revealItems.forEach((item) => observer.observe(item));
    } else { revealItems.forEach((item) => item.classList.add("is-visible")); }
    const menuToggle = document.querySelector("[data-menu-toggle]");
    const navigation = document.querySelector("[data-primary-nav]");
    if (menuToggle && navigation) { menuToggle.addEventListener("click", () => { const isOpen = navigation.classList.toggle("is-open"); menuToggle.setAttribute("aria-expanded", String(isOpen)); }); }
    const header = document.querySelector("[data-header]");
    const updateHeader = () => { if (header) header.classList.toggle("is-scrolled", window.scrollY > 8); };
    updateHeader(); window.addEventListener("scroll", updateHeader, { passive: true });
}());
