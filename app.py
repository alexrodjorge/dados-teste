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
    'Caixa Síndico': 'Ignorar',
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

mapa_analise = {
    # ======================
    # DESPESAS FIXAS
    # ======================
    'Adiantamento de Ferias': 'Despesa_Fixa',
    'Adiantamento de Salarios': 'Despesa_Fixa',
    'Assistencia Familiar e  Funeral Sindeac PAF': 'Despesa_Fixa',
    'Cartao Alimentacao\\Cesta Basica\\Cesta Natal': 'Despesa_Fixa',
    'Consultoria em Medicina do Trabalho': 'Despesa_Fixa',
    'FGTS a Pagar': 'Obrigacao_CP',
    'INSS a Pagar': 'Obrigacao_CP',
    'Pis s/Folha de Pagamento': 'Obrigacao_CP',
    'Pro- Labore': 'Despesa_Fixa',
    'Rescisão': 'Despesa_Variavel',  # não é recorrente
    'Salario a Pagar': 'Obrigacao_CP',
    'Servico de Suporte na Administracao': 'Despesa_Fixa',
    'Sindeac PROFPS': 'Despesa_Fixa',
    'Sistema de Ponto': 'Despesa_Fixa',
    'Uniformes': 'Despesa_Variavel',
    'Vale Transporte': 'Despesa_Fixa',
    'Rescisao a Pagar': 'Despesa_Variavel',
    'Emprestimo Consignado Colaborador Fgts': 'Despesa_Variavel',
    'Caixa Síndico': 'Ignorar',

    # ======================
    # DESPESAS FIXAS CONDOMÍNIO
    # ======================
    'Honorarios Contabeis': 'Despesa_Fixa',
    'Seguros': 'Despesa_Fixa',
    'Sistema Interno Cond 21': 'Despesa_Fixa',
    'Telefone/Internet': 'Despesa_Fixa',
    'Sistema Interno Despesa_Cond 21': 'Despesa_Fixa',
    'Energia Eletrica': 'Despesa_Fixa',  # recorrente
    'Despesas c/ Servicos Terceiros (PJ)': 'Despesa_Fixa',

    # ======================
    # DESPESAS VARIÁVEIS
    # ======================
    'Combustivel/Lubrificantes/Troca Oleo ': 'Despesa_Variavel',
    'Conservacao e Manutencao': 'Despesa_Variavel',
    'Conservacao e manutencao de Motos': 'Despesa_Variavel',
    'Conservação e Manutençao da Portaria': 'Despesa_Variavel',
    'Correio': 'Despesa_Variavel',
    'Despesas c/Chaveiro': 'Despesa_Variavel',
    'Despesas com Assembleia': 'Despesa_Variavel',
    'Despesas com transporte e entrega': 'Despesa_Variavel',
    'Encadernaçao de livros': 'Despesa_Variavel',
    'Fretes e Carretos': 'Despesa_Variavel',
    'Lanches e Refeicoes': 'Despesa_Variavel',
    'Locaçao de Equipamentos/ Veiculos': 'Despesa_Variavel',
    'Material Eletrico': 'Despesa_Variavel',
    'Material Hidraulico': 'Despesa_Variavel',
    'Material de Construçao': 'Despesa_Variavel',
    'Material de Copa': 'Despesa_Variavel',
    'Material de Escritorio/Toner/Manutenção Impressora': 'Despesa_Variavel',
    'Material de Segurança EPI': 'Despesa_Variavel',
    'Material de divulgacao ': 'Despesa_Variavel',
    'Material de limpeza': 'Despesa_Variavel',
    'Moveis e Utensilios - Portaria ': 'Despesa_Variavel',
    'Reembolso de Quilometragem': 'Despesa_Variavel',
    'Servico Eletricista': 'Despesa_Variavel',
    'Despesas c/ Servicos Terceiros (PF)': 'Despesa_Variavel',
    'Combustivel/Lubrificantes/Troca Oleo': 'Despesa_Variavel',
    'Material/Serviço Poco Artesiano': 'Despesa_Variavel',
    'Material de divulgacao': 'Despesa_Variavel',
    'Bens de Reduzido Valor': 'Despesa_Variavel',

    # ======================
    # Despesa_Imobilizado (não entra em custo mensal)
    # ======================
    'Material /Servico - Iluminação interna': 'Despesa_Imobilizado',
    'Portão de acesso': 'Despesa_Imobilizado',
    'Postes e Placas de Sinalização': 'Despesa_Imobilizado',
    'Reforma Portaria': 'Despesa_Imobilizado',
    'Aparelhos Celulares' : 'Despesa_Imobilizado',
    'Moveis e Utensilios': 'Despesa_Imobilizado',
    'Moveis e Utensilios - Portaria': 'Despesa_Imobilizado',

    # ======================
    # TRIBUTOS (curto prazo)
    # ======================
    'IOF/IRRF': 'Obrigacao_CP',
    'IPTU': 'Obrigacao_CP',
    'IPVA': 'Obrigacao_CP',
    'IRRF': 'Obrigacao_CP',
    'Multa e Juros': 'Despesa_Variavel',
    'Tarifas Bancarias': 'Despesa_Variavel',
    'Taxa de Alvara': 'Obrigacao_CP',
    'Dae- Recursos Hidricos': 'Obrigacao_CP',
    'Juros e Multa': 'Obrigacao_CP',

    # ======================
    # RECEITAS
    # ======================
    'Taxa Condominio Acordo administrativo': 'Receita',
    'Taxa Consumo de Agua': 'Receita',
    'Taxa de Condominio': 'Receita',
    'Receita Reembolso Mercado Livre': 'Receita',
    'Receitas de Aplicacoes Financeiras': 'Receita',
    'Taxa Controle de Acesso': 'Receita',
    'Taxa Espaço Gourmet': 'Receita',
    'Taxa de instalacao de hidrometro': 'Receita',
    'Taxa Multa': 'Receita'

    # ======================
    # APLICAÇÕES (tratar como Caixa)
    # ======================
    #'Aplicação Caixa Econômica Federal - resgate' : 'Disponivel',
    #'Aplicação Caixa Econômica Federal' : 'Disponivel'
}

