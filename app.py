import streamlit as st
from groq import Groq
import time
from datetime import datetime

# --- 1. CONFIGURAÇÃO E DESIGN "NEXUS" ---
st.set_page_config(page_title="NEXUS LAUNCHER", page_icon="🧠", layout="wide")

if 'memoria' not in st.session_state: st.session_state.memoria = {}
canal_selecionado = st.session_state.memoria.get('canal_escolhido', 'Padrão')

cores_canais = {
    "WhatsApp": "#25D366",
    "YouTube": "#FF0000",
    "Facebook": "#1877F2",
    "E-mail Marketing": "#1F2937", # Estilo Dark para E-mail
    "Padrão": "#00BFFF"
}
cor_tema = cores_canais.get(canal_selecionado, "#00BFFF")

st.markdown(f"""
    <style>
    [data-testid="stSidebar"] {{ display: none; }}
    header {{ visibility: hidden; }}
    .stApp {{ background-color: #FFFFFF; color: #000000; padding-bottom: 100px; }}
    h1, h2, h3, h4, p, span, label, .stMarkdown, .stMarkdown p {{ color: #000000 !important; font-family: 'Inter', sans-serif; }}
    .stProgress > div > div > div > div {{ background-color: {cor_tema}; }}
    
    .nexus-card {{
        background: #F0F2F6 !important;
        border: 2px solid {cor_tema};
        padding: 25px;
        border-radius: 20px;
        margin-bottom: 20px;
    }}
    
    .stButton > button {{
        background: {cor_tema} !important;
        color: #FFFFFF !important;
        padding: 12px 20px !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        width: 100% !important;
        text-transform: uppercase;
        border: none;
    }}
    
    .instruction-box {{
        background-color: #F8FAFC;
        border-left: 5px solid #007BFF;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }}
    
    .footer {{ position: fixed; left: 0; bottom: 0; width: 100%; background-color: {cor_tema}; color: #FFFFFF; text-align: center; padding: 10px; z-index: 1000; }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. LÓGICA DE INTELIGÊNCIA ---
def nexus_ai(prompt, system_role, api_key):
    try:
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            messages=[{"role": "system", "content": system_role}, {"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile"
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Erro: {str(e)}"

# --- 3. ESTADO E NAVEGAÇÃO ---
if 'etapa' not in st.session_state: st.session_state.etapa = 0
if 'api_key' not in st.session_state: st.session_state.api_key = "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"

# --- 4. INTERFACE ---

if st.session_state.etapa == 0:
    st.title("🧠 NEXUS LAUNCHER")
    st.write("### O Mentor Estratégico para seu Próximo Lançamento")
    if st.button("INICIAR OPERAÇÃO"):
        st.session_state.etapa = 1; st.rerun()

elif st.session_state.etapa == 1:
    st.title("🎯 1. DEFINIÇÃO DE NICHO")
    st.session_state.memoria['nicho'] = st.text_input("Qual o nicho do projeto?", value=st.session_state.memoria.get('nicho', ''))
    if st.button("AVANÇAR"): st.session_state.etapa = 2; st.rerun()

elif st.session_state.etapa == 2:
    st.title("🧲 2. MENTOR DE ATRAÇÃO & GERAÇÃO DE LEADS")
    canal = st.selectbox("Canal de Aquisição:", ["E-mail Marketing", "WhatsApp", "YouTube"], index=0)
    st.session_state.memoria['canal_escolhido'] = canal
    
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🚀 GERAR AUDIÊNCIA (LEADS)", "🤝 CONTEÚDO DE ENTRADA"])
    
    with tab1:
        st.subheader("Fábrica de Leads")
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            if st.button("🎁 GERAR E-BOOK ISCA"):
                p = f"Crie um E-book simples de 5 cartões para isca digital no nicho {st.session_state.memoria['nicho']}. Inclua Título, Promessa e o conteúdo dos 5 cartões."
                st.session_state.memoria['isca_txt'] = nexus_ai(p, "Escritor de Iscas", st.session_state.api_key)
        
        with col_b:
            if st.button("🌐 TEXTOS LANDING PAGE"):
                p = f"Crie a copy para uma Landing Page de captura focada no e-book: {st.session_state.memoria.get('isca_txt', 'Isca Digital')}. Preciso de Headline, Subheadline e CTA."
                st.session_state.memoria['lp_copy'] = nexus_ai(p, "Copywriter de LP", st.session_state.api_key)
        
        with col_c:
            if st.button("📈 ANÚNCIO GOOGLE/META"):
                p = f"Crie um anúncio de alta conversão para Google Search e Meta Ads focados em baixar o e-book do nicho {st.session_state.memoria['nicho']}."
                st.session_state.memoria['ads_txt'] = nexus_ai(p, "Gestor de Tráfego AI", st.session_state.api_key)

        # Exibição dos resultados e Orientações
        if 'isca_txt' in st.session_state.memoria:
            st.markdown("### 📘 Seu E-book Isca")
            st.info(st.session_state.memoria['isca_txt'])
            st.markdown("<div class='instruction-box'><b>COMO FAZER:</b> Use o Canva ou Gamma.app. Crie 5 slides simples com esses textos. Cada slide é um 'cartão' do conhecimento.</div>", unsafe_allow_html=True)

        if 'lp_copy' in st.session_state.memoria:
            st.markdown("### 🌐 Copy da Landing Page")
            st.success(st.session_state.memoria['lp_copy'])
            st.markdown("<div class='instruction-box'><b>ONDE CRIAR:</b> Use GreatPages ou o próprio Canva (Websites). Insira o campo de E-mail/WhatsApp integrado para entregar o E-book após o cadastro.</div>", unsafe_allow_html=True)

        if 'ads_txt' in st.session_state.memoria:
            st.markdown("### 📢 Script de Anúncio")
            st.warning(st.session_state.memoria['ads_txt'])
            st.markdown("<div class='instruction-box'><b>COMO ANUNCIAR:</b> No Google Ads, use a rede de pesquisa. No Meta, anuncie para Stories e Reels focando na dor que esse e-book resolve.</div>", unsafe_allow_html=True)

    with tab2:
        if st.button("GERAR GANCHOS VIRAIS"):
            st.write(nexus_ai(f"Gere 5 ganchos virais para {canal} no nicho {st.session_state.memoria['nicho']}.", "Expert em Viralização", st.session_state.api_key))
    
    st.markdown("</div>", unsafe_allow_html=True)
    if st.button("IR PARA O PRODUTO 👉"): st.session_state.etapa = 3; st.rerun()

elif st.session_state.etapa == 3:
    st.title("🧩 3. MATERIALIZAÇÃO DO PRODUTO")
    st.session_state.memoria['nome_produto'] = st.text_input("Nome do Produto Final:", value=st.session_state.memoria.get('nome_produto', ''))
    
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    tab_ebook, tab_video = st.tabs(["📄 PRODUTO E-BOOK (60 CARTÕES)", "🎥 VÍDEO AULAS"])
    
    with tab_ebook:
        if st.button("ESTRUTURAR E-BOOK COMPLETO"):
            p = f"Crie a estrutura de 60 cartões de conteúdo para o produto {st.session_state.memoria['nome_produto']}."
            st.session_state.memoria['prod_ebook'] = nexus_ai(p, "Info-produtor Senior", st.session_state.api_key)
        st.text_area("Conteúdo do Produto:", value=st.session_state.memoria.get('prod_ebook', ''), height=300)
    
    with tab_video:
        if st.button("GERAR ROTEIROS HEYGEN"):
            p = f"Crie 6 roteiros para o produto {st.session_state.memoria['nome_produto']}."
            st.write(nexus_ai(p, "Roteirista de IA", st.session_state.api_key))
    
    st.markdown("</div>", unsafe_allow_html=True)
    if st.button("AVANÇAR PARA DOUTRINAÇÃO 👉"): st.session_state.etapa = 4; st.rerun()

# Botão de Voltar Geral
if st.session_state.etapa > 0:
    if st.button("⬅ VOLTAR"): st.session_state.etapa -= 1; st.rerun()

st.markdown(f'<div class="footer">NEXUS SYSTEM — Atrai, Engaja e Vende Automático</div>', unsafe_allow_html=True)
