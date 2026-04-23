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

# --- INICIALIZAÇÃO DE ESTADO ---
if 'etapa' not in st.session_state: st.session_state.etapa = "Login"
if 'dados' not in st.session_state: st.session_state.dados = {}
if 'projetos' not in st.session_state: st.session_state.projetos = {}
if 'chat_hist' not in st.session_state: st.session_state.chat_hist = []

# --- FUNÇÃO DE IA ---
def chamar_ia(prompt, system_prompt, key):
    try:
        client = Groq(api_key=key)
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile",
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Erro na API: Verifique sua chave. {e}"

# --- COMPONENTES REUTILIZÁVEIS ---
def barra_topo():
    if st.session_state.etapa != "Login":
        col_new, col_proj = st.columns(2)
        with col_new:
            if st.button("➕ INICIAR NOVO PROJETO"):
                st.session_state.dados = {}
                st.session_state.etapa = "Formulario"
                st.rerun()
        with col_proj:
            with st.expander("📂 MEUS PROJETOS"):
                if not st.session_state.projetos:
                    st.write("Nenhum projeto salvo.")
                for nome in st.session_state.projetos.keys():
                    if st.button(f"📄 {nome}"):
                        st.session_state.dados = st.session_state.projetos[nome]
                        st.session_state.etapa = "Visualizacao"
                        st.rerun()

def navegação(voltar_para, avancar_para):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="btn-voltar">', unsafe_allow_html=True)
        if st.button("VOLTAR", key=f"btn_v_{voltar_para}"):
            st.session_state.etapa = voltar_para
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        if st.button("AVANÇAR", key=f"btn_a_{avancar_para}"):
            st.session_state.etapa = avancar_para
            st.rerun()

# --- FLUXO DE TELAS ---

if st.session_state.etapa == "Login":
    st.title("NEXUS LAUNCER")
    st.subheader("USO RESTRITO À ASSOCIADOS QUIZ MAIS PRÊMIOS")
    st.info("Não coloque senha do site, só a chave api_key")
    nome_usuario = st.text_input("Nome")
    chave_api = st.text_input("Chave", type="password")
    if st.button("ENTRAR"):
        if nome_usuario and chave_api:
            st.session_state.usuario = nome_usuario
            st.session_state.api_key = chave_api
            st.session_state.etapa = "Formulario"
            st.rerun()

elif st.session_state.etapa == "Formulario":
    barra_topo()
    st.title("PREENCHA FORMULÁRIO")
    nicho = st.text_input("Nicho")
    nome_eb = st.text_input("Nome do e-book")
    dor = st.text_input("Qual dor ele resolve")
    preco = st.text_input("Preço")
    if st.button("AVANÇAR"):
        st.session_state.dados.update({"nicho": nicho, "nome_eb": nome_eb, "dor": dor, "preco": preco})
        st.session_state.etapa = "Ebook_Gerar"
        st.rerun()

elif st.session_state.etapa == "Ebook_Gerar":
    barra_topo()
    st.title("📚 E-BOOK PROFISSIONAL")
    if st.button("GERAR CONTEUDO – 60 CARTÕES"):
        prompt = f"Gere 60 cartões de conteúdo para o eBook '{st.session_state.dados['nome_eb']}' no nicho {st.session_state.dados['nicho']} focado em resolver a dor: {st.session_state.dados['dor']}."
        st.session_state.dados['eb_conteudo'] = chamar_ia(prompt, "Você é um especialista em criação de eBooks.", st.session_state.api_key)
    
    if 'eb_conteudo' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['eb_conteudo']}</div>", unsafe_allow_html=True)
        navegação("Formulario", "VSL_Gerar")

elif st.session_state.etapa == "VSL_Gerar":
    barra_topo()
    st.title("🎬 1. VSL DO ANÚNCIO")
    if st.button("GERAR ROTEIRO"):
        sys_vsl = "Você deve personalizar o texto para o nicho do usuário sem simplificá-lo. Mantenha os parágrafos. Oriente também sobre as imagens e onde encaixá-las de forma 100% personalizada."
        prompt_vsl = f"Nicho: {st.session_state.dados['nicho']}. Texto base: Se você quer [RESULTADO], mas sente que está perdido... provavelmente não é falta de esforço. É falta de direção. A maioria das pessoas comete um erro simples... e por isso continua tentando e não sai do lugar. E o pior: nem percebem onde estão errando. Eu organizei um caminho direto pra resolver isso... e vou mostrar dentro de um grupo fechado. Sem complicação. É gratuito. Clica em SAIBA MAIS para entrar"
        st.session_state.dados['vsl_roteiro'] = chamar_ia(prompt_vsl, sys_vsl, st.session_state.api_key)
    
    if 'vsl_roteiro' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['vsl_roteiro']}</div>", unsafe_allow_html=True)
        navegação("Ebook_Gerar", "LP_Gerar")

elif st.session_state.etapa == "LP_Gerar":
    barra_topo()
    st.title("🌐 2. LANDING PAGE")
    if st.button("GERAR ROTEIRO"):
        sys_lp = "Personalize o texto para o nicho sem simplificá-lo, mantendo parágrafos."
        prompt_lp = f"Nome: {st.session_state.usuario}. Nicho: {st.session_state.dados['nicho']}. Texto base: Headline: Um caminho simples para [RESULTADO], mesmo começando do zero. Eu sou {st.session_state.usuario}. Já estive exatamente onde você está... tentando várias coisas... sem resultado. Até começar a estudar e aplicar o que realmente funciona... e identificar um padrão simples que muda completamente o jogo. Depois de aplicar isso na prática... eu percebi que o problema nunca foi esforço — foi direção. Se você sente que está tentando... mas não sai do lugar... provavelmente está passando por isso também. Eu criei um grupo onde vou te mostrar isso de forma direta. O erro que te mantém travado. O caminho mais simples. O que realmente funciona na prática. ENTRAR NO GRUPO"
        st.session_state.dados['lp_roteiro'] = chamar_ia(prompt_lp, sys_lp, st.session_state.api_key)
    
    if 'lp_roteiro' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['lp_roteiro']}</div>", unsafe_allow_html=True)
        navegação("VSL_Gerar", "MSG_Gerar")

