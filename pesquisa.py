import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# ==============================================================================
# 1. CONFIGURAÇÃO E CRIAÇÃO DO BANCO DE DADOS (SQLite - Expandido)
# ==============================================================================
DB_NAME = "pesquisa_rural_completa.db"

def inicializar_banco():
    """Cria a tabela com todos os novos campos da pesquisa se não existir."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS respostas_survey (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            -- Seção A: Perfil do Respondente
            idade TEXT, sexo TEXT, tamanho_familia TEXT, escolaridade TEXT,
            sucessao_geracional TEXT, perfil_fazenda TEXT, nome_respondente TEXT, email TEXT,
            -- Seção B: Caracterização da Propriedade
            nome_propriedade TEXT, estado TEXT, cultura_principal TEXT, culturas_demais TEXT,
            area_cultivo TEXT, area_cultivo_nota INTEGER,
            -- Seção C: Infraestrutura e Gestão
            maquinas_implementos TEXT, conectividade TEXT, conectividade_nota INTEGER,
            assistencia_tecnica TEXT, credito_rural TEXT, logistica_transporte TEXT,
            comercializa_produtos TEXT, associado_cooperativa TEXT, nome_cooperativa TEXT,
            apoio_privado TEXT, acoes_inovacao TEXT, familiaridade_digital TEXT, familiaridade_nota INTEGER,
            -- Seção D: Tecnologias Digitais
            adota_tecnologias TEXT, tecnologias_utilizadas TEXT, aplicacoes_tecnologia TEXT,
            barreiras_adocao TEXT, proxima_tecnologia TEXT, sugestao_politica TEXT,
            -- Núcleo Matemático
            ipt_score REAL, cluster_classificacao TEXT
        )
    """)
    conn.commit()
    conn.close()

