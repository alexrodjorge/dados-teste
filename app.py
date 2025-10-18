import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ===============================
# 2️⃣ Carregar base de dados
# ===============================
df = pd.read_csv(
    "https://raw.githubusercontent.com/alexrodjorge/dados-teste/main/base.csv",
    sep=";", encoding="utf-8"
)

# ===============================
# 🎨 Configurações de cores e hover globais
# ===============================
CORES_CATEGORIA = {
    "Receita": "#2CA02C",
    "Despesa_Cond": "#1F77B4",
    "Despesa_DP": "#FF7F0E",
    "Despesa_Imobilizado": "#D62728",
    "Despesa_Tributaria": "#9467BD",
    "Receita_Ordinaria": "#17BECF",
    "Receita_Extra": "#BCBD22",
    "Outros": "#7F7F7F"
}

HOVER_TEMPLATE = "<b>%{label}</b><br>Valor: R$ %{value:,.2f}<br>%{percent}"

# ===============================
# Função utilitária para padronizar gráficos
# ===============================
def padronizar_grafico(fig):
    fig.update_traces(hovertemplate=HOVER_TEMPLATE)
    fig.update_layout(
        legend_title_text='Categoria',
        template='plotly_white',
        margin=dict(l=40, r=40, t=60, b=40)
    )
    return fig

# ===============================
# 3️⃣ Mapear categorias
# ===============================
mapa_classificacao = {
    # Despesa_Imobilizado
    'Moveis e Utensilios': 'Despesa_Imobilizado',
    'Aparelhos Celulares': 'Despesa_Imobilizado',
    'Moveis e Utensilios - Portaria': 'Despesa_Imobilizado',
    'Portão de acesso': 'Despesa_Imobilizado',
    'Postes e Placas de Sinalização': 'Despesa_Imobilizado',
    'Reforma Portaria': 'Despesa_Imobilizado',
    'Material /Servico - Iluminação interna': 'Despesa_Imobilizado',
    'Conservação e Manutençao da Portaria': 'Despesa_Imobilizado',

    # Despesa_DP
    'Adiantamento de Ferias': 'Despesa_DP',
    'Adiantamento de Salarios': 'Despesa_DP',
    'Salario a Pagar': 'Despesa_DP',
    'Rescisao a Pagar': 'Despesa_DP',
    'Pis s/Folha de Pagamento': 'Despesa_DP',
    'IRRF': 'Despesa_DP',
    'INSS a Pagar': 'Despesa_DP',
    'FGTS a Pagar': 'Despesa_DP',
    'Emprestimo Consignado Colaborador Fgts': 'Despesa_DP',
    'Vale Transporte': 'Despesa_DP',
    'Uniformes': 'Despesa_DP',
    'Cartao Alimentacao\\Cesta Basica\\Cesta Natal': 'Despesa_DP',
    'Assistencia Familiar e  Funeral Sindeac PAF': 'Despesa_DP',
    'Consultoria em Medicina do Trabalho': 'Despesa_DP',
    'Rescisão': 'Despesa_DP',
    'Pro- Labore': 'Despesa_DP',
    'Sindeac PROFPS': 'Despesa_DP',
    'Servico de Suporte na Administracao': 'Despesa_DP',
    'Sistema de Ponto': 'Despesa_DP',
    'Material de Segurança EPI': 'Despesa_DP',

    # Despesa_Cond
    'Caixa Síndico': 'N.A',
    'Conservacao e Manutencao': 'Despesa_Cond',
    'Correio': 'Despesa_Cond',
    'Material de Construçao': 'Despesa_Cond',
    'Sistema Interno Cond 21': 'Despesa_Cond',
    'Honorarios Contabeis': 'Despesa_Cond',
    'Material de limpeza': 'Despesa_Cond',
    'Servico Eletricista': 'Despesa_Cond',
    'Lanches e Refeicoes': 'Despesa_Cond',
    'Locaçao de Equipamentos/ Veiculos': 'Despesa_Cond',
    'Reembolso de Quilometragem': 'Despesa_Cond',
    'Despesas c/ Servicos Terceiros (PJ)': 'Despesa_Cond',
    'Despesas c/ Servicos Terceiros (PF)': 'Despesa_Cond',
    'Combustivel/Lubrificantes/Troca Oleo': 'Despesa_Cond',
    'Conservacao e manutencao de Motos': 'Despesa_Cond',
    'Energia Eletrica': 'Despesa_Cond',
    'Despesas com transporte e entrega': 'Despesa_Cond',
    'Telefone/Internet': 'Despesa_Cond',
    'Despesas c/Chaveiro': 'Despesa_Cond',
    'Seguros': 'Despesa_Cond',
    'Despesas com Assembleia': 'Despesa_Cond',
    'Fretes e Carretos': 'Despesa_Cond',
    'Material de divulgacao': 'Despesa_Cond',
    'Material Eletrico': 'Despesa_Cond',
    'Material/Serviço Poco Artesiano': 'Despesa_Cond',
    'Material de Escritorio/Toner/Manutenção Impressora': 'Despesa_Cond',
    'Encadernaçao de livros': 'Despesa_Cond',
    'Bens de Reduzido Valor': 'Despesa_Cond',
    'Material Hidraulico': 'Despesa_Cond',
    'Material de Copa': 'Despesa_Cond',

    # Receita Ordinária
    'Taxa de Condominio': 'Receita_Ordinaria',
    'Taxa Condominio Acordo administrativo': 'Receita_Ordinaria',
    'Taxa Consumo de Agua': 'Receita_Ordinaria',
    'Receitas de Aplicacoes Financeiras': 'Receita_Ordinaria',
    'Multa e Juros': 'Receita_Ordinaria',

    # Receita Extraordinária
    'Taxa de instalacao de hidrometro': 'Receita_Extra',
    'Taxa Controle de Acesso': 'Receita_Extra',
    'Taxa Espaço Gourmet': 'Receita_Extra',
    'Taxa Multa': 'Receita_Extra',
    'Receita Reembolso Mercado Livre': 'Receita_Extra',

    # Tributário
    'IPTU': 'Despesa_Tributaria',
    'IPVA': 'Despesa_Tributaria',
    'Dae- Recursos Hidricos': 'Despesa_Tributaria',
    'Taxa de Alvara': 'Despesa_Tributaria',
    'Tarifas Bancarias': 'Despesa_Tributaria',
    'Juros e Multa': 'Despesa_Tributaria',
    'IOF/IRRF': 'Despesa_Tributaria'
}

