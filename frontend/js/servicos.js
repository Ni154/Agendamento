/* API_BASE guard */
var API_BASE = (typeof API_BASE !== 'undefined' && API_BASE) ? API_BASE : `${location.protocol}//${location.host}`;
const API_S = API_BASE + '/api/services';

function $(s){return document.querySelector(s)}
async function rq(u,o={}){const r=await fetch(u,{headers:{'Content-Type':'application/json'},...o});const d=await r.json().catch(()=>null);return{r,d};}

async function saveService(e){
  e?.preventDefault();
  const payload = {
    name: $('#s_nome')?.value.trim(),
    description: $('#s_desc')?.value.trim(),
    price: parseFloat($('#s_preco')?.value||0),
    duration_min: parseInt($('#s_duracao')?.value||0),
  };
  const {r,d}=await rq(API_S,{method:'POST',body:JSON.stringify(payload)});
  if(!r.ok) return alert((d&&d.error)||'Erro ao salvar');
  e.target?.reset(); loadServices();
}
async function loadServices(){
  const box=$('#servicosLista'); if(!box) return;
  const {d}=await rq(API_S); const items=(d&&d.items)||[];
  if(!items.length){ box.innerHTML='<div class="muted">Nenhum serviço.</div>'; return; }
  box.innerHTML=items.map(s=>`
    <div class="row">
      <div><strong>${s.name}</strong> — R$ ${s.price||0}<br/><small>${s.description||''}</small></div>
      <div class="actions">
        <button class="btn" onclick="editService(${s.id})">Editar</button>
        <button class="btn" onclick="delService(${s.id})">Excluir</button>
      </div>
    </div>
  `).join('');
}
async function editService(id){
  const name=prompt('Novo nome:'); if(!name) return;
  const {r,d}=await rq(`${API_S}/${id}`,{method:'PUT',body:JSON.stringify({name})});
  if(!r.ok) return alert((d&&d.error)||'Falha ao editar');
  loadServices();
}
async function delService(id){
  if(!confirm('Excluir serviço?')) return;
  const {r}=await rq(`${API_S}/${id}`,{method:'DELETE'});
  if(!r.ok) return alert('Falha ao excluir');
  loadServices();
}
document.getElementById('formServico')?.addEventListener('submit', saveService);
document.addEventListener('DOMContentLoaded', loadServices);
