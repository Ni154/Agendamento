/* API_BASE guard */
var API_BASE = (typeof API_BASE !== 'undefined' && API_BASE) ? API_BASE : `${location.protocol}//${location.host}`;
const API_D = API_BASE + '/api/despesas';
const API_P = API_BASE + '/api/produtos';

function $(s){return document.querySelector(s)}
function el(html){const d=document.createElement('div'); d.innerHTML=html.trim(); return d.firstChild;}
async function rq(u,o={}){const r=await fetch(u,{headers:{'Content-Type':'application/json'},...o});const d=await r.json().catch(()=>null);return{r,d};}

async function fillProdutos(select){
  const {d}=await rq(API_P); const items=(d&&d.items)||[];
  select.innerHTML = `<option value="">(Sem produto)</option>` + items.map(p=>`<option value="${p.id}">${p.nome}</option>`).join('');
}

function addItemRow(){
  const wrap = $('#desp_itens');
  const row = el(`
    <div class="row" style="gap:8px;align-items:center">
      <select class="sel-prod" style="min-width:220px"></select>
      <input type="text"  class="txt-desc" placeholder="Descrição (se não tiver produto)"/>
      <input type="number" class="num-qtd" min="0" step="0.01" placeholder="Qtde"/>
      <input type="number" class="num-custo"  min="0" step="0.01" placeholder="Custo unit."/>
      <button type="button" class="btn btn-del">−</button>
    </div>
  `);
  row.querySelector('.btn-del').onclick = ()=> row.remove();
  wrap.appendChild(row);
  fillProdutos(row.querySelector('.sel-prod'));
}

async function saveDespesa(e){
  e?.preventDefault();
  const categoria = ($('#desp_categoria')?.value||'').toLowerCase(); // "revenda"|"uso"
  const itens = Array.from(document.querySelectorAll('#desp_itens .row')).map(r=>{
    return {
      produto_id: parseInt(r.querySelector('.sel-prod')?.value||0) || null,
      descricao: r.querySelector('.txt-desc')?.value.trim(),
      qtd: parseFloat(r.querySelector('.num-qtd')?.value||0),
      custo_unit: parseFloat(r.querySelector('.num-custo')?.value||0),
    }
  }).filter(i=> (i.produto_id || i.descricao) && i.qtd>0);

  if (!itens.length) return alert('Adicione ao menos um item.');
  if (categoria === 'revenda' && itens.some(i=>!i.produto_id)){
    return alert('Em "Revenda" cada item deve estar vinculado a um produto.');
  }

  const payload = {
    data: $('#desp_data')?.value,
    fornecedor: $('#desp_fornecedor')?.value.trim(),
    categoria, observacoes: $('#desp_obs')?.value.trim(),
    itens
  };
  const {r,d}=await rq(API_D,{method:'POST',body:JSON.stringify(payload)});
  if(!r.ok) return alert((d&&d.error)||'Erro ao lançar despesa');
  e.target?.reset(); $('#desp_itens').innerHTML=''; addItemRow();
  loadDespesas();
}

async function loadDespesas(){
  const box = $('#despLista'); if(!box) return;
  const {d}=await rq(API_D); const items=(d&&d.items)||[];
  if(!items.length){ box.innerHTML='<div class="muted">Nenhuma despesa.</div>'; return; }
  box.innerHTML = items.map(e=>`
    <div class="row">
      <div><strong>${e.data}</strong> — ${e.categoria.toUpperCase()} • Forn.: ${e.fornecedor||'—'} • Total: R$ ${e.total.toFixed(2)}</div>
    </div>
  `).join('');
}

document.getElementById('btnAddItem')?.addEventListener('click', addItemRow);
document.getElementById('formDesp')?.addEventListener('submit', saveDespesa);
document.addEventListener('DOMContentLoaded', ()=>{ addItemRow(); loadDespesas(); });
