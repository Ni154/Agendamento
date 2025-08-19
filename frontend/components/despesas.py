 import streamlit as st
 import requests
+import pandas as pd
 from datetime import date
 
 API_URL = "https://seu-backend.onrender.com"
 
 def despesas_page():
     st.title("📉 Controle de Despesas")
 
     with st.form("form_despesa"):
         descricao = st.text_input("Descrição da Despesa")
         valor = st.number_input("Valor", min_value=0.0, step=0.01)
         data = st.date_input("Data", value=date.today())
-        categoria = st.selectbox("Categoria", ["Aluguel", "Água", "Luz", "Internet", "Produtos", "Outros"])
+        fornecedor = st.text_input("Fornecedor")
+        cnpj = st.text_input("CNPJ")
+        descricao_item = st.text_input("Descrição do Item")
+        preco_custo = st.number_input("Preço de Custo", min_value=0.0, step=0.01)
+        preco_venda = st.number_input("Preço de Venda", min_value=0.0, step=0.01)
+        revenda = st.checkbox("Revenda?")
+
+        produto = None
+        quantidade = None
+        categoria = None
+        if revenda:
+            produtos = requests.get(f"{API_URL}/produtos").json()
+            produto_nomes = [p.get("nome", "") for p in produtos]
+            produto = st.selectbox("Produto", produto_nomes)
+            quantidade = st.number_input("Quantidade", min_value=1, step=1)
+        else:
+            categorias = requests.get(f"{API_URL}/categorias").json()
+            if isinstance(categorias, list) and categorias:
+                categoria = st.selectbox("Categoria", [c.get("nome", c) for c in categorias])
+            else:
+                categoria = st.text_input("Categoria")
 
         if st.form_submit_button("Salvar"):
             payload = {
                 "descricao": descricao,
                 "valor": valor,
                 "data": str(data),
-                "categoria": categoria
+                "fornecedor": fornecedor,
+                "cnpj": cnpj,
+                "descricao_item": descricao_item,
+                "preco_custo": preco_custo,
+                "preco_venda": preco_venda,
+                "revenda": revenda
             }
+            if revenda:
+                payload.update({
+                    "produto": produto,
+                    "quantidade": quantidade
+                })
+            else:
+                payload["categoria"] = categoria
+
             response = requests.post(f"{API_URL}/despesas", json=payload)
             if response.status_code == 201:
                 st.success("Despesa registrada com sucesso!")
             else:
                 st.error("Erro ao registrar despesa.")
 
     st.subheader("📜 Histórico de Despesas")
     despesas = requests.get(f"{API_URL}/despesas").json()
 
     if despesas:
-        st.table(despesas)
+        df = pd.DataFrame(despesas)
+        colunas = [
+            "descricao",
+            "valor",
+            "data",
+            "fornecedor",
+            "cnpj",
+            "descricao_item",
+            "preco_custo",
+            "preco_venda",
+            "revenda",
+            "produto",
+            "quantidade",
+            "categoria",
+        ]
+        colunas_presentes = [c for c in colunas if c in df.columns]
+        st.table(df[colunas_presentes])
     else:
         st.info("Nenhuma despesa cadastrada.")
 
EOF
)
