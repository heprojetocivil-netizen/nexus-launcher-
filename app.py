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

api_key = "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"

def gerar_ia(prompt, system="Você é o NEXUS LANCEUR, mestre em lançamentos e copywriter de elite."):
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
    .resumo-ia { background-color: #F1F5F9; padding: 15px; border-radius: 10px; border-left: 5px solid #00BFFF; margin-bottom: 20px; font-size: 14px;}
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("📂 NEXUS LANCEUR")
    st.info(f"Usuário Ativo: Orlando Rousseau")
    st.subheader("PROJETOS SALVOS")
    for p_nome in st.session_state.projetos.keys():
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

# 1. FORMULÁRIO INTELIGENTE
if st.session_state.etapa == "Novo Projeto":
    st.title("🚀 FORMULÁRIO INTELIGENTE NEXUS LANCEUR")
    with st.form("f1"):
        col1, col2 = st.columns(2)
        with col1:
            n_p = st.text_input("Nome do Projeto")
            nicho = st.text_input("Nicho do Produto")
            publico = st.text_input("Público-alvo")
            tipo = st.text_input("Tipo de Produto (ex: eBook, Guia)")
        with col2:
            objetivo = st.text_input("Objetivo Principal (Resultado)")
            experiencia = st.selectbox("Seu nível de experiência", ["Iniciante", "Já testei", "Já tive resultados"])
            preco = st.text_input("Preço do Produto (Valor final)")
            garantia = st.text_input("Garantia")
        
        if st.form_submit_button("AVANÇAR"):
            with st.spinner("🤖 Nexus Gerando Inteligência Estratégica..."):
                p = f"Crie para o nicho {nicho} e público {publico}: 1. Dor central REAL, 2. Objeções específicas, 3. Desejo emocional profundo, 4. Promessa forte, 5. Mecanismo único (Dê um nome criativo para o método), 6. Ângulo de ataque."
                analise = gerar_ia(p)
                st.session_state.dados = {"nome": n_p, "nicho": nicho, "publico": publico, "tipo": tipo, "objetivo": objetivo, "analise_ia": analise, "preco": preco, "garantia": garantia}
                st.session_state.etapa = "Confeccao Ebook"
                st.rerun()

# 2. CONFECÇÃO EBOOK
elif st.session_state.etapa == "Confeccao Ebook":
    st.title("📦 GERE SEU E-BOOK PROFISSIONAL")
    st.markdown(f"<div class='resumo-ia'>{st.session_state.dados['analise_ia']}</div>", unsafe_allow_html=True)
    if st.button("GERAR 60 CARTÕES"):
        st.session_state.dados['ebook'] = gerar_ia(f"Crie um roteiro de 60 cartões rápidos para um {st.session_state.dados['tipo']} de {st.session_state.dados['nicho']} focado em {st.session_state.dados['objetivo']}.")
    
    if 'ebook' in st.session_state.dados:
        st.text_area("Conteúdo do E-book", st.session_state.dados['ebook'], height=300)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "Gere Anuncio"
            st.rerun()

# 3. ANÚNCIO VSL (GOOGLE/SABER MAIS)
elif st.session_state.etapa == "Gere Anuncio":
    st.title("🎬 GERE O ANÚNCIO (GOOGLE ADS)")
    if st.button("GERAR ANÚNCIO"):
        prompt = f"Crie um script de VSL curta para anúncio no Google Ads para o nicho {st.session_state.dados['nicho']}. Termine obrigatoriamente com o CTA: 'CLIQUE EM SABER MAIS'."
        st.session_state.dados['anuncio'] = gerar_ia(prompt)
    
    if 'anuncio' in st.session_state.dados:
        st.text_area("Script do Anúncio", st.session_state.dados['anuncio'], height=250)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "Gere LP"
            st.rerun()

# 4. LANDING PAGE
elif st.session_state.etapa == "Gere LP":
    st.title("🌐 GERE SUA LANDING PAGE")
    if st.button("GERAR PÁGINA"):
        st.session_state.dados['lp'] = gerar_ia(f"Crie uma Landing Page de captura para {st.session_state.dados['nicho']}. Use a análise: {st.session_state.dados['analise_ia']}.")
    
    if 'lp' in st.session_state.dados:
        st.text_area("Conteúdo da LP", st.session_state.dados['lp'], height=250)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "Sequencia Mensagens"
            st.rerun()

# 5. MENSAGENS E VSL FINAL PERSONALIZADO
elif st.session_state.etapa == "Sequencia Mensagens":
    st.title("📌 LANÇAMENTO E VSL FINAL")
    if st.button("GERAR SEQUÊNCIA COMPLETA + VSL FINAL"):
        vsl_template = f"""
        Use EXATAMENTE este modelo de copy adaptado para {st.session_state.dados['nicho']}:
        'Você percebeu que… não importa o quanto você tenta… se você não corrigir esse ponto… nada muda? 
        O erro da maioria das pessoas é simples: elas fazem mais… quando na verdade deveriam fazer diferente. 
        E foi isso que eu descobri depois de errar várias vezes. Eu organizei tudo em um método simples — que eu chamo de: 👉 [NOME DO MECANISMO ÚNICO]. 
        Esse método mostra exatamente: o que fazer, como fazer e em que ordem fazer, sem enrolação. 
        E eu coloquei tudo isso em um material direto ao ponto. Sem teoria desnecessária. Só o que realmente funciona. 
        Você pode acessar agora. E testar por {st.session_state.dados['garantia']}. Se não fizer sentido pra você, é só pedir reembolso. 
        O acesso já está disponível. Por apenas {st.session_state.dados['preco']}. Clique no link da descrição.'
        """
        prompt_final = f"Gere 6 mensagens de grupo e a VSL final baseada neste modelo: {vsl_template}"
        st.session_state.dados['mensagens'] = gerar_ia(prompt_final)
    
    if 'mensagens' in st.session_state.dados:
        st.text_area("Sequência e VSL Final", st.session_state.dados['mensagens'], height=300)
        if st.button("SALVAR PROJETO"):
            st.session_state.projetos[st.session_state.dados['nome']] = st.session_state.dados
            st.session_state.etapa = "Projeto Final"
            st.rerun()

# 6. PROJETO FINAL (VISUALIZAÇÃO)
elif st.session_state.etapa == "Projeto Final":
    d = st.session_state.dados
    st.title(f"🚀 NEXUS LANCEUR: {d['nome']}")
    
    with st.expander("📦 CONFECÇÃO DO EBOOK"): st.code(d.get('ebook', ''))
    with st.expander("🎬 1. VSL DO ANÚNCIO (SABER MAIS)"): st.code(d.get('anuncio', ''))
    with st.expander("🌐 2. LANDING PAGE"): st.code(d.get('lp', ''))
    with st.expander("📌 3. MENSAGENS + VSL FINAL"): st.code(d.get('mensagens', ''))
    with st.expander("🛠️ COMO APLICAR"):
        st.markdown(f"1. E-book no Canva.\n2. Anúncio no Google Ads (Botão Saber Mais).\n3. LP de Captura.\n4. Mensagens no WhatsApp.\n5. Link de Checkout de R$ {d.get('preco')}.")

    st.markdown("---")
    st.subheader("💬 SUPORTE NEXUS")
    duvida = st.text_input("Dúvida sobre o projeto?")
    if st.button("Enviar"):
        resposta = gerar_ia(f"Dúvida sobre projeto {d['nome']}: {duvida}")
        st.session_state.chat_history.append(f"👤: {duvida}")
        st.session_state.chat_history.append(f"🤖: {resposta}")
    
    for msg in reversed(st.session_state.chat_history):
        st.write(msg)

st.markdown('<div style="position: fixed; bottom: 0; left: 0; width: 100%; background-color: #00BFFF; color: white; text-align: center; padding: 5px;">NEXUS LANCEUR - SISTEMA PROTEGIDO</div>', unsafe_allow_html=True)
