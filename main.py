# dashboard_online_retail.py
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
# ------------------------
# Funções auxiliares
# ------------------------
@st.cache_data
def carregar_dados():
    df = pd.read_excel("Online Retail.xlsx")
    df = df.dropna(subset=["CustomerID"])
    df["PreçoTotal"] = df["Quantity"] * df["UnitPrice"]
    df["DataNota"] = pd.to_datetime(df["InvoiceDate"])
    df["Mês"] = df["DataNota"].dt.to_period("M").dt.to_timestamp()
    df["Hora"] = df["DataNota"].dt.hour
    df["DiaSemana"] = df["DataNota"].dt.day_name()

    df = df.rename(columns={
        "InvoiceNo": "NotaFiscal",
        "StockCode": "CódigoProduto",
        "Description": "Descrição",
        "Quantity": "Quantidade",
        "UnitPrice": "PreçoUnitário",
        "CustomerID": "ClienteID",
        "Country": "País"
    })
    return df

# ------------------------
# Carregamento dos dados
# ------------------------
df = carregar_dados()

# ------------------------
# Sidebar - Filtros globais
# ------------------------
st.sidebar.title("Dashboard - Online Retail")

st.sidebar.markdown("""
#### ℹ️ Sobre o Dashboard
Este painel interativo tem como objetivo analisar os dados de vendas do dataset Online Retail.

""")

# Filtro por data
data_min = df["DataNota"].min()
data_max = df["DataNota"].max()
periodo = st.sidebar.date_input("🗓️ Período:", (data_min, data_max), format="DD/MM/YYYY")
if len(periodo) == 2:
    df = df[(df["DataNota"] >= pd.to_datetime(periodo[0])) & (df["DataNota"] <= pd.to_datetime(periodo[1]))]

# Botão para download dos dados filtrados
csv = df.to_csv(index=False).encode('utf-8')
st.sidebar.download_button(
    label="⬇️ Baixar dados filtrados",
    data=csv,
    file_name='dados_filtrados.csv',
    mime='text/csv'
)

# ------------------------
# Navegação entre páginas
# ------------------------
pagina = st.sidebar.radio("Ir para:", [
    "Visão Geral",
    "Produtos",
    "Clientes e Países",
    "Análises Temporais"
])

st.sidebar.markdown("""
#### ℹ️ Navegação
Você pode navegar entre as páginas usando o menu lateral. Cada seção apresenta diferentes perspectivas dos dados:
- **Visão Geral:** indicadores e receita mensal.
- **Produtos:** análise de produtos mais vendidos e preços.
- **Clientes e Países:** principais clientes e países com maior receita.
- **Análises Temporais:** comportamento por hora e dia da semana.

**Filtros de período** disponíveis no topo da barra lateral afetam todos os dados exibidos nas páginas.
""")
# ------------------------
# Página 1 - Visão Geral
# ------------------------
if pagina == "Visão Geral":
    st.title("📈 Visão Geral das Vendas")
    st.markdown("Resumo geral de indicadores e tendências mensais.")

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Receita Total", f"£{df['PreçoTotal'].sum():,.2f}")
    col2.metric("📦 Pedidos", df["NotaFiscal"].nunique())
    col3.metric("🧑‍💼 Clientes", df["ClienteID"].nunique())

    # Indicadores extras
    pedido_medio = df["PreçoTotal"].sum() / df["NotaFiscal"].nunique()
    produto_top = df.groupby("Descrição")["Quantidade"].sum().idxmax()
    cliente_top = df.groupby("ClienteID")["PreçoTotal"].sum().idxmax()

    st.info(f"📌 Pedido médio: £{pedido_medio:,.2f}\n\n🔝 Produto mais vendido: {produto_top}\n\n🏆 Melhor Cliente: {cliente_top}")

    # Receita mensal
    receita_mensal = df.groupby("Mês")["PreçoTotal"].sum().reset_index()
    fig = px.line(receita_mensal, x="Mês", y="PreçoTotal", markers=True, title="Receita Mensal")
    st.plotly_chart(fig, use_container_width=True)

