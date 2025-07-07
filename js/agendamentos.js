// js/agendamentos.js

async function cadastrarAgendamento(event) {
  event.preventDefault();
  const form = event.target;
  const novoAgendamento = {
    nome_cliente: form.nome_cliente.value,
    data: form.data.value,
    hora: form.hora.value,
    servicos: form.servicos.value,
    status: form.status.value
  };

  const { error } = await supabase.from('agendamentos').insert([novoAgendamento]);

  if (error) {
    alert("Erro ao salvar agendamento: " + error.message);
  } else {
    alert("Agendamento registrado com sucesso!");
    form.reset();
    carregarAgendamentos();
  }
}

async function carregarAgendamentos() {
  const { data, error } = await supabase.from('agendamentos').select('*').order('data', { ascending: true });

  const container = document.getElementById('lista-agendamentos');
  container.innerHTML = '';

  if (error) {
    container.innerHTML = '<p>Erro ao carregar agendamentos.</p>';
    return;
  }

  data.forEach(item => {
    const div = document.createElement('div');
    div.className = 'card';
    div.innerHTML = `
      <strong>👤 ${item.nome_cliente}</strong><br>
      📅 ${item.data} às ${item.hora}<br>
      💼 Serviços: ${item.servicos}<br>
      📝 Status: ${item.status}
    `;
    container.appendChild(div);
  });
}

document.addEventListener('DOMContentLoaded', carregarAgendamentos);

