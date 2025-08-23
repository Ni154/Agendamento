const API_A = API_BASE + '/api/appointments';
const API_C = API_BASE + '/api/clients';
const API_SV= API_BASE + '/api/services';

function $(s){return document.querySelector(s)}
async function rq(u,o={}){const r=await fetch(u,{headers:{'Content-Type':'application/json'},...o});const d=await r.json().catch(()=>null);return{r,d};}

async function fillSelects(){
  const sc = $('#ag_cliente'), ss = $('#ag_servico');
  const c = await rq(API_C); const s = await rq(API_SV);
  sc.innerHTML = `<option value="">Selecione...</option>` + ((c.d?.items)||[]).map(x=>`<option value="${x.id}">${x.nome||x.name}</option>`).join('');
  ss.innerHTML = `<option value="">Selecione...</option>` + ((s.d?.items)||[]).map(x=>`<option value="${x.id}">${x.name}</option>`).join('');
}

async function saveAppt(e){
  e?.preventDefault();
  const payload = {
    client_id: parseInt($('#ag_cliente')?.value),
    service_id: parseInt($('#ag_servico')?.value),
    date: $('#ag_data')?.value,
    time: $('#ag_hora')?.value,
    status: 'PENDENTE',
    notes: $('#ag_obs')?.value.trim()
  };
  const {r,d}=await rq(API_A,{method:'POST',body:JSON.stringify(payload)});
  if(!r.ok) return alert((d&&d.error)||'Erro ao agendar');
  e.target?.reset(); loadAppts();
}

async function loadAppts(){
  const box = $('#agLista'); if(!box) return;
  const d = $('#ag_data')?.value;
  const {d:resp} = await rq(`${API_A}${d?`?date=${d}`:''}`);
  const items = (resp && resp.items) || [];
  if(!items.length){ box.innerHTML='<div class="muted">Nenhum agendamento.</div>'; return; }
  box.innerHTML = items.map(a=>`
    <div class="row">
      <div><strong>${a.time}</strong> — Cliente #${a.client_id} • Serviço #${a.service_id}<br/><small>${a.date}</small></div>
      <div class="actions">
        <select onchange="updStatus(${a.id}, this.value)">
          ${['PENDENTE','EM_ANDAMENTO','FINALIZADO'].map(s=>`<option ${s==a.status?'selected':''}>${s}</option>`).join('')}
        </select>
      </div>
    </div>
  `).join('');
}
async function updStatus(id, status){
  const {r,d}=await rq(`${API_A}/${id}/status`,{method:'PUT',body:JSON.stringify({status})});
  if(!r.ok) return alert((d&&d.error)||'Falha ao atualizar status');
}

document.getElementById('formAg')?.addEventListener('submit', saveAppt);
document.addEventListener('DOMContentLoaded', ()=>{ fillSelects(); loadAppts(); });
document.getElementById('ag_data')?.addEventListener('change', loadAppts);