# 2️⃣ Strip nos nomes da base
df["ContaNome"] = df["ContaNome"].astype(str).str.strip()

# 3️⃣ Aplicar classificação
df["Categoria"] = df["ContaNome"].map(mapa_classificacao)

# ===============================
# 4️⃣ Ajuste de valores numéricos
# ===============================
df["Debito"] = df["Debito"].astype(str).str.replace(",", ".").astype(float).round(2)
df["Credito"] = df["Credito"].astype(str).str.replace(",", ".").astype(float).round(2)

# ===============================
# 5️⃣ Criar coluna de Mês e Ano
# ===============================
df["Data"] = pd.to_datetime(df["Data"], dayfirst=True)
df["Mes"] = df["Data"].dt.to_period("M")
df["Ano"] = df["Data"].dt.year

# ===============================
# 5️⃣ Inicializar session_state
# ===============================
if "tipo_despesa" not in st.session_state:
    st.session_state.tipo_despesa = "Todos"
if "tipo_receita" not in st.session_state:
    st.session_state.tipo_receita = "Todos"
if "periodo" not in st.session_state:
    st.session_state.periodo = "Todos"

def atualizar_despesa():
    if st.session_state.tipo_despesa != "Todos":
        st.session_state.tipo_receita = "Todos"

def atualizar_receita():
    if st.session_state.tipo_receita != "Todos":
        st.session_state.tipo_despesa = "Todos"

# ===============================
# 6️⃣ Aplicar filtros globais
# ===============================
# Filtros precisam estar aqui, antes de qualquer página
periodo = st.session_state.periodo  # valor padrão
if "periodo" in st.session_state:
    periodo = st.session_state.periodo

