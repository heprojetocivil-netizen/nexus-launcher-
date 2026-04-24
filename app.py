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
    .footer { text-align: center; padding: 30px; color: #94A3B8; font-size: 0.8em; opacity: 0.6; }
    .chat-bubble { background-color: #F1F5F9; padding: 15px; border-radius: 10px; margin-bottom: 10px; border: 1px solid #E2E8F0; }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO DE ESTADO ---
if 'etapa' not in st.session_state: st.session_state.etapa = "Login"
if 'dados' not in st.session_state: st.session_state.dados = {}
if 'projetos' not in st.session_state: st.session_state.projetos = {}
if 'chat_hist' not in st.session_state: st.session_state.chat_hist = []

# --- FUNÇÕES DE APOIO ---
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

def barra_topo():
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ INICIAR NOVO PROJETO"):
            st.session_state.dados = {}
            st.session_state.etapa = "Formulario"
            st.rerun()
    with col2:
        with st.expander("📂 MEUS PROJETOS"):
            if not st.session_state.projetos: st.write("Nenhum projeto.")
            for nome in list(st.session_state.projetos.keys()):
                c_abrir, c_del = st.columns([3, 1])
                if c_abrir.button(f"📄 {nome}", key=f"ab_{nome}"):
                    st.session_state.dados = st.session_state.projetos[nome]
                    st.session_state.etapa = "Visualizacao"
                    st.rerun()
                if c_del.button("🗑️", key=f"del_{nome}"):
                    del st.session_state.projetos[nome]
                    st.rerun()

# --- TELAS ---

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
    barra_topo()
    st.title("PREENCHA O FORMULÁRIO")
    d = st.session_state.dados
    d['nicho'] = st.text_input("Nicho:", help="ex: emagrecimento, renda extra")
    d['publico'] = st.text_input("Público-alvo:", help="ex: homens de 25 a 40")
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
    barra_topo()
    st.title("📚 GERAR E-BOOK PROFISSIONAL")
    if st.button("GERAR CONTEÚDO - 60 CARTÕES"):
        prompt = f"Gere 60 cartões de conteúdo para o e-book {st.session_state.dados['nome_eb']}. Público: {st.session_state.dados['publico']}. Dor: {st.session_state.dados['dor']}. Diferencial: {st.session_state.dados['diferencial']}."
        st.session_state.dados['ebook'] = chamar_ia(prompt, "Você é um especialista em criação de produtos digitais.")
    
    if 'ebook' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['ebook']}</div>", unsafe_allow_html=True)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "Gerar_Face"
            st.rerun()

elif st.session_state.etapa == "Gerar_Face":
    barra_topo()
    st.title("📱 COPY PARA FACEBOOK")
    if st.button("GERAR 5 VARIAÇÕES"):
        prompt = f"Crie 5 variações de copy para Facebook Ads. Nicho: {st.session_state.dados['nicho']}. Promessa: {st.session_state.dados['promessa']}. Data: {st.session_state.dados['data_lancto']}. Leve para a Landing Page. Separe em parágrafos e sugira imagens para cada uma."
        st.session_state.dados['face'] = chamar_ia(prompt, "Você é um copywriter expert em Facebook Ads.")
    
    if 'face' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['face']}</div>", unsafe_allow_html=True)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "Gerar_LP"
            st.rerun()

elif st.session_state.etapa == "Gerar_LP":
    barra_topo()
    st.title("🌐 COPY PARA LANDING PAGE")
    if st.button("GERAR ROTEIRO LP"):
        prompt = f"Crie uma copy de Landing Page de alta conversão. Situação atual: {st.session_state.dados['atual']}. Situação desejada: {st.session_state.dados['desejada']}. Promessa: {st.session_state.dados['promessa']}. Botão: ENTRAR NO GRUPO. Sugira imagens."
        st.session_state.dados['lp'] = chamar_ia(prompt, "Você é um especialista em Landing Pages.")
    
    if 'lp' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['lp']}</div>", unsafe_allow_html=True)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "Gerar_Mensagens"
            st.rerun()

