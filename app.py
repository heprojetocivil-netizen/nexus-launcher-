import streamlit as st
from groq import Groq

# --- CONFIGURAÇÃO NEXUS LANCEUR ---
st.set_page_config(page_title="NEXUS LANCEUR", page_icon="🚀", layout="wide")

# --- SISTEMA DE CHAVE DE ACESSO (O SITE TRAVA AQUI) ---
CHAVE_MESTRA = "NEXUS-PRO-2026"

if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🔐 ACESSO RESTRITO - NEXUS LANCEUR")
    st.markdown("---")
    chave_input = st.text_input("Insira sua Chave de Ativação:", type="password")
    if st.button("ATIVAR SISTEMA"):
        if chave_input == CHAVE_MESTRA:
            st.session_state.autenticado = True
            st.success("Acesso Liberado! Carregando...")
            st.rerun()
        else:
            st.error("Chave inválida. Fale com Orlando Rousseau.")
    st.stop()

# --- INICIALIZAÇÃO DE ESTADOS ---
if 'projetos' not in st.session_state: st.session_state.projetos = {}
if 'etapa' not in st.session_state: st.session_state.etapa = "Novo Projeto"
if 'dados' not in st.session_state: st.session_state.dados = {}
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

# --- CONFIGURAÇÃO DA IA (GROQ) ---
# SUBSTITUA ABAIXO PELA SUA CHAVE gsk_...
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

