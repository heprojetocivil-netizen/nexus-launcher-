import streamlit as st
from groq import Groq
import time
from datetime import datetime

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
        background: #F0F2F6 !important;
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
        border: 1px solid #FF0000;
        color: #CC0000;
        padding: 15px;
        border-radius: 10px;
        font-weight: bold;
        text-align: center;
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
if 'api_key' not in st.session_state: st.session_state.api_key = "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"

# --- 4. FLUXO NEXUS ---

if st.session_state.etapa == 0:
    st.title("🧠 NEXUS: MENTOR DE LANÇAMENTO AO VIVO")
    st.write("### Prepare seu Minicurso, sua Live e sua Venda.")
    st.session_state.memoria['nicho'] = st.text_input("Qual o seu Nicho?", placeholder="Ex: Marketing para Dentistas")
    if st.button("INICIAR ESTRATÉGIA"):
        if st.session_state.memoria['nicho']: st.session_state.etapa = 1; st.rerun()

elif st.session_state.etapa == 1:
    st.title("🎯 1. ATRAÇÃO E CAPTAÇÃO")
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.memoria['data_live'] = st.text_input("Data e Hora da Live:", placeholder="Ex: 15/05 às 20h")
    with col2:
        st.session_state.memoria['link_grupo'] = st.text_input("Link do Grupo WhatsApp:", placeholder="Cole o link aqui")

    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("📈 CRIAR ANÚNCIO"):
            p = f"Crie um anúncio focado em convite para o Minicurso no nicho {st.session_state.memoria['nicho']}. Foque em dor e na solução que será dada na Live do dia {st.session_state.memoria['data_live']}."
            st.session_state.memoria['txt_ads'] = nexus_ai(p, "Gestor de Tráfego", st.session_state.api_key)
    with c2:
        if st.button("🌐 COPY LANDING PAGE"):
            p = f"Crie a copy para uma Landing Page de inscrição. Deve conter: Headline forte, o que a pessoa vai aprender e botão para entrar no Grupo VIP."
            st.session_state.memoria['txt_lp'] = nexus_ai(p, "Copywriter", st.session_state.api_key)
    with c3:
        if st.button("📲 MENSAGEM DO GRUPO"):
            p = f"Crie a mensagem de boas-vindas do Grupo de WhatsApp e a regra do grupo para o evento no nicho {st.session_state.memoria['nicho']}."
            st.session_state.memoria['txt_grupo'] = nexus_ai(p, "Social Manager", st.session_state.api_key)

    if 'txt_ads' in st.session_state.memoria: st.info(st.session_state.memoria['txt_ads'])
    if 'txt_lp' in st.session_state.memoria: st.success(st.session_state.memoria['txt_lp'])
    if 'txt_grupo' in st.session_state.memoria: st.warning(st.session_state.memoria['txt_grupo'])
    st.markdown("</div>", unsafe_allow_html=True)
    if st.button("CONFIGURAR AQUECIMENTO 👉"): st.session_state.etapa = 2; st.rerun()

elif st.session_state.etapa == 2:
    st.title("🔥 2. AQUECIMENTO E PRODUTO")
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    st.subheader("Sequência de Mensagens para o Grupo")
    if st.button("GERAR MENSAGENS DE AQUECIMENTO (7 DIAS)"):
        p = f"Gere 7 mensagens curtas para enviar no grupo de WhatsApp antes da live de {st.session_state.memoria['nicho']}. Devem gerar curiosidade e antecipação."
        st.session_state.memoria['txt_aquecimento'] = nexus_ai(p, "Estrategista", st.session_state.api_key)
    
    if 'txt_aquecimento' in st.session_state.memoria: st.write(st.session_state.memoria['txt_aquecimento'])
    
    st.markdown("---")
    st.subheader("Criação do Produto (Videoaulas ou E-book)")
    if st.button("ONDE CADASTRAR E COMO ORGANIZAR"):
        st.session_state.memoria['plataformas'] = """
        ### 🚀 Onde hospedar seu conhecimento:
        1. **Kiwify ou Hotmart:** Melhores para videoaulas e E-books. Simples de configurar e já processam o pagamento.
        2. **YouTube (Não listado):** Se for fazer o minicurso gratuito, suba as aulas lá e envie o link no grupo.
        3. **Google Drive:** Apenas para entrega imediata de PDFs simples (não recomendado para venda).
        
        **Dica de Gravação:** Não use robôs. Use seu celular, boa iluminação e foque na clareza.
        """
    if 'plataformas' in st.session_state.memoria: st.info(st.session_state.memoria['plataformas'])
    st.markdown("</div>", unsafe_allow_html=True)
    if st.button("PREPARAR A LIVE DE VENDA 👉"): st.session_state.etapa = 3; st.rerun()

elif st.session_state.etapa == 3:
    st.title("🔴 3. A LIVE E ORATÓRIA")
    st.markdown("<div class='live-alert'>TUDO DEPENDE DESTE MOMENTO</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎤 MENTOR DE ORATÓRIA"):
            p = f"Dê 5 dicas de oratória para quem vai vender um curso de {st.session_state.memoria['nicho']} ao vivo. Foque em postura, tom de voz e como vencer o nervosismo."
            st.session_state.memoria['oratoria'] = nexus_ai(p, "Coach de Oratória", st.session_state.api_key)
    with col2:
        if st.button("💰 SCRIPT DE VENDA (PITCH)"):
            p = f"Crie o roteiro final da live. Como sair do conteúdo e entrar na oferta do curso. Use gatilhos de escassez e urgência."
            st.session_state.memoria['pitch'] = nexus_ai(p, "Copywriter Senior", st.session_state.api_key)
    
    if 'oratoria' in st.session_state.memoria: 
        st.markdown("<div class='mentor-box'><b>Dicas de Oratória:</b><br>"+st.session_state.memoria['oratoria']+"</div>", unsafe_allow_html=True)
    if 'pitch' in st.session_state.memoria: 
        st.markdown("### 🎬 Script da Live")
        st.write(st.session_state.memoria['pitch'])
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("FINALIZAR OPERAÇÃO"):
        st.balloons()
        st.success("Operação Nexus concluída. Agora a execução é com você!")

if st.session_state.etapa > 0:
    if st.button("⬅ VOLTAR"): st.session_state.etapa -= 1; st.rerun()

st.markdown(f'<div class="footer">NEXUS — LANÇAMENTO AO VIVO E AUTORIDADE REAL</div>', unsafe_allow_html=True)
