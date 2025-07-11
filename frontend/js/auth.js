// Inicializa o Supabase (substitua as chaves abaixo pelas suas)
const SUPABASE_URL = "https://SEU-PROJETO.supabase.co";
const SUPABASE_ANON_KEY = "sb_publishable_XmW5t1y3YcJWzCYlvRtLDA_LcJSs4gH";

const supabase = supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

const form = document.getElementById("login-form");
const errorMsg = document.getElementById("login-error");

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    errorMsg.textContent = "";

    const email = form.email.value.trim();
    const password = form.password.value;

    if (!email || !password) {
        errorMsg.textContent = "Preencha todos os campos.";
        return;
    }

    const { data, error } = await supabase.auth.signInWithPassword({
        email,
        password,
    });

    if (error) {
        errorMsg.textContent = "Erro no login: " + error.message;
        return;
    }

    // Login sucesso - redirecionar para dashboard
    window.location.href = "dashboard.html";
});

