import streamlit as st
from groq import Groq
from datetime import datetime, timedelta

# --- 1. CONFIGURAÇÃO E DESIGN "NEXUS" ---
st.set_page_config(page_title="NEXUS: DIRETOR DE LANÇAMENTO", page_icon="🧠", layout="wide")

if 'memoria' not in st.session_state: st.session_state.memoria = {}
cor_tema = "#00BFFF" 

st.markdown(f"""
    <style>
    [data-testid="stSidebar"] {{ display: none; }}
    header {{ visibility: hidden; }}
    .stApp {{ background-color: #FFFFFF; color: #000000; padding-bottom: 100px; }}
    h1, h2, h3, h4, p, span, label, .stMarkdown, .stMarkdown p {{ color: #000000 !important; font-family: 'Inter', sans-serif; }}
    .nexus-card {{ background: #F8FAFC !important; border: 2px solid {cor_tema}; padding: 25px; border-radius: 20px; margin-bottom: 20px; }}
    .stButton > button {{ background: {cor_tema} !important; color: #FFFFFF !important; padding: 15px 25px !important; font-weight: bold !important; border-radius: 12px !important; width: 100% !important; text-transform: uppercase; border: none; }}
    .instruction-box {{ background-color: #F1F5F9; border-left: 5px solid {cor_tema}; padding: 15px; border-radius: 8px; margin: 10px 0; font-size: 0.9em; }}
    .footer {{ position: fixed; left: 0; bottom: 0; width: 100%; background-color: {cor_tema}; color: #FFFFFF; text-align: center; padding: 10px; z-index: 1000; }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. LÓGICA DE INTELIGÊNCIA ---
def nexus_ai(prompt, system_role, api_key):
    try:
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            messages=[{"role": "system", "content": system_role}, {"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile"
        )
        return completion.choices[0].message.content
    except Exception as e: return f"Erro: {str(e)}"

# --- 3. ESTADO ---
if 'etapa' not in st.session_state: st.session_state.etapa = 0
api_key = "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"

# --- 4. FLUXO NEXUS ---

if st.session_state.etapa == 0:
    st.title("🧠 NEXUS: SISTEMA DIRETOR DE LANÇAMENTO")
    st.write("### Estratégia: Criação do E-book → Captação → Distribuição → Live de Venda")
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.memoria['nicho'] = st.text_input("Nicho do E-book:", placeholder="Ex: Culinária Gourmet")
        st.session_state.memoria['data_inicio'] = datetime.now().strftime("%d/%m/%Y")
    with col2:
        st.session_state.memoria['data_live'] = st.date_input("Data da Live de Venda:")
    
    if st.button("INICIAR PRODUÇÃO"):
        if st.session_state.memoria['nicho']: st.session_state.etapa = 1; st.rerun()

elif st.session_state.etapa == 1:
    st.title("📄 1. O PRODUTO E MONETIZZE")
    st.markdown("<div class='instruction-box'><b>Ação:</b> Crie os 60 cartões e cadastre na Monetizze.</div>", unsafe_allow_html=True)
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    if st.button("🧠 GERAR CONTEÚDO: E-BOOK (60 CARTÕES)"):
        p = f"Crie um roteiro de 60 cartões educativos sobre {st.session_state.memoria['nicho']}. Cada cartão deve ser prático."
        st.session_state.memoria['ebook_60'] = nexus_ai(p, "Escritor de Infoprodutos", api_key)
    
    if 'ebook_60' in st.session_state.memoria:
        st.info(st.session_state.memoria['ebook_60'])
        st.markdown("---")
        st.subheader("🛠️ ORIENTAÇÃO MONETIZZE")
        st.write("1. Cadastre o produto como **E-book (PDF)**.\n2. No checkout, defina o preço.\n3. Copie o **Link** para a live.")
    st.markdown("</div>", unsafe_allow_html=True)
    if st.button("GERAR ANÚNCIO E PÁGINA 👉"): st.session_state.etapa = 2; st.rerun()

elif st.session_state.etapa == 2:
    st.title("📢 2. ATRAÇÃO E ESTRUTURA")
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    
    if st.button("🎬 GERAR SCRIPT DE VÍDEO + DADOS DA LANDING PAGE"):
        data_f = st.session_state.memoria['data_live'].strftime("%d/%m/%Y")
        nicho = st.session_state.memoria['nicho']
        
        # PROMPT PADRONIZADO ANUNCIO
        p_video = f"""Adapte este roteiro de anúncio para o nicho {nicho}. 
        Mantenha a estrutura: 'Você já imaginou [Desejo]?', 'Convite para o minicurso gratuito [Nome do Curso]', data {data_f} às 20h. 
        Inclua os tópicos: possibilidades do nicho, segredos por trás, caminho percorrido, se tornar referência e montar negócio. 
        Finalize com: 'Esse anúncio provavelmente não aparecerá de novo'."""
        st.session_state.memoria['script_ads'] = nexus_ai(p_video, "Diretor de Criativos", api_key)
        
        # PROMPT PADRONIZADO LP
        p_lp = f"""Adapte este roteiro de Landing Page para o nicho {nicho}.
        Headline impactante, 'Quem sou eu' adaptado, lista 'Você vai conhecer' com 7 tópicos, seção 'Por que este minicurso é para você', 
        Data {data_f} às 20h, Depoimentos fictícios coerentes e FAQ (experiência prévia, equipamentos, gravação)."""
        st.session_state.memoria['copy_lp'] = nexus_ai(p_lp, "Copywriter de Alta Conversão", api_key)
    
    if 'script_ads' in st.session_state.memoria:
        st.subheader("🎥 Script do Vídeo Convite")
        st.info(st.session_state.memoria['script_ads'])
        st.subheader("🌐 Dados da Landing Page")
        st.success(st.session_state.memoria['copy_lp'])
    st.markdown("</div>", unsafe_allow_html=True)
    if st.button("DISTRIBUIÇÃO NO WHATSAPP 👉"): st.session_state.etapa = 3; st.rerun()

elif st.session_state.etapa == 3:
    st.title("📲 3. CALENDÁRIO E WHATSAPP")
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    if st.button("📅 GERAR MENSAGENS PADRONIZADAS"):
        data_f = st.session_state.memoria['data_live'].strftime("%d/%m/%Y")
        nicho = st.session_state.memoria['nicho']
        p = f"""Adapte rigorosamente as seguintes mensagens para o nicho {nicho}:
        1. Descrição do Grupo (Data: {data_f} às 20h).
        2. Boas-vindas (Lista de 6 benefícios).
        3. Aquecimento (1 dia antes).
        4. Dia do Evento (Hoje às 20h, link às 19:50).
        5. Hora do Evento (Estamos ao vivo).
        6. Convite Compra E-book (Com índice de 7 tópicos atraentes do e-book).
        7. Pós-vendas (Última chance, 65% já adquiriram).
        8. Última chamada (Oferta encerra hoje)."""
        st.session_state.memoria['whats_cronograma'] = nexus_ai(p, "Estrategista de WhatsApp", api_key)
    
    if 'whats_cronograma' in st.session_state.memoria:
        st.write(st.session_state.memoria['whats_cronograma'])
    st.markdown("</div>", unsafe_allow_html=True)
    if st.button("Ir para a live 👉"): st.session_state.etapa = 4; st.rerun()

elif st.session_state.etapa == 4:
    st.title("🔴 4. MATERIAL FINAL DA LIVE (3 PARTES)")
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    if st.button("🚀 GERAR LIVE COMPLETA PERSONALIZADA"):
        nicho = st.session_state.memoria['nicho']
        
        # ROLE PARA PERSONALIZAÇÃO COMPLETA DAS 3 PARTES
        role_live = f"""Você é um Roteirista de Elite. Adapte 100% as 3 PARTES do roteiro para o nicho {nicho}.
        PARTE 1: Jornada do Herói (Mundo comum até Elixir).
        PARTE 2: Conectando ao tema (Introdução, Identificação, Curiosidade, Exemplos Reais, Evolução, Interesse, Benefícios Práticos).
        PARTE 3: Conectando à oferta (Promessa de transformação e chamada para o E-book).
        DIRETRIZES: Linguagem adequada ao nicho, mantenha gatilhos, dores e desejos adaptados. 
        Mantenha o mesmo número de caracteres e estrutura idêntica de tópicos."""
        
        st.session_state.memoria['script_live'] = nexus_ai(f"Gere o roteiro completo de 3 partes para {nicho}", role_live, api_key)
        
        p_desc = f"Crie a descrição do vídeo para {nicho}. Primeira linha: 'Clique no link para acessar o e-book: [LINK]'."
        st.session_state.memoria['desc_video_final'] = nexus_ai(p_desc, "Copywriter", api_key)

    if 'script_live' in st.session_state.memoria: 
        st.subheader("🎬 Script da Live Completo (Partes 1, 2 e 3)")
        st.write(st.session_state.memoria['script_live'])
        st.markdown("---")
        st.subheader("📝 Descrição do Vídeo")
        st.success(st.session_state.memoria['desc_video_final'])
    st.markdown("</div>", unsafe_allow_html=True)
    if st.button("CONCLUIR LANÇAMENTO"):
        st.balloons(); st.success("Lançamento Totalmente Estruturado!")

if st.session_state.etapa > 0:
    if st.button("⬅ VOLTAR"): st.session_state.etapa -= 1; st.rerun()

st.markdown(f'<div class="footer">NEXUS — ESTRUTURA PADRONIZADA APLICADA</div>', unsafe_allow_html=True)
