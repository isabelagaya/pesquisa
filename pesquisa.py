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
            "Muito grande (acima de 5.000 ha)": 5
        }
        p9_area_cultivo = st.selectbox("9 - Qual área de cultivo da sua fazenda?", list(dict_area.keys()))
        nota_area = dict_area[p9_area_cultivo]
        
        p10_maquinas_implementos = st.selectbox("10 - Qual a disponibilidade de máquinas e implementos agrícolas na sua fazenda?", ["Insuficiente para as demandas", "Suficiente, mas defasada tecnologicamente", "Suficiente e atualizada mecanicamente", "Altamente tecnológica/conectada"])
        
        # 11. Conectividade (Variável Core IPT - Peso 0.9)
        dict_conect = {
            "Isolado - sem conexão": 1,
            "Conectado - cobertura na gestão administrativa da fazenda (sede)": 2,
            "Operacional (cobertura em pontos estratégicos e galpões)": 3,
            "Inteligente - cobertura total (sede+galpões+talhões)": 4
        }
        p11_conectividade = st.selectbox("11 - Qual tipo de conectividade em sua fazenda?", list(dict_conect.keys()))
        nota_conect = dict_conect[p11_conectividade]
        
        p12_assistencia_tecnica = st.selectbox("12 - Qual a sua atuação em relação à assistência técnica?", ["Não recebo assistência", "Recebo assistência pública (EMATER/Órgãos Estaduais)", "Recebo assistência de Cooperativas", "Contrato consultoria/assistência privada", "Recebo apoio técnico de canais integrados de indústrias"])
        p13_credito_rural = st.radio("13 - Você faz uso de crédito rural?", ["Sim, frequentemente", "Sim, ocasionalmente", "Não, utilizo recursos próprios"])
        p14_infra_transporte = st.selectbox("14 - Qual a eficiência da infraestrutura de transporte e logística para as atividades agrícolas da sua fazenda?", ["Péssima/Ruim (Gargalo crítico)", "Regular (Afeta custos mas funciona)", "Boa/Excelente (Atende perfeitamente)"])
        p15_comercializacao = st.selectbox("15 - Você comercializa os produtos da sua fazenda?", ["Venda direta para o consumidor final", "Venda para intermediários/atravessadores", "Entrega total/parcial para cooperativas", "Venda direta para agroindústrias / Tradings", "Apenas consumo próprio/Subsistência"])
        
        # Cooperativismo
        p16_cooperativa = st.radio("16 - Você está associado a alguma cooperativa agro?", ["Sim", "Não"])
        p17_nome_cooperativa = st.text_input("17 - Nome da Cooperativa ou Instituição vinculada (opcional):")
        
        p18_apoio_privado = st.radio("18 - Sua fazenda recebe algum apoio privado de empresas líderes de mercado ou instituições (máquinas, capacitação, insumos...)?", ["Sim", "Não"])
        
        p19_list = ["Participação em dias de campo/feiras", "Consultorias externas", "Troca de experiências com vizinhos", "Testes em pequenas áreas antes de expandir", "Contratação de profissionais qualificados", "Não costumo realizar ações direcionadas à inovação"]
        p19_acoes_inovar = st.multiselect("19 - Quais ações você costuma utilizar para inovar na fazenda? (Selecione todas que se aplicam)", p19_list)
        p19_string = ", ".join(p19_acoes_inovar)
        
        # 20. Familiaridade Digital (Variável Core IPT - Peso 1.0)
        dict_fam = {
            "Nenhuma Experiência / Totalmente Inexperiente": 1,
            "Muito Baixa Experiência / Pouco Familiarizado": 2,
            "Experiência Moderada / Familiarizado com o Básico": 3,
            "Boa Experiência / Confiante e Habilidoso": 4,
            "Experiência Avançada / Especialista e Proativo": 5
        }
        p20_familiaridade = st.selectbox("20 - Qual a sua familiaridade com o uso de tecnologias digitais?", list(dict_fam.keys()))
        nota_fam = dict_fam[p20_familiaridade]

        st.divider()
        st.subheader("💻 SEÇÃO 2: Tecnologias Digitais Aplicadas")
        
        p21_adota_tecnologias = st.radio("21 - Você adota tecnologias digitais em sua fazenda?", ["Sim", "Não", "Em fase de planejamento/estudo"])
        
        p22_list = ["GPS Agrícola / Piloto Automático", "Drones de imageamento ou pulverização", "Sensores de solo ou clima (Estações)", "Softwares de gestão financeira/operacional", "Aplicativos de previsão do tempo ou pragas", "Telemetria de maquinários", "Plataformas de Marketplace / Compra de insumos online", "Não utilizo nenhuma tecnologia digital"]
        p22_quais_tecnologias = st.multiselect("22 - Se sim, quais tecnologias digitais utiliza em sua fazenda?", p22_list)
        p22_string = ", ".join(p22_quais_tecnologias)
        
        p23_tipo_aplicacao = st.text_area("23 - Se sim, para qual tipo de aplicação? OPCIONAL (Ex: Monitoramento de talhões, controle de fluxo de caixa, regulagem de maquinários):")
        
        p24_list = ["Alto custo financeiro de implantação", "Falta de cobertura/sinal de internet de qualidade", "Falta de treinamento ou mão de obra qualificada", "Dificuldade de integração entre sistemas/marcas", "Falta de assistência técnica especializada próxima", "Complexidade excessiva das ferramentas disponíveis"]
        p24_principais_barreiras = st.multiselect("24 - Quais as PRINCIPAIS barreiras para a adoção de tecnologias?", p24_list)
        p24_string = ", ".join(p24_principais_barreiras)
        
        st.divider()
        st.markdown("### 👤 Dados de Contato e Encerramento")
        p25_email = st.text_input("25 - Qual seu email (para concorrer aos prêmios)? (opcional)")
        p26_nome = st.text_input("26 - Qual seu nome? (opcional)")
        p27_perfil_fazenda = st.selectbox("27 - Qual seu perfil na fazenda?", ["Proprietário / Titular", "Gerente / Administrador", "Agrônomo / Técnico", "Familiar / Herdeiro", "Colaborador operacional"])
        p28_proxima_tecnologia = st.text_input("28 - Qual a próxima tecnologia que gostaria de implantar na fazenda?")
        p29_sugestao_politica = st.text_area("29 - Sugestão para política pública ou comentários gerais:")
        
        submetido = st.form_submit_button("ENVIAR FORMULÁRIO E PROCESSAR ÍNDICE DE PRONTIDÃO")

