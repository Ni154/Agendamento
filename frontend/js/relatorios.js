/* relatorios.js */
(() => {
  const API_BASE = window.API_BASE || 'http://127.0.0.1:5000';
  const USE_CREDENTIALS = true;
  const REPORTS = API_BASE + '/api/reports';

  const $ = sel => document.querySelector(sel);
  const creds = USE_CREDENTIALS ? 'include' : 'same-origin';
  const money = v => (Number(v||0)).toLocaleString('pt-BR',{style:'currency',currency:'BRL'});
  async function jsonFetch(url, { method='GET', headers={}, body } = {}){
    const res = await fetch(url, { method, headers:{'Content-Type':'application/json',...headers}, body, credentials:creds });
    let data=null; try{ data=await res.json(); }catch{}
    return { res, data };
  }

  function toCSV(rows){
    if(!rows?.length) return '';
    const cols = Object.keys(rows[0]);
    const esc = s => `"${String(s??'').replace(/"/g,'""')}"`;
    const head = cols.map(esc).join(',');
    const body = rows.map(r => cols.map(k => esc(r[k])).join(',')).join('\n');
    return head + '\n' + body;
  }

  function renderTable(ret){
    const head = $('#rel-head'), body = $('#rel-body'); if(!head||!body) return;
    let rows = [];
    if(Array.isArray(ret)) rows = ret;
    else if(Array.isArray(ret?.rows)) rows = ret.rows;
    else if(Array.isArray(ret?.items)) rows = ret.items;
    else rows = [];

    const cols = rows[0]? Object.keys(rows[0]) : [];
    head.innerHTML = cols.map(c=>`<th>${c}</th>`).join('') || '<th>resultado</th>';
    body.innerHTML = rows.map(r=>`
      <tr>${cols.map(c=>`<td>${/valor|total|preco/i.test(c)? (money(r[c])) : (r[c]??'')}</td>`).join('')}</tr>
    `).join('') || '<tr><td>Sem dados para o filtro.</td></tr>';

    return rows;
  }

  async function runReport(){
    const tipo = $('#rel-tipo')?.value || 'VENDAS';
    const de   = $('#rel-de')?.value || '';
    const ate  = $('#rel-ate')?.value || '';
    const qs = new URLSearchParams();
    qs.set('type', tipo);
    if(de) qs.set('from', de);
    if(ate) qs.set('to', ate);
    const { res, data } = await jsonFetch(`${REPORTS}?${qs}`);
    if(!res.ok){ $('#rel-msg').textContent = data?.error||'Erro ao gerar'; $('#rel-msg').className='note error'; return []; }
    $('#rel-msg').textContent='';
    return renderTable(data);
  }

  document.addEventListener('DOMContentLoaded', ()=>{
    const form = $('#relForm'); if(!form) return;
    const expBtn = $('#rel-export');

    form.addEventListener('submit', async (e)=>{
      e.preventDefault();
      await runReport();
    });

    expBtn?.addEventListener('click', async ()=>{
      const rows = await runReport();
      if(!rows?.length) return alert('Nada para exportar.');
      const csv = toCSV(rows);
      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url; a.download = 'relatorio.csv';
      document.body.appendChild(a); a.click(); a.remove();
      URL.revokeObjectURL(url);
    });
  });
})();
