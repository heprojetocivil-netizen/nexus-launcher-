import streamlit as st
from groq import Groq

# --- CONFIGURAÇÕES DE PÁGINA ---
st.set_page_config(page_title="NEXUS LAUNCER", layout="centered")

# --- ESTILO CUSTOMIZADO ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { display: none; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3.5em; background-color: #00BFFF !important; color: white !important; font-weight: bold; border: none; }
    .caixa-texto { background-color: #F8FAFC; padding: 20px; border-radius: 10px; border-left: 5px solid #00BFFF; margin-bottom: 20px; white-space: pre-wrap; color: #1E293B; }
    .footer { text-align: center; padding: 40px; color: #94A3B8; font-size: 0.85em; border-top: 1px solid #E2E8F0; margin-top: 50px; }
    </style>
""", unsafe_allow_html=True)

# --- ESTADOS DA SESSÃO ---
if 'etapa' not in st.session_state: st.session_state.etapa = "Login"
if 'dados' not in st.session_state: st.session_state.dados = {}
if 'projetos' not in st.session_state: st.session_state.projetos = {}

# --- FUNÇÃO DE CHAMADA À IA ---
def gerar_copy(prompt, api_key):
    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Você é o LaunchBot. Sua missão é personalizar textos de copy sem NUNCA resumir, simplificar ou alterar o tamanho do texto original. Mantenha o teor fiel e apenas adapte os termos entre colchetes para o nicho do usuário. Para vídeos, inclua obrigatoriamente descrições de imagens e cenas que combinem com o nicho."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile"
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Erro de conexão: Verifique sua chave API. ({e})"

# --- FLUXO DE TELAS ---

# 1. TELA DE LOGIN
if st.session_state.etapa == "Login":
    st.title("NEXUS LAUNCER")
    st.subheader("USO RESTRITO À ASSOCIADOS QUIZ MAIS PRÊMIOS")
    st.info("Não coloque senha do site, só a chave api_key")
    
    nome = st.text_input("Nome")
    chave = st.text_input("Chave", type="password", placeholder="Insira sua gsk_...")
    
    if st.button("ENTRAR"):
        if nome and chave:
            st.session_state.nome_associado = nome
            st.session_state.api_key = chave
            st.session_state.etapa = "Formulario"
            st.rerun()
        else:
            st.warning("Preencha o nome e a chave corretamente.")

# 2. PREENCHA FORMULÁRIO
elif st.session_state.etapa == "Formulario":
    st.title("PREENCHA FORMULÁRIO")
    nicho = st.text_input("Nicho")
    nome_eb = st.text_input("Nome do e-book")
    dor = st.text_input("Qual dor ele resolve")
    preco = st.text_input("Preço")
    
    if st.button("AVANÇAR"):
        st.session_state.dados = {"nicho": nicho, "nome_eb": nome_eb, "dor": dor, "preco": preco}
        st.session_state.etapa = "Ebook"
        st.rerun()

# 3. E-BOOK PROFISSIONAL
elif st.session_state.etapa == "Ebook":
    st.title("E-BOOK PROFISSIONAL")
    if st.button("GERAR CONTEUDO – 60 CARTÕES"):
        with st.spinner("Gerando conteúdo completo..."):
            p = f"Gere exatamente 60 cartões de conteúdo para o e-book '{st.session_state.dados['nome_eb']}' focado no nicho {st.session_state.dados['nicho']} para resolver a dor: {st.session_state.dados['dor']}."
            st.session_state.dados['conteudo_ebook'] = gerar_copy(p, st.session_state.api_key)
    
    if 'conteudo_ebook' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['conteudo_ebook']}</div>", unsafe_allow_html=True)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "VSL_Anuncio"
            st.rerun()

# 4. VSL DO ANÚNCIO
elif st.session_state.etapa == "VSL_Anuncio":
    st.title("🎬 1. VSL DO ANÚNCIO")
    if st.button("GERAR ROTEIRO"):
        with st.spinner("Personalizando roteiro e imagens..."):
            prompt = f"""Personalize este texto sem simplificá-lo para o nicho {st.session_state.dados['nicho']}. Oriente também as imagens e cenas para cada trecho:
            'Se você quer [RESULTADO], mas sente que está perdido… provavelmente não é falta de esforço. É falta de direção. A maioria das pessoas comete um erro simples… e por isso continua tentando e não sai do lugar. E o pior: nem percebem onde estão errando. Eu organizei um caminho direto pra resolver isso… e vou mostrar dentro de um grupo fechado. Sem complicação. É gratuito. Clica em SAIBA MAIS para entrar'"""
            st.session_state.dados['vsl_anuncio'] = gerar_copy(prompt, st.session_state.api_key)
    
    if 'vsl_anuncio' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['vsl_anuncio']}</div>", unsafe_allow_html=True)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "LP"
            st.rerun()

# 5. LANDING PAGE
elif st.session_state.etapa == "LP":
    st.title("🌐 2. LANDING PAGE")
    link_convite = st.text_input("insira o link convite para o grupo no botão abaixo")
    if st.button("GERAR ROTEIRO"):
        with st.spinner("Personalizando Landing Page..."):
            prompt = f"""Personalize este roteiro de Landing Page para o usuário '{st.session_state.nome_associado}' no nicho {st.session_state.dados['nicho']} sem resumir:
            Headline: Um caminho simples para [RESULTADO], mesmo começando do zero.
            Texto: Eu sou {st.session_state.nome_associado}. Já estive exatamente onde você está… tentando várias coisas… sem resultado. Até começar a estudar e aplicar o que realmente funciona… e identificar um padrão simples que muda completamente o jogo. Depois de aplicar isso na prática… eu percebi que o problema nunca foi esforço — foi direção.
            Se você sente que está tentando… mas não sai do lugar… provavelmente está passando por isso também. Eu criei um grupo onde vou te mostrar isso de forma direta: O erro que te mantém travado; O caminho mais simples; O que realmente funciona na prática.
            BOTÃO: ENTRAR NO GRUPO (Link: {link_convite})"""
            st.session_state.dados['lp_copy'] = gerar_copy(prompt, st.session_state.api_key)

    if 'lp_copy' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['lp_copy']}</div>", unsafe_allow_html=True)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "Mensagens"
            st.rerun()

# 6. MENSAGENS DO GRUPO
elif st.session_state.etapa == "Mensagens":
    st.title("📌 3. MENSAGEM FIXA DO GRUPO")
    if st.button("GERAR MENSAGENS PARA O GRUPO"):
        with st.spinner("Personalizando sequência de 6 dias..."):
            prompt = f"""Personalize as mensagens abaixo para o nicho {st.session_state.dados['nicho']} sem simplificar, mantendo o tamanho e o teor original.
            DESCRIÇÃO DO GRUPO: Esse grupo é silencioso. Você não será incomodado hora nenhuma. Eu vou te mostrar um caminho simples para [RESULTADO]. Não é teoria… é algo direto. Fica até o final.
            DIA 1: Deixa eu te fazer uma pergunta direta: Você sente que está no caminho certo… ou só tentando coisas e esperando dar certo?
            DIA 2: A maioria das pessoas não falha por falta de esforço… falha porque está andando na direção errada. E o pior: só percebe depois de muito tempo.
            DIA 3: Existe um ponto simples que separa quem consegue resultado… de quem continua tentando. E não tem nada a ver com trabalhar mais.
            DIA 4: Quando você entende isso… você para de perder tempo com o que não funciona. E começa a focar no que realmente dá resultado.
            DIA 5: Eu poderia explicar tudo aqui… mas a maioria das pessoas não aplicaria. Então amanhã eu vou te mostrar isso de forma diferente.
            DIA 6 (VSL FINAL): Eu falei que hoje ia te mostrar… então presta atenção nisso: O que trava a maioria das pessoas não é falta de esforço… é não entender esse ponto: você não precisa fazer mais… você precisa fazer da forma certa. Enquanto você tenta sem direção… você continua no mesmo lugar. Quando você entende isso… tudo muda. E foi exatamente isso que eu fiz: eu organizei um caminho simples… direto… pra sair desse ciclo e chegar em [RESULTADO]. E coloquei tudo isso em um eBook simples e direto ao ponto… com o passo a passo pra você aplicar. Você pode acessar agora… com garantia de 7 dias. Se não fizer sentido pra você, pode pedir reembolso sem complicação. O acesso já está liberado. Clica no link e vê todos os detalhes.
            DESCRIÇÃO DO VSL: Clique no link para acessar o seu e-book com 30% de desconto, somente hoje.
            ORIENTAÇÃO DE IMAGENS: Inclua orientações de cenas para o vídeo do Dia 6."""
            st.session_state.dados['msgs_grupo'] = gerar_copy(prompt, st.session_state.api_key)

    if 'msgs_grupo' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['msgs_grupo']}</div>", unsafe_allow_html=True)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "Final"
            st.rerun()

# 7. TELA FINAL E PROJETOS
elif st.session_state.etapa == "Final":
    st.title(f"PROJETO: {st.session_state.dados['nome_eb']}")
    
    # Abas conforme solicitado
    aba1, aba2, aba3, aba4, aba5 = st.tabs(["📚 E-BOOK", "🎬 1. VSL DO ANÚNCIO", "🌐 2. LANDING PAGE", "📌 3. MENSAGENS", "📅 APLICAÇÃO"])
    
    with aba1: st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('conteudo_ebook')}</div>", unsafe_allow_html=True)
    with aba2: st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('vsl_anuncio')}</div>", unsafe_allow_html=True)
    with aba3: st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('lp_copy')}</div>", unsafe_allow_html=True)
    with aba4: st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('msgs_grupo')}</div>", unsafe_allow_html=True)
    with aba5:
        st.markdown(f"""
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

    if st.button("SALVAR PROJETO"):
        nome_p = st.session_state.dados['nome_eb']
        st.session_state.projetos[nome_p] = dict(st.session_state.dados)
        st.success(f"Projeto '{nome_p}' salvo com sucesso!")

    st.markdown("---")
    st.subheader("Meus Projetos")
    for proj in list(st.session_state.projetos.keys()):
        col_n, col_d = st.columns([0.8, 0.2])
        if col_n.button(f"📂 {proj}"):
            st.session_state.dados = st.session_state.projetos[proj]
            st.rerun()
        if col_d.button(f"🗑️", key=f"del_{proj}"):
            del st.session_state.projetos[proj]
            st.rerun()

st.markdown('<div class="footer">© 2026 Nexus Launcer Lançamento inteligente de produtos digitais</div>', unsafe_allow_html=True)
