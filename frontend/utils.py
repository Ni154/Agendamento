
-// ==================== CONFIGURAÇÃO ====================
-// Ajuste para a URL pública do seu backend no Railway
-const API_BASE_URL = "https://SEU-PROJETO.up.railway.app";
-
-// ==================== FUNÇÕES DE REQUISIÇÃO ====================
-
-// Função genérica para requisições GET
-async function apiGet(endpoint) {
-    try {
-        const response = await fetch(`${API_BASE_URL}${endpoint}`);
-        if (!response.ok) throw new Error(`Erro: ${response.status}`);
-        return await response.json();
-    } catch (error) {
-        console.error("Erro no GET:", error);
-        alert("Erro ao buscar dados.");
-        return null;
-    }
-}
-
-// Função genérica para requisições POST
-async function apiPost(endpoint, data) {
-    try {
-        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
-            method: "POST",
-            headers: { "Content-Type": "application/json" },
-            body: JSON.stringify(data)
-        });
-        if (!response.ok) throw new Error(`Erro: ${response.status}`);
-        return await response.json();
-    } catch (error) {
-        console.error("Erro no POST:", error);
-        alert("Erro ao enviar dados.");
-        return null;
-    }
-}
-
-// Função genérica para requisições PUT
-async function apiPut(endpoint, data) {
-    try {
-        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
-            method: "PUT",
-            headers: { "Content-Type": "application/json" },
-            body: JSON.stringify(data)
-        });
-        if (!response.ok) throw new Error(`Erro: ${response.status}`);
-        return await response.json();
-    } catch (error) {
-        console.error("Erro no PUT:", error);
-        alert("Erro ao atualizar dados.");
-        return null;
-    }
-}
-
-// Função genérica para requisições DELETE
-async function apiDelete(endpoint) {
-    try {
-        const response = await fetch(`${API_BASE_URL}${endpoint}`, { method: "DELETE" });
-        if (!response.ok) throw new Error(`Erro: ${response.status}`);
-        return true;
-    } catch (error) {
-        console.error("Erro no DELETE:", error);
-        alert("Erro ao excluir dados.");
-        return false;
-    }
-}
-
-// ==================== FUNÇÕES ESPECÍFICAS ====================
-
-// Login de usuário
-async function loginUsuario(email, senha) {
-    return await apiPost("/usuarios/login", { email, senha });
-}
-
-// Cadastro de usuário
-async function cadastrarUsuario(nome, email, senha) {
-    return await apiPost("/usuarios", { nome, email, senha });
-}
-
-// Listar clientes
-async function listarClientes() {
-    return await apiGet("/clientes");
-}
-
-// Cadastrar cliente (com ficha de anamnese)
-async function cadastrarCliente(dados) {
-    return await apiPost("/clientes", dados);
-}
-
-// Listar produtos
-async function listarProdutos() {
-    return await apiGet("/produtos");
-}
-
-// Cadastrar produto
-async function cadastrarProduto(dados) {
-    return await apiPost("/produtos", dados);
-}
-
-// Listar serviços
-async function listarServicos() {
-    return await apiGet("/servicos");
-}
-
-// Cadastrar serviço
-async function cadastrarServico(dados) {
-    return await apiPost("/servicos", dados);
-}
-
-// Listar agendamentos
-async function listarAgendamentos() {
-    return await apiGet("/agendamentos");
-}
-
-// Criar agendamento
-async function criarAgendamento(dados) {
-    return await apiPost("/agendamentos", dados);
-}
-
-// Registrar venda
-async function registrarVenda(dados) {
-    return await apiPost("/vendas", dados);
-}
-
-// Lançar despesa
-async function lancarDespesa(dados) {
-    return await apiPost("/despesas", dados);
-}
-
-// Gerar relatório em PDF
-async function gerarRelatorio(tipo) {
-    return await apiGet(`/relatorios/${tipo}`);
-}
-
-// ==================== EXPORTAR FUNÇÕES ====================
-export {
-    loginUsuario,
-    cadastrarUsuario,
-    listarClientes,
-    cadastrarCliente,
-    listarProdutos,
-    cadastrarProduto,
-    listarServicos,
-    cadastrarServico,
-    listarAgendamentos,
-    criarAgendamento,
-    registrarVenda,
-    lancarDespesa,
-    gerarRelatorio
-};
+"""Utility helpers for the Streamlit frontend.
+
+All HTTP requests to the backend API go through this module.  The base
+URL is configurable via the ``API_URL`` environment variable, making it
+straightforward to point the frontend at different Railway deployments.
+"""
+
+from __future__ import annotations
+
+import os
+from datetime import datetime
+from typing import Any, Dict, Optional
+
+import requests
+import streamlit as st
+
+# Base URL for the backend API.  Can be overridden at runtime with the
+# ``API_URL`` environment variable.
+API_URL = os.getenv("API_URL", "https://agendamento-banco-de-dados.up.railway.app")
+
+
+def token_header() -> Dict[str, str]:
+    """Return an Authorization header using the token in ``st.session_state``.
+
+    Returns an empty dictionary when the user is not logged in.
+    """
+
+    token = st.session_state.get("token")
+    return {"Authorization": f"Bearer {token}"} if token else {}
+
+
+def _request(method: str, endpoint: str, token: Optional[str] = None, **kwargs: Any) -> Optional[requests.Response]:
+    """Internal helper to perform HTTP requests against the API."""
+
+    headers = kwargs.pop("headers", {})
+    if token:
+        headers["Authorization"] = token
+    url = f"{API_URL}{endpoint}"
+    try:
+        resp = requests.request(method, url, headers=headers, timeout=10, **kwargs)
+        if resp.ok:
+            return resp
+        return None
+    except requests.RequestException:
+        return None
+
+
+def api_get(endpoint: str, token: Optional[str] = None) -> Optional[Any]:
+    resp = _request("GET", endpoint, token)
+    return resp.json() if resp is not None else None
+
+
+def api_post(endpoint: str, data: Any, token: Optional[str] = None) -> Optional[Any]:
+    headers = {"Content-Type": "application/json"}
+    resp = _request("POST", endpoint, token, json=data, headers=headers)
+    return resp.json() if resp is not None else None
+
+
+def api_delete(endpoint: str, token: Optional[str] = None) -> bool:
+    resp = _request("DELETE", endpoint, token)
+    return resp is not None
+
+
+def formatar_data_br(data_str: str) -> str:
+    """Converte ``YYYY-MM-DD`` para ``DD/MM/YYYY``."""
+
+    try:
+        return datetime.strptime(data_str, "%Y-%m-%d").strftime("%d/%m/%Y")
+    except Exception:
+        return data_str
+
+
+__all__ = [
+    "API_URL",
+    "api_delete",
+    "api_get",
+    "api_post",
+    "formatar_data_br",
+    "token_header",
+]
