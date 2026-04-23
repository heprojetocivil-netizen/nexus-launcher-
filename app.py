import streamlit as st
from groq import Groq

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="NEXUS LAUNCER", layout="wide")

# --- ESTILO ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { display: none; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3.5em; background-color: #00BFFF !important; color: white !important; font-weight: bold; border: none; }
    .caixa-texto { background-color: #F8FAFC; padding: 20px; border-radius: 10px; border-left: 5px solid #00BFFF; margin-bottom: 20px; white-space: pre-wrap; color: #1E293B; }
    .footer { text-align: center; padding: 30px; color: #94A3B8; font-size: 0.9em; border-top: 1px solid #E2E8F0; margin-top: 50px; }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO ---
if 'etapa' not in st.session_state: st.session_state.etapa = "Login"
if 'dados' not in st.session_state: st.session_state.dados = {}
if 'projetos' not in st.session_state: st.session_state.projetos = {}
if 'chat_hist' not in st.session_state: st.session_state.chat_hist = []

def ia_nexus(prompt, key):
    try:
        client = Groq(api_key=key)
        resp = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Você é o LaunchBot. Seja FIEL aos textos. NÃO RESUMA. NÃO SIMPLIFIQUE. Mantenha o tamanho original. Personalize apenas o nicho/dor. Para VSL, descreva imagens para cada cena."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile"
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"Erro na API: {e}"

# --- COMPONENTES PERSISTENTES ---
def barra_topo():
    if st.session_state.etapa != "Login":
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("➕ INICIAR NOVO PROJETO"):
                st.session_state.dados = {}
                st.session_state.etapa = "Formulario"
                st.rerun()
        with col2:
            with st.expander("📂 MEUS PROJETOS"):
                if not st.session_state.projetos: st.write("Vazio")
                for p in st.session_state.projetos.keys():
                    if st.button(f"📄 {p}"):
                        st.session_state.dados = st.session_state.projetos[p]
                        st.session_state.etapa = "Visualizacao"
                        st.rerun()

# --- TELAS ---

if st.session_state.etapa == "Login":
    st.title("NEXUS LAUNCER")
    st.subheader("USO RESTRITO À ASSOCIADOS QUIZ MAIS PRÊMIOS")
    st.info("Não coloque senha do site, só a chave api_key")
    n = st.text_input("Nome")
    c = st.text_input("Chave", type="password")
    if st.button("ENTRAR"):
        if n and c:
            st.session_state.usuario, st.session_state.api_key = n, c
            st.session_state.etapa = "Formulario"
            st.rerun()

elif st.session_state.etapa == "Formulario":
    barra_topo()
    st.title("PREENCHA FORMULÁRIO")
    ni, no, do, pr = st.text_input("Nicho"), st.text_input("Nome do e-book"), st.text_input("Qual dor ele resolve"), st.text_input("Preço")
    if st.button("AVANÇAR"):
        st.session_state.dados.update({"nicho": ni, "nome_eb": no, "dor": do, "preco": pr})
        st.session_state.etapa = "Ebook"
        st.rerun()

elif st.session_state.etapa == "Ebook":
    barra_topo()
    st.title("E-BOOK PROFISSOAL")
    if st.button("GERAR CONTEUDO – 60 CARTÕES"):
        st.session_state.dados['eb_txt'] = ia_nexus(f"Gere 60 cartões para {st.session_state.dados['nome_eb']} focado em {st.session_state.dados['dor']}", st.session_state.api_key)
    if 'eb_txt' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['eb_txt']}</div>", unsafe_allow_html=True)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "VSL1"
            st.rerun()

elif st.session_state.etapa == "VSL1":
    barra_topo()
    st.title("🎬 1. VSL DO ANÚNCIO")
    if st.button("GERAR ROTEIRO"):
        p = f"Personalize sem simplificar para o nicho {st.session_state.dados['nicho']} e oriente imagens: 'Se você quer [RESULTADO], mas sente que está perdido… provavelmente não é falta de esforço. É falta de direção. A maioria das pessoas comete um erro simples… e por isso continua tentando e não sai do lugar. E o pior: nem percebem onde estão errando. Eu organizei um caminho direto pra resolver isso… e vou mostrar dentro de um grupo fechado. Sem complicação. É gratuito. Clica em SAIBA MAIS para entrar'"
        st.session_state.dados['vsl1_txt'] = ia_nexus(p, st.session_state.api_key)
    if 'vsl1_txt' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['vsl1_txt']}</div>", unsafe_allow_html=True)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "LP"
            st.rerun()

