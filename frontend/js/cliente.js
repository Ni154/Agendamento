document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("cliente-form");
  const canvas = document.getElementById("assinatura");
  const limpar = document.getElementById("limpar");
  const ctx = canvas.getContext("2d");
  let desenhando = false;

  canvas.addEventListener("mousedown", () => desenhando = true);
  canvas.addEventListener("mouseup", () => desenhando = false);
  canvas.addEventListener("mouseleave", () => desenhando = false);

  canvas.addEventListener("mousemove", (e) => {
    if (!desenhando) return;
    const rect = canvas.getBoundingClientRect();
    ctx.lineWidth = 2;
    ctx.lineCap = "round";
    ctx.strokeStyle = "#000";
    ctx.lineTo(e.clientX - rect.left, e.clientY - rect.top);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(e.clientX - rect.left, e.clientY - rect.top);
  });

  limpar.addEventListener("click", () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
  });

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const dados = Object.fromEntries(new FormData(form));
    dados.assinatura = canvas.toDataURL();

    const resposta = await fetch("https://SEU_BACKEND_URL/api/clientes", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(dados)
    });

    const msg = document.getElementById("msg");
    if (resposta.ok) {
      msg.innerHTML = "✅ Cliente cadastrado com sucesso!";
      form.reset();
      ctx.clearRect(0, 0, canvas.width, canvas.height);
    } else {
      msg.innerHTML = "❌ Erro ao salvar. Verifique os dados.";
    }
  });
});

