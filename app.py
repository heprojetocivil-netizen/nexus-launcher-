import streamlit as st
from groq import Groq

# --- 1. CONFIGURAÇÃO E DESIGN "NEXUS" ---
st.set_page_config(page_title="NEXUS LAUNCHER", page_icon="🧠", layout="wide")

if 'memoria' not in st.session_state: st.session_state.memoria = {}
cor_tema = "#00BFFF" 

st.markdown(f"""
    <style>
    [data-testid="stSidebar"] {{ display: none; }}
    header {{ visibility: hidden; }}
    .stApp {{ background-color: #FFFFFF; color: #000000; padding-bottom: 100px; }}
    h1, h2, h3, h4, p, span, label, .stMarkdown, .stMarkdown p {{ color: #000000 !important; font-family: 'Inter', sans-serif; }}
    
    .nexus-card {{
        background: #F8FAFC !important;
        border: 2px solid {cor_tema};
        padding: 25px;
        border-radius: 20px;
        margin-bottom: 20px;
    }}
    
    .stButton > button {{
        background: {cor_tema} !important;
        color: #FFFFFF !important;
        padding: 15px 25px !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        width: 100% !important;
        text-transform: uppercase;
        border: none;
    }}

    .instruction-box {{
        background-color: #F1F5F9;
        border-left: 5px solid {cor_tema};
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        font-size: 0.9em;
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
    except Exception as e: return f"Erro: {str(e)}"

# --- 3. ESTADO ---
if 'etapa' not in st.session_state: st.session_state.etapa = 0
api_key = "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"

# --- 4. FLUXO NEXUS ---

if st.session_state.etapa == 0:
    st.title("🧠 NEXUS: SISTEMA DE LANÇAMENTO DIRETO")
    st.write("### Anúncio → Landing Page → Grupo → Live")
    st.session_state.memoria['nicho'] = st.text_input("Qual o seu Nicho?", placeholder="Ex: Marketing para Dentistas")
    if st.button("INICIAR ESTRATÉGIA"):
        if st.session_state.memoria['nicho']: st.session_state.etapa = 1; st.rerun()

elif st.session_state.etapa == 1:
    st.title("📢 1. CAPTAÇÃO (VÍDEO E PÁGINA)")
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🎬 GERAR SCRIPT DO VÍDEO"):
            p = f"Crie um roteiro de 60s para anúncio em vídeo. Eu convidando para um minicurso de {st.session_state.memoria['nicho']}. Foque em dor e chamada para ação."
            st.session_state.memoria['script_video'] = nexus_ai(p, "Diretor de Criativos", api_key)
    with c2:
        if st.button("🌐 ESTRUTURA DA LANDING PAGE"):
            p = f"Crie Headline, Promessa e 3 Benefícios para a página de captura do nicho {st.session_state.memoria['nicho']}."
            st.session_state.memoria['txt_lp'] = nexus_ai(p, "Copywriter Senior", api_key)

    if 'script_video' in st.session_state.memoria: st.info(st.session_state.memoria['script_video'])
    if 'txt_lp' in st.session_state.memoria: st.success(st.session_state.memoria['txt_lp'])
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("CRIAR O PRODUTO E AQUECIMENTO 👉"): st.session_state.etapa = 2; st.rerun()

elif st.session_state.etapa == 2:
    st.title("📦 2. PRODUTOS E MENSAGENS")
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    
    tab_prod, tab_whats = st.tabs(["🎁 CRIAÇÃO DOS PRODUTOS", "📲 COMANDO DO WHATSAPP"])
    
    with tab_prod:
        st.subheader("Conteúdo para entregar")
        col_eb, col_aula = st.columns(2)
        with col_eb:
            if st.button("📄 E-BOOK ISCA (5 CARTÕES)"):
                p = f"Crie o conteúdo de um E-book isca de 5 cartões para entregar no grupo de {st.session_state.memoria['nicho']}."
                st.session_state.memoria['isca_pdf'] = nexus_ai(p, "Escritor", api_key)
        with col_aula:
            if st.button("🎥 EMENTA DO CURSO PRINCIPAL"):
                p = f"Crie a ementa de 6 módulos para o curso pago de {st.session_state.memoria['nicho']} que será vendido na live."
                st.session_state.memoria['ementa_curso'] = nexus_ai(p, "Infoprodutor", api_key)
        
        if 'isca_pdf' in st.session_state.memoria: st.info(st.session_state.memoria['isca_pdf'])
        if 'ementa_curso' in st.session_state.memoria: st.success(st.session_state.memoria['ementa_curso'])

    with tab_whats:
        st.subheader("Textos do Grupo")
        if st.button("GERAR DESCRIÇÃO E MENSAGENS"):
            p = f"Gere a descrição do grupo VIP e 3 mensagens de aquecimento para o nicho {st.session_state.memoria['nicho']}."
            st.session_state.memoria['txt_whats'] = nexus_ai(p, "Expert em WhatsApp", api_key)
        if 'txt_whats' in st.session_state.memoria: st.write(st.session_state.memoria['txt_whats'])
        
    st.markdown("</div>", unsafe_allow_html=True)
    if st.button("PREPARAR A LIVE DE VENDA 👉"): st.session_state.etapa = 3; st.rerun()

elif st.session_state.etapa == 3:
    st.title("🎤 3. LIVE E FECHAMENTO")
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🧠 ORIENTAÇÃO DE ORATÓRIA"):
            p = f"Dê dicas de postura e oratória para a live de {st.session_state.memoria['nicho']}."
            st.session_state.memoria['oratoria'] = nexus_ai(p, "Coach", api_key)
    with c2:
        if st.button("💰 SCRIPT DO PITCH"):
            p = f"Crie o roteiro da oferta final para vender o curso pago na live."
            st.session_state.memoria['pitch'] = nexus_ai(p, "Vendedor Senior", api_key)
    
    if 'oratoria' in st.session_state.memoria: st.info(st.session_state.memoria['oratoria'])
    if 'pitch' in st.session_state.memoria: st.success(st.session_state.memoria['pitch'])
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("FINALIZAR"): st.balloons(); st.success("Lançamento configurado!")

if st.session_state.etapa > 0:
    if st.button("⬅ VOLTAR"): st.session_state.etapa -= 1; st.rerun()

st.markdown(f'<div class="footer">NEXUS — SISTEMA COMPLETO ATIVADO</div>', unsafe_allow_html=True)
