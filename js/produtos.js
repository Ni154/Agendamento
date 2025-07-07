// js/produtos.js

async function cadastrarProduto(event) {
  event.preventDefault();
  const form = event.target;

  const novoProduto = {
    nome: form.nome.value,
    quantidade: parseInt(form.quantidade.value),
    preco_custo: parseFloat(form.preco_custo.value),
    preco_venda: parseFloat(form.preco_venda.value)
  };

  const { error } = await supabase.from('produtos').insert([novoProduto]);

  if (error) {
    alert("Erro ao salvar produto: " + error.message);
  } else {
    alert("Produto cadastrado com sucesso!");
    form.reset();
    carregarProdutos();
  }
}

async function carregarProdutos() {
  const { data, error } = await supabase.from('produtos').select('*').order('id', { ascending: false });
  const container = document.getElementById('lista-produtos');
  container.innerHTML = '';

  if (error) {
    container.innerHTML = '<p>Erro ao carregar produtos.</p>';
    return;
  }

  data.forEach(prod => {
    const div = document.createElement('div');
    div.className = 'card';
    div.innerHTML = `
      <strong>📦 ${prod.nome}</strong><br>
      Quantidade: ${prod.quantidade}<br>
      Custo: R$ ${prod.preco_custo.toFixed(2)}<br>
      Venda: R$ ${prod.preco_venda.toFixed(2)}
    `;
    container.appendChild(div);
  });
}

document.addEventListener('DOMContentLoaded', carregarProdutos);