# Mapear a classificação analítica
df["Classificacao_Analise"] = df["ContaNome"].map(mapa_analise).fillna("Nao_Classificado")

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
pagina = st.sidebar.radio("Escolha a Página:", ["Dashboard", "Análise Contábil", "Bases"])

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

    if st.session_state.periodo == "Todos":
        mensal = df_graf.groupby(["Mes", "Categoria"])[["Debito", "Credito"]].sum().reset_index()
        despesa = mensal[mensal["Categoria"].str.contains("Despesa")].groupby("Mes")["Debito"].mean().reset_index()
        receita = mensal[mensal["Categoria"].str.contains("Receita")].groupby("Mes")["Credito"].mean().reset_index()
        graf_data = pd.merge(receita, despesa, on="Mes", how="outer").sort_values("Mes")
        graf_data["Mes_str"] = graf_data["Mes"].astype(str)

        fig = px.bar(
            graf_data,
            x="Mes_str",
            y=["Credito", "Debito"],
            barmode="group",
            labels={"Mes_str": "Mês", "value": "R$"},
            title="Receita x Despesa Média Mensal"
        )
        st.plotly_chart(fig, use_container_width=True)

    else:
        df_mes = df_graf[df_graf["Mes"].astype(str) == st.session_state.periodo]
        df_despesa = df_mes[df_mes["Categoria"].str.contains("Despesa")].groupby("Categoria")[["Debito"]].sum().reset_index()
        df_receita = df_mes[df_mes["Categoria"].str.contains("Receita")].groupby("Categoria")[["Credito"]].sum().reset_index()

        col1, col2 = st.columns(2)
        with col1:
            fig_desp = px.pie(
                df_despesa, names="Categoria", values="Debito",
                title=f"Distribuição de Débitos - {st.session_state.periodo}"
            )
            st.plotly_chart(fig_desp, use_container_width=True)
        with col2:
            fig_rec = px.pie(
                df_receita, names="Categoria", values="Credito",
                title=f"Distribuição de Créditos - {st.session_state.periodo}"
            )
            st.plotly_chart(fig_rec, use_container_width=True)

    st.markdown("---")
    st.subheader("📊 Médias do Período")

    # 🔹 Definir número de meses para média
    n_meses = df_filtrado["Mes"].nunique() if periodo == "Todos" else 1

    # 🔹 MÉDIAS DE RECEITA
    receita_filtrada = df_filtrado[df_filtrado["Categoria"].str.contains("Receita", na=False)]
    media_rec_total = receita_filtrada["Credito"].sum() / n_meses if not receita_filtrada.empty else 0

    taxa_cond_filtrada = df_filtrado[df_filtrado["ContaNome"]=="Taxa de Condominio"]
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

    # 🔹 MÉDIAS DE DESPESA
    despesa_filtrada = df_filtrado[df_filtrado["Categoria"].str.contains("Despesa", na=False)]
    media_desp_total = despesa_filtrada["Debito"].sum() / n_meses if not despesa_filtrada.empty else 0

    desp_dp_filtrada = df_filtrado[df_filtrado["Categoria"]=="Despesa_DP"]
    media_desp_dp = desp_dp_filtrada["Debito"].sum() / n_meses if not desp_dp_filtrada.empty else 0

    outras_desp_filtrada = df_filtrado[df_filtrado["Categoria"].isin(["Despesa_Cond","Despesa_Imobilizado","Despesa_Tributaria"])]
    media_desp_outras = outras_desp_filtrada["Debito"].sum() / n_meses if not outras_desp_filtrada.empty else 0

    # 🔹 Exibição em colunas
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Média Total Receita", f"R$ {media_rec_total:,.2f}")
    col2.metric("💰 Média Taxa de Condomínio", f"R$ {media_rec_taxa_cond:,.2f}")
    col3.metric("💰 Outras Receitas", f"R$ {media_rec_taxa_acordo:,.2f}")

    col4, col5, col6 = st.columns(3)
    col4.metric("📉 Média Total Despesa", f"R$ {media_desp_total:,.2f}")
    col5.metric("📉 Média Despesa DP", f"R$ {media_desp_dp:,.2f}")
    col6.metric("📉 Outras Despesas", f"R$ {media_desp_outras:,.2f}")




