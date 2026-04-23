import streamlit as st
from groq import Groq

# --- CONFIGURAÇÃO NEXUS LANCEUR ---
st.set_page_config(page_title="NEXUS LANCEUR", page_icon="🚀", layout="wide")

# --- SISTEMA DE CHAVE DE ACESSO ---
CHAVE_MESTRA = "NEXUS-PRO-2026"

if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🔐 ACESSO RESTRITO - NEXUS LANCEUR")
    chave_input = st.text_input("Insira sua Chave de Ativação:", type="password")
    if st.button("ATIVAR SISTEMA"):
        if chave_input == CHAVE_MESTRA:
            st.session_state.autenticado = True
            st.success("Acesso Liberado!")
            st.rerun()
        else:
            st.error("Chave inválida. Fale com o administrador.")
    st.stop()

# --- INICIALIZAÇÃO DE ESTADOS ---
if 'projetos' not in st.session_state: st.session_state.projetos = {}
if 'etapa' not in st.session_state: st.session_state.etapa = "Novo Projeto"
if 'dados' not in st.session_state: st.session_state.dados = {}
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

# --- COLOQUE SUA CHAVE DA GROQ ABAIXO ---
api_key = "COLOQUE_SUA_CHAVE_AQUI"

def gerar_ia(prompt, system="Você é o NEXUS LANCEUR, mestre em lançamentos e copywriter de elite."):
    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile"
        )
        return response.choices[0].message.content
    except Exception as e: return f"Erro na IA: {e}"

# --- ESTILO ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; background-color: #00BFFF !important; color: white !important; font-weight: bold; }
    .resumo-ia { background-color: #F1F5F9; padding: 20px; border-radius: 10px; border-left: 5px solid #00BFFF; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("📂 NEXUS LANCEUR")
    st.info(f"Usuário: Orlando Rousseau")
    st.subheader("PROJETOS SALVOS")
    for p_nome in list(st.session_state.projetos.keys()):
        if st.button(f"📌 {p_nome}"):
            st.session_state.dados = st.session_state.projetos[p_nome]
            st.session_state.etapa = "Projeto Final"
            st.rerun()
    st.markdown("---")
    if st.button("➕ NOVO PROJETO"):
        st.session_state.etapa = "Novo Projeto"
        st.session_state.dados = {}
        st.session_state.chat_history = []
        st.rerun()

# --- FLUXO ---

if st.session_state.etapa == "Novo Projeto":
    st.title("🚀 FORMULÁRIO INTELIGENTE NEXUS LANCEUR")
    with st.form("f1"):
        col1, col2 = st.columns(2)
        with col1:
            n_p = st.text_input("Nome do Projeto")
            nicho = st.text_input("Nicho do Produto")
            publico = st.text_input("Público-alvo")
            tipo = st.text_input("Tipo de Produto")
        with col2:
            objetivo = st.text_input("Objetivo Principal")
            experiencia = st.selectbox("Nível de experiência", ["Iniciante", "Já testei", "Já tive resultados"])
            preco = st.text_input("Preço")
            garantia = st.text_input("Garantia")
        
        if st.form_submit_button("AVANÇAR"):
            with st.spinner("🤖 Gerando Estratégia..."):
                p = f"Analise o nicho {nicho} e público {publico} e crie: 1. Dor central REAL, 2. Objeções específicas, 3. Desejo emocional profundo, 4. Promessa forte, 5. Mecanismo único, 6. Ângulo de ataque."
                st.session_state.dados = {"nome": n_p, "nicho": nicho, "publico": publico, "tipo": tipo, "objetivo": objetivo, "analise_ia": gerar_ia(p), "preco": preco, "garantia": garantia}
                st.session_state.etapa = "Confeccao Ebook"
                st.rerun()

elif st.session_state.etapa == "Confeccao Ebook":
    st.title("📦 GERE SEU E-BOOK PROFISSIONAL")
    st.markdown(f"<div class='resumo-ia'><b>ESTRATÉGIA GERADA:</b><br>{st.session_state.dados['analise_ia']}</div>", unsafe_allow_html=True)
    if st.button("GERAR 60 CARTÕES"):
        st.session_state.dados['ebook'] = gerar_ia(f"Crie 60 cartões rápidos para um {st.session_state.dados['tipo']} de {st.session_state.dados['nicho']}.")
    
    if 'ebook' in st.session_state.dados:
        st.text_area("Conteúdo:", st.session_state.dados['ebook'], height=300)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "Gere Anuncio"
            st.rerun()

elif st.session_state.etapa == "Gere Anuncio":
    st.title("🎬 ANÚNCIO (GOOGLE ADS)")
    if st.button("GERAR ANÚNCIO"):
        st.session_state.dados['anuncio'] = gerar_ia(f"Crie um script de VSL para Google Ads (Nicho: {st.session_state.dados['nicho']}). Termine com: 'CLIQUE EM SABER MAIS'.")
    
    if 'anuncio' in st.session_state.dados:
        st.text_area("Script:", st.session_state.dados['anuncio'], height=250)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "Gere LP"
            st.rerun()

elif st.session_state.etapa == "Gere LP":
    st.title("🌐 LANDING PAGE")
    if st.button("GERAR TEXTO DA PÁGINA"):
        st.session_state.dados['lp'] = gerar_ia(f"Crie uma LP de captura para {st.session_state.dados['nicho']} baseada na dor: {st.session_state.dados['analise_ia']}.")
    
    if 'lp' in st.session_state.dados:
        st.text_area("LP:", st.session_state.dados['lp'], height=250)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "Sequencia Mensagens"
            st.rerun()

elif st.session_state.etapa == "Sequencia Mensagens":
    st.title("📌 LANÇAMENTO + VSL FINAL")
    if st.button("GERAR SEQUÊNCIA + VSL"):
        vsl_template = f"Roteiro: 'Você percebeu que... nada muda? O erro é fazer igual. Meu método 👉 [MECANISMO] resolve. Teste por {st.session_state.dados['garantia']}. Acesso por {st.session_state.dados['preco']}. Clique no link.'"
        st.session_state.dados['mensagens'] = gerar_ia(f"Crie 6 mensagens e a VSL final usando este modelo: {vsl_template}")
    
    if 'mensagens' in st.session_state.dados:
        st.text_area("Final:", st.session_state.dados['mensagens'], height=300)
        if st.button("SALVAR PROJETO"):
            st.session_state.projetos[st.session_state.dados['nome']] = st.session_state.dados
            st.session_state.etapa = "Projeto Final"
            st.rerun()

elif st.session_state.etapa == "Projeto Final":
    d = st.session_state.dados
    st.title(f"🚀 NEXUS LANCEUR: {d['nome']}")
    with st.expander("📦 EBOOK"): st.code(d.get('ebook', ''))
    with st.expander("🎬 ANÚNCIO"): st.code(d.get('anuncio', ''))
    with st.expander("🌐 LANDING PAGE"): st.code(d.get('lp', ''))
    with st.expander("📌 LANÇAMENTO + VSL"): st.code(d.get('mensagens', ''))
    
    st.markdown("---")
    st.subheader("💬 SUPORTE")
    duvida = st.text_input("Dúvida?")
    if st.button("Enviar"):
        st.session_state.chat_history.append(f"🤖: {gerar_ia(duvida)}")
    for m in reversed(st.session_state.chat_history): st.write(m)

st.markdown('<div style="position: fixed; bottom: 0; left: 0; width: 100%; background-color: #00BFFF; color: white; text-align: center; padding: 5px;">NEXUS LANCEUR - PROTEGIDO</div>', unsafe_allow_html=True)
