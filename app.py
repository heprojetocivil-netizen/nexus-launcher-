import streamlit as st
from groq import Groq

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="NEXUS LANCEUR", page_icon="🚀", layout="centered")

# --- ESTILO CSS ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background-color: #00BFFF !important; color: white !important; font-weight: bold; border: none; }
    .ia-output { background-color: #F1F5F9; padding: 20px; border-radius: 10px; border-left: 6px solid #00BFFF; margin-top: 15px; }
    [data-testid="stSidebar"] { display: none; }
    </style>
""", unsafe_allow_html=True)

# --- CHAVE DE ATIVAÇÃO MESTRA ---
CHAVE_MESTRA = "NEXUS-PRO-2026"

# --- INICIALIZAÇÃO ---
if 'etapa' not in st.session_state: st.session_state.etapa = "Login"
if 'dados' not in st.session_state: st.session_state.dados = {}
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

def nexus_ia(prompt, user_key, system="Você é o NEXUS LANCEUR, especialista do Quiz Mais Prêmios."):
    try:
        client = Groq(api_key=user_key)
        response = client.chat.completions.create(
            messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile"
        )
        return response.choices[0].message.content
    except Exception as e: return f"Erro: Verifique se sua Chave API Groq está correta. {e}"

# --- 0. TELA DE LOGIN ---
if st.session_state.etapa == "Login":
    st.title("🚀 NEXUS LANCEUR")
    st.subheader("Área restrita para associados do Quiz mais Prêmios")
    
    nome_user = st.text_input("Seu nome:")
    chave_user = st.text_input("Chave de ativação (Senha do site):", type="password")
    st.markdown("---")
    st.info("Para usar a IA, insira sua própria API Key da Groq abaixo:")
    groq_key = st.text_input("Sua API KEY da Groq (gsk_...):", type="password")
    
    if st.button("ENTRAR NO SISTEMA"):
        if chave_user == CHAVE_MESTRA and nome_user and groq_key.startswith("gsk_"):
            st.session_state.usuario = nome_user
            st.session_state.user_api_key = groq_key
            st.session_state.etapa = "Novo Projeto"
            st.rerun()
        else:
            st.error("Verifique os dados. Lembre-se de colocar a sua chave da Groq.")

# --- 1. FORMULÁRIO (PARTE 1 E 2) ---
elif st.session_state.etapa == "Novo Projeto":
    st.title("🚀 FORMULÁRIO INTELIGENTE DE FUNIL")
    with st.form("f_setup"):
        st.subheader("👤 PARTE 1 — PREENCHIMENTO")
        nicho = st.text_input("1. Nicho do produto")
        publico = st.text_input("2. Público-alvo")
        objetivo = st.text_input("4. Objetivo principal")
        promessa = st.text_input("6. Promessa do produto (opcional)")
        preco = st.text_input("7. Preço do produto")
        btn_gerar = st.form_submit_button("GERAR INTELIGÊNCIA")

    if btn_gerar:
        with st.spinner("🤖 Nexus IA analisando..."):
            p = f"Nicho: {nicho}, Público: {publico}. Gere: 1. Dor principal, 2. Objeções, 3. Desejo emocional, 4. Promessa forte."
            st.session_state.dados = {
                "nicho": nicho, "publico": publico, "objetivo": objetivo, 
                "preco": preco, "promessa_opc": promessa, 
                "analise": nexus_ia(p, st.session_state.user_api_key)
            }

    if "analise" in st.session_state.dados:
        st.subheader("🧠 PARTE 2 — IA GERA AUTOMATICAMENTE")
        st.markdown(f"<div class='ia-output'>{st.session_state.dados['analise']}</div>", unsafe_allow_html=True)
        if st.button("AVANÇAR PARA E-BOOKS ➡️"):
            st.session_state.etapa = "Confeccao Ebook"
            st.rerun()

# --- 2. EBOOK ---
elif st.session_state.etapa == "Confeccao Ebook":
    st.title("📦 GERE O SEU E-BOOKS PROFISSIONAL")
    if st.button("GERAR OS 60 CARTÕES"):
        with st.spinner("Gerando..."):
            st.session_state.dados['ebook'] = nexus_ia(f"Gere 60 cartões de eBook para {st.session_state.dados['nicho']}.", st.session_state.user_api_key)
    
    if 'ebook' in st.session_state.dados:
        st.text_area("Conteúdo:", st.session_state.dados['ebook'], height=300)
        if st.button("AVANÇAR PARA ANÚNCIO ➡️"):
            st.session_state.etapa = "Gere Anuncio"
            st.rerun()

# --- 3. ANÚNCIO VSL ---
elif st.session_state.etapa == "Gere Anuncio":
    st.title("🎬 GERE O ANÚNCIO EM VSL")
    if st.button("GERAR ANÚNCIO"):
        st.session_state.dados['anuncio'] = nexus_ia(f"Script VSL Google Ads: {st.session_state.dados['nicho']}. CTA: Saber Mais.", st.session_state.user_api_key)
    
    if 'anuncio' in st.session_state.dados:
        st.text_area("Script:", st.session_state.dados['anuncio'], height=250)
        if st.button("AVANÇAR PARA LANDING PAGE ➡️"):
            st.session_state.etapa = "Gere LP"
            st.rerun()

# --- 4. LANDING PAGE ---
elif st.session_state.etapa == "Gere LP":
    st.title("🌐 GERE SUA LANDING PAGE")
    if st.button("GERAR PÁGINA"):
        st.session_state.dados['lp'] = nexus_ia(f"Copy LP para {st.session_state.dados['nicho']}.", st.session_state.user_api_key)
    
    if 'lp' in st.session_state.dados:
        st.text_area("LP:", st.session_state.dados['lp'], height=250)
        if st.button("AVANÇAR PARA LANÇAMENTO ➡️"):
            st.session_state.etapa = "Lancamento"
            st.rerun()

# --- 5. LANÇAMENTO ---
elif st.session_state.etapa == "Lancamento":
    st.title("📅 SEQUÊNCIA DE LANÇAMENTO")
    if st.button("GERAR TUDO"):
        p = f"Mensagens Dia 1-6 e VSL Final Dia 7 para {st.session_state.dados['nicho']} preço {st.session_state.dados['preco']}."
        st.session_state.dados['sequencia'] = nexus_ia(p, st.session_state.user_api_key)
    
    if 'sequencia' in st.session_state.dados:
        st.text_area("Final:", st.session_state.dados['sequencia'], height=300)
        if st.button("💾 SALVAR PROJETO FINAL"):
            st.session_state.etapa = "Versao Final"
            st.rerun()

# --- 6. VERSÃO FINAL ---
elif st.session_state.etapa == "Versao Final":
    st.title("🚀 FUNIL COMPLETO (VERSÃO FINAL)")
    d = st.session_state.dados
    tabs = st.tabs(["📦 EBOOK", "🎬 VSL", "🌐 LP", "📌 GRUPO", "🛠️ APLICAR"])
    with tabs[0]: st.code(d.get('ebook', ''))
    with tabs[1]: st.code(d.get('anuncio', ''))
    with tabs[2]: st.code(d.get('lp', ''))
    with tabs[3]: st.code(d.get('sequencia', ''))
    with tabs[4]: st.write("Siga o passo a passo de implementação do Quiz Mais Prêmios.")

    st.markdown("---")
    st.subheader("💬 DÚVIDA?")
    user_q = st.text_input("Digite sua dúvida:")
    if st.button("ENVIAR"):
        st.session_state.chat_history.append(f"🤖: {nexus_ia(user_q, st.session_state.user_api_key)}")
    for m in reversed(st.session_state.chat_history): st.write(m)

st.markdown('<div style="text-align:center; padding:10px; color:#00BFFF; font-weight:bold;">NEXUS LANCEUR - QUIZ MAIS PRÊMIOS</div>', unsafe_allow_html=True)
🎯 O que mudou?