# ===============================
# Página 2: Análise Contábil
# ===============================
if pagina == "Análise Contábil":
    st.title("📊 Análise Contábil do Condomínio")

    # Criar coluna com classificação analítica
    df["Classificacao_Analise"] = df["ContaNome"].map(mapa_analise)
    
    # Define o valor do caixa
    total_disponivel = 108_838.91  # saldo em banco


    # -------------------------------
    # Cálculos Consolidados
    # -------------------------------

    obrigações_cp = df.loc[df["Classificacao_Analise"]=="Obrigacao_CP", "Debito"].sum()
    despesas_fixas = df.loc[df["Classificacao_Analise"]=="Despesa_Fixa", "Debito"].sum()
    despesas_variaveis = df.loc[df["Classificacao_Analise"]=="Despesa_Variavel", "Debito"].sum()
    custo_operacional_mensal = despesas_fixas + despesas_variaveis
    media_diaria_despesas = custo_operacional_mensal / 30

    liquidez_corrente = total_disponivel / obrigações_cp
    liquidez_liquida = total_disponivel - obrigações_cp
    dias_de_caixa = total_disponivel / media_diaria_despesas


    # -------------------------------
    # Exibição de métricas
    # -------------------------------
    col1, col2 = st.columns(2)
    col1.metric("💰 Liquidez Corrente", f"{liquidez_corrente:.2f}")
    col1.metric("📉 Liquidez Líquida", f"R$ {liquidez_liquida:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    col2.metric("📆 Dias de Caixa", f"{dias_de_caixa:.0f} dias")
    col2.metric("🏷️ Custo Operacional Mensal", f"R$ {custo_operacional_mensal:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))


    # -------------------------------
    # Preparar dados por mês
    # -------------------------------
    # Agrupar por mês (mantém Period para cálculos)
    df["MesAno"] = df["Data"].dt.to_period("M")

    df_despesas_mensal = df.groupby("MesAno").apply(
        lambda x: pd.Series({
            "Despesas_Fixas": x.loc[x["Classificacao_Analise"]=="Despesa_Fixa", "Debito"].sum(),
            "Despesas_Variaveis": x.loc[x["Classificacao_Analise"]=="Despesa_Variavel", "Debito"].sum(),
            "Obrigações_CP": x.loc[x["Classificacao_Analise"]=="Obrigacao_CP", "Debito"].sum()
        })
    ).reset_index()

    # Coluna para exibir nos gráficos
    df_despesas_mensal["MesAno_str"] = df_despesas_mensal["MesAno"].astype(str)


    df_despesas_mensal["Total_Disponivel"] = total_disponivel
    df_despesas_mensal["Liquidez_Corrente"] = df_despesas_mensal["Total_Disponivel"] / df_despesas_mensal["Obrigações_CP"].replace(0,np.nan)
    df_despesas_mensal["Liquidez_Liquida"] = df_despesas_mensal["Total_Disponivel"] - df_despesas_mensal["Obrigações_CP"]
    df_despesas_mensal["Custo_Operacional"] = df_despesas_mensal["Despesas_Fixas"] + df_despesas_mensal["Despesas_Variaveis"]
    df_despesas_mensal["Dias_de_Caixa"] = df_despesas_mensal["Total_Disponivel"] / (df_despesas_mensal["Custo_Operacional"] / 30).replace(0,np.nan)

    # -------------------------------
    # Evolução Mensal de Liquidez e Custo
    # -------------------------------
    fig1 = px.line(
        df_despesas_mensal,
        x="MesAno_str",
        y=["Liquidez_Corrente", "Custo_Operacional"],
        labels={"value":"R$", "MesAno":"Mês"},
        title="Evolução Mensal de Liquidez e Custo Operacional"
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("""
    **Análise:** 
    """)

    # -------------------------------
    # Disponível vs Obrigações
    # -------------------------------
    fig2 = px.bar(
        df_despesas_mensal,
        x="MesAno_str",
        y=["Total_Disponivel","Obrigações_CP"],
        barmode="group",
        labels={"value":"R$", "MesAno":"Mês"},
        title="Disponível x Obrigações de Curto Prazo"
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("""
    **Análise:** 
    """)

    # -------------------------------
    # Composição de despesas do último mês (Top 5 + Outros)
    # -------------------------------
    ult = df_despesas_mensal.iloc[-1]
    df_ult = df[df["MesAno"] == ult["MesAno"]]
    df_despesa = df_ult[df_ult["Classificacao_Analise"].str.contains("Despesa", na=False)].groupby("ContaNome")[["Debito"]].sum().reset_index()
    df_despesa = df_despesa.sort_values("Debito", ascending=False)

    top_n = 5
    df_top = df_despesa.head(top_n)
    df_outros = df_despesa.tail(len(df_despesa) - top_n)
    if not df_outros.empty:
        df_outros_sum = pd.DataFrame({"ContaNome":["Outros"], "Debito":[df_outros["Debito"].sum()]})
        df_despesa_final = pd.concat([df_top, df_outros_sum], ignore_index=True)
    else:
        df_despesa_final = df_top

    fig3 = px.pie(
        df_despesa_final,
        names="ContaNome",
        values="Debito",
        title=f"Distribuição de Despesas - {ult['MesAno']}",
        hole=0.3,
        color_discrete_sequence=px.colors.sequential.Reds
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("""
    **Análise:** 
    """)

# ===============================
# Página 3: Bases
# ===============================
if pagina == "Bases":
    st.subheader("📄 Base Filtrada")
    st.dataframe(df_filtrado)

    st.subheader("📄 Consolidação por Categoria")
    st.dataframe(cat_summary_filtrado)

    st.subheader("📄 Consolidação por Categoria e Conta")
    st.dataframe(conta_summary_filtrado)

    st.subheader("📄 Percentual de cada Conta na Categoria")
    st.dataframe(percentual_categoria_filtrado)

