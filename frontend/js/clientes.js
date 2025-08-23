/* API_BASE guard */
var API_BASE = (typeof API_BASE !== 'undefined' && API_BASE) ? API_BASE : `${location.protocol}//${location.host}`;
const API = API_BASE + '/api/clients'; // seu endpoint existente de clientes

function $(s){return document.querySelector(s)}

async function api(url, opt={}){
  const res = await fetch(url, {headers:{'Content-Type':'application/json'}, ...opt});
  const data = await res.json().catch(()=>null);
  return {res,data};
}

async function loadClients(){
  const box = $('#clientesLista'); if(!box) return;
  box.innerHTML = 'Carregando...';
  const {data} = await api(API);
  const items = (data && data.items) || [];
  if(!items.length){ box.innerHTML = '<div class="muted">Nenhum cliente.</div>'; return; }
  box.innerHTML = items.map(c=>`
    <div class="row">
      <div><strong>${c.nome || c.name}</strong><br/><span class="muted">${c.email||''} ${c.telefone||''}</span></div>
      <div class="actions">
        <button class="btn" onclick="editClient(${c.id})">Editar</button>
        <button class="btn" onclick="delClient(${c.id})">Excluir</button>
      </div>
    </div>
  `).join('');
}

async function saveClient(e){
  e?.preventDefault();
  const payload = {
    nome: $('#nome')?.value.trim(),
    apelido: $('#apelido')?.value.trim(),
    telefone: $('#telefone')?.value.trim(),
    whatsapp: $('#whatsapp')?.value.trim(),
    email: $('#email')?.value.trim(),
    cpf: $('#cpf')?.value.trim(),
    nascimento: $('#nascimento')?.value || null,
    endereco: $('#endereco')?.value.trim(),
  };
  const {res,data} = await api(API, {method:'POST', body:JSON.stringify(payload)});
  if(!res.ok) return alert((data && data.error)||'Erro ao salvar');
  e.target?.reset();
  loadClients();
}

async function editClient(id){
  const nome = prompt('Novo nome:'); if(!nome) return;
  const {res,data} = await api(`${API}/${id}`, {method:'PUT', body:JSON.stringify({nome})});
  if(!res.ok) return alert((data && data.error)||'Falha ao editar');
  loadClients();
}
async function delClient(id){
  if(!confirm('Excluir cliente?')) return;
  const {res} = await api(`${API}/${id}`, {method:'DELETE'});
  if(!res.ok) return alert('Falha ao excluir');
  loadClients();
}

document.getElementById('formCliente')?.addEventListener('submit', saveClient);
document.addEventListener('DOMContentLoaded', loadClients);
