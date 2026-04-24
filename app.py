import streamlit as st
from groq import Groq
from datetime import timedelta
import re

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="NEXUS LAUNCHER", layout="wide")

# --- ESTILO CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700&family=Inter:wght@400;500&display=swap');

    [data-testid="stSidebar"] { display: none; }

    body, .stApp { font-family: 'Inter', sans-serif; }

    h1, h2, h3 { font-family: 'Rajdhani', sans-serif; letter-spacing: 1px; }

    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3.5em;
        background-color: #00BFFF !important;
        color: white !important;
        font-weight: bold;
        border: none;
        font-family: 'Rajdhani', sans-serif;
        letter-spacing: 1px;
        font-size: 1em;
        transition: background-color 0.2s ease;
    }
    .stButton>button:hover { background-color: #0099CC !important; }

    .caixa-texto {
        background-color: #F8FAFC;
        padding: 25px;
        border-radius: 12px;
        border-left: 6px solid #00BFFF;
        margin-bottom: 20px;
        white-space: pre-wrap;
        color: #1E293B;
        line-height: 1.6;
    }

    .chat-bubble {
        background-color: #F1F5F9;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #E2E8F0;
        margin-bottom: 10px;
    }

    .btn-perigo>button {
        background-color: #ef4444 !important;
        height: 2em !important;
    }

    .btn-secundario>button {
        background-color: #64748B !important;
        height: 2.5em !important;
        font-size: 0.85em !important;
    }

    .btn-verde>button {
        background-color: #22c55e !important;
        height: 2.5em !important;
        font-size: 0.85em !important;
    }

    .footer {
        text-align: center;
        padding: 60px;
        color: #94A3B8;
        font-size: 0.8em;
        opacity: 0.4;
        margin-top: 100px;
        font-style: italic;
    }

    .step-indicator {
        display: flex;
        gap: 8px;
        margin-bottom: 20px;
        flex-wrap: wrap;
    }

    .step-badge {
        background: #E2E8F0;
        color: #64748B;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 0.75em;
        font-weight: 600;
        font-family: 'Rajdhani', sans-serif;
        letter-spacing: 0.5px;
    }

    .step-badge.ativo {
        background: #00BFFF;
        color: white;
    }

    .preview-box {
        background: #EFF6FF;
        border: 1px solid #BFDBFE;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        color: #1E3A5F;
        line-height: 1.7;
    }

    .exemplo-btn>button {
        background-color: #F1F5F9 !important;
        color: #334155 !important;
        border: 1px solid #CBD5E1 !important;
        height: 2.2em !important;
        font-size: 0.8em !important;
        font-family: 'Inter', sans-serif !important;
        letter-spacing: 0 !important;
    }

    .checklist-item {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        padding: 12px 0;
        border-bottom: 1px solid #E2E8F0;
    }

    .checklist-num {
        background: #00BFFF;
        color: white;
        border-radius: 50%;
        width: 26px;
        height: 26px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 0.85em;
        flex-shrink: 0;
    }

    .meta-card {
        background: linear-gradient(135deg, #0EA5E9, #0284C7);
        color: white;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO DE ESTADO ---
defaults = {
    'etapa': "Login",
    'dados': {},
    'projetos': {},
    'chat_hist': [],
    'usuario': '',
    'api_key': '',
    'chat_input_key': 0,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# --- ETAPAS PARA INDICADOR DE PROGRESSO ---
ETAPAS = ["Formulario", "Gerar_Ebook", "Copy_Face", "Copy_LP", "Mensagens_Grupo", "Visualizacao"]
ETAPAS_LABELS = {
    "Formulario": "1. Formulário",
    "Gerar_Ebook": "2. E-book",
    "Copy_Face": "3. Anúncio",
    "Copy_LP": "4. Landing Page",
    "Mensagens_Grupo": "5. Mensagens",
    "Visualizacao": "6. Projeto Final",
}

# --- EXEMPLOS POR NICHO ---
EXEMPLOS = {
    "Emagrecimento": {
        "nicho": "emagrecimento",
        "publico": "mulheres de 30 a 50 anos que querem emagrecer",
        "nome_eb": "Barriga Zero em 30 Dias",
        "dor": "não consigo perder peso mesmo fazendo dieta e exercício",
        "atual": "A pessoa está acima do peso, frustrada com dietas que não funcionam e sem energia no dia a dia",
        "desejada": "Ter um corpo mais saudável, se sentir bonita, ter disposição e autoestima elevada",
        "promessa": "Emagrecer até 7kg em 30 dias com um método simples e sem passar fome",
        "diferencial": "Método baseado em refeições rápidas de até 15 minutos, sem academia",
    },
    "Criptomoedas": {
        "nicho": "criptomoedas",
        "publico": "iniciantes que querem investir em cripto mas têm medo de perder dinheiro",
        "nome_eb": "Cripto do Zero: Como Começar a Investir com Segurança",
        "dor": "medo de perder dinheiro por falta de conhecimento sobre o mercado cripto",
        "atual": "A pessoa ouve falar de cripto mas não entende nada, fica de fora e vê outros lucrando",
        "desejada": "Entender como funciona o mercado, fazer os primeiros investimentos com segurança e confiança",
        "promessa": "Aprender a investir em criptomoedas do zero, com segurança, mesmo sem experiência",
        "diferencial": "Linguagem simples, sem jargões técnicos, com passo a passo prático para iniciantes",
    },
    "Renda Extra": {
        "nicho": "renda extra",
        "publico": "pessoas que trabalham com carteira assinada e querem ganhar dinheiro extra online",
        "nome_eb": "Renda Extra Digital: Ganhe R$1.000 por Mês Trabalhando 1 Hora por Dia",
        "dor": "salário não cobre todas as despesas e não há tempo para um segundo emprego",
        "atual": "A pessoa está endividada ou no limite financeiro, sem tempo livre e sem saber por onde começar",
        "desejada": "Ter uma renda extra de pelo menos R$1.000 por mês trabalhando no celular nas horas vagas",
        "promessa": "Gerar R$1.000 extras por mês pelo celular em apenas 1 hora por dia",
        "diferencial": "Estratégias testadas que não exigem investimento inicial nem experiência prévia",
    },
    "Relacionamentos": {
        "nicho": "relacionamentos",
        "publico": "mulheres de 25 a 45 anos que querem reconquistar ou melhorar seu relacionamento",
        "nome_eb": "Amor de Volta: Como Reconquistar Quem Você Ama em 21 Dias",
        "dor": "terminou um relacionamento e não sabe como reconquistar ou se deve tentar",
        "atual": "A pessoa está sofrendo após um término, se sentindo perdida e sem esperança de reconciliação",
        "desejada": "Reconquistar a pessoa amada ou ter clareza para seguir em frente com autoestima elevada",
        "promessa": "Reconquistar o ex em 21 dias usando técnicas de psicologia comportamental",
        "diferencial": "Método com base em psicologia aplicada, sem joguinhos ou manipulação",
    },
}

# --- FUNÇÃO DE IA ---
def chamar_ia(prompt: str, system_prompt: str) -> str:
    try:
        client = Groq(api_key=st.session_state.api_key)
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile",
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Erro na API: {e}"

# --- LIMPAR HTML PARA CÓPIA ---
def limpar_html(texto: str) -> str:
    limpo = re.sub(r'<[^>]+>', '', texto)
    limpo = limpo.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    return limpo.strip()

# --- NORMALIZAR MARKDOWN PARA HTML ---
def normalizar_markdown(texto: str) -> str:
    linhas = texto.split('\n')
    resultado = []
    for linha in linhas:
        if linha.startswith('#### '):
            linha = f"<h4>{linha[5:]}</h4>"
        elif linha.startswith('### '):
            linha = f"<h3>{linha[4:]}</h3>"
        elif linha.startswith('## '):
            linha = f"<h2>{linha[3:]}</h2>"
        elif linha.startswith('# '):
            linha = f"<h2>{linha[2:]}</h2>"
        linha = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', linha)
        linha = re.sub(r'\*(.+?)\*', r'<em>\1</em>', linha)
        resultado.append(linha)
    return '\n'.join(resultado)

# --- COMPONENTE: BLOCO COM BOTÕES DE COPIAR E REGENERAR ---
def bloco_conteudo(chave: str, titulo: str, prompt_fn=None, system_fn=None):
    conteudo = st.session_state.dados.get(chave, '')
    if not conteudo:
        st.info(f"{titulo} ainda não foi gerado.")
        return

    conteudo_html = normalizar_markdown(conteudo)
    st.markdown(f"<div class='caixa-texto'>{conteudo_html}</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        texto_limpo = limpar_html(conteudo)
        st.download_button(
            label="📋 Copiar como .txt",
            data=texto_limpo,
            file_name=f"{chave}.txt",
            mime="text/plain",
            key=f"copy_{chave}",
            use_container_width=True,
        )
    with col2:
        if prompt_fn and system_fn:
            st.markdown('<div class="btn-secundario">', unsafe_allow_html=True)
            if st.button(f"🔄 Regenerar {titulo}", key=f"regen_{chave}", use_container_width=True):
                with st.spinner(f"Regenerando {titulo}..."):
                    st.session_state.dados[chave] = chamar_ia(prompt_fn(), system_fn())
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# --- INDICADOR DE PROGRESSO ---
def mostrar_progresso():
    etapa_atual = st.session_state.etapa
    badges = ""
    for chave, label in ETAPAS_LABELS.items():
        if chave == etapa_atual:
            badges += f'<span class="step-badge ativo">{label}</span>'
        else:
            badges += f'<span class="step-badge">{label}</span>'
    st.markdown(f'<div class="step-indicator">{badges}</div>', unsafe_allow_html=True)

# --- BARRA DE NAVEGAÇÃO ---
def barra_navegacao():
    mostrar_progresso()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ INICIAR NOVO PROJETO"):
            st.session_state.dados = {}
            st.session_state.etapa = "Formulario"
            st.rerun()
    with col2:
        with st.expander("📂 MEUS PROJETOS"):
            if not st.session_state.projetos:
                st.write("Nenhum projeto salvo.")
            for nome in list(st.session_state.projetos.keys()):
                c_abrir, c_deletar = st.columns([4, 1])
                if c_abrir.button(f"📄 {nome}", key=f"abrir_{nome}"):
                    st.session_state.dados = st.session_state.projetos[nome].copy()
                    st.session_state.etapa = "Visualizacao"
                    st.rerun()
                st.markdown('<div class="btn-perigo">', unsafe_allow_html=True)
                if c_deletar.button("🗑️", key=f"del_{nome}", help="Excluir projeto"):
                    del st.session_state.projetos[nome]
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

# --- PROMPTS (funções para regeneração) ---
def prompt_ebook():
    d = st.session_state.dados
    return (
        f"Gere 60 cartões educativos numerados para o e-book '{d['nome_eb']}'. "
        f"Público-alvo: {d['publico']}. Dor principal: {d['dor']}. "
        f"Diferencial: {d['diferencial']}. Cada cartão deve ter título e conteúdo útil."
    )

def system_ebook():
    return "Você é um especialista em conteúdo digital educativo. Seja objetivo e prático."

def prompt_fb():
    d = st.session_state.dados
    return (
        f"Crie 5 variações de copy curta para Facebook Ads. "
        f"Nicho: {d['nicho']}. Público: {d['publico']}. Dor: {d['dor']}. "
        f"Lançamento: {d['data_lancto'].strftime('%d/%m/%Y')}. "
        f"OBRIGATÓRIO para cada variação: "
        f"1. Identifique com título em negrito HTML usando a tag <strong> (ex: <strong>Variação 1: [Nome]</strong>). "
        f"2. Inclua sugestão detalhada de imagem/criativo visual. "
        f"3. Finalize com: ⬇️ Clique abaixo e descubra como. "
        f"4. Separe parágrafos com linha em branco."
    )

def system_fb():
    return (
        "Você é um copywriter especialista em anúncios diretos e curtos para Facebook Ads. "
        "Use sempre tags HTML <strong> para títulos em negrito, nunca use ** (asteriscos)."
    )

def prompt_lp():
    d = st.session_state.dados
    return (
        f"Crie 5 variações de copy completa para Landing Page. "
        f"Situação atual: {d['atual']}. Situação desejada: {d['desejada']}. "
        f"Promessa: {d['promessa']}. Diferencial: {d['diferencial']}. "
        f"Para cada variação, sugira imagens e elementos visuais. "
        f"Finalize cada variação com o botão de ação: [ ENTRAR NO GRUPO ]."
    )

def system_lp():
    return (
        "Você é um especialista em Landing Pages de alta conversão. "
        "Identifique cada variação com título em negrito usando a tag HTML <strong>. "
        "Nunca use ** (asteriscos) para negrito, use sempre a tag HTML <strong>."
    )

def prompt_msg():
    d = st.session_state.dados
    data = d['data_lancto'].strftime('%d/%m/%Y')
    data_d1 = (d['data_lancto'] - timedelta(days=1)).strftime('%d/%m/%Y')
    return (
        f"Crie 3 mensagens para um grupo de WhatsApp/Telegram de lançamento digital. "
        f"Use os dados abaixo para personalizar as mensagens de forma natural e fluida, "
        f"sem repetir textos longos e sem incoerências gramaticais.\n\n"
        f"- Nicho: {d['nicho']}\n"
        f"- Público-alvo: {d['publico']}\n"
        f"- Nome do e-book: {d['nome_eb']}\n"
        f"- Principal dor: {d['dor']}\n"
        f"- Promessa/resultado: {d['promessa']}\n"
        f"- Data de lançamento: {data}\n"
        f"- Data de aquecimento (1 dia antes): {data_d1}\n\n"
        f"Estruture EXATAMENTE assim:\n\n"
        f"**Descrição do grupo:**\n"
        f"Este grupo é silencioso. Você não será incomodado.\n"
        f"Aqui você receberá apenas conteúdos e avisos relacionados ao tema.\n\n"
        f"---\n\n"
        f"**📩 Mensagem 1 – Boas-vindas + Pré-lançamento**\n"
        f"[mensagem de boas-vindas calorosa, mencione o nicho, diga que vai liberar conteúdo no dia {data}]\n\n"
        f"---\n\n"
        f"**⏳ Mensagem 2 – 1 dia antes ({data_d1}) — aquecimento**\n"
        f"[mensagem de aquecimento, mencione a dor, crie expectativa para amanhã]\n\n"
        f"---\n\n"
        f"**🚀 Mensagem 3 – Lançamento ({data})**\n"
        f"[mensagem de lançamento, diga que o conteúdo foi liberado, mencione o resultado, "
        f"finalize com: 👉 [LINK DA MONETIZZE]\n"
        f"Disponível apenas até [coloque uma data concreta 3 dias após {data}] — após isso o preço sobe.]"
    )

def system_msg():
    return (
        "Você é um especialista em copywriting para lançamentos digitais no WhatsApp e Telegram. "
        "Escreva mensagens naturais, humanas e sem incoerências gramaticais. "
        "Nunca repita textos longos na íntegra. Use linguagem simples e direta."
    )

# ============================================================
# TELA: LOGIN
# ============================================================
if st.session_state.etapa == "Login":
    st.title("NEXUS LAUNCHER")
    st.subheader("ACESSO RESTRITO A ASSOCIADOS DO QUIZ MAIS PRÊMIOS")
    st.session_state.usuario = st.text_input("Nome")
    st.session_state.api_key = st.text_input("Chave Groq", type="password")

    if st.button("ENTRAR"):
        if not st.session_state.usuario.strip():
            st.error("Informe seu nome.")
        elif not st.session_state.api_key.strip():
            st.error("Informe sua chave de API.")
        else:
            st.session_state.etapa = "Formulario"
            st.rerun()

# ============================================================
# TELA: FORMULÁRIO
# ============================================================
elif st.session_state.etapa == "Formulario":
    barra_navegacao()
    st.title("PREENCHA O FORMULÁRIO")
    d = st.session_state.dados

    # --- MELHORIA 1: Exemplos clicáveis ---
    st.markdown("#### Começar com um exemplo pronto")
    st.caption("Escolha um nicho de exemplo e preencha tudo automaticamente — depois é só ajustar.")
    cols = st.columns(len(EXEMPLOS))
    for i, (nome_ex, vals) in enumerate(EXEMPLOS.items()):
        with cols[i]:
            st.markdown('<div class="exemplo-btn">', unsafe_allow_html=True)
            if st.button(f"📋 {nome_ex}", key=f"ex_{nome_ex}", use_container_width=True):
                for k, v in vals.items():
                    st.session_state.dados[k] = v
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # --- MELHORIA 2: IA preenche pelo nicho ---
    st.markdown("#### Ou deixe a IA preencher pelo nicho")
    nicho_rapido = st.text_input("Digite só o assunto do seu ebook:", placeholder="ex: meditação, finanças pessoais, culinária saudável")
    if st.button("✨ PREENCHER COM IA"):
        if nicho_rapido.strip():
            with st.spinner("IA preenchendo o formulário..."):
                resultado_ia = chamar_ia(
                    f"Preencha os campos abaixo para um ebook digital sobre '{nicho_rapido}'. "
                    f"Responda EXATAMENTE neste formato, sem explicações extras:\n"
                    f"NICHO: ...\nPUBLICO: ...\nNOME_EB: ...\nDOR: ...\nATUAL: ...\nDESEJADA: ...\nPROMESSA: ...\nDIFERENCIAL: ...",
                    "Você é especialista em marketing digital e lançamentos. Seja direto e prático."
                )
                linhas = resultado_ia.strip().split('\n')
                mapa = {}
                for linha in linhas:
                    if ':' in linha:
                        chave, _, valor = linha.partition(':')
                        mapa[chave.strip()] = valor.strip()
                if mapa:
                    st.session_state.dados['nicho']       = mapa.get('NICHO', '')
                    st.session_state.dados['publico']      = mapa.get('PUBLICO', '')
                    st.session_state.dados['nome_eb']      = mapa.get('NOME_EB', '')
                    st.session_state.dados['dor']          = mapa.get('DOR', '')
                    st.session_state.dados['atual']        = mapa.get('ATUAL', '')
                    st.session_state.dados['desejada']     = mapa.get('DESEJADA', '')
                    st.session_state.dados['promessa']     = mapa.get('PROMESSA', '')
                    st.session_state.dados['diferencial']  = mapa.get('DIFERENCIAL', '')
                    st.rerun()
        else:
            st.warning("Digite o assunto do ebook antes de continuar.")

    st.divider()

    # --- Campos do formulário ---
    st.markdown("#### Revise ou preencha manualmente")
    d['nicho']       = st.text_input("Nicho:", value=d.get('nicho', ''), help="ex: emagrecimento, renda extra")
    d['publico']     = st.text_input("Público-alvo:", value=d.get('publico', ''), help="ex: homens de 25 a 40")
    d['nome_eb']     = st.text_input("Nome do e-book:", value=d.get('nome_eb', ''))
    d['dor']         = st.text_input("Principal dor que resolve:", value=d.get('dor', ''))
    d['atual']       = st.text_area("Situação atual da pessoa:", value=d.get('atual', ''))
    d['desejada']    = st.text_area("Situação desejada:", value=d.get('desejada', ''))
    d['promessa']    = st.text_input("Promessa do e-book:", value=d.get('promessa', ''))
    d['diferencial'] = st.text_input("Diferencial:", value=d.get('diferencial', ''))
    d['preco']       = st.number_input("Preço do e-book (R$):", min_value=9, max_value=997, value=int(d.get('preco', 47)), step=1)
    from datetime import date
    data_sugerida = d.get('data_lancto', date.today() + timedelta(days=15))
    d['data_lancto'] = st.date_input(
        "Data de lançamento",
        value=data_sugerida,
        min_value=date.today(),
        help="💡 Sugerimos daqui a 15 dias: 1 semana para encher o grupo e 1 semana para aquecer."
    )
    st.caption("💡 Dica: Use os primeiros 7 dias para encher o grupo com tráfego e os próximos 7 para aquecer com as mensagens. Lance no 15º dia.")

    # --- MELHORIA 3: Calculadora de meta ---
    st.divider()
    st.markdown("#### Calculadora de faturamento")
    st.caption("Veja o potencial antes de avançar.")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        leads = st.number_input("Pessoas no grupo:", min_value=100, max_value=100000, value=1000, step=100)
    with col_b:
        conversao = st.slider("Taxa de conversão (%):", min_value=1, max_value=30, value=10)
    with col_c:
        preco_calc = d.get('preco', 47)
        st.metric("Preço definido", f"R${preco_calc}")

    vendas = int(leads * conversao / 100)
    faturamento = vendas * preco_calc
    custo_estimado = int(leads * 1.5)
    lucro = faturamento - custo_estimado

    col1, col2, col3 = st.columns(3)
    col1.metric("Vendas estimadas", f"{vendas}")
    col2.metric("Faturamento bruto", f"R${faturamento:,.0f}".replace(',', '.'))
    col3.metric("Lucro estimado", f"R${lucro:,.0f}".replace(',', '.'), delta="após tráfego ~R$1,50/lead")

    # --- MELHORIA 3: Preview antes de avançar ---
    campos_obrigatorios = ['nicho', 'publico', 'nome_eb', 'dor', 'atual', 'desejada', 'promessa', 'diferencial']
    tudo_preenchido = all(d.get(c, '').strip() for c in campos_obrigatorios)

    if tudo_preenchido:
        st.divider()
        st.markdown("#### Resumo do que será gerado")
        st.markdown(f"""
        <div class="preview-box">
        Vamos gerar um lançamento completo para você:<br><br>
        📚 <strong>E-book:</strong> {d.get('nome_eb')} — 60 cartões educativos sobre {d.get('nicho')}<br>
        🎯 <strong>Público:</strong> {d.get('publico')}<br>
        💬 <strong>5 anúncios</strong> focados na dor: <em>{d.get('dor')}</em><br>
        🌐 <strong>5 variações de Landing Page</strong> com CTA para o grupo<br>
        📩 <strong>3 mensagens</strong> de aquecimento e lançamento<br>
        🚀 <strong>Data de lançamento:</strong> {d['data_lancto'].strftime('%d/%m/%Y')}
        </div>
        """, unsafe_allow_html=True)

    if st.button("AVANÇAR →"):
        faltando = [c for c in campos_obrigatorios if not d.get(c, '').strip()]
        if faltando:
            st.warning("Preencha todos os campos antes de avançar.")
        else:
            st.session_state.etapa = "Gerar_Ebook"
            st.rerun()

# ============================================================
# TELA: GERAR E-BOOK
# ============================================================
elif st.session_state.etapa == "Gerar_Ebook":
    barra_navegacao()
    st.title("📚 GERAR E-BOOK PROFISSIONAL")

    if st.button("GERAR E-BOOK – 60 CARTÕES"):
        with st.spinner("Gerando e-book com IA..."):
            st.session_state.dados['ebook_cont'] = chamar_ia(prompt_ebook(), system_ebook())

    if 'ebook_cont' in st.session_state.dados:
        bloco_conteudo('ebook_cont', 'E-book', prompt_ebook, system_ebook)
        if st.button("AVANÇAR →"):
            st.session_state.etapa = "Copy_Face"
            st.rerun()

# ============================================================
# TELA: COPY FACEBOOK
# ============================================================
elif st.session_state.etapa == "Copy_Face":
    barra_navegacao()
    st.title("📱 COPY PARA O FACEBOOK")

    if st.button("GERAR 5 VARIAÇÕES"):
        with st.spinner("Gerando copies com IA..."):
            st.session_state.dados['fb_copy'] = chamar_ia(prompt_fb(), system_fb())

    if 'fb_copy' in st.session_state.dados:
        bloco_conteudo('fb_copy', 'Anúncios', prompt_fb, system_fb)
        if st.button("AVANÇAR →"):
            st.session_state.etapa = "Copy_LP"
            st.rerun()

# ============================================================
# TELA: COPY LANDING PAGE
# ============================================================
elif st.session_state.etapa == "Copy_LP":
    barra_navegacao()
    st.title("🌐 COPY PARA A LANDING PAGE")

    if st.button("GERAR 5 VARIAÇÕES LP"):
        with st.spinner("Gerando landing pages com IA..."):
            st.session_state.dados['lp_copy'] = chamar_ia(prompt_lp(), system_lp())

    if 'lp_copy' in st.session_state.dados:
        bloco_conteudo('lp_copy', 'Landing Page', prompt_lp, system_lp)
        if st.button("AVANÇAR →"):
            st.session_state.etapa = "Mensagens_Grupo"
            st.rerun()

# ============================================================
# TELA: MENSAGENS DO GRUPO
# ============================================================
elif st.session_state.etapa == "Mensagens_Grupo":
    barra_navegacao()
    st.title("📌 MENSAGENS PARA O GRUPO")

    if 'msg_grupo' not in st.session_state.dados:
        if st.button("✉️ GERAR MENSAGENS DO GRUPO"):
            with st.spinner("Gerando mensagens com IA..."):
                st.session_state.dados['msg_grupo'] = chamar_ia(prompt_msg(), system_msg())
                st.rerun()
    else:
        bloco_conteudo('msg_grupo', 'Mensagens', prompt_msg, system_msg)

    if 'msg_grupo' in st.session_state.dados:
        if st.button("💾 SALVAR PROJETO"):
            nome_projeto = st.session_state.dados.get('nome_eb', 'Sem nome')
            st.session_state.projetos[nome_projeto] = st.session_state.dados.copy()
            st.session_state.etapa = "Visualizacao"
            st.rerun()

# ============================================================
# TELA: VISUALIZAÇÃO FINAL
# ============================================================
elif st.session_state.etapa == "Visualizacao":
    barra_navegacao()
    nome_projeto = st.session_state.dados.get('nome_eb', 'Projeto')
    st.title(f"PROJETO: {nome_projeto}")

    # --- MELHORIA 5: Download completo ---
    d = st.session_state.dados
    texto_completo = f"""
NEXUS LAUNCHER — PROJETO COMPLETO
{'='*50}
E-BOOK: {d.get('nome_eb', '')}
NICHO: {d.get('nicho', '')}
PÚBLICO: {d.get('publico', '')}
DATA DE LANÇAMENTO: {d.get('data_lancto', '')}
{'='*50}

📚 E-BOOK
{'-'*40}
{limpar_html(d.get('ebook_cont', 'Não gerado.'))}

🎬 ANÚNCIOS (FACEBOOK)
{'-'*40}
{limpar_html(d.get('fb_copy', 'Não gerado.'))}

🌐 LANDING PAGE
{'-'*40}
{limpar_html(d.get('lp_copy', 'Não gerado.'))}

📌 MENSAGENS DO GRUPO
{'-'*40}
{limpar_html(d.get('msg_grupo', 'Não gerado.'))}
""".strip()

    st.markdown('<div class="btn-verde">', unsafe_allow_html=True)
    st.download_button(
        label="⬇️ BAIXAR PROJETO COMPLETO (.txt)",
        data=texto_completo,
        file_name=f"{nome_projeto.replace(' ', '_')}_lancamento.txt",
        mime="text/plain",
        use_container_width=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    with st.expander("📚 E-BOOK"):
        bloco_conteudo('ebook_cont', 'E-book', prompt_ebook, system_ebook)

    with st.expander("🎬 ANÚNCIO (Facebook)"):
        bloco_conteudo('fb_copy', 'Anúncios', prompt_fb, system_fb)

    with st.expander("🌐 LANDING PAGE"):
        bloco_conteudo('lp_copy', 'Landing Page', prompt_lp, system_lp)

    with st.expander("📌 MENSAGENS DO GRUPO"):
        bloco_conteudo('msg_grupo', 'Mensagens', prompt_msg, system_msg)

    # --- MELHORIA 6: Checklist de lançamento ---
    st.divider()
    with st.expander("✅ CHECKLIST DE LANÇAMENTO — O QUE FAZER AGORA"):
        data_lancto = d.get('data_lancto', '')
        checklist = [
            ("Hoje", "Criar o grupo no WhatsApp ou Telegram com o nome do nicho"),
            ("Hoje", "Cadastrar o e-book na Monetizze e pegar o link de venda"),
            ("Hoje", "Subir o arquivo do e-book na Monetizze (PDF ou link)"),
            ("Hoje", "Definir o preço e configurar o checkout"),
            ("Hoje", "Postar o anúncio no Facebook/Instagram apontando para a LP ou grupo"),
            ("Hoje", "Enviar a Mensagem 1 (boas-vindas) para quem entrar no grupo"),
            (f"Dia anterior ao lançamento", "Enviar a Mensagem 2 (aquecimento) para o grupo"),
            (f"Dia do lançamento ({data_lancto})", "Enviar a Mensagem 3 com o link da Monetizze"),
            (f"Dia do lançamento", "Monitorar as vendas na Monetizze e responder dúvidas"),
            ("Após lançamento", "Analisar: quantas pessoas no grupo vs. quantas compraram"),
            ("Após lançamento", "Guardar a base para o próximo lançamento — custo zero de tráfego!"),
        ]
        for i, (quando, acao) in enumerate(checklist, 1):
            st.markdown(f"""
            <div class="checklist-item">
                <div class="checklist-num">{i}</div>
                <div>
                    <div style="font-size:0.75em;color:#64748B;font-weight:600;text-transform:uppercase;letter-spacing:0.5px">{quando}</div>
                    <div style="font-size:0.95em;color:#1E293B">{acao}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # --- MELHORIA 8: Calculadora de meta na visualização ---
    st.divider()
    with st.expander("📊 CALCULADORA DE FATURAMENTO"):
        col_a, col_b = st.columns(2)
        with col_a:
            leads_v = st.number_input("Pessoas no grupo:", min_value=100, max_value=100000, value=1000, step=100, key="leads_vis")
            conv_v  = st.slider("Taxa de conversão (%):", 1, 30, 10, key="conv_vis")
        with col_b:
            preco_v = st.number_input("Preço (R$):", min_value=9, max_value=997, value=int(d.get('preco', 47)), key="preco_vis")
            custo_v = st.number_input("Custo de tráfego (R$):", min_value=0, max_value=50000, value=int(leads_v * 1.5), key="custo_vis")

        vendas_v = int(leads_v * conv_v / 100)
        fat_v    = vendas_v * preco_v
        lucro_v  = fat_v - custo_v

        c1, c2, c3 = st.columns(3)
        c1.metric("Vendas", f"{vendas_v}")
        c2.metric("Faturamento", f"R${fat_v:,.0f}".replace(',', '.'))
        c3.metric("Lucro", f"R${lucro_v:,.0f}".replace(',', '.'))

    # --- LAUNCERBOT (CHAT) ---
    st.divider()
    st.markdown("### 🤖 Launcerbot")
    st.info(
        f"**Olá, {st.session_state.usuario}! 👋** "
        "Eu sou o **Launcerbot**. Ajudo você a criar e lançar produtos digitais, mesmo do zero. "
        "Pode me perguntar qualquer coisa sobre seu lançamento 👇"
    )

    pergunta = st.text_input(
        "Sua pergunta:",
        key=f"chat_input_{st.session_state.chat_input_key}"
    )

    if st.button("ENVIAR"):
        if pergunta.strip():
            with st.spinner("Launcerbot pensando..."):
                contexto_projeto = (
                    f"Nicho: {st.session_state.dados.get('nicho')}. "
                    f"E-book: {st.session_state.dados.get('nome_eb')}. "
                    f"Público: {st.session_state.dados.get('publico')}."
                )
                system = (
                    f"Você é o Launcerbot, assistente especialista em lançamentos digitais. "
                    f"O usuário se chama {st.session_state.usuario}. "
                    f"Contexto do projeto atual: {contexto_projeto}"
                )
                try:
                    client = Groq(api_key=st.session_state.api_key)
                    messages = [{"role": "system", "content": system}]
                    for q_hist, r_hist in st.session_state.chat_hist:
                        messages.append({"role": "user", "content": q_hist})
                        messages.append({"role": "assistant", "content": r_hist})
                    messages.append({"role": "user", "content": pergunta})
                    response = client.chat.completions.create(
                        messages=messages,
                        model="llama-3.3-70b-versatile",
                    )
                    resp = response.choices[0].message.content
                except Exception as e:
                    resp = f"⚠️ Erro na API: {e}"
                st.session_state.chat_hist.append((pergunta, resp))
                st.session_state.chat_input_key += 1
                st.rerun()
        else:
            st.warning("Digite uma pergunta antes de enviar.")

    if st.session_state.chat_hist:
        st.markdown("---")
        for q, r in reversed(st.session_state.chat_hist):
            st.markdown(f"**Você:** {q}")
            st.markdown(f"<div class='chat-bubble'>{r}</div>", unsafe_allow_html=True)

# --- RODAPÉ ---
st.markdown("<div class='footer'>© 2026 Nexus Launcher – Lançamento digital inteligente</div>", unsafe_allow_html=True)
