// 3.1 – leva o botão de toggle para a topbar (se ele surgiu dentro do sidebar)
(function fixTogglePlacement(){
  const top = document.querySelector('.topbar .topbar-inner');
  const btn = document.getElementById('btnToggle') || document.querySelector('.toggle');
  if (top && btn && !top.contains(btn)) {
    top.prepend(btn);
  }
})();

// 3.2 – quando colapsar/expandir a sidebar, empurra a .main corretamente
(function hookSidebarCollapse(){
  const sidebar = document.querySelector('.sidebar');
  const main = document.querySelector('.main');
  const btn = document.getElementById('btnToggle') || document.querySelector('.toggle');
  if (!sidebar || !main || !btn) return;

  btn.addEventListener('click', () => {
    sidebar.classList.toggle('collapsed');
    // a margem da .main é controlada via CSS pelo seletor adjacente (.sidebar.collapsed + .main)
    // então aqui não precisa fazer nada além de alternar a classe
  });
})();
