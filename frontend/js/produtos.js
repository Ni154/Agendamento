/* API_BASE guard */
var API_BASE = (typeof API_BASE !== 'undefined' && API_BASE) ? API_BASE : `${location.protocol}//${location.host}`;
const API_P = API_BASE + '/api/products';

function $q(s){return document.querySelector(s)}
async function req(u,o={}){
  const r=await fetch(u,{headers:{'Content-Type':'application/json'},...o});
  const d=await r.json().catch(()=>null); return {r,d};
}

async function loadCategories(){
  const sel = $q('#p_categoria'); if(!sel) return;
  const {d} = await req(API_P+'/categories');
  const items=(d&&d.items)||[];
  sel.innerHTML = `<option value="">—</option>` + items.map(c=>`<option>${c}</option>`).join('');
}
function addCategory(){
  const c = prompt('Nova categoria:'); if(!c) return;
  const sel = $q('#p_categoria');
  const opt = document.createElement('option'); opt.value=c; opt.textContent=c;
  sel.appendChild(opt); sel.value=c;
}

async function saveProduct(e){
  e?.preventDefault();
  const payload = {
    name: $q('#p_nome')?.value.trim(),
    sku: $q('#p_sku')?.value.trim(),
    category: $q('#p_categoria')?.value.trim(),
    unit: $q('#p_unidade')?.value.trim(),
    cost_price: parseFloat($q('#p_custo')?.value||0),
    sale_price: parseFloat($q('#p_preco')?.value||0),
    stock_qty: parseFloat($q('#p_estoque')?.value||0),
  };
  const {r,d}=await req(API_P, {method:'POST', body:JSON.stringify(payload)});
  if(!r.ok) return alert((d&&d.error)||'Erro ao salvar');
  e.target?.reset();
  await loadCategories();
  loadProducts();
}

async function loadProducts(){
  const box = $q('#produtosLista'); if(!box) return;
  const {d}=await req(API_P); const items=(d&&d.items)||[];
  if(!items.length){ box.innerHTML='<div class="muted">Nenhum produto.</div>'; return; }
  box.innerHTML = items.map(p=>`
    <div class="row">
      <div><strong>${p.name}</strong> <span class="muted">[${p.category||'—'}]</span><br/>
      <small>SKU: ${p.sku||'—'} • Estoque: ${p.stock_qty||0} • Custo: ${p.cost_price||0} • Preço: ${p.sale_price||0}</small></div>
      <div class="actions">
        <button class="btn" onclick="editProduct(${p.id})">Editar</button>
        <button class="btn" onclick="delProduct(${p.id})">Excluir</button>
      </div>
    </div>
  `).join('');
}
async function editProduct(id){
  const name = prompt('Novo nome:'); if(!name) return;
  const {r,d}=await req(`${API_P}/${id}`, {method:'PUT', body:JSON.stringify({name})});
  if(!r.ok) return alert((d&&d.error)||'Falha ao editar');
  loadProducts();
}
async function delProduct(id){
  if(!confirm('Excluir produto?')) return;
  const {r}=await req(`${API_P}/${id}`, {method:'DELETE'});
  if(!r.ok) return alert('Falha ao excluir');
  loadProducts();
}

document.getElementById('formProduto')?.addEventListener('submit', saveProduct);
document.getElementById('btnAddCategoria')?.addEventListener('click', addCategory);
document.addEventListener('DOMContentLoaded', ()=>{ loadCategories(); loadProducts(); });
