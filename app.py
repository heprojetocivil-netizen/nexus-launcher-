import streamlit as st
from groq import Groq

# --- CONFIGURAÇÃO INICIAL ---
st.set_page_config(page_title="NEXUS LAUNCER", layout="centered")

# --- ESTILO CSS ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { display: none; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3.5em; background-color: #00BFFF !important; color: white !important; font-weight: bold; border: none; }
    .footer { text-align: center; padding: 30px; color: #888; font-size: 0.9em; border-top: 1px solid #eee; margin-top: 50px; }
    .output-box { background-color: #F8FAFC; padding: 20px; border-radius: 10px; border-left: 5px solid #00BFFF; margin-bottom: 20px; white-space: pre-wrap; }
    </style>
""", unsafe_allow_html=True)

# --- ESTADOS DA SESSÃO ---
if 'etapa' not in st.session_state: st.session_state.etapa = "Login"
if 'dados' not in st.session_state: st.session_state.dados = {}
if 'projetos' not in st.session_state: st.session_state.projetos = {}
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

# --- MOTOR DE IA ---
api_key = "SUA_CHAVE_AQUI" 

def chamar_ia(prompt):
    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            messages=[{"role": "system", "content": "Você é o LaunchBot. Personalize os roteiros fornecidos mantendo o tamanho e teor original, sem simplificar. Para vídeos, inclua orientações detalhadas de imagens e cenas personalizadas ao nicho."}, 
                      {"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile"
        )
        return response.choices[0].message.content
    except Exception as e: return f"Erro: {e}"

# --- FLUXO DO SISTEMA ---

# 1. TELA DE LOGIN
if st.session_state.etapa == "Login":
    st.title("NEXUS LAUNCER")
    st.subheader("USO RESTRITO À ASSOCIADOS QUIZ MAIS PRÊMIOS")
    nome = st.text_input("Nome")
    chave = st.text_input("Chave", type="password")
    if st.button("ENTRAR"):
        if chave == "NEXUS-PRO-2026" and nome:
            st.session_state.usuario = nome
            st.session_state.etapa = "Formulario"
            st.rerun()
        else: st.error("Chave inválida.")

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
        with st.spinner("Gerando conteúdo..."):
            p = f"Gere 60 cartões de conteúdo para o eBook '{st.session_state.dados['nome_ebook']}' no nicho {st.session_state.dados['nicho']} focado em: {st.session_state.dados['dor']}."
            st.session_state.dados['ebook_out'] = chamar_ia(p)
    if 'ebook_out' in st.session_state.dados:
        st.markdown(f"<div class='output-box'>{st.session_state.dados['ebook_out']}</div>", unsafe_allow_html=True)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "VSL_Anuncio"
            st.rerun()

# 4. VSL DO ANÚNCIO
elif st.session_state.etapa == "VSL_Anuncio":
    st.title("🎬 1. VSL DO ANÚNCIO")
    if st.button("GERAR ROTEIRO"):
        with st.spinner("Personalizando e orientando imagens..."):
            template = f"""Personalize este roteiro para o nicho {st.session_state.dados['nicho']} focado em {st.session_state.dados['dor']}. Mantenha o texto e oriente as imagens:
            'Se você quer [RESULTADO], mas sente que está perdido… provavelmente não é falta de esforço. É falta de direção. A maioria das pessoas comete um erro simples… e por isso continua tentando e não sai do lugar. E o pior: nem percebem onde estão errando. Eu organizei um caminho direto pra resolver isso… e vou mostrar dentro de um grupo fechado. Sem complicação. É gratuito. Clica em SAIBA MAIS para entrar'"""
            st.session_state.dados['vsl_an_out'] = chamar_ia(template)
    if 'vsl_an_out' in st.session_state.dados:
        st.markdown(f"<div class='output-box'>{st.session_state.dados['vsl_an_out']}</div>", unsafe_allow_html=True)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "LP"
            st.rerun()

# 5. LANDING PAGE
elif st.session_state.etapa == "LP":
    st.title("🌐 2. LANDING PAGE")
    link_grupo = st.text_input("insira o link convite para o grupo no botão acima")
    if st.button("GERAR ROTEIRO"):
        with st.spinner("Personalizando LP..."):
            template = f"""Personalize este roteiro de LP para {st.session_state.usuario} no nicho {st.session_state.dados['nicho']}:
            Headline: Um caminho simples para [RESULTADO], mesmo começando do zero.
            Corpo: Eu sou {st.session_state.usuario}. Já estive exatamente onde você está… tentando várias coisas… sem resultado. Até começar a estudar e aplicar o que realmente funciona… e identificar um padrão simples que muda completamente o jogo. Depois de aplicar isso na prática… eu percebi que o problema nunca foi esforço — foi direção.
            Se você sente que está tentando… mas não sai do lugar… provavelmente está passando por isso também. Eu criei um grupo onde vou te mostrar isso de forma direta.
            Tópicos: O erro que te mantém travado, O caminho mais simples, O que realmente funciona na prática.
            Botão: ENTRAR NO GRUPO (Link: {link_grupo})"""
            st.session_state.dados['lp_out'] = chamar_ia(template)
    if 'lp_out' in st.session_state.dados:
        st.markdown(f"<div class='output-box'>{st.session_state.dados['lp_out']}</div>", unsafe_allow_html=True)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "Mensagens"
            st.rerun()

# 6. MENSAGENS E VSL FINAL
elif st.session_state.etapa == "Mensagens":
    st.title("📌 3. MENSAGEM FIXA DO GRUPO")
    if st.button("GERAR MENSAGENS PARA O GRUPO"):
        with st.spinner("Gerando sequência completa..."):
            template = f"""Personalize sem simplificar mantendo o tamanho original para o nicho {st.session_state.dados['nicho']} e preço {st.session_state.dados['preco']}:
            1. DESCRIÇÃO DO GRUPO: Esse grupo é silencioso... vou mostrar um caminho para [RESULTADO].
            2. DIA 1 ao 5: Siga o roteiro de perguntas diretas, direção errada, ponto simples.
            3. DIA 6 - VSL FINAL: Use o roteiro 'O que trava a maioria não é falta de esforço... é direção'. Inclua garantia de 7 dias, oferta do eBook e link da loja com 30% desconto.
            ORIENTE AS IMAGENS para este VSL e gere abaixo a DESCRIÇÃO rápida com o link."""
            st.session_state.dados['msg_out'] = chamar_ia(template)
    if 'msg_out' in st.session_state.dados:
        st.markdown(f"<div class='output-box'>{st.session_state.dados['msg_out']}</div>", unsafe_allow_html=True)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "Visualizacao"
            st.rerun()

# 7. PROJETO FINAL E SALVAR
elif st.session_state.etapa == "Visualizacao":
    st.title(f"🚀 PROJETO: {st.session_state.dados['nome_ebook']}")
    
    t1, t2, t3, t4, t5 = st.tabs(["📚 E-BOOK", "🎬 VSL ANÚNCIO", "🌐 LP", "📌 MENSAGENS", "📅 APLICAÇÃO"])
    with t1: st.write(st.session_state.dados.get('ebook_out'))
    with t2: st.write(st.session_state.dados.get('vsl_an_out'))
    with t3: st.write(st.session_state.dados.get('lp_out'))
    with t4: st.write(st.session_state.dados.get('msg_out'))
    with t5:
        st.markdown("""
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
        st.success("Projeto salvo!")

    st.markdown("---")
    st.subheader("Meus Projetos")
    for p_name in list(st.session_state.projetos.keys()):
        c1, c2 = st.columns([0.8, 0.2])
        if c1.button(f"📂 Abrir {p_name}"):
            st.session_state.dados = st.session_state.projetos[p_name]
            st.rerun()
        if c2.button(f"🗑️", key=f"del_{p_name}"):
            del st.session_state.projetos[p_name]
            st.rerun()

    st.markdown("---")
    st.write("**Eu sou LaunchBot seu assistente virtual**")
    user_q = st.text_input("Digite sua dúvida abaixo e tecle enter")
    if user_q:
        st.session_state.chat_history.append(f"👤: {user_q}")
        st.session_state.chat_history.append(f"🤖: {chamar_ia(user_q)}")
    for m in reversed(st.session_state.chat_history): st.write(m)

st.markdown('<div class="footer">© 2026 Nexus Launcer Lançamento inteligente de produtos digitais</div>', unsafe_allow_html=True)
