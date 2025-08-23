// embed.js – controla abas com iframe ocupando toda a área disponível
(() => {
  const $ = s => document.querySelector(s);

  // mede e ajusta altura do iframe ativo conforme viewport
  function fitIframe() {
    const topbar = document.querySelector('.topbar');
    const tabsbar = document.querySelector('.tabsbar');
    const panes = document.querySelector('.panes');
    const iframe = document.querySelector('.pane.active iframe');
    if (!iframe || !panes) return;
    const topH = (topbar?.offsetHeight || 0) + (tabsbar?.offsetHeight || 0);
    const h = Math.max(300, window.innerHeight - topH - 24); // 24px padding
    iframe.style.height = h + 'px';
  }
  window.addEventListener('resize', fitIframe);

  // garante botão de toggle dentro da topbar
  (function fixTogglePlacement(){
    const top = document.querySelector('.topbar .topbar-inner');
    const btn = document.getElementById('btnToggle') || document.querySelector('.toggle');
    if (top && btn && !top.contains(btn)) top.prepend(btn);
  })();

  // alterna colapso do sidebar
  (function hookSidebarCollapse(){
    const sidebar = document.querySelector('.sidebar');
    const btn = document.getElementById('btnToggle') || document.querySelector('.toggle');
    if (!sidebar || !btn) return;
    btn.addEventListener('click', () => {
      sidebar.classList.toggle('collapsed');
      fitIframe();
    });
  })();

  // API simples para abrir abas – use em app.js
  window.openTab = function openTab(id, title, url){
    // cria/encontra aba
    const tabs = document.getElementById('tabsBar');
    const panes = document.querySelector('.panes');
    if (!tabs || !panes) return;

    // ativa apenas a atual
    tabs.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    panes.querySelectorAll('.pane').forEach(p => p.classList.remove('active'));

    let tab = tabs.querySelector(`.tab[data-id="${id}"]`);
    let pane = panes.querySelector(`.pane[data-id="${id}"]`);

    if (!tab) {
      tab = document.createElement('div');
      tab.className = 'tab active';
      tab.dataset.id = id;
      tab.innerHTML = `<span>${title}</span> <button class="x" aria-label="Fechar">×</button>`;
      tabs.appendChild(tab);
      tab.querySelector('.x').addEventListener('click', () => {
        const isActive = tab.classList.contains('active');
        panes.querySelector(`.pane[data-id="${id}"]`)?.remove();
        tab.remove();
        if (isActive) {
          const last = tabs.querySelector('.tab:last-child');
          if (last) last.click();
        }
      });
      tab.addEventListener('click', () => {
        tabs.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        panes.querySelectorAll('.pane').forEach(p => p.classList.remove('active'));
        tab.classList.add('active');
        panes.querySelector(`.pane[data-id="${id}"]`)?.classList.add('active');
        fitIframe();
      });
    } else {
      tab.classList.add('active');
    }

    if (!pane) {
      pane = document.createElement('div');
      pane.className = 'pane active';
      pane.dataset.id = id;
      // iframe 100% (sem atributos width/height fixos)
      const iframe = document.createElement('iframe');
      iframe.setAttribute('loading', 'lazy');
      iframe.style.width = '100%';
      iframe.style.border = '0';
      iframe.src = url;
      pane.appendChild(iframe);
      panes.appendChild(pane);
    } else {
      pane.classList.add('active');
    }

    fitIframe();
  };

  // abre “Início” se nada estiver aberto
  document.addEventListener('DOMContentLoaded', () => {
    if (!document.querySelector('.pane')) {
      // ajuste o caminho da sua página inicial:
      if (window.DASHBOARD_URL) {
        openTab('home', 'Início', window.DASHBOARD_URL);
      }
    }
  });
})();