elif st.session_state.etapa == "MSG_Gerar":
    barra_topo()
    st.title("📌 3. MENSAGEM FIXA DO GRUPO")
    if st.button("GERAR MENSAGENS PARA O GRUPO"):
        # Lógica de fidelidade total para mensagens 1 a 5
        nicho = st.session_state.dados['nicho']
        ebook = st.session_state.dados['nome_eb']
        st.session_state.dados['msg_grupo'] = f"""DESCRIÇÃO DO GRUPO
Esse grupo é silencioso. Você não será incomodado hora nenhuma.
Eu vou te mostrar um caminho simples para {nicho}.
Não é teoria… é algo direto.
Fica até o final.

🔥 DIA 1
Deixa eu te fazer uma pergunta direta:
Você sente que está no caminho certo… ou só tentando coisas e esperando dar certo?

🔥 DIA 2
A maioria das pessoas não falha por falta de esforço… falha porque está andando na direção errada. E o pior: só percebe depois de muito tempo.

🔥 DIA 3
Existe um ponto simples que separa quem consegue resultado… de quem continua tentando. E não tem nada a ver com trabalhar mais.

🔥 DIA 4
Quando você entende isso… você para de perder tempo com o que não funciona. E começa a focar no que realmente dá resultado.

🔥 DIA 5
Eu poderia explicar tudo aqui… mas a maioria das pessoas não aplicaria. Então amanhã eu vou te mostrar isso de forma diferente.

🔥 DIA 6
Eu falei que hoje ia te mostrar… então presta atenção nisso: O que trava a maioria das pessoas não é falta de esforço… é não entender esse ponto: você não precisa fazer mais… você precisa fazer da forma certa. Enquanto você tenta sem direção… você continua no mesmo lugar. Quando você entende isso… tudo muda. E foi exatamente isso que eu fiz: eu organizei um caminho simples… direto… pra chegar em {nicho}. E coloquei tudo isso em um eBook simples e direto ao ponto: {ebook}. Você pode acessar agora… com garantia de 7 dias. O acesso já está liberado. Clica no link e vê todos os detalhes.

DESCRIÇÃO: Clique no link para acessar o seu e-book com 30% de desconto, somente hoje."""

    if 'msg_grupo' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['msg_grupo']}</div>", unsafe_allow_html=True)
        navegação("LP_Gerar", "Visualizacao")

elif st.session_state.etapa == "Visualizacao":
    barra_topo()
    st.title(f"PROJETO: {st.session_state.dados.get('nome_eb')}")
    
    with st.expander("📚 E-BOOK", expanded=False): st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('eb_conteudo')}</div>", True)
    with st.expander("🎬 1. VSL DO ANÚNCIO", expanded=False): st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('vsl_roteiro')}</div>", True)
    with st.expander("🌐 2. LANDING PAGE", expanded=False): st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('lp_roteiro')}</div>", True)
    with st.expander("📌 3. MENSAGENS", expanded=False): st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('msg_grupo')}</div>", True)
    with st.expander("📅 APLICAÇÃO", expanded=False):
        st.markdown("""<div class='caixa-texto'>🚀 Sistema de lançamento simplificado
📘 1. Criação do produto
- Gere o seu eBook usando o Gamma AI
- Cadastre o produto na plataforma Monetizze 
- Estruture o material de forma simples e direta para venda 

🎬 2. VSL (Vídeo de Vendas)
- Crie o vídeo do anúncio e o vídeo de vendas na plataforma Heygen e suba no Youtube
- Crie a LP usando o Gamma e insira o link do grupo
- Insira o link da Monetizze na descrição do vídeo de vendas

👥 4. Estrutura do grupo
- Crie o grupo na segunda-feira 
- Segunda a sexta: Anuncie e preencha o grupo

🔥 5. Sequência de vendas
- Na semana seguinte, inicie as mensagens
- Finalize levando para a oferta na Monetizze</div>""", True)

    if st.button("💾 SALVAR PROJETO"):
        st.session_state.projetos[st.session_state.dados['nome_eb']] = st.session_state.dados
        st.success("Projeto salvo com sucesso!")

    st.divider()
    st.subheader("💬 LaunchBot")
    st.write("Eu sou o LaunchBot, especialista em lançamentos digitais de alta conversão")
    msg_chat = st.text_input("Digite a sua dúvida e aperte Enter", key="chat_input")
    if msg_chat:
        resp = chamar_ia(msg_chat, "Você é o LaunchBot, especialista em marketing digital.", st.session_state.api_key)
        st.session_state.chat_hist.append((msg_chat, resp))
    
    for q, a in reversed(st.session_state.chat_hist):
        st.markdown(f"**Você:** {q}")
        st.markdown(f"<div class='chat-bubble'>{a}</div>", unsafe_allow_html=True)

# --- RODAPÉ ---
st.markdown(f"<div class='footer'>© 2026 Nexus Launcer Lançamento inteligente de produtos digitais</div>", unsafe_allow_html=True)
