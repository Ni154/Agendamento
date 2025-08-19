
+"""Blueprint of Streamlit pages for the frontend.
+
+This module centralizes the mapping between menu labels and the
+corresponding page rendering functions.  It acts similarly to a
+Flask/FastAPI blueprint, keeping all "routes" for the Streamlit
+interface in a single place so that ``main.py`` only needs to look up
+and execute the desired page.
+"""
+
+from typing import Callable, Dict
+
+from frontend.components import (
+    agendamento,
+    cadastro_cliente,
+    cadastro_produto,
+    cadastro_servico,
+    dashboard,
+    vendas,
+)
+
+# Mapping of menu labels to the callable that renders the page.
+ROUTES: Dict[str, Callable[[], None]] = {
+    "Dashboard": dashboard.dashboard_page,
+    "Cadastro Cliente": cadastro_cliente.clientes_page,
+    "Cadastro Produtos": cadastro_produto.produtos_page,
+    "Cadastro Serviços": cadastro_servico.servicos_page,
+    "Agendamento": agendamento.agendamento_page,
+    "Vendas": vendas.vendas_page,
+}
+
+__all__ = ["ROUTES"]
