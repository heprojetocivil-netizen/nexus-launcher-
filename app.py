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
    .chat-container { background-color: #F1F5F9; padding: 20px; border-radius: 10px; border: 1px solid #CBD5E1; margin-top: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO ---
if 'etapa' not in st.session_state: st.session_state.etapa = "Login"
if 'dados' not in st.session_state: st.session_state.dados = {}
if 'projetos' not in st.session_state: st.session_state.projetos = {}
if 'chat_hist' not in st.session_state: st.session_state.chat_hist = []

# --- MOTOR IA ---
def processar_ia(prompt, key, system_msg="Você é o LaunchBot. Siga os roteiros FIELMENTE."):
    try:
        client = Groq(api_key=key)
        resp = client.chat.completions.create(
            messages=[{"role": "system", "content": system_msg}, {"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile"
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"Erro: {e}"

# --- COMPONENTES DE NAVEGAÇÃO ---
def menu_global():
    if st.session_state.etapa != "Login":
        c1, c2 = st.columns([1, 1])
        with c1:
            if st.button("➕ INICIAR NOVO PROJETO"):
                st.session_state.dados = {}
                st.session_state.etapa = "Formulario"
                st.rerun()
        with c2:
            with st.expander("📂 MEUS PROJETOS"):
                if not st.session_state.projetos: st.write("Nenhum projeto.")
                for p in list(st.session_state.projetos.keys()):
                    if st.button(f"📄 {p}"):
                        st.session_state.dados = st.session_state.projetos[p]
                        st.session_state.etapa = "Visualizacao"
                        st.rerun()

def botoes_navegacao(voltar_para, avancar_para, label_avancar="AVANÇAR"):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="btn-voltar">', unsafe_allow_html=True)
        if st.button("VOLTAR", key=f"btn_voltar_{voltar_para}"):
            st.session_state.etapa = voltar_para
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        if st.button(label_avancar, key=f"btn_avancar_{avancar_para}"):
            st.session_state.etapa = avancar_para
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
    menu_global()
    st.title("PREENCHA FORMULÁRIO")
    ni, no, do, pr = st.text_input("Nicho"), st.text_input("Nome do e-book"), st.text_input("Qual dor ele resolve"), st.text_input("Preço")
    if st.button("AVANÇAR"):
        st.session_state.dados.update({"nicho": ni, "nome_eb": no, "dor": do, "preco": pr})
        st.session_state.etapa = "Ebook"
        st.rerun()

elif st.session_state.etapa == "Ebook":
    menu_global()
    st.title("E-BOOK PROFISSIONAL")
    if st.button("GERAR CONTEUDO – 60 CARTÕES"):
        st.session_state.dados['txt_eb'] = processar_ia(f"Gere 60 cartões de conteúdo para o eBook {st.session_state.dados['nome_eb']} no nicho {st.session_state.dados['nicho']}", st.session_state.api_key)
    if 'txt_eb' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['txt_eb']}</div>", unsafe_allow_html=True)
        botoes_navegacao("Formulario", "VSL1")

elif st.session_state.etapa == "VSL1":
    menu_global()
    st.title("🎬 1. VSL DO ANÚNCIO")
    if st.button("GERAR ROTEIRO"):
        p = f"Personalize este texto sem simplificar para o nicho {st.session_state.dados['nicho']} mantendo parágrafos e orientando imagens: 'Se você quer [RESULTADO], mas sente que está perdido… provavelmente não é falta de esforço. É falta de direção. A maioria das pessoas comete um erro simples… e por isso continua tentando e não sai do lugar. E o pior: nem percebem onde estão errando. Eu organizei um caminho direto pra resolver isso… e vou mostrar dentro de um grupo fechado. Sem complicação. É gratuito. Clica em SAIBA MAIS para entrar'"
        st.session_state.dados['txt_vsl1'] = processar_ia(p, st.session_state.api_key)
    if 'txt_vsl1' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['txt_vsl1']}</div>", unsafe_allow_html=True)
        botoes_navegacao("Ebook", "LP")

elif st.session_state.etapa == "LP":
    menu_global()
    st.title("🌐 2. LANDING PAGE")
    if st.button("GERAR ROTEIRO"):
        p = f"Personalize para {st.session_state.usuario} no nicho {st.session_state.dados['nicho']} em parágrafos: Headline: Um caminho simples para [RESULTADO], mesmo começando do zero. Texto: Eu sou {st.session_state.usuario}. Já estive exatamente onde você está… tentando várias coisas… sem resultado. Até começar a estudar e aplicar o que realmente funciona… e identificar um padrão simples que muda completamente o jogo. Depois de aplicar isso na prática… eu percebi que o problema nunca foi esforço — foi direção. Se você sente que está tentando… mas não sai do lugar… provavelmente está passando por isso também. Eu criei um grupo onde vou te mostrar isso de forma direta: O erro que te mantém travado; O caminho mais simples; O que realmente funciona na prática. Botão: ENTRAR NO GRUPO"
        st.session_state.dados['txt_lp'] = processar_ia(p, st.session_state.api_key)
    if 'txt_lp' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['txt_lp']}</div>", unsafe_allow_html=True)
        botoes_navegacao("VSL1", "MSG")

elif st.session_state.etapa == "MSG":
    menu_global()
    st.title("📌 3. MENSAGEM FIXA DO GRUPO")
    if st.button("GERAR MENSAGENS PARA O GRUPO"):
        sys = "Você deve ser 100% LITERAL no Dia 1 ao 5. Não mude uma vírgula."
        p = f"Nicho: {st.session_state.dados['nicho']}. DESCRIÇÃO: Silencioso, caminho para [RESULTADO]. DIA 1 ao 5: REPLIQUE LITERALMENTE OS TEXTOS ENVIADOS. DIA 6 VSL: Personalize 'O que trava a maioria... fazer da forma certa' para o eBook {st.session_state.dados['nome_eb']}, garantia 7 dias, link 30% off e oriente as imagens."
        st.session_state.dados['txt_msg'] = processar_ia(p, st.session_state.api_key, sys)
    if 'txt_msg' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['txt_msg']}</div>", unsafe_allow_html=True)
        botoes_navegacao("LP", "Visualizacao")

