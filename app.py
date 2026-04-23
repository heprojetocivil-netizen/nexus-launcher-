import streamlit as st
from groq import Groq
from datetime import datetime

# --- 1. CONFIGURAÇÃO E DESIGN "NEXUS" ---
st.set_page_config(page_title="NEXUS: SISTEMA DE VENDAS DIRETAS", page_icon="🎯", layout="wide")

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

# --- 3. ESTADO E CHAVE ---
if 'etapa' not in st.session_state: st.session_state.etapa = 0
api_key = "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"

# --- 4. FLUXO DO PROJETO ---

if st.session_state.etapa == 0:
    st.title("🎯 NEXUS: FUNIL DE AQUECIMENTO PSICOLÓGICO")
    st.write("### Estratégia: 60 Cartões → Anúncio → 2 Semanas de Grupo → Venda Direta")
    
    nicho = st.text_input("Qual o nicho do projeto?", placeholder="Ex: Licitações, Marketing Digital, Culinária...")
    
    if st.button("INICIAR SISTEMA"):
        if nicho: 
            st.session_state.memoria['nicho'] = nicho
            st.session_state.etapa = 1
            st.rerun()

elif st.session_state.etapa == 1:
    st.title("📘 1. PRODUÇÃO DO PRODUTO (E-BOOK)")
    st.markdown("<div class='instruction-box'><b>Ação:</b> Criando a base de conhecimento do seu e-book.</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    if st.button("🧠 GERAR ROTEIRO: 60 CARTÕES EDUCATIVOS"):
        nicho = st.session_state.memoria['nicho']
        p = f"Crie um roteiro detalhado de 60 cartões educativos e práticos para um e-book sobre {nicho}. Cada cartão deve ser uma lição rápida."
        st.session_state.memoria['ebook_60'] = nexus_ai(p, "Escritor de Infoprodutos", api_key)
    
    if 'ebook_60' in st.session_state.memoria:
        st.info(st.session_state.memoria['ebook_60'])
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("GERAR ANÚNCIO REFINADO 👉"): st.session_state.etapa = 2; st.rerun()

elif st.session_state.etapa == 2:
    st.title("🎬 2. ANÚNCIO (ESTILO REFINADO)")
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    
    if st.button("🎬 GERAR SCRIPT DE ANÚNCIO"):
        nicho = st.session_state.memoria['nicho']
        p = f"""Adapte este modelo de anúncio para o nicho {nicho}:
        'Se você quer começar a ganhar dinheiro... talvez esteja ignorando o maior [Comprador/Oportunidade]. [Explicação Curta]. Existe um caminho simples mesmo do zero. Criei um grupo onde vou mostrar isso na prática. É gratuito. Clique e entra.'
        Mantenha o tom direto e os espaçamentos curtos."""
        st.session_state.memoria['anuncio_refinado'] = nexus_ai(p, "Copywriter Minimalista", api_key)
    
    if 'anuncio_refinado' in st.session_state.memoria:
        st.success(st.session_state.memoria['anuncio_refinado'])
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("GERAR 2 SEMANAS DE AQUECIMENTO 👉"): st.session_state.etapa = 3; st.rerun()

elif st.session_state.etapa == 3:
    st.title("📆 3. AQUECIMENTO PSICOLÓGICO (10 DIAS)")
    st.markdown("<div class='instruction-box'><b>Estratégia:</b> Gerar curiosidade, autoridade e o sentimento de 'preciso disso'.</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    if st.button("📅 GERAR MENSAGENS (SEMANA 1 E 2)"):
        nicho = st.session_state.memoria['nicho']
        p = f"""Adapte rigorosamente os temas abaixo para o nicho {nicho}:
        SEMANA 1 (DESPERTAR):
        Dia 1: Depender de cliente comum = competir com todos.
        Dia 2: O cliente que compra todo dia e ninguém fala.
        Dia 3: Não falta oportunidade, falta direção.
        Dia 4: Vender no lugar certo.
        Dia 5: Por que parece complicado (mas não é).
        
        SEMANA 2 (DESEJO):
        Dia 6: O erro de nem tentar.
        Dia 7: Não precisa ser grande pra começar.
        Dia 8: O jeito simples de entrar nesse mercado.
        Dia 9: Quem entende sai na frente.
        Dia 10: Amanhã vou mostrar o caminho direto.
        Mantenha o estilo: frases curtas e impacto psicológico."""
        st.session_state.memoria['aquecimento'] = nexus_ai(p, "Estrategista de Grupos Silenciosos", api_key)
    
    if 'aquecimento' in st.session_state.memoria:
        st.write(st.session_state.memoria['aquecimento'])
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("GERAR SEMANA DE VENDAS 👉"): st.session_state.etapa = 4; st.rerun()

elif st.session_state.etapa == 4:
    st.title("💰 4. SEMANA DE VENDAS (MÉTODO)")
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    
    if st.button("🚀 GERAR SEQUÊNCIA DE FECHAMENTO"):
        nicho = st.session_state.memoria['nicho']
        p = f"""Adapte as 5 mensagens de venda final para o nicho {nicho}:
        Dia 1: Abertura. 'Organizei tudo em um método simples e direto. O acesso está aqui.'
        Dia 2: 'Dúvida é falta de explicação simples'.
        Dia 3: 'Entrar no jogo certo'.
        Dia 4: 'Mudar o nível do jogo'.
        Dia 5: Fechamento Forte. 'Depois de hoje encerro. Quem deixou passar vai lembrar disso depois.'"""
        st.session_state.memoria['vendas'] = nexus_ai(p, "Copywriter de Fechamento", api_key)
        
    if 'vendas' in st.session_state.memoria:
        st.success(st.session_state.memoria['vendas'])
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("FINALIZAR LANÇAMENTO"):
        st.balloons()
        st.success(f"Funil de {st.session_state.memoria['nicho']} estruturado com sucesso!")

if st.session_state.etapa > 0:
    if st.button("⬅ VOLTAR"): st.session_state.etapa -= 1; st.rerun()

st.markdown(f'<div class="footer">NEXUS — FUNIL PSICOLÓGICO: {st.session_state.memoria.get("nicho", "").upper()}</div>', unsafe_allow_html=True)
