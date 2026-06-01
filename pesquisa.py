import streamlit as st
import sqlite3
import pandas as pd
import os

# ==============================================================================
# 1. CONFIGURAÇÃO E CRIAÇÃO DO BANCO DE DADOS (SQLite)
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
            -- Outputs do Modelo Preditivo
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
# 2. INTERFACE E DESIGN DA TELA (Streamlit)
# ==============================================================================
st.set_page_config(page_title="SDR 4.0 - Diagnóstico Rural", page_icon="🚜", layout="centered")

st.title("🚜 Painel de Tecnologias Digitais Agrícola")

st.markdown("""
**Prezado(a) Produtor(a) Rural,**

Agradecemos imensamente a sua disponibilidade em participar desta importante pesquisa, que tem como objetivo compreender os fatores que influenciam a adoção de tecnologias digitais no campo, de forma a proposing instrumentos que ajudem o produtor a adquirir novas ferramentas que ajudem em seu dia a dia, trazendo mais lucro e reduzindo custos, além de colaborar com o meio ambiente.

Este questionário levará apenas alguns minutos para ser preenchido (8-10 min). Suas respostas serão tratadas com confidencialidade e anonimato, sendo utilizadas exclusivamente para fins de pesquisa e análise estatística. Não haverá identificação individual das suas informações. Recomendamos que baseiem suas respostas em evidências (dados) e não apenas em impressões.

Os participantes concorrerão a edições do Livro Agro 4.0, a serem sorteados ao final da pesquisa.

Contamos com a sua valiosa participação!
""")

# Abas de navegação
aba_form, aba_dados = st.tabs(["📋 Responder Questionário", "📊 Painel de Dados Coletados"])

