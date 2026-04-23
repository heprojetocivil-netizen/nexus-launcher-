import streamlit as st
from groq import Groq

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="NEXUS LANCEUR", page_icon="🚀", layout="centered")

# --- ESTILO CSS CUSTOMIZADO ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background-color: #00BFFF !important; color: white !important; font-weight: bold; border: none; }
    .main-card { background-color: #F8FAFC; padding: 25px; border-radius: 15px; border: 1px solid #E2E8F0; margin-bottom: 20px; }
    .ia-output { background-color: #F1F5F9; padding: 20px; border-radius: 10px; border-left: 6px solid #00BFFF; margin-top: 15px; font-style: italic; }
    [data-testid="stSidebar"] { display: none; }
    </style>
""", unsafe_allow_html=True)

# --- CHAVE DE ATIVAÇÃO MESTRA ---
CHAVE_MESTRA = "NEXUS-PRO-2026"

# --- INICIALIZAÇÃO DE ESTADOS ---
if 'etapa' not in st.session_state: st.session_state.etapa = "Login"
if 'dados' not in st.session_state: st.session_state.dados = {}
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

# --- FUNÇÃO GERADORA IA ---
# Coloque sua chave Groq aqui
api_key = "SUA_CHAVE_AQUI" 

def nexus_ia(prompt, system="Você é o NEXUS LANCEUR, especialista do Quiz Mais Prêmios."):
    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile"
        )
        return response.choices[0].message.content
    except Exception as e: return f"Erro na conexão: {e}"

# --- FLUXO DO APLICATIVO ---

# 0. TELA DE LOGIN
if st.session_state.etapa == "Login":
    st.title("🚀 NEXUS LANCEUR")
    st.subheader("Área restrita para associados do Quiz mais Prêmios")
    
    with st.container():
        nome_user = st.text_input("Seu nome:")
        chave_user = st.text_input("Chave de ativação:", type="password")
        
        if st.button("ENTRAR"):
            if chave_user == CHAVE_MESTRA and nome_user:
                st.session_state.usuario = nome_user
                st.session_state.etapa = "Novo Projeto"
                st.rerun()
            else:
                st.error("Chave inválida ou campo vazio.")

# 1. NOVO PROJETO + FORMULÁRIO (PARTE 1 E 2)
elif st.session_state.etapa == "Novo Projeto":
    st.title("🚀 FORMULÁRIO INTELIGENTE DE FUNIL")
    st.write(f"Operador: **{st.session_state.usuario}**")
    
    with st.form("f_setup"):
        st.subheader("👤 PARTE 1 — O USUÁRIO PREENCHE")
        nicho = st.text_input("1. Nicho do produto")
        publico = st.text_input("2. Público-alvo")
        st.info("📦 3. Produto: E-books")
        objetivo = st.text_input("4. Objetivo principal do produto")
        promessa = st.text_input("6. Promessa do produto (opcional)")
        preco = st.text_input("7. Preço do produto")
        
        btn_gerar = st.form_submit_button("GERAR INTELIGÊNCIA")

    if btn_gerar:
        with st.spinner("🤖 Nexus IA analisando dados..."):
            prompt = f"Com base no nicho {nicho} e público {publico}, gere: 1. Dor principal, 2. Objeções prováveis, 3. Desejo emocional, 4. Promessa forte."
            st.session_state.dados = {
                "nicho": nicho, "publico": publico, "objetivo": objetivo, 
                "preco": preco, "promessa_opc": promessa, "analise": nexus_ia(prompt)
            }

    if "analise" in st.session_state.dados:
        st.subheader("🧠 PARTE 2 — O QUE A IA GERA AUTOMATICAMENTE")
        st.markdown(f"<div class='ia-output'>{st.session_state.dados['analise']}</div>", unsafe_allow_html=True)
        
        if st.button("AVANÇAR PARA E-BOOKS ➡️"):
            st.session_state.etapa = "Confeccao Ebook"
            st.rerun()

# 2. CONFECÇÃO E-BOOK
elif st.session_state.etapa == "Confeccao Ebook":
    st.title("📦 GERE O SEU E-BOOKS PROFISSIONAL")
    if st.button("GERAR OS 60 CARTÕES"):
        with st.spinner("Gerando conteúdo..."):
            st.session_state.dados['ebook'] = nexus_ia(f"Gere 60 cartões rápidos para um eBook de {st.session_state.dados['nicho']} focado em {st.session_state.dados['objetivo']}.")
    
    if 'ebook' in st.session_state.dados:
        st.text_area("Cartões Gerados:", st.session_state.dados['ebook'], height=300)
        if st.button("AVANÇAR PARA ANÚNCIO ➡️"):
            st.session_state.etapa = "Gere Anuncio"
            st.rerun()

# 3. ANÚNCIO VSL
elif st.session_state.etapa == "Gere Anuncio":
    st.title("🎬 GERE O ANÚNCIO EM VSL")
    if st.button("GERAR ANÚNCIO"):
        with st.spinner("Criando script..."):
            st.session_state.dados['anuncio'] = nexus_ia(f"Crie um script de VSL curta para Google Ads no nicho {st.session_state.dados['nicho']}. CTA: Saber Mais.")
    
    if 'anuncio' in st.session_state.dados:
        st.text_area("Script VSL:", st.session_state.dados['anuncio'], height=250)
        if st.button("AVANÇAR PARA LANDING PAGE ➡️"):
            st.session_state.etapa = "Gere LP"
            st.rerun()

# 4. LANDING PAGE
elif st.session_state.etapa == "Gere LP":
    st.title("🌐 GERE SUA LANDING PAGE")
    if st.button("GERAR PÁGINA"):
        with st.spinner("Desenhando copy..."):
            st.session_state.dados['lp'] = nexus_ia(f"Crie uma Landing Page para {st.session_state.dados['nicho']} baseada na promessa: {st.session_state.dados.get('promessa_opc')}.")
    
    if 'lp' in st.session_state.dados:
        st.text_area("Copy da LP:", st.session_state.dados['lp'], height=250)
        if st.button("AVANÇAR PARA LANÇAMENTO ➡️"):
            st.session_state.etapa = "Lancamento"
            st.rerun()

# 5. LANÇAMENTO COMPLETO
elif st.session_state.etapa == "Lancamento":
    st.title("📅 SEQUÊNCIA DE LANÇAMENTO")
    if st.button("GERAR SEQUÊNCIA COMPLETA"):
        with st.spinner("Gerando mensagens e VSL Final..."):
            p = f"Crie descrição do grupo, mensagens de aquecimento Dia 1 a 6 e VSL Final Dia 7 para {st.session_state.dados['nicho']} com preço {st.session_state.dados['preco']}."
            st.session_state.dados['sequencia'] = nexus_ia(p)
    
    if 'sequencia' in st.session_state.dados:
        st.text_area("Cronograma:", st.session_state.dados['sequencia'], height=300)
        if st.button("💾 SALVAR PROJETO FINAL"):
            st.session_state.etapa = "Versao Final"
            st.rerun()

# 6. VERSÃO FINAL (VISUALIZAÇÃO)
elif st.session_state.etapa == "Versao Final":
    st.title("🚀 FUNIL COMPLETO (VERSÃO FINAL PROFISSIONAL)")
    d = st.session_state.dados
    
    aba1, aba2, aba3, aba4, aba5 = st.tabs(["📦 EBOOK", "🎬 ANÚNCIO", "🌐 LP", "📌 LANÇAMENTO", "🛠️ COMO APLICAR"])
    
    with aba1: st.code(d.get('ebook', ''))
    with aba2: st.code(d.get('anuncio', ''))
    with aba3: st.code(d.get('lp', ''))
    with aba4: st.code(d.get('sequencia', ''))
    with aba5:
        st.write("1. E-book no Canva.")
        st.write("2. Anúncio no Google Ads.")
        st.write("3. LP no Elementor.")
        st.write("4. Siga os 7 dias de grupo.")

    st.markdown("---")
    st.subheader("💬 TEM ALGUMA DÚVIDA?")
    user_q = st.text_input("Digite sua dúvida sobre o projeto:")
    if st.button("ENVIAR"):
        resp = nexus_ia(f"Dúvida do usuário: {user_q}")
        st.session_state.chat_history.append(f"🤖: {resp}")
    
    for m in reversed(st.session_state.chat_history):
        st.write(m)

st.markdown('<div class="footer">NEXUS LANCEUR - QUIZ MAIS PRÊMIOS</div>', unsafe_allow_html=True)
