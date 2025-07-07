const SUPABASE_URL = 'https://stqbqsrznhhtbvjeugyb.supabase.co';
const SUPABASE_KEY = 'sb_publishable_XmW5t1y3YcJWzCYlvRtLDA_LcJSs4gH';

const supabase = supabase.createClient(SUPABASE_URL, SUPABASE_KEY);

// LOGIN PADRÃO (usuario e senha)
async function loginUsuario() {
  const usuario = document.getElementById('usuario').value.trim();
  const senha = document.getElementById('senha').value.trim();

  if (!usuario || !senha) {
    document.getElementById('login-erro').innerText = 'Informe o usuário e a senha.';
    return;
  }

  const { data, error } = await supabase
    .from('usuarios')
    .select('*')
    .eq('usuario', usuario)
    .eq('senha', senha)
    .single();

  if (error || !data) {
    document.getElementById('login-erro').innerText = 'Usuário ou senha inválidos.';
    return;
  }

  localStorage.setItem('usuarioLogado', JSON.stringify(data));
  window.location.href = 'dashboard.html';
}

// LOGOUT
function logout() {
  localStorage.removeItem('usuarioLogado');
  window.location.href = 'index.html';
}

// NAVEGAÇÃO ENTRE PÁGINAS
function navegar(pagina) {
  window.location.href = `${pagina}.html`;
}

// LISTAR AGENDAMENTOS DO DIA
async function carregarAgendamentosHoje() {
  const container = document.getElementById('lista-agendamentos');
  const hoje = new Date().toISOString().split('T')[0];

  const { data, error } = await supabase
    .from('agendamentos')
    .select('id, cliente:clientes(nome), data, hora, status')
    .eq('data', hoje)
    .order('hora', { ascending: true });

  if (error) {
    container.innerHTML = '<p>Erro ao carregar agendamentos.</p>';
    return;
  }

  if (!data || data.length === 0) {
    container.innerHTML = '<p>Nenhum agendamento para hoje.</p>';
    return;
  }

  container.innerHTML = ''; // Limpa o container antes de preencher

  data.forEach((ag) => {
    const div = document.createElement('div');
    div.className = 'agendamento-card';
    div.innerHTML = `
      <strong>🧍 Cliente:</strong> ${ag.cliente.nome} <br/>
      <strong>📅 Data:</strong> ${ag.data} <br/>
      <strong>🕒 Hora:</strong> ${ag.hora} <br/>
      <strong>Status:</strong> ${ag.status}
    `;
    container.appendChild(div);
  });
}
