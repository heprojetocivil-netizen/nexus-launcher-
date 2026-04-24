import streamlit as st
from groq import Groq
from datetime import timedelta

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="NEXUS LAUNCER", layout="wide")

# --- CSS ---
st.markdown("""
<style>
[data-testid="stSidebar"] { display: none; }
.stButton>button { width: 100%; border-radius: 8px; height: 3.5em; background-color: #00BFFF !important; color: white !important; font-weight: bold; border: none; }
.caixa-texto { background-color: #F8FAFC; padding: 25px; border-radius: 12px; border-left: 6px solid #00BFFF; margin-bottom: 20px; white-space: pre-wrap; color: #1E293B; }
.chat-bubble { background-color: #F1F5F9; padding: 15px; border-radius: 10px; border: 1px solid #E2E8F0; margin-bottom: 10px; }
.footer { text-align: center; padding: 40px; opacity: 0.3; }
</style>
""", unsafe_allow_html=True)

# --- ESTADO ---
if 'etapa' not in st.session_state: st.session_state.etapa = "Login"
if 'dados' not in st.session_state: st.session_state.dados = {}
if 'chat_hist' not in st.session_state: st.session_state.chat_hist = []

# --- IA ---
def chamar_ia(prompt, system_prompt):
    try:
        client = Groq(api_key=st.session_state.api_key)

        messages = [{"role": "system", "content": system_prompt}]
        for q, r in st.session_state.chat_hist:
            messages.append({"role": "user", "content": q})
            messages.append({"role": "assistant", "content": r})
        messages.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"Erro: {e}"

# --- LOGIN ---
if st.session_state.etapa == "Login":
    st.title("NEXUS LAUNCER")

    st.session_state.usuario = st.text_input("Nome")
    st.session_state.api_key = st.text_input("Chave API", type="password")

    if st.button("ENTRAR"):
        if not st.session_state.usuario or not st.session_state.api_key:
            st.warning("Preencha todos os campos.")
        else:
            st.session_state.etapa = "Formulario"
            st.rerun()

# --- FORMULÁRIO ---
elif st.session_state.etapa == "Formulario":
    st.title("PREENCHA O FORMULÁRIO")

    d = st.session_state.dados

    d['nicho'] = st.text_input("Nicho")
    d['nome_eb'] = st.text_input("Nome do e-book")
    d['dor'] = st.text_input("Dor principal")
    d['promessa'] = st.text_input("Promessa")
    d['data_lancto'] = st.date_input("Data lançamento")

    if st.button("AVANÇAR"):
        if not d.get('nicho') or not d.get('nome_eb'):
            st.warning("Preencha pelo menos nicho e nome.")
        else:
            st.session_state.etapa = "Gerar_Ebook"
            st.rerun()

# --- GERAR EBOOK ---
elif st.session_state.etapa == "Gerar_Ebook":
    st.title("GERAR EBOOK")

    if st.button("GERAR"):
        with st.spinner("Gerando conteúdo..."):
            prompt = f"""
            Crie 60 cartões educativos extremamente práticos.
            Nicho: {st.session_state.dados['nicho']}
            Dor: {st.session_state.dados['dor']}
            Promessa: {st.session_state.dados['promessa']}

            Seja direto, use linguagem simples e gere valor real.
            """
            st.session_state.dados['ebook'] = chamar_ia(prompt, "Especialista em conteúdo")

    if 'ebook' in st.session_state.dados:
        st.markdown(st.session_state.dados['ebook'])

        if st.button("PRÓXIMO"):
            st.session_state.etapa = "Copy"
            st.rerun()

# --- COPY ---
elif st.session_state.etapa == "Copy":
    st.title("COPY FACEBOOK")

    if st.button("GERAR COPY"):
        with st.spinner("Criando anúncios..."):
            prompt = f"""
            Crie 3 anúncios curtos e diretos.
            Nicho: {st.session_state.dados['nicho']}

            Use:
            - Dor
            - Curiosidade
            - CTA forte
            """
            st.session_state.dados['copy'] = chamar_ia(prompt, "Copywriter especialista")

    if 'copy' in st.session_state.dados:
        st.markdown(st.session_state.dados['copy'])

        if st.button("PRÓXIMO"):
            st.session_state.etapa = "Grupo"
            st.rerun()

# --- MENSAGENS ---
elif st.session_state.etapa == "Grupo":
    st.title("MENSAGENS WHATSAPP")

    data = st.session_state.dados.get('data_lancto')

    if data:
        data_format = data.strftime('%d/%m/%Y')
    else:
        data_format = "EM BREVE"

    msg = f"""
Bem-vindo 👋

📅 Dia {data_format} teremos o lançamento

Fique atento.
"""

    st.markdown(msg)

# --- CHAT ---
st.divider()
st.markdown("### Chat")

pergunta = st.text_input("Pergunte algo")

if pergunta:
    resposta = chamar_ia(pergunta, "Você é especialista em lançamentos")
    st.session_state.chat_hist.append((pergunta, resposta))

for q, r in reversed(st.session_state.chat_hist):
    st.markdown(f"**Você:** {q}")
    st.markdown(f"<div class='chat-bubble'>{r}</div>", unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("<div class='footer'>NEXUS LAUNCER</div>", unsafe_allow_html=True)
