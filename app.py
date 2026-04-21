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

    # --- ETAPA 1: IDEIA ---
    elif st.session_state.etapa == 1:
        st.title("🧠 1. DEFINIÇÃO DA IDEIA")
        st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
        p_nome = st.text_input("Qual o nicho ou nome do produto?", value=st.session_state.memoria.get('nome_produto', ''))
        p_ganho = st.selectbox("Meta de faturamento:", ["R$ 5k", "R$ 20k", "R$ 50k+"])
        if st.button("DEFINIR E AVANÇAR"):
            with st.spinner("Refinando ideia..."):
                sys = "Você é um estrategista digital. Crie uma Promessa Irresistível (Big Idea) e valide o público alvo."
                st.session_state.memoria['etapa1'] = nexus_ai(f"Produto: {p_nome}, Meta: {p_ganho}", sys, st.session_state.api_key)
                st.session_state.memoria['nome_produto'] = p_nome
                st.session_state.etapa = 2; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # --- ETAPA 2: AUDIÊNCIA ---
    elif st.session_state.etapa == 2:
        st.title("👥 2. CONSTRUÇÃO DE AUDIÊNCIA")
        st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
        st.write("### 🎥 Clique aqui para assistir o video com dicas mestre")
        st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='price-tip'><strong>IMPORTANTE:</strong> Se você não tem audiência, o produto não vende.</div>", unsafe_allow_html=True)
        
        tab_reels, tab_stories = st.tabs(["🎥 REELS / TIKTOK (Atração)", "🤳 STORIES (Conexão)"])
        with tab_reels:
            if st.button("GERAR ROTEIROS DE VÍDEOS CURTOS"):
                st.session_state.memoria['reels'] = nexus_ai(st.session_state.memoria['etapa1'], "Crie 3 roteiros de Reels.", st.session_state.api_key)
            st.markdown(st.session_state.memoria.get('reels', 'Aguardando...'))
        with tab_stories:
            if st.button("GERAR SEQUÊNCIA DE STORIES"):
                st.session_state.memoria['stories'] = nexus_ai(st.session_state.memoria['etapa1'], "Crie 5 stories de autoridade.", st.session_state.api_key)
            st.markdown(st.session_state.memoria.get('stories', 'Aguardando...'))
        if st.button("ESTRATÉGIA DE AUDIÊNCIA PRONTA 👉"):
            st.session_state.etapa = 3; salvar_progresso(); st.rerun()

    # --- ETAPA 3: CONTEÚDO (PRODUTO) ---
    elif st.session_state.etapa == 3:
        st.title("🧩 3. CONSTRUÇÃO DO CONTEÚDO (PRODUTO)")
        contexto_fixo = st.session_state.memoria.get('etapa1', 'Ideia não definida')
        st.info(f"Foco Temático: {contexto_fixo}")
        
        # ELIMINADA A ABA VIDEOAULAS (CONTEÚDO) E ADICIONADO EMOJI NO HEYGEN
        tab_eb, tab_heygen = st.tabs(["📄 E-BOOK (60 CARTÕES GAMMA)", "🎥 VIDEO AULAS (HEYGEN PRO)"])
        
        with tab_eb:
            if st.button("GERAR E-BOOK COMPLETO (60 CARTÕES)"):
                prompt_ebook = (
                    f"Com base na Big Idea: {contexto_fixo}, escreva o conteúdo de um e-book de alta conversão "
                    f"dividido em EXATAMENTE 60 blocos ou cartões numerados. "
                    f"Cada bloco deve conter um Título e um Texto explicativo persuasivo. "
                    f"Esta estrutura será colada no Gamma.app (Plano Pro), então mantenha um fluxo lógico de "
                    f"Início, Meio e Fim em 60 slides. Não simplifique, gere o conteúdo denso e completo."
                )
                st.session_state.memoria['ebook_content'] = nexus_ai(prompt_ebook, "Você é um escritor especialista em infoprodutos e design de conteúdo para Gamma.app.", st.session_state.api_key)
            
            st.session_state.memoria['ebook_content'] = st.text_area("Conteúdo para copiar e colar no Gamma (60 Cartões):", value=st.session_state.memoria.get('ebook_content', ''), height=400)
            st.markdown("<div class='ai-tool-box'><strong>🚀 Dica Gamma Pro:</strong> Copie o texto acima, vá ao <a href='https://gamma.app/' target='_blank' class='tool-link'>Gamma.app</a>, escolha 'Texto para Apresentação' e cole. O sistema gerará os 60 cartões automaticamente.</div>", unsafe_allow_html=True)
            
        with tab_heygen:
            st.markdown("### 🎥 VIDEO AULAS (HEYGEN PRO)")
            if st.button("GERAR 6 ROTEIROS DE AULAS PARA HEYGEN PRO"):
                prompt_heygen = (
                    f"Com base na Big Idea: {contexto_fixo}, crie EXATAMENTE 6 roteiros de videoaulas (conteúdo do curso) "
                    f"otimizados para criação no HeyGen. Formato: Vídeo 1: Introdução ao Método + Script Narrativo. "
                    f"Os vídeos devem compor o curso completo."
                )
                st.session_state.memoria['heygen_scripts'] = nexus_ai(prompt_heygen, "Você é um especialista em roteiros para avatares de IA no HeyGen focado em videoaulas didáticas.", st.session_state.api_key)
            
            st.session_state.memoria['heygen_scripts'] = st.text_area("Roteiros das Aulas para HeyGen:", value=st.session_state.memoria.get('heygen_scripts', ''), height=400)
            st.markdown("""
                <div class='ai-tool-box'>
                    <strong>🚀 Instruções HeyGen Pro:</strong><br>
                    1. Copie um roteiro por aula.<br>
                    2. Acesse o <a href='https://www.heygen.com/' target='_blank' class='tool-link'>HeyGen.com</a>.<br>
                    3. Escolha seu Avatar Pro e cole o script da aula.<br>
                    4. Selecione uma voz humana ultra-realista e gere a videoaula.
                </div>
            """, unsafe_allow_html=True)
        
        if st.button("CONTEÚDO PRONTO 👉"):
            st.session_state.etapa = 4; salvar_progresso(); st.rerun()

    # --- ETAPA 4: ARSENAL DE VENDAS ---
    elif st.session_state.etapa == 4:
        st.title("📢 4. ARSENAL DE VENDAS")
        ctx = st.session_state.memoria.get('etapa1')
        st.markdown("<div class='price-tip'><strong>CONFIGURAÇÃO DE FOCO:</strong> Escolha apenas um formato para gerar a divulgação completa agora.</div>", unsafe_allow_html=True)
        
        tipo_divulgacao = st.radio(
            "O que você deseja divulgar agora?",
            ["E-book", "Videoaulas"],
            index=0 if st.session_state.memoria.get('tipo_divulgacao') == "E-book" else 1
        )
        st.session_state.memoria['tipo_divulgacao'] = tipo_divulgacao
        
        if tipo_divulgacao == "E-book":
            preco = st.text_input("Preço E-book (ex: R$ 29,90):", value=st.session_state.memoria.get('preco_eb', 'R$ 29,90'))
            st.session_state.memoria['preco_eb'] = preco
            prompt_cta = f"O produto é um E-book. Use EXCLUSIVAMENTE o CTA: 'Clique aqui para baixar o ebook preço {preco}'."
        else:
            preco = st.text_input("Preço Vídeos (ex: R$ 97,00):", value=st.session_state.memoria.get('preco_vid', 'R$ 97,00'))
            st.session_state.memoria['preco_vid'] = preco
            prompt_cta = f"O produto são Videoaulas. Use EXCLUSIVAMENTE o CTA: 'Clique aqui para baixar o curso completo em videoaulas preço {preco}'."

        t1, t2, t3, t4 = st.tabs(["📹 VSL", "📢 ANÚNCIOS", "💬 WHATSAPP", "📧 E-MAILS"])
        
        # INSTRUÇÃO PARA CONTEÚDO PRO DO HEYGEN NO VSL ADICIONADA
        aida_sys = (
            f"Você é um Copywriter Sênior. Crie roteiros detalhados seguindo a estrutura AIDA. "
            f"REGRAS OBRIGATÓRIAS: {prompt_cta}. Foque 100% no formato escolhido. "
            f"IMPORTANTE: No roteiro de VSL, inclua uma seção de CONTEÚDO PRO incentivando a pessoa a também fazer o HeyGen para criar seus próprios vídeos. "
            f"Ao final da explicação sobre o HeyGen no VSL, inclua EXATAMENTE estas instruções: "
            f"1. Copie um roteiro por aula. 2. Acesse o HeyGen.com. 3. Escolha seu Avatar Pro e cole o script da aula. 4. Selecione uma voz humana ultra-realista e gere a videoaula."
        )

        with t1:
            if st.button("GERAR ROTEIRO VSL"): 
                st.session_state.memoria['vsl'] = nexus_ai(f"Crie um roteiro de VSL longo para: {ctx}", aida_sys, st.session_state.api_key)
            st.markdown(st.session_state.memoria.get('vsl', ''))
        with t2:
            if st.button("GERAR SEQUÊNCIA DE ANÚNCIOS"): 
                st.session_state.memoria['ads'] = nexus_ai(f"Crie uma sequência de anúncios de alta conversão para: {ctx}", aida_sys, st.session_state.api_key)
            st.markdown(st.session_state.memoria.get('ads', ''))
        with t3:
            if st.button("GERAR SCRIPTS WHATSAPP"): 
                st.session_state.memoria['zap'] = nexus_ai(f"Crie funil de mensagens para: {ctx}", aida_sys, st.session_state.api_key)
            st.markdown(st.session_state.memoria.get('zap', ''))
        with t4:
            if st.button("GERAR SEQUÊNCIA DE E-MAILS"): 
                st.session_state.memoria['emails'] = nexus_ai(f"Crie sequência de 5 e-mails para: {ctx}", aida_sys, st.session_state.api_key)
            st.markdown(st.session_state.memoria.get('emails', ''))
            
        if st.button("AVANÇAR 👉"):
            st.session_state.etapa = 5; salvar_progresso(); st.rerun()

    # --- ETAPA 5: CRONOGRAMA ---
    elif st.session_state.etapa == 5:
        st.title("📅 5. CRONOGRAMA MESTRE (15 DIAS)")
        st.markdown("<div class='price-tip'>Siga este cronograma para garantir o aquecimento e a conversão máxima do seu lançamento.</div>", unsafe_allow_html=True)
        
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.subheader("🔥 FASE 1: ATRAÇÃO & ANTECIPAÇÃO")
            with st.expander("Dias 1 a 3: Consciência do Problema"):
                st.checkbox("Dia 1: Postar Reels quebrando um mito comum do nicho.")
                st.checkbox("Dia 2: Stories contando uma história de fracasso por falta do método.")
                st.checkbox("Dia 3: Enviar 1º E-mail da sequência AIDA (Atenção).")
            with st.expander("Dias 4 a 7: Autoridade & Prova"):
                st.checkbox("Dia 4: Mostrar bastidores da criação do produto nos Stories.")
                st.checkbox("Dia 5: Postar depoimento ou resultado gerado pelo método.")
                st.checkbox("Dia 6: Abrir box de perguntas para tirar dúvidas técnicas.")
                st.checkbox("Dia 7: Anúncio de 'Algo novo está chegando' (Remarketing).")

        with col_c2:
            st.subheader("💰 FASE 2: OFERTA & ESCASSEZ")
            with st.expander("Dias 8 a 11: Abertura de Carrinho"):
                st.checkbox("Dia 8: Lançamento oficial! Enviar VSL para lista de Zap/E-mail.")
                st.checkbox("Dia 9: Live de tirar dúvidas ou Stories 'O que tem dentro'.")
                st.checkbox("Dia 10: Primeiro Bônus Exclusivo para quem comprar hoje.")
                st.checkbox("Dia 11: Mostrar prints de novos alunos entrando (Prova Social).")
            with st.expander("Dias 12 a 15: Fechamento & Urgência"):
                st.checkbox("Dia 12: Enviar e-mail focado em Desejo (AIDA).")
                st.checkbox("Dia 13: Quebra de objeção final: 'Não tenho tempo/dinheiro'.")
                st.checkbox("Dia 14: Aviso de 24 horas para o fim das inscrições.")
                st.checkbox("Dia 15: ÚLTIMO DIA! Postar contagem regressiva de hora em hora.")

        if st.button("FINALIZAR OPERAÇÃO"):
            st.session_state.etapa = 6; st.rerun()

        st.markdown("<br><hr>", unsafe_allow_html=True)
        st.markdown("### 💬 Mentor Nexus: Dúvidas sobre a Execução")
        chat_container = st.container()
        with chat_container:
            for msg in st.session_state.chat_cronograma:
                div = "chat-bubble-user" if msg["role"] == "user" else "chat-bubble-ai"
                st.markdown(f"<div class='{div}'>{msg['content']}</div>", unsafe_allow_html=True)

        with st.form("chat_etapa_5", clear_on_submit=True):
            user_q = st.text_input("Ex: 'Como faço o Story do Dia 4 para meu nicho?' ➔")
            if st.form_submit_button("CONSULTAR MENTOR ➔"):
                if user_q:
                    st.session_state.chat_cronograma.append({"role": "user", "content": user_q})
                    sys_cronograma = f"Você é um Mentor Expert em Lançamentos da Nexus Launcher. Sua missão é ajudar {st.session_state.nome_user} com o produto {st.session_state.memoria.get('nome_produto')}. Seja prático."
                    resp_cron = nexus_ai(user_q, sys_cronograma, st.session_state.api_key, history=st.session_state.chat_cronograma[:-1])
                    st.session_state.chat_cronograma.append({"role": "assistant", "content": resp_cron})
                    st.rerun()

    # --- ETAPA 6: CONCLUÍDO ---
    elif st.session_state.etapa == 6:
        st.title("🏆 OPERAÇÃO FINALIZADA!")
        st.balloons()
        st.markdown("<div class='nexus-card' style='background: #D1FFD1 !important; text-align:center;'>", unsafe_allow_html=True)
        st.write("### Parabéns! Seu império digital começou.")
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

        if st.button("CRIAR NOVA ESTRATÉGIA COMPLETA"):
            st.session_state.chat_history = []; st.session_state.chat_cronograma = []
            st.session_state.memoria = {'nome_produto': st.session_state.memoria.get('nome_produto', '')}
            st.session_state.etapa = 1; st.rerun()
