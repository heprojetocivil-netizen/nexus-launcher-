import streamlit as st
from groq import Groq

# --- 1. CONFIGURAÇÃO NEXUS ---
st.set_page_config(page_title="NEXUS - MATRIZ PROFISSIONAL", page_icon="🚀", layout="wide")

if 'projetos' not in st.session_state: st.session_state.projetos = {}
if 'etapa' not in st.session_state: st.session_state.etapa = "Formulário"
if 'dados' not in st.session_state: st.session_state.dados = {}

api_key = "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"

def gerar_ia(prompt, system):
    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile"
        )
        return response.choices[0].message.content
    except Exception as e: return f"Erro na conexão: {e}"

# --- DESIGN ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #F1F5F9; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #00BFFF !important; color: white !important; font-weight: bold; border: none; }
    .status-box { background-color: #E0F2FE; padding: 15px; border-radius: 10px; border-left: 5px solid #00BFFF; margin-bottom: 20px; }
    .instrucao { background-color: #f9f9f9; padding: 10px; border-radius: 5px; border-left: 3px solid #00BFFF; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR: GESTÃO DE PROJETOS ---
with st.sidebar:
    st.title("📂 PROJETOS")
    if st.session_state.projetos:
        for p_nome in st.session_state.projetos.keys():
            if st.button(f"📄 {p_nome}"):
                st.session_state.dados = st.session_state.projetos[p_nome]
                st.session_state.etapa = "Visualização Total"
                st.rerun()
    st.markdown("---")
    if st.button("➕ NOVO PROJETO"):
        st.session_state.etapa = "Formulário"
        st.session_state.dados = {}
        st.rerun()

# --- ETAPA 1: FORMULÁRIO E PROCESSAMENTO AUTOMÁTICO ---
if st.session_state.etapa == "Formulário":
    st.title("🧠 1. INTELIGÊNCIA DO FUNIL")
    st.write("Preencha os dados e a IA criará o funil completo automaticamente.")
    
    with st.form("form_matriz"):
        col1, col2 = st.columns(2)
        with col1:
            nome_p = st.text_input("Nome do Projeto")
            nicho = st.text_input("Nicho")
            publico = st.text_input("Público-alvo")
            resultado = st.text_input("Resultado Específico (ex: primeira venda em 7 dias)")
            tentou = st.text_area("O que já tentou e não funcionou?")
        with col2:
            dificuldade = st.text_area("Maior dificuldade hoje")
            medo = st.text_area("Maior medo")
            preco = st.text_input("Preço do Produto")
            garantia = st.text_input("Garantia (ex: 7 dias)")
        
        gerar_tudo = st.form_submit_button("🚀 GERAR FUNIL COMPLETO")

        if gerar_tudo and nome_p:
            with st.status("Construindo Funil de Alta Conversão...", expanded=True) as status:
                d = {"nome": nome_p, "nicho": nicho, "publico": publico, "resultado": resultado, "tentou": tentou, "dificuldade": dificuldade, "medo": medo, "preco": preco, "garantia": garantia}
                
                st.write("📦 Criando E-book (60 Cartões)...")
                d['ebook'] = gerar_ia(f"Crie um roteiro de e-book com 60 cartões educativos sobre {nicho} focado em {resultado}.", "Escritor de Infoprodutos")
                
                st.write("🎬 Criando Anúncio (VSL Curta)...")
                d['vsl_anuncio'] = gerar_ia(f"Crie uma copy de VSL curta para anúncio no nicho {nicho}. Use a estrutura: 'Se já tentou {tentou} e não conseguiu {resultado}... erro invisível... método simples... entra no grupo'.", "Copywriter de Alta Performance")
                
                st.write("🌐 Criando Landing Page...")
                d['lp'] = gerar_ia(f"Crie uma Landing Page para {nicho}. Headline sobre {resultado}, texto de autoridade do Orlando, conexão emocional e bullets matadores.", "Especialista em Landing Pages")
                
                st.write("📌 Criando Mensagem do Grupo...")
                d['msg_grupo'] = gerar_ia(f"Crie a mensagem fixa do grupo silencioso para {nicho}. Foco no {resultado}.", "Gestor de Grupos")
                
                st.write("📅 Criando Aquecimento (7 Dias)...")
                d['aquecimento'] = gerar_ia(f"Crie 7 mensagens de aquecimento psicológico para {nicho}. Siga: Dia 1 Confronto, 2 Crença, 3 Revelação, 4 Lógica, 5 Tensão, 6 Pré-revelação, 7 Venda.", "Psicólogo de Vendas")
                
                st.write("🎬 Criando VSL de Venda Final + CTA no Link...")
                d['vsl_final'] = gerar_ia(f"Crie o roteiro da VSL final de venda para {nicho}. Preço {preco}, Garantia {garantia}. Foque no erro invisível e no mecanismo único. NO FINAL DO VÍDEO, dê uma instrução clara para a pessoa clicar no link da descrição para acessar o e-book agora.", "Copywriter de Elite")
                d['desc_venda'] = gerar_ia(f"Crie uma descrição rápida e matadora para colocar abaixo do vídeo de vendas ou no WhatsApp, chamando para o link de compra do produto de {nicho} por R$ {preco}.", "Copywriter de Alta Conversão")
                
                st.session_state.dados = d
                st.session_state.projetos[nome_p] = d
                status.update(label="✅ Funil Completo Gerado!", state="complete", expanded=False)
                st.session_state.etapa = "Visualização Total"
                st.rerun()

# --- ETAPA 2: VISUALIZAÇÃO E CÓPIA ---
elif st.session_state.etapa == "Visualização Total":
    d = st.session_state.dados
    st.title(f"🚀 PROJETO: {d['nome']}")
    st.markdown(f"**Nicho:** {d['nicho']} | **Resultado:** {d['resultado']}")
    
    st.info("Clique nas abas abaixo para copiar o conteúdo e ver como aplicar.")

    with st.expander("📦 1. E-BOOK (60 CARTÕES)"):
        st.code(d.get('ebook', ''), language="markdown")

    with st.expander("🎬 2. VSL DO ANÚNCIO (SCRIPT)"):
        st.code(d.get('vsl_anuncio', ''), language="markdown")

    with st.expander("🌐 3. LANDING PAGE (TEXTO COMPLETO)"):
        st.code(d.get('lp', ''), language="markdown")

    with st.expander("📌 4. MENSAGEM FIXA DO GRUPO"):
        st.code(d.get('msg_grupo', ''), language="markdown")

    with st.expander("📅 5. AQUECIMENTO (7 MENSAGENS)"):
        st.code(d.get('aquecimento', ''), language="markdown")

    with st.expander("🎬 6. VSL DE VENDA FINAL (OFERTA + DESCRIÇÃO)"):
        st.subheader("Script do Vídeo (Com CTA para o Link da Descrição)")
        st.code(d.get('vsl_final', ''), language="markdown")
        st.markdown("---")
        st.subheader("📝 Descrição para o Link de Vendas")
        st.write("Use este texto logo abaixo do vídeo (na descrição do YouTube/Vimeo) ou na mensagem de fechamento:")
        st.code(d.get('desc_venda', ''), language="markdown")

    with st.expander("🛠️ 7. COMO APLICAR (PASSO A PASSO)"):
        st.markdown(f"""
        ### 🗺️ Guia de Implementação
        
        **1. O E-book (60 Cartões)**
        * **Onde criar:** Vá ao **Canva**. Use um template de "Post para Instagram" ou "E-book".
        * **Como fazer:** Copie cada um dos 60 textos gerados e coloque um em cada página. Salve como **PDF**.
        
        **2. VSL do Anúncio**
        * **Onde criar:** Use o **CapCut**.
        * **Como fazer:** Grave um vídeo curto seguindo o script. Suba no **Facebook/Google Ads** levando para sua Landing Page.
        
        **3. Landing Page (Captura)**
        * **Onde criar:** **Elementor** ou **Typebot**.
        * **Como fazer:** Use a Headline e os Bullets gerados. O botão leva para o seu **Grupo de WhatsApp**.
        
        **4. O Vídeo de Vendas (VSL Final)**
        * **Onde criar:** **CapCut**.
        * **Onde colocar:** Hospede no **YouTube (Não listado)**. 
        * **IMPORTANTE:** Coloque o seu link de checkout (Hotmart/Kiwify) na **primeira linha da descrição do vídeo**, pois você orientou o cliente a clicar lá no final do script.
        
        **5. O Link de Pagamento (Checkout)**
        * **Configuração:** Preço **R$ {d.get('preco')}** e Garantia de **{d.get('garantia')}**. 
        * **Ação:** Copie a **Descrição para o Link de Vendas** (Aba 6), insira seu link e cole na descrição do vídeo e no grupo.
        """)

    st.success("O projeto está salvo na barra lateral. Copie os textos e siga o passo a passo de aplicação.")

st.markdown(f'<div style="position: fixed; bottom: 0; left: 0; width: 100%; background-color: #00BFFF; color: white; text-align: center; padding: 10px;">NEXUS — MATRIZ DE ALTA CONVERSÃO</div>', unsafe_allow_html=True)
