import streamlit as st
import sqlite3
import pandas as pd
import os

# ==============================================================================
# 1. CONFIGURAÇÃO E CRIAÇÃO DO BANCO DE DADOS (SQLite - Expandido)
# ==============================================================================
DB_NAME = "pesquisa_rural.db"

def inicializar_banco():
    """Cria a tabela no banco de dados com as perguntas adicionais se não existir."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS respostas_survey (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            nome_propriedade TEXT,
            estado TEXT,
            escolaridade TEXT,
            atividade_principal TEXT,
            area_cultivo TEXT,
            area_cultivo_nota INTEGER,
            conectividade TEXT,
            conectividade_nota INTEGER,
            familiaridade_digital TEXT,
            familiaridade_nota INTEGER,
            cultura_dados TEXT,
            desafios_tecnologicos TEXT,
            ipt_score REAL,
            cluster_classificacao TEXT
        )
    """)
    conn.commit()
    conn.close()

def salvar_resposta(dados):
    """Insere a linha completa de respostas capturadas no formulário."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO respostas_survey (
            nome_propriedade, estado, escolaridade, atividade_principal,
            area_cultivo, area_cultivo_nota, conectividade, conectividade_nota, 
            familiaridade_digital, familiaridade_nota, cultura_dados, desafios_tecnologicos,
            ipt_score, cluster_classificacao
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, dados)
    conn.commit()
    conn.close()

# Inicializa o banco de dados na primeira execução
inicializar_banco()

# ==============================================================================
# 2. INTERFACE E DESIGN DA TELA DO SOFTWARE (Streamlit)
# ==============================================================================
st.set_page_config(page_title="SDR 4.0 - Diagnóstico Rural", page_icon="🚜", layout="centered")

st.title("🚜 Sistema de Diagnóstico de Prontidão Tecnológica Rural")
st.markdown("""
Este software avalia a maturidade e a capacidade de absorção tecnológica da sua propriedade rural baseado no **Índice de Prontidão Tecnológica (IPT)**, utilizando um modelo preditivo calibrado por regressão logística.
""")

# Abas de navegação internas
aba_form, aba_dados = st.tabs(["📋 Responder Diagnóstico", "📊 Visualizar Banco de Dados (Livre)"])

# ------------------------------------------------------------------------------
# ABA 1: FORMULÁRIO DE PESQUISA COMPLETO
# ------------------------------------------------------------------------------
with aba_form:
    st.header("Formulário de Coleta e Avaliação")
    
    with st.form("form_pesquisa"):
        # Seção A: Identificação e Perfil do Produtor
        st.subheader("Seção A: Identificação e Perfil")
        nome_prop = st.text_input("Nome da Propriedade / Produtor (Opcional)", placeholder="Ex: Fazenda Santa Maria")
        estado_uf = st.text_input("Estado / UF", placeholder="Ex: SP")
        
        escolaridade = st.selectbox(
            "Escolaridade do Gestor / Produtor Principal:",
            [
                "Ensino Fundamental (Completo ou Incompleto)",
                "Ensino Médio (Completo ou Incompleto)",
                "Ensino Técnico",
                "Ensino Superior / Graduação",
                "Pós-Graduação (Especialização, Mestrado, Doutorado)"
            ]
        )
        
        atividade_principal = st.selectbox(
            "Qual a principal atividade econômica da propriedade?",
            [
                "Agricultura (Grãos - Soja, Milho, etc.)",
                "Pecuária de Corte",
                "Pecuária de Leite",
                "Hortifrúti / Olericultura",
                "Vitivinicultura / Fruticultura",
                "Multicultura / Mista"
            ]
        )
        
        st.divider()
        
        # Seção B: Condicionantes de Prontidão (Variáveis do Core Matemático)
        st.subheader("Seção B: Condicionantes de Prontidão (Cálculo do IPT)")
        st.caption("As respostas desta seção determinam o seu Índice de Prontidão Tecnológica.")
        
        # 1. Variável Estrutural: Área de Cultivo (Mapeada de 1 a 5)
        dict_area = {
            "Micro (até 50 ha)": 1,
            "Pequeno (51 a 200 ha)": 2,
            "Médio (201 a 1.000 ha)": 3,
            "Grande (1.001 a 5.000 ha)": 4,
            "Muito grande (acima de 5.000 ha)": 5
        }
        escolha_area = st.selectbox("1. Qual área de cultivo da sua fazenda?", list(dict_area.keys()))
        nota_area = dict_area[escolha_area]
        
        # 2. Variável Infraestrutural: Conectividade (Mapeada de 1 a 4)
        dict_conect = {
            "Isolado - sem conexão": 1,
            "Conectado - cobertura na gestão administrativa da fazenda (sede)": 2,
            "Operacional (cobertura em pontos estratégicos e galpões)": 3,
            "Inteligente - cobertura total (sede+galpões+talhões)": 4
        }
        escolha_conect = st.selectbox("2. Qual tipo de conectividade em sua fazenda?", list(dict_conect.keys()))
        nota_conect = dict_conect[escolha_conect]
        
        # 3. Variável Humana: Familiaridade Digital (Mapeada de 1 a 5)
        dict_fam = {
            "Nenhuma Experiência / Totalmente Inexperiente": 1,
            "Muito Baixa Experiência / Pouco Familiarizado": 2,
            "Experiência Moderada / Familiarizado com o Básico": 3,
            "Boa Experiência / Confiante e Habilidoso": 4,
            "Experiência Avançada / Especialista e Proativo": 5
        }
        escolha_fam = st.selectbox("3. Qual a sua familiaridade com o uso de tecnologias digitais?", list(dict_fam.keys()))
        nota_fam = dict_fam[escolha_fam]
        
        st.divider()
        
        # Seção C: Contexto de Gestão e Desafios (Apenas Coleta)
        st.subheader("Seção C: Cultura de Gestão e Desafios")
        st.caption("Informações adicionais para mapeamento estratégico de gargalos locais.")
        
        cultura_dados = st.radio(
            "Como a propriedade realiza o registro e análise de dados da produção atualmente?",
            [
                "Não realiza registros (Gestão visual / Caderno)",
                "Registra em planilhas básicas (Excel) de forma manual",
                "Utiliza softwares ou aplicativos dedicados de gestão rural",
                "Utiliza sistemas integrados com sensores e automação de campo"
            ]
        )
        
        desafios_tecnologicos = st.selectbox(
            "Qual o principal obstáculo para a adoção de novas tecnologias na sua visão?",
            [
                "Alto custo financeiro de implantação",
                "Falta de cobertura/sinal de internet de qualidade",
                "Falta de treinamento ou mão de obra qualificada",
                "Dificuldade de integração entre os sistemas/maquinários",
                "Falta de assistência técnica especializada próxima"
            ]
        )
        
        # Botão de envio
        submetido = st.form_submit_button("PROCESSAR DIAGNÓSTICO DIGITAL")

# ==============================================================================
# 3. NÚCLEO MATEMÁTICO: CÁLCULO DO IPT E ENQUADRAMENTO NO CLUSTER
# ==============================================================================
if submetido:
    # Fórmula ponderada original mantida estritamente intacta
    ipt_bruto = (1.4 * nota_area) + (1.0 * nota_fam) + (0.9 * nota_conect)
    
    # Normalização Min-Max para escala de 0 a 100%
    ipt_percentual = ((ipt_bruto - 3.3) / 12.3) * 100
    
    # Classificação por Linhas de Corte nos Clusters de Maturidade
    if ipt_percentual < 40.0:
        cluster_final = "Cluster 1: Prontidão Tecnológica Baixa (Exclusão)"
        cor_alerta = "error"
        txt_recomendacao = "🚨 **Ação Recomendada:** Sua propriedade enfrenta gargalos severos de infraestrutura básica ou familiaridade. Recomenda-se focar em programas de alfabetização digital básica e estender o sinal de internet de pontos fixos em direção às áreas operacionais da fazenda."
    elif ipt_percentual < 70.0:
        cluster_final = "Cluster 2: Prontidão Tecnológica Média (Transição)"
        cor_alerta = "warning"
        txt_recomendacao = "⚠️ **Ação Recomendada:** Sua propriedade está na vanguarda da transição! Você já possui conectividade operacional e boa familiaridade. O próximo passo é buscar soluções integradas (Crédito Coletivo 4.0) e investir em redes de sensores de campo (Última Milha Rural) para cobrir a área de cultivo de forma contínua."
    else:
        cluster_final = "Cluster 3: Prontidão Tecnológica Alta (Fronteira)"
        cor_alerta = "success"
        txt_recomendacao = "✅ **Ação Recomendada:** Excelente! Sua fazenda encontra-se na Fronteira Tecnológica 4.0. O foco deve estar em automação profunda de processos, inteligência de dados em tempo real e compartilhamento de melhores práticas com a cadeia produtiva local."

    # Salva todos os dados coletados (incluindo as novas colunas)
    payload = (
        nome_prop if nome_prop else "Não identificado",
        estado_uf if estado_uf else "Não especificado",
        escolaridade,
        atividade_principal,
        escolha_area, nota_area,
        escolha_conect, nota_conect,
        escolha_fam, nota_fam,
        cultura_dados,
        desafios_tecnologicos,
        round(ipt_percentual, 1),
        cluster_final
    )
    salvar_resposta(payload)
    
    # Exibição dos relatórios na tela de forma amigável
    with aba_form:
        st.success("Diagnóstico concluído e armazenado com sucesso na base de dados!")
        
        # Card de resultado do Índice
        st.metric(label="Seu Índice de Prontidão Tecnológica (IPT)", value=f"{ipt_percentual:.1f} %")
        
        # Card de enquadramento do Cluster
        if cor_alerta == "error": st.error(f"**Posicionamento:** {cluster_final}")
        elif cor_alerta == "warning": st.warning(f"**Posicionamento:** {cluster_final}")
        else: st.success(f"**Posicionamento:** {cluster_final}")
        
        st.info(txt_recomendacao)

# ------------------------------------------------------------------------------
# ABA 2: VISUALIZAÇÃO DA BASE DE DADOS EXPANDIDA
# ------------------------------------------------------------------------------
with aba_dados:
    st.header("Painel da Base de Dados Livre (SQLite)")
    st.write("Abaixo estão listadas todas as entradas capturadas pelo software em tempo real:")
    
    # Consulta os dados salvos para exibir em formato de tabela (Pandas Dataframe)
    conn = sqlite3.connect(DB_NAME)
    try:
        df_dados = pd.read_sql_query("SELECT * FROM respostas_survey ORDER BY timestamp DESC", conn)
        st.dataframe(df_dados)
        
        # Botão para baixar a planilha limpa para auditoria ou uso no Excel
        csv = df_dados.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Baixar Dados Coletados (.CSV)",
            data=csv,
            file_name="dados_coletados_ipt.csv",
            mime="text/csv",
        )
    except Exception as e:
        st.write("Nenhum registro encontrado ou erro na tabela.")
    finally:
        conn.close()
