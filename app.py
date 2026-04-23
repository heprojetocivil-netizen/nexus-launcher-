import streamlit as st
from groq import Groq
from datetime import datetime, timedelta

# --- 1. CONFIGURAÇÃO E DESIGN "NEXUS" ---
st.set_page_config(page_title="NEXUS: DIRETOR DE LANÇAMENTO", page_icon="🧠", layout="wide")

if 'memoria' not in st.session_state: st.session_state.memoria = {}
cor_tema = "#00BFFF" 

st.markdown(f"""
    <style>
    [data-testid="stSidebar"] {{ display: none; }}
    header {{ visibility: hidden; }}
    .stApp {{ background-color: #FFFFFF; color: #000000; padding-bottom: 100px; }}
    h1, h2, h3, h4, p, span, label, .stMarkdown, .stMarkdown p {{ color: #000000 !important; font-family: 'Inter', sans-serif; }}
    .nexus-card {{ background: #F8FAFC !important; border: 2px solid {cor_tema}; padding: 25px; border-radius: 20px; margin-bottom: 20px; }}
    .stButton > button {{ background: {cor_tema} !important; color: #FFFFFF !important; padding: 15px 25px !important; font-weight: bold !important; border-radius: 12px !important; width: 100% !important; text-transform: uppercase; border: none; }}
    .instruction-box {{ background-color: #F1F5F9; border-left: 5px solid {cor_tema}; padding: 15px; border-radius: 8px; margin: 10px 0; font-size: 0.9em; }}
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
    st.title("🧠 NEXUS: SISTEMA DIRETOR DE LANÇAMENTO")
    st.write("### Estratégia: Criação do E-book → Captação → Distribuição → Live de Venda")
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.memoria['nicho'] = st.text_input("Nicho do E-book:", placeholder="Ex: Marketing Digital")
        st.session_state.memoria['data_inicio'] = datetime.now().strftime("%d/%m/%Y")
    with col2:
        st.session_state.memoria['data_live'] = st.date_input("Data da Live de Venda:")
    
    if st.button("INICIAR PRODUÇÃO"):
        if st.session_state.memoria['nicho']: st.session_state.etapa = 1; st.rerun()

elif st.session_state.etapa == 1:
    st.title("📄 1. O PRODUTO E MONETIZZE")
    st.markdown("<div class='instruction-box'><b>Ação:</b> Crie os 60 cartões e cadastre na Monetizze para obter o seu link de vendas.</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    if st.button("🧠 GERAR CONTEÚDO: E-BOOK (60 CARTÕES)"):
        p = f"Crie um roteiro de 60 cartões educativos sobre {st.session_state.memoria['nicho']}. Cada cartão deve ser prático."
        st.session_state.memoria['ebook_60'] = nexus_ai(p, "Escritor de Infoprodutos", api_key)
    
    if 'ebook_60' in st.session_state.memoria:
        st.info(st.session_state.memoria['ebook_60'])
        st.markdown("---")
        st.subheader("🛠️ ORIENTAÇÃO MONETIZZE")
        st.write("1. Cadastre o produto como **E-book (PDF)**.\n2. No checkout, defina o preço.\n3. Copie o **Link da Página de Venda/Checkout** para usar na live.")
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("GERAR ANÚNCIO E PÁGINA 👉"): st.session_state.etapa = 2; st.rerun()

elif st.session_state.etapa == 2:
    st.title("📢 2. ATRAÇÃO E ESTRUTURA")
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🎬 SCRIPT VÍDEO (1 MINUTO)"):
            p = f"Crie um roteiro de 1 minuto para vídeo de anúncio. O produtor deve falar direto para a câmera convidando para a live sobre {st.session_state.memoria['nicho']} no dia {st.session_state.memoria['data_live']}."
            st.session_state.memoria['script_ads'] = nexus_ai(p, "Diretor de Criativos", api_key)
    with c2:
        if st.button("🌐 DADOS DA LANDING PAGE"):
            p = f"Gere Headline, Promessa e o texto completo para a página de inscrição focada em levar o lead para o WhatsApp."
            st.session_state.memoria['copy_lp'] = nexus_ai(p, "Copywriter", api_key)
    
    if 'script_ads' in st.session_state.memoria: st.info(st.session_state.memoria['script_ads'])
    if 'copy_lp' in st.session_state.memoria: st.success(st.session_state.memoria['copy_lp'])
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("DISTRIBUIÇÃO NO WHATSAPP 👉"): st.session_state.etapa = 3; st.rerun()

elif st.session_state.etapa == 3:
    st.title("📲 3. CALENDÁRIO E WHATSAPP")
    st.markdown(f"<div class='instruction-box'><b>Cronograma:</b> De {st.session_state.memoria['data_inicio']} até {st.session_state.memoria['data_live']}.</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    if st.button("📅 GERAR DESCRIÇÃO E MENSAGENS AGENDADAS"):
        p = f"Gere a descrição do grupo VIP e 5 mensagens de aquecimento para serem distribuídas entre hoje e o dia da live ({st.session_state.memoria['data_live']})."
        st.session_state.memoria['whats_cronograma'] = nexus_ai(p, "Estrategista de Grupos", api_key)
    
    if 'whats_cronograma' in st.session_state.memoria:
        st.write(st.session_state.memoria['whats_cronograma'])
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("TREINAMENTO PARA A LIVE 👉"): st.session_state.etapa = 4; st.rerun()

elif st.session_state.etapa == 4:
    st.title("🔴 4. MENTORIA, SCRIPT E DESCRIÇÃO")
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎤 MENTORIA DE ORATÓRIA"):
            p = f"Crie apenas as orientações técnicas de oratória para a live de {st.session_state.memoria['nicho']}. Foque em postura, energia e como olhar para a câmera."
            st.session_state.memoria['mentor_ora'] = nexus_ai(p, "Mentor de Oratória", api_key)
            
    with col2:
        if st.button("🎬 SCRIPT DA LIVE"):
            p = f"Crie o roteiro de fala para a live de {st.session_state.memoria['nicho']}. Deve começar com 'Olá pessoal, eu sou [Seu Nome]...', entregar o conteúdo prometido e, no final, anunciar que o link para a venda do e-book está na descrição."
            st.session_state.memoria['script_live'] = nexus_ai(p, "Estrategista de Vendas", api_key)
            
    with col3:
        if st.button("📝 DESCRIÇÃO + LINK"):
            p = f"Crie apenas a descrição para o vídeo da live de {st.session_state.memoria['nicho']}. Coloque o LINK DE COMPRA em destaque na primeira linha e um resumo persuasivo abaixo."
            st.session_state.memoria['desc_video_final'] = nexus_ai(p, "Copywriter de Vendas", api_key)

    if 'mentor_ora' in st.session_state.memoria: 
        st.subheader("🎤 Mentoria de Oratória")
        st.info(st.session_state.memoria['mentor_ora'])
        
    if 'script_live' in st.session_state.memoria: 
        st.subheader("🎬 Script da Live")
        st.write(st.session_state.memoria['script_live'])
        
    if 'desc_video_final' in st.session_state.memoria: 
        st.subheader("📝 Descrição + Link")
        st.success(st.session_state.memoria['desc_video_final'])
        
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("CONCLUIR LANÇAMENTO"):
        st.balloons()
        st.success("Lançamento Totalmente Estruturado!")

if st.session_state.etapa > 0:
    if st.button("⬅ VOLTAR"): st.session_state.etapa -= 1; st.rerun()

st.markdown(f'<div class="footer">NEXUS — DO ANÚNCIO AO LINK NA DESCRIÇÃO</div>', unsafe_allow_html=True)
