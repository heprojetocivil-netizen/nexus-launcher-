import streamlit as st
from groq import Groq
from datetime import datetime

# --- 1. CONFIGURAÇÃO E DESIGN "NEXUS BLACK" ---
st.set_page_config(page_title="NEXUS: DIRETOR DE LANÇAMENTO", page_icon="🚀", layout="wide")

if 'memoria' not in st.session_state: st.session_state.memoria = {}
cor_tema = "#00BFFF" 

st.markdown(f"""
    <style>
    [data-testid="stSidebar"] {{ display: none; }}
    header {{ visibility: hidden; }}
    .stApp {{ background-color: #FFFFFF; color: #000000; padding-bottom: 100px; }}
    h1, h2, h3, h4, p, span, label, .stMarkdown, .stMarkdown p {{ color: #000000 !important; font-family: 'Inter', sans-serif; }}
    .nexus-card {{ background: #F8FAFC !important; border: 2px solid {cor_tema}; padding: 25px; border-radius: 20px; margin-bottom: 20px; box-shadow: 5px 5px 15px rgba(0,0,0,0.05); }}
    .stButton > button {{ background: {cor_tema} !important; color: #FFFFFF !important; padding: 15px 25px !important; font-weight: bold !important; border-radius: 12px !important; width: 100% !important; border: none; }}
    .instruction-box {{ background-color: #E0F7FA; border-left: 5px solid {cor_tema}; padding: 15px; border-radius: 8px; margin: 10px 0; font-size: 0.95em; }}
    .step-label {{ background: {cor_tema}; color: white; padding: 5px 15px; border-radius: 50px; font-size: 0.8em; font-weight: bold; margin-bottom: 10px; display: inline-block; }}
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
    except Exception as e: return f"Erro na conexão: {str(e)}"

# --- 3. ESTADO ---
if 'etapa' not in st.session_state: st.session_state.etapa = 0
api_key = "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"

# --- 4. FLUXO NEXUS ---

if st.session_state.etapa == 0:
    st.title("🧠 NEXUS: ESTRATEGISTA DE VENDAS")
    st.write("### O Caminho: E-book → Anúncio → Grupo → Live de Venda")
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.memoria['nicho'] = st.text_input("Qual o nicho do seu produto?", placeholder="Ex: Marketing de Afiliados")
    with col2:
        st.session_state.memoria['data_live'] = st.date_input("Data da sua Live de Venda:")
    
    if st.button("ATIVAR PROTOCOLO DE LANÇAMENTO"):
        if st.session_state.memoria['nicho']: st.session_state.etapa = 1; st.rerun()

elif st.session_state.etapa == 1:
    st.title("📄 ETAPA 1: O PRODUTO (60 CARTÕES)")
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    if st.button("💎 GERAR CONTEÚDO DO E-BOOK"):
        p = f"Crie um roteiro de 60 lições/cartões para um E-book sobre {st.session_state.memoria['nicho']}. Esse será o produto vendido na live."
        st.session_state.memoria['ebook_60'] = nexus_ai(p, "Escritor de Infoprodutos", api_key)
    
    if 'ebook_60' in st.session_state.memoria:
        st.write(st.session_state.memoria['ebook_60'])
        st.info("💡 **DICA:** Cadastre esse PDF na Monetizze agora e pegue seu link de vendas!")
    st.markdown("</div>", unsafe_allow_html=True)
    if st.button("PROXIMO: ATRAÇÃO 👉"): st.session_state.etapa = 2; st.rerun()

elif st.session_state.etapa == 2:
    st.title("📢 ETAPA 2: ANÚNCIO E LANDING PAGE")
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    if st.button("🎬 GERAR ROTEIRO DO VÍDEO (1 MIN)"):
        p = f"Crie um roteiro de 60s para anúncio em vídeo. Convite direto para a live de {st.session_state.memoria['nicho']} no dia {st.session_state.memoria['data_live']}."
        st.session_state.memoria['script_ads'] = nexus_ai(p, "Diretor de Criativos", api_key)
    if 'script_ads' in st.session_state.memoria: st.info(st.session_state.memoria['script_ads'])
    st.markdown("</div>", unsafe_allow_html=True)
    if st.button("PROXIMO: WHATSAPP 👉"): st.session_state.etapa = 3; st.rerun()

elif st.session_state.etapa == 3:
    st.title("📲 ETAPA 3: GRUPO E CRONOGRAMA")
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    if st.button("📅 GERAR MENSAGENS DO GRUPO"):
        p = f"Crie a descrição do grupo e as mensagens de aquecimento para o nicho {st.session_state.memoria['nicho']}."
        st.session_state.memoria['whats_txt'] = nexus_ai(p, "Expert WhatsApp", api_key)
    if 'whats_txt' in st.session_state.memoria: st.write(st.session_state.memoria['whats_txt'])
    st.markdown("</div>", unsafe_allow_html=True)
    if st.button("PROXIMO: ROTEIRO DA LIVE 👉"): st.session_state.etapa = 4; st.rerun()

elif st.session_state.etapa == 4:
    st.title("🔴 ETAPA 4: O SCRIPT DA LIVE (PALAVRA POR PALAVRA)")
    st.markdown("<div class='instruction-box'><b>IMPORTANTE:</b> Este é o roteiro completo para você ler ou seguir durante a live de venda.</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🎤 SCRIPT DA LIVE"):
            p = f"Crie um roteiro completo de live para o nicho {st.session_state.memoria['nicho']}. Comece com 'Olá pessoal, eu sou [Seu Nome]...'. Inclua introdução, a promessa do que vai ensinar, o conteúdo e o fechamento vendendo o E-book com link na descrição."
            st.session_state.memoria['live_script'] = nexus_ai(p, "Estrategista de Vendas ao Vivo", api_key)
    with col2:
        if st.button("🧠 MENTORIA DE ORATÓRIA"):
            p = f"Dê dicas de postura, tom de voz e como agir durante a live de {st.session_state.memoria['nicho']}."
            st.session_state.memoria['oratoria'] = nexus_ai(p, "Mentor de Oratória", api_key)
    with col3:
        if st.button("📝 DESCRIÇÃO DO VÍDEO"):
            p = f"Crie a copy para a descrição do vídeo da live, com chamadas para o link da Monetizze."
            st.session_state.memoria['desc_video'] = nexus_ai(p, "Copywriter", api_key)

    if 'live_script' in st.session_state.memoria:
        st.markdown("### 🎬 Roteiro Falado (Script)")
        st.write(st.session_state.memoria['live_script'])
    if 'oratoria' in st.session_state.memoria: st.info(st.session_state.memoria['oratoria'])
    if 'desc_video' in st.session_state.memoria: st.success(st.session_state.memoria['desc_video'])
    
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("FINALIZAR LANÇAMENTO"):
        st.balloons()
        st.success("Tudo pronto, Orlando! Agora é só seguir o roteiro e vender!")

if st.session_state.etapa > 0:
    if st.button("⬅ VOLTAR"): st.session_state.etapa -= 1; st.rerun()

st.markdown(f'<div class="footer">NEXUS — DO ANÚNCIO AO SCRIPT FINAL DA LIVE</div>', unsafe_allow_html=True)