# ==============================================================================
# 3. CORE MATEMÁTICO MANTIDO INTEGRALMENTE
# ==============================================================================
if submetido:
    if not concordou:
        st.error("❌ Você precisa aceitar o Termo de Consentimento da Seção 1 para enviar suas respostas.")
    else:
        # Ponderação Logística Padrão
        ipt_bruto = (1.4 * nota_area) + (1.0 * nota_fam) + (0.9 * nota_conect)
        ipt_percentual = ((ipt_bruto - 3.3) / 12.3) * 100
        
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

        # Montagem estruturada do payload do SQLite
        payload = (
            p1_idade, p2_sexo, p3_tamanho_familia, p4_escolaridade, p5_proxima_geracao,
            p6_localizacao, p7_cultura_principal, p8_string, p9_area_cultivo, nota_area,
            p10_maquinas_implementos, p11_conectividade, nota_conect, p12_assistencia_tecnica,
            p13_credito_rural, p14_infra_transporte, p15_comercializacao, p16_cooperativa, p17_nome_cooperativa,
            p18_apoio_privado, p19_string, p20_familiaridade, nota_fam,
            p21_adota_tecnologias, p22_string, p23_tipo_aplicacao, p24_string,
            p25_email, p26_nome if p26_nome else "Anônimo", p27_perfil_fazenda, p28_proxima_tecnologia, p29_sugestao_politica,
            round(ipt_percentual, 1), cluster_final
        )
        
        salvar_resposta(payload)
        
        with aba_form:
            st.success("🎉 Formulário enviado e computado com sucesso! Obrigado por colaborar com a pesquisa e boa sorte no sorteio do Livro Agro 4.0.")
            st.metric(label="Seu Índice de Prontidão Tecnológica (IPT)", value=f"{ipt_percentual:.1f} %")
            
            if cor_alerta == "error": st.error(f"**Posicionamento:** {cluster_final}")
            elif cor_alerta == "warning": st.warning(f"**Posicionamento:** {cluster_final}")
            else: st.success(f"**Posicionamento:** {cluster_final}")
            
            st.info(txt_recomendacao)

# ------------------------------------------------------------------------------
# 4. ABA DE AUDITORIA E EXTRAÇÃO DE BANCO DE DADOS
# ------------------------------------------------------------------------------
with aba_dados:
    st.header("Painel de Controle da Pesquisa (SQLite)")
    st.write("Registros consolidados capturados em tempo real:")
    
    conn = sqlite3.connect(DB_NAME)
    try:
        df_dados = pd.read_sql_query("SELECT * FROM respostas_survey ORDER BY timestamp DESC", conn)
        st.dataframe(df_dados)
        
        csv = df_dados.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Baixar Base de Dados Consolidada (.CSV)",
            data=csv,
            file_name="respostas_pesquisa_ipt.csv",
            mime="text/csv",
        )
    except Exception as e:
        st.write("Nenhum registro armazenado na tabela até o momento.")
    finally:
        conn.close()
