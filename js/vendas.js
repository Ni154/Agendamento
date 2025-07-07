// Supabase Client Config
const SUPABASE_URL = "https://stqbqsrznhhtbvjeugyb.supabase.co";
const SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN0cWJxc3J6bmhodGJ2amV1Z3liIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE5MDQ3OTcsImV4cCI6MjA2NzQ4MDc5N30.m5iS5AsWKWJIIHcXJSJg7Tc66SUUN31zJob_-AzPwCw";

const supabase = supabase.createClient(SUPABASE_URL, SUPABASE_KEY);

document.addEventListener("DOMContentLoaded", () => {
  const vendaTipoRadios = document.querySelectorAll('input[name="vendaTipo"]');
  const agendamentoSection = document.getElementById("agendamentoSection");
  const novaVendaSection = document.getElementById("novaVendaSection");

  const selectAgendamento = document.getElementById("selectAgendamento");
  const detalhesAgendamento = document.getElementById("detalhesAgendamento");
  const finalizarVendaBtn = document.getElementById("finalizarVendaBtn");

  const posVendaRadios = document.querySelectorAll('input[name="posVenda"]');
  const reagendarInputs = document.getElementById("reagendarInputs");
  const btnConfirmarReagendamento = document.getElementById("btnConfirmarReagendamento");
  const btnConfirmarCancelamento = document.getElementById("btnConfirmarCancelamento");

  const selectCliente = document.getElementById("selectCliente");
  const selectProdutos = document.getElementById("selectProdutos");
  const selectServicos = document.getElementById("selectServicos");
  const produtosQuantidade = document.getElementById("produtosQuantidade");
  const servicosQuantidade = document.getElementById("servicosQuantidade");
  const totalVenda = document.getElementById("totalVenda");
  const finalizarNovaVendaBtn = document.getElementById("finalizarNovaVendaBtn");
  const novaVendaBtn = document.getElementById("novaVendaBtn");

  let agendamentosData = [];
  let servicosData = [];
  let produtosData = [];
  let clientesData = [];

  function formatarData(dataISO) {
    const d = new Date(dataISO);
    return d.toLocaleDateString("pt-BR") + " " + d.toLocaleTimeString("pt-BR", {hour: '2-digit', minute:'2-digit'});
  }

  // Atualiza exibição total
  function atualizarTotal(itens) {
    let total = 0;
    itens.forEach(item => {
      total += item.quantidade * item.preco;
    });
    totalVenda.textContent = total.toFixed(2).replace('.', ',');
  }

  // Alterna seções
  vendaTipoRadios.forEach(radio => {
    radio.addEventListener("change", () => {
      if (radio.value === "agendamento") {
        agendamentoSection.style.display = "block";
        novaVendaSection.style.display = "none";
        carregarAgendamentos();
      } else {
        agendamentoSection.style.display = "none";
        novaVendaSection.style.display = "block";
        carregarClientes();
        carregarProdutos();
        carregarServicos();
        totalVenda.textContent = "0,00";
      }
    });
  });

  // Carregar agendamentos pendentes
  async function carregarAgendamentos() {
    selectAgendamento.innerHTML = "";
    detalhesAgendamento.innerHTML = "";
    try {
      let { data, error } = await supabase
        .from("agendamentos")
        .select(`
          id, cliente_id, data, hora, servicos, status,
          clientes!inner(nome)
        `)
        .eq("status", "Pendente")
        .order("data", { ascending: true });

      if (error) throw error;
      agendamentosData = data;

      if (data.length === 0) {
        selectAgendamento.innerHTML = "<option>Nenhum agendamento pendente</option>";
        finalizarVendaBtn.disabled = true;
        return;
      }
      finalizarVendaBtn.disabled = false;
      data.forEach(ag => {
        const option = document.createElement("option");
        option.value = ag.id;
        option.textContent = `ID ${ag.id} - ${ag.clientes.nome} - ${ag.data} ${ag.hora} - Serviços: ${ag.servicos}`;
        selectAgendamento.appendChild(option);
      });

      mostrarDetalhesAgendamento(data[0].id);
    } catch (err) {
      console.error("Erro ao carregar agendamentos:", err.message);
    }
  }

  selectAgendamento.addEventListener("change", (e) => {
    mostrarDetalhesAgendamento(parseInt(e.target.value));
  });

  // Mostrar detalhes do agendamento selecionado
  function mostrarDetalhesAgendamento(id) {
    const ag = agendamentosData.find(a => a.id === id);
    if (!ag) {
      detalhesAgendamento.innerHTML = "";
      return;
    }

    detalhesAgendamento.innerHTML = `
      <p><strong>Cliente:</strong> ${ag.clientes.nome}</p>
      <p><strong>Data/Hora:</strong> ${ag.data} ${ag.hora}</p>
      <p><strong>Serviços:</strong> ${ag.servicos}</p>
      <p><strong>Status:</strong> ${ag.status}</p>
    `;

    // Preparar seleção quantidade para cada serviço
    const servicosList = ag.servicos.split(",").map(s => s.trim()).filter(Boolean);
    let quantHtml = "<h3>Quantidade por serviço</h3>";
    servicosList.forEach(serv => {
      quantHtml += `
        <label>${serv}:
          <input type="number" min="1" value="1" data-servico="${serv}" />
        </label><br/>
      `;
    });
    detalhesAgendamento.innerHTML += quantHtml;
  }

  finalizarVendaBtn.addEventListener("click", async () => {
    const agendamentoId = parseInt(selectAgendamento.value);
    if (!agendamentoId) return alert("Selecione um agendamento.");

    // Obter quantidades
    const inputsQtd = detalhesAgendamento.querySelectorAll('input[type="number"]');
    let itensVenda = [];
    inputsQtd.forEach(input => {
      const servico = input.dataset.servico;
      const quantidade = parseInt(input.value);
      if (quantidade > 0) {
        itensVenda.push({ servico, quantidade });
      }
    });

    // Buscar preços dos serviços
    const servicosMap = new Map();
    servicosData.forEach(s => servicosMap.set(s.nome, s.valor));

    let total = 0;
    itensVenda.forEach(item => {
      const preco = servicosMap.get(item.servico) || 0;
      total += preco * item.quantidade;
    });

    try {
      // Obter cliente_id do agendamento
      const agendamento = agendamentosData.find(a => a.id === agendamentoId);
      const cliente_id = agendamento.cliente_id;
      const data_venda = new Date().toISOString();

      // Inserir venda
      const { data: venda, error: errVenda } = await supabase
        .from("vendas")
        .insert([{ cliente_id, data: data_venda, total }])
        .select()
        .single();
      if (errVenda) throw errVenda;

      // Inserir itens da venda
      for (const item of itensVenda) {
        const serv = item.servico;
        const qtd = item.quantidade;
        // Buscar id e valor do serviço
        const servData = servicosData.find(s => s.nome === serv);
        if (!servData) continue;

        const { error: errItem } = await supabase
          .from("venda_itens")
          .insert([{
            venda_id: venda.id,
            tipo: "servico",
            item_id: servData.id,
            quantidade: qtd,
            preco: servData.valor,
          }]);
        if (errItem) throw errItem;
      }

      // Atualizar status do agendamento para 'Finalizada'
      const { error: errAtualiza } = await supabase
        .from("agendamentos")
        .update({ status: "Finalizada" })
        .eq("id", agendamentoId);
      if (errAtualiza) throw errAtualiza;

      alert("Venda finalizada e agendamento marcado como Finalizado!");
      carregarAgendamentos();
    } catch (err) {
      alert("Erro ao finalizar venda: " + err.message);
    }
  });

  // Controlar opções pós-venda (reagendar, cancelar)
  posVendaRadios.forEach(radio => {
    radio.addEventListener("change", () => {
      if (radio.value === "reagendar") {
        reagendarInputs.style.display = "block";
        btnConfirmarCancelamento.style.display = "none";
      } else if (radio.value === "cancelar") {
        reagendarInputs.style.display = "none";
        btnConfirmarCancelamento.style.display = "inline-block";
      } else {
        reagendarInputs.style.display = "none";
        btnConfirmarCancelamento.style.display = "none";
      }
    });
  });

  btnConfirmarReagendamento.addEventListener("click", async () => {
    const agendamentoId = parseInt(selectAgendamento.value);
    const novaData = document.getElementById("novaData").value;
    const novaHora = document.getElementById("novaHora").value;
    if (!novaData || !novaHora) return alert("Informe nova data e hora.");

    try {
      const { error } = await supabase
        .from("agendamentos")
        .update({ data: novaData, hora: novaHora, status: "Reagendada" })
        .eq("id", agendamentoId);
      if (error) throw error;

      alert("Agendamento reagendado com sucesso!");
      carregarAgendamentos();
    } catch (err) {
      alert("Erro ao reagendar: " + err.message);
    }
  });

  btnConfirmarCancelamento.addEventListener("click", async () => {
    const agendamentoId = parseInt(selectAgendamento.value);
    if (!confirm("Confirma cancelamento do agendamento?")) return;

    try {
      const { error } = await supabase
        .from("agendamentos")
        .update({ status: "Cancelada" })
        .eq("id", agendamentoId);
      if (error) throw error;

      alert("Agendamento cancelado com sucesso!");
      carregarAgendamentos();
    } catch (err) {
      alert("Erro ao cancelar: " + err.message);
    }
  });

  // Carregar clientes para nova venda
  async function carregarClientes() {
    selectCliente.innerHTML = "";
    try {
      let { data, error } = await supabase.from("clientes").select("id, nome");
      if (error) throw error;
      clientesData = data;
      data.forEach(c => {
        const opt = document.createElement("option");
        opt.value = c.id;
        opt.textContent = c.nome;
        selectCliente.appendChild(opt);
      });
    } catch (err) {
      console.error("Erro ao carregar clientes:", err.message);
    }
  }

  // Carregar produtos para nova venda
  async function carregarProdutos() {
    selectProdutos.innerHTML = "";
    produtosQuantidade.innerHTML = "";
    try {
      let { data, error } = await supabase.from("produtos").select("id, nome, quantidade, preco_venda");
      if (error) throw error;
      produtosData = data;
      data.forEach(p => {
        const opt = document.createElement("option");
        opt.value = p.id;
        opt.textContent = `${p.nome} (Estoque: ${p.quantidade})`;
        selectProdutos.appendChild(opt);
      });
    }

