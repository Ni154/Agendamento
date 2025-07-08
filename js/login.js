<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js"></script>
<script>
  const SUPABASE_URL = "https://stqbqsrznhhtbvjeugyb.supabase.co";
  const SUPABASE_KEY = "sb_publishable_XmW5t1y3YcJWzCYlvRtLDA_LcJSs4gH";

  const supabase = supabase.createClient(SUPABASE_URL, SUPABASE_KEY);

  document.getElementById("login-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const usuario = document.getElementById("usuario").value.trim();
    const senha = document.getElementById("senha").value.trim();
    const msg = document.getElementById("msg");

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

      localStorage.setItem("usuario_logado", JSON.stringify(data));
      window.location.href = "dashboard.html";
    } catch (err) {
      msg.textContent = "Erro ao tentar login.";
      msg.style.color = "red";
    }
  });
</script>