with aba_form:
    with st.form("form_completo"):
        
        # Termo de consentimento obrigatório
        st.info("⚠️ **Termo de Consentimento:** Ao responder este questionário, você concorda voluntariamente em participar da pesquisa e estar ciente que as respostas serão tratadas com confidencialidade e anonimato, sendo utilizadas exclusivamente para fins de pesquisa e análise estatística.")
        concordou = st.checkbox("Li e concordo com os termos da pesquisa. *", value=False)
        
        st.subheader("📋 SEÇÃO 1: Caracterização do Produtor e da Propriedade")
        
        p1_idade = st.selectbox("1 - Qual sua idade: *", ["Até 34 anos", "Entre 35 a 44 anos", "Entre 45 a 54 anos", "Entre 55 a 65 anos", "Mais de 65 anos"])
        p2_sexo = st.radio("2 - Qual seu sexo: *", ["Feminino", "Masculino", "Outro"])
        p3_tamanho_familia = st.selectbox("3 - Qual o tamanho da sua família: *", ["Família Muito Pequena (1-2 pessoas)", "Família Pequena (3 pessoas)", "Família Média (4 pessoas)", "Família Grande (5-6 pessoas)", "Família Muito Grande (7 ou + pessoas)"])
        p4_escolaridade = st.selectbox("4 - Qual seu grau de escolaridade? *", ["Não alfabetizado", "Ensino Fundamental (Completo ou Incompleto)", "Ensino Médio / Técnico", "Ensino Superior", "Pós-graduação"])
        p5_proxima_geracao = st.radio("5 - Há membros da próxima geração (filhos/netos) envolvidos na gestão tecnológica da fazenda? *", ["Sim", "Não"])
        
        estados_br = ["AC", "AP", "AM", "PA", "RO", "RR", "TO", "AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE", "DF", "GO", "MT", "MS", "ES", "MG", "RJ", "SP", "PR", "RS", "SC"]
        p6_localizacao = st.selectbox("6 - Localização da fazenda: *", estados_br)
        
        p7_cultura_principal = st.selectbox("7 - Qual a principal cultura da sua fazenda: *", ["Soja", "Milho", "Hortaliças", "Frutas", "Outro:"])
        p7_outro = st.text_input("Se selecionou 'Outro:' na cultura principal, especifique:")
        p7_final = f"Outro: {p7_outro}" if (p7_cultura_principal == "Outro:" and p7_outro) else p7_cultura_principal

        p8_demais_culturas = st.selectbox("8 - Demais culturas da sua fazenda (se houver):", ["Nenhuma / Não se aplica", "Grandes Culturas (commodities e grãos)", "Pecuária", "Hortifruticultura", "Outro:"])
        p8_outro = st.text_input("Se selecionou 'Outro:' nas demais culturas, especifique:")
        p8_final = f"Outro: {p8_outro}" if (p8_demais_culturas == "Outro:" and p8_outro) else p8_demais_culturas

        st.divider()
        st.markdown("### 🧮 Variáveis de Impacto Direto no IPT")
        st.caption("As perguntas 9, 11 e 20 são as variáveis base que compõem o cálculo do Índice de Prontidão Tecnológica.")
        
        # 9. Área de Cultivo (Mapeada de 1 a 5 - Peso: 1.4)
        dict_area = {
            "Micro (até 50 ha)": 1,
            "Pequeno (51 a 200 ha)": 2,
            "Médio (201 a 1.000 ha)": 3,
            "Grande (1.001 a 5.000 ha)": 4,
            "Muito grande (acima de 5.000 ha)": 5
        }
        p9_area_cultivo = st.selectbox("9 - Qual área de cultivo da sua fazenda? *", list(dict_area.keys()))
        nota_area = dict_area[p9_area_cultivo]
        
        p10_maquinas_implementos = st.selectbox("10 - Qual a disponibilidade de máquinas e implementos agrícolas na sua fazenda: *", ["Não existente", "Tecnificação com uso de alguns implementos agrícolas", "Uso de mecanização (ex.: trator, colheitadeira ou plantadeira)", "Uso de sistemas de gestão da fazenda"])
        
        # 11. Conectividade (Mapeada com base nas 3 opções do questionário - Peso: 0.9)
        dict_conect = {
            "Isolado - sem conexão": 1,
            "Conectado - cobertura na gestão administrativa da fazenda (sede)": 2,
            "Inteligente - cobertura total (sede+galpões+talhões)": 4
        }
        p11_conectividade = st.selectbox("11 - Qual tipo de conectividade em sua fazenda? *", list(dict_conect.keys()))
        nota_conect = dict_conect[p11_conectividade]
        
        p12_assistencia_tecnica = st.selectbox("12 - Qual a sua atuação em relação à assistência técnica? *", ["Desassistido - não recebe orientação", "Assistido básico - recebe visitas esporádicas (ex.: MAPA, EMATER, SENAR, Cooperativa)", "Especializado - recebe consultoria técnica privada", "Gestão Integrada - recebe assistência técnica e gerencial completa"])
        p13_credito_rural = st.radio("13 - Você faz uso de crédito rural? *", ["Não - utiliza apenas capital próprio", "Sim - Crédito público. Ex.: Plano Safra e bancos públicos)", "Sim - Crédito privado. Ex.: opções privadas e cooperativas", "Sim - Crédito público e privado"])
        p14_infra_transporte = st.selectbox("14 - Qual a eficiência da infraestrutura de transporte e logística para as atividades agrícolas da sua fazenda? *", ["Totalmente Inadequada", "Muito Ruim / Grandes Dificuldades", "Regular / Desafios Pontuais", "Boa / Eficiente", "Excelente / Otimizada e Estratégica"])
        p15_comercializacao = st.radio("15 - Você comercializa os produtos da sua fazenda? *", ["Sim", "Não"])
        p16_cooperativa = st.radio("16 - Você está associado a alguma cooperativa agro? *", ["Sim", "Não"])
        p17_nome_cooperativa = st.text_input("17 - Nome da Cooperativa ou Instituição vinculada (opcional):")
        p18_apoio_privado = st.radio("18 - Sua fazenda recebe algum apoio privado de empresas líderes de mercado ou institutions (máquinas, capacitação, insumos...)? *", ["Não", "Sim"])
        
        p19_list = ["Participação em evento, feiras e dias de campo", "Interação com universidades e centros de pesquisa", "Contratação de consultoria de mercado", "Interação com startups (\"Agritechs\")", "Apoio de EMBRAPA, CNA, EMATER, OCB ou demais hubs de inovação agro", "Experimentos próprios / Testes internos na fazenda", "Não realizo ações de inovação"]
        p19_acoes_inovar = st.multiselect("19 - Quais ações você costuma utilizar para inovar na fazenda? *", p19_list)
        p19_outro = st.text_input("Se utilizou outra ação de inovação não listada (opção 'Outro:'), digite aqui:")

        # 20. Familiaridade Digital (Mapeada de 1 a 5 - Peso: 1.0)
        dict_fam = {
            "Nenhuma Experiência / Totalmente Inexperiente": 1,
            "Muito Baixa Experiência / Pouco Familiarizado": 2,
            "Experiência Moderada / Familiarizado com o Básico": 3,
            "Boa Experiência / Confiante e Habilidoso": 4,
            "Experiência Avançada / Especialista e Proativo": 5
        }
        p20_familiaridade = st.selectbox("20 - Qual a sua familiaridade com o uso de tecnologias digitais? *", list(dict_fam.keys()))
        nota_fam = dict_fam[p20_familiaridade]

        st.divider()
        st.subheader("💻 SEÇÃO 2: Tecnologias Digitais Aplicadas")
        
        p21_adota_tecnologias = st.radio("21 - Você adota tecnologias digitais em sua fazenda? *", ["Sim", "Não", "Não conheço"])
        
        p22_list = ["Sensores / Câmeras / IOT", "Drones / Satélite", "Robôs", "Inteligência artificial", "Sistemas de análise de dados e gestão", "Marketplaces e comercialização digital (compra/venda)", "Telemetria e piloto automático", "Sistemas de integração com a cadeia produtiva", "Blockchain/rastreabilidade", "Não adoto"]
        p22_quais_tecnologias = st.multiselect("22 - Se sim, quais tecnologias digitais utiliza em sua fazenda? *", p22_list)
        p22_outro = st.text_input("Se utiliza outra tecnologia não listada (opção 'Outro:'), digite aqui:")
        
        p23_list = ["Eficiência de insumos (ex.: taxa variável)", "Gestão hídrica (ex.: irrigação inteligente)", "Manutenção e operação de máquinas", "Gestão da produção (clima, solo, planta, safra, praga)", "Gestão logística", "Gestão de energia", "Integração com a cadeia produtiva"]
        p23_tipo_aplicacao = st.multiselect("23 - Se sim, para qual tipo de aplicação? OPCIONAL", p23_list)
        
        p24_list = ["Preço para a adoção, instalação e manutenção", "Dificuldade de entender os ganhos com a tecnologia", "Dificuldade de escalar a solução para toda fazenda", "Falta de pessoal treinado na fazenda para operar a ferramenta", "Risco de resultados negativos", "Risco de perda de mão de obra da fazenda", "Falta de segurança e privacidade de dados", "Falta de conectividade adequada", "Dificuldade de integração entre diferentes softwares e máquinas (falta de compatibilidade)"]
        p24_principais_barreiras = st.multiselect("24 - Quais as PRINCIPAIS barreiras para a adoção de tecnologias? *", p24_list)
        p24_outro = st.text_input("Se identificou outra barreira marcante (opção 'Outro:'), digite aqui:")
        
        st.divider()
        st.markdown("### 👤 Dados de Contato e Encerramento")
        p25_email = st.text_input("25 - Qual seu email (para concorrer aos prêmios)? (opcional)")
        p26_nome = st.text_input("26 - Qual seu nome (opcional)?")
        
        p27_perfil_fazenda = st.selectbox("27 - Qual seu perfil na fazenda? *", ["Proprietário / Familiar", "Gerente de Fazenda / Administrador", "Agrônomo / Consultor Externo", "Colaborador", "Outro:"])
        p27_outro = st.text_input("Se selecionou 'Outro:' no perfil da fazenda, especifique:")
        p27_final = f"Outro: {p27_outro}" if (p27_perfil_fazenda == "Outro:" and p27_outro) else p27_perfil_fazenda

        p28_proxima_tecnologia = st.text_input("28 - Qual a próxima tecnologia que gostaria de implantar na fazenda?")
        p29_sugestao_politica = st.text_area("29 - Sugestão para política pública ou comentário gerais:")
        
        submetido = st.form_submit_button("ENVIAR FORMULÁRIO E PROCESSAR ÍNDICE DE PRONTIDÃO")

