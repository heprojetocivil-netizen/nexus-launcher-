import streamlit as st
from groq import Groq

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="NEXUS LAUNCER", layout="wide")

# --- ESTILO CSS ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { display: none; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3.5em; background-color: #00BFFF !important; color: white !important; font-weight: bold; border: none; }
    .caixa-texto { background-color: #F8FAFC; padding: 20px; border-radius: 10px; border-left: 5px solid #00BFFF; margin-bottom: 20px; white-space: pre-wrap; color: #1E293B; font-size: 1.1em; }
    .footer { text-align: center; padding: 30px; color: #94A3B8; font-size: 0.9em; border-top: 1px solid #E2E8F0; margin-top: 50px; }
    .stExpander { border: 1px solid #E2E8F0; border-radius: 10px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO DE ESTADOS ---
if 'etapa' not in st.session_state: st.session_state.etapa = "Login"
if 'dados' not in st.session_state: st.session_state.dados = {}
if 'projetos' not in st.session_state: st.session_state.projetos = {}
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

# --- MOTOR DE IA ---
def chamar_ia(prompt, api_key):
    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Você é o LaunchBot. Siga os roteiros fornecidos FIELMENTE. Não resuma, não simplifique e não altere o tamanho do texto. Apenas personalize os campos entre colchetes para o nicho do usuário. Para vídeos, oriente detalhadamente as imagens para cada cena."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile"
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Erro: Verifique sua Chave API. ({e})"

# --- NAVEGAÇÃO GLOBAL (NOVO PROJETO / MEUS PROJETOS) ---
def barra_ferramentas():
    if st.session_state.etapa != "Login":
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("➕ INICIAR NOVO PROJETO", key="btn_novo"):
                st.session_state.dados = {}
                st.session_state.etapa = "Formulario"
                st.rerun()
        with col2:
            with st.expander("📂 MEUS PROJETOS"):
                if not st.session_state.projetos:
                    st.write("Nenhum projeto salvo.")
                for p_nome in list(st.session_state.projetos.keys()):
                    c1, c2 = st.columns([0.8, 0.2])
                    if c1.button(f"📄 {p_nome}", key=f"abrir_{p_nome}"):
                        st.session_state.dados = st.session_state.projetos[p_nome]
                        st.session_state.etapa = "Visualizacao"
                        st.rerun()
                    if c2.button("🗑️", key=f"del_{p_nome}"):
                        del st.session_state.projetos[p_nome]
                        st.rerun()

# --- TELAS DO SISTEMA ---

# 1. LOGIN
if st.session_state.etapa == "Login":
    st.title("NEXUS LAUNCER")
    st.subheader("USO RESTRITO À ASSOCIADOS QUIZ MAIS PRÊMIOS")
    st.info("Não coloque senha do site, só a chave api_key")
    nome = st.text_input("Nome")
    chave = st.text_input("Chave", type="password")
    if st.button("ENTRAR"):
        if nome and chave:
            st.session_state.usuario = nome
            st.session_state.api_key = chave
            st.session_state.etapa = "Formulario"
            st.rerun()

# 2. FORMULÁRIO
elif st.session_state.etapa == "Formulario":
    barra_ferramentas()
    st.title("PREENCHA FORMULÁRIO")
    n_nicho = st.text_input("Nicho")
    n_ebook = st.text_input("Nome do e-book")
    n_dor = st.text_input("Qual dor ele resolve")
    n_preco = st.text_input("Preço")
    if st.button("AVANÇAR"):
        st.session_state.dados = {"nicho": n_nicho, "nome_ebook": n_ebook, "dor": n_dor, "preco": n_preco}
        st.session_state.etapa = "Ebook"
        st.rerun()

# 3. E-BOOK
elif st.session_state.etapa == "Ebook":
    barra_ferramentas()
    st.title("E-BOOK PROFISSOAL")
    if st.button("GERAR CONTEUDO – 60 CARTÕES"):
        with st.spinner("Gerando conteúdo..."):
            p = f"Gere 60 cartões de conteúdo para o eBook {st.session_state.dados['nome_ebook']} no nicho {st.session_state.dados['nicho']} resolvendo a dor {st.session_state.dados['dor']}."
            st.session_state.dados['out_eb'] = chamar_ia(p, st.session_state.api_key)
    if 'out_eb' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['out_eb']}</div>", unsafe_allow_html=True)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "VSL_Anuncio"
            st.rerun()

# 4. VSL ANÚNCIO
elif st.session_state.etapa == "VSL_Anuncio":
    barra_ferramentas()
    st.title("🎬 1. VSL DO ANÚNCIO")
    if st.button("GERAR ROTEIRO"):
        with st.spinner("Personalizando..."):
            p = f"Personalize este texto sem simplificar para o nicho {st.session_state.dados['nicho']} e oriente as imagens: 'Se você quer [RESULTADO], mas sente que está perdido… provavelmente não é falta de esforço. É falta de direção. A maioria das pessoas comete um erro simples… e por isso continua tentando e não sai do lugar. E o pior: nem percebem onde estão errando. Eu organizei um caminho direto pra resolver isso… e vou mostrar dentro de um grupo fechado. Sem complicação. É gratuito. Clica em SAIBA MAIS para entrar'"
            st.session_state.dados['out_vsl_an'] = chamar_ia(p, st.session_state.api_key)
    if 'out_vsl_an' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['out_vsl_an']}</div>", unsafe_allow_html=True)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "LP"
            st.rerun()

# 5. LANDING PAGE
elif st.session_state.etapa == "LP":
    barra_ferramentas()
    st.title("🌐 2. LANDING PAGE")
    link_g = st.text_input("insira o link convite para o grupo no botão acima")
    if st.button("GERAR ROTEIRO"):
        with st.spinner("Criando parágrafos..."):
            p = f"Personalize para {st.session_state.usuario} no nicho {st.session_state.dados['nicho']} separando em parágrafos: Headline: Um caminho simples para [RESULTADO], mesmo começando do zero. Texto: Eu sou {st.session_state.usuario}. Já estive exatamente onde você está… tentando várias coisas… sem resultado. Até começar a estudar e aplicar o que realmente funciona… e identificar um padrão simples que muda completamente o jogo. Depois de aplicar isso na prática… eu percebi que o problema nunca foi esforço — foi direção. Se você sente que está tentando… mas não sai do lugar… provavelmente está passando por isso também. Eu criei um grupo onde vou te mostrar isso de forma direta: O erro que te mantém travado; O caminho mais simples; O que realmente funciona na prática. Botão: ENTRAR NO GRUPO (Link: {link_g})"
            st.session_state.dados['out_lp'] = chamar_ia(p, st.session_state.api_key)
    if 'out_lp' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['out_lp']}</div>", unsafe_allow_html=True)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "Mensagens"
            st.rerun()

