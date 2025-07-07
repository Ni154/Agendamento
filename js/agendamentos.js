// js/agendamentos.js

let agendamentos = [];
let clientes = [];
let servicos = [];

async function carregarClientes() {
  const { data, error } = await supabase.from('clientes').select('id,nome');
  if (error) {
    alert("Erro ao carregar clientes: " + error.message);
  } else {
    clientes = data;
    const selectCliente = document.getElementById('cliente');
    selectCliente.innerHTML = '';
    data.forEach(c => {
      const option = document.createElement('option');
      option.value = c.id;
      option.textContent = c.nome;
      selectCliente.appendChild(option);
    });
  }
}

async function carregarServicos() {
  const { data, error } = await supabase.from('servicos').select('id,nome');
  if (error) {
    alert("Erro ao carregar serviços: " + error.message);
  } else {
    servicos = data;
    const selectServicos = document.getElementById('servicos');
    selectServicos.innerHTML = '';
    data.forEach(s => {
      const option = document.createElement('option');
      option.value = s.nome;
      option.textContent = s.nome;
      selectServicos.appendChild(option);
    });
  }
}

async function carregarAgendamentos() {
  const { data, error } = await supabase.from('agendamentos').select('id,cliente_id,data,hora,servicos,status').order('data', { ascending: true });
  if (error) {
    alert("Erro ao carregar agendamentos: " + error.message);
  } else {
    agendamentos = data;
    const selectAgendamento = document.getElementById('select-agendamento');
    selectAgendamento.innerHTML = '<option value="">Selecione um agendamento para reagendar</option>';
    data.forEach(a => {
      const clienteNome = clientes.find(c => c.id === a.cliente_id)?.nome || "Cliente Desconhecido";
      const option = document.createElement('option');
      option.value = a.id;
      option.textContent = `ID ${a.id} - ${clienteNome} - ${a.data} ${a.hora} - Serviços: ${a.servicos} - Status: ${a.status}`;
      selectAgendamento.appendChild(option);
    });
  }
}

function mostrarAgendamento() {
  const select = document.getElementById('select-agendamento');
  const agendamentoId = parseInt(select.value);
  const detalhes = document.getElementById('detalhes-agendamento');
  detalhes.innerHTML = '';

  if (!agendamentoId) return;

  const ag = agendamentos.find(a => a.id === agendamentoId);
  if (!ag) return;

  const clienteNome = clientes.find(c => c.id === ag.cliente_id)?.nome || "Cliente Desconhecido";

  detalhes.innerHTML = `
    <p><strong>Cliente:</strong> ${clienteNome}</p>
    <p><strong>Data Atual:</strong> ${ag.data}</p>
    <p><strong>Hora Atual:</strong> ${ag.hora}</p>
    <p><strong>Serviços:</strong> ${ag.servicos}</p>
    <p><strong>Status:</strong> ${ag.status}</p>
    <label for="novaData">Nova Data:</label>
    <input type="date" id="novaData" name="novaData" value="${ag.data}" />
    <label for="novaHora">Nova Hora:</label>
    <input type="time" id="novaHora" name="novaHora" value="${ag.hora}" />
    <button onclick="reagendar(${ag.id})">Confirmar Reagendamento</button>
  `;
}

async function reagendar(id) {
  const novaData = document.getElementById('novaData').value;
  const novaHora = document.getElementById('novaHora').value;

  if (!novaData || !novaHora) {
    alert("Informe nova data e hora");
    return;
  }

  const statusNovo = `Reagendada para ${novaData} ${novaHora}`;

  const { error } = await supabase
    .from('agendamentos')
    .update({ data: novaData, hora: novaHora, status: statusNovo })
    .eq('id', id);

  if (error) {
    alert("Erro ao reagendar: " + error.message);
  } else {
    alert("Agendamento reagendado com sucesso!");
    carregarAgendamentos();
    document.getElementById('detalhes-agendamento').innerHTML = '';
  }
}

async function criarAgendamento(event) {
  event.preventDefault();

  const clienteId = document.getElementById('cliente').value;
  const data = document.getElementById('data').value;
  const hora = document.getElementById('hora').value;
  const servicosSelected = Array.from(document.getElementById('servicos').selectedOptions).map(opt => opt.value);

  if (!clienteId || !data || !hora || servicosSelected.length === 0) {
    alert("Preencha todos os campos.");
    return;
  }

  const servicosStr = servicosSelected.join(", ");

  const { error } = await supabase.from('agendamentos').insert([{
    cliente_id: parseInt(clienteId),
    data: data,
    hora: hora,
    servicos: servicosStr,
    status: "Pendente"
  }]);

  if (error) {
    alert("Erro ao criar agendamento: " + error.message);
  } else {
    alert("Agendamento criado com sucesso!");
    event.target.reset();
    carregarAgendamentos();
  }
}

document.addEventListener('DOMContentLoaded', async () => {
  await carregarClientes();
  await carregarServicos();
  await carregarAgendamentos();
});
