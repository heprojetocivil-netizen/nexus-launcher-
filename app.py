import streamlit as st
from groq import Groq

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="NEXUS LAUNCER", layout="wide")

# --- ESTILO CSS ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { display: none; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3.5em; background-color: #00BFFF !important; color: white !important; font-weight: bold; border: none; }
    .btn-voltar>button { background-color: #64748B !important; }
    .caixa-texto { background-color: #F8FAFC; padding: 20px; border-radius: 10px; border-left: 5px solid #00BFFF; margin-bottom: 20px; white-space: pre-wrap; color: #1E293B; font-size: 1.1em; line-height: 1.6; }
    .footer { text-align: center; padding: 30px; color: #94A3B8; font-size: 0.9em; border-top: 1px solid #E2E8F0; margin-top: 50px; }
    .chat-box { background-color: #F1F5F9; padding: 15px; border-radius: 10px; margin-top: 5px; border: 1px solid #CBD5E1; }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO ---
if 'etapa' not in st.session_state: st.session_state.etapa = "Login"
if 'dados' not in st.session_state: st.session_state.dados = {}
if 'projetos' not in st.session_state: st.session_state.projetos = {}
if 'chat_hist' not in st.session_state: st.session_state.chat_hist = []

# --- MOTOR IA ---
def chamar_ia(prompt, key, literal=False):
    try:
        client = Groq(api_key=key)
        system_content = "Você é o LaunchBot. "
        if literal:
            system_content += "REPLIQUE OS TEXTOS FORNECIDOS LITERALMENTE. Não resuma. Não altere as mensagens dos dias 1 a 6."
        else:
            system_content += "Personalize para o nicho sem simplificar ou resumir o texto original."
            
        resp = client.chat.completions.create(
            messages=[{"role": "system", "content": system_content}, {"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile"
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"Erro na Chave API: {e}"

# --- BARRA GLOBAL ---
def barra_global():
    if st.session_state.etapa != "Login":
        c1, c2 = st.columns([1, 1])
        with c1:
            if st.button("➕ INICIAR NOVO PROJETO"):
                st.session_state.dados = {}
                st.session_state.etapa = "Formulario"
                st.rerun()
        with c2:
            with st.expander("📂 MEUS PROJETOS"):
                if not st.session_state.projetos: st.write("Vazio")
                for p in st.session_state.projetos.keys():
                    if st.button(f"📄 {p}"):
                        st.session_state.dados = st.session_state.projetos[p]
                        st.session_state.etapa = "Visualizacao"
                        st.rerun()

def navegação(anterior, proximo):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="btn-voltar">', unsafe_allow_html=True)
        if st.button("VOLTAR", key=f"v_{anterior}"):
            st.session_state.etapa = anterior
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        if st.button("AVANÇAR", key=f"a_{proximo}"):
            st.session_state.etapa = proximo
            st.rerun()

# --- TELAS ---

if st.session_state.etapa == "Login":
    st.title("NEXUS LAUNCER")
    st.subheader("USO RESTRITO À ASSOCIADOS QUIZ MAIS PRÊMIOS")
    st.warning("Não coloque senha do site, só a chave api_key")
    n = st.text_input("Nome")
    k = st.text_input("Chave", type="password")
    if st.button("ENTRAR"):
        if n and k:
            st.session_state.usuario, st.session_state.api_key = n, k
            st.session_state.etapa = "Formulario"
            st.rerun()

elif st.session_state.etapa == "Formulario":
    barra_global()
    st.title("PREENCHA FORMULÁRIO")
    ni = st.text_input("Nicho")
    no = st.text_input("Nome do e-book")
    do = st.text_input("Qual dor ele resolve")
    pr = st.text_input("Preço")
    if st.button("AVANÇAR"):
        st.session_state.dados.update({"nicho": ni, "nome_eb": no, "dor": do, "preco": pr})
        st.session_state.etapa = "Ebook"
        st.rerun()

elif st.session_state.etapa == "Ebook":
    barra_global()
    st.title("E-BOOK PROFISSOAL")
    if st.button("GERAR CONTEUDO – 60 CARTÕES"):
        prompt = f"Gere 60 cartões de conteúdo para o e-book {st.session_state.dados['nome_eb']} no nicho {st.session_state.dados['nicho']} resolvendo a dor {st.session_state.dados['dor']}."
        st.session_state.dados['eb_res'] = chamar_ia(prompt, st.session_state.api_key)
    
    if 'eb_res' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['eb_res']}</div>", unsafe_allow_html=True)
        navegação("Formulario", "VSL1")

elif st.session_state.etapa == "VSL1":
    barra_topo() if 'barra_topo' in globals() else barra_global()
    st.title("🎬 1. VSL DO ANÚNCIO")
    if st.button("GERAR ROTEIRO"):
        p = f"Personalize sem simplificar para o nicho {st.session_state.dados['nicho']} mantendo parágrafos: 'Se você quer [RESULTADO], mas sente que está perdido… provavelmente não é falta de esforço. É falta de direção. A maioria das pessoas comete um erro simples… e por isso continua tentando e não sai do lugar. E o pior: nem percebem onde estão errando. Eu organizei um caminho direto pra resolver isso… e vou mostrar dentro de um grupo fechado. Sem complicação. É gratuito. Clica em SAIBA MAIS para entrar'. IA: oriente imagens 100% personalizadas."
        st.session_state.dados['vsl1_res'] = chamar_ia(p, st.session_state.api_key)
    
    if 'vsl1_res' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['vsl1_res']}</div>", unsafe_allow_html=True)
        navegação("Ebook", "LP")

elif st.session_state.etapa == "LP":
    barra_global()
    st.title("🌐 2. LANDING PAGE")
    if st.button("GERAR ROTEIRO"):
        p = f"Personalize para {st.session_state.usuario} no nicho {st.session_state.dados['nicho']} mantendo parágrafos: Headline: Um caminho simples para [RESULTADO], mesmo começando do zero. Texto: Eu sou {st.session_state.usuario}. Já estive exatamente onde você está… tentando várias coisas… sem resultado. Até começar a estudar e aplicar o que realmente funciona… e identificar um padrão simples que muda completamente o jogo. Depois de aplicar isso na prática… eu percebi que o problema nunca foi esforço — foi direção. Se você sente que está tentando… mas não sai do lugar… provavelmente está passando por isso também. Eu criei um grupo onde vou te mostrar isso de forma direta: O erro que te mantém travado; O caminho mais simples; O que realmente funciona na prática. Botão: ENTRAR NO GRUPO"
        st.session_state.dados['lp_res'] = chamar_ia(p, st.session_state.api_key)
    
    if 'lp_res' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['lp_res']}</div>", unsafe_allow_html=True)
        navegação("VSL1", "MSG")

elif st.session_state.etapa == "MSG":
    barra_global()
    st.title("📌 3. MENSAGEM FIXA DO GRUPO")
    if st.button("GERAR MENSAGENS PARA O GRUPO"):
        p = f"REPLIQUE LITERALMENTE para o nicho {st.session_state.dados['nicho']}: DESCRIÇÃO DO GRUPO (caminho simples para [RESULTADO]). DIA 1 ao 5: REPLIQUE FIELMENTE OS TEXTOS. DIA 6 VSL: 'Eu falei que hoje ia te mostrar... você precisa fazer da forma certa'. eBook {st.session_state.dados['nome_eb']}, garantia 7 dias. Oriente imagens para o Dia 6 e gere descrição curta com link 30% off."
        st.session_state.dados['msg_res'] = chamar_ia(p, st.session_state.api_key, literal=True)
    
    if 'msg_res' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['msg_res']}</div>", unsafe_allow_html=True)
        navegação("LP", "Visualizacao")

elif st.session_state.etapa == "Visualizacao":
    barra_global()
    st.title(f"PROJETO: {st.session_state.dados.get('nome_eb')}")
    
    with st.expander("📚 E-BOOK", expanded=False): st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('eb_res')}</div>", True)
    with st.expander("🎬 1. VSL DO ANÚNCIO", expanded=False): st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('vsl1_res')}</div>", True)
    with st.expander("🌐 2. LANDING PAGE", expanded=False): st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('lp_res')}</div>", True)
    with st.expander("📌 3. MENSAGENS", expanded=False): st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('msg_res')}</div>", True)
    with st.expander("📅 APLICAÇÃO", expanded=False):
        st.markdown("""<div class='caixa-texto'>🚀 Sistema de lançamento simplificado\n📘 1. Criação: Gamma AI, Monetizze.\n🎬 2. VSL: Heygen e Youtube.\n👥 4. Grupo: Criar segunda-feira.\n🔥 5. Sequência: Mensagens e Oferta final.</div>""", True)

    if st.button("💾 SALVAR PROJETO"):
        st.session_state.projetos[st.session_state.dados['nome_eb']] = st.session_state.dados
        st.success("Salvo com sucesso!")

    st.divider()
    st.subheader("💬 LaunchBot")
    st.write("Eu sou o LaunchBot, especialista em lançamentos digitais de alta conversão")
    msg_chat = st.text_input("Digite a sua dúvida", key="chat_input")
    if msg_chat:
        st.session_state.chat_hist.append((msg_chat, chamar_ia(msg_chat, st.session_state.api_key)))
    for q, a in reversed(st.session_state.chat_hist):
        st.info(f"**Você:** {q}")
        st.success(f"**LaunchBot:** {a}")

st.markdown('<div class="footer">© 2026 Nexus Launcer Lançamento inteligente de produtos digitais</div>', unsafe_allow_html=True)
