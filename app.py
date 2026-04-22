import streamlit as st
from groq import Groq
import time

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

    .mentor-box {{
        background-color: #E0F2FE;
        border-left: 5px solid #0369A1;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }}
    
    .live-alert {{
        background-color: #FFF0F0;
        border: 2px solid #FF0000;
        color: #CC0000;
        padding: 20px;
        border-radius: 15px;
        font-weight: bold;
        text-align: center;
        font-size: 20px;
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
    except Exception as e: return f"Erro na conexão Nexus: {str(e)}"

# --- 3. ESTADO ---
if 'etapa' not in st.session_state: st.session_state.etapa = 0
if 'api_key' not in st.session_state: st.session_state.api_key = "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"

# --- 4. FLUXO NEXUS ---

if st.session_state.etapa == 0:
    st.title("🧠 NEXUS: ESTRATEGISTA DE LIVE & VENDAS")
    st.write("### O único canal: Minicurso Gratuito com Oferta Irresistível na Live.")
    st.session_state.memoria['nicho'] = st.text_input("Defina o Nicho do Evento:", placeholder="Ex: Copywriting para Iniciantes")
    if st.button("INICIAR PLANEJAMENTO"):
        if st.session_state.memoria['nicho']: st.session_state.etapa = 1; st.rerun()

elif st.session_state.etapa == 1:
    st.title("🎯 1. CAPTAÇÃO (ANÚNCIO + PÁGINA + GRUPO)")
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.memoria['data_live'] = st.text_input("Data da Live de Venda:", placeholder="Ex: Quinta, 20h")
    with col2:
        st.session_state.memoria['nome_evento'] = st.text_input("Nome do Minicurso:", value="Minicurso Gratuito")

    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("📈 ANÚNCIO (ADS)"):
            p = f"Gere copy de anúncio para o minicurso {st.session_state.memoria['nome_evento']} no nicho {st.session_state.memoria['nicho']}."
            st.session_state.memoria['txt_ads'] = nexus_ai(p, "Gestor de Tráfego", st.session_state.api_key)
    with c2:
        if st.button("🌐 LANDING PAGE"):
            p = f"Crie Headline e subheadline para a página de inscrição do evento {st.session_state.memoria['nome_evento']}."
            st.session_state.memoria['txt_lp'] = nexus_ai(p, "Copywriter", st.session_state.api_key)
    with c3:
        if st.button("📲 GRUPO WHATSAPP"):
            p = f"Gere a mensagem de boas-vindas do grupo VIP do evento {st.session_state.memoria['nome_evento']}."
            st.session_state.memoria['txt_grupo'] = nexus_ai(p, "Expert em Grupos", st.session_state.api_key)

    if 'txt_ads' in st.session_state.memoria: st.info(st.session_state.memoria['txt_ads'])
    if 'txt_lp' in st.session_state.memoria: st.success(st.session_state.memoria['txt_lp'])
    if 'txt_grupo' in st.session_state.memoria: st.warning(st.session_state.memoria['txt_grupo'])
    st.markdown("</div>", unsafe_allow_html=True)
    if st.button("PREPARAR AQUECIMENTO 👉"): st.session_state.etapa = 2; st.rerun()

elif st.session_state.etapa == 2:
    st.title("🔥 2. AQUECIMENTO & ESTRUTURA")
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    if st.button("GERAR MENSAGENS DE AQUECIMENTO"):
        p = f"Crie 5 mensagens de aquecimento para enviar no grupo antes da live de {st.session_state.memoria['nicho']}."
        st.session_state.memoria['txt_aquecimento'] = nexus_ai(p, "Estrategista", st.session_state.api_key)
    
    if 'txt_aquecimento' in st.session_state.memoria: st.write(st.session_state.memoria['txt_aquecimento'])
    
    st.markdown("---")
    st.subheader("🛠️ Organização do Produto")
    if st.button("COMO ORGANIZAR AULAS E PAGAMENTOS"):
        st.session_state.memoria['checklist'] = """
        **1. Onde cadastrar?** Use Kiwify ou Hotmart. São as mais rápidas para criar o link de pagamento.
        **2. Como entregar?** Se for videoaula, suba na área de membros da plataforma. Se for E-book, suba o PDF lá.
        **3. Aulas Reais:** Não use IA para as aulas. Grave com seu celular, seja você mesmo. A conexão vende mais que a perfeição.
        """
    if 'checklist' in st.session_state.memoria: st.info(st.session_state.memoria['checklist'])
    st.markdown("</div>", unsafe_allow_html=True)
    if st.button("PREPARAR A LIVE (HORA H) 👉"): st.session_state.etapa = 3; st.rerun()

elif st.session_state.etapa == 3:
    st.title("🎤 3. LIVE DE VENDA & ORATÓRIA")
    st.markdown("<div class='live-alert'>FOCO TOTAL: CONTEÚDO + PITCH DE VENDA</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧠 MENTOR DE ORATÓRIA"):
            p = f"Me dê 5 dicas de oratória e postura para uma live de venda de {st.session_state.memoria['nicho']}. Como segurar a audiência e não parecer nervoso."
            st.session_state.memoria['oratoria'] = nexus_ai(p, "Coach de Oratória", st.session_state.api_key)
    with col2:
        if st.button("💰 SCRIPT DO PITCH"):
            p = f"Crie o roteiro da oferta final. Como passar do conteúdo para a venda do curso. Use ancoragem de preço e bônus."
            st.session_state.memoria['pitch'] = nexus_ai(p, "Copywriter Senior", st.session_state.api_key)
    
    if 'oratoria' in st.session_state.memoria: 
        st.markdown("<div class='mentor-box'><b>Dicas de Oratória:</b><br>"+st.session_state.memoria['oratoria']+"</div>", unsafe_allow_html=True)
    if 'pitch' in st.session_state.memoria: 
        st.markdown("### 🎬 Script da Live (O Pitch)")
        st.write(st.session_state.memoria['pitch'])
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("CONCLUIR OPERAÇÃO"):
        st.balloons()
        st.success("Operação Nexus Finalizada com Sucesso!")

if st.session_state.etapa > 0:
    if st.button("⬅ VOLTAR"): st.session_state.etapa -= 1; st.rerun()

st.markdown(f'<div class="footer">NEXUS — ESTRATÉGIA DE LIVE DE ALTA CONVERSÃO</div>', unsafe_allow_html=True)
