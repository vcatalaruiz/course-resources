// ===== VC MENU JS =====
(function(){
  const $ = (sel, root=document) => root.querySelector(sel);
  const $$ = (sel, root=document) => Array.from(root.querySelectorAll(sel));

  const rail     = $('#vc-rail');
  const list     = $('#vc-list');
  const toggle   = $('#vc-toggle');    // botón siempre visible
  const closeBtn = $('#vc-close');     // X dentro del rail (para móvil)
  const backdrop = $('#vc-backdrop');

  if (!rail || !list || !toggle) return;

  const isDesktop = () => matchMedia('(min-width: 1024px)').matches;

  // --- Slug utilitario ---
  const slug = t => (t||'')
    .toString()
    .normalize('NFD').replace(/[\u0300-\u036f]/g,'')
    .toLowerCase()
    .replace(/[^a-z0-9\s\-_.]/g,'')
    .trim()
    .replace(/\s+/g,'-');

  // --- 1) Construir índice H2/H3 ---
  const sections = $$('main > section');
  const data = [];

  sections.forEach((sec, i) => {
    const h2 = $('h2', sec);
    if(!h2) return;

    if(!sec.id){
      const base = (h2.textContent || '').replace(/^\d+(\.\s*)?/, '');
      let id = slug(base) || `seccion-${i+1}`;
      for(let k=2; document.getElementById(id); k++) id = `${slug(base)}-${k}`;
      sec.id = id;
    }

    const children = $$('h3', sec).map((h3, j) => {
      if(!h3.id){
        const base3 = (h3.textContent || '').replace(/^\d+(\.\d+)*\.\s*/, '');
        let id3 = slug(base3) || `sub-${i+1}-${j+1}`;
        for(let k=2; document.getElementById(id3); k++) id3 = `${slug(base3)}-${k}`;
        h3.id = id3;
      }
      return { id: h3.id, title: (h3.textContent||'').trim() };
    });

    data.push({ id: sec.id, title: (h2.textContent||'').trim(), children });
  });

  // Rellenar lista (sin innerHTML para evitar sanitizados)
  list.replaceChildren();
  data.forEach(item => {
    const li = document.createElement('li');

    const row = document.createElement('div');
    row.className = 'vc-row';

    let disc = null;
    if (item.children.length){
      disc = document.createElement('button');
      disc.type = 'button';
      disc.className = 'vc-disc';
      disc.setAttribute('aria-controls', `sub-${item.id}`);
      disc.setAttribute('aria-expanded', String(isDesktop()));
      row.appendChild(disc);
    } else {
      const spacer = document.createElement('span');
      spacer.style.width = '28px'; spacer.style.height = '28px';
      row.appendChild(spacer);
    }

    const a1 = document.createElement('a');
    a1.href = `#${item.id}`;
    a1.dataset.id = item.id;
    a1.className = 'vc-lvl1';
    a1.textContent = item.title;
    row.appendChild(a1);

    li.appendChild(row);

    if (item.children.length){
      const sub = document.createElement('ul');
      sub.className = 'vc-sub';
      sub.id = `sub-${item.id}`;
      sub.hidden = !isDesktop();

      item.children.forEach(child => {
        const li2 = document.createElement('li');
        const a2 = document.createElement('a');
        a2.href = `#${child.id}`;
        a2.dataset.id = child.id;
        a2.className = 'vc-lvl2';
        a2.textContent = child.title;
        li2.appendChild(a2);
        sub.appendChild(li2);
      });

      disc.addEventListener('click', () => {
        sub.hidden = !sub.hidden;
        disc.setAttribute('aria-expanded', String(!sub.hidden));
      });

      li.appendChild(sub);
    }

    list.appendChild(li);
  });

  // --- 2) Drawer móvil ---
  const openDrawer = () => {
    rail.classList.add('is-open');
    rail.setAttribute('aria-hidden', 'false');
    document.body.classList.add('vc-lock');
    if (backdrop){
      backdrop.hidden = false;
      requestAnimationFrame(() => backdrop.classList.add('show'));
    }
    const first = rail.querySelector('a'); first && first.focus();
  };
  const closeDrawer = () => {
    rail.classList.remove('is-open');
    rail.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('vc-lock');
    if (backdrop){
      backdrop.classList.remove('show');
      setTimeout(() => backdrop.hidden = true, 200);
    }
  };

  // Botón X (móvil)
  closeBtn?.addEventListener('click', () => {
    if (!isDesktop()) closeDrawer();
  });
  // Backdrop clic
  backdrop?.addEventListener('click', () => {
    if (!isDesktop()) closeDrawer();
  });
  // ESC cierra drawer en móvil
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && !isDesktop() && rail.classList.contains('is-open')){
      e.preventDefault(); closeDrawer();
    }
  });

  // --- 3) Botón SIEMPRE visible: móvil ⇄ drawer, escritorio ⇄ colapsado ---
  const COLLAPSE_KEY = 'vc-rail-collapsed';

  // Estado inicial (recuerda preferencia en escritorio)
  if (isDesktop() && localStorage.getItem(COLLAPSE_KEY) === '1'){
    document.body.classList.add('vc-collapsed');
  }

  toggle.addEventListener('click', () => {
    if (isDesktop()){
      const collapsed = document.body.classList.toggle('vc-collapsed');
      if (collapsed) {
        localStorage.setItem(COLLAPSE_KEY, '1');
        rail.setAttribute('aria-hidden', 'true');
      } else {
        localStorage.removeItem(COLLAPSE_KEY);
        rail.setAttribute('aria-hidden', 'false');
        const first = rail.querySelector('a'); first && first.focus();
      }
    } else {
      rail.classList.contains('is-open') ? closeDrawer() : openDrawer();
    }
  });

  // --- 4) Navegación, activo, foco accesible ---
  const setActive = (id, expandParent=false) => {
    $$('.vc-list a').forEach(a => {
      a.setAttribute('aria-current', a.dataset.id === id ? 'true' : 'false');
    });
    if (expandParent){
      const link = $(`.vc-list a[data-id="${CSS.escape(id)}"]`);
      if (link && link.classList.contains('vc-lvl2')){
        const sub = link.closest('.vc-sub');
        const disc = sub?.previousElementSibling?.querySelector?.('.vc-disc');
        if (sub && sub.hidden){ sub.hidden = false; disc?.setAttribute('aria-expanded','true'); }
      }
    }
  };

  // Scroll-control y hash limpio
  list.addEventListener('click', (e) => {
    const a = e.target.closest('a'); if (!a) return;
    const id = a.dataset.id; if (!id) return;
    const target = document.getElementById(id); if (!target) return;

    e.preventDefault();
    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    setActive(id, true);

    if (history.pushState) history.pushState(null, '', `#${id}`);
    else location.hash = `#${id}`;

    // Foco accesible en el heading destino
    const heading = target.matches('h2,h3') ? target : (target.querySelector('h2,h3') || target);
    if (heading){
      const prev = heading.getAttribute('tabindex');
      if (prev === null) heading.setAttribute('tabindex','-1');
      setTimeout(() => heading.focus({ preventScroll: true }), 300);
      setTimeout(() => { if (prev === null) heading.removeAttribute('tabindex'); }, 600);
    }

    // Cerrar drawer si estamos en móvil
    if (!isDesktop()) setTimeout(closeDrawer, 0);
  });

  // Marcar activo desde el hash inicial o cambios posteriores
  const fromHash = () => {
    const current = decodeURIComponent(location.hash||'').slice(1);
    if (current) setActive(current, true);
  };
  window.addEventListener('hashchange', fromHash);
  fromHash();

  // Resalte dinámico con IntersectionObserver (opcional)
  const heads = [
    ...$$('main > section > h2'),
    ...$$('main > section h3')
  ];
  if ('IntersectionObserver' in window && heads.length){
    const io = new IntersectionObserver((entries) => {
      const visible = entries.filter(e => e.isIntersecting)
                             .sort((a,b) => a.boundingClientRect.top - b.boundingClientRect.top);
      if (visible[0]){
        const id = visible[0].target.id || visible[0].target.closest('section')?.id;
        if (id) setActive(id, true);
      }
    }, { rootMargin: '0px 0px -60% 0px', threshold: [0.2, 0.5] });
    heads.forEach(h => { if (!h.id && h.tagName==='H2'){ const sec=h.closest('section'); if(sec?.id) h.id = sec.id; } if (h.id) io.observe(h); });
  }

  // Coherencia al redimensionar
  window.addEventListener('resize', () => {
    if (isDesktop()){
      // cerrar drawer si venimos de móvil
      closeDrawer();
      // respetar preferencia colapsado
      if (localStorage.getItem(COLLAPSE_KEY) === '1') document.body.classList.add('vc-collapsed');
      else document.body.classList.remove('vc-collapsed');

      // abrir sublistas en escritorio
      $$('.vc-sub').forEach(ul => ul.hidden = false);
      $$('.vc-disc').forEach(btn => btn.setAttribute('aria-expanded','true'));
    } else {
      // estado móvil por defecto
      rail.setAttribute('aria-hidden', 'true');
      $$('.vc-sub').forEach(ul => ul.hidden = true);
      $$('.vc-disc').forEach(btn => btn.setAttribute('aria-expanded','false'));
    }
  });
})();