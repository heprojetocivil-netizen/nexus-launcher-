import streamlit as st
from groq import Groq

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="NEXUS LAUNCER", layout="wide")

# --- ESTILO CSS ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { display: none; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3.5em; background-color: #00BFFF !important; color: white !important; font-weight: bold; border: none; }
    .stButton .voltar-btn>button { background-color: #64748B !important; }
    .caixa-texto { background-color: #F8FAFC; padding: 25px; border-radius: 12px; border-left: 6px solid #00BFFF; margin-bottom: 20px; white-space: pre-wrap; color: #1E293B; line-height: 1.6; font-size: 1.1em; }
    .footer { text-align: center; padding: 40px; color: #94A3B8; font-size: 0.9em; border-top: 1px solid #E2E8F0; margin-top: 50px; }
    .chat-bubble { background-color: #F1F5F9; padding: 15px; border-radius: 10px; border: 1px solid #CBD5E1; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO DE ESTADOS ---
if 'etapa' not in st.session_state: st.session_state.etapa = "Login"
if 'dados' not in st.session_state: st.session_state.dados = {}
if 'projetos' not in st.session_state: st.session_state.projetos = {}
if 'chat_log' not in st.session_state: st.session_state.chat_log = []

# --- MOTOR DE IA ---
def gerar_conteudo(prompt, api_key):
    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Você é o LaunchBot. Seja 100% FIEL aos textos fornecidos. NÃO RESUMA. NÃO SIMPLIFIQUE. Mantenha os parágrafos originais. Apenas personalize os campos entre colchetes para o nicho do usuário. No VSL, detalhe as imagens sugeridas para cada frase."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile"
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Erro: Verifique sua Chave API. ({e})"

# --- NAVEGAÇÃO GLOBAL ---
def barra_topo():
    if st.session_state.etapa != "Login":
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("➕ INICIAR NOVO PROJETO", key="global_novo"):
                st.session_state.dados = {}
                st.session_state.etapa = "Formulario"
                st.rerun()
        with col2:
            with st.expander("📂 MEUS PROJETOS"):
                if not st.session_state.projetos: st.write("Vazio")
                for nome in list(st.session_state.projetos.keys()):
                    if st.button(f"📄 {nome}", key=f"load_{nome}"):
                        st.session_state.dados = st.session_state.projetos[nome]
                        st.session_state.etapa = "Visualizacao"
                        st.rerun()

def botoes_fluxo(anterior, proximo):
    col_v, col_a = st.columns(2)
    with col_v:
        if st.button("⬅️ VOLTAR", key=f"voltar_{anterior}"):
            st.session_state.etapa = anterior
            st.rerun()
    with col_a:
        if st.button("AVANÇAR ➡️", key=f"avancar_{proximo}"):
            st.session_state.etapa = proximo
            st.rerun()

# --- TELAS ---

if st.session_state.etapa == "Login":
    st.title("NEXUS LAUNCER")
    st.subheader("USO RESTRITO À ASSOCIADOS QUIZ MAIS PRÊMIOS")
    st.info("Não coloque senha do site, só a chave api_key")
    u_nome = st.text_input("Nome")
    u_chave = st.text_input("Chave", type="password")
    if st.button("ENTRAR"):
        if u_nome and u_chave:
            st.session_state.usuario, st.session_state.api_key = u_nome, u_chave
            st.session_state.etapa = "Formulario"
            st.rerun()

elif st.session_state.etapa == "Formulario":
    barra_topo()
    st.title("PREENCHA FORMULÁRIO")
    ni, eb, do, pr = st.text_input("Nicho"), st.text_input("Nome do e-book"), st.text_input("Qual dor ele resolve"), st.text_input("Preço")
    if st.button("AVANÇAR"):
        st.session_state.dados.update({"nicho": ni, "nome_eb": eb, "dor": do, "preco": pr})
        st.session_state.etapa = "Ebook"
        st.rerun()

elif st.session_state.etapa == "Ebook":
    barra_topo()
    st.title("E-BOOK PROFISSOAL")
    if st.button("GERAR CONTEUDO – 60 CARTÕES"):
        p = f"Gere 60 cartões de conteúdo para o eBook {st.session_state.dados['nome_eb']} no nicho {st.session_state.dados['nicho']} focado na dor {st.session_state.dados['dor']}"
        st.session_state.dados['eb_res'] = gerar_conteudo(p, st.session_state.api_key)
    if 'eb_res' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['eb_res']}</div>", unsafe_allow_html=True)
        botoes_fluxo("Formulario", "VSL1")

elif st.session_state.etapa == "VSL1":
    barra_topo()
    st.title("🎬 1. VSL DO ANÚNCIO")
    if st.button("GERAR ROTEIRO"):
        p = f"Personalize sem simplificar mantendo os parágrafos para o nicho {st.session_state.dados['nicho']} e oriente as imagens: 'Se você quer [RESULTADO], mas sente que está perdido… provavelmente não é falta de esforço. É falta de direção. A maioria das pessoas comete um erro simples… e por isso continua tentando e não sai do lugar. E o pior: nem percebem onde estão errando. Eu organizei um caminho direto pra resolver isso… e vou mostrar dentro de um grupo fechado. Sem complicação. É gratuito. Clica em SAIBA MAIS para entrar'"
        st.session_state.dados['vsl1_res'] = gerar_conteudo(p, st.session_state.api_key)
    if 'vsl1_res' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['vsl1_res']}</div>", unsafe_allow_html=True)
        botoes_fluxo("Ebook", "LP")

elif st.session_state.etapa == "LP":
    barra_topo()
    st.title("🌐 2. LANDING PAGE")
    if st.button("GERAR ROTEIRO"):
        p = f"Personalize para {st.session_state.usuario} no nicho {st.session_state.dados['nicho']} mantendo fielmente os parágrafos: Headline: Um caminho simples para [RESULTADO], mesmo começando do zero. Texto: Eu sou {st.session_state.usuario}. Já estive exatamente onde você está… tentando várias coisas… sem resultado. Até começar a estudar e aplicar o que realmente funciona… e identificar um padrão simples que muda completamente o jogo. Depois de aplicar isso na prática… eu percebi que o problema nunca foi esforço — foi direção. Se você sente que está tentando… mas não sai do lugar… provavelmente está passando por isso também. Eu criei um grupo onde vou te mostrar isso de forma direta: O erro que te mantém travado; O caminho mais simples; O que realmente funciona na prática. Botão: ENTRAR NO GRUPO"
        st.session_state.dados['lp_res'] = gerar_conteudo(p, st.session_state.api_key)
    if 'lp_res' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['lp_res']}</div>", unsafe_allow_html=True)
        botoes_fluxo("VSL1", "Mensagens")

elif st.session_state.etapa == "Mensagens":
    barra_topo()
    st.title("📌 3. MENSAGEM FIXA DO GRUPO")
    if st.button("GERAR MENSAGENS PARA O GRUPO"):
        p = f"REPLIQUE LITERALMENTE SEM RESUMIR para o nicho {st.session_state.dados['nicho']}: DESCRIÇÃO DO GRUPO: Esse grupo é silencioso... caminho simples para [RESULTADO]. DIA 1: Deixa eu te fazer uma pergunta direta... DIA 2: A maioria das pessoas não falha por falta de esforço... DIA 3: Existe um ponto simples... DIA 4: Quando você entende isso... DIA 5: Eu poderia explicar tudo aqui... DIA 6 VSL FINAL: 'Eu falei que hoje ia te mostrar... O que trava a maioria... fazer da forma certa'. eBook {st.session_state.dados['nome_eb']}, garantia 7 dias. Oriente imagens para o Dia 6 e gere descrição com link 30% off."
        st.session_state.dados['msg_res'] = gerar_conteudo(p, st.session_state.api_key)
    if 'msg_res' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['msg_res']}</div>", unsafe_allow_html=True)
        botoes_fluxo("LP", "Visualizacao")

