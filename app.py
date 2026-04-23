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
    .btn-novo { background-color: #EF4444 !important; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO ---
if 'etapa' not in st.session_state: st.session_state.etapa = "Login"
if 'dados' not in st.session_state: st.session_state.dados = {}
if 'projetos' not in st.session_state: st.session_state.projetos = {}

# --- FUNÇÃO IA ---
def nexus_ia(prompt, api_key):
    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Você é o LaunchBot. Siga os roteiros de copy fielmente. NÃO RESUMA, NÃO SIMPLIFIQUE. Mantenha o mesmo tamanho e teor. Personalize apenas os termos técnicos para o nicho. Para VSLs, inclua orientações de imagens/cenas detalhadas."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile"
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Erro na Chave: {e}"

# --- COMPONENTES GLOBAIS ---
def menu_global():
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("➕ INICIAR NOVO PROJETO", key="btn_novo_global"):
            st.session_state.dados = {}
            st.session_state.etapa = "Formulario"
            st.rerun()
    with col2:
        with st.expander("📂 MEUS PROJETOS"):
            if not st.session_state.projetos:
                st.write("Nenhum projeto salvo.")
            for p in list(st.session_state.projetos.keys()):
                if st.button(f"📄 {p}", key=f"load_{p}"):
                    st.session_state.dados = st.session_state.projetos[p]
                    st.session_state.etapa = "Visualizacao"
                    st.rerun()

# --- TELAS ---

if st.session_state.etapa == "Login":
    st.title("NEXUS LAUNCER")
    st.subheader("USO RESTRITO À ASSOCIADOS QUIZ MAIS PRÊMIOS")
    st.warning("Não coloque senha do site, só a chave api_key")
    nome = st.text_input("Nome")
    chave = st.text_input("Chave (API Key)", type="password")
    if st.button("ENTRAR"):
        if nome and chave:
            st.session_state.usuario = nome
            st.session_state.api_key = chave
            st.session_state.etapa = "Formulario"
            st.rerun()

elif st.session_state.etapa == "Formulario":
    menu_global()
    st.title("PREENCHA FORMULÁRIO")
    nicho = st.text_input("Nicho")
    nome_eb = st.text_input("Nome do e-book")
    dor = st.text_input("Qual dor ele resolve")
    preco = st.text_input("Preço")
    if st.button("AVANÇAR"):
        st.session_state.dados = {"nicho": nicho, "nome_eb": nome_eb, "dor": dor, "preco": preco}
        st.session_state.etapa = "Ebook"
        st.rerun()

elif st.session_state.etapa == "Ebook":
    menu_global()
    st.title("E-BOOK PROFISSIONAL")
    if st.button("GERAR CONTEUDO – 60 CARTÕES"):
        with st.spinner("Gerando..."):
            p = f"Gere 60 cartões de conteúdo para o eBook {st.session_state.dados['nome_eb']} no nicho {st.session_state.dados['nicho']} focado em {st.session_state.dados['dor']}."
            st.session_state.dados['out_eb'] = nexus_ia(p, st.session_state.api_key)
    if 'out_eb' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['out_eb']}</div>", unsafe_allow_html=True)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "VSL_Anuncio"
            st.rerun()

elif st.session_state.etapa == "VSL_Anuncio":
    menu_global()
    st.title("🎬 1. VSL DO ANÚNCIO")
    if st.button("GERAR ROTEIRO"):
        with st.spinner("Processando..."):
            p = f"Personalize este roteiro para {st.session_state.dados['nicho']} sem simplificar e oriente imagens: 'Se você quer [RESULTADO], mas sente que está perdido… provavelmente não é falta de esforço. É falta de direção. A maioria das pessoas comete um erro simples… e por isso continua tentando e não sai do lugar. E o pior: nem percebem onde estão errando. Eu organizei um caminho direto pra resolver isso… e vou mostrar dentro de um grupo fechado. Sem complicação. É gratuito. Clica em SAIBA MAIS para entrar'"
            st.session_state.dados['out_vsl1'] = nexus_ia(p, st.session_state.api_key)
    if 'out_vsl1' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['out_vsl1']}</div>", unsafe_allow_html=True)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "LP"
            st.rerun()

