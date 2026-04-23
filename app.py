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
    .caixa-texto { background-color: #F8FAFC; padding: 25px; border-radius: 12px; border-left: 6px solid #00BFFF; margin-bottom: 20px; white-space: pre-wrap; color: #1E293B; line-height: 1.6; font-size: 1.1em; }
    .footer { text-align: center; padding: 40px; color: #94A3B8; font-size: 0.9em; border-top: 1px solid #E2E8F0; margin-top: 50px; }
    .chat-bubble { background-color: #F1F5F9; padding: 15px; border-radius: 10px; border: 1px solid #CBD5E1; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO DE ESTADOS ---
if 'etapa' not in st.session_state: st.session_state.etapa = "Login"
if 'dados' not in st.session_state: st.session_state.dados = {}
if 'projetos' not in st.session_state: st.session_state.projetos = {}
if 'chat_hist' not in st.session_state: st.session_state.chat_hist = []

# --- MOTOR DE IA ---
def processar_ia(prompt, system_msg, key):
    try:
        client = Groq(api_key=key)
        resp = client.chat.completions.create(
            messages=[{"role": "system", "content": system_msg}, {"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile"
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"Erro: Verifique sua chave API. {e}"

# --- NAVEGAÇÃO E BOTÕES ---
def barra_global():
    if st.session_state.etapa != "Login":
        c1, c2 = st.columns(2)
        with c1:
            if st.button("➕ INICIAR NOVO PROJETO"):
                st.session_state.dados = {}
                st.session_state.etapa = "Formulario"
                st.rerun()
        with c2:
            with st.expander("📂 MEUS PROJETOS"):
                for nome in list(st.session_state.projetos.keys()):
                    if st.button(f"📄 {nome}"):
                        st.session_state.dados = st.session_state.projetos[nome]
                        st.session_state.etapa = "Visualizacao"
                        st.rerun()

def botoes_nav(voltar, avancar):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="btn-voltar">', unsafe_allow_html=True)
        if st.button("VOLTAR", key=f"v_{voltar}"):
            st.session_state.etapa = voltar
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        if st.button("AVANÇAR", key=f"a_{avancar}"):
            st.session_state.etapa = avancar
            st.rerun()

# --- TELAS DO SISTEMA ---

if st.session_state.etapa == "Login":
    st.title("NEXUS LAUNCER")
    st.subheader("USO RESTRITO À ASSOCIADOS QUIZ MAIS PRÊMIOS")
    st.warning("Não coloque senha do site, só a chave api_key")
    u_nome = st.text_input("Nome")
    u_key = st.text_input("Chave", type="password")
    if st.button("ENTRAR"):
        if u_nome and u_key:
            st.session_state.usuario = u_nome
            st.session_state.api_key = u_key
            st.session_state.etapa = "Formulario"
            st.rerun()

elif st.session_state.etapa == "Formulario":
    barra_global()
    st.title("PREENCHA FORMULÁRIO")
    ni, eb, dor, pr = st.text_input("Nicho"), st.text_input("Nome do e-book"), st.text_input("Qual dor ele resolve"), st.text_input("Preço")
    if st.button("AVANÇAR"):
        st.session_state.dados.update({"nicho": ni, "nome_eb": eb, "dor": dor, "preco": pr})
        st.session_state.etapa = "Ebook"
        st.rerun()

elif st.session_state.etapa == "Ebook":
    barra_global()
    st.title("E-BOOK PROFISSOAL")
    if st.button("GERAR CONTEUDO – 60 CARTÕES"):
        p = f"Gere 60 cartões de conteúdo para o eBook {st.session_state.dados['nome_eb']} no nicho {st.session_state.dados['nicho']}."
        st.session_state.dados['eb_res'] = processar_ia(p, "Você é um especialista em conteúdo.", st.session_state.api_key)
    if 'eb_res' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['eb_res']}</div>", unsafe_allow_html=True)
        botoes_nav("Formulario", "VSL1")

elif st.session_state.etapa == "VSL1":
    barra_global()
    st.title("🎬 1. VSL DO ANÚNCIO")
    if st.button("GERAR ROTEIRO"):
        sys = "Personalize o nicho sem simplificar, mantenha parágrafos e oriente imagens 100% personalizadas."
        p = f"Nicho: {st.session_state.dados['nicho']}. Texto: Se você quer [RESULTADO], mas sente que está perdido… provavelmente não é falta de esforço. É falta de direção. A maioria das pessoas comete um erro simples… e por isso continua tentando e não sai do lugar. E o pior: nem percebem onde estão errando. Eu organizei um caminho direto pra resolver isso… e vou mostrar dentro de um grupo fechado. Sem complicação. É gratuito. Clica em SAIBA MAIS para entrar."
        st.session_state.dados['vsl1_res'] = processar_ia(p, sys, st.session_state.api_key)
    if 'vsl1_res' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['vsl1_res']}</div>", unsafe_allow_html=True)
        botoes_nav("Ebook", "LP")

elif st.session_state.etapa == "LP":
    barra_global()
    st.title("🌐 2. LANDING PAGE")
    if st.button("GERAR ROTEIRO"):
        sys = "Personalize o nicho sem simplificar o texto original."
        p = f"Nome: {st.session_state.usuario}, Nicho: {st.session_state.dados['nicho']}. Texto: Headline: Um caminho simples para [RESULTADO], mesmo começando do zero. Eu sou {st.session_state.usuario}. Já estive exatamente onde você está… tentando várias coisas… sem resultado. Até começar a estudar e aplicar o que realmente funciona… e identificar um padrão simples que muda completamente o jogo. Depois de aplicar isso na prática… eu percebi que o problema nunca foi esforço — foi direção. Se você sente que está tentando… mas não sai do lugar… provavelmente está passando por isso também. Eu criei um grupo onde vou te mostrar isso de forma direta: O erro que te mantém travado; O caminho mais simples; O que realmente funciona na prática. ENTRAR NO GRUPO"
        st.session_state.dados['lp_res'] = processar_ia(p, sys, st.session_state.api_key)
    if 'lp_res' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['lp_res']}</div>", unsafe_allow_html=True)
        botoes_nav("VSL1", "MSG")

elif st.session_state.etapa == "MSG":
    barra_global()
    st.title("📌 3. MENSAGEM FIXA DO GRUPO")
    if st.button("GERAR MENSAGENS PARA O GRUPO"):
        sys = "REPLIQUE LITERALMENTE do Dia 1 ao 5. Personalize apenas o Dia 6 e o nicho."
        p = f"Nicho: {st.session_state.dados['nicho']}. DESCRIÇÃO: Silencioso, caminho para [RESULTADO]. MENSAGENS LITERAIS DIA 1 A 5. DIA 6 VSL: Presta atenção nisso... o que trava a maioria... caminho direto para [RESULTADO]. eBook {st.session_state.dados['nome_eb']}. Garantia 7 dias. Link 30% off."
        st.session_state.dados['msg_res'] = processar_ia(p, sys, st.session_state.api_key)
    if 'msg_res' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['msg_res']}</div>", unsafe_allow_html=True)
        botoes_nav("LP", "Visualizacao")

elif st.session_state.etapa == "Visualizacao":
    barra_global()
    st.title(f"PROJETO: {st.session_state.dados.get('nome_eb')}")
    
    with st.expander("📚 E-BOOK", expanded=False): st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('eb_res')}</div>", True)
    with st.expander("🎬 1. VSL DO ANÚNCIO", expanded=False): st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('vsl1_res')}</div>", True)
    with st.expander("🌐 2. LANDING PAGE", expanded=False): st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('lp_res')}</div>", True)
    with st.expander("📌 3. MENSAGENS", expanded=False): st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('msg_res')}</div>", True)
    with st.expander("📅 APLICAÇÃO", expanded=False):
        st.markdown("""<div class='caixa-texto'>🚀 Sistema de lançamento simplificado\n\n📘 1. Criação do produto\n- Gere o seu eBook usando o Gamma AI\n- Cadastre na Monetizze\n\n🎬 2. VSL (Vídeo de Vendas)\n- Vídeos no Heygen\n- Landing Page no Gamma\n\n👥 4. Estrutura\n- Criar grupo na segunda-feira e encher até sexta.\n\n🔥 5. Sequência\n- Iniciar mensagens na semana seguinte e vender no Dia 6.</div>""", True)

    if st.button("💾 SALVAR PROJETO"):
        st.session_state.projetos[st.session_state.dados['nome_eb']] = st.session_state.dados
        st.success("Salvo!")

    st.divider()
    st.subheader("💬 LaunchBot")
    st.write("Eu sou o LaunchBot, especialista em lançamentos digitais de alta conversão")
    prompt_chat = st.text_input("Digite a sua dúvida", key="chat_input")
    if prompt_chat:
        st.session_state.chat_hist.append((prompt_chat, processar_ia(prompt_chat, "Você é o LaunchBot.", st.session_state.api_key)))
    for q, a in reversed(st.session_state.chat_hist):
        st.markdown(f"**Você:** {q}")
        st.markdown(f"<div class='chat-bubble'>**Bot:** {a}</div>", unsafe_allow_html=True)

st.markdown('<div class="footer">© 2026 Nexus Launcer Lançamento inteligente de produtos digitais</div>', unsafe_allow_html=True)
