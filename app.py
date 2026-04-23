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
    .chat-box { background-color: #F1F5F9; padding: 15px; border-radius: 10px; margin-top: 5px; border: 1px solid #CBD5E1; }
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
                {"role": "system", "content": "Você é o LaunchBot. Siga os roteiros fornecidos de forma 100% fiel. NÃO RESUMA, NÃO SIMPLIFIQUE. Mantenha o tamanho original. Apenas adapte os termos entre colchetes para o nicho. Para vídeos, inclua orientações de imagens detalhadas para cada frase."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile"
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Erro na conexão com a IA: {e}"

# --- BARRA GLOBAL (INICIAR NOVO / MEUS PROJETOS) ---
def barra_global():
    if st.session_state.etapa != "Login":
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("➕ INICIAR NOVO PROJETO"):
                st.session_state.dados = {}
                st.session_state.etapa = "Formulario"
                st.rerun()
        with col2:
            with st.expander("📂 MEUS PROJETOS"):
                if not st.session_state.projetos:
                    st.write("Nenhum projeto salvo.")
                for nome_p in list(st.session_state.projetos.keys()):
                    c1, c2 = st.columns([0.8, 0.2])
                    if c1.button(f"📄 {nome_p}", key=f"load_{nome_p}"):
                        st.session_state.dados = st.session_state.projetos[nome_p]
                        st.session_state.etapa = "Visualizacao"
                        st.rerun()
                    if c2.button("🗑️", key=f"del_{nome_p}"):
                        del st.session_state.projetos[nome_p]
                        st.rerun()

# --- FLUXO DE TELAS ---

if st.session_state.etapa == "Login":
    st.title("NEXUS LAUNCER")
    st.subheader("USO RESTRITO À ASSOCIADOS QUIZ MAIS PRÊMIOS")
    st.info("Não coloque senha do site, só a chave api_key")
    nome_user = st.text_input("Nome")
    key_user = st.text_input("Chave", type="password")
    if st.button("ENTRAR"):
        if nome_user and key_user:
            st.session_state.usuario = nome_user
            st.session_state.api_key = key_user
            st.session_state.etapa = "Formulario"
            st.rerun()

elif st.session_state.etapa == "Formulario":
    barra_global()
    st.title("PREENCHA FORMULÁRIO")
    ni = st.text_input("Nicho")
    no = st.text_input("Nome do e-book")
    do = st.text_input("Qual dor ele resolve")
    pr = st.text_input("Preço")
    if st.button("AVANÇAR"):
        st.session_state.dados = {"nicho": ni, "nome_eb": no, "dor": do, "preco": pr}
        st.session_state.etapa = "Ebook"
        st.rerun()

elif st.session_state.etapa == "Ebook":
    barra_global()
    st.title("E-BOOK PROFISSOAL")
    if st.button("GERAR CONTEUDO – 60 CARTÕES"):
        with st.spinner("Gerando conteúdo..."):
            p = f"Gere 60 cartões de conteúdo para o eBook '{st.session_state.dados['nome_eb']}' no nicho {st.session_state.dados['nicho']} focado na dor: {st.session_state.dados['dor']}."
            st.session_state.dados['out_eb'] = chamar_ia(p, st.session_state.api_key)
    if 'out_eb' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['out_eb']}</div>", unsafe_allow_html=True)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "VSL_Anuncio"
            st.rerun()

elif st.session_state.etapa == "VSL_Anuncio":
    barra_global()
    st.title("🎬 1. VSL DO ANÚNCIO")
    if st.button("GERAR ROTEIRO"):
        with st.spinner("Personalizando roteiro..."):
            p = f"Personalize este texto sem simplificar para o nicho {st.session_state.dados['nicho']} e oriente as imagens: 'Se você quer [RESULTADO], mas sente que está perdido… provavelmente não é falta de esforço. É falta de direção. A maioria das pessoas comete um erro simples… e por isso continua tentando e não sai do lugar. E o pior: nem percebem onde estão errando. Eu organizei um caminho direto pra resolver isso… e vou mostrar dentro de um grupo fechado. Sem complicação. É gratuito. Clica em SAIBA MAIS para entrar'"
            st.session_state.dados['out_vsl1'] = chamar_ia(p, st.session_state.api_key)
    if 'out_vsl1' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['out_vsl1']}</div>", unsafe_allow_html=True)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "LP"
            st.rerun()

