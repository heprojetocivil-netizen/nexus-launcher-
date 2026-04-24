import streamlit as st
from groq import Groq
from datetime import timedelta

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="NEXUS LAUNCER", layout="wide")

# --- ESTILO CSS ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { display: none; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3.5em; background-color: #00BFFF !important; color: white !important; font-weight: bold; border: none; }
    .caixa-texto { background-color: #F8FAFC; padding: 25px; border-radius: 12px; border-left: 6px solid #00BFFF; margin-bottom: 20px; white-space: pre-wrap; color: #1E293B; line-height: 1.6; }
    .footer { text-align: center; padding: 60px; color: #94A3B8; font-size: 0.8em; opacity: 0.4; margin-top: 100px; font-style: italic; }
    .chat-bubble { background-color: #F1F5F9; padding: 15px; border-radius: 10px; border: 1px solid #E2E8F0; margin-bottom: 10px; }
    .btn-perigo>button { background-color: #ef4444 !important; height: 2em !important; }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO DE ESTADO ---
if 'etapa' not in st.session_state: st.session_state.etapa = "Login"
if 'dados' not in st.session_state: st.session_state.dados = {}
if 'projetos' not in st.session_state: st.session_state.projetos = {}
if 'chat_hist' not in st.session_state: st.session_state.chat_hist = []

# --- FUNÇÃO DE IA ---
def chamar_ia(prompt, system_prompt):
    try:
        client = Groq(api_key=st.session_state.api_key)
        response = client.chat.completions.create(
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Erro na API: {e}"

# --- COMPONENTES REUTILIZÁVEIS ---
def barra_navegacao():
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
                    st.session_state.dados = st.session_state.projetos[nome]
                    st.session_state.etapa = "Visualizacao"
                    st.rerun()
                st.markdown('<div class="btn-perigo">', unsafe_allow_html=True)
                if c_deletar.button("EXCLUIR", key=f"del_{nome}"):
                    del st.session_state.projetos[nome]
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

# --- FLUXO DE TELAS ---

if st.session_state.etapa == "Login":
    st.title("NEXUS LAUNCER")
    st.subheader("ACESSO RESTRITO A ASSOCIADOS DO QUIZ MAIS PRÊMIOS")
    st.session_state.usuario = st.text_input("Nome")
    st.session_state.api_key = st.text_input("Chave", type="password")
    if st.button("ENTRAR"):
        if st.session_state.usuario and st.session_state.api_key:
            st.session_state.etapa = "Formulario"
            st.rerun()

elif st.session_state.etapa == "Formulario":
    barra_navegacao()
    st.title("PREENCHA O FORMULÁRIO")
    d = st.session_state.dados
    d['nicho'] = st.text_input("Nicho:", help="ex: emagrecimento, renda extra")
    d['publico'] = st.text_input("Público-target:", help="ex: homens de 25 a 40")
    d['nome_eb'] = st.text_input("Nome do e-book:")
    d['dor'] = st.text_input("Principal dor que resolve:")
    d['atual'] = st.text_area("Situação atual da pessoa:")
    d['desejada'] = st.text_area("Situação desejada:")
    d['promessa'] = st.text_input("Promessa do e-book:")
    d['diferencial'] = st.text_input("Diferencial:")
    d['data_lancto'] = st.date_input("Data de lançamento")
    
    if st.button("AVANÇAR"):
        st.session_state.etapa = "Gerar_Ebook"
        st.rerun()

elif st.session_state.etapa == "Gerar_Ebook":
    barra_navegacao()
    st.title("📚 GERAR E-BOOK PROFISSIONAL")
    if st.button("GERAR E-BOOK – 60 CARTÕES"):
        prompt = f"Gere 60 cartões educativos para o e-book '{st.session_state.dados['nome_eb']}'. Dor: {st.session_state.dados['dor']}. Diferencial: {st.session_state.dados['diferencial']}."
        st.session_state.dados['ebook_cont'] = chamar_ia(prompt, "Você é um especialista em conteúdo digital.")
    
    if 'ebook_cont' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['ebook_cont']}</div>", unsafe_allow_html=True)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "Copy_Face"
            st.rerun()

elif st.session_state.etapa == "Copy_Face":
    barra_navegacao()
    st.title("📱 COPY PARA O FACEBOOK")
    if st.button("GERAR 5 VARIAÇÕES"):
        prompt = f"""Crie 5 variações de copy curta para Facebook Ads (o texto deve ser menor que uma LP). 
        Nicho: {st.session_state.dados['nicho']}. Lançamento: {st.session_state.dados['data_lancto']}. 
        OBRIGATÓRIO: 
        1. Identifique as variações com títulos em negrito como **Variação 1**, **Variação 2**, **Variação 3**, **Variação 4** e **Variação 5**. 
        2. Para CADA variação, inclua uma sugestão detalhada de imagem ou criativo visual que gere alta conversão.
        3. Ao final de cada variação, use EXATAMENTE esta chamada para ação: ⬇️ Clique abaixo e descubra como. 
        4. Separe parágrafos com linha em branco."""
        st.session_state.dados['fb_copy'] = chamar_ia(prompt, "Você é um copywriter especialista em anúncios diretos e curtos para Facebook Ads.")
    
    if 'fb_copy' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['fb_copy']}</div>", unsafe_allow_html=True)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "Copy_LP"
            st.rerun()

elif st.session_state.etapa == "Copy_LP":
    barra_navegacao()
    st.title("🌐 COPY PARA A LANDING PAGE")
    if st.button("GERAR 5 VARIAÇÕES LP"):
        prompt = f"Crie 5 variações de copy para Landing Page. Situação atual: {st.session_state.dados['atual']}. Situação desejada: {st.session_state.dados['desejada']}. Promessa: {st.session_state.dados['promessa']}. Sugira imagens."
        st.session_state.dados['lp_copy'] = chamar_ia(prompt, "Você é um especialista em Landing Pages. OBRIGATÓRIO: Identifique cada variação com título em negrito (ex: **Variação 1: [Nome]**). Ao final de cada variação, inclua o botão [ ENTRAR NO GRUPO ].")
    
    if 'lp_copy' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['lp_copy']}</div>", unsafe_allow_html=True)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "Mensagens_Grupo"
            st.rerun()

elif st.session_state.etapa == "Mensagens_Grupo":
    barra_navegacao()
    st.title("📌 MENSAGENS PARA O GRUPO")
    
    nicho = st.session_state.dados['nicho']
    data = st.session_state.dados['data_lancto'].strftime('%d/%m/%Y')
    resultado = st.session_state.dados['promessa']
    dor = st.session_state.dados['dor']
    data_ontem = (st.session_state.dados['data_lancto'] - timedelta(days=1)).strftime('%d/%m/%Y')

    msg_template = f"""
**Descrição do grupo:**
Este grupo é silencioso. Você não será incomodado.
Aqui você receberá apenas conteúdos e avisos relacionados ao tema.

---

**📩 Mensagem 1 – Boas-vindas + Pré-lançamento**
Bem-vindo(a) 👋
Este grupo é silencioso, então pode ficar tranquilo(a), você não será incomodado.
Você entrou aqui porque quer aprender mais sobre {nicho} — e eu preparei algo direto ao ponto pra isso.
📅 No dia {data}, eu vou liberar um conteúdo exclusivo onde mostro um método simples que pode te ajudar a {resultado}.
Fica por aqui… porque o que eu vou mostrar pode mudar a forma como você enxerga isso.

**⏳ Mensagem 2 – 1 dia antes (aquecimento)**
Amanhã é o dia.
Depois de organizar tudo, finalmente vou liberar o conteúdo sobre {nicho}.
Se você sente que ainda está travado(a) em {dor}, presta atenção nisso…
O que você vai ver amanhã não é teoria — é um caminho direto que você pode aplicar.
⏰ Fica atento(a), porque vou liberar aqui no grupo.

**🚀 Mensagem 3 – Lançamento (com link Monetizze)**
Chegou o momento.
Como prometido, acabei de liberar o conteúdo completo.
Nele, eu mostro exatamente como você pode aprender o passo a passo que pode te ajudar a {resultado}, mesmo começando do zero.
Se você quer parar de {dor} e finalmente ter resultado em {nicho}, esse é o próximo passo:
👉 [LINK DA MONETIZZE]
A partir de agora, está disponível — mas não sei por quanto tempo vou deixar assim.
"""
    st.session_state.dados['msg_grupo'] = msg_template
    st.session_state.dados['dicas'] = "Texto genérico: Para aplicar este lançamento, foque em tráfego pago para o grupo de WhatsApp nos primeiros 7 dias..."
    
    st.markdown(f"<div class='caixa-texto'>{msg_template}</div>", unsafe_allow_html=True)
    
    if st.button("💾 SALVAR PROJETO"):
        st.session_state.projetos[st.session_state.dados['nome_eb']] = st.session_state.dados
        st.session_state.etapa = "Visualizacao"
        st.rerun()

elif st.session_state.etapa == "Visualizacao":
    barra_navegacao()
    st.title(f"PROJETO: {st.session_state.dados.get('nome_eb')}")
    
    with st.expander("📚 E-BOOKS"):
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('ebook_cont')}</div>", True)
    
    with st.expander("🎬 ANUNCIO"):
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('fb_copy')}</div>", True)
        
    with st.expander("🌐 LANDING PAGE"):
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('lp_copy')}</div>", True)

    with st.expander("📌 MENSAGENS"):
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('msg_grupo')}</div>", True)
        
    with st.expander("💡 DICAS PARA APLICAÇÃO"):
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('dicas')}</div>", True)

    st.divider()
    st.markdown("### Olá 👋")
    st.info("**Eu sou o Launcerbot.** Eu ajudo pessoas a criar e lançar produtos digitais, mesmo começando do zero. Se você quer vender na internet, pode me perguntar qualquer coisa 👇")
    
    pergunta = st.text_input("Sua pergunta:")
    if pergunta:
        resp = chamar_ia(pergunta, f"Você é o Launcerbot. O usuário é {st.session_state.usuario}.")
        st.session_state.chat_hist.append((pergunta, resp))
    
    for q, r in reversed(st.session_state.chat_hist):
        st.markdown(f"**Você:** {q}")
        st.markdown(f"<div class='chat-bubble'>{r}</div>", unsafe_allow_html=True)

# --- RODAPÉ MARCA D'ÁGUA ---
st.markdown("<div class='footer'>© 2026 Nexus Launcer – Lançamento digital inteligente</div>", unsafe_allow_html=True)
