import streamlit as st
from groq import Groq
from datetime import timedelta

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="NEXUS LAUNCER", layout="wide")

# --- ESTILO CSS ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { display: none; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3.5em; background-color: #00BFFF !important; color: white !important; font-weight: bold; border: none; }
    .btn-voltar>button { background-color: #64748B !important; }
    .btn-deletar>button { background-color: #94A3B8 !important; height: 2.5em !important; margin-top: 0.5em; }
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

# --- FUNÇÃO CHAT CONTÍNUO ---
def chat_continuo(pergunta, key):
    try:
        client = Groq(api_key=key)
        mensagens = [{"role": "system", "content": "Você é o LaunchBot, especialista em lançamentos digitais de alta conversão."}]
        for q, a in st.session_state.chat_hist:
            mensagens.append({"role": "user", "content": q})
            mensagens.append({"role": "assistant", "content": a})
        mensagens.append({"role": "user", "content": pergunta})
        response = client.chat.completions.create(messages=mensagens, model="llama-3.3-70b-versatile")
        return response.choices[0].message.content
    except Exception as e:
        return f"Erro no chat: {e}"

# --- COMPONENTES ---
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
                if not st.session_state.projetos: st.write("Nenhum projeto salvo.")
                for nome in list(st.session_state.projetos.keys()):
                    col_p_abrir, col_p_del = st.columns([3, 1])
                    with col_p_abrir:
                        if st.button(f"📄 {nome}", key=f"abrir_{nome}"):
                            st.session_state.dados = st.session_state.projetos[nome]
                            st.session_state.etapa = "Visualizacao"
                            st.rerun()
                    with col_p_del:
                        st.markdown('<div class="btn-deletar">', unsafe_allow_html=True)
                        if st.button("EXCLUIR", key=f"del_{nome}"):
                            del st.session_state.projetos[nome]
                            st.rerun()
                        st.markdown('</div>', unsafe_allow_html=True)

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
    nicho = st.text_input("Nicho (ex: ioga)")
    nome_eb = st.text_input("Nome do e-book")
    dor = st.text_input("Qual dor ele resolve")
    preco = st.text_input("Preço")
    data_sel = st.date_input("Selecione a data do lançamento (Liberação)")
    if st.button("AVANÇAR"):
        st.session_state.dados.update({
            "nicho": nicho, "nome_eb": nome_eb, "dor": dor, 
            "preco": preco, "data_obj": data_sel,
            "data_lancto": data_sel.strftime('%d/%m/%Y')
        })
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
        sys_vsl = "Você deve personalizar o texto para o nicho do usuário sem simplificá-lo. Mantenha os parágrafos."
        prompt_vsl = f"Nicho: {st.session_state.dados['nicho']}. Gere um roteiro de VSL focado em convidar para o grupo de WhatsApp, destacando que a falta de direção é o erro principal."
        st.session_state.dados['vsl_roteiro'] = chamar_ia(prompt_vsl, sys_vsl, st.session_state.api_key)
    if 'vsl_roteiro' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['vsl_roteiro']}</div>", unsafe_allow_html=True)
        navegação("Ebook_Gerar", "LP_Gerar")

elif st.session_state.etapa == "LP_Gerar":
    barra_topo()
    st.title("🌐 2. LANDING PAGE")
    if st.button("GERAR ROTEIRO"):
        nicho = st.session_state.dados['nicho']
        st.session_state.dados['lp_roteiro'] = f"Headline: Um caminho simples para {nicho}...\n\nEu sou {st.session_state.usuario} e vou te mostrar o caminho direto.\n\nClique para entrar no grupo."
    if 'lp_roteiro' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['lp_roteiro']}</div>", unsafe_allow_html=True)
        navegação("VSL_Gerar", "MSG_Gerar")

