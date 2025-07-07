// Config Supabase
const SUPABASE_URL = "https://stqbqsrznhhtbvjeugyb.supabase.co";
const SUPABASE_KEY = "sb_publishable_XmW5t1y3YcJWzCYlvRtLDA_LcJSs4gH;

const supabase = supabase.createClient(SUPABASE_URL, SUPABASE_KEY);

let chart = null;

// Função principal de filtro
async function filtrarRelatorio() {
  const inicio = document.getElementById("dataInicio").value;
  const fim = document.getElementById("dataFim").value;

  if (!inicio || !fim) {
    alert("Selecione um período válido.");
    return;
  }

  try {
    const { data: vendas, error } = await supabase
      .from("vendas")
      .select("id, data, total")
      .gte("data", inicio)
      .lte("data", fim);

    if (error) throw error;

    atualizarGrafico(vendas);
    preencherResumo(vendas);
  } catch (err) {
    alert("Erro ao buscar relatórios: " + err.message);
  }
}

// Gráfico de barras
function atualizarGrafico(vendas) {
  const dias = {};
  vendas.forEach(v => {
    const dia = new Date(v.data).toLocaleDateString("pt-BR");
    dias[dia] = (dias[dia] || 0) + v.total;
  });

  const labels = Object.keys(dias);
  const valores = Object.values(dias);

  const ctx = document.getElementById("graficoVendas").getContext("2d");
  if (chart) chart.destroy();

  chart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [{
        label: "Total de Vendas (R$)",
        data: valores,
        backgroundColor: "#0d6efd",
        borderRadius: 8
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: ctx => `R$ ${ctx.raw.toFixed(2)}` } }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            callback: value => `R$ ${value}`
          }
        }
      }
    }
  });
}

// Preencher tabela resumo
function preencherResumo(vendas) {
  const tbody = document.getElementById("tabelaResumo");
  tbody.innerHTML = "";

  vendas.forEach(venda => {
    const tr = document.createElement("tr");
    const dataVenda = new Date(venda.data).toLocaleDateString("pt-BR");

    tr.innerHTML = `
      <td>${dataVenda}</td>
      <td>R$ ${venda.total.toFixed(2).replace(".", ",")}</td>
      <td>-</td>
      <td>-</td>
    `;
    tbody.appendChild(tr);
  });
}

// Autocarregamento inicial com últimos 7 dias
window.addEventListener("DOMContentLoaded", () => {
  const hoje = new Date();
  const seteDiasAtras = new Date();
  seteDiasAtras.setDate(hoje.getDate() - 7);

  document.getElementById("dataFim").value = hoje.toISOString().split("T")[0];
  document.getElementById("dataInicio").value = seteDiasAtras.toISOString().split("T")[0];

  filtrarRelatorio();
});

