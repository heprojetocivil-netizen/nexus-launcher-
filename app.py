import streamlit as st
from groq import Groq
from datetime import datetime, timedelta

# --- 1. CONFIGURAÇÃO E DESIGN "NEXUS" ---
st.set_page_config(page_title="NEXUS: MATRIZ DE LANÇAMENTO", page_icon="🎯", layout="wide")

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

# --- 4. FLUXO NEXUS: MATRIZ DE NICHO ---

if st.session_state.etapa == 0:
    st.title("🧠 NEXUS: MATRIZ DE INTELIGÊNCIA")
    st.write("### Estrutura Psicológica: Curiosidade → Direção → Decisão")
    
    col1, col2 = st.columns(2)
    with col1:
        # Aqui a pessoa escolhe o nicho (Matriz)
        st.session_state.memoria['nicho'] = st.text_input("Defina o Nicho do Projeto:", placeholder="Ex: Licitações, Marketing, Culinária...")
    with col2:
        st.session_state.memoria['data_inicio'] = datetime.now().strftime("%d/%m/%Y")

    if st.button("INICIAR MATRIZ"):
        if st.session_state.memoria['nicho']: st.session_state.etapa = 1; st.rerun()

elif st.session_state.etapa == 1:
    st.title("🎬 1. ANÚNCIO E SETUP DO GRUPO")
    st.markdown(f"<div class='instruction-box'><b>Nicho Ativo:</b> {st.session_state.memoria['nicho']}</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    if st.button(f"🧠 GERAR ANÚNCIO DIRETO: {st.session_state.memoria['nicho'].upper()}"):
        nicho = st.session_state.memoria['nicho']
        p = f"""Adapte este modelo de anúncio seco e direto para o nicho {nicho}:
        ESTRUTURA: 'Se você quer ganhar dinheiro... talvez esteja ignorando o maior [Comprador/Oportunidade] do [Nicho]. Existe um caminho simples mesmo do zero. Criei um grupo. Clique e entra.'
        Também gere o Nome do Grupo e a Mensagem Fixada de Boas-vindas seguindo o estilo 'Grupo Silencioso'."""
        st.session_state.memoria['etapa1_copy'] = nexus_ai(p, "Estrategista de Copywriting Direto", api_key)
    
    if 'etapa1_copy' in st.session_state.memoria:
        st.info(st.session_state.memoria['etapa1_copy'])
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("GERAR AQUECIMENTO (2 SEMANAS) 👉"): st.session_state.etapa = 2; st.rerun()

elif st.session_state.etapa == 2:
    st.title("📆 2. CRONOGRAMA PSICOLÓGICO")
    st.markdown("<div class='instruction-box'><b>Estratégia:</b> Gerar curiosidade constante e autoridade implícita.</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    if st.button("📅 GERAR 10 DIAS DE PROVOCAÇÃO"):
        nicho = st.session_state.memoria['nicho']
        p = f"""Gere 10 mensagens de aquecimento para o grupo de {nicho}.
        ESTILO: Frases curtas, muito espaço, provocação psicológica.
        TEMAS: Competir com o comum vs oportunidade oculta, a falta de direção, o erro de nem tentar, o jeito simples de entrar, e a preparação para 'O Caminho' que será revelado."""
        st.session_state.memoria['cronograma_2s'] = nexus_ai(p, "Expert em Gatilhos Mentais", api_key)
    
    if 'cronograma_2s' in st.session_state.memoria:
        st.write(st.session_state.memoria['cronograma_2s'])
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("GERAR SEMANA DE VENDAS 👉"): st.session_state.etapa = 3; st.rerun()

elif st.session_state.etapa == 3:
    st.title("💰 3. OFERTA E FECHAMENTO")
    st.markdown("<div class='instruction-box'><b>Ação:</b> Conversão direta usando escassez e decisão.</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    if st.button("🚀 GERAR SEQUÊNCIA DE FECHAMENTO (5 DIAS)"):
        nicho = st.session_state.memoria['nicho']
        p = f"""Adapte a sequência de 5 dias de fechamento para o nicho {nicho}:
        Dia 1: Abertura (Método organizado).
        Dia 2: Quebra de dúvida (Explicado de forma simples).
        Dia 3: O jogo certo.
        Dia 4: Mudança de nível.
        Dia 5: Fechamento forte (Quem entrou entrou)."""
        st.session_state.memoria['venda_final'] = nexus_ai(p, "Diretor de Vendas", api_key)
        
    if 'venda_final' in st.session_state.memoria:
        st.success(st.session_state.memoria['venda_final'])
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("CONCLUIR MATRIZ"):
        st.balloons()
        st.success(f"Funil de {st.session_state.memoria['nicho']} Finalizado!")

if st.session_state.etapa > 0:
    if st.button("⬅ VOLTAR"): st.session_state.etapa -= 1; st.rerun()

st.markdown(f'<div class="footer">NEXUS — MATRIZ DE ESTRATÉGIA ADAPTÁVEL</div>', unsafe_allow_html=True)