elif st.session_state.etapa == "LP":
    barra_global()
    st.title("🌐 2. LANDING PAGE")
    link_convite = st.text_input("insira o link convite para o grupo no botão acima")
    if st.button("GERAR ROTEIRO"):
        with st.spinner("Formatando em parágrafos..."):
            p = f"Personalize para {st.session_state.usuario} no nicho {st.session_state.dados['nicho']} separando em parágrafos fiéis ao texto: Headline: Um caminho simples para [RESULTADO], mesmo começando do zero. Texto: Eu sou {st.session_state.usuario}. Já estive exatamente onde você está… tentando várias coisas… sem resultado. Até começar a estudar e aplicar o que realmente funciona… e identificar um padrão simples que muda completamente o jogo. Depois de aplicar isso na prática… eu percebi que o problema nunca foi esforço — foi direção. Se você sente que está tentando… mas não sai do lugar… provavelmente está passando por isso também. Eu criei um grupo onde vou te mostrar isso de forma direta: O erro que te mantém travado; O caminho mais simples; O que realmente funciona na prática. Link do botão: {link_convite}"
            st.session_state.dados['out_lp'] = chamar_ia(p, st.session_state.api_key)
    if 'out_lp' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['out_lp']}</div>", unsafe_allow_html=True)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "Mensagens"
            st.rerun()

elif st.session_state.etapa == "Mensagens":
    barra_global()
    st.title("📌 3. MENSAGEM FIXA DO GRUPO")
    if st.button("GERAR MENSAGENS PARA O GRUPO"):
        with st.spinner("Gerando sequência completa..."):
            p = f"""Personalize sem simplificar para {st.session_state.dados['nicho']} mantendo o teor original: 
            DESCRIÇÃO DO GRUPO: Esse grupo é silencioso... caminho simples para [RESULTADO].
            DIA 1: Pergunta direta sobre caminho certo.
            DIA 2: Direção errada.
            DIA 3: Ponto simples que separa resultados.
            DIA 4: Parar de perder tempo.
            DIA 5: Amanhã mostro diferente.
            DIA 6 VSL FINAL: 'O que trava a maioria... fazer da forma certa'. eBook {st.session_state.dados['nome_eb']}, garantia 7 dias. Oriente as imagens para o vídeo do Dia 6 e gere a descrição curta com o link de 30% desconto."""
            st.session_state.dados['out_msgs'] = chamar_ia(p, st.session_state.api_key)
    if 'out_msgs' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['out_msgs']}</div>", unsafe_allow_html=True)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "Visualizacao"
            st.rerun()

elif st.session_state.etapa == "Visualizacao":
    barra_global()
    st.title(f"PROJETO: {st.session_state.dados.get('nome_eb', 'Novo Projeto')}")
    
    # Abas iniciam fechadas (expanded=False)
    with st.expander("📚 E-BOOK", expanded=False):
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('out_eb')}</div>", unsafe_allow_html=True)
    with st.expander("🎬 1. VSL DO ANÚNCIO", expanded=False):
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('out_vsl1')}</div>", unsafe_allow_html=True)
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
        st.session_state.projetos[st.session_state.dados['nome_eb']] = st.session_state.dados
        st.success("Projeto salvo com sucesso!")

    st.divider()
    # --- CHAT CONTÍNUO ---
    st.subheader("💬 LaunchBot")
    st.write("Eu sou o LaunchBot, especialista em lançamentos digitais de alta conversão")
    
    input_chat = st.text_input("Digite a sua dúvida", key="chat_input")
    if input_chat:
        resp = chamar_ia(input_chat, st.session_state.api_key)
        st.session_state.chat_history.append({"q": input_chat, "a": resp})
    
    for chat in reversed(st.session_state.chat_history):
        st.markdown(f"**Você:** {chat['q']}")
        st.markdown(f"<div class='chat-box'>**LaunchBot:** {chat['a']}</div>", unsafe_allow_html=True)
        st.markdown("---")

# --- RODAPÉ ---
st.markdown('<div class="footer">© 2026 Nexus Launcer Lançamento inteligente de produtos digitais</div>', unsafe_allow_html=True)
