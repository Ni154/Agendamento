import streamlit as st
import requests
import matplotlib.pyplot as plt

API_URL = "http://localhost:8000"  # ajuste para seu backend

def dashboard():
    st.subheader("📊 Visão Geral")

    try:
        res = requests.get(f"{API_URL}/dashboard/metrics")
        res.raise_for_status()
        metrics = res.json()
    except Exception as e:
        st.error(f"Erro ao carregar métricas: {e}")
        return

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("👥 Clientes", metrics.get("total_clientes", 0))
    col2.metric("🧾 Vendas", metrics.get("total_vendas", 0))
    col3.metric("📦 Produtos", metrics.get("total_produtos", 0))
    col4.metric("💆 Serviços", metrics.get("total_servicos", 0))

    st.metric("💰 Faturamento Total", f"R$ {metrics.get('total_faturamento', 0):.2f}")
    st.metric("💸 Despesas", f"R$ {metrics.get('total_despesas', 0):.2f}")
    st.metric("📈 Lucro Líquido", f"R$ {metrics.get('lucro_liquido', 0):.2f}")

    # Gráfico de vendas canceladas x realizadas
    vendas_data = metrics.get("vendas_data", {"realizadas": 0, "canceladas": 0})

    fig, ax = plt.subplots()
    ax.bar(
        ["Realizadas", "Canceladas"],
        [vendas_data.get("realizadas", 0), vendas_data.get("canceladas", 0)],
        color=["green", "red"]
    )
    ax.set_ylabel("Quantidade")
    ax.set_title("Resumo de Vendas")
    st.pyplot(fig)

