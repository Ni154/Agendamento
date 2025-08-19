
 import streamlit as st
 import requests
 
-API_URL = "https://seu-backend.onrender.com"  # Ajuste para sua URL backend
+from frontend.utils import API_URL, token_header
 
 def dashboard_page():
     st.title("📊 Dashboard")
 
-    headers = {}
-    if "token" in st.session_state and st.session_state.token:
-        headers = {"Authorization": f"Bearer {st.session_state.token}"}
+    headers = token_header()
 
     try:
         response = requests.get(f"{API_URL}/dashboard", headers=headers)
         if response.status_code == 200:
             data = response.json()
 
             st.metric("Clientes", data.get("total_clientes", 0))
             st.metric("Vendas", data.get("total_vendas", 0))
             st.metric("Produtos", data.get("total_produtos", 0))
             st.metric("Serviços", data.get("total_servicos", 0))
             st.metric("Faturamento", f"R$ {data.get('total_faturamento', 0):.2f}")
             st.metric("Despesas", f"R$ {data.get('total_despesas', 0):.2f}")
             st.metric("Lucro Líquido", f"R$ {data.get('lucro_liquido', 0):.2f}")
         else:
             st.error("Erro ao carregar dados do dashboard")
     except Exception as e:
         st.error(f"Erro na requisição: {e}")
