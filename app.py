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
    "E-mail Marketing": "#1F2937",
    "Padrão": "#00BFFF"
}
cor_tema = cores_canais.get(canal_selecionado, "#00BFFF")

st.markdown(f"""
    <style>
    [data-testid="stSidebar"] {{ display: none; }}
    header {{ visibility: hidden; }}
    .stApp {{ background-color: #FFFFFF; color: #000000; padding-bottom: 100px; }}
    h1, h2, h3, h4, p, span, label, .stMarkdown {{ color: #000000 !important; font-family: 'Inter', sans-serif; }}
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
    
    .stTabs [data-baseweb="tab-list"] {{ background-color: #F0F2F6 !important; border-radius: 10px 10px 0 0; }}
    .stTabs [data-baseweb="tab"] {{ color: #000000 !important; font-weight: bold; }}

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

    .home-btn-container .stButton > button {{
        background: #E5E7EB !important;
        color: #000000 !important;
        padding: 10px !important;
        font-size: 12px !important;
    }}

    textarea {{ border: 1px solid {cor_tema} !important; border-radius: 15px !important; }}

    .badge-recompensa {{
        background: {cor_tema}22;
        color: {cor_tema};
        padding: 8px 20px;
        border-radius: 20px;
        font-size: 14px;
        border: 1px solid {cor_tema};
        font-weight: bold;
        display: inline-block;
    }}

    .footer {{
        position: fixed; left: 0; bottom: 0; width: 100%;
        background-color: {cor_tema}; color: #FFFFFF;
        text-align: center; padding: 15px; font-weight: bold; z-index: 1000;
    }}
    
    .warning-box {{
        background-color: #FFF3CD;
        color: #856404;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #FFEEBA;
        margin-bottom: 20px;
    }}

    .chat-bubble-user {{ background: #E0F7FA; padding: 15px; border-radius: 15px; margin-bottom: 10px; border-left: 5px solid {cor_tema}; color: #000; }}
    .chat-bubble-ai {{ background: #F0F2F6; padding: 15px; border-radius: 15px; margin-bottom: 10px; border-left: 5px solid #333; color: #000; }}
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
st.markdown(f"""
    <div class="footer">
        Acesse <a href="http://www.quizmaispremios.com.br" style="color: #FFF; text-decoration: underline;">www.quizmaispremios.com.br</a> 
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
        if st.button("DEFINIR NICHO E AVANÇAR"):
            st.session_state.memoria['nicho'] = p_nicho
            st.session_state.etapa = 2; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # --- ETAPA 2: CANAL E METAS ---
    elif st.session_state.etapa == 2:
        st.title(f"👥 2. CANAL E GESTÃO DE METAS")
        st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
        
        canal = st.selectbox("Escolha o canal principal:", ["WhatsApp", "YouTube", "Facebook", "E-mail Marketing"], 
                             index=["WhatsApp", "YouTube", "Facebook", "E-mail Marketing"].index(st.session_state.memoria.get('canal_escolhido', 'WhatsApp')))
        st.session_state.memoria['canal_escolhido'] = canal
        
        metas_ideais = {"WhatsApp": 800, "YouTube": 1000, "Facebook": 2000, "E-mail Marketing": 1000}
        unidade = {"WhatsApp": "Membros", "YouTube": "Inscritos", "Facebook": "Seguidores", "E-mail Marketing": "Leads"}
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            atual = st.number_input(f"{unidade[canal]} atuais:", min_value=0, value=st.session_state.memoria.get('audiencia_atual', 0))
            st.session_state.memoria['audiencia_atual'] = atual
        with col_m2:
            st.write(f"**Meta Ideal para Lançamento:** {metas_ideais[canal]} {unidade[canal]}")
        
        progresso = min(atual / metas_ideais[canal], 1.0)
        st.progress(progresso)
        
        if atual < metas_ideais[canal]:
            st.markdown(f"""<div class='warning-box'>⚠️ <b>Cuidado:</b> Você ainda não atingiu a meta ideal. 
            Você pode estar antecipando a venda, o que reduz a conversão. Prossiga por conta própria ou foque em Atração.</div>""", unsafe_allow_html=True)
        
        tab_atracao, tab_engaja = st.tabs(["🧲 MENTOR DE ATRAÇÃO", "🤝 MENTOR DE CONTEÚDO"])
        
        with tab_atracao:
            if st.button("GERAR ANÚNCIO E CONTEÚDO DE ENTRADA"):
                sys = "Você é um Mentor de Atração focado em ganchos virais e promessas fortes."
                prompt = f"Gere um anúncio completo e 3 ganchos virais para levar pessoas ao {canal} no nicho {st.session_state.memoria['nicho']}."
                st.session_state.memoria['atracao_msg'] = nexus_ai(prompt, sys, st.session_state.api_key)
            st.write(st.session_state.memoria.get('atracao_msg', ''))
            
        with tab_engaja:
            if st.button("GERAR CONTEÚDO DE ENGAJAMENTO"):
                sys = "Você é um Mentor de Conteúdo. Oriente sobre materialização (Vídeo, Texto ou Anúncio) e horários."
                prompt = f"Gere 3 conteúdos de engajamento (Curiosidade, Autoridade, Quebra de Crença) para {canal} no nicho {st.session_state.memoria['nicho']}."
                st.session_state.memoria['engaja_msg'] = nexus_ai(prompt, sys, st.session_state.api_key)
            st.write(st.session_state.memoria.get('engaja_msg', ''))

        if st.button("AVANÇAR PARA O PRODUTO 👉"):
            st.session_state.etapa = 3; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # --- ETAPA 3: CRIAÇÃO DO PRODUTO (REINTEGRADO) ---
    elif st.session_state.etapa == 3:
        st.title("🧩 3. CRIAÇÃO DO PRODUTO")
        st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
        p_nome = st.text_input("Qual será o nome do seu produto?", value=st.session_state.memoria.get('nome_produto', ''))
        st.session_state.memoria['nome_produto'] = p_nome
        
        # Módulos específicos por canal (E-mail e YouTube)
        if st.session_state.memoria['canal_escolhido'] == "E-mail Marketing":
            st.markdown("#### 📧 Módulo E-mail Marketing")
            col_e1, col_e2 = st.columns(2)
            with col_e1:
                if st.button("GERAR ISCA DIGITAL (E-BOOK GRÁTIS)"):
                    st.session_state.memoria['isca'] = nexus_ai(f"Crie o título e a ideia de conteúdo para um E-book grátis no nicho {st.session_state.memoria['nicho']}.", "Escritor", st.session_state.api_key)
            with col_e2:
                if st.button("TEXTOS PARA LANDING PAGE"):
                    st.session_state.memoria['lp_text'] = nexus_ai(f"Gere Headline e textos de benefícios para uma Landing Page de {p_nome}.", "Copywriter", st.session_state.api_key)
            st.write(st.session_state.memoria.get('isca', ''))
            st.write(st.session_state.memoria.get('lp_text', ''))

        elif st.session_state.memoria['canal_escolhido'] == "YouTube":
            st.markdown("#### ▶️ Módulo YouTube")
            if st.button("ESTRATÉGIA DE SHORTS/ANÚNCIOS"):
                st.session_state.memoria['yt_strat'] = nexus_ai(f"Gere ideias de Shorts para crescer inscritos no nicho {st.session_state.memoria['nicho']}.", "YouTube Expert", st.session_state.api_key)
            st.write(st.session_state.memoria.get('yt_strat', ''))

        # Módulo Geral de Criação de Conteúdo do Produto
        st.markdown("---")
        st.subheader("Conteúdo Interno do Produto")
        tab_eb, tab_heygen = st.tabs(["📄 E-BOOK (60 CARTÕES)", "🎥 VIDEO AULAS (HEYGEN)"])
        
        with tab_eb:
            if st.button("GERAR CONTEÚDO PARA GAMMA.APP (60 CARTÕES)"):
                prompt_eb = f"Crie o conteúdo do produto {p_nome} dividido em 60 cartões numerados para o Gamma.app no nicho {st.session_state.memoria['nicho']}."
                st.session_state.memoria['ebook_content'] = nexus_ai(prompt_eb, "Escritor de Infoprodutos", st.session_state.api_key)
            st.text_area("Cópia para Gamma:", value=st.session_state.memoria.get('ebook_content', ''), height=200)
            
        with tab_heygen:
            if st.button("GERAR ROTEIROS PARA AVATAR HEYGEN"):
                prompt_hg = f"Crie 6 roteiros de aulas para o produto {p_nome} focados em Avatares de IA."
                st.session_state.memoria['heygen_scripts'] = nexus_ai(prompt_hg, "Roteirista", st.session_state.api_key)
            st.text_area("Scripts HeyGen:", value=st.session_state.memoria.get('heygen_scripts', ''), height=200)

        if st.button("PRODUTO DEFINIDO 👉"):
            st.session_state.etapa = 4; salvar_progresso(); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # --- ETAPA 4: ARSENAL E DOUTRINAÇÃO ---
    elif st.session_state.etapa == 4:
        st.title("📢 4. DOUTRINAÇÃO E ARSENAL")
        st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
        
        if st.button("GERAR SEQUÊNCIA DE DOUTRINAÇÃO (ESTILO CURIOSIDADE)"):
            sys = "Você cria mensagens de curiosidade disruptiva (ex: caso da carne cultivada). Não venda ainda, intrigue."
            prompt = f"Gere 3 mensagens de curiosidade profunda para o nicho {st.session_state.memoria['nicho']} para aquecer a audiência."
            st.session_state.memoria['doutrinacao'] = nexus_ai(prompt, sys, st.session_state.api_key)
        st.write(st.session_state.memoria.get('doutrinacao', ''))
        
        if st.button("GERAR SCRIPT DE VENDAS (VSL)"):
            sys = "Você é um Copywriter de Elite focado em VSL."
            prompt = f"Crie um script de VSL para o produto {st.session_state.memoria['nome_produto']} com Promessa, História e Oferta."
            st.session_state.memoria['vsl'] = nexus_ai(prompt, sys, st.session_state.api_key)
        st.write(st.session_state.memoria.get('vsl', ''))

        if st.button("AVANÇAR PARA O LANÇAMENTO 👉"):
            st.session_state.etapa = 5; salvar_progresso(); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # --- ETAPA 5: CRONOGRAMA ---
    elif st.session_state.etapa == 5:
        st.title("📅 5. CRONOGRAMA MESTRE (15 DIAS)")
        st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
        st.write(f"**Plano para {st.session_state.memoria['canal_escolhido']}**")
        st.checkbox("Dias 1-7: Atração massiva (Shorts/Ads/Ganchos).")
        st.checkbox("Dias 8-12: Doutrinação (Curiosidades/Autoridade).")
        st.checkbox("Dias 13-15: Oferta VSL e Fechamento.")
        if st.button("FINALIZAR OPERAÇÃO"):
            st.session_state.etapa = 6; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # --- ETAPA 6: CONCLUÍDO ---
    elif st.session_state.etapa == 6:
        st.title("🏆 OPERAÇÃO FINALIZADA!")
        st.balloons()
        st.markdown(f"<div class='nexus-card' style='background: #D1FFD1 !important; text-align:center;'>", unsafe_allow_html=True)
        st.write("### O Nexus Launcher concluiu sua estratégia.")
        if st.button("ACESSAR SUPORTE E ANÁLISE 👉"):
            st.session_state.etapa = 7; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # --- ETAPA 7: SUPORTE ---
    elif st.session_state.etapa == 7:
        st.title("🎧 7. SUPORTE E ANÁLISE")
        for msg in st.session_state.chat_history:
            div = "chat-bubble-user" if msg["role"] == "user" else "chat-bubble-ai"
            st.markdown(f"<div class='{div}'>{msg['content']}</div>", unsafe_allow_html=True)

        with st.form("chat_nexus", clear_on_submit=True):
            user_input = st.text_input("Dúvida ou análise ➔")
            if st.form_submit_button("ENVIAR ➔"):
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                sys_role = f"Você é o consultor da Nexus Launcher."
                resp = nexus_ai(user_input, sys_role, st.session_state.api_key, history=st.session_state.chat_history[:-1])
                st.session_state.chat_history.append({"role": "assistant", "content": resp})
                st.rerun()