elif st.session_state.etapa == "LP":
    barra_topo()
    st.title("🌐 2. LANDING PAGE")
    link = st.text_input("insira o link convite para o grupo no botão acima")
    if st.button("GERAR ROTEIRO"):
        p = f"Personalize para {st.session_state.usuario} no nicho {st.session_state.dados['nicho']} em parágrafos: Headline: Um caminho simples para [RESULTADO], mesmo começando do zero. Texto: Eu sou {st.session_state.usuario}. Já estive exatamente onde você está… tentando várias coisas… sem resultado. Até começar a estudar e aplicar o que realmente funciona… e identificar um padrão simples que muda completamente o jogo. Depois de aplicar isso na prática… eu percebi que o problema nunca foi esforço — foi direção. Se você sente que está tentando… mas não sai do lugar… provavelmente está passando por isso também. Eu criei um grupo onde vou te mostrar isso de forma direta: O erro que te mantém travado; O caminho mais simples; O que realmente funciona na prática. Botão: ENTRAR NO GRUPO ({link})"
        st.session_state.dados['lp_txt'] = ia_nexus(p, st.session_state.api_key)
    if 'lp_txt' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['lp_txt']}</div>", unsafe_allow_html=True)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "MSG"
            st.rerun()

elif st.session_state.etapa == "MSG":
    barra_topo()
    st.title("📌 3. MENSAGEM FIXA DO GRUPO")
    if st.button("GERAR MENSAGENS PARA O GRUPO"):
        p = f"Personalize sem simplificar para {st.session_state.dados['nicho']}: Descrição do Grupo (caminho para [RESULTADO]). Dia 1 ao 5 (fiel aos textos originais). Dia 6 VSL Final: 'O que trava a maioria... fazer da forma certa'. eBook {st.session_state.dados['nome_eb']}, garantia 7 dias. Oriente imagens para o Dia 6 e descrição com link 30% off."
        st.session_state.dados['msg_txt'] = ia_nexus(p, st.session_state.api_key)
    if 'msg_txt' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['msg_txt']}</div>", unsafe_allow_html=True)
        if st.button("AVANÇAR"):
            st.session_state.etapa = "Visualizacao"
            st.rerun()

elif st.session_state.etapa == "Visualizacao":
    barra_topo()
    st.title(f"PROJETO: {st.session_state.dados.get('nome_eb', 'Sem Nome')}")
    
    with st.expander("📚 E-BOOK", expanded=False): st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('eb_txt')}</div>", unsafe_allow_html=True)
    with st.expander("🎬 1. VSL DO ANÚNCIO", expanded=False): st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('vsl1_txt')}</div>", unsafe_allow_html=True)
    with st.expander("🌐 2. LANDING PAGE", expanded=False): st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('lp_txt')}</div>", unsafe_allow_html=True)
    with st.expander("📌 3. MENSAGENS", expanded=False): st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('msg_txt')}</div>", unsafe_allow_html=True)
    with st.expander("📅 APLICAÇÃO", expanded=False):
        st.markdown("""<div class='caixa-texto'>🚀 Sistema de lançamento simplificado\n📘 1. Criação do produto\n- Gere o seu eBook usando o Gamma AI\n- Cadastre na Monetizze\n- Estruture material\n🎬 2. VSL\n- Use Heygen e suba no Youtube\n- LP no Gamma\n- Link na descrição\n👥 4. Estrutura\n- Segunda-feira: crie o grupo\n- Semana: Anúncios\n🔥 5. Sequência\n- Próxima semana: Mensagens e Oferta</div>""", unsafe_allow_html=True)

    if st.button("💾 SALVAR PROJETO"):
        st.session_state.projetos[st.session_state.dados['nome_eb']] = st.session_state.dados
        st.success("Salvo com abas fechadas!")

    st.divider()
    st.subheader("💬 LaunchBot")
    st.write("Eu sou o LaunchBot, especialista em lançamentos digitais de alta conversão")
    duvida = st.text_input("Digite a sua dúvida", key="chat_input")
    if duvida:
        st.session_state.chat_hist.append((duvida, ia_nexus(duvida, st.session_state.api_key)))
    for q, a in reversed(st.session_state.chat_hist):
        st.info(f"**Você:** {q}")
        st.success(f"**LaunchBot:** {a}")

st.markdown('<div class="footer">© 2026 Nexus Launcer Lançamento inteligente de produtos digitais</div>', unsafe_allow_html=True)
