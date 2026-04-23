import streamlit as st
from groq import Groq

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="NEXUS LAUNCER", page_icon="🚀", layout="centered")

# --- ESTILO VISUAL ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background-color: #00BFFF !important; color: white !important; font-weight: bold; border: none; }
    .resumo-ia { background-color: #F8FAFC; padding: 20px; border-radius: 10px; border-left: 5px solid #00BFFF; margin-bottom: 20px; color: #1E293B; }
    [data-testid="stSidebar"] { display: none; }
    .footer { text-align: center; padding: 20px; color: #64748b; font-size: 0.8em; }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO DE ESTADOS ---
if 'etapa' not in st.session_state: st.session_state.etapa = "Login"
if 'dados' not in st.session_state: st.session_state.dados = {}
if 'projetos' not in st.session_state: st.session_state.projetos = {}
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

# --- MOTOR IA ---
api_key = "SUA_CHAVE_AQUI" # <--- INSIRA SUA CHAVE DA GROQ

def nexus_ia(prompt):
    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            messages=[{"role": "system", "content": "Você é o LaunchBot. Personalize os textos fornecidos mantendo o tamanho e teor original. Não simplifique. Adicione orientações de imagens/cenas para vídeos conforme o nicho."}, 
                      {"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile"
        )
        return response.choices[0].message.content
    except Exception as e: return f"Erro técnico: {e}"

# --- FLUXO DO SISTEMA ---

# 1. LOGIN
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
        else: st.error("Acesso Negado.")

# 2. FORMULÁRIO
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

# 3. E-BOOK
elif st.session_state.etapa == "Ebook":
    st.title("E-BOOK PROFISSIONAL")
    if st.button("GERAR CONTEÚDO – 60 CARTÕES"):
        with st.spinner("Criando conteúdo estruturado..."):
            p = f"Gere 60 cartões de conteúdo para o eBook '{st.session_state.dados['nome_eb']}' no nicho {st.session_state.dados['nicho']} focado em {st.session_state.dados['dor']}."
            st.session_state.dados['ebook_txt'] = nexus_ia(p)
    if 'ebook_txt' in st.session_state.dados:
        st.markdown(f"<div class='resumo-ia'>{st.session_state.dados['ebook_txt']}</div>", unsafe_allow_html=True)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "VSL_Anuncio"
            st.rerun()

# 4. VSL ANÚNCIO
elif st.session_state.etapa == "VSL_Anuncio":
    st.title("🎬 1. VSL DO ANÚNCIO")
    if st.button("GERAR ROTEIRO"):
        with st.spinner("Personalizando e sugerindo imagens..."):
            template = f"Personalize este roteiro para o nicho {st.session_state.dados['nicho']} (Objetivo: {st.session_state.dados['dor']}). Mantenha o texto e adicione orientações de imagens para cada parágrafo: 'Se você quer [RESULTADO], mas sente que está perdido… provavelmente não é falta de esforço. É falta de direção. A maioria das pessoas comete um erro simples… e por isso continua tentando e não sai do lugar. E o pior: nem percebem onde estão errando. Eu organizei um caminho direto pra resolver isso… e vou mostrar dentro de um grupo fechado. Sem complicação. É gratuito. Clica em SAIBA MAIS para entrar'"
            st.session_state.dados['vsl_anuncio'] = nexus_ia(template)
    if 'vsl_anuncio' in st.session_state.dados:
        st.markdown(f"<div class='resumo-ia'>{st.session_state.dados['vsl_anuncio']}</div>", unsafe_allow_html=True)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "LP"
            st.rerun()

# 5. LANDING PAGE
elif st.session_state.etapa == "LP":
    st.title("🌐 2. LANDING PAGE")
    link_grupo = st.text_input("Insira o link convite para o grupo")
    if st.button("GERAR ROTEIRO"):
        with st.spinner("Criando Landing Page..."):
            template = f"Personalize este roteiro de LP para {st.session_state.usuario} no nicho {st.session_state.dados['nicho']}: Headline: Um caminho simples para [RESULTADO], mesmo começando do zero. Texto: Eu sou {st.session_state.usuario}. Já estive onde você está... tentando várias coisas sem resultado. Até identificar um padrão simples que muda o jogo. O problema nunca foi esforço, foi direção. Se você sente que não sai do lugar, criei um grupo: O erro que te trava, O caminho simples, O que funciona na prática. Botão: ENTRAR NO GRUPO (Link: {link_grupo})."
            st.session_state.dados['lp_txt'] = nexus_ia(template)
    if 'lp_txt' in st.session_state.dados:
        st.markdown(f"<div class='resumo-ia'>{st.session_state.dados['lp_txt']}</div>", unsafe_allow_html=True)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "Mensagens"
            st.rerun()

# 6. MENSAGENS E VSL FINAL
elif st.session_state.etapa == "Mensagens":
    st.title("📌 3. MENSAGEM FIXA DO GRUPO")
    if st.button("GERAR MENSAGENS PARA O GRUPO"):
        with st.spinner("Personalizando sequência e VSL de Venda..."):
            template = f"Gere a Descrição do Grupo, Mensagens Dia 1 a 5 e VSL Final Dia 6 para o nicho {st.session_state.dados['nicho']} (Preço: {st.session_state.dados['preco']}). Siga rigorosamente o roteiro de copy fornecido (Perguntas diretas, Direção errada, Ponto simples, VSL Final com Garantia de 7 dias e link com 30% desconto). Adicione sugestões de imagens para a VSL Final do Dia 6."
            st.session_state.dados['msg_txt'] = nexus_ia(template)
    if 'msg_txt' in st.session_state.dados:
        st.markdown(f"<div class='resumo-ia'>{st.session_state.dados['msg_txt']}</div>", unsafe_allow_html=True)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "Finalizacao"
            st.rerun()

# 7. VISUALIZAÇÃO FINAL E PROJETOS
elif st.session_state.etapa == "Finalizacao":
    st.title(f"🚀 PROJETO: {st.session_state.dados['nome_eb']}")
    
    t1, t2, t3, t4, t5 = st.tabs(["📚 E-BOOK", "🎬 VSL", "🌐 LP", "📌 MENSAGENS", "📅 APLICAÇÃO"])
    
    with t1: st.write(st.session_state.dados.get('ebook_txt'))
    with t2: st.write(st.session_state.dados.get('vsl_anuncio'))
    with t3: st.write(st.session_state.dados.get('lp_txt'))
    with t4: st.write(st.session_state.dados.get('msg_txt'))
    with t5:
        st.markdown("""
        📘 **1. Criação do produto**
        - Gere o seu eBook usando o Gamma AI
        - Cadastre o produto na plataforma Monetizze
        - Estruture o material de forma simples e direta para venda

        🎬 **2. VSL (Vídeo de Vendas)**
        - Crie o vídeo do anúncio e o vídeo de vendas “última mensagem” na plataforma Heygen e suba no seu canal Youtube
        - Crie a Landing Page usando o Gamma, Insira o link do grupo e transforme ela em site também na plataforma Gamma.
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
        st.session_state.projetos[st.session_state.dados['nome_eb']] = st.session_state.dados
        st.success("Projeto Salvo!")

    st.markdown("---")
    st.subheader("Meus Projetos")
    for p_nome in list(st.session_state.projetos.keys()):
        c1, c2 = st.columns([0.8, 0.2])
        if c1.button(f"📂 {p_nome}"):
            st.session_state.dados = st.session_state.projetos[p_nome]
            st.rerun()
        if c2.button(f"🗑️", key=f"del_{p_nome}"):
            del st.session_state.projetos[p_nome]
            st.rerun()

    st.markdown("---")
    st.write("**Eu sou LaunchBot seu assistente virtual**")
    user_q = st.text_input("Digite sua dúvida abaixo e tecle enter")
    if user_q:
        st.session_state.chat_history.append(f"👤: {user_q}")
        st.session_state.chat_history.append(f"🤖: {nexus_ia(user_q)}")
    for m in reversed(st.session_state.chat_history): st.write(m)

st.markdown('<div class="footer">© 2026 Nexus Launcer - Lançamento inteligente de produtos digitais</div>', unsafe_allow_html=True)
