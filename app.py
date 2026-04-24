import streamlit as st
from groq import Groq
from datetime import timedelta

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="NEXUS LAUNCHER", layout="wide")

# --- ESTILO CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700&family=Inter:wght@400;500&display=swap');

    [data-testid="stSidebar"] { display: none; }

    body, .stApp { font-family: 'Inter', sans-serif; }

    h1, h2, h3 { font-family: 'Rajdhani', sans-serif; letter-spacing: 1px; }

    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3.5em;
        background-color: #00BFFF !important;
        color: white !important;
        font-weight: bold;
        border: none;
        font-family: 'Rajdhani', sans-serif;
        letter-spacing: 1px;
        font-size: 1em;
        transition: background-color 0.2s ease;
    }
    .stButton>button:hover { background-color: #0099CC !important; }

    .caixa-texto {
        background-color: #F8FAFC;
        padding: 25px;
        border-radius: 12px;
        border-left: 6px solid #00BFFF;
        margin-bottom: 20px;
        white-space: pre-wrap;
        color: #1E293B;
        line-height: 1.6;
    }

    .chat-bubble {
        background-color: #F1F5F9;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #E2E8F0;
        margin-bottom: 10px;
    }

    .btn-perigo>button {
        background-color: #ef4444 !important;
        height: 2em !important;
    }

    .footer {
        text-align: center;
        padding: 60px;
        color: #94A3B8;
        font-size: 0.8em;
        opacity: 0.4;
        margin-top: 100px;
        font-style: italic;
    }

    .step-indicator {
        display: flex;
        gap: 8px;
        margin-bottom: 20px;
        flex-wrap: wrap;
    }

    .step-badge {
        background: #E2E8F0;
        color: #64748B;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 0.75em;
        font-weight: 600;
        font-family: 'Rajdhani', sans-serif;
        letter-spacing: 0.5px;
    }

    .step-badge.ativo {
        background: #00BFFF;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO DE ESTADO ---
defaults = {
    'etapa': "Login",
    'dados': {},
    'projetos': {},
    'chat_hist': [],
    'usuario': '',
    'api_key': '',
    'chat_input_key': 0,
    'admin_mode_dicas': False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# --- ETAPAS PARA INDICADOR DE PROGRESSO ---
ETAPAS = ["Formulario", "Gerar_Ebook", "Copy_Face", "Copy_LP", "Mensagens_Grupo", "Visualizacao"]
ETAPAS_LABELS = {
    "Formulario": "1. Formulário",
    "Gerar_Ebook": "2. E-book",
    "Copy_Face": "3. Anúncio",
    "Copy_LP": "4. Landing Page",
    "Mensagens_Grupo": "5. Mensagens",
    "Visualizacao": "6. Projeto Final",
}

# --- FUNÇÃO DE IA ---
def chamar_ia(prompt: str, system_prompt: str) -> str:
    try:
        client = Groq(api_key=st.session_state.api_key)
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile",
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Erro na API: {e}"

# --- INDICADOR DE PROGRESSO ---
def mostrar_progresso():
    etapa_atual = st.session_state.etapa
    badges = ""
    for chave, label in ETAPAS_LABELS.items():
        classe = "ativo" if chave == etapa_atual else "step-badge"
        if chave == etapa_atual:
            badges += f'<span class="step-badge ativo">{label}</span>'
        else:
            badges += f'<span class="step-badge">{label}</span>'
    st.markdown(f'<div class="step-indicator">{badges}</div>', unsafe_allow_html=True)

# --- BARRA DE NAVEGAÇÃO ---
def barra_navegacao():
    mostrar_progresso()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ INICIAR NOVO PROJETO"):
            st.session_state.dados = {}
            st.session_state.etapa = "Formulario"
            st.rerun()
    with col2:
        with st.expander("📂 MEUS PROJETOS"):
            if not st.session_state.projetos:
                st.write("Nenhum projeto salvo.")
            for nome in list(st.session_state.projetos.keys()):
                c_abrir, c_deletar = st.columns([4, 1])
                if c_abrir.button(f"📄 {nome}", key=f"abrir_{nome}"):
                    st.session_state.dados = st.session_state.projetos[nome].copy()
                    st.session_state.etapa = "Visualizacao"
                    st.rerun()
                st.markdown('<div class="btn-perigo">', unsafe_allow_html=True)
                if c_deletar.button("🗑️", key=f"del_{nome}", help="Excluir projeto"):
                    del st.session_state.projetos[nome]
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# TELA: LOGIN
# ============================================================
if st.session_state.etapa == "Login":
    st.title("NEXUS LAUNCHER")
    st.subheader("ACESSO RESTRITO A ASSOCIADOS DO QUIZ MAIS PRÊMIOS")
    st.session_state.usuario = st.text_input("Nome")
    st.session_state.api_key = st.text_input("Chave Groq", type="password")

    if st.button("ENTRAR"):
        if not st.session_state.usuario.strip():
            st.error("Informe seu nome.")
        elif not st.session_state.api_key.strip():
            st.error("Informe sua chave de API.")
        else:
            st.session_state.etapa = "Formulario"
            st.rerun()

# ============================================================
# TELA: FORMULÁRIO
# ============================================================
elif st.session_state.etapa == "Formulario":
    barra_navegacao()
    st.title("PREENCHA O FORMULÁRIO")
    d = st.session_state.dados

    d['nicho']      = st.text_input("Nicho:", value=d.get('nicho', ''), help="ex: emagrecimento, renda extra")
    d['publico']    = st.text_input("Público-alvo:", value=d.get('publico', ''), help="ex: homens de 25 a 40")
    d['nome_eb']    = st.text_input("Nome do e-book:", value=d.get('nome_eb', ''))
    d['dor']        = st.text_input("Principal dor que resolve:", value=d.get('dor', ''))
    d['atual']      = st.text_area("Situação atual da pessoa:", value=d.get('atual', ''))
    d['desejada']   = st.text_area("Situação desejada:", value=d.get('desejada', ''))
    d['promessa']   = st.text_input("Promessa do e-book:", value=d.get('promessa', ''))
    d['diferencial']= st.text_input("Diferencial:", value=d.get('diferencial', ''))
    d['data_lancto']= st.date_input("Data de lançamento")

    campos_obrigatorios = ['nicho', 'publico', 'nome_eb', 'dor', 'atual', 'desejada', 'promessa', 'diferencial']
    if st.button("AVANÇAR"):
        faltando = [c for c in campos_obrigatorios if not d.get(c, '').strip()]
        if faltando:
            st.warning(f"Preencha todos os campos antes de avançar.")
        else:
            st.session_state.etapa = "Gerar_Ebook"
            st.rerun()

# ============================================================
# TELA: GERAR E-BOOK
# ============================================================
elif st.session_state.etapa == "Gerar_Ebook":
    barra_navegacao()
    st.title("📚 GERAR E-BOOK PROFISSIONAL")

    if st.button("GERAR E-BOOK – 60 CARTÕES"):
        with st.spinner("Gerando e-book com IA..."):
            d = st.session_state.dados
            prompt = (
                f"Gere 60 cartões educativos numerados para o e-book '{d['nome_eb']}'. "
                f"Público-alvo: {d['publico']}. Dor principal: {d['dor']}. "
                f"Diferencial: {d['diferencial']}. Cada cartão deve ter título e conteúdo útil."
            )
            st.session_state.dados['ebook_cont'] = chamar_ia(
                prompt,
                "Você é um especialista em conteúdo digital educativo. Seja objetivo e prático."
            )

    if 'ebook_cont' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['ebook_cont']}</div>", unsafe_allow_html=True)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "Copy_Face"
            st.rerun()

# ============================================================
# TELA: COPY FACEBOOK
# ============================================================
elif st.session_state.etapa == "Copy_Face":
    barra_navegacao()
    st.title("📱 COPY PARA O FACEBOOK")

    if st.button("GERAR 5 VARIAÇÕES"):
        with st.spinner("Gerando copies com IA..."):
            d = st.session_state.dados
            prompt = (
                f"Crie 5 variações de copy curta para Facebook Ads. "
                f"Nicho: {d['nicho']}. Público: {d['publico']}. Dor: {d['dor']}. "
                f"Lançamento: {d['data_lancto'].strftime('%d/%m/%Y')}. "
                f"OBRIGATÓRIO para cada variação: "
                f"1. Identifique com título em negrito (ex: **Variação 1: [Nome]**). "
                f"2. Inclua sugestão detalhada de imagem/criativo visual. "
                f"3. Finalize com: ⬇️ Clique abaixo e descubra como. "
                f"4. Separe parágrafos com linha em branco."
            )
            st.session_state.dados['fb_copy'] = chamar_ia(
                prompt,
                "Você é um copywriter especialista em anúncios diretos e curtos para Facebook Ads."
            )

    if 'fb_copy' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['fb_copy']}</div>", unsafe_allow_html=True)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "Copy_LP"
            st.rerun()

# ============================================================
# TELA: COPY LANDING PAGE
# ============================================================
elif st.session_state.etapa == "Copy_LP":
    barra_navegacao()
    st.title("🌐 COPY PARA A LANDING PAGE")

    if st.button("GERAR 5 VARIAÇÕES LP"):
        with st.spinner("Gerando landing pages com IA..."):
            d = st.session_state.dados
            prompt = (
                f"Crie 5 variações de copy completa para Landing Page. "
                f"Situação atual: {d['atual']}. Situação desejada: {d['desejada']}. "
                f"Promessa: {d['promessa']}. Diferencial: {d['diferencial']}. "
                f"Para cada variação, sugira imagens e elementos visuais. "
                f"Finalize cada variação com o botão de ação: [ ENTRAR NO GRUPO ]."
            )
            st.session_state.dados['lp_copy'] = chamar_ia(
                prompt,
                "Você é um especialista em Landing Pages de alta conversão. "
                "Identifique cada variação com título em negrito (ex: **Variação 1: [Nome]**)."
            )

    if 'lp_copy' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['lp_copy']}</div>", unsafe_allow_html=True)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "Mensagens_Grupo"
            st.rerun()