# ==============================================================================
# 3. CORE MATEMÁTICO E PROCESSAMENTO LOGÍSTICO
# ==============================================================================
if submetido:
    if not concordou:
        st.error("❌ Você precisa aceitar o Termo de Consentimento da Seção 1 para enviar suas respostas.")
    else:
        # Tratamento e agrupamento das opções dinâmicas com campos de texto adicionais
        p19_comb = p19_acoes_inovar + ([f"Outro: {p19_outro}"] if p19_outro else [])
        p19_string = ", ".join(p19_comb) if p19_comb else ""

        p22_comb = p22_quais_tecnologias + ([f"Outro: {p22_outro}"] if p22_outro else [])
        p22_string = ", ".join(p22_comb) if p22_comb else ""

        p23_string = ", ".join(p23_tipo_aplicacao) if p23_tipo_aplicacao else ""

        p24_comb = p24_principais_barreiras + ([f"Outro: {p24_outro}"] if p24_outro else [])
        p24_string = ", ".join(p24_comb) if p24_comb else ""

        # Cálculo Ponderado do IPT (Core Baseado nas Notas 9, 20 e 11)
        # IPT_Bruto = (1.4 * Area) + (1.0 * Fam) + (0.9 * Cone)
        ipt_bruto = (1.4 * nota_area) + (1.0 * nota_fam) + (0.9 * nota_conect)
        
        # Normalização matemática de 0% a 100%
        # Mínimo possível (tudo 1) = 3.3 | Máximo possível (5, 5, 4) = 15.6 | Intervalo amplitude = 12.3
        ipt_percentual = ((ipt_bruto - 3.3) / 12.3) * 100
        
        # Classificação por réguas de corte nos Clusters estabelecidos
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

        # Estruturação estruturada do payload do banco de dados SQLite
        payload = (
            p1_idade, p2_sexo, p3_tamanho_familia, p4_escolaridade, p5_proxima_geracao,
            p6_localizacao, p7_final, p8_final, p9_area_cultivo, nota_area,
            p10_maquinas_implementos, p11_conectividade, nota_conect, p12_assistencia_tecnica,
            p13_credito_rural, p14_infra_transporte, p15_comercializacao, p16_cooperativa, p17_nome_cooperativa,
            p18_apoio_privado, p19_string, p20_familiaridade, nota_fam,
            p21_adota_tecnologias, p22_string, p23_string, p24_string,
            p25_email, p26_nome if p26_nome else "Anônimo", p27_final, p28_proxima_tecnologia, p29_sugestao_politica,
            round(ipt_percentual, 1), cluster_final
        )
        
        salvar_resposta(payload)
        
        with aba_form:
            st.success("🎉 Formulário enviado e computado com sucesso! Obrigado por colaborar com a pesquisa e boa sorte no sorteio.")
            st.metric(label="Seu Índice de Prontidão Tecnológica (IPT)", value=f"{ipt_percentual:.1f} %")
            
            if cor_alerta == "error": st.error(f"**Posicionamento:** {cluster_final}")
            elif cor_alerta == "warning": st.warning(f"**Posicionamento:** {cluster_final}")
            else: st.success(f"**Posicionamento:** {cluster_final}")
            
            st.info(txt_recomendacao)

# ------------------------------------------------------------------------------
# 4. ABA DE AUDITORIA E EXTRAÇÃO DE BANCO DE DADOS
# ------------------------------------------------------------------------------
with aba_dados:
