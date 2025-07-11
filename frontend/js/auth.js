// Import Supabase client
import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js/+esm'

// Sua URL pública do projeto Supabase — substitua pelo seu endpoint real
const SUPABASE_URL = 'https://xyzcompany.supabase.co'  // <== troque pela sua URL real!
const SUPABASE_KEY = 'sb_publishable_XmW5t1y3YcJWzCYlvRtLDA_LcJSs4gH'

const supabase = createClient(SUPABASE_URL, SUPABASE_KEY)

// Seleciona o formulário e a mensagem de erro
const form = document.getElementById('login-form')
const errorMessage = document.getElementById('error-message')

form.addEventListener('submit', async (e) => {
  e.preventDefault()
  errorMessage.textContent = '' // limpa mensagem anterior

  const email = form.email.value.trim()
  const password = form.password.value.trim()

  if (!email || !password) {
    errorMessage.textContent = 'Por favor, preencha todos os campos.'
    return
  }

  // Chamada para autenticação
  const { error, data } = await supabase.auth.signInWithPassword({ email, password })

  if (error) {
    errorMessage.textContent = 'Erro no login: ' + error.message
    return
  }

  // Login bem sucedido
  // Você pode redirecionar para dashboard ou armazenar sessão local
  window.location.href = 'dashboard.html'
})
