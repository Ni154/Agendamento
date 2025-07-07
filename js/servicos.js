
// js/servicos.js

async function cadastrarServico(event) {
  event.preventDefault();
  const form = event.target;

  const novoServico = {
    nome: form.nome.value,
    unidade: form.unidade.value,
    quantidade: parseInt(form.quantidade.value),
    valor: parseFloat(form.valor.value)
  };

  const { error } = await supabase.from('servicos').insert([novoServico]);

  if (error) {
    alert("Erro ao salvar serviço: " + error.message);
  } else {
    alert("Serviço cadastrado com sucesso!");
    form.reset();
    carregarServicos();
  }
}

async function carregarServicos() {
  const { data, error } = await supabase.from('servicos').select('*').order('id', { ascending: false });
  const container = document.getElementById('lista-servicos');
  container.innerHTML = '';

  if (error) {
    container.innerHTML = '<p>Erro ao carregar serviços.</p>';
    return;
  }

  data.forEach(serv => {
    const div = document.createElement('div');
    div.className = 'card';
    div.innerHTML = `
      <strong>💼 ${serv.nome}</strong><br>
      Unidade: ${serv.unidade}<br>
      Quantidade: ${serv.quantidade}<br>
      Valor: R$ ${serv.valor.toFixed(2)}
    `;
    container.appendChild(div);
  });
}

document.addEventListener('DOMContentLoaded', carregarServicos);
