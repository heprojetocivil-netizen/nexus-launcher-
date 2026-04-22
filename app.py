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
    st.session_state.memoria['nicho'] = st.text_input("Qual o seu Nicho?", placeholder="Ex: Emagrecimento, Marketing, etc.")
    if st.button("INICIAR ESTRATÉGIA"):
        if st.session_state.memoria['nicho']: st.session_state.etapa = 1; st.rerun()

elif st.session_state.etapa == 1:
    st.title("📢 1. ANÚNCIO EM VÍDEO & LANDING PAGE")
    st.markdown("<div class='instruction-box'><b>ORIENTAÇÃO:</b> O anúncio deve ser você falando. O lead clica e cai na Landing Page para entrar no Grupo.</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🎬 GERAR SCRIPT DO VÍDEO"):
            p = f"Crie um roteiro detalhado para um anúncio em vídeo de 60s convidando para um minicurso de {st.session_state.memoria['nicho']}. Inclua orientações de cenário e tom de voz."
            st.session_state.memoria['script_video'] = nexus_ai(p, "Diretor de Criativos", api_key)
    with c2:
        if st.button("🌐 ESTRUTURA DA LANDING PAGE"):
            p = f"Crie todos os textos para a Landing Page do evento no nicho {st.session_state.memoria['nicho']}: Headline, Promessa, 3 Benefícios e texto do botão para o Grupo WhatsApp."
            st.session_state.memoria['txt_lp'] = nexus_ai(p, "Copywriter Senior", api_key)

    if 'script_video' in st.session_state.memoria:
        st.markdown("### 🎥 Script para Gravação")
        st.info(st.session_state.memoria['script_video'])
    if 'txt_lp' in st.session_state.memoria:
        st.markdown("### 🌐 Conteúdo da Landing Page")
        st.success(st.session_state.memoria['txt_lp'])
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("CONFIGURAR COMANDO DO GRUPO 👉"): st.session_state.etapa = 2; st.rerun()

elif st.session_state.etapa == 2:
    st.title("📲 2. COMANDO DO GRUPO (WHATSAPP)")
    st.markdown("<div class='instruction-box'><b>OBJETIVO:</b> Definir a cara do grupo e o que será falado nele.</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    if st.button("GERAR DESCRIÇÃO E MENSAGENS DO GRUPO"):
        p = f"Gere: 1) Descrição do Grupo VIP de {st.session_state.memoria['nicho']}. 2) Mensagem de Boas-vindas imediata. 3) 3 Mensagens de aquecimento (Dia 1, Dia 2 e Dia da Live)."
        st.session_state.memoria['txt_grupo_completo'] = nexus_ai(p, "Expert em WhatsApp", api_key)
    
    if 'txt_grupo_completo' in st.session_state.memoria:
        st.markdown("### 📝 Textos para o WhatsApp")
        st.write(st.session_state.memoria['txt_grupo_completo'])
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("PREPARAR A LIVE DE VENDA 👉"): st.session_state.etapa = 3; st.rerun()

elif st.session_state.etapa == 3:
    st.title("🎤 3. LIVE DE VENDA & ORATÓRIA")
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧠 ORIENTAÇÃO DE ORATÓRIA"):
            p = f"Dê orientações práticas de como se comportar na live de {st.session_state.memoria['nicho']}. Fale sobre como lidar com o chat e manter a energia alta."
            st.session_state.memoria['oratoria'] = nexus_ai(p, "Coach de Oratória", api_key)
    with col2:
        if st.button("💰 SCRIPT DA VENDA"):
            p = f"Crie o roteiro do fechamento da live (O Pitch). Como oferecer o curso e onde o link de pagamento deve ser enviado."
            st.session_state.memoria['pitch'] = nexus_ai(p, "Especialista em Vendas", api_key)
    
    if 'oratoria' in st.session_state.memoria: st.info(st.session_state.memoria['oratoria'])
    if 'pitch' in st.session_state.memoria: st.success(st.session_state.memoria['pitch'])
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("FINALIZAR E EXECUTAR"):
        st.balloons()
        st.success("Tudo pronto! Siga o roteiro e boas vendas.")

if st.session_state.etapa > 0:
    if st.button("⬅ VOLTAR"): st.session_state.etapa -= 1; st.rerun()

st.markdown(f'<div class="footer">NEXUS — O CAMINHO MAIS CURTO ENTRE O ANÚNCIO E O PIX</div>', unsafe_allow_html=True)