# ------------------------
# Página 2 - Produtos
# ------------------------
elif pagina == "Produtos":
    st.title("📦 Produtos Vendidos")
    st.markdown("Analise os produtos mais populares e a distribuição dos preços unitários.")

    paises = sorted(df['País'].unique())
    pais_selecionado = st.selectbox("🌍 Selecione o país:", options=paises, index=paises.index("United Kingdom"))
    df_filtrado = df[df['País'] == pais_selecionado]

    tab1, tab2 = st.tabs(["🔝 Top Produtos", "💲 Preços por Unidade"])

    with tab1:
        top_produtos = df_filtrado.groupby("Descrição")["Quantidade"].sum().sort_values(ascending=False).head(10)
        fig_bar = px.bar(top_produtos, x=top_produtos.values, y=top_produtos.index,
                         orientation='h', title=f"Top 10 Produtos - {pais_selecionado}")
        st.plotly_chart(fig_bar, use_container_width=True)

    with tab2:
        max_preco = int(df["PreçoUnitário"].quantile(0.99))
        faixa_preco = st.slider("Faixa de preço:", 0, max_preco, (0, max_preco))
        df_preco = df_filtrado[(df_filtrado["PreçoUnitário"] >= faixa_preco[0]) & (df_filtrado["PreçoUnitário"] <= faixa_preco[1])]
        fig_hist = px.histogram(df_preco, x="PreçoUnitário", nbins=50, title="Distribuição dos Preços")
        st.plotly_chart(fig_hist, use_container_width=True)

# ------------------------
# Página 3 - Clientes e Países
# ------------------------
elif pagina == "Clientes e Países":
    st.title("🌍 Clientes e Países")

    tab1, tab2 = st.tabs(["🌐 Receita por País", "👤 Receita por Cliente"])

    with tab1:
        receita_paises = df.groupby("País")["PreçoTotal"].sum().sort_values(ascending=False).head(10)
        fig_paises = px.bar(receita_paises, x=receita_paises.index, y=receita_paises.values,
                            labels={"x": "País", "y": "Receita"}, title="Top 10 Países por Receita")
        st.plotly_chart(fig_paises, use_container_width=True)

    with tab2:
        min_receita = int(df["PreçoTotal"].sum() * 0.001)
        receita_min = st.slider("Receita mínima:", min_receita, 10000, min_receita)
        receita_clientes = df.groupby("ClienteID")["PreçoTotal"].sum().reset_index()
        receita_clientes = receita_clientes[receita_clientes["PreçoTotal"] >= receita_min].sort_values("PreçoTotal", ascending=False).head(10)
        fig_clientes = px.bar(receita_clientes, x="ClienteID", y="PreçoTotal",
                              labels={"ClienteID": "Cliente", "PreçoTotal": "Receita"},
                              title="Top 10 Clientes por Receita")
        st.plotly_chart(fig_clientes, use_container_width=True)
        st.dataframe(receita_clientes, use_container_width=True)

# ------------------------
# Página 4 - Análises Temporais
# ------------------------
elif pagina == "Análises Temporais":
    st.title("⏱️ Análises Temporais")

    tab1, tab2 = st.tabs(["🕘 Pedidos por Hora", "📅 Pedidos por Dia da Semana"])

    with tab1:
        pedidos_hora = df.groupby("Hora")["NotaFiscal"].nunique().reset_index(name="Pedidos")
        fig_hora = px.bar(pedidos_hora, x="Hora", y="Pedidos",
                          title="Pedidos por Hora do Dia",
                          labels={"Hora": "Hora", "Pedidos": "Pedidos"})
        st.plotly_chart(fig_hora, use_container_width=True)

    with tab2:
        pedidos_dia = df.groupby("DiaSemana")["NotaFiscal"].nunique().reset_index(name="Pedidos")
        ordem_dias = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        pedidos_dia["DiaSemana"] = pd.Categorical(pedidos_dia["DiaSemana"], categories=ordem_dias, ordered=True)
        pedidos_dia = pedidos_dia.sort_values("DiaSemana")
        fig_semana = px.bar(pedidos_dia, x="DiaSemana", y="Pedidos",
                            title="Pedidos por Dia da Semana",
                            labels={"DiaSemana": "Dia", "Pedidos": "Pedidos"})
        st.plotly_chart(fig_semana, use_container_width=True)

# ------------------------
# Rodapé
# ------------------------
st.sidebar.markdown("---")
st.sidebar.caption("Desenvolvido por Jonathan | Dataset: UCI Online Retail")