# ============================================================
# TELA: MENSAGENS DO GRUPO
# ============================================================
elif st.session_state.etapa == "Mensagens_Grupo":
    barra_navegacao()
    st.title("📌 MENSAGENS PARA O GRUPO")

    d = st.session_state.dados
    nicho    = d['nicho']
    data     = d['data_lancto'].strftime('%d/%m/%Y')
    data_d1  = (d['data_lancto'] - timedelta(days=1)).strftime('%d/%m/%Y')
    resultado= d['promessa']
    dor      = d['dor']

    msg_template = f"""**Descrição do grupo:**
Este grupo é silencioso. Você não será incomodado.
Aqui você receberá apenas conteúdos e avisos relacionados ao tema.

---

**📩 Mensagem 1 – Boas-vindas + Pré-lançamento**
Bem-vindo(a) 👋
Este grupo é silencioso, então pode ficar tranquilo(a), você não será incomodado.
Você entrou aqui porque quer aprender mais sobre {nicho} — e eu preparei algo direto ao ponto pra isso.
📅 No dia {data}, vou liberar um conteúdo exclusivo onde mostro um método simples que pode te ajudar a {resultado}.
Fica por aqui… porque o que vou mostrar pode mudar a forma como você enxerga isso.

---

**⏳ Mensagem 2 – 1 dia antes ({data_d1}) — aquecimento**
Amanhã é o dia.
Depois de organizar tudo, finalmente vou liberar o conteúdo sobre {nicho}.
Se você sente que ainda está travado(a) em {dor}, presta atenção nisso…
O que você vai ver amanhã não é teoria — é um caminho direto que você pode aplicar.
⏰ Fica atento(a), porque vou liberar aqui no grupo.

---

**🚀 Mensagem 3 – Lançamento ({data})**
Chegou o momento.
Como prometido, acabei de liberar o conteúdo completo.
Nele, mostro exatamente como você pode {resultado}, mesmo começando do zero.
Se você quer parar de {dor} e finalmente ter resultado em {nicho}, esse é o próximo passo:
👉 [LINK DA MONETIZZE]
A partir de agora está disponível — mas não sei por quanto tempo vou deixar assim."""

    st.session_state.dados['msg_grupo'] = msg_template
    st.markdown(f"<div class='caixa-texto'>{msg_template}</div>", unsafe_allow_html=True)

    # --- DICAS DE APLICAÇÃO COM MODO ADMIN ---
    st.markdown("---")
    st.markdown("### 💡 Dicas de Aplicação")

    dicas_prompt = (
        f"Dê dicas práticas e detalhadas de como aplicar este lançamento digital. "
        f"Nicho: {nicho}. Público: {d['publico']}. Promessa: {resultado}. "
        f"Inclua dicas de tráfego pago, engajamento do grupo e conversão."
    )
    dicas_system = "Você é um especialista em lançamentos digitais e marketing de performance."

    col_ia, col_admin = st.columns(2)

    with col_ia:
        if st.button("🤖 GERAR / REGENERAR DICAS COM IA"):
            with st.spinner("Gerando dicas com IA..."):
                st.session_state.dados['dicas'] = chamar_ia(dicas_prompt, dicas_system)
                st.session_state.admin_mode_dicas = False
                st.rerun()

    with col_admin:
        label_btn = "❌ FECHAR EDITOR" if st.session_state.admin_mode_dicas else "✏️ EDITAR DICAS MANUALMENTE"
        if st.button(label_btn):
            st.session_state.admin_mode_dicas = not st.session_state.admin_mode_dicas
            st.rerun()

    if st.session_state.admin_mode_dicas:
        st.markdown("**✏️ Editor de Dicas — Admin**")
        dicas_editadas = st.text_area(
            "Edite o texto das dicas abaixo:",
            value=st.session_state.dados.get('dicas', ''),
            height=400,
            key="editor_dicas"
        )
        if st.button("💾 SALVAR EDIÇÃO DAS DICAS"):
            st.session_state.dados['dicas'] = dicas_editadas
            st.session_state.admin_mode_dicas = False
            st.success("✅ Dicas atualizadas com sucesso!")
            st.rerun()
    else:
        if 'dicas' in st.session_state.dados and st.session_state.dados['dicas']:
            st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['dicas']}</div>", unsafe_allow_html=True)
        else:
            st.info("Nenhuma dica gerada ainda. Clique em 'Gerar com IA' ou edite manualmente.")

    if st.button("💾 SALVAR PROJETO"):
        nome_projeto = st.session_state.dados.get('nome_eb', 'Sem nome')
        st.session_state.projetos[nome_projeto] = st.session_state.dados.copy()
        st.session_state.etapa = "Visualizacao"
        st.rerun()

