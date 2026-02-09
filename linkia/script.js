// Navegación básica con teclado entre "secciones-diapo"
(function () {
    const slides = Array.from(document.querySelectorAll('section.slide'));
    let idx = 0;
    const scrollTo = (i) => {
        idx = Math.max(0, Math.min(i, slides.length - 1));
        slides[idx].scrollIntoView({ behavior: 'smooth', block: 'start' });
        location.hash = `#${slides[idx].id}`;
    }
    document.addEventListener('keydown', (e) => {
        if (['ArrowRight', 'PageDown', 'ArrowDown', ' '].includes(e.key)) { e.preventDefault(); scrollTo(idx + 1); }
        if (['ArrowLeft', 'PageUp', 'ArrowUp'].includes(e.key)) { e.preventDefault(); scrollTo(idx - 1); }
        if (e.key === 'Home') { e.preventDefault(); scrollTo(0); }
        if (e.key === 'End') { e.preventDefault(); scrollTo(slides.length - 1); }
    });
    // Restaurar por hash
    const h = location.hash.replace('#', '');
    if (h) { const pos = slides.findIndex(s => s.id === h); if (pos >= 0) { idx = pos; slides[idx].scrollIntoView(); } }
})();