(function(){
  const tabsEl  = document.getElementById('tabs');
  const panesEl = document.getElementById('panes');
  const appRoot = document.getElementById('appRoot');

  const keyFrom = url => new URL(url, location.origin).pathname;
  const withEmbed = url => {
    const u = new URL(url, location.origin);
    if(!u.searchParams.has('embed')) u.searchParams.set('embed','1');
    return u.pathname + u.search; // mantém same-origin
  };

  function activate(key){
    document.querySelectorAll('.tab').forEach(t=>t.classList.toggle('active', t.dataset.key===key));
    document.querySelectorAll('.pane').forEach(p=>p.style.display = (p.dataset.key===key ? 'block' : 'none'));
  }

  function openTab(url, title, icon){
    const key = keyFrom(url);
    let tab = tabsEl.querySelector(`.tab[data-key="${key}"]`);
    if(tab){ activate(key); return; }

    tab = document.createElement('div');
    tab.className = 'tab';
    tab.dataset.key = key;
    tab.innerHTML = `<span class="ico">${icon||''}</span><span class="ttl">${title||key}</span><button class="x" title="Fechar">×</button>`;
    tabsEl.appendChild(tab);

    const pane = document.createElement('div');
    pane.className = 'pane';
    pane.dataset.key = key;

    const iframe = document.createElement('iframe');
    iframe.src = withEmbed(url);
    iframe.loading = 'lazy';

    iframe.addEventListener('load', ()=>{
      try{
        const doc = iframe.contentDocument;
        if(!doc) return;

        // Remove a sidebar interna e expande o conteúdo
        doc.querySelectorAll('.sidebar').forEach(el=>el.remove());
        const app = doc.querySelector('.app');
        if(app){ app.style.display = 'block'; app.style.gridTemplateColumns = '1fr'; }
        const content = doc.querySelector('.content');
        if(content){ content.style.minHeight = '100vh'; content.style.padding = '24px 16px'; }
        doc.querySelectorAll('.card').forEach(c=>{ c.style.width='100%'; c.style.maxWidth='none'; });

        // CSS de reforço dentro do iframe
        const style = doc.createElement('style');
        style.textContent = `
          a { text-decoration: none; color: inherit; }
        `;
        doc.head.appendChild(style);
      }catch(err){
        console.warn('tabs.js: ajuste interno falhou:', err);
      }
    });

    pane.appendChild(iframe);
    panesEl.appendChild(pane);

    tab.addEventListener('click', (e)=>{
      if(e.target.classList.contains('x')){
        panesEl.querySelector(`.pane[data-key="${key}"]`)?.remove();
        tab.remove();
        const last = tabsEl.querySelector('.tab:last-child');
        if(last) activate(last.dataset.key);
      }else{
        activate(key);
      }
    });

    activate(key);
  }

  // intercepta o menu do shell
  document.querySelectorAll('.sb-item[data-open]').forEach(a=>{
    a.addEventListener('click', (e)=>{
      e.preventDefault();
      document.querySelectorAll('.sb-item').forEach(x=>x.classList.remove('active'));
      a.classList.add('active');
      openTab(a.dataset.open, a.dataset.title, a.dataset.icon);
    });
  });

  // primeira aba
  const first = document.querySelector('.sb-item[data-open]');
  if(first){ first.click(); } else { openTab('/dashboard.html','Início','🏠'); }

  // recolher/expandir sidebar do shell
  document.getElementById('btnToggle')?.addEventListener('click', ()=>{
    appRoot.classList.toggle('collapsed');
  });
})();
