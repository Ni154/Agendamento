import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js/+esm'

const SUPABASE_URL = 'https://stqbqsrznhhtbvjeugyb.supabase.co' // sua URL Supabase
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN0cWJxc3J6bmhodGJ2amV1Z3liIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE5MDQ3OTcsImV4cCI6MjA2NzQ4MDc5N30.m5iS5AsWKWJIIHcXJSJg7Tc66SUUN31zJob_-AzPwCw' // sua anon key

const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY)

const loginForm = document.getElementById('login-form')
const msg = document.getElementById('msg')

loginForm.addEventListener('submit', async (e) => {
  e.preventDefault()
  const email = document.getElementById('email').value.trim()

  if (!email) {
    msg.textContent = 'Por favor, insira um e-mail válido.'
    msg.style.color = 'red'
    return
  }

  const { error } = await supabase.auth.signInWithOtp({ email })

  if (error) {
    msg.textContent = `Erro ao enviar link: ${error.message}`
    msg.style.color = 'red'
  } else {
    msg.textContent = 'Link enviado! Verifique seu e-mail para acessar.'
    msg.style.color = '#198754'
  }
})

