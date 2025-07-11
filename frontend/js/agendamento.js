// Função para salvar agendamento com verificação de horário
async function salvarAgendamento(payload) {
  // Verifica se já tem agendamento na mesma data e hora
  const verifica = await fetch(`https://SEU_BACKEND_URL/api/agendamentos/verificar?data=${payload.data}&hora=${payload.hora}`);
  const resultado = await verifica.json();

  if (resultado.ocupado) {
    alert("⚠️ Já existe um agendamento para essa data e hora. Escolha outro horário.");
    return false;
  }

  // Se horário livre, salva o agendamento
  const res = await fetch("https://SEU_BACKEND_URL/api/agendamentos", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    alert("Erro ao salvar agendamento.");
    return false;
  }

  alert("Agendamento salvo com sucesso!");
  return true;
}

// Exemplo de uso no evento submit do formulário
document.getElementById("form-agendamento").addEventListener("submit", async (e) => {
  e.preventDefault();

  const cliente_id = document.getElementById("cliente").value;
  const data = document.getElementById("data").value;
  const hora = document.getElementById("hora").value;
  const servicos = Array.from(document.getElementById("servicos").selectedOptions).map(opt => opt.value);

  const payload = { cliente_id, data, hora, servicos };

  const sucesso = await salvarAgendamento(payload);
  if (sucesso) {
    // Limpar formulário, atualizar UI ou redirecionar
    e.target.reset();
  }
});

