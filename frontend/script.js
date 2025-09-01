const API = (window.API_URL || '').trim() || '/_api';

function subdomain() {
  const h = location.hostname;
  if (h === 'localhost' || h === '127.0.0.1') return null;
  const parts = h.split('.');
  if (parts.length <= 2) return null;
  return parts[0];
}

async function getSettings() {
  try {
    const res = await fetch(`${API}/tenant/settings`, { headers: { 'X-Tenant': subdomain() || '' } });
    const data = await res.json();
    if (data.logo_url) document.getElementById('logo').src = data.logo_url;
    document.documentElement.style.setProperty('--primary', data.theme_primary || '#0ea5e9');
  } catch (e) {}
}
getSettings();

document.getElementById('btnLogin').onclick = async () => {
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
  const res = await fetch(`${API}/tenant/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-Tenant': subdomain() || '' },
    body: JSON.stringify({ email, password })
  });
  if (!res.ok) {
    document.getElementById('loginStatus').innerText = 'Falha no login';
    return;
  }
  const data = await res.json();
  localStorage.setItem('token', data.access_token);
  document.getElementById('login').style.display = 'none';
  document.getElementById('app').style.display = 'block';
  listClientes();
  listDespesas();
};

async function listClientes() {
  const res = await fetch(`${API}/cliente`, { headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') } });
  const data = await res.json();
  const ul = document.getElementById('listaClientes');
  ul.innerHTML = '';
  data.forEach(c => {
    const li = document.createElement('li');
    li.innerText = `${c.nome} - ${c.email || ''}`;
    ul.appendChild(li);
  });
}
document.getElementById('btnAddCliente').onclick = async () => {
  const payload = {
    nome: document.getElementById('clienteNome').value,
    email: document.getElementById('clienteEmail').value,
    telefone: document.getElementById('clienteTel').value
  };
  const res = await fetch(`${API}/cliente`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + localStorage.getItem('token') },
    body: JSON.stringify(payload)
  });
  if (res.ok) listClientes();
};

async function listDespesas() {
  const res = await fetch(`${API}/despesas`, { headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') } });
  const data = await res.json();
  const ul = document.getElementById('listaDespesas');
  ul.innerHTML = '';
  data.forEach(d => {
    const li = document.createElement('li');
    li.innerText = `${d.tipo} - ${d.fornecedor_razao || ''} - R$ ${d.valor_total}`;
    ul.appendChild(li);
  });
}
document.getElementById('btnAddDesp').onclick = async () => {
  const payload = {
    tipo: document.getElementById('despTipo').value,
    fornecedor_razao: document.getElementById('fornecedor').value,
    fornecedor_cnpj: document.getElementById('cnpj').value,
    data_emissao: document.getElementById('emissao').value,
    valor_total: Number(document.getElementById('valor').value || 0),
    centro_custo: document.getElementById('centro').value,
    forma_pagto: document.getElementById('pagto').value,
    numero: document.getElementById('numero').value,
    serie: document.getElementById('serie').value,
    chave_acesso: document.getElementById('chave').value,
    numero_rps: document.getElementById('numero').value,
    municipio: document.getElementById('municipio').value,
    aliquota_iss: Number(document.getElementById('aliq').value || 0),
    discriminacao_servico: document.getElementById('disc').value
  };
  const res = await fetch(`${API}/despesas`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + localStorage.getItem('token') },
    body: JSON.stringify(payload)
  });
  if (res.ok) listDespesas();
};

