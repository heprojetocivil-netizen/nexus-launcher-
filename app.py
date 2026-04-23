import streamlit as st
from groq import Groq

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="NEXUS LAUNCER", layout="centered")

# --- ESTILO VISUAL ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { display: none; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3.5em; background-color: #00BFFF !important; color: white !important; font-weight: bold; border: none; }
    .footer { text-align: center; padding: 25px; color: #666; font-size: 0.9em; border-top: 1px solid #eee; margin-top: 50px; }
    .caixa-saida { background-color: #F1F5F9; padding: 20px; border-radius: 10px; border-left: 5px solid #00BFFF; margin-bottom: 20px; white-space: pre-wrap; color: #1E293B; }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO DE ESTADOS ---
if 'etapa' not in st.session_state: st.session_state.etapa = "Login"
if 'dados' not in st.session_state: st.session_state.dados = {}
if 'projetos' not in st.session_state: st.session_state.projetos = {}
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

# --- FUNÇÃO DO MOTOR DE IA ---
def chamar_nexus_ia(prompt, key):
    try:
        client = Groq(api_key=key)
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Você é o LaunchBot. Personalize os roteiros mantendo o tamanho e teor original, sem simplificar. Para os vídeos, forneça instruções detalhadas de imagens/cenas para cada trecho, garantindo que combine com o nicho do usuário."}, 
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile"
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Erro na Chave ou Conexão: {e}"

# --- FLUXO DO SISTEMA ---

# 1. TELA DE LOGIN (ACESSO PELA API KEY)
if st.session_state.etapa == "Login":
    st.title("NEXUS LAUNCER")
    st.subheader("USO RESTRITO À ASSOCIADOS QUIZ MAIS PRÊMIOS")
    nome_usuario = st.text_input("Nome")
    chave_api = st.text_input("Chave (API Key da Groq)", type="password")
    
    if st.button("ENTRAR"):
        if nome_usuario and chave_api.startswith("gsk_"):
            st.session_state.usuario = nome_usuario
            st.session_state.api_key = chave_api
            st.session_state.etapa = "Formulario"
            st.rerun()
        else:
            st.error("Por favor, insira seu nome e uma Chave API válida (começando com gsk_).")

# 2. PREENCHA FORMULÁRIO
elif st.session_state.etapa == "Formulario":
    st.title("PREENCHA FORMULÁRIO")
    nicho = st.text_input("Nicho")
    nome_ebook = st.text_input("Nome do e-book")
    dor = st.text_input("Qual dor ele resolve")
    preco = st.text_input("Preço")
    
    if st.button("AVANÇAR"):
        st.session_state.dados = {"nicho": nicho, "nome_ebook": nome_ebook, "dor": dor, "preco": preco}
        st.session_state.etapa = "Ebook"
        st.rerun()

# 3. E-BOOK PROFISSIONAL
elif st.session_state.etapa == "Ebook":
    st.title("E-BOOK PROFISSIONAL")
    if st.button("GERAR CONTEUDO – 60 CARTÕES"):
        with st.spinner("Gerando conteúdo do e-book..."):
            prompt = f"Gere 60 cartões de conteúdo para o e-book '{st.session_state.dados['nome_ebook']}' focado no nicho {st.session_state.dados['nicho']} e resolvendo a dor: {st.session_state.dados['dor']}."
            st.session_state.dados['ebook_txt'] = chamar_nexus_ia(prompt, st.session_state.api_key)
    
    if 'ebook_txt' in st.session_state.dados:
        st.markdown(f"<div class='caixa-saida'>{st.session_state.dados['ebook_txt']}</div>", unsafe_allow_html=True)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "VSL_Anuncio"
            st.rerun()

# 4. VSL DO ANÚNCIO
elif st.session_state.etapa == "VSL_Anuncio":
    st.title("🎬 1. VSL DO ANÚNCIO")
    if st.button("GERAR ROTEIRO"):
        with st.spinner("Personalizando script e imagens..."):
            prompt = f"""Personalize este roteiro para o nicho {st.session_state.dados['nicho']} sem simplificar. Adicione orientações de imagens/cenas para cada bloco de texto:
            'Se você quer [RESULTADO], mas sente que está perdido… provavelmente não é falta de esforço. É falta de direção. A maioria das pessoas comete um erro simples… e por isso continua tentando e não sai do lugar. E o pior: nem percebem onde estão errando. Eu organizei um caminho direto pra resolver isso… e vou mostrar dentro de um grupo fechado. Sem complicação. É gratuito. Clica em SAIBA MAIS para entrar'"""
            st.session_state.dados['vsl_anuncio'] = chamar_nexus_ia(prompt, st.session_state.api_key)

    if 'vsl_anuncio' in st.session_state.dados:
        st.markdown(f"<div class='caixa-saida'>{st.session_state.dados['vsl_anuncio']}</div>", unsafe_allow_html=True)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "Landing_Page"
            st.rerun()

# 5. LANDING PAGE
elif st.session_state.etapa == "Landing_Page":
    st.title("🌐 2. LANDING PAGE")
    link_grupo = st.text_input("insira o link convite para o grupo no botão acima")
    if st.button("GERAR ROTEIRO"):
        with st.spinner("Gerando copy da página..."):
            prompt = f"""Personalize este roteiro de LP para {st.session_state.usuario} no nicho {st.session_state.dados['nicho']}:
            Headline: Um caminho simples para [RESULTADO], mesmo começando do zero.
            Texto: Eu sou {st.session_state.usuario}. Já estive exatamente onde você está… tentando várias coisas… sem resultado. Até começar a estudar e aplicar o que realmente funciona… e identificar um padrão simples que muda completamente o jogo. Depois de aplicar isso na prática… eu percebi que o problema nunca foi esforço — foi direção.
            Chamada: Se você sente que está tentando… mas não sai do lugar… provavelmente está passando por isso também. Eu criei um grupo onde vou te mostrar isso de forma direta: O erro que te mantém travado; O caminho mais simples; O que realmente funciona na prática.
            Botão: ENTRAR NO GRUPO (Link: {link_grupo})"""
            st.session_state.dados['lp_txt'] = chamar_nexus_ia(prompt, st.session_state.api_key)

    if 'lp_txt' in st.session_state.dados:
        st.markdown(f"<div class='caixa-saida'>{st.session_state.dados['lp_txt']}</div>", unsafe_allow_html=True)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "Mensagens"
            st.rerun()

# 6. MENSAGENS E VSL FINAL
elif st.session_state.etapa == "Mensagens":
    st.title("📌 3. MENSAGEM FIXA DO GRUPO")
    if st.button("GERAR MENSAGENS PARA O GRUPO"):
        with st.spinner("Criando sequência de 6 dias e VSL final..."):
            prompt = f"""Personalize sem simplificar para o nicho {st.session_state.dados['nicho']} e preço {st.session_state.dados['preco']}:
            1. DESCRIÇÃO DO GRUPO: Esse grupo é silencioso... vou mostrar um caminho direto focado em [RESULTADO].
            2. DIA 1 ao 5: Perguntas sobre direção vs esforço.
            3. DIA 6 (VSL FINAL): Roteiro sobre 'fazer da forma certa', oferta do eBook '{st.session_state.dados['nome_ebook']}' com garantia de 7 dias. 
            Adicione orientações de imagens para este VSL e gere a DESCRIÇÃO rápida com o link para a loja (desconto de 30%)."""
            st.session_state.dados['mensagens_txt'] = chamar_nexus_ia(prompt, st.session_state.api_key)

    if 'mensagens_txt' in st.session_state.dados:
        st.markdown(f"<div class='caixa-saida'>{st.session_state.dados['mensagens_txt']}</div>", unsafe_allow_html=True)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "Projeto_Final"
            st.rerun()

# 7. PROJETO FINAL E APLICAÇÃO
elif st.session_state.etapa == "Projeto_Final":
    st.title(f"🚀 PROJETO: {st.session_state.dados['nome_ebook']}")
    
    aba1, aba2, aba3, aba4, aba5 = st.tabs(["📚 E-BOOK", "🎬 VSL ANÚNCIO", "🌐 LP", "📌 MENSAGENS", "📅 APLICAÇÃO"])
    with aba1: st.write(st.session_state.dados.get('ebook_txt'))
    with aba2: st.write(st.session_state.dados.get('vsl_anuncio'))
    with aba3: st.write(st.session_state.dados.get('lp_txt'))
    with aba4: st.write(st.session_state.dados.get('mensagens_txt'))
    with aba5:
        st.markdown("""
        🚀 **Sistema de lançamento simplificado**
        
        📘 **1. Criação do produto**
        - Gere o seu eBook usando o Gamma AI
        - Cadastre o produto na plataforma Monetizze 
        - Estruture o material de forma simples e direta para venda 

        🎬 **2. VSL (Vídeo de Vendas)**
        - Crie o vídeo do anúncio e o vídeo de vendas “última mensagem” na plataforma Heygen e suba no seu canal Youtube
        - Cria a Landing Page usando o Gamma, Insira o link do grupo e transforme ela em site também na plataforma Gamma.
        - Insira o link da Monetizze na descrição do vídeo de vendas

        👥 **4. Estrutura do grupo**
        - Crie o grupo na segunda-feira 
        - Durante a semana (segunda a sexta), faça o anúncio e preencha o grupo 
        - Foque em gerar atenção e entrada de participantes até completar a audiência 

        🔥 **5. Sequência de vendas**
        - Na semana seguinte, inicie a sequência de mensagens 
        - Conduza o grupo com conteúdos estratégicos e direcionamento para o VSL “ultima mensagem” 
        - Finalize levando as pessoas para a oferta na Monetizze 
        """)

    if st.button("SALVAR PROJETO"):
        st.session_state.projetos[st.session_state.dados['nome_ebook']] = st.session_state.dados
        st.success("Projeto salvo com sucesso!")

    st.markdown("---")
    st.subheader("Meus Projetos")
    for proj in list(st.session_state.projetos.keys()):
        col1, col2 = st.columns([0.8, 0.2])
        if col1.button(f"📂 Abrir {proj}"):
            st.session_state.dados = st.session_state.projetos[proj]
            st.rerun()
        if col2.button(f"🗑️", key=f"apagar_{proj}"):
            del st.session_state.projetos[proj]
            st.rerun()

    st.markdown("---")
    st.write("**Eu sou LaunchBot seu assistente virtual**")
    pergunta = st.text_input("Digite sua dúvida abaixo e tecle enter")
    if pergunta:
        st.session_state.chat_history.append(f"👤: {pergunta}")
        st.session_state.chat_history.append(f"🤖: {chamar_nexus_ia(pergunta, st.session_state.api_key)}")
    for msg in reversed(st.session_state.chat_history): st.write(msg)

st.markdown('<div class="footer">© 2026 Nexus Launcer Lançamento inteligente de produtos digitais</div>', unsafe_allow_html=True)