df_filtrado = df.copy()
if st.session_state.tipo_despesa != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Categoria"].str.contains(st.session_state.tipo_despesa)]
if st.session_state.tipo_receita != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Categoria"].str.contains(st.session_state.tipo_receita)]
if periodo != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Mes"].astype(str) == periodo]

df_graf = df_filtrado.copy()

# ===============================
# Nº de meses para dividir as médias
# - quando "Todos": usa a qtd de meses da base (ex.: 7 de jan–jul/25)
# - quando um mês específico está selecionado: usa 1
# >> Se quiser FORÇAR sempre 7 meses, troque a linha do n_meses pelo: n_meses = 7
# ===============================
n_meses_base = df['Mes'].nunique()
n_meses = 1 if periodo != "Todos" else n_meses_base

# ===============================
# 8️⃣ Consolidações dinâmicas
# ===============================
if not df_filtrado.empty:
    cat_summary = df_filtrado.groupby("Categoria")[["Debito","Credito"]].agg(["sum","mean"]).round(2)
else:
    cat_summary = pd.DataFrame(columns=pd.MultiIndex.from_product([["Debito","Credito"], ["sum","mean"]]))

# ===============================
# 8️⃣ Consolidações dinâmicas
# ===============================
if not df_filtrado.empty:
    cat_summary_filtrado = df_filtrado.groupby("Categoria")[["Debito","Credito"]].agg(["sum","mean","max"]).round(2)
    conta_summary_filtrado = df_filtrado.groupby(["Categoria","ContaNome"])[["Debito","Credito"]].agg(["sum","mean","max"]).round(2)
    percentual_categoria_filtrado = df_filtrado.groupby(["Categoria","ContaNome"])[["Debito"]].sum()
    percentual_categoria_filtrado["%Categoria"] = percentual_categoria_filtrado.groupby(level=0)["Debito"].transform(lambda x: 100*x/x.sum())
    percentual_categoria_filtrado = percentual_categoria_filtrado.round(2)
else:
    cat_summary_filtrado = pd.DataFrame(columns=pd.MultiIndex.from_product([["Debito","Credito"], ["sum","mean","max"]]))
    conta_summary_filtrado = pd.DataFrame(columns=pd.MultiIndex.from_product([["Debito","Credito"], ["sum","mean","max"]]))
    percentual_categoria_filtrado = pd.DataFrame(columns=["Debito","%Categoria"])


# ===============================
# 8️⃣ Configuração de páginas
# ===============================
st.sidebar.title("Menu")
pagina = st.sidebar.radio("Escolha a Página:", ["Dashboard", "Bases"])

st.sidebar.markdown("### Filtros Globais")

periodo = st.sidebar.selectbox(
    "Período (Ano-Mês)",
    ["Todos"] + [str(m) for m in df["Mes"].sort_values().unique()],
    key="periodo"   # <- atualiza o session_state automaticamente
)
st.sidebar.selectbox(
    "Tipo de Despesa",
    ["Todos", "Despesa_Cond", "Despesa_DP", "Despesa_Imobilizado", "Despesa_Tributaria"],
    key="tipo_despesa",
    on_change=atualizar_despesa,
    disabled=st.session_state.tipo_receita != "Todos"
)
st.sidebar.selectbox(
    "Tipo de Receita",
    ["Todos", "Receita_Ordinaria", "Receita_Extra"],
    key="tipo_receita",
    on_change=atualizar_receita,
    disabled=st.session_state.tipo_despesa != "Todos"
)

