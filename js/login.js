const SUPABASE_URL = "https://stqbqsrznhhtbvjeugyb.supabase.co";
const SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN0cWJxc3J6bmhodGJ2amV1Z3liIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE5MDQ3OTcsImV4cCI6MjA2NzQ4MDc5N30.m5iS5AsWKWJIIHcXJSJg7Tc66SUUN31zJob_-AzPwCw";

const supabase = supabase.createClient(SUPABASE_URL, SUPABASE_KEY);

const form = document.getElementById("login-form");
const msg = document.getElementById("msg");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const usuario = document.getElementById("usuario").value;
  const senha = document.getElementById("senha").value;

  try {
    const { data, error } = await supabase
      .from("usuarios")
      .select("*")
      .eq("usuario", usuario)
      .eq("senha", senha)
      .single();

    if (error || !data) {
      msg.textContent = "Usuário ou senha inválidos!";
      msg.style.color = "red";
      return;
    }

    // Login OK, redireciona
    localStorage.setItem("usuario_logado", JSON.stringify(data));
    window.location.href = "dashboard.html";
  } catch (err) {
    msg.textContent = "Erro ao tentar login.";
    msg.style.color = "red";
  }
});
