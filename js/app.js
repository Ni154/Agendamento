// js/app.js

const SUPABASE_URL = 'https://stqbqsrznhhtbvjeugyb.supabase.co';
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN0cWJxc3J6bmhodGJ2amV1Z3liIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE5MDQ3OTcsImV4cCI6MjA2NzQ4MDc5N30.m5iS5AsWKWJIIHcXJSJg7Tc66SUUN31zJob_-AzPwCw';

const supabase = supabase.createClient(SUPABASE_URL, SUPABASE_KEY);

// LOGIN
async function loginUsuario() {
  const email = document.getElementById('email').value;
  const senha = document.getElementById('senha').value;

  const { data, error } = await supabase
    .from('usuarios')
    .select('*')
    .eq('email', email)
    .eq('senha', senha)
    .single();

  if (data) {
    localStorage.setItem('usuarioLogado', JSON.stringify(data));
    window.location.href = 'dashboard.html';
  } else {
    document.getElementById('login-erro').innerText = 'Usuário ou senha inválidos.';
  }
}

// LOGOUT
function logout() {
  localStorage.removeItem('usuarioLogado');
  window.location.href = 'index.html';
}

// NAVEGAR
function navegar(pagina) {
  window.location.href = `${pagina}.html`;
}

// AGENDAMENTOS DO DIA
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

  if (data.length === 0) {
    container.innerHTML = '<p>Nenhum agendamento para hoje.</p>';
    return;
  }

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