elif st.session_state.etapa == "LP":
    menu_global()
    st.title("🌐 2. LANDING PAGE")
    link = st.text_input("insira o link convite para o grupo no botão abaixo")
    if st.button("GERAR ROTEIRO"):
        with st.spinner("Gerando parágrafos..."):
            p = f"Personalize para {st.session_state.usuario} no nicho {st.session_state.dados['nicho']} separando em parágrafos: Headline: Um caminho simples para [RESULTADO], mesmo começando do zero. Texto: Eu sou {st.session_state.usuario}. Já estive exatamente onde você está… tentando várias coisas… sem resultado. Até começar a estudar e aplicar o que realmente funciona… e identificar um padrão simples que muda completamente o jogo. Depois de aplicar isso na prática… eu percebi que o problema nunca foi esforço — foi direção. Se você sente que está tentando… mas não sai do lugar… provavelmente está passando por isso também. Eu criei um grupo onde vou te mostrar isso de forma direta: O erro que te mantém travado; O caminho mais simples; O que realmente funciona na prática. BOTÃO: ENTRAR NO GRUPO (Link: {link})"
            st.session_state.dados['out_lp'] = nexus_ia(p, st.session_state.api_key)
    if 'out_lp' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['out_lp']}</div>", unsafe_allow_html=True)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "Mensagens"
            st.rerun()

elif st.session_state.etapa == "Mensagens":
    menu_global()
    st.title("📌 3. MENSAGEM FIXA DO GRUPO")
    if st.button("GERAR MENSAGENS PARA O GRUPO"):
        with st.spinner("Gerando sequência fiel..."):
            p = f"Personalize sem simplificar para {st.session_state.dados['nicho']}: Descrição do Grupo (caminho simples para [RESULTADO]). Dia 1: Pergunta direta. Dia 2: Direção Errada. Dia 3: Ponto Simples. Dia 4: Parar de perder tempo. Dia 5: Amanhã mostro diferente. Dia 6 VSL Final: 'O que trava a maioria... fazer da forma certa'. eBook {st.session_state.dados['nome_eb']}, garantia 7 dias, link loja 30% desconto. Oriente imagens para o Dia 6 e gere a descrição curta abaixo com o link."
            st.session_state.dados['out_msg'] = nexus_ia(p, st.session_state.api_key)
    if 'out_msg' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['out_msg']}</div>", unsafe_allow_html=True)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "Visualizacao"
            st.rerun()

elif st.session_state.etapa == "Visualizacao":
    menu_global()
    st.title(f"PROJETO: {st.session_state.dados.get('nome_eb', 'Sem Nome')}")
    
    aba1, aba2, aba3, aba4, aba5 = st.tabs(["📚 E-BOOK", "🎬 1. VSL DO ANÚNCIO", "🌐 2. LANDING PAGE", "📌 3. MENSAGENS", "📅 APLICAÇÃO"])
    
    with aba1: st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('out_eb')}</div>", unsafe_allow_html=True)
    with aba2: st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('out_vsl1')}</div>", unsafe_allow_html=True)
    with aba3: st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('out_lp')}</div>", unsafe_allow_html=True)
    with aba4: st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('out_msg')}</div>", unsafe_allow_html=True)
    with aba5:
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
        name = st.session_state.dados['nome_eb']
        st.session_state.projetos[name] = st.session_state.dados
        st.success("Projeto salvo!")

# --- RODAPÉ ---
st.markdown(f'<div class="footer">© 2026 Nexus Launcer Lançamento inteligente de produtos digitais</div>', unsafe_allow_html=True)