elif st.session_state.etapa == "Visualizacao":
    menu_global()
    st.title(f"PROJETO: {st.session_state.dados.get('nome_eb')}")
    
    with st.expander("📚 E-BOOK", False): st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('txt_eb')}</div>", True)
    with st.expander("🎬 1. VSL DO ANÚNCIO", False): st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('txt_vsl1')}</div>", True)
    with st.expander("🌐 2. LANDING PAGE", False): st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('txt_lp')}</div>", True)
    with st.expander("📌 3. MENSAGENS", False): st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('txt_msg')}</div>", True)
    with st.expander("📅 APLICAÇÃO", False):
        st.markdown("""<div class='caixa-texto'>🚀 Sistema de lançamento simplificado\n📘 1. Criação: Gamma AI, Monetizze.\n🎬 2. VSL: Heygen e Youtube.\n👥 4. Grupo: Criar segunda-feira.\n🔥 5. Vendas: Sequência e Oferta final.</div>""", True)

    if st.button("💾 SALVAR PROJETO"):
        st.session_state.projetos[st.session_state.dados['nome_eb']] = st.session_state.dados
        st.success("Salvo!")

    st.markdown("---")
    st.subheader("💬 LaunchBot")
    st.write("Eu sou o LaunchBot, especialista em lançamentos digitais de alta conversão")
    duvida = st.text_input("Digite a sua dúvida", key="chat_input")
    if duvida:
        st.session_state.chat_hist.append((duvida, processar_ia(duvida, st.session_state.api_key)))
    for q, a in reversed(st.session_state.chat_hist):
        st.info(f"👤 {q}"); st.success(f"🤖 {a}")

st.markdown('<div class="footer">© 2026 Nexus Launcer Lançamento inteligente de produtos digitais</div>', unsafe_allow_html=True)
