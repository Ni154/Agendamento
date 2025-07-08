// login.js

// Substitua com sua URL e chave pública do Supabase
const SUPABASE_URL = "https://stqbqsrznhhtbvjeugyb.supabase.co";
const SUPABASE_KEY = "sb_publishable_XmW5t1y3YcJWzCYlvRtLDA_LcJSs4gH";

// Cria o cliente
const supabase = supabase.createClient(SUPABASE_URL, SUPABASE_KEY);

// Captura o formulário
const form = document.getElementById("login-form");
const msg = document.getElementById("msg");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  // Captura os valores
  const usuario = document.getElementById("usuario").value.trim();
  const senha = document.getElementById("senha").value.trim();

  // Verifica se campos foram preenchidos
  if (!usuario || !senha) {
    msg.textContent = "Preencha todos os campos!";
    msg.style.color = "red";
    return;
  }

  try {
    // Consulta a tabela 'usuarios'
    const { data, error } = await supabase
      .from("usuarios")
      .select("*")
      .eq("usuario", usuario)
      .eq("senha", senha)
      .single();

    if (error || !data) {
      msg.textContent = "Usuário ou senha incorretos!";
      msg.style.color = "red";
      return;
    }

    // Login bem-sucedido
    localStorage.setItem("usuario_logado", JSON.stringify(data));
    window.location.href = "dashboard.html"; // Redireciona
  } catch (err) {
    msg.textContent = "Erro ao conectar. Tente novamente.";
    msg.style.color = "red";
    console.error("Erro de login:", err);
  }
});