# ============================================================
# TELA: VISUALIZAÇÃO FINAL
# ============================================================
elif st.session_state.etapa == "Visualizacao":
    barra_navegacao()
    nome_projeto = st.session_state.dados.get('nome_eb', 'Projeto')
    st.title(f"PROJETO: {nome_projeto}")

    with st.expander("📚 E-BOOK"):
        conteudo = st.session_state.dados.get('ebook_cont', '_Não gerado ainda._')
        st.markdown(f"<div class='caixa-texto'>{conteudo}</div>", unsafe_allow_html=True)

    with st.expander("🎬 ANÚNCIO (Facebook)"):
        conteudo = st.session_state.dados.get('fb_copy', '_Não gerado ainda._')
        st.markdown(f"<div class='caixa-texto'>{conteudo}</div>", unsafe_allow_html=True)

    with st.expander("🌐 LANDING PAGE"):
        conteudo = st.session_state.dados.get('lp_copy', '_Não gerado ainda._')
        st.markdown(f"<div class='caixa-texto'>{conteudo}</div>", unsafe_allow_html=True)

    with st.expander("📌 MENSAGENS DO GRUPO"):
        conteudo = st.session_state.dados.get('msg_grupo', '_Não gerado ainda._')
        st.markdown(f"<div class='caixa-texto'>{conteudo}</div>", unsafe_allow_html=True)

    with st.expander("💡 DICAS PARA APLICAÇÃO"):
        conteudo = st.session_state.dados.get('dicas', '')

        col_ia2, col_admin2 = st.columns(2)
        with col_ia2:
            if st.button("🤖 REGENERAR DICAS COM IA", key="regen_dicas_viz"):
                d_viz = st.session_state.dados
                with st.spinner("Gerando dicas com IA..."):
                    prompt_viz = (
                        f"Dê dicas práticas e detalhadas de como aplicar este lançamento digital. "
                        f"Nicho: {d_viz.get('nicho')}. Público: {d_viz.get('publico')}. Promessa: {d_viz.get('promessa')}. "
                        f"Inclua dicas de tráfego pago, engajamento do grupo e conversão."
                    )
                    st.session_state.dados['dicas'] = chamar_ia(
                        prompt_viz,
                        "Você é um especialista em lançamentos digitais e marketing de performance."
                    )
                    st.session_state.admin_mode_dicas = False
                    st.rerun()
        with col_admin2:
            label_viz = "❌ FECHAR EDITOR" if st.session_state.admin_mode_dicas else "✏️ EDITAR MANUALMENTE"
            if st.button(label_viz, key="admin_dicas_viz"):
                st.session_state.admin_mode_dicas = not st.session_state.admin_mode_dicas
                st.rerun()

        if st.session_state.admin_mode_dicas:
            st.markdown("**✏️ Editor de Dicas — Admin**")
            dicas_ed = st.text_area(
                "Edite o texto das dicas:",
                value=conteudo,
                height=400,
                key="editor_dicas_viz"
            )
            if st.button("💾 SALVAR EDIÇÃO", key="salvar_dicas_viz"):
                st.session_state.dados['dicas'] = dicas_ed
                st.session_state.admin_mode_dicas = False
                st.success("✅ Dicas atualizadas!")
                st.rerun()
        else:
            if conteudo:
                st.markdown(f"<div class='caixa-texto'>{conteudo}</div>", unsafe_allow_html=True)
            else:
                st.info("Nenhuma dica gerada ainda.")

    # --- LAUNCERBOT (CHAT) ---
    st.divider()
    st.markdown("### 🤖 Launcerbot")
    st.info(
        f"**Olá, {st.session_state.usuario}! 👋** "
        "Eu sou o **Launcerbot**. Ajudo você a criar e lançar produtos digitais, mesmo do zero. "
        "Pode me perguntar qualquer coisa sobre seu lançamento 👇"
    )

    # Chat com botão — evita chamadas duplicadas a cada rerun
    pergunta = st.text_input(
        "Sua pergunta:",
        key=f"chat_input_{st.session_state.chat_input_key}"
    )

    if st.button("ENVIAR"):
        if pergunta.strip():
            with st.spinner("Launcerbot pensando..."):
                contexto_projeto = (
                    f"Nicho: {st.session_state.dados.get('nicho')}. "
                    f"E-book: {st.session_state.dados.get('nome_eb')}. "
                    f"Público: {st.session_state.dados.get('publico')}."
                )
                system = (
                    f"Você é o Launcerbot, assistente especialista em lançamentos digitais. "
                    f"O usuário se chama {st.session_state.usuario}. "
                    f"Contexto do projeto atual: {contexto_projeto}"
                )
                resp = chamar_ia(pergunta, system)
                st.session_state.chat_hist.append((pergunta, resp))
                # Incrementa a key para limpar o campo de texto
                st.session_state.chat_input_key += 1
                st.rerun()
        else:
            st.warning("Digite uma pergunta antes de enviar.")

    # Exibe histórico do chat
    if st.session_state.chat_hist:
        st.markdown("---")
        for q, r in reversed(st.session_state.chat_hist):
            st.markdown(f"**Você:** {q}")
            st.markdown(f"<div class='chat-bubble'>{r}</div>", unsafe_allow_html=True)

# --- RODAPÉ ---
st.markdown("<div class='footer'>© 2026 Nexus Launcher – Lançamento digital inteligente</div>", unsafe_allow_html=True)