elif st.session_state.etapa == "MSG_Gerar":
    barra_topo()
    st.title("📌 3. MENSAGENS DO GRUPO")
    if st.button("GERAR SEQUÊNCIA DE 3 DIAS"):
        nicho = st.session_state.dados['nicho']
        ebook = st.session_state.dados['nome_eb']
        dor = st.session_state.dados['dor']
        data_f = st.session_state.dados['data_obj']
        data_anterior = (data_f - timedelta(days=1)).strftime('%d/%m/%Y')
        data_venda = data_f.strftime('%d/%m/%Y')
        
        st.session_state.dados['msg_grupo'] = f"""🔥 1ª MENSAGEM
Se você deseja {nicho}, mas sente que está perdido na busca por uma prática de {nicho} eficaz... provavelmente não é falta de esforço. É falta de direção. A maioria das pessoas que começam a praticar {nicho} comete um erro simples: não têm um plano claro e personalizado para alcançar seus objetivos. E por isso, continuam tentando e não saem do lugar. E o pior: nem percebem onde estão errando.
Eu organizei um caminho direto para resolver isso... um material que eu preparei e vou liberar o acesso para todos os membros desse grupo no dia {data_venda}. Fiquem ligados e atentos as mensagens. Até…

🔥 2ª MENSAGEM - DIA {data_anterior}
Amanhã é o dia.
Depois de tanto tempo tentando encontrar uma prática de {nicho} que realmente funcione para você, talvez o que faltava não era mais esforço… era apenas um caminho mais claro.
Muita gente insiste, muda de vídeo, muda de sequência, mas continua sem evolução real — porque segue sem direção definida.
E isso vai mudar a partir de amanhã. Quando será liberado o acesso ao material que eu organizei especialmente para te mostrar um caminho simples, direto e estruturado para evoluir na prática.
Até amanhã, abraços

🔥 3ª MENSAGEM - DIA {data_venda} (LIBERAÇÃO)
Eu falei que hoje ia te mostrar… então presta atenção nisso: O que trava a maioria das pessoas não é falta de esforço… é não entender esse ponto: você não precisa fazer mais… você precisa fazer da forma certa. Enquanto você tenta sem direção… você continua no mesmo lugar. Quando você entende isso… tudo muda. E foi exatamente isso que eu fiz: eu organizei um caminho simples… direto… em um e-book que você poderá acessar hoje com 30% de desconto. 
O método “{ebook}” ele foi pensado para “{dor}”. 
Clique no link agora e garanta o seu. Essa promoção irá acabar a qualquer momento. Obrigado por estar comigo até agora."""

    if 'msg_grupo' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['msg_grupo']}</div>", unsafe_allow_html=True)
        navegação("LP_Gerar", "Visualizacao")

elif st.session_state.etapa == "Visualizacao":
    barra_topo()
    st.title(f"PROJETO: {st.session_state.dados.get('nome_eb')}")
    
    # EXIBINDO TUDO O QUE FOI GERADO
    with st.expander("📚 CONTEÚDO DO E-BOOK", expanded=False):
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('eb_conteudo', 'Não gerado')}</div>", True)
    
    with st.expander("🎬 ROTEIRO DO ANÚNCIO (VSL)", expanded=False):
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('vsl_roteiro', 'Não gerado')}</div>", True)
        
    with st.expander("🌐 LANDING PAGE", expanded=False):
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('lp_roteiro', 'Não gerado')}</div>", True)

    with st.expander("📌 SEQUÊNCIA DE MENSAGENS (3 DIAS)", expanded=True):
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('msg_grupo', 'Não gerado')}</div>", True)
        
    if st.button("💾 SALVAR PROJETO"):
        st.session_state.projetos[st.session_state.dados['nome_eb']] = st.session_state.dados
        st.success("Projeto completo salvo com sucesso!")

# --- RODAPÉ ---
st.markdown(f"<div class='footer'>© 2026 Nexus Launcer Lançamento inteligente</div>", unsafe_allow_html=True)