# 6. MENSAGENS
elif st.session_state.etapa == "Mensagens":
    barra_ferramentas()
    st.title("📌 3. MENSAGEM FIXA DO GRUPO")
    if st.button("GERAR MENSAGENS PARA O GRUPO"):
        with st.spinner("Gerando sequência..."):
            p = f"""Personalize sem simplificar para {st.session_state.dados['nicho']} e preço {st.session_state.dados['preco']}: 
            DESCRIÇÃO DO GRUPO: Esse grupo é silencioso... caminho simples para [RESULTADO]. 
            DIA 1: Pergunta direta. 
            DIA 2: Direção errada. 
            DIA 3: Ponto simples. 
            DIA 4: Parar de perder tempo. 
            DIA 5: Amanhã mostro diferente. 
            DIA 6 VSL FINAL: Roteiro 'O que trava a maioria... fazer da forma certa'. eBook {st.session_state.dados['nome_ebook']}, garantia 7 dias. Oriente imagens para o Dia 6 e gere a descrição curta com link 30% desconto."""
            st.session_state.dados['out_msgs'] = chamar_ia(p, st.session_state.api_key)
    if 'out_msgs' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['out_msgs']}</div>", unsafe_allow_html=True)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "Visualizacao"
            st.rerun()

# 7. VISUALIZAÇÃO FINAL (ABAS FECHADAS)
elif st.session_state.etapa == "Visualizacao":
    barra_ferramentas()
    st.title(f"PROJETO: {st.session_state.dados.get('nome_ebook', 'Sem Nome')}")
    
    # Abas iniciam fechadas (expanded=False)
    with st.expander("📚 E-BOOK", expanded=False):
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('out_eb')}</div>", unsafe_allow_html=True)
    with st.expander("🎬 1. VSL DO ANÚNCIO", expanded=False):
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('out_vsl_an')}</div>", unsafe_allow_html=True)
    with st.expander("🌐 2. LANDING PAGE", expanded=False):
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('out_lp')}</div>", unsafe_allow_html=True)
    with st.expander("📌 3. MENSAGENS", expanded=False):
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('out_msgs')}</div>", unsafe_allow_html=True)
    with st.expander("📅 APLICAÇÃO", expanded=False):
        st.markdown("""
        <div class='caixa-texto'>
        🚀 Sistema de lançamento simplificado
        📘 1. Criação do produto
        - Gere o seu eBook usando o Gamma AI
        - Cadastre o produto na plataforma Monetizze 
        - Estruture o material de forma simples e direta para venda 
        🎬 2. VSL (Vídeo de Vendas)
        - Crie o vídeo do anúncio e o vídeo de vendas “última mensagem” na plataforma Heygen e suba no seu canal Youtube
        - Cria a Landing Page usando o Gamma, Insira o link do grupo e transforme ela em site também na plataforma Gamma.
        - Insira o link da Monetizze na descrição do vídeo de vendas
        👥 4. Estrutura do grupo
        - Crie o grupo na segunda-feira 
        - Durante a semana (segunda a sexta), faça o anúncio e preencha o grupo 
        - Foque em gerar atenção e entrada de participantes até completar a audiência 
        🔥 5. Sequência de vendas
        - Na semana seguinte, inicie a sequência de mensagens 
        - Conduza o grupo com conteúdos estratégicos e direcionamento para o VSL “ultima mensagem” 
        - Finalize levando as pessoas para a oferta na Monetizze 
        </div>
        """, unsafe_allow_html=True)

    if st.button("💾 SALVAR PROJETO"):
        st.session_state.projetos[st.session_state.dados['nome_ebook']] = st.session_state.dados
        st.success("Projeto salvo!")

    st.markdown("---")
    # CHAT CONTÍNUO EMBAIXO DAS ABAS
    st.subheader("💬 LaunchBot - Especialista em Lançamentos")
    st.write("Eu sou o LaunchBot, especialista em lançamentos digitais de alta conversão")
    pergunta = st.text_input("Digite a sua dúvida", key="chat_input")
    if pergunta:
        resposta = chamar_ia(pergunta, st.session_state.api_key)
        st.session_state.chat_history.append((pergunta, resposta))
    
    for q, a in reversed(st.session_state.chat_history):
        st.write(f"👤: {q}")
        st.write(f"🤖: {a}")
        st.markdown("---")

# RODAPÉ
st.markdown('<div class="footer">© 2026 Nexus Launcer Lançamento inteligente de produtos digitais</div>', unsafe_allow_html=True)
