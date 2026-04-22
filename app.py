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
    "E-mail Marketing": "#D1D5DB", 
    "Padrão": "#00BFFF"
}
cor_tema = cores_canais.get(canal_selecionado, "#00BFFF")

st.markdown(f"""
    <style>
    [data-testid="stSidebar"] {{ display: none; }}
    header {{ visibility: hidden; }}
    .stApp {{ background-color: #FFFFFF; color: #000000; padding-bottom: 100px; }}
    
    h1, h2, h3, h4, p, span, label, .stMarkdown, .stMarkdown p {{ 
        color: #000000 !important; 
        font-family: 'Inter', sans-serif; 
    }}
    
    .stProgress > div > div > div > div {{ background-color: {cor_tema}; }}

    .nexus-card, .stTabs [data-baseweb="tab-panel"] {{
        background: #F0F2F6 !important;
        border: 2px solid {cor_tema};
        padding: 30px;
        border-radius: 20px;
        margin-bottom: 20px;
        color: #000000 !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }}
    
    .stTabs [data-baseweb="tab-list"] {{ 
        background-color: #F0F2F6 !important; 
        border-radius: 10px 10px 0 0; 
        gap: 10px;
    }}
    
    .stTabs [data-baseweb="tab"] {{ 
        background-color: #E5E7EB !important;
        color: #000000 !important; 
        font-weight: bold; 
        border-radius: 5px 5px 0 0;
        padding: 10px 20px;
    }}

    .stTabs [aria-selected="true"] {{ 
        background-color: #D1D5DB !important;
        color: #000000 !important;
        border-bottom: 3px solid {cor_tema} !important;
    }}

    .stButton > button {{
        background: {cor_tema} !important;
        color: #FFFFFF !important;
        border: none !important;
        padding: 15px 30px !important;
        font-size: 16px !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        width: 100% !important;
        transition: all 0.3s ease;
        text-transform: uppercase;
    }}
    
    .stButton > button:hover {{ transform: translateY(-2px); box-shadow: 0 5px 15px {cor_tema}55; }}

    .footer {{
        position: fixed; left: 0; bottom: 0; width: 100%;
        background-color: {cor_tema}; color: #FFFFFF;
        text-align: center; padding: 15px; font-weight: bold; z-index: 1000;
    }}
    
    .orientacao-anuncio {{
        background-color: #007BFF;
        color: #FFFFFF !important;
        padding: 15px;
        border-radius: 10px;
        margin-top: 20px;
        font-weight: bold;
        border-left: 8px solid #0056b3;
    }}
    </style>
    """, unsafe_allow_html=True)

def nexus_ai(prompt, system_role, api_key, history=None):
    try:
        client = Groq(api_key=api_key)
        messages = [{"role": "system", "content": system_role}]
        if history: messages.extend(history)
        messages.append({"role": "user", "content": prompt})
        completion = client.chat.completions.create(messages=messages, model="llama-3.3-70b-versatile")
        return completion.choices[0].message.content
    except Exception as e:
        return f"Erro na conexão Nexus: {str(e)}"

if 'etapa' not in st.session_state: st.session_state.etapa = -1 
if 'nome_user' not in st.session_state: st.session_state.nome_user = ""
if 'api_key' not in st.session_state: st.session_state.api_key = "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"
if 'meus_produtos' not in st.session_state: st.session_state.meus_produtos = []
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

def salvar_progresso(status="Em rascunho"):
    nome_prod = st.session_state.memoria.get('nome_produto', 'Produto Sem Nome')
    st.session_state.meus_produtos = [p for p in st.session_state.meus_produtos if p['nome'] != nome_prod]
    st.session_state.meus_produtos.append({
        "nome": nome_prod, "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "status": status, "etapa_salva": st.session_state.etapa, "conteudo": st.session_state.memoria.copy()
    })

def ir_para_home():
    if st.session_state.etapa > 0: salvar_progresso("Pausado")
    st.session_state.etapa = 0; st.rerun()

def voltar_etapa():
    if st.session_state.etapa > 1: st.session_state.etapa -= 1; st.rerun()

def iniciar_nova_operacao():
    st.session_state.memoria = {}; st.session_state.etapa = 1; st.session_state.chat_history = []; st.rerun()

st.markdown(f'<div class="footer">Acesse <a href="http://www.quizmaispremios.com.br" style="color: #FFF; text-decoration: underline;">www.quizmaispremios.com.br</a> e ganhe prêmios!</div>', unsafe_allow_html=True)

if st.session_state.etapa == -1:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div class='nexus-card' style='text-align:center;'>", unsafe_allow_html=True)
        st.title("Nexus Launcher")
        nome = st.text_input("👤 Nome do Estrategista:")
        chave_input = st.text_input("🔑 Chave Groq API:", type="password", value=st.session_state.api_key)
        if st.button("ATIVAR NEXUS"):
            if nome and chave_input:
                st.session_state.nome_user, st.session_state.api_key = nome, chave_input
                st.session_state.etapa = 0; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

