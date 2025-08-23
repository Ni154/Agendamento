const API = window.location.origin;

async function apiGet(path){ const r=await fetch(API+path); return r.json(); }
async function apiPatch(path, body){
  const r=await fetch(API+path,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
  try{ return {status:r.status, data: await r.json()} }catch{ return {status:r.status, data:null} }
}

function fmtHora(iso){
  const d = new Date(iso);
  const hh = String(d.getHours()).padStart(2,'0');
  const mm = String(d.getMinutes()).padStart(2,'0');
  return `${hh}:${mm}`;
}

function badge(status){
  const m = { agendado:'Agendado', cancelado:'Cancelado', finalizado:'Finalizado' };
  return m[status] || status;
}

async function loadMe(){
  try{
    const me = await apiGet('/api/auth/me');
    const nome = me?.user?.name || 'Usuário';
    document.getElementById('bemvindo').textContent = `Olá, ${nome} 👋`;
  }catch{}
}

async function loadAgenda(){
  const vazio = document.getElementById('agendaVazia');
  const tbl = document.getElementById('tblAgenda');
  const body = document.getElementById('agendaBody');
  body.innerHTML=''; vazio.style.display='block'; tbl.style.display='none';
  const data = await apiGet('/api/appointments/today');
  if(!data || !data.length){ vazio.textContent='Sem agendamentos para hoje.'; return; }
  vazio.style.display='none'; tbl.style.display='table';
  for(const a of data){
    const tr = document.createElement('tr');
    const cliente = a.cliente?.nome || '-';
    const serv = a.servico?.nome || '-';
    tr.innerHTML = `
      <td>${fmtHora(a.start_at)}</td>
      <td>${cliente}</td>
      <td>${serv}</td>
      <td>
        ${a.status === 'finalizado'
          ? `<span class="note ok">Finalizado</span>`
          : `<select data-id="${a.id}">
               <option value="agendado"${a.status==='agendado'?' selected':''}>Agendado</option>
               <option value="cancelado"${a.status==='cancelado'?' selected':''}>Cancelado</option>
             </select>`}
      </td>
    `;
    body.appendChild(tr);
  }
  // bind changes
  body.querySelectorAll('select[data-id]').forEach(sel=>{
    sel.addEventListener('change', async ()=>{
      const id = sel.getAttribute('data-id');
      const status = sel.value;
      const {status:code} = await apiPatch(`/api/appointments/${id}/status`, {status});
      if(code!==200){ alert('Erro ao alterar status'); }
    });
  });
}

document.addEventListener('DOMContentLoaded', ()=>{
  loadMe(); loadAgenda();
  document.getElementById('btnRefresh')?.addEventListener('click', loadAgenda);
  setInterval(loadAgenda, 30000);
});
