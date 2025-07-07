// js/clientes.js

async function cadastrarCliente(event) {
  event.preventDefault();
  const form = event.target;
  const cliente = {
    nome: form.nome.value,
    telefone: form.telefone.value,
    nascimento: form.nascimento.value,
    hora_agendada: form.hora_agendada.value,
    instagram: form.instagram.value,
    cantor: form.cantor.value,
    bebida: form.bebida.value
  };

  const { error } = await supabase.from('clientes').insert([cliente]);

  if (error) {
    alert("Erro ao salvar cliente: " + error.message);
  } else {
    alert("Cliente cadastrado com sucesso!");
    form.reset();
    carregarClientes();
  }
}

async function carregarClientes() {
  const { data, error } = await supabase.from('clientes').select('*').order('id', { ascending: false });
  const container = document.getElementById('lista-clientes');
  container.innerHTML = '';

  if (error) {
    container.innerHTML = '<p>Erro ao carregar clientes.</p>';
    return;
  }

  data.forEach(cliente => {
    const div = document.createElement('div');
    div.className = 'card';
    div.innerHTML = `
      <strong>🧍 ${cliente.nome}</strong><br>
      📞 ${cliente.telefone}<br>
      🎂 ${cliente.nascimento} às ${cliente.hora_agendada}<br>
      📸 IG: ${cliente.instagram}
    `;
    container.appendChild(div);
  });
}

// Carregar lista ao abrir a página
document.addEventListener('DOMContentLoaded', carregarClientes);

