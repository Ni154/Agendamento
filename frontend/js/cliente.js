document.addEventListener("DOMContentLoaded", () => {
  const canvas = document.getElementById("assinatura");
  const ctx = canvas.getContext("2d");
  let desenhando = false;
  let ultimaPos = { x: 0, y: 0 };

  // Ajusta canvas para alta resolução (opcional)
  function ajustarCanvas() {
    const ratio = window.devicePixelRatio || 1;
    canvas.width = canvas.offsetWidth * ratio;
    canvas.height = canvas.offsetHeight * ratio;
    ctx.scale(ratio, ratio);
    ctx.lineWidth = 2;
    ctx.lineCap = "round";
    ctx.strokeStyle = "#000";
  }
  ajustarCanvas();

  function iniciarDesenho(e) {
    desenhando = true;
    const rect = canvas.getBoundingClientRect();
    ultimaPos = {
      x: (e.clientX || e.touches[0].clientX) - rect.left,
      y: (e.clientY || e.touches[0].clientY) - rect.top,
    };
  }

  function desenhar(e) {
    if (!desenhando) return;
    const rect = canvas.getBoundingClientRect();
    const x = (e.clientX || e.touches[0].clientX) - rect.left;
    const y = (e.clientY || e.touches[0].clientY) - rect.top;

    ctx.beginPath();
    ctx.moveTo(ultimaPos.x, ultimaPos.y);
    ctx.lineTo(x, y);
    ctx.stroke();
    ultimaPos = { x, y };
  }

  function pararDesenho() {
    desenhando = false;
  }

  canvas.addEventListener("mousedown", iniciarDesenho);
  canvas.addEventListener("touchstart", iniciarDesenho);

  canvas.addEventListener("mousemove", desenhar);
  canvas.addEventListener("touchmove", desenhar);

  canvas.addEventListener("mouseup", pararDesenho);
  canvas.addEventListener("touchend", pararDesenho);
  canvas.addEventListener("touchcancel", pararDesenho);

  // Botão limpar assinatura
  document.getElementById("btnLimpar").addEventListener("click", () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
  });

  // Lógica do envio do formulário
  const form = document.getElementById("formCliente");
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Captura assinatura como imagem base64
    const assinaturaBase64 = canvas.toDataURL();

    // Monta objeto com dados do formulário
    const dados = {
      nome: form.nome.value.trim(),
      email: form.email.value.trim(),
      telefone: form.telefone.value.trim(),
      nascimento: form.nascimento.value,
      cpf: form.cpf.value.trim(),
      problema_saude: form.problema_saude.value,
      descricao_saude: form.descricao_saude.value.trim(),
      medicamento: form.medicamento.value,
      descricao_medicamento: form.descricao_medicamento.value.trim(),
      assinatura: assinaturaBase64,
    };

    // Validação simples de assinatura (canvas não vazio)
    if (assinaturaBase64.length < 1000) {
      alert("Por favor, faça a assinatura no campo indicado.");
      return;
    }

    try {
      // Enviar via API (substituir URL pelo backend real)
      const response = await fetch("/api/clientes", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(dados),
      });

      if (!response.ok) {
        throw new Error("Erro ao salvar cliente");
      }

      alert("Cliente cadastrado com sucesso!");
      form.reset();
      ctx.clearRect(0, 0, canvas.width, canvas.height);

    } catch (error) {
      alert("Erro no cadastro: " + error.message);
    }
  });

  // Mostrar/ocultar campos descrição conforme resposta SIM/NAO
  function toggleDescricao(idSelect, idTextarea) {
    const select = document.getElementById(idSelect);
    const textarea = document.getElementById(idTextarea);
    const label = document.querySelector(`label[for=${idTextarea}]`);

    function atualizar() {
      if (select.value === "sim") {
        textarea.classList.remove("hidden");
        label.classList.remove("hidden");
        textarea.required = true;
      } else {
        textarea.classList.add("hidden");
        label.classList.add("hidden");
        textarea.required = false;
        textarea.value = "";
      }
    }

    select.addEventListener("change", atualizar);
    atualizar();
  }

  toggleDescricao("problema_saude", "descricao_saude");
  toggleDescricao("medicamento", "descricao_medicamento");
});