def salvar_resposta(dados):
    """Insere todas as variáveis capturadas no formulário."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # 33 campos para inserção
    placeholders = ", ".join(["?"] * 33)
    query = f"""
        INSERT INTO respostas_survey (
            idade, sexo, tamanho_familia, escolaridade, sucessao_geracional, perfil_fazenda, 
            nome_respondente, email, nome_propriedade, estado, cultura_principal, culturas_demais, 
            area_cultivo, area_cultivo_nota, maquinas_implementos, conectividade, conectividade_nota, 
            assistencia_tecnica, credito_rural, logistica_transporte, comercializa_produtos, 
            associado_cooperativa, nome_cooperativa, apoio_privado, acoes_inovacao, familiaridade_digital, 
            familiaridade_nota, adota_tecnologias, tecnologias_utilizadas, aplicacoes_tecnologia, 
            barreiras_adocao, proxima_tecnologia, sugestao_politica, ipt_score, cluster_classificacao
        ) VALUES ({placeholders})
    """
    cursor.execute(query, dados)
    conn.commit()
    conn.close()

inicializar_banco()

# ==============================================================================
# 2. INTERFACE INTERATIVA (Streamlit)
# ==============================================================================
st.set_page_config(page_title="SDR 4.0 - Painel Digital Agrícola", page_icon="🚜", layout="wide")

st.title("Painel de Tecnologias Digitais Agrícolas")
st.subheader("Sistema de Diagnóstico de Prontidão Tecnológica Rural")

# Termo de Consentimento e Boas-vindas
with st.expander("ℹ️ Prezado(a) Produtor(a) Rural - Leia as instruções da pesquisa", expanded=True):
    st.markdown("""
    Agradecemos imensamente a sua disponibilidade em participar desta importante pesquisa, que tem como objetivo compreender os fatores que influenciam a adoção de tecnologias digitais no campo, de forma a propor instrumentos que ajudem o produtor a adquirir novas ferramentas que ajudem em seu dia a dia, trazendo mais lucro e reduzindo custos, além de colaborar com o meio ambiente.
    
    Este questionário levará apenas alguns minutos para ser preenchido (**8-10 min**). Suas respostas serão tratadas com confidencialidade e anonimato, sendo utilizadas exclusivamente para fins de pesquisa e análise estatística. Não haverá identificação individual das suas informações. Recomendamos que baseiem suas respostas em evidências (dados) e não apenas em impressões.
    
    Os participantes concorrerão a edições do **Livro Agro 4.0**, a serem sorteados ao final da pesquisa.
    
    *👉 Ao responder este questionário, você concorda voluntariamente em participar da pesquisa e estar ciente de que as respostas serão tratadas com confidencialidade e anonimato.*
    """)

aba_form, aba_dados = st.tabs(["📝 Responder Questionário & Diagnóstico", "📊 Visualizar Banco de Dados (Auditoria)"])

# ------------------------------------------------------------------------------
# ABA 1: FORMULÁRIO DIVIDIDO EM ETAPAS LOGICAS
# ------------------------------------------------------------------------------
with aba_form:
    with st.form("form_pesquisa_completo"):
        
        # --- ETAPA 1: PERFIL DO RESPONDENTE ---
        st.header("1️⃣ Perfil do Respondente")
        col1, col2 = st.columns(2)
        with col1:
            q1_idade = st.selectbox("1 - Qual sua idade? *", ["Até 34 anos", "Entre 35 a 44 anos", "Entre 45 a 54 anos", "Entre 55 a 65 anos", "Mais de 65 anos"])
            q2_sexo = st.selectbox("2 - Qual seu sexo? *", ["Masculino", "Feminino", "Outro"])
            q3_familia = st.selectbox("3 - Qual o tamanho da sua família? *", ["Família Muito Pequena (1-2 pessoas)", "Família Pequena (3 pessoas)", "Família Média (4 pessoas)", "Família Grande (5-6 pessoas)", "Família Muito Grande (7 ou + pessoas)"])
            q4_escolaridade = st.selectbox("4 - Qual seu grau de escolaridade? *", ["Não alfabetizado", "Ensino Fundamental (Completo ou Incompleto)", "Ensino Médio / Técnico", "Ensino Superior", "Pós-graduação"])
        with col2:
            q5_sucessao = st.radio("5 - Há membros da próxima geração (filhos/netos) envolvidos na gestão tecnológica da fazenda? *", ["Sim", "Não"])
            q27_perfil = st.selectbox("27 - Qual seu perfil na fazenda? *", ["Proprietário / Familiar", "Gerente de Fazenda / Administrador", "Agrônomo / Consultor Externo", "Colaborador", "Outro"])
            q26_nome = st.text_input("26 - Qual seu nome? (Opcional)", placeholder="Digite seu nome completo")
            q25_email = st.text_input("25 - Qual seu email para concorrer aos prêmios? (Opcional)", placeholder="exemplo@email.com")

        st.divider()

        # --- ETAPA 2: CARACTERIZAÇÃO DA PROPRIEDADE ---
        st.header("2️⃣ Caracterização da Fazenda")
        col3, col4 = st.columns(2)
        with col3:
            q17_nome_prop = st.text_input("Nome da Propriedade / Fazenda (Opcional)", placeholder="Ex: Fazenda Santa Maria")
            q6_estado = st.selectbox("6 - Localização da fazenda (UF): *", ["AC","AP","AM","PA","RO","RR","TO","AL","BA","CE","MA","PB","PE","PI","RN","SE","DF","GO","MT","MS","ES","MG","RJ","SP","PR","RS","SC"])
            q7_cultura = st.selectbox("7 - Qual a principal cultura da sua fazenda? *", ["Soja", "Milho", "Hortaliças", "Frutas", "Outro"])
        with col4:
            q8_demais_culturas = st.multiselect("8 - Demais culturas da sua fazenda (se houver):", ["Grandes Culturas (commodities e grãos)", "Pecuária", "Hortifruticultura", "Outro"])
            
            # Mapeamento Matemático 1 (Área de Cultivo)
            dict_area = {
                "Micro (até 50 ha)": 1,
                "Pequeno (51 a 200 ha)": 2,
                "Médio (201 a 1.000 ha)": 3,
                "Grande (1.001 a 5.000 ha)": 4,
                "Muito grande (acima de 5.000 ha)": 5
            }
            q9_area = st.selectbox("9 - Qual área de cultivo da sua fazenda? *", list(dict_area.keys()))
            nota_area = dict_area[q9_area]

        st.divider()

        # --- ETAPA 3: INFRAESTRUTURA, ASSISTÊNCIA E LOGÍSTICA ---
        st.header("3️⃣ Infraestrutura, Conectividade e Inovação")
        
        q10_maquinas = st.selectbox("10 - Qual a disponibilidade de máquinas e implementos agrícolas na sua fazenda: *", ["Não existente", "Tecnificação com uso de alguns implementos agrícolas", "Uso de mecanização (ex.: trator, colheitadeira ou plantadeira)", "Uso de sistemas de gestão da fazenda"])
        
        # Mapeamento Matemático 2 (Conectividade) ajustado para abranger as novas opções da pergunta 11 de forma correlacionada
        dict_conect = {
            "Isolado - sem conexão": 1,
            "Conectado - cobertura na gestão administrativa da fazenda (sede)": 2,
            "Inteligente - cobertura total (sede+galpões+talhões)": 4
        }
        q11_conect = st.selectbox("11 - Qual tipo de conectividade em sua fazenda? *", list(dict_conect.keys()))
        nota_conect = dict_conect[q11_conect]
        
        q12_assistencia = st.selectbox("12 - Qual a sua atuação em relação à assistência técnica? *", ["Desassistido - não recebe orientação", "Assistido básico - recebe visitas esporádicas (ex.: MAPA, EMATER, SENAR, Cooperativa)", "Especializado - recebe consultoria técnica privada", "Gestão Integrada - recebe assistência técnica e gerencial completa"])
        q13_credito = st.selectbox("13 - Você faz uso de crédito rural? *", ["Não - utiliza apenas capital próprio", "Sim - Crédito público. Ex.: Plano Safra e bancos públicos)", "Sim - Crédito privado. Ex.: opções privadas e cooperativas", "Sim - Crédito público e privado"])
        q14_logistica = st.selectbox("14 - Qual a eficiência da infraestrutura de transporte e logística para as atividades agrícolas da sua fazenda? *", ["Totalmente Inadequada", "Muito Ruim / Grandes Dificuldades", "Regular / Desafios Pontuais", "Boa / Eficiente", "Excelente / Otimizada e Estratégica"])
        
        col5, col6 = st.columns(2)
        with col5:
            q15_comercializa = st.radio("15 - Você comercializa os produtos da sua fazenda? *", ["Sim", "Não"])
            q16_cooperativa = st.radio("16 - Você está associado a alguma cooperativa agro? *", ["Sim", "Não"])
            q17_coop_nome = st.text_input("17 - Nome da Cooperativa ou Instituição vinculada (Opcional)")
        with col6:
            q18_apoio_privado = st.radio("18 - Sua fazenda recebe algum apoio privado de empresas líderes de mercado ou instituições (máquinas, capacitação, insumos...)? *", ["Não", "Sim"])
            q19_inovacao = st.multiselect("19 - Quais ações você costuma utilizar para inovar na fazenda? *", ["Participação em evento, feiras e dias de campo", "Interação com universidades e centros de pesquisa", "Contratação de consultoria de mercado", "Interação com startups (\"Agritechs\")", "Apoio de EMBRAPA, CNA, EMATER, OCB ou demais hubs de inovação agro", "Experimentos próprios / Testes internos na fazenda", "Não realizo ações de inovação", "Outro"])

        # Mapeamento Matemático 3 (Familiaridade Digital)
        dict_fam = {
            "Nenhuma Experiência / Totalmente Inexperiente": 1,
            "Muito Baixa Experiência / Pouco Familiarizado": 2,
            "Experiência Moderada / Familiarizado com o Básico": 3,
            "Boa Experiência / Confiante e Habilidoso": 4,
            "Experiência Avançada / Especialista e Proativo": 5
        }
        q20_familiaridade = st.selectbox("20 - Qual a sua familiaridade com o uso de tecnologias digitais? *", list(dict_fam.keys()))
        nota_fam = dict_fam[q20_familiaridade]

        st.divider()

        # --- ETAPA 4: TECNOLOGIAS DIGITAIS E BARREIRAS ---
        st.header("4️⃣ Aplicação de Tecnologias Digitais em sua Fazenda")
        
        q21_adota = st.radio("21 - Você adota tecnologias digitais em sua fazenda? *", ["Sim", "Não", "Não conheço"])
        q22_quais_tech = st.multiselect("22 - Se sim, quais tecnologias digitais utiliza em sua fazenda? *", ["Sensores / Câmeras / IOT", "Drones / Satélite", "Robôs", "Inteligência artificial", "Sistemas de análise de dados e gestão", "Marketplaces e comercialização digital (compra/venda)", "Telemetria e piloto automático", "Sistemas de integração com a cadeia produtiva", "Blockchain/rastreabilidade", "Não adoto", "Outro"])
        q23_aplicacao = st.multiselect("23 - Se sim, para qual tipo de aplicação? (Opcional)", ["Eficiência de insumos (ex.: taxa variável)", "Gestão hídrica (ex.: irrigação inteligente)", "Manutenção e operação de máquinas", "Gestão da produção (clima, solo, planta, safra, praga)", "Gestão logística", "Gestão de energia", "Integração com a cadeia produtiva"])
        q24_barreiras = st.multiselect("24 - Quais as PRINCIPAIS barreiras para a adoção de tecnologias? *", ["Preço para a adoção, installation e manutenção", "Dificuldade de entender os ganhos com a tecnologia", "Dificuldade de escalar a solução para toda fazenda", "Falta de pessoal treinado na fazenda para operar a ferramenta", "Risco de resultados negativos", "Risco de perda de mão de obra da fazenda", "Falta de segurança e privacidade de dados", "Falta de conectividade adequada", "Dificuldade de integração entre diferentes softwares e máquinas (falta de compatibilidade)", "Outro"])
        
        q28_proxima = st.text_area("28 - Qual a próxima tecnologia que gostaria de implantar na fazenda?")
        q29_sugestao = st.text_area("29 - Sugestão para política pública ou comentários gerais:")

        # Botão unificado para processar tudo
        submetido = st.form_submit_button("💥 SUBMETER RESPOSTAS & CALCULAR IPT")

    # ==============================================================================
    # 3. NÚCLEO MATEMÁTICO: CÁLCULO E PERSISTÊNCIA (SESSION STATE)
    # ==============================================================================
    if submetido:
        # Execução da fórmula ponderada baseada no modelo original
        ipt_bruto = (1.4 * nota_area) + (1.0 * nota_fam) + (0.9 * nota_conect)
        
        # Normalização Min-Max exata para a escala percentual de 0 a 100%
        # Mínimo: (1.4*1)+(1.0*1)+(0.9*1) = 3.3 | Máximo: (1.4*5)+(1.0*5)+(0.9*4) = 15.6 | Delta = 12.3
        ipt_percentual = ((ipt_bruto - 3.3) / 12.3) * 100
        
        if ipt_percentual < 40.0:
            cluster_final = "Cluster 1: Prontidão Tecnológica Baixa (Exclusão)"
            cor_alerta = "error"
            txt_recomendacao = "**Ação Recomendada:** Sua propriedade enfrenta gargalos severos de infraestrutura básica ou familiaridade. Recomenda-se focar em programas de alfabetização digital básica e estender o sinal de internet de pontos fixos em direção às áreas operacionais da fazenda."
        elif ipt_percentual < 70.0:
            cluster_final = "Cluster 2: Prontidão Tecnológica Média (Transição)"
            cor_alerta = "warning"
            txt_recomendacao = "**Ação Recomendada:** Sua propriedade está na vanguarda da transição! Você já possui conectividade operacional e boa familiaridade. O próximo passo é buscar soluções integradas (Crédito Coletivo 4.0) e investir em redes de sensores de campo (Última Milha Rural) para cobrir a área de cultivo de forma contínua."
        else:
            cluster_final = "Cluster 3: Prontidão Tecnológica Alta (Fronteira)"
            cor_alerta = "success"
            txt_recomendacao = "**Ação Recomendada:** Excelente! Sua fazenda encontra-se na Fronteira Tecnológica 4.0. O foco deve estar em automação profunda de processos, inteligência de dados em tempo real e compartilhamento de melhores práticas com a cadeia produtiva local."

        # Preparação das listas/multiselects estruturadas como string para salvar no banco de dados SQLite
        culturas_str = ", ".join(q8_demais_culturas) if q8_demais_culturas else ""
        inovacao_str = ", ".join(q19_inovacao) if q19_inovacao else ""
        tech_str = ", ".join(q22_quais_tech) if q22_quais_tech else ""
        aplicacao_str = ", ".join(q23_aplicacao) if q23_aplicacao else ""
        barreiras_str = ", ".join(q24_barreiras) if q24_barreiras else ""

        # Montagem estruturada do payload do SQLite
        payload = (
            q1_idade, q2_sexo, q3_familia, q4_escolaridade, q5_sucessao, q27_perfil, q26_nome, q25_email,
            q17_nome_prop, q6_estado, q7_cultura, culturas_str, q9_area, nota_area,
            q10_maquinas, q11_conect, nota_conect, q12_assistencia, q13_credito, q14_logistica,
            q15_comercializa, q16_cooperativa, q17_coop_nome, q18_apoio_privado, inovacao_str,
            q20_familiaridade, nota_fam, q21_adota, tech_str, aplicacao_str, barreiras_str,
            q28_proxima, q29_sugestao, round(ipt_percentual, 1), cluster_final
        )
        
        salvar_resposta(payload)
        
        # Guarda o resultado estruturado em Session State para evitar perdas em ciclos de re-renderizações
        st.session_state['resultado_diagnostico'] = {
            'score': ipt_percentual,
            'cluster': cluster_final,
            'cor': cor_alerta,
            'rec': txt_recomendacao
        }
        st.success("🎉 Diagnóstico e respostas salvas com absoluto sucesso!")

    # Seção visual de exibição dinâmica do relatório técnico gerado
    if 'resultado_diagnostico' in st.session_state:
        st.markdown("---")
        res = st.session_state['resultado_diagnostico']
        st.header("📊 Relatório de Diagnóstico Tecnológico")
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric(label="Seu Índice de Prontidão Tecnológica (IPT)", value=f"{res['score']:.1f} %")
        with col_m2:
            if res['cor'] == "error": st.error(f"📍 **Posicionamento:** {res['cluster']}")
            elif res['cor'] == "warning": st.warning(f"📍 **Posicionamento:** {res['cluster']}")
            else: st.success(f"📍 **Posicionamento:** {res['cluster']}")
            
        st.info(res['rec'])

# ------------------------------------------------------------------------------
# ABA 2: PAINEL ADMINISTRATIVO DO BANCO DE DADOS (E EXTRAÇÃO CSV)
# ------------------------------------------------------------------------------
with aba_dados:
    st.header("📋 Painel Consolidador do Banco de Dados Livre (SQLite)")
    st.write("Abaixo estão listadas todas as informações e métricas estatísticas consolidadas capturadas em tempo real:")
    
    conn = sqlite3.connect(DB_NAME)
    try:
        df_dados = pd.read_sql_query("SELECT * FROM respostas_survey ORDER BY timestamp DESC", conn)
        st.dataframe(df_dados, use_container_width=True)
        
        # Download para auditorias no Excel, PowerBI ou SPSS
        csv = df_dados.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Baixar Base Completa de Respostas (.CSV)",
            data=csv,
            file_name="pesquisa_digital_agricola_ipt.csv",
            mime="text/csv",
        )
    except Exception as e:
        st.error(f"Erro na leitura ou banco vazio: {e}")
    finally:
        conn.close()
