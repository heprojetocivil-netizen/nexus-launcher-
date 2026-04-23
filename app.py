import streamlit as st
from groq import Groq

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="LANÇAMENTO INTELIGENTE", page_icon="🚀", layout="wide")

if 'projetos' not in st.session_state: st.session_state.projetos = {}
if 'etapa' not in st.session_state: st.session_state.etapa = "Novo Projeto"
if 'dados' not in st.session_state: st.session_state.dados = {}
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

api_key = "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"

def gerar_ia(prompt, system="Você é um mestre em lançamentos de eBooks e copywriter de alta conversão."):
    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile"
        )
        return response.choices[0].message.content
    except Exception as e: return f"Erro: {e}"

# --- ESTILO ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; background-color: #00BFFF !important; color: white !important; font-weight: bold; }
    .main-card { background-color: #F8FAFC; padding: 20px; border-radius: 15px; border: 1px solid #E2E8F0; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("📂 MEUS PROJETOS")
    for p_nome in st.session_state.projetos.keys():
        if st.button(f"📌 {p_nome}"):
            st.session_state.dados = st.session_state.projetos[p_nome]
            st.session_state.etapa = "Projeto Final"
            st.rerun()
    st.markdown("---")
    if st.button("➕ NOVO PROJETO"):
        st.session_state.etapa = "Novo Projeto"
        st.session_state.dados = {}
        st.rerun()

# --- FLUXO DE ETAPAS ---

# 1. FORMULÁRIO
if st.session_state.etapa == "Novo Projeto":
    st.title("🚀 FORMULÁRIO INTELIGENTE DE FUNIL")
    with st.form("f1"):
        col1, col2 = st.columns(2)
        with col1:
            n_p = st.text_input("Nome do Projeto")
            nicho = st.text_input("Nicho do Produto")
            publico = st.text_input("Público-alvo")
            tipo = st.text_input("Tipo de Produto (ex: eBook, Guia)")
            objetivo = st.text_input("Objetivo Principal (Resultado)")
        with col2:
            experiencia = st.selectbox("Seu nível de experiência", ["Iniciante", "Já testei", "Já tive resultados"])
            promessa_opc = st.text_input("Promessa do produto (opcional)")
            preco = st.text_input("Preço do Produto")
            garantia = st.text_input("Garantia")
        
        if st.form_submit_button("AVANÇAR"):
            with st.spinner("IA Gerando Inteligência..."):
                p = f"Com base no nicho {nicho}, público {publico} e objetivo {objetivo}, crie: 1. Dor principal, 2. Objeções prováveis, 3. Desejo emocional, 4. Promessa forte."
                analise = gerar_ia(p)
                st.session_state.dados = {"nome": n_p, "nicho": nicho, "publico": publico, "tipo": tipo, "objetivo": objetivo, "analise_ia": analise, "preco": preco, "garantia": garantia}
                st.session_state.etapa = "Confeccao Ebook"
                st.rerun()

# 2. CONFECÇÃO EBOOK
elif st.session_state.etapa == "Confeccao Ebook":
    st.title("📦 GERE SEU E-BOOK PROFISSIONAL")
    if st.button("GERAR 60 CARTÕES"):
        st.session_state.dados['ebook'] = gerar_ia(f"Crie um roteiro de 60 cartões rápidos para um {st.session_state.dados['tipo']} de {st.session_state.dados['nicho']} focado em {st.session_state.dados['objetivo']}.")
    
    if 'ebook' in st.session_state.dados:
        st.text_area("Conteúdo do E-book", st.session_state.dados['ebook'], height=300)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "Gere Anuncio"
            st.rerun()

# 3. ANÚNCIO VSL
elif st.session_state.etapa == "Gere Anuncio":
    st.title("🎬 GERE O ANÚNCIO EM VSL")
    if st.button("GERAR ANÚNCIO"):
        st.session_state.dados['anuncio'] = gerar_ia(f"Crie um script de VSL curta para anúncio de {st.session_state.dados['nicho']}. Foque em quebra de padrão e levar para o grupo.")
    
    if 'anuncio' in st.session_state.dados:
        st.text_area("Script do Anúncio", st.session_state.dados['anuncio'], height=250)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "Gere LP"
            st.rerun()

# 4. LANDING PAGE
elif st.session_state.etapa == "Gere LP":
    st.title("🌐 GERE SUA LANDING PAGE")
    if st.button("GERAR PÁGINA"):
        st.session_state.dados['lp'] = gerar_ia(f"Crie uma Landing Page de captura para {st.session_state.dados['nicho']}. Inclua Headline, autoridade e bullets.")
    
    if 'lp' in st.session_state.dados:
        st.text_area("Conteúdo da LP", st.session_state.dados['lp'], height=250)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "Sequencia Mensagens"
            st.rerun()

# 5. MENSAGENS E VSL FINAL
elif st.session_state.etapa == "Sequencia Mensagens":
    st.title("📌 MENSAGENS E VSL DE VENDA")
    if st.button("GERAR SEQUÊNCIA COMPLETA"):
        p = f"Gere a descrição e a sequência de 7 dias de mensagens para grupo de lançamento de {st.session_state.dados['nicho']}. O Dia 7 deve ser o script completo da VSL de Venda com preço {st.session_state.dados['preco']} e garantia {st.session_state.dados['garantia']}."
        st.session_state.dados['mensagens'] = gerar_ia(p)
    
    if 'mensagens' in st.session_state.dados:
        st.text_area("Sequência de Lançamento", st.session_state.dados['mensagens'], height=300)
        if st.button("SALVAR PROJETO"):
            st.session_state.projetos[st.session_state.dados['nome']] = st.session_state.dados
            st.session_state.etapa = "Projeto Final"
            st.rerun()

# 6. PROJETO FINAL (VISUALIZAÇÃO)
elif st.session_state.etapa == "Projeto Final":
    d = st.session_state.dados
    st.title(f"🚀 PROJETO: {d['nome']}")
    
    with st.expander("📦 CONFECÇÃO DO EBOOK"): st.code(d.get('ebook', ''))
    with st.expander("🎬 1. VSL DO ANÚNCIO"): st.code(d.get('anuncio', ''))
    with st.expander("🌐 2. LANDING PAGE"): st.code(d.get('lp', ''))
    with st.expander("📌 3. MENSAGEM FIXA + AQUECIMENTO + VSL FINAL"): st.code(d.get('mensagens', ''))
    with st.expander("🛠️ COMO APLICAR"):
        st.write("1. E-book: Copie os cartões para o Canva.\n2. Anúncio: Grave no CapCut e suba no Facebook Ads.\n3. LP: Use o Elementor para o texto da página.\n4. Grupo: Siga o cronograma de 7 dias e poste o link de checkout no final.")

    st.markdown("---")
    st.subheader("💬 TEM ALGUMA DÚVIDA?")
    duvida = st.text_input("Digite sua pergunta abaixo:")
    if st.button("Enviar Pergunta"):
        resposta = gerar_ia(f"O usuário tem a seguinte dúvida sobre o projeto {d['nome']}: {duvida}")
        st.session_state.chat_history.append(f"👤: {duvida}")
        st.session_state.chat_history.append(f"🤖: {resposta}")
    
    for msg in reversed(st.session_state.chat_history):
        st.write(msg)

st.markdown('<div style="position: fixed; bottom: 0; left: 0; width: 100%; background-color: #00BFFF; color: white; text-align: center; padding: 5px;">NEXUS - LANÇAMENTO INTELIGENTE</div>', unsafe_allow_html=True)