# --- ESTILO VISUAL ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 8px; height: 3.5em; background-color: #00BFFF !important; color: white !important; font-weight: bold; }
    .resumo-ia { background-color: #F1F5F9; padding: 20px; border-radius: 10px; border-left: 5px solid #00BFFF; margin-bottom: 20px; color: #1E293B; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("📂 NEXUS LANCEUR")
    st.info(f"Usuário: Orlando Rousseau")
    st.markdown("---")
    st.subheader("MEUS PROJETOS")
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

# --- FLUXO DE ETAPAS ---

# 1. FORMULÁRIO (PARTE 1)
if st.session_state.etapa == "Novo Projeto":
    st.title("🚀 FORMULÁRIO INTELIGENTE NEXUS")
    with st.form("f1"):
        col1, col2 = st.columns(2)
        with col1:
            n_p = st.text_input("Nome do Projeto")
            nicho = st.text_input("Nicho do Produto")
            publico = st.text_input("Público-alvo")
            tipo = st.text_input("Tipo de Produto (eBook, Guia, etc)")
        with col2:
            objetivo = st.text_input("Objetivo Principal")
            experiencia = st.selectbox("Nível de experiência", ["Iniciante", "Já testei", "Já tive resultados"])
            preco = st.text_input("Preço do Produto")
            garantia = st.text_input("Garantia (ex: 7 dias)")
        
        if st.form_submit_button("AVANÇAR"):
            with st.spinner("🤖 Gerando Estratégia de IA (Parte 2)..."):
                p = f"Nicho: {nicho}, Público: {publico}. Crie: 1. Dor central REAL, 2. Objeções específicas, 3. Desejo emocional profundo, 4. Promessa forte, 5. Mecanismo único (Dê um nome), 6. Ângulo de ataque."
                st.session_state.dados = {
                    "nome": n_p, "nicho": nicho, "publico": publico, "tipo": tipo, 
                    "objetivo": objetivo, "analise_ia": gerar_ia(p), "preco": preco, "garantia": garantia
                }
                st.session_state.etapa = "Confeccao Ebook"
                st.rerun()

# 2. EBOOK
elif st.session_state.etapa == "Confeccao Ebook":
    st.title("📦 GERE SEU E-BOOK PROFISSIONAL")
    st.markdown(f"<div class='resumo-ia'><b>ESTRATÉGIA DEFINIDA:</b><br>{st.session_state.dados['analise_ia']}</div>", unsafe_allow_html=True)
    if st.button("✨ GERAR 60 CARTÕES"):
        st.session_state.dados['ebook'] = gerar_ia(f"Crie um roteiro de 60 cartões rápidos para um {st.session_state.dados['tipo']} de {st.session_state.dados['nicho']} focado em {st.session_state.dados['objetivo']}.")
    
    if 'ebook' in st.session_state.dados:
        st.text_area("Roteiro do E-book:", st.session_state.dados['ebook'], height=300)
        if st.button("AVANÇAR PARA O ANÚNCIO ➡️"):
            st.session_state.etapa = "Gere Anuncio"
            st.rerun()

# 3. ANÚNCIO GOOGLE
elif st.session_state.etapa == "Gere Anuncio":
    st.title("🎬 ANÚNCIO (GOOGLE ADS)")
    if st.button("✨ GERAR SCRIPT DE ANÚNCIO"):
        st.session_state.dados['anuncio'] = gerar_ia(f"Crie um script de VSL curta para anúncio no Google Ads para o nicho {st.session_state.dados['nicho']}. Termine com: 'CLIQUE EM SABER MAIS'.")
    
    if 'anuncio' in st.session_state.dados:
        st.text_area("Script:", st.session_state.dados['anuncio'], height=250)
        if st.button("AVANÇAR PARA LANDING PAGE ➡️"):
            st.session_state.etapa = "Gere LP"
            st.rerun()

# 4. LANDING PAGE
elif st.session_state.etapa == "Gere LP":
    st.title("🌐 LANDING PAGE")
    if st.button("✨ GERAR TEXTO DA PÁGINA"):
        st.session_state.dados['lp'] = gerar_ia(f"Crie uma LP de captura para {st.session_state.dados['nicho']} focada em converter {st.session_state.dados['publico']}.")
    
    if 'lp' in st.session_state.dados:
        st.text_area("Conteúdo LP:", st.session_state.dados['lp'], height=250)
        if st.button("AVANÇAR PARA MENSAGENS ➡️"):
            st.session_state.etapa = "Sequencia Mensagens"
            st.rerun()

# 5. MENSAGENS E VSL FINAL
elif st.session_state.etapa == "Sequencia Mensagens":
    st.title("📌 LANÇAMENTO + VSL FINAL")
    if st.button("✨ GERAR SEQUÊNCIA COMPLETA"):
        vsl_template = f"""
        Personalize este roteiro: 'Você percebeu que... nada muda? O erro é fazer mais do mesmo. 
        Eu organizei o método 👉 [NOME DO MECANISMO]. Sem enrolação. Teste por {st.session_state.dados['garantia']}. 
        Acesso agora por apenas {st.session_state.dados['preco']}. Clique no link da descrição.'
        """
        st.session_state.dados['mensagens'] = gerar_ia(f"Gere 6 mensagens de aquecimento e o roteiro da VSL final baseado nisto: {vsl_template}")
    
    if 'mensagens' in st.session_state.dados:
        st.text_area("Lançamento Completo:", st.session_state.dados['mensagens'], height=300)
        if st.button("💾 SALVAR E FINALIZAR PROJETO"):
            st.session_state.projetos[st.session_state.dados['nome']] = st.session_state.dados
            st.session_state.etapa = "Projeto Final"
            st.rerun()

# 6. VISUALIZAÇÃO FINAL
elif st.session_state.etapa == "Projeto Final":
    d = st.session_state.dados
    st.title(f"🚀 PROJETO FINALIZADO: {d['nome']}")
    
    with st.expander("📦 EBOOK (60 CARTÕES)"): st.code(d.get('ebook', ''))
    with st.expander("🎬 ANÚNCIO (GOOGLE ADS)"): st.code(d.get('anuncio', ''))
    with st.expander("🌐 LANDING PAGE"): st.code(d.get('lp', ''))
    with st.expander("📌 MENSAGENS + VSL FINAL"): st.code(d.get('mensagens', ''))
    
    st.markdown("---")
    st.subheader("💬 SUPORTE CONTÍNUO")
    duvida = st.text_input("Dúvida?")
    if st.button("Enviar"):
        resp = gerar_ia(f"Dúvida sobre projeto {d['nome']}: {duvida}")
        st.session_state.chat_history.append(f"🤖: {resp}")
    for m in reversed(st.session_state.chat_history): st.write(m)

st.markdown('<div style="position: fixed; bottom: 0; left: 0; width: 100%; background-color: #00BFFF; color: white; text-align: center; padding: 5px; font-weight: bold;">NEXUS LANCEUR - SISTEMA PROTEGIDO</div>', unsafe_allow_html=True)
