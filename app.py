import streamlit as st
from groq import Groq

# --- CONFIGURAÇÃO INICIAL ---
st.set_page_config(page_title="NEXUS LANCEUR", page_icon="🚀", layout="centered")

# --- ESTILO PERSONALIZADO ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background-color: #00BFFF !important; color: white !important; font-weight: bold; border: none; }
    .resumo-ia { background-color: #F8FAFC; padding: 20px; border-radius: 15px; border: 1px solid #E2E8F0; margin-top: 20px; }
    .footer { position: fixed; bottom: 0; left: 0; width: 100%; background-color: #00BFFF; color: white; text-align: center; padding: 5px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- CHAVE DE ACESSO ---
CHAVE_MESTRA = "NEXUS-PRO-2026"

if 'autenticado' not in st.session_state: st.session_state.autenticado = False
if 'etapa' not in st.session_state: st.session_state.etapa = "Login"
if 'dados' not in st.session_state: st.session_state.dados = {}
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

# --- FUNÇÃO IA ---
api_key = "SUA_CHAVE_AQUI" # <--- COLOQUE SUA CHAVE GSK AQUI

def gerar_ia(prompt, system="Você é o NEXUS LANCEUR, especialista em lançamentos do Quiz Mais Prêmios."):
    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile"
        )
        return response.choices[0].message.content
    except Exception as e: return f"Erro: Verifique sua chave API. {e}"

# --- 1. TELA DE LOGIN (NEXUS LANCEUR) ---
if not st.session_state.autenticado:
    st.title("🚀 NEXUS LANCEUR")
    st.subheader("Área restrita para associados do Quiz Mais Prêmios")
    
    with st.container():
        nome = st.text_input("Seu nome:")
        chave = st.text_input("Chave de ativação:", type="password")
        if st.button("ENTRAR"):
            if chave == CHAVE_MESTRA and nome:
                st.session_state.autenticado = True
                st.session_state.usuario = nome
                st.session_state.etapa = "Formulario"
                st.rerun()
            else:
                st.error("Chave inválida ou nome não preenchido.")
    st.stop()

# --- 2. FORMULÁRIO INTELIGENTE ---
if st.session_state.etapa == "Formulario":
    st.title("🚀 FORMULÁRIO INTELIGENTE DE FUNIL")
    st.write(f"Bem-vindo, {st.session_state.usuario}!")
    
    with st.form("form_parte1"):
        nicho = st.text_input("1. Nicho do produto (ex: dinheiro online, emagrecimento)")
        publico = st.text_input("2. Público-alvo (ex: iniciantes, frustrados)")
        st.info("3. Produto: E-books (Padrão)")
        objetivo = st.text_input("4. Objetivo principal (O resultado final)")
        promessa = st.text_input("5. Promessa do produto (Opcional)")
        preco = st.text_input("6. Preço do produto")
        
        gerar_analise = st.form_submit_button("GERAR INTELIGÊNCIA ESTRATÉGICA")
        
    if gerar_analise:
        with st.spinner("IA processando Parte 2..."):
            prompt = f"Com base no nicho {nicho} e público {publico}, gere: 1. Dor principal, 2. Objeções prováveis, 3. Desejo emocional, 4. Promessa forte, 5. Mecanismo único."
            st.session_state.dados = {
                "nicho": nicho, "publico": publico, "objetivo": objetivo, "preco": preco, 
                "promessa": promessa, "parte2": gerar_ia(prompt)
            }

    if "parte2" in st.session_state.dados:
        st.markdown("### 🧠 PARTE 2 — IA GERA AUTOMATICAMENTE")
        st.markdown(f"<div class='resumo-ia'>{st.session_state.dados['parte2']}</div>", unsafe_allow_html=True)
        if st.button("AVANÇAR PARA E-BOOK ➡️"):
            st.session_state.etapa = "Ebook"
            st.rerun()

# --- 3. CONFECCÃO E-BOOK ---
elif st.session_state.etapa == "Ebook":
    st.title("📦 GERE SEU E-BOOK PROFISSIONAL")
    if st.button("GERAR OS 60 CARTÕES"):
        with st.spinner("Escrevendo..."):
            st.session_state.dados['ebook'] = gerar_ia(f"Crie um roteiro de 60 cartões rápidos para um eBook de {st.session_state.dados['nicho']} focado em {st.session_state.dados['objetivo']}.")
    
    if 'ebook' in st.session_state.dados:
        st.text_area("Conteúdo Gerado:", st.session_state.dados['ebook'], height=300)
        if st.button("AVANÇAR PARA ANÚNCIO ➡️"):
            st.session_state.etapa = "Anuncio"
            st.rerun()

# --- 4. ANÚNCIO VSL ---
elif st.session_state.etapa == "Anuncio":
    st.title("🎬 GERE O ANÚNCIO EM VSL")
    if st.button("GERAR ANÚNCIO"):
        st.session_state.dados['anuncio'] = gerar_ia(f"Crie um script de VSL curta para Google Ads (Nicho: {st.session_state.dados['nicho']}). Termine com: 'CLIQUE EM SABER MAIS'.")
    
    if 'anuncio' in st.session_state.dados:
        st.text_area("Script:", st.session_state.dados['anuncio'], height=250)
        if st.button("AVANÇAR PARA LANDING PAGE ➡️"):
            st.session_state.etapa = "LP"
            st.rerun()

# --- 5. LANDING PAGE ---
elif st.session_state.etapa == "LP":
    st.title("🌐 GERE SUA LANDING PAGE")
    if st.button("GERAR PÁGINA"):
        st.session_state.dados['lp'] = gerar_ia(f"Crie uma LP de alta conversão para {st.session_state.dados['nicho']}.")
    
    if 'lp' in st.session_state.dados:
        st.text_area("Texto da LP:", st.session_state.dados['lp'], height=250)
        if st.button("AVANÇAR PARA LANÇAMENTO ➡️"):
            st.session_state.etapa = "Lancamento"
            st.rerun()

# --- 6. SEQUÊNCIA DE MENSAGENS ---
elif st.session_state.etapa == "Lancamento":
    st.title("📅 SEQUÊNCIA DE LANÇAMENTO")
    if st.button("GERAR SEQUÊNCIA + VSL FINAL"):
        template = f"Gere a descrição do grupo, mensagens do Dia 1 ao 6 e no Dia 7 o script VSL final para {st.session_state.dados['nicho']} custando {st.session_state.dados['preco']}."
        st.session_state.dados['final'] = gerar_ia(template)
    
    if 'final' in st.session_state.dados:
        st.text_area("Conteúdo Completo:", st.session_state.dados['final'], height=300)
        if st.button("💾 SALVAR PROJETO"):
            st.session_state.etapa = "Visualizacao"
            st.rerun()

# --- 7. VISUALIZAÇÃO FINAL ---
elif st.session_state.etapa == "Visualizacao":
    st.title("🚀 FUNIL COMPLETO (VERSÃO FINAL)")
    d = st.session_state.dados
    
    t1, t2, t3, t4, t5 = st.tabs(["📦 EBOOK", "🎬 ANÚNCIO", "🌐 LP", "📌 LANÇAMENTO", "🛠️ COMO APLICAR"])
    with t1: st.code(d.get('ebook', ''))
    with t2: st.code(d.get('anuncio', ''))
    with t3: st.code(d.get('lp', ''))
    with t4: st.code(d.get('final', ''))
    with t5: st.write("1. Ebook no Canva\n2. Anúncio no Google Ads\n3. LP de Captura\n4. Mensagens no Grupo.")

    st.markdown("---")
    st.subheader("💬 TEM ALGUMA DÚVIDA?")
    duvida = st.text_input("Digite aqui:")
    if st.button("ENVIAR"):
        st.session_state.chat_history.append(f"🤖: {gerar_ia(duvida)}")
    for msg in reversed(st.session_state.chat_history): st.write(msg)

st.markdown('<div class="footer">NEXUS LANCEUR - QUIZ MAIS PRÊMIOS</div>', unsafe_allow_html=True)
