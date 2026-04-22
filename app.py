import streamlit as st
from groq import Groq
import time
from datetime import datetime

# --- 1. CONFIGURAÇÃO E DESIGN "NEXUS" ---
st.set_page_config(page_title="NEXUS LAUNCHER", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    [data-testid="stSidebar"] { display: none; }
    header { visibility: hidden; }
    .stApp { background-color: #FFFFFF; color: #000000; padding-bottom: 100px; }
    h1, h2, h3, h4, p, span, label, .stMarkdown { color: #000000 !important; font-family: 'Inter', sans-serif; }
    .stProgress > div > div > div > div { background-color: #00BFFF; }

    .nexus-card, .stTabs [data-baseweb="tab-panel"] {
        background: #F0F2F6 !important;
        border: 1px solid #D1D5DB;
        padding: 30px;
        border-radius: 20px;
        margin-bottom: 20px;
        color: #000000 !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    
    .stTabs [data-baseweb="tab-list"] { background-color: #F0F2F6 !important; border-radius: 10px 10px 0 0; }
    .stTabs [data-baseweb="tab"] { color: #000000 !important; font-weight: bold; }

    .stButton > button {
        background: #00BFFF !important;
        color: #000000 !important;
        border: none !important;
        padding: 15px 30px !important;
        font-size: 16px !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        width: 100% !important;
        transition: all 0.3s ease;
        text-transform: uppercase;
    }
    
    .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0, 191, 255, 0.3); }

    .home-btn-container .stButton > button {
        background: #E5E7EB !important;
        color: #000000 !important;
        padding: 10px !important;
        font-size: 12px !important;
    }

    textarea { border: 1px solid #00BFFF !important; border-radius: 15px !important; }

    .badge-recompensa {
        background: rgba(0, 191, 255, 0.1);
        color: #0080FF;
        padding: 8px 20px;
        border-radius: 20px;
        font-size: 14px;
        border: 1px solid #00BFFF;
        font-weight: bold;
        display: inline-block;
    }

    .chat-bubble-user { background: #E0F7FA; padding: 15px; border-radius: 15px; margin-bottom: 10px; border-left: 5px solid #00BFFF; color: #000; }
    .chat-bubble-ai { background: #F0F2F6; padding: 15px; border-radius: 15px; margin-bottom: 10px; border-left: 5px solid #333; color: #000; }

    .ai-tool-box {
        background: #E0F7FA;
        border-left: 5px solid #00BFFF;
        padding: 15px;
        border-radius: 10px;
        margin-top: 15px;
        text-align: left;
    }

    .price-tip {
        background: #FFF9C4;
        border-left: 5px solid #FBC02D;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
        color: #000000;
        font-size: 14px;
    }

    .tool-link {
        display: inline-block;
        background: #000000;
        color: #FFFFFF !important;
        padding: 5px 12px;
        border-radius: 6px;
        text-decoration: none;
        font-weight: bold;
        font-size: 11px;
        margin: 5px 2px;
    }

    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #00BFFF;
        color: #000000;
        text-align: center;
        padding: 15px;
        font-weight: bold;
        z-index: 1000;
        border-top: 2px solid #0080FF;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LÓGICA DE INTELIGÊNCIA ---
def nexus_ai(prompt, system_role, api_key, history=None):
    try:
        client = Groq(api_key=api_key)
        messages = [{"role": "system", "content": system_role}]
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": prompt})
        
        completion = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Erro na conexão Nexus: {str(e)}"

# --- 3. CONTROLE DE ESTADO ---
if 'etapa' not in st.session_state: st.session_state.etapa = -1 
if 'memoria' not in st.session_state: st.session_state.memoria = {}
if 'nome_user' not in st.session_state: st.session_state.nome_user = ""
if 'api_key' not in st.session_state: st.session_state.api_key = "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"
if 'meus_produtos' not in st.session_state: st.session_state.meus_produtos = []
if 'chat_history' not in st.session_state: st.session_state.chat_history = []
if 'chat_cronograma' not in st.session_state: st.session_state.chat_cronograma = []

def salvar_progresso(status="Em rascunho"):
    nome_prod = st.session_state.memoria.get('nome_produto', 'Produto Sem Nome')
    st.session_state.meus_produtos = [p for p in st.session_state.meus_produtos if p['nome'] != nome_prod]
    st.session_state.meus_produtos.append({
        "nome": nome_prod,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "status": status,
        "etapa_salva": st.session_state.etapa,
        "conteudo": st.session_state.memoria.copy()
    })

def ir_para_home():
    if st.session_state.etapa > 0: salvar_progresso("Pausado")
    st.session_state.etapa = 0
    st.rerun()

def voltar_etapa():
    if st.session_state.etapa > 1: st.session_state.etapa -= 1; st.rerun()

def iniciar_nova_operacao():
    st.session_state.memoria = {}; st.session_state.etapa = 1; st.session_state.chat_history = []; st.session_state.chat_cronograma = []; st.rerun()

# --- RODAPÉ ---
st.markdown("""
    <div class="footer">
        Acesse <a href="http://www.quizmaispremios.com.br" style="color: #000; text-decoration: underline;">www.quizmaispremios.com.br</a> 
        e venha se divertir com a gente e ganhar muitos prêmios!
    </div>
    """, unsafe_allow_html=True)

# --- 4. TELA DE IDENTIFICAÇÃO ---
if st.session_state.etapa == -1:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div class='nexus-card' style='text-align:center;'>", unsafe_allow_html=True)
        st.title("Nexus Launcher")
        st.write("### Ativação de Sistema")
        nome = st.text_input("👤 Nome do Estrategista:")
        chave_input = st.text_input("🔑 Chave Groq API:", type="password", value=st.session_state.api_key)
        st.markdown("<a href='https://console.groq.com/keys' target='_blank' class='tool-link'>Obter chave Groq grátis</a>", unsafe_allow_html=True)
        if st.button("ATIVAR NEXUS"):
            if nome and chave_input:
                st.session_state.nome_user, st.session_state.api_key = nome, chave_input
                st.session_state.etapa = 0; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# --- 5. CABEÇALHO E FLUXO ---
else:
    col_status_1, col_status_2 = st.columns([3, 1])
    with col_status_1: st.progress(max(0, st.session_state.etapa) / 7)
    with col_status_2: st.markdown(f"<div class='badge-recompensa'>Fase {st.session_state.etapa} de 7</div>", unsafe_allow_html=True)
    st.markdown("---")

    if st.session_state.etapa != 0:
        st.markdown("<div class='home-btn-container'>", unsafe_allow_html=True)
        c_nav1, c_nav2, c_nav3 = st.columns(3)
        with c_nav1: 
            if st.button("⬅ VOLTAR"): voltar_etapa()
        with c_nav2:
            if st.button("➕ NOVO PROJETO"): iniciar_nova_operacao()
        with c_nav3:
            if st.button("🏠 DASHBOARD"): ir_para_home()
        st.markdown("</div>", unsafe_allow_html=True)

    # --- ETAPA 0: DASHBOARD ---
    if st.session_state.etapa == 0:
        st.title(f"🚀 Dashboard, {st.session_state.nome_user}")
        tab_new, tab_list = st.tabs(["CRIAR NOVO", "MEUS PROJETOS"])
        with tab_new:
            if st.button("INICIAR CRIAÇÃO DE PRODUTO"): iniciar_nova_operacao()
        with tab_list:
            if not st.session_state.meus_produtos: st.write("Nenhum projeto salvo.")
            for i, p in enumerate(st.session_state.meus_produtos):
                col_p1, col_p2 = st.columns([4, 1])
                with col_p1:
                    if st.button(f"Retomar: {p['nome']} ({p['status']})", key=f"retomar_{i}"):
                        st.session_state.memoria = p['conteudo']; st.session_state.etapa = p['etapa_salva']; st.rerun()
                with col_p2:
                    if st.button(f"🗑️ EXCLUIR", key=f"del_{i}"):
                        st.session_state.meus_produtos.pop(i); st.rerun()

    # --- ETAPA 1: NICHO ---
    elif st.session_state.etapa == 1:
        st.title("🎯 1. DEFINIÇÃO DO NICHO")
        st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
        p_nicho = st.text_input("Qual o nicho de mercado que você quer atuar?", value=st.session_state.memoria.get('nicho', ''))
        p_ganho = st.selectbox("Expectativa de faturamento com este nicho:", ["R$ 5k", "R$ 20k", "R$ 50k+"])
        if st.button("DEFINIR NICHO E AVANÇAR"):
            with st.spinner("Analisando nicho..."):
                sys = "Você é um analista de mercado digital. Defina o público-alvo ideal e as maiores dores desse nicho."
                st.session_state.memoria['etapa1'] = nexus_ai(f"Nicho: {p_nicho}, Meta: {p_ganho}", sys, st.session_state.api_key)
                st.session_state.memoria['nicho'] = p_nicho
                st.session_state.etapa = 2; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # --- ETAPA 2: CANAL DE AUDIÊNCIA ---
    elif st.session_state.etapa == 2:
        st.title("👥 2. CANAL DE AUDIÊNCIA")
        st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
        st.write(f"Nicho: **{st.session_state.memoria.get('nicho')}**")
        canal = st.radio("Escolha o canal principal para gerar sua audiência:", 
                         ["WhatsApp", "YouTube", "Facebook", "E-mail Marketing"])
        st.session_state.memoria['canal_escolhido'] = canal
        
        if st.button("GERAR ESTRATÉGIA DE CANAL"):
            with st.spinner("Criando estratégia..."):
                sys_canal = f"Você é um especialista em tráfego e engajamento no {canal}."
                prompt_canal = f"Para o nicho {st.session_state.memoria.get('nicho')}, gere 3 ideias de conteúdo de atração e uma dica prática de como levar essa audiência para o canal {canal}."
                st.session_state.memoria['estratégia_canal'] = nexus_ai(prompt_canal, sys_canal, st.session_state.api_key)
                st.rerun()
        
        if 'estratégia_canal' in st.session_state.memoria:
            st.markdown(st.session_state.memoria['estratégia_canal'])
            if st.button("AVANÇAR PARA O PRODUTO 👉"):
                st.session_state.etapa = 3; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # --- ETAPA 3: NOME E CRIAÇÃO DO PRODUTO ---
    elif st.session_state.etapa == 3:
        st.title("🧩 3. NOME E CRIAÇÃO DO PRODUTO")
        st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
        p_nome = st.text_input("Qual será o nome do seu produto?", value=st.session_state.memoria.get('nome_produto', ''))
        st.session_state.memoria['nome_produto'] = p_nome
        
        tab_eb, tab_heygen = st.tabs(["📄 E-BOOK (60 CARTÕES)", "🎥 VIDEO AULAS (HEYGEN PRO)"])
        
        with tab_eb:
            if st.button("GERAR CONTEÚDO DO E-BOOK"):
                prompt_ebook = (f"Crie o conteúdo para o produto '{p_nome}' no nicho {st.session_state.memoria.get('nicho')} "
                                f"dividido em 60 cartões numerados para o Gamma.app.")
                st.session_state.memoria['ebook_content'] = nexus_ai(prompt_ebook, "Escritor de infoprodutos.", st.session_state.api_key)
            st.text_area("Cópia para Gamma.app:", value=st.session_state.memoria.get('ebook_content', ''), height=200)
            
        with tab_heygen:
            if st.button("GERAR ROTEIROS DE VIDEOAULAS"):
                prompt_heygen = f"Crie 6 roteiros de aulas para o produto '{p_nome}' para usar com avatares HeyGen."
                st.session_state.memoria['heygen_scripts'] = nexus_ai(prompt_heygen, "Roteirista HeyGen.", st.session_state.api_key)
            st.text_area("Scripts das Aulas:", value=st.session_state.memoria.get('heygen_scripts', ''), height=200)

        if st.button("PRODUTO DEFINIDO 👉"):
            st.session_state.etapa = 4; salvar_progresso(); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # --- ETAPA 4: ARSENAL DE VENDAS (UPGRADE) ---
    elif st.session_state.etapa == 4:
        st.title("📢 4. ARSENAL DE VENDAS E CONVERSÃO")
        canal = st.session_state.memoria.get('canal_escolhido')
        nicho = st.session_state.memoria.get('nicho')
        produto = st.session_state.memoria.get('nome_produto')
        
        st.subheader(f"Estratégia de Conversão: {canal}")
        
        if canal == "WhatsApp":
            if st.button("GERAR SEQUÊNCIA DE 5 MENSAGENS PERSUASIVAS"):
                sys_zap = "Especialista em fechamento no WhatsApp."
                prompt_zap = (f"Crie uma sequência de 5 mensagens para o nicho {nicho}. "
                              f"Mensagem 1: Curiosidade. Mensagem 2: Conexão. Mensagem 3: Prova/Dica. "
                              f"Mensagem 4: Oferta do produto {produto}. Mensagem 5: Escassez e Quebra de Objeções. "
                              f"Intercale dicas com a oferta de forma natural.")
                st.session_state.memoria['zap_arsenal'] = nexus_ai(prompt_zap, sys_zap, st.session_state.api_key)
            st.markdown(st.session_state.memoria.get('zap_arsenal', 'Aguardando geração...'))
            
        elif canal == "E-mail Marketing":
            if st.button("GERAR FUNIL DE E-MAIL MARKETING"):
                st.session_state.memoria['email_arsenal'] = nexus_ai(f"Crie um funil de 5 emails para vender {produto}.", "Especialista em Copy de Email.", st.session_state.api_key)
            st.markdown(st.session_state.memoria.get('email_arsenal', ''))

        elif canal == "YouTube":
            if st.button("GERAR ESTRATÉGIA DE VÍDEO NO YOUTUBE"):
                st.session_state.memoria['yt_arsenal'] = nexus_ai(f"Crie um roteiro de vídeo de conteúdo + CTA para {produto}.", "Especialista em YouTube Ads.", st.session_state.api_key)
            st.markdown(st.session_state.memoria.get('yt_arsenal', ''))

        elif canal == "Facebook":
            if st.button("GERAR ESTRATÉGIA DE GRUPOS/ANÚNCIOS FACEBOOK"):
                st.session_state.memoria['fb_arsenal'] = nexus_ai(f"Crie posts engajadores para grupos de Facebook sobre {nicho} vendendo {produto}.", "Gestor de Comunidade Facebook.", st.session_state.api_key)
            st.markdown(st.session_state.memoria.get('fb_arsenal', ''))

        if st.button("AVANÇAR PARA O LANÇAMENTO 👉"):
            st.session_state.etapa = 5; salvar_progresso(); st.rerun()

    # --- ETAPA 5: CRONOGRAMA ---
    elif st.session_state.etapa == 5:
        st.title("📅 5. CRONOGRAMA MESTRE (15 DIAS)")
        st.markdown("<div class='price-tip'>Siga este cronograma para garantir o aquecimento e a conversão máxima do seu lançamento.</div>", unsafe_allow_html=True)
        
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.subheader("🔥 FASE 1: ATRAÇÃO")
            st.checkbox("Dia 1-5: Gerar curiosidade no canal escolhido.")
            st.checkbox("Dia 6-10: Entregar as dicas e intercalar mensagens.")
        with col_c2:
            st.subheader("💰 FASE 2: OFERTA")
            st.checkbox("Dia 11: Abertura oficial do carrinho.")
            st.checkbox("Dia 15: Fechamento com escassez.")

        if st.button("FINALIZAR OPERAÇÃO"):
            st.session_state.etapa = 6; st.rerun()

    # --- ETAPA 6: CONCLUÍDO ---
    elif st.session_state.etapa == 6:
        st.title("🏆 OPERAÇÃO FINALIZADA!")
        st.balloons()
        st.markdown("<div class='nexus-card' style='background: #D1FFD1 !important; text-align:center;'>", unsafe_allow_html=True)
        st.write("### Sucesso! Seu sistema de vendas está pronto.")
        if st.button("ACESSAR SUPORTE E CHAT DE ANÁLISE 👉"):
            st.session_state.etapa = 7; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # --- ETAPA 7: SUPORTE ---
    elif st.session_state.etapa == 7:
        st.title("🎧 7. SUPORTE E ANÁLISE")
        for msg in st.session_state.chat_history:
            div = "chat-bubble-user" if msg["role"] == "user" else "chat-bubble-ai"
            st.markdown(f"<div class='{div}'>{msg['content']}</div>", unsafe_allow_html=True)

        with st.form("chat_nexus", clear_on_submit=True):
            user_input = st.text_input("Sua dúvida geral ➔")
            if st.form_submit_button("ENVIAR ➔"):
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                sys_role = f"Você é o consultor da Nexus Launcher. Ajude o {st.session_state.nome_user}."
                resp = nexus_ai(user_input, sys_role, st.session_state.api_key, history=st.session_state.chat_history[:-1])
                st.session_state.chat_history.append({"role": "assistant", "content": resp})
                st.rerun()
