
 API_URL = "https://seu-backend.onrender.com"
 
 def despesas_page():
     st.title("📉 Controle de Despesas")
 
     with st.form("form_despesa"):
         descricao = st.text_input("Descrição da Despesa")
         valor = st.number_input("Valor", min_value=0.0, step=0.01)
         data = st.date_input("Data", value=date.today())
         categoria = st.selectbox("Categoria", ["Aluguel", "Água", "Luz", "Internet", "Produtos", "Outros"])
 
         if st.form_submit_button("Salvar"):
             payload = {
                 "descricao": descricao,
                 "valor": valor,
                 "data": str(data),
                 "categoria": categoria
             }
             response = requests.post(f"{API_URL}/despesas", json=payload)
             if response.status_code == 201:
                 st.success("Despesa registrada com sucesso!")
             else:
                 st.error("Erro ao registrar despesa.")
 
     st.subheader("📜 Histórico de Despesas")
-    despesas = requests.get(f"{API_URL}/despesas").json()
+
+    agrupar_revenda = st.checkbox("Agrupar revendas por produto")
+    params = {"revenda": "true"} if agrupar_revenda else {}
+
+    dados_relatorio = requests.get(
+        f"{API_URL}/relatorio/despesas", params=params
+    ).json()
+    despesas = dados_relatorio.get("despesas", [])
 
     if despesas:
         st.table(despesas)
+        st.write(
+            f"Total: R$ {dados_relatorio.get('total_despesas', 0):.2f}"
+        )
     else:
         st.info("Nenhuma despesa cadastrada.")