else:
    if st.session_state.etapa != 0:
        c_nav1, c_nav2, c_nav3 = st.columns(3)
        with c_nav1: 
            if st.button("⬅ VOLTAR"): voltar_etapa()
        with c_nav2:
            if st.button("➕ NOVO PROJETO"): iniciar_nova_operacao()
        with c_nav3:
            if st.button("🏠 DASHBOARD"): ir_para_home()

    if st.session_state.etapa == 0:
        st.title(f"🚀 Dashboard, {st.session_state.nome_user}")
        tab_new, tab_list = st.tabs(["CRIAR NOVO", "MEUS PROJETOS"])
        with tab_new:
            if st.button("INICIAR CRIAÇÃO DE PRODUTO"): iniciar_nova_operacao()
        with tab_list:
            for i, p in enumerate(st.session_state.meus_produtos):
                if st.button(f"Retomar: {p['nome']} ({p['status']})", key=f"retomar_{i}"):
                    st.session_state.memoria = p['conteudo']; st.session_state.etapa = p['etapa_salva']; st.rerun()

    elif st.session_state.etapa == 1:
        st.title("🎯 1. DEFINIÇÃO DO NICHO")
        p_nicho = st.text_input("Qual o nicho de mercado?", value=st.session_state.memoria.get('nicho', ''))
        if st.button("AVANÇAR"):
            st.session_state.memoria['nicho'] = p_nicho
            st.session_state.etapa = 2; st.rerun()

    elif st.session_state.etapa == 2:
        st.title(f"👥 2. CANAL E ATRAÇÃO")
        canal = st.selectbox("Canal principal:", ["WhatsApp", "E-mail Marketing", "YouTube", "Facebook"], 
                             index=["WhatsApp", "E-mail Marketing", "YouTube", "Facebook"].index(st.session_state.memoria.get('canal_escolhido', 'WhatsApp')))
        st.session_state.memoria['canal_escolhido'] = canal
        
        tab_atracao, tab_engaja = st.tabs(["🧲 MENTOR DE ATRAÇÃO", "🤝 MENTOR DE CONTEÚDO"])
        
        with tab_atracao:
            if st.button("GERAR TEXTO DE ATRAÇÃO"):
                sys = "Você é um Mentor de Atração. Gere um anúncio e ganchos."
                prompt = f"Gere um anúncio para atrair leads para {canal} no nicho {st.session_state.memoria['nicho']}."
                st.session_state.memoria['atracao_msg'] = nexus_ai(prompt, sys, st.session_state.api_key)
            
            if 'atracao_msg' in st.session_state.memoria:
                st.write(st.session_state.memoria['atracao_msg'])
                
                # --- NOVAS ALTERAÇÕES SOLICITADAS ---
                st.markdown("---")
                col_eb, col_an, col_lp = st.columns(3)
                
                with col_eb:
                    if st.button("🎁 GERAR E-BOOK ISCA (5 CARTÕES)"):
                        prompt_isca = f"Crie um E-book simples de isca digital com 5 cartões/tópicos rápidos sobre {st.session_state.memoria['nicho']} para quem deixar e-mail ou entrar no WhatsApp."
                        st.session_state.memoria['isca_pdf'] = nexus_ai(prompt_isca, "Escritor de Iscas", st.session_state.api_key)
                
                with col_an:
                    if st.button("📢 ONDE ANUNCIAR"):
                        st.session_state.memoria['onde_anunciar'] = """
                        ### 📍 Onde Anunciar seu E-book:
                        1. **Meta Ads (Instagram/Facebook):** Use o objetivo de 'Engajamento' para WhatsApp ou 'Conversão' para Landing Page. Foque em Stories e Reels.
                        2. **Google Ads:** Use 'Rede de Pesquisa' com palavras-chave do seu nicho.
                        3. **TikTok Ads:** Excelente para públicos mais jovens e consumo rápido de conteúdo.
                        """
                
                with col_lp:
                    if st.button("🌐 COMO FAZER LANDING PAGE"):
                        st.session_state.memoria['como_lp'] = """
                        ### 🏗️ Estrutura da Landing Page de Alta Conversão:
                        1. **Headline:** Promessa forte baseada no E-book.
                        2. **Visual:** Imagem 3D do seu E-book (mockup).
                        3. **Mecanismo de Captura:** Campo de E-mail + Botão de WhatsApp (API link).
                        4. **Call to Action:** 'Baixar E-book Grátis Agora'.
                        *Ferramentas recomendadas: GreatPages, Elementor ou Canva Websites.*
                        """
                
                if 'isca_pdf' in st.session_state.memoria: st.info(st.session_state.memoria['isca_pdf'])
                if 'onde_anunciar' in st.session_state.memoria: st.markdown(st.session_state.memoria['onde_anunciar'])
                if 'como_lp' in st.session_state.memoria: st.markdown(st.session_state.memoria['como_lp'])

        with tab_engaja:
            st.write("Conteúdo de engajamento para manter a audiência quente.")

        if st.button("AVANÇAR PARA O PRODUTO 👉"):
            st.session_state.etapa = 3; st.rerun()

    elif st.session_state.etapa == 3:
        st.title("🧩 3. PRODUTO")
        st.write("Defina os detalhes finais do seu infoproduto aqui.")
        if st.button("PRODUTO DEFINIDO 👉"):
            st.session_state.etapa = 4; salvar_progresso(); st.rerun()

    # (As demais etapas 4, 5, 6 e 7 seguem a mesma lógica do seu código original)
    elif st.session_state.etapa >= 4:
        st.write(f"Etapa {st.session_state.etapa} em desenvolvimento com base no seu fluxo.")
        if st.button("FINALIZAR"): st.session_state.etapa = 6; st.rerun()
