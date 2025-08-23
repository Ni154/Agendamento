// ======== CONFIG (mesma origem) ========
const API_BASE = 'http://127.0.0.1:5000';
const USE_CREDENTIALS = true;

console.log('[auth.js] carregado');

// ======== HELPERS ========
function $(sel) { return document.querySelector(sel); }

function setMsg(el, msg, type = 'info') {
  if (!el) return;
  el.textContent = msg;
  el.classList.remove('ok', 'err', 'info');
  el.classList.add(type);
}

async function jsonFetch(url, { method = 'GET', headers = {}, body, credentials } = {}) {
  const opts = {
    method,
    headers: { 'Content-Type': 'application/json', ...headers },
    body
  };
  if (credentials !== undefined) opts.credentials = credentials;
  const res = await fetch(url, opts);
  let data = null;
  try { data = await res.json(); } catch (_) {}
  return { res, data };
}

function getQueryParam(name) {
  const params = new URLSearchParams(window.location.search);
  return params.get(name);
}

// ======== LOGIN ========
function setupLogin() {
  const form = $('#loginForm');
  if (!form) return;
  if (form.dataset.bound === '1') return;
  form.dataset.bound = '1';

  const msg  = $('#loginMsg');
  const btn  = form.querySelector('button[type="submit"]');

  console.log('[auth.js] bind loginForm');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    console.log('[auth.js] submit login');

    const email    = $('#email')?.value.trim().toLowerCase();
    const password = $('#password')?.value;

    if (!email || !password) {
      setMsg(msg, 'Informe e-mail e senha.', 'err');
      return;
    }

    btn && (btn.disabled = true);
    setMsg(msg, 'Conectando...', 'info');

    try {
      const { res, data } = await jsonFetch(`${AUTH_BASE}/login`, {
        method: 'POST',
        body: JSON.stringify({ email, password }),
        credentials: USE_CREDENTIALS ? 'include' : undefined
      });

      if (!res.ok) {
        const err = (data && (data.error || data.message)) || `Erro ${res.status}`;
        setMsg(msg, err, 'err');
      } else {
        setMsg(msg, 'Login realizado com sucesso!', 'ok');
        window.location.href = '/workspace.html';
      }
      console.log('[auth.js] login res:', res.status, data);
    } catch (error) {
      setMsg(msg, `Falha de rede: ${error}`, 'err');
      console.error(error);
    } finally {
      btn && (btn.disabled = false);
    }
  });
}

// ======== REGISTER ========
function setupRegister() {
  const form = $('#registerForm');
  if (!form) return;
  if (form.dataset.bound === '1') return;
  form.dataset.bound = '1';

  const msg  = $('#registerMsg');
  const btn  = form.querySelector('button[type="submit"]');

  console.log('[auth.js] bind registerForm');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    console.log('[auth.js] submit register');

    const name     = $('#name')?.value.trim();
    const email    = $('#email')?.value.trim().toLowerCase();
    const password = $('#password')?.value;

    if (!name || !email || !password) {
      setMsg(msg, 'Preencha nome, e-mail e senha.', 'err');
      return;
    }

    btn && (btn.disabled = true);
    setMsg(msg, 'Criando conta...', 'info');

    try {
      const { res, data } = await jsonFetch(`${AUTH_BASE}/register`, {
        method: 'POST',
        body: JSON.stringify({ name, email, password }),
        credentials: USE_CREDENTIALS ? 'include' : undefined
      });

      if (!res.ok) {
        const err = (data && (data.error || data.message)) || `Erro ${res.status}`;
        setMsg(msg, err, 'err');
      } else {
        setMsg(msg, 'Conta criada com sucesso! Redirecionando para o login...', 'ok');
        setTimeout(() => { window.location.href = '/index.html'; }, 800);
      }
      console.log('[auth.js] register res:', res.status, data);
    } catch (error) {
      setMsg(msg, `Falha de rede: ${error}`, 'err');
      console.error(error);
    } finally {
      btn && (btn.disabled = false);
    }
  });
}

// ======== RECOVER ========
function setupRecover() {
  const form = $('#recoverForm');
  if (!form) return;
  if (form.dataset.bound === '1') return;
  form.dataset.bound = '1';

  const msg  = $('#recoverMsg');
  const btn  = form.querySelector('button[type="submit"]');

  console.log('[auth.js] bind recoverForm');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    console.log('[auth.js] submit recover');

    const email = $('#email')?.value.trim().toLowerCase();
    if (!email) {
      setMsg(msg, 'Informe o e-mail.', 'err');
      return;
    }

    btn && (btn.disabled = true);
    setMsg(msg, 'Enviando link...', 'info');

    try {
      const { res, data } = await jsonFetch(`${AUTH_BASE}/recover`, {
        method: 'POST',
        body: JSON.stringify({ email }),
        credentials: USE_CREDENTIALS ? 'include' : undefined
      });

      if (!res.ok) {
        const err = (data && (data.error || data.message)) || `Erro ${res.status}`;
        setMsg(msg, err, 'err');
      } else {
        if (data && data.link) {
          setMsg(msg, 'Link de redefinição (dev): ' + data.link, 'ok');
        } else {
          setMsg(msg, 'Se o e-mail existir, você receberá um link para redefinir a senha.', 'ok');
        }
      }
      console.log('[auth.js] recover res:', res.status, data);
    } catch (error) {
      setMsg(msg, `Falha de rede: ${error}`, 'err');
      console.error(error);
    } finally {
      btn && (btn.disabled = false);
    }
  });
}

// ======== RESET ========
function setupReset() {
  const form = $('#resetForm');
  if (!form) return;
  if (form.dataset.bound === '1') return;
  form.dataset.bound = '1';

  const msg  = $('#resetMsg');
  const btn  = form.querySelector('button[type="submit"]');

  console.log('[auth.js] bind resetForm');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    console.log('[auth.js] submit reset');

    const password = $('#password')?.value;
    const token = getQueryParam('token');

    if (!token) {
      setMsg(msg, 'Token não encontrado no link. Verifique o e-mail recebido.', 'err');
      return;
    }
    if (!password) {
      setMsg(msg, 'Informe a nova senha.', 'err');
      return;
    }

    btn && (btn.disabled = true);
    setMsg(msg, 'Redefinindo senha...', 'info');

    try {
      const { res, data } = await jsonFetch(`${AUTH_BASE}/reset`, {
        method: 'POST',
        body: JSON.stringify({ token, password }),
        credentials: USE_CREDENTIALS ? 'include' : undefined
      });

      if (!res.ok) {
        const err = (data && (data.error || data.message)) || `Erro ${res.status}`;
        setMsg(msg, err, 'err');
      } else {
        setMsg(msg, 'Senha redefinida com sucesso! Vá para o login.', 'ok');
        setTimeout(() => { window.location.href = '/index.html'; }, 1000);
      }
      console.log('[auth.js] reset res:', res.status, data);
    } catch (error) {
      setMsg(msg, `Falha de rede: ${error}`, 'err');
      console.error(error);
    } finally {
      btn && (btn.disabled = false);
    }
  });
}

// ======== INIT ========
document.addEventListener('DOMContentLoaded', () => {
  console.log('[auth.js] DOMContentLoaded');
  setupLogin();
  setupRegister();
  setupRecover();
  setupReset();
});

// Expor para debug opcional no console (pode remover depois)
window.setupLogin = setupLogin;
window.setupRegister = setupRegister;
window.setupRecover = setupRecover;
window.setupReset = setupReset;
