import streamlit as st
import sqlite3
import pandas as pd
import os

# ==============================================================================
# 1. CONFIGURAÇÃO E CRIAÇÃO DO BANCO DE DADOS (SQLite - Carga Completa)
# ==============================================================================
DB_NAME = "pesquisa_rural.db"

def inicializar_banco():
    """Cria a tabela no banco com todas as 29 variáveis do mapeamento oficial."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS respostas_survey (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            -- Seção 1: Perfil e Condicionantes
            p1_idade TEXT,
            p2_sexo TEXT,
            p3_tamanho_familia TEXT,
            p4_escolaridade TEXT,
            p5_proxima_geracao TEXT,
            p6_localizacao TEXT,
            p7_cultura_principal TEXT,
            p8_demais_culturas TEXT,
            p9_area_cultivo TEXT,
            p9_area_cultivo_nota INTEGER,
            p10_maquinas_implementos TEXT,
            p11_conectividade TEXT,
            p11_conectividade_nota INTEGER,
            p12_assistencia_tecnica TEXT,
            p13_credito_rural TEXT,
            p14_infra_transporte TEXT,
            p15_comercializacao TEXT,
            p16_cooperativa TEXT,
            p17_nome_cooperativa TEXT,
            p18_apoio_privado TEXT,
            p19_acoes_inovar TEXT,
            p20_familiaridade TEXT,
            p20_familiaridade_nota INTEGER,
            -- Seção 2: Tecnologias Digitais
            p21_adota_tecnologias TEXT,
            p22_quais_tecnologias TEXT,
            p23_tipo_aplicacao TEXT,
            p24_principais_barreiras TEXT,
            p25_email TEXT,
            p26_nome TEXT,
            p27_perfil_fazenda TEXT,
            p28_proxima_tecnologia TEXT,
            p29_sugestao_politica TEXT,
            -- Outputs do Modelo
            ipt_score REAL,
            cluster_classificacao TEXT
        )
    """)
    conn.commit()
    conn.close()

def salvar_resposta(dados):
    """Insere o payload completo contendo as 29 respostas + métricas do IPT."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    query = """
        INSERT INTO respostas_survey (
            p1_idade, p2_sexo, p3_tamanho_familia, p4_escolaridade, p5_proxima_geracao,
            p6_localizacao, p7_cultura_principal, p8_demais_culturas, p9_area_cultivo, p9_area_cultivo_nota,
            p10_maquinas_implementos, p11_conectividade, p11_conectividade_nota, p12_assistencia_tecnica,
            p13_credito_rural, p14_infra_transporte, p15_comercializacao, p16_cooperativa, p17_nome_cooperativa,
            p18_apoio_privado, p19_acoes_inovar, p20_familiaridade, p20_familiaridade_nota,
            p21_adota_tecnologias, p22_quais_tecnologias, p23_tipo_aplicacao, p24_principais_barreiras,
            p25_email, p26_nome, p27_perfil_fazenda, p28_proxima_tecnologia, p29_sugestao_politica,
            ipt_score, cluster_classificacao
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(query, dados)
    conn.commit()
    conn.close()

inicializar_banco()

# ==============================================================================
# 2. INTERFACE E DESIGN (Streamlit)
# ==============================================================================
st.set_page_config(page_title="SDR 4.0 - Diagnóstico Rural", page_icon="🚜", layout="centered")

st.title("🚜 Painel de Tecnologias Digitais Agrícola")

# Texto institucional do cabeçalho
st.markdown("""
**Prezado(a) Produtor(a) Rural,**

Agradecemos imensamente a sua disponibilidade em participar desta importante pesquisa, que tem como objetivo compreender os fatores que influenciam a adoção de tecnologias digitais no campo, de forma a propor instrumentos que ajudem o produtor a adquirir novas ferramentas que ajudem em seu dia a dia, trazendo mais lucro e reduzindo custos, além de colaborar com o meio ambiente.

Este questionário levará apenas alguns minutos para ser preenchido (8-10 min). Suas respostas serão tratadas com confidencialidade e anonimato, sendo utilizadas exclusivamente para fins de pesquisa e análise estatística. Não haverá identificação individual das suas informações. Recomendamos que baseiem suas respostas em evidências (dados) e não apenas em impressões.

🎁 *Os participantes concorrerão a edições do Livro Agro 4.0, a serem sorteados ao final da pesquisa.*
""")

# Abas de navegação
aba_form, aba_dados = st.tabs(["📋 Responder Questionário", "📊 Painel de Dados Coletados"])

with aba_form:
    with st.form("form_completo"):
        
        # Termo de consentimento obrigatório
        st.info("⚠️ **Termo de Consentimento:** Ao responder este questionário, você concorda voluntariamente em participar da pesquisa e está ciente de que as respostas serão tratadas com confidencialidade e anonimato.")
        concordou = st.checkbox("Li e concordo com os termos da pesquisa.", value=False)
        
        st.subheader("📋 SEÇÃO 1: Caracterização do Produtor e da Propriedade")
        
        p1_idade = st.selectbox("1 - Qual sua idade?", ["Até 25 anos", "26 a 35 anos", "36 a 45 anos", "46 a 55 anos", "56 a 65 anos", "Acima de 65 anos"])
        p2_sexo = st.radio("2 - Qual seu sexo?", ["Masculino", "Feminino", "Prefiro não responder"])
        p3_tamanho_familia = st.selectbox("3 - Qual o tamanho da sua família (pessoas que residem ou dependem da propriedade)?", ["1 a 2 pessoas", "3 a 4 pessoas", "5 a 6 pessoas", "Mais de 6 pessoas"])
        
        p4_escolaridade = st.selectbox(
            "4 - Qual seu grau de escolaridade?",
            ["Ensino Fundamental", "Ensino Médio", "Ensino Técnico", "Ensino Superior / Graduação", "Pós-Graduação (Especialização/Mestrado/Doutorado)"]
        )
        
        p5_proxima_geracao = st.radio("5 - Há membros da próxima geração (filhos/netos) envolvidos na gestão tecnológica da fazenda?", ["Sim", "Não", "Não se aplica / Não tenho herdeiros"])
        p6_localizacao = st.text_input("6 - Localização da fazenda (Município / UF):", placeholder="Ex: Rio Verde / GO")
        
        # Culturas
        p7_cultura_principal = st.text_input("7 - Qual a principal cultura da sua fazenda?", placeholder="Ex: Soja, Café, Uva de Vinho, etc.")
        p8_demais_culturas = st.text_input("8 - Demais culturas da sua fazenda (se houver, separe por vírgula):", placeholder="Ex: Milho, Sorgo, Caprino")

        st.divider()
        st.markdown("### 🧮 Variáveis de Impacto no IPT")
        
        # 9. Área de Cultivo (Variável Core IPT - Peso 1.4)
        dict_area = {
            "Micro (até 50 ha)": 1,
            "Pequeno (51 a 200 ha)": 2,
            "Médio (201 a 1.000 ha)": 3,
            "Grande (1.001 a 5.000 ha)": 4,
            "Muito grande (acima de 5