elif st.session_state.etapa == "Gerar_Mensagens":
    barra_topo()
    st.title("📌 MENSAGENS PARA O GRUPO")
    
    nicho = st.session_state.dados['nicho']
    data = st.session_state.dados['data_lancto'].strftime('%d/%m/%Y')
    resultado = st.session_state.dados['promessa']
    dor = st.session_state.dados['dor']
    data_ontem = (st.session_state.dados['data_lancto'] - timedelta(days=1)).strftime('%d/%m/%Y')

    st.session_state.dados['msg'] = f"""
**Descrição do Grupo:**
Este grupo é silencioso. Você não será incomodado.
Aqui você receberá apenas conteúdos e avisos relacionados ao tema.

---
**📩 Mensagem 1 – Boas-vindas + Pré-lançamento**
Bem-vindo(a) 👋
Este grupo é silencioso, então pode ficar tranquilo(a), você não será incomodado.
Você entrou aqui porque quer aprender mais sobre {nicho} — e eu preparei algo direto ao ponto pra isso.
📅 No dia {data}, eu vou liberar um conteúdo exclusivo onde mostro um método simples que pode te ajudar a {resultado}.
Fica por aqui… porque o que eu vou mostrar pode mudar a forma como você enxerga isso.

---
**⏳ Mensagem 2 – {data_ontem} (Aquecimento)**
Amanhã é o dia.
Depois de organizar tudo, finalmente vou liberar o conteúdo sobre {nicho}.
Se você sente que ainda está travado(a) em {dor}, presta atenção nisso…
O que você vai ver amanhã não é teoria — é um caminho direto que você pode aplicar.
⏰ Fica atento(a), porque vou liberar aqui no grupo.

---
**🚀 Mensagem 3 – Lançamento**
Chegou o momento.
Como prometido, acabei de liberar o conteúdo completo.
Nele, eu mostro exatamente como você pode {resultado}, mesmo começando do zero.
Se você quer parar de {dor} e finalmente ter resultado em {nicho}, esse é o próximo passo:
👉 [LINK DA MONETIZZE]
A partir de agora, está disponível — mas não sei por quanto tempo vou deixar assim.
"""
    st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['msg']}</div>", unsafe_allow_html=True)
    
    if st.button("💾 SALVAR PROJETO"):
        st.session_state.projetos[st.session_state.dados['nome_eb']] = st.session_state.dados
        st.session_state.etapa = "Visualizacao"
        st.rerun()

elif st.session_state.etapa == "Visualizacao":
    barra_topo()
    st.title(f"PROJETO: {st.session_state.dados.get('nome_eb')}")
    
    with st.expander("E-BOOKS"): st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('ebook')}</div>", True)
    with st.expander("ANUNCIO"): st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('face')}</div>", True)
    with st.expander("LANDING PAGE"): st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('lp')}</div>", True)
    with st.expander("MENSAGENS"): st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('msg')}</div>", True)

    st.divider()
    st.subheader("Olá 👋 Eu sou o Launcerbot.")
    st.info("Eu ajudo pessoas a criar e lançar produtos digitais, mesmo começando do zero. Se você quer vender na internet, pode me perguntar qualquer coisa 👇")
    
    pergunta = st.text_input("Sua dúvida:")
    if pergunta:
        resp = chamar_ia(pergunta, "Você é o Launcerbot, especialista em vendas online.")
        st.session_state.chat_hist.append((pergunta, resp))
    
    for q, r in reversed(st.session_state.chat_hist):
        st.markdown(f"**Você:** {q}")
        st.markdown(f"<div class='chat-bubble'>{r}</div>", unsafe_allow_html=True)

# --- RODAPÉ ---
st.markdown("<div class='footer'>© 2026 Nexus Launcer – Lançamento digital inteligente</div>", unsafe_allow_html=True)
