// ==================== CONFIGURAÇÃO ====================
// Ajuste para a URL pública do seu backend no Railway
const API_BASE_URL = "https://SEU-PROJETO.up.railway.app";

// ==================== FUNÇÕES DE REQUISIÇÃO ====================

// Função genérica para requisições GET
async function apiGet(endpoint) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`);
        if (!response.ok) throw new Error(`Erro: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error("Erro no GET:", error);
        alert("Erro ao buscar dados.");
        return null;
    }
}

// Função genérica para requisições POST
async function apiPost(endpoint, data) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });
        if (!response.ok) throw new Error(`Erro: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error("Erro no POST:", error);
        alert("Erro ao enviar dados.");
        return null;
    }
}

// Função genérica para requisições PUT
async function apiPut(endpoint, data) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });
        if (!response.ok) throw new Error(`Erro: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error("Erro no PUT:", error);
        alert("Erro ao atualizar dados.");
        return null;
    }
}

// Função genérica para requisições DELETE
async function apiDelete(endpoint) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, { method: "DELETE" });
        if (!response.ok) throw new Error(`Erro: ${response.status}`);
        return true;
    } catch (error) {
        console.error("Erro no DELETE:", error);
        alert("Erro ao excluir dados.");
        return false;
    }
}

// ==================== FUNÇÕES ESPECÍFICAS ====================

// Login de usuário
async function loginUsuario(email, senha) {
    return await apiPost("/usuarios/login", { email, senha });
}

// Cadastro de usuário
async function cadastrarUsuario(nome, email, senha) {
    return await apiPost("/usuarios", { nome, email, senha });
}

// Listar clientes
async function listarClientes() {
    return await apiGet("/clientes");
}

// Cadastrar cliente (com ficha de anamnese)
async function cadastrarCliente(dados) {
    return await apiPost("/clientes", dados);
}

// Listar produtos
async function listarProdutos() {
    return await apiGet("/produtos");
}

// Cadastrar produto
async function cadastrarProduto(dados) {
    return await apiPost("/produtos", dados);
}

// Listar serviços
async function listarServicos() {
    return await apiGet("/servicos");
}

// Cadastrar serviço
async function cadastrarServico(dados) {
    return await apiPost("/servicos", dados);
}

// Listar agendamentos
async function listarAgendamentos() {
    return await apiGet("/agendamentos");
}

// Criar agendamento
async function criarAgendamento(dados) {
    return await apiPost("/agendamentos", dados);
}

// Registrar venda
async function registrarVenda(dados) {
    return await apiPost("/vendas", dados);
}

// Lançar despesa
async function lancarDespesa(dados) {
    return await apiPost("/despesas", dados);
}

// Gerar relatório em PDF
async function gerarRelatorio(tipo) {
    return await apiGet(`/relatorios/${tipo}`);
}

// ==================== EXPORTAR FUNÇÕES ====================
export {
    loginUsuario,
    cadastrarUsuario,
    listarClientes,
    cadastrarCliente,
    listarProdutos,
    cadastrarProduto,
    listarServicos,
    cadastrarServico,
    listarAgendamentos,
    criarAgendamento,
    registrarVenda,
    lancarDespesa,
    gerarRelatorio
};