# ===============================
# Página 1: Dashboard
# ===============================
if pagina == "Dashboard":
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: baseline;">
        <h2>📊 Prestação de Contas<br><small>Condomínio Retiro Três Barras</small></h2>
        <p style="font-size:16px; color:gray;">Janeiro/2025 a Setembro/2025</p>
    </div>
    """, unsafe_allow_html=True)

    # ===============================
    # 🔹 Bloco 1 - Fundo de Reserva
    # ===============================
    col1, col2 = st.columns(2)
    col1.metric("💼 Saldo Fundo de Reserva (12/2024)", "R$ 90.772,22")
    col2.metric("💼 Saldo Fundo de Reserva (09/2025)", "R$ 99.650,25")

    # ===============================
    # 🔹 Bloco 2 - Saldo Bancário
    # ===============================
    col3, col4 = st.columns(2)
    col3.metric("🏦 Saldo em Conta (12/2024)", "R$ 116.322,36")
    col4.metric("🏦 Saldo em Conta (09/2025)", "R$ 108.838,91")

    # ===============================
    # 🔹 Bloco 3 - Resultado do Período
    # ===============================
    col5, col6, col7 = st.columns(3)
    total_receita = df_filtrado[df_filtrado["Categoria"].str.contains("Receita", na=False)]["Credito"].sum()
    total_despesa = df_filtrado[df_filtrado["Categoria"].str.contains("Despesa", na=False)]["Debito"].sum()
    resultado = total_receita - total_despesa

    col5.metric("📈 Receita Total", f"R$ {total_receita:,.2f}")
    col6.metric("📉 Despesa Total", f"R$ {total_despesa:,.2f}")

    if resultado >= 0:
        resultado_texto = f"🟢 Superávit: R$ {resultado:,.2f}"
    else:
        resultado_texto = f"🔴 Déficit: R$ {abs(resultado):,.2f}"

    col7.metric("⚖️ Resultado do Período", f"R$ {resultado:,.2f}")
    st.markdown(f"<p style='text-align:center; color:gray;'>{resultado_texto}</p>", unsafe_allow_html=True)

    # ===============================
    # 🔹 Gráficos
    # ===============================
    st.markdown("---")

    periodo_atual = str(st.session_state.periodo)
    tipo_despesa = st.session_state.get("tipo_despesa", "Todos")
    tipo_receita = st.session_state.get("tipo_receita", "Todos")

    # ==========================================================
    # 📊 CASO 1 — PERÍODO = "TODOS"  →  Gráfico de barras mensais
    # ==========================================================
    if periodo_atual == "Todos":
        mensal = df_graf.groupby(["Mes", "Categoria"])[["Debito","Credito"]].sum().reset_index()
        despesa = (
            mensal[mensal["Categoria"].str.contains("Despesa", na=False)]
            .groupby("Mes", as_index=False)["Debito"]
            .sum()
        )
        receita = (
            mensal[mensal["Categoria"].str.contains("Receita", na=False)]
            .groupby("Mes", as_index=False)["Credito"]
            .sum()
        )
        graf_data = pd.merge(receita, despesa, on="Mes", how="outer").sort_values("Mes")
        graf_data = graf_data.fillna(0)
        graf_data["Mes_str"] = graf_data["Mes"].astype(str)

        # 🔹 Definir título dinâmico conforme os filtros
        if tipo_despesa != "Todos" and "Despesa" in tipo_despesa:
            titulo = f"Detalhamento Mensal das {tipo_despesa.replace('_', ' ')}"
            y_cols = ["Debito"]
            color_map = {"Debito": CORES_CATEGORIA.get(tipo_despesa, "#FF4B4B")}
        elif tipo_receita != "Todos" and "Receita" in tipo_receita:
            titulo = f"Detalhamento Mensal das {tipo_receita.replace('_', ' ')}"
            y_cols = ["Credito"]
            color_map = {"Credito": CORES_CATEGORIA.get(tipo_receita, "#4CAF50")}
        else:
            titulo = "Receita x Despesa Média Mensal"
            y_cols = ["Credito", "Debito"]
            color_map = {
                "Credito": CORES_CATEGORIA["Receita"],
                "Debito": CORES_CATEGORIA["Despesa_Cond"]
            }

        # 🔹 Criar gráfico dinâmico com estilo padronizado
        fig_receita_despesa = px.bar(
            graf_data,
            x="Mes_str",
            y=y_cols,
            barmode="group",
            labels={"Mes_str": "Mês", "value": "R$"},
            title=titulo,
            color_discrete_map=color_map,
            text_auto=".2f"
        )

        # 🔹 Formatação dos rótulos e tooltips
        fig_receita_despesa.update_traces(
            texttemplate="R$ %{y:,.2f}" if "Debito" in y_cols or "Credito" in y_cols else None,
            textposition="outside",
            hovertemplate="<b>Mês:</b> %{x}<br><b>Valor:</b> R$ %{y:,.2f}<extra></extra>",
            marker_line_width=0.5,
            marker_line_color="rgba(0,0,0,0.1)"
        )

        # 🔹 Layout geral (estilo semelhante aos gráficos horizontais)
        fig_receita_despesa.update_layout(
            title=dict(x=0.02, xanchor="left"),
            xaxis_title=None,
            yaxis_title="R$",
            bargap=0.25,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(size=12),
            legend=dict(
                title=None,
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )

        st.plotly_chart(fig_receita_despesa, use_container_width=True)


    # ==========================================================
    # 📊 CASO 2 — PERÍODO ESPECÍFICO  →  Gráficos de pizza
    # ==========================================================
    else:
        df_mes = df_graf[df_graf["Mes"].astype(str) == periodo_atual]
        df_despesa = df_mes[df_mes["Categoria"].str.contains("Despesa")].groupby("Categoria")[["Debito"]].sum().reset_index()
        df_receita = df_mes[df_mes["Categoria"].str.contains("Receita")].groupby("Categoria")[["Credito"]].sum().reset_index()

        col1, col2 = st.columns(2)
        with col1:
            fig_pie_despesa = px.pie(
                df_despesa,
                names="Categoria",
                values="Debito",
                title=f"Distribuição de Despesas - {periodo_atual}",
                hole=0.3,
                color="Categoria",
                color_discrete_map=CORES_CATEGORIA
            )
            fig_pie_despesa = padronizar_grafico(fig_pie_despesa)
            st.plotly_chart(fig_pie_despesa, use_container_width=True)

        with col2:
            fig_rec = px.pie(
                df_receita,
                names="Categoria",
                values="Credito",
                title=f"Distribuição de Créditos - {periodo_atual}",
                hole=0.3,
                color="Categoria",
                color_discrete_map=CORES_CATEGORIA
            )
            fig_rec = padronizar_grafico(fig_rec)
            st.plotly_chart(fig_rec, use_container_width=True)

    # ===============================
    # 🔹 Exibição de KPIs ou gráfico detalhado
    # ===============================
    st.markdown("---")

    # ==========================================================
    # CASO A — Tudo em "Todos" → Médias do período
    # ==========================================================
    if (
        periodo_atual == "Todos"
        and tipo_despesa == "Todos"
        and tipo_receita == "Todos"
    ):
        st.subheader("📊 Médias do Período")

        n_meses = df_filtrado["Mes"].nunique()

        # === MÉDIAS DE RECEITA ===
        receita_filtrada = df_filtrado[df_filtrado["Categoria"].str.contains("Receita", na=False)]
        media_rec_total = receita_filtrada["Credito"].sum() / n_meses if not receita_filtrada.empty else 0

        taxa_cond_filtrada = df_filtrado[df_filtrado["ContaNome"] == "Taxa de Condominio"]
        media_rec_taxa_cond = taxa_cond_filtrada["Credito"].sum() / n_meses if not taxa_cond_filtrada.empty else 0

        contas_taxa_acordo = [
            "Taxa Condominio Acordo administrativo",
            "Taxa Consumo de Agua",
            "Receitas de Aplicacoes Financeiras",
            "Multa e Juros",
            "Taxa de instalacao de hidrometro",
            "Taxa Controle de Acesso",
            "Taxa Espaço Gourmet",
            "Taxa Multa",
            "Receita Reembolso Mercado Livre"
        ]
        taxa_acordo_filtrada = df_filtrado[df_filtrado["ContaNome"].isin(contas_taxa_acordo)]
        media_rec_taxa_acordo = taxa_acordo_filtrada["Credito"].sum() / n_meses if not taxa_acordo_filtrada.empty else 0

        # === MÉDIAS DE DESPESA ===
        despesa_filtrada = df_filtrado[df_filtrado["Categoria"].str.contains("Despesa", na=False)]
        media_desp_total = despesa_filtrada["Debito"].sum() / n_meses if not despesa_filtrada.empty else 0

        desp_dp_filtrada = df_filtrado[df_filtrado["Categoria"] == "Despesa_DP"]
        media_desp_dp = desp_dp_filtrada["Debito"].sum() / n_meses if not desp_dp_filtrada.empty else 0

        outras_desp_filtrada = df_filtrado[df_filtrado["Categoria"].isin(["Despesa_Cond", "Despesa_Imobilizado", "Despesa_Tributaria"])]
        media_desp_outras = outras_desp_filtrada["Debito"].sum() / n_meses if not outras_desp_filtrada.empty else 0

        # === Exibição KPI's ===
        col1, col2, col3 = st.columns(3)
        col1.metric("💰 Média Total Receita", f"R$ {media_rec_total:,.2f}")
        col2.metric("💰 Média Taxa de Condomínio", f"R$ {media_rec_taxa_cond:,.2f}")
        col3.metric("💰 Outras Receitas", f"R$ {media_rec_taxa_acordo:,.2f}")

        col4, col5, col6 = st.columns(3)
        col4.metric("📉 Média Total Despesa", f"R$ {media_desp_total:,.2f}")
        col5.metric("📉 Média Despesa DP", f"R$ {media_desp_dp:,.2f}")
        col6.metric("📉 Outras Despesas", f"R$ {media_desp_outras:,.2f}")

    # ==========================================================
    # CASO B — Período = "Todos" mas há filtro → Detalhamento consolidado
    # ==========================================================
    elif (
        periodo_atual == "Todos"
        and (tipo_despesa != "Todos" or tipo_receita != "Todos")
    ):
        st.subheader("📊 Detalhamento — Todos (Consolidado)")

        df_mes = df_graf.copy()  # todos os meses, consolidado

        # --- Despesas detalhadas ---
        df_despesa = (
            df_mes[df_mes["Categoria"].str.contains("Despesa", na=False)]
            .groupby("ContaNome", as_index=False)[["Debito"]]
            .sum()
            .sort_values("Debito", ascending=True)
        )

        if not df_despesa.empty:
            df_despesa["Percentual"] = df_despesa["Debito"] / df_despesa["Debito"].sum() * 100
            num_categorias_desp = len(df_despesa)
            cores_desp_seq = px.colors.sequential.Oranges_r
            cores_desp = [
                cores_desp_seq[int(i * (len(cores_desp_seq) - 1) / max(1, num_categorias_desp - 1))]
                for i in range(num_categorias_desp)
            ]

            fig_desp = px.bar(
                df_despesa,
                x="Debito",
                y="ContaNome",
                orientation='h',
                labels={"Debito": "R$", "ContaNome": "Conta"},
                title="Detalhamento de Despesas - Consolidado",
                text="Debito",
                custom_data=["Percentual"]
            )
            fig_desp.update_traces(
                marker_color=cores_desp,
                texttemplate="R$ %{x:,.2f}",
                textposition="outside",
                hovertemplate="<b>%{y}</b><br>R$ %{x:,.2f} (%{customdata[0]:.2f}%)<extra></extra>"
            )
            st.plotly_chart(fig_desp, use_container_width=True)
        else:
            st.info("Nenhuma despesa neste filtro.")

        # --- Receitas detalhadas ---
        df_receita = (
            df_mes[df_mes["Categoria"].str.contains("Receita", na=False)]
            .groupby("ContaNome", as_index=False)[["Credito"]]
            .sum()
            .sort_values("Credito", ascending=True)
        )

        if not df_receita.empty:
            df_receita["Percentual"] = df_receita["Credito"] / df_receita["Credito"].sum() * 100
            num_categorias_rec = len(df_receita)
            cores_rec_seq = px.colors.sequential.Greens_r
            cores_rec = [
                cores_rec_seq[int(i * (len(cores_rec_seq) - 1) / max(1, num_categorias_rec - 1))]
                for i in range(num_categorias_rec)
            ]

            fig_receita = px.bar(
                df_receita,
                x="Credito",
                y="ContaNome",
                orientation='h',
                labels={"Credito": "R$", "ContaNome": "Conta"},
                title="Detalhamento de Receitas - Consolidado",
                text="Credito",
                custom_data=["Percentual"]
            )
            fig_receita.update_traces(
                marker_color=cores_rec,
                texttemplate="R$ %{x:,.2f}",
                textposition="outside",
                hovertemplate="<b>%{y}</b><br>R$ %{x:,.2f} (%{customdata[0]:.2f}%)<extra></extra>"
            )
            st.plotly_chart(fig_receita, use_container_width=True)
        else:
            st.info("Nenhuma receita neste filtro.")

    # ==========================================================
    # CASO C — Período específico → Detalhamento do mês
    # ==========================================================
    else:
        st.subheader(f"📊 Detalhamento — {periodo_atual}")

        df_mes = df_graf[df_graf["Mes"].astype(str) == periodo_atual]

        # --- Despesas detalhadas ---
        df_despesa = (
            df_mes[df_mes["Categoria"].str.contains("Despesa", na=False)]
            .groupby("ContaNome", as_index=False)[["Debito"]]
            .sum()
            .sort_values("Debito", ascending=True)
        )

        if not df_despesa.empty:
            df_despesa["Percentual"] = df_despesa["Debito"] / df_despesa["Debito"].sum() * 100
            num_categorias_desp = len(df_despesa)
            cores_desp_seq = px.colors.sequential.Oranges_r
            cores_desp = [
                cores_desp_seq[int(i * (len(cores_desp_seq) - 1) / max(1, num_categorias_desp - 1))]
                for i in range(num_categorias_desp)
            ]

            fig_desp = px.bar(
                df_despesa,
                x="Debito",
                y="ContaNome",
                orientation='h',
                labels={"Debito": "R$", "ContaNome": "Conta"},
                title=f"Detalhamento de Despesas - {periodo_atual}",
                text="Debito",
                custom_data=["Percentual"]
            )
            fig_desp.update_traces(
                marker_color=cores_desp,
                texttemplate="R$ %{x:,.2f}",
                textposition="outside",
                hovertemplate="<b>%{y}</b><br>R$ %{x:,.2f} (%{customdata[0]:.2f}%)<extra></extra>"
            )
            st.plotly_chart(fig_desp, use_container_width=True)
        else:
            st.info("Nenhuma despesa neste filtro.")

        # --- Receitas detalhadas ---
        df_receita = (
            df_mes[df_mes["Categoria"].str.contains("Receita", na=False)]
            .groupby("ContaNome", as_index=False)[["Credito"]]
            .sum()
            .sort_values("Credito", ascending=True)
        )

        if not df_receita.empty:
            df_receita["Percentual"] = df_receita["Credito"] / df_receita["Credito"].sum() * 100
            num_categorias_rec = len(df_receita)
            cores_rec_seq = px.colors.sequential.Greens_r
            cores_rec = [
                cores_rec_seq[int(i * (len(cores_rec_seq) - 1) / max(1, num_categorias_rec - 1))]
                for i in range(num_categorias_rec)
            ]

            fig_receita = px.bar(
                df_receita,
                x="Credito",
                y="ContaNome",
                orientation='h',
                labels={"Credito": "R$", "ContaNome": "Conta"},
                title=f"Detalhamento de Receitas - {periodo_atual}",
                text="Credito",
                custom_data=["Percentual"]
            )
            fig_receita.update_traces(
                marker_color=cores_rec,
                texttemplate="R$ %{x:,.2f}",
                textposition="outside",
                hovertemplate="<b>%{y}</b><br>R$ %{x:,.2f} (%{customdata[0]:.2f}%)<extra></extra>"
            )
            st.plotly_chart(fig_receita, use_container_width=True)
        else:
            st.info("Nenhuma receita neste filtro.")

# ===============================
# Página 3: Bases
# ===============================
if pagina == "Bases":
    st.subheader("📄 Bases de Dados")

    with st.expander("📊 Base Filtrada"):
        st.caption(f"{len(df_filtrado):,} registros — Período: {st.session_state.periodo}")
        st.dataframe(df_filtrado)

    with st.expander("📊 Consolidação por Categoria"):
        st.dataframe(cat_summary_filtrado)

    with st.expander("📊 Consolidação por Categoria e Conta"):
        st.dataframe(conta_summary_filtrado)

    with st.expander("📊 Percentual de cada Conta na Categoria"):
        st.dataframe(percentual_categoria_filtrado)

    st.download_button(
        "⬇️ Baixar Base Filtrada (CSV)",
        data=df_filtrado.to_csv(index=False).encode("utf-8"),
        file_name="base_filtrada.csv",
        mime="text/csv"
    )

