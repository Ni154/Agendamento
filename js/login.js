const SUPABASE_URL = "https://stqbqsrznhhtbvjeugyb.supabase.co";
const SUPABASE_KEY = "sb_publishable_XmW5t1y3YcJWzCYlvRtLDA_LcJSs4gH";

const supabase = supabase.createClient(SUPABASE_URL, SUPABASE_KEY);

const form = document.getElementById("login-form");
const msg = document.getElementById("msg");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const usuario = document.getElementById("usuario").value.trim();
  const senha = document.getElementById("senha").value.trim();

  if (!usuario || !senha) {
    msg.textContent = "Informe usuário e senha!";
    msg.style.color = "red";
    return;
  }

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

    // Login OK
    localStorage.setItem("usuario_logado", JSON.stringify(data));
    window.location.href = "dashboard.html";
  } catch (err) {
    msg.textContent = "Erro ao tentar login.";
    msg.style.color = "red";
    console.error(err);
  }
});