elif st.session_state.etapa == "Visualizacao":
    barra_topo()
    st.title(f"PROJETO: {st.session_state.dados.get('nome_eb', 'Novo')}")
    
    with st.expander("📚 E-BOOK", expanded=False): st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('eb_res')}</div>", True)
    with st.expander("🎬 1. VSL DO ANÚNCIO", expanded=False): st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('vsl1_res')}</div>", True)
    with st.expander("🌐 2. LANDING PAGE", expanded=False): st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('lp_res')}</div>", True)
    with st.expander("📌 3. MENSAGENS", expanded=False): st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('msg_res')}</div>", True)
    with st.expander("📅 APLICAÇÃO", expanded=False):
        st.markdown("""<div class='caixa-texto'>🚀 Sistema de lançamento simplificado\n📘 1. Criação: Gamma AI, Monetizze.\n🎬 2. VSL: Heygen e Youtube.\n👥 4. Estrutura: Criar segunda-feira.\n🔥 5. Sequência: Mensagens e Oferta final.</div>""", True)

    if st.button("💾 SALVAR PROJETO"):
        st.session_state.projetos[st.session_state.dados['nome_eb']] = st.session_state.dados
        st.success("Salvo com abas fechadas!")

    st.divider()
    st.subheader("💬 LaunchBot")
    st.write("Eu sou o LaunchBot, especialista em lançamentos digitais de alta conversão")
    prompt_chat = st.text_input("Digite a sua dúvida e aperte Enter", key="chat_input")
    if prompt_chat:
        st.session_state.chat_log.append((prompt_chat, gerar_conteudo(prompt_chat, st.session_state.api_key)))
    for q, a in reversed(st.session_state.chat_log):
        st.markdown(f"**Você:** {q}")
        st.markdown(f"<div class='chat-bubble'>**LaunchBot:** {a}</div>", unsafe_allow_html=True)

st.markdown(f'<div class="footer">© 2026 Nexus Launcer Lançamento inteligente de produtos digitais</div>', unsafe_allow_html=True)
