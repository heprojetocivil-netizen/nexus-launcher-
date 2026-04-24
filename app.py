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
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO DE ESTADO ---
if 'etapa' not in st.session_state: st.session_state.etapa = "Login"
if 'dados' not in st.session_state: st.session_state.dados = {}
if 'projetos' not in st.session_state: st.session_state.projetos = {}

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
        return f"Erro na API: {e}"

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
                        if st.button("EXCLUIR", key=f"del_{nome}"):
                            del st.session_state.projetos[nome]
                            st.rerun()

def navegação(voltar_para, avancar_para):
    col1, col2 = st.columns(2)
    with col1:
        if st.button("VOLTAR", key=f"btn_v_{voltar_para}"):
            st.session_state.etapa = voltar_para
            st.rerun()
    with col2:
        if st.button("AVANÇAR", key=f"btn_a_{avancar_para}"):
            st.session_state.etapa = avancar_para
            st.rerun()

# --- TELAS ---

if st.session_state.etapa == "Login":
    st.title("NEXUS LAUNCER")
    st.subheader("USO RESTRITO")
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
    nicho = st.text_input("Nicho (ex: Praticar Ioga)")
    nome_eb = st.text_input("Nome do e-book")
    dor = st.text_input("Qual dor ele resolve (ex: Dores nas costas)")
    data_sel = st.date_input("Data da liberação do E-book")
    if st.button("AVANÇAR"):
        st.session_state.dados.update({
            "nicho": nicho, "nome_eb": nome_eb, "dor": dor, 
            "data_obj": data_sel, "data_lancto": data_sel.strftime('%d/%m/%Y')
        })
        st.session_state.etapa = "Ebook_Gerar"
        st.rerun()

elif st.session_state.etapa == "Ebook_Gerar":
    barra_topo()
    st.title("📚 E-BOOK PROFISSIONAL")
    if st.button("GERAR CONTEUDO – 60 CARTÕES"):
        prompt = f"Gere 60 cartões de conteúdo para o eBook '{st.session_state.dados['nome_eb']}' focado em {st.session_state.dados['dor']}."
        st.session_state.dados['eb_conteudo'] = chamar_ia(prompt, "Você é um especialista em eBooks.", st.session_state.api_key)
    if 'eb_conteudo' in st.session_state.dados:
        st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['eb_conteudo']}</div>", unsafe_allow_html=True)
        navegação("Formulario", "VSL_Gerar")

elif st.session_state.etapa == "VSL_Gerar":
    barra_topo()
    st.title("🎬 1. ROTEIRO DO ANÚNCIO (VSL)")
    # ROTEIRO FIXO CONFORME MODELO ORLANDO ROUSSEAU
    nicho = st.session_state.dados['nicho']
    dor = st.session_state.dados['dor']
    st.session_state.dados['vsl_roteiro'] = f"""[ROTEIRO DE ALTA CONVERSÃO]

Se você quer {nicho}, mas sente que está perdido... provavelmente não é falta de esforço. 
É falta de direção. 

A maioria das pessoas comete um erro simples: elas tentam sem um método claro para resolver as {dor}. 
E por isso continuam tentando e não saem do lugar. 

E o pior: nem percebem onde estão errando. 

Eu organizei um caminho direto pra resolver isso... e vou mostrar tudo dentro de um grupo fechado no WhatsApp. 

Sem complicação. É gratuito. 

Clique no botão SAIBA MAIS para entrar no grupo e garantir sua vaga."""
    
    st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['vsl_roteiro']}</div>", unsafe_allow_html=True)
    navegação("Ebook_Gerar", "LP_Gerar")

elif st.session_state.etapa == "LP_Gerar":
    barra_topo()
    st.title("🌐 2. LANDING PAGE")
    nicho = st.session_state.dados['nicho']
    st.session_state.dados['lp_roteiro'] = f"""Headline: Um caminho simples para {nicho}, mesmo começando do zero

Eu sou {st.session_state.usuario}. 
Já estive exatamente onde você está… tentando várias coisas sem resultado.

Até que identifiquei um padrão simples que muda o jogo. 
O problema nunca foi esforço — foi direção.

Eu criei um grupo exclusivo onde vou te mostrar:
- O erro que te mantém travado
- O caminho simples e direto
- O método que realmente funciona

[ BOTÃO: ENTRAR NO GRUPO GRATUITO ]"""
    
    st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['lp_roteiro']}</div>", unsafe_allow_html=True)
    navegação("VSL_Gerar", "MSG_Gerar")

elif st.session_state.etapa == "MSG_Gerar":
    barra_topo()
    st.title("📌 3. MENSAGENS DO GRUPO")
    nicho = st.session_state.dados['nicho']
    ebook = st.session_state.dados['nome_eb']
    dor = st.session_state.dados['dor']
    data_f = st.session_state.dados['data_obj']
    data_anterior = (data_f - timedelta(days=1)).strftime('%d/%m/%Y')
    data_venda = data_f.strftime('%d/%m/%Y')

    st.session_state.dados['msg_grupo'] = f"""🔥 1ª MENSAGEM (BOAS-VINDAS)
Se você deseja {nicho}, mas sente que está perdido... provavelmente não é falta de esforço. É falta de direção. A maioria das pessoas comete um erro simples: não têm um plano claro. Por isso, continuam tentando e não saem do lugar.
Eu organizei um caminho direto para resolver isso... um material que eu preparei e vou liberar o acesso para todos os membros desse grupo no dia {data_venda}. Fiquem ligados!

🔥 2ª MENSAGEM - DIA {data_anterior} (ANTECIPAÇÃO)
Amanhã é o dia. 
Depois de tanto tempo tentando encontrar algo que realmente funcione para você, talvez o que faltava não era mais esforço… era apenas um caminho mais claro. 
Isso vai mudar amanhã, quando liberarei o acesso ao material estruturado para você evoluir de vez. Até amanhã!

🔥 3ª MENSAGEM - DIA {data_venda} (OFERTA)
Eu falei que hoje ia te mostrar… O que trava a maioria não é falta de esforço, é não fazer da forma certa. 
Eu organizei um caminho direto em um e-book que você poderá acessar HOJE com 30% de desconto. 
O método “{ebook}” foi pensado exatamente para eliminar as {dor}. 
Clique no link agora e garanta o seu. Essa promoção acaba a qualquer momento!"""

    st.markdown(f"<div class='caixa-texto'>{st.session_state.dados['msg_grupo']}</div>", unsafe_allow_html=True)
    navegação("LP_Gerar", "Visualizacao")

elif st.session_state.etapa == "Visualizacao":
    barra_topo()
    st.title(f"PROJETO: {st.session_state.dados.get('nome_eb')}")
    
    with st.expander("📚 CONTEÚDO DO E-BOOK"): st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('eb_conteudo')}</div>", True)
    with st.expander("🎬 ANÚNCIO (VSL)"): st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('vsl_roteiro')}</div>", True)
    with st.expander("🌐 LANDING PAGE"): st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('lp_roteiro')}</div>", True)
    with st.expander("📌 MENSAGENS DO GRUPO"): st.markdown(f"<div class='caixa-texto'>{st.session_state.dados.get('msg_grupo')}</div>", True)
    
    if st.button("💾 SALVAR PROJETO"):
        st.session_state.projetos[st.session_state.dados['nome_eb']] = st.session_state.dados
        st.success("Projeto salvo com sucesso!")

st.markdown(f"<div class='footer'>© 2026 Nexus Launcer - Orlando Rousseau</div>", unsafe_allow_html=True)
