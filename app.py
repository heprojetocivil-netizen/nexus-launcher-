import streamlit as st
from groq import Groq
from datetime import timedelta, date
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
        width: 100%; border-radius: 8px; height: 3.5em;
        background-color: #00BFFF !important; color: white !important;
        font-weight: bold; border: none; font-family: 'Rajdhani', sans-serif;
        letter-spacing: 1px; font-size: 1em; transition: background-color 0.2s ease;
    }
    .stButton>button:hover { background-color: #0099CC !important; }

    .caixa-texto {
        background-color: #F8FAFC; padding: 25px; border-radius: 12px;
        border-left: 6px solid #00BFFF; margin-bottom: 20px;
        white-space: pre-wrap; color: #1E293B; line-height: 1.6;
    }
    .chat-bubble {
        background-color: #F1F5F9; padding: 15px; border-radius: 10px;
        border: 1px solid #E2E8F0; margin-bottom: 10px;
    }
    .btn-perigo>button  { background-color: #ef4444 !important; height: 2em !important; }
    .btn-secundario>button { background-color: #64748B !important; height: 2.5em !important; font-size: 0.85em !important; }
    .btn-verde>button   { background-color: #22c55e !important; height: 2.5em !important; font-size: 0.85em !important; }
    .btn-roxo>button    { background-color: #7C3AED !important; height: 3.5em !important; }
    .btn-roxo>button:hover { background-color: #5B21B6 !important; }
    .btn-verde15>button { background-color: #059669 !important; height: 3.5em !important; }
    .btn-verde15>button:hover { background-color: #047857 !important; }

    .footer { text-align: center; padding: 60px; color: #94A3B8; font-size: 0.8em; opacity: 0.4; margin-top: 100px; font-style: italic; }

    .step-indicator { display: flex; gap: 8px; margin-bottom: 20px; flex-wrap: wrap; }
    .step-badge { background: #E2E8F0; color: #64748B; padding: 4px 12px; border-radius: 999px; font-size: 0.75em; font-weight: 600; font-family: 'Rajdhani', sans-serif; letter-spacing: 0.5px; }
    .step-badge.ativo { background: #00BFFF; color: white; }

    .preview-box { background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 10px; padding: 20px; margin: 15px 0; color: #1E3A5F; line-height: 1.7; }
    .exemplo-btn>button { background-color: #F1F5F9 !important; color: #334155 !important; border: 1px solid #CBD5E1 !important; height: 2.2em !important; font-size: 0.8em !important; font-family: 'Inter', sans-serif !important; letter-spacing: 0 !important; }

    .checklist-item { display: flex; align-items: flex-start; gap: 12px; padding: 12px 0; border-bottom: 1px solid #E2E8F0; }

    .bonus-card-header { background: linear-gradient(135deg, #0EA5E9, #0284C7); color: white; border-radius: 8px; padding: 12px 18px; margin-bottom: 16px; font-family: 'Rajdhani', sans-serif; font-size: 1.1em; font-weight: 700; letter-spacing: 0.5px; }
    .bonus-descricao { background: #EFF6FF; border-left: 4px solid #0EA5E9; border-radius: 6px; padding: 12px 16px; margin-bottom: 14px; color: #1E3A5F; font-size: 0.92em; line-height: 1.6; }
    .bonus-conteudo { background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 16px 20px; color: #334155; font-size: 0.88em; line-height: 1.7; white-space: pre-wrap; }

    /* MENSAGENS */
    .msg-dia-header { background: linear-gradient(135deg, #059669, #047857); color: white; border-radius: 8px; padding: 10px 16px; margin: 14px 0 8px 0; font-family: 'Rajdhani', sans-serif; font-size: 1.0em; font-weight: 700; letter-spacing: 0.5px; }
    .msg-conteudo { background: #FFFFFF; border: 1px solid #D1FAE5; border-radius: 8px; padding: 14px 18px; color: #1E293B; font-size: 0.88em; line-height: 1.75; white-space: pre-wrap; }
    .msg-alerta { background: #ECFDF5; border: 1px solid #6EE7B7; border-radius: 8px; padding: 12px 16px; color: #064E3B; font-size: 0.85em; margin-bottom: 16px; }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO DE ESTADO ---
# Initialize all state — projetos persists, never gets cleared
_one_time = {'etapa': "Login", 'dados': {}, 'projetos': {},
    'chat_hist': [], 'usuario': '', 'api_key': '', 'chat_input_key': 0}
for k, v in _one_time.items():
    if k not in st.session_state:
        st.session_state[k] = v

# --- ETAPAS ---
ETAPAS_LABELS = {
    "Formulario":      "1. Formulário",
    "Gerar_Ebook":     "2. E-book",
    "Gerar_Bonus":     "3. Bônus",
    "Copy_Face":       "4. Anúncio",
    "Copy_LP":         "5. Landing Page",
    "Mensagens_Grupo": "6. Mensagens",
    "Visualizacao":    "7. Projeto Final",
}

# --- EXEMPLOS ---
EXEMPLOS = {
    "Emagrecimento": {
        "nicho": "emagrecimento", "publico": "mulheres de 30 a 50 anos que querem emagrecer",
        "nome_eb": "Barriga Zero em 30 Dias", "dor": "não consigo perder peso mesmo fazendo dieta e exercício",
        "atual": "A pessoa está acima do peso, frustrada com dietas que não funcionam e sem energia no dia a dia",
        "desejada": "Ter um corpo mais saudável, se sentir bonita, ter disposição e autoestima elevada",
        "promessa": "Emagrecer até 7kg em 30 dias com um método simples e sem passar fome",
        "diferencial": "Método baseado em refeições rápidas de até 15 minutos, sem academia",
    },
    "Criptomoedas": {
        "nicho": "criptomoedas", "publico": "iniciantes que querem investir em cripto mas têm medo de perder dinheiro",
        "nome_eb": "Cripto do Zero: Como Começar a Investir com Segurança",
        "dor": "medo de perder dinheiro por falta de conhecimento sobre o mercado cripto",
        "atual": "A pessoa ouve falar de cripto mas não entende nada, fica de fora e vê outros lucrando",
        "desejada": "Entender como funciona o mercado, fazer os primeiros investimentos com segurança e confiança",
        "promessa": "Aprender a investir em criptomoedas do zero, com segurança, mesmo sem experiência",
        "diferencial": "Linguagem simples, sem jargões técnicos, com passo a passo prático para iniciantes",
    },
    "Renda Extra": {
        "nicho": "renda extra", "publico": "pessoas que trabalham com carteira assinada e querem ganhar dinheiro extra online",
        "nome_eb": "Renda Extra Digital: Ganhe R$1.000 por Mês Trabalhando 1 Hora por Dia",
        "dor": "salário não cobre todas as despesas e não há tempo para um segundo emprego",
        "atual": "A pessoa está endividada ou no limite financeiro, sem tempo livre e sem saber por onde começar",
        "desejada": "Ter uma renda extra de pelo menos R$1.000 por mês trabalhando no celular nas horas vagas",
        "promessa": "Gerar R$1.000 extras por mês pelo celular em apenas 1 hora por dia",
        "diferencial": "Estratégias testadas que não exigem investimento inicial nem experiência prévia",
    },
    "Relacionamentos": {
        "nicho": "relacionamentos", "publico": "mulheres de 25 a 45 anos que querem reconquistar ou melhorar seu relacionamento",
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
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Erro na API: {e}"

def limpar_html(texto: str) -> str:
    limpo = re.sub(r'<[^>]+>', '', texto)
    return limpo.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').strip()

def normalizar_markdown(texto: str) -> str:
    linhas = texto.split('\n')
    resultado = []
    for linha in linhas:
        if linha.startswith('#### '): linha = f"<h4>{linha[5:]}</h4>"
        elif linha.startswith('### '): linha = f"<h3>{linha[4:]}</h3>"
        elif linha.startswith('## '): linha = f"<h2>{linha[3:]}</h2>"
        elif linha.startswith('# '): linha = f"<h2>{linha[2:]}</h2>"
        linha = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', linha)
        linha = re.sub(r'\*(.+?)\*', r'<em>\1</em>', linha)
        resultado.append(linha)
    return '\n'.join(resultado)

# --- PARSERS ---
def _linha_e_marcador_bonus(linha):
    l = linha.strip().replace("🎁", "").strip()
    lu = l.upper()
    for num in ("1", "2", "3"):
        for pref in (f"BONUS {num}:", f"BONUS{num}:", f"BONUS {num} -", f"BONUS{num} -"):
            if lu.startswith(pref):
                return num, l[len(pref):].strip(" :-")
        for pref in (f"BÔNUS {num}:", f"BÔNUS{num}:", f"BÔNUS {num} -"):
            if lu.startswith(pref.upper()):
                return num, l[len(pref):].strip(" :-")
    return None, None

def parsear_bonus(texto: str) -> list:
    linhas = texto.split("\n")
    marcadores = []
    for idx, linha in enumerate(linhas):
        num, nome = _linha_e_marcador_bonus(linha)
        if num is not None: marcadores.append((idx, num, nome))
    if not marcadores: return [{"titulo": "🎁 Bônus", "descricao": "", "conteudo": texto.strip()}]
    bonus_list = []
    for i, (idx_ini, num, nome_bonus) in enumerate(marcadores):
        idx_fim = marcadores[i+1][0] if i+1 < len(marcadores) else len(linhas)
        bloco = linhas[idx_ini+1:idx_fim]
        descricao_partes, conteudo_partes, estado = [], [], "cabecalho"
        for linha in bloco:
            ls = linha.strip(); lu = ls.upper()
            if estado == "cabecalho" and not ls: continue
            if lu.startswith("DESCRI") and ":" in ls:
                estado = "descricao"
                parte = ls[ls.index(":")+1:].strip()
                if parte: descricao_partes.append(parte)
                continue
            if lu.startswith("CONTE") and ":" in ls:
                estado = "conteudo"
                parte = ls[ls.index(":")+1:].strip()
                if parte: conteudo_partes.append(parte)
                continue
            if estado == "descricao": descricao_partes.append(ls)
            elif estado == "conteudo": conteudo_partes.append(linha)
            else: conteudo_partes.append(linha)
        descricao = "\n".join(descricao_partes).strip()
        conteudo = "\n".join(conteudo_partes).strip()
        if not conteudo and not descricao: conteudo = "\n".join(bloco).strip()
        bonus_list.append({"titulo": "🎁 BÔNUS " + num + (": " + nome_bonus if nome_bonus else ""), "descricao": descricao, "conteudo": conteudo})
    return bonus_list

def parsear_mensagens(texto: str) -> list:
    """
    Divide as mensagens em blocos por seção.
    Detecta: BOAS_VINDAS, DIA_7, DIA_6, DIA_5, DIA_4, DIA_3, DIA_2, VESPERA, VENDA_MANHA, VENDA_NOITE
    """
    SECOES = ["DESCRICAO_GRUPO","BOAS_VINDAS","DIA_7","DIA_6","DIA_5","DIA_4","DIA_3","VESPERA","VENDA_MANHA","VENDA_NOITE"]
    LABELS = {
        "DESCRICAO_GRUPO": "📋 Descrição do grupo (bio)",
        "BOAS_VINDAS":  "💬 D-8 — Boas-vindas (mensagem automática)",
        "DIA_7":        "📅 D-9 — Abertura do programa",
        "DIA_6":        "🎯 D-10 — Enquete interativa",
        "DIA_5":        "🔥 D-11 — Dica prática",
        "DIA_4":        "📌 D-12 — Atividade interativa",
        "DIA_3":        "💡 D-13 — Conteúdo de valor / prova social",
        "VESPERA":      "⏳ D-14 — Véspera da venda",
        "VENDA_MANHA":  "🚀 Dia do lançamento — Manhã",
        "VENDA_NOITE":  "⏰ Dia do lançamento — Lembrete noturno (19h)",
    }
    linhas = texto.split('\n')
    secoes, atual_label, atual_linhas = [], None, []
    for linha in linhas:
        ls = linha.strip(); lu = ls.upper()
        achou = False
        for chave in SECOES:
            if lu.startswith(chave + ":") or lu.startswith(chave.replace("_"," ") + ":"):
                if atual_label:
                    secoes.append({"label": LABELS.get(atual_label, atual_label), "chave": atual_label, "conteudo": '\n'.join(atual_linhas).strip()})
                atual_label = chave
                resto = ls[ls.index(":")+1:].strip()
                atual_linhas = [resto] if resto else []
                achou = True
                break
        if not achou and atual_label:
            atual_linhas.append(linha)
    if atual_label:
        secoes.append({"label": LABELS.get(atual_label, atual_label), "chave": atual_label, "conteudo": '\n'.join(atual_linhas).strip()})
    if not secoes:
        secoes = [{"label": "Mensagens", "chave": "RAW", "conteudo": texto.strip()}]
    return secoes

# --- BLOCO DE CONTEÚDO ---
def bloco_conteudo(chave: str, titulo: str, prompt_fn=None, system_fn=None):
    conteudo = st.session_state.dados.get(chave, '')
    if not conteudo:
        st.info(f"{titulo} ainda não foi gerado.")
        return

    if chave == 'bonus_cont':
        for b in parsear_bonus(conteudo):
            st.markdown(f"<div class='bonus-card-header'>{b['titulo']}</div>", unsafe_allow_html=True)
            if b['descricao']:
                st.markdown(f"<div class='bonus-descricao'><strong>Descrição:</strong><br>{b['descricao']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='bonus-conteudo'>{normalizar_markdown(b['conteudo'])}</div>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

    elif chave == 'msg_grupo':
        secoes = parsear_mensagens(conteudo)
        for i, s in enumerate(secoes):
            st.markdown(f"<div class='msg-dia-header'>{s['label']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='msg-conteudo'>{normalizar_markdown(s['conteudo'])}</div>", unsafe_allow_html=True)
            texto_limpo = limpar_html(s['conteudo'])
            st.download_button(
                label="📋 Copiar esta mensagem",
                data=texto_limpo,
                file_name=f"{s['chave'].lower()}.txt",
                mime="text/plain",
                key=f"copy_msg_{i}_{chave}",
                use_container_width=False,
            )
            st.markdown("<br>", unsafe_allow_html=True)

    else:
        st.markdown(f"<div class='caixa-texto'>{normalizar_markdown(conteudo)}</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(label="📋 Copiar como .txt", data=limpar_html(conteudo), file_name=f"{chave}.txt", mime="text/plain", key=f"copy_{chave}", use_container_width=True)
    with col2:
        if prompt_fn and system_fn:
            st.markdown('<div class="btn-secundario">', unsafe_allow_html=True)
            if st.button(f"🔄 Regenerar {titulo}", key=f"regen_{chave}", use_container_width=True):
                with st.spinner(f"Regenerando {titulo}..."):
                    st.session_state.dados[chave] = chamar_ia(prompt_fn(), system_fn())
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# --- NAVEGAÇÃO ---
def mostrar_progresso():
    etapa_atual = st.session_state.etapa
    badges = ""
    for chave, label in ETAPAS_LABELS.items():
        cls = "ativo" if chave == etapa_atual else ""
        badges += f'<span class="step-badge {cls}">{label}</span>'
    st.markdown(f'<div class="step-indicator">{badges}</div>', unsafe_allow_html=True)

def barra_navegacao():
    mostrar_progresso()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ INICIAR NOVO PROJETO"):
            st.session_state.dados = {}; st.session_state.chat_hist = []; st.session_state.etapa = "Formulario"; st.rerun()
    with col2:
        with st.expander("📂 MEUS PROJETOS"):
            if not st.session_state.projetos: st.write("Nenhum projeto salvo.")
            for nome in list(st.session_state.projetos.keys()):
                c_abrir, c_deletar = st.columns([4,1])
                if c_abrir.button(f"📄 {nome}", key=f"abrir_{nome}"):
                    st.session_state.dados = st.session_state.projetos[nome].copy(); st.session_state.etapa = "Visualizacao"; st.rerun()
                st.markdown('<div class="btn-perigo">', unsafe_allow_html=True)
                if c_deletar.button("🗑️", key=f"del_{nome}", help="Excluir projeto"):
                    del st.session_state.projetos[nome]; st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

# =============================================================
# PROMPTS
# =============================================================

def prompt_ebook():
    d = st.session_state.dados
    return (f"Gere 60 cartões educativos numerados para o e-book '{d['nome_eb']}'. "
            f"Público-alvo: {d['publico']}. Dor principal: {d['dor']}. "
            f"Diferencial: {d['diferencial']}. Cada cartão deve ter título e conteúdo útil.")

def system_ebook():
    return "Você é um especialista em conteúdo digital educativo. Seja objetivo e prático."

def prompt_bonus():
    d = st.session_state.dados
    return (
        f"Crie 3 ebooks bônus complementares para quem comprou o ebook principal sobre {d.get('nicho')}. "
        f"Ebook principal: {d.get('nome_eb')}. Publico-alvo: {d.get('publico')}. "
        f"Dor principal: {d.get('dor')}. Promessa: {d.get('promessa')}. "
        f"Para cada ebook bonus, gere EXATAMENTE neste formato:\n\n"
        f"BONUS 1: [Nome]\nDescricao: [2 linhas]\nConteudo: [20 cartoes educativos numerados]\n\n"
        f"BONUS 2: [Nome]\nDescricao: [2 linhas]\nConteudo: [20 cartoes educativos numerados]\n\n"
        f"BONUS 3: [Nome]\nDescricao: [2 linhas]\nConteudo: [20 cartoes educativos numerados]"
    )

def system_bonus():
    return "Você é um especialista em conteúdo digital educativo. Crie ebooks bônus práticos que agreguem valor real ao produto principal."

def prompt_fb():
    d = st.session_state.dados
    return (
        f"Crie UM anúncio completo para Facebook Ads convidando pessoas para um grupo gratuito.\n\n"
        f"CONTEXTO:\n"
        f"- Nicho: {d['nicho']}\n- Público: {d['publico']}\n- Dor principal: {d['dor']}\n\n"
        f"CONCEITO OBRIGATÓRIO: O anúncio convida para um PROGRAMA GRATUITO DE 15 DIAS sobre {d['nicho']}. "
        f"Use um nome atrativo para o programa baseado no tema — ex: 'Programa 15 Dias para [objetivo]'. "
        f"NUNCA mencione ebook, produto pago, lançamento, preço ou qualquer venda. "
        f"O grupo é gratuito, com dicas e atividades práticas durante 15 dias. Só isso.\n\n"
        f"ESTRUTURA OBRIGATÓRIA:\n"
        f"1. Título chamativo em <strong>negrito HTML</strong> — centrado no programa gratuito\n"
        f"2. Texto principal (máx 5 linhas) — foca na dor do público e no que vão receber grátis\n"
        f"3. Lista rápida: ✅ Gratuito ✅ Grupo fechado ✅ Dicas diárias ✅ Vagas limitadas\n"
        f"4. Sugestão de criativo visual (1 linha)\n"
        f"5. CTA: ⬇️ Clique abaixo e garanta sua vaga\n\n"
        f"REGRAS: Deixe BEM EXPLÍCITO que o programa é 100% GRATUITO — use essa palavra em destaque. Sem exageros. Tom humano. Parece um convite, não um anúncio de produto."
    )

def system_fb():
    return ("Você é um copywriter especialista em Facebook Ads. "
            "O anúncio deve convidar para um grupo gratuito — sem mencionar produto pago, ebook ou lançamento. "
            "A oferta é o programa gratuito em si. Use tags HTML <strong> para negrito, nunca asteriscos.")

def prompt_lp():
    d = st.session_state.dados
    secao_autor = ''
    if d.get('autor_nome') or d.get('autor_experiencia'):
        secao_autor = (f"Autor: {d.get('autor_nome','')}, Experiência: {d.get('autor_experiencia','')}, "
                       f"Credenciais: {d.get('autor_credenciais','')}.  ")
    return (
        f"Crie UMA landing page completa para capturar leads para um grupo gratuito.\n\n"
        f"CONTEXTO:\n"
        f"- Nicho: {d.get('nicho')}\n- Público: {d.get('publico')}\n"
        f"- Dor principal: {d['dor']}\n- Situação atual: {d['atual']}\n"
        f"- Objetivo que a pessoa quer alcançar: {d['desejada']}\n"
        f"- {secao_autor}\n\n"
        f"CONCEITO OBRIGATÓRIO: A landing page convida para um PROGRAMA GRATUITO DE 15 DIAS sobre {d.get('nicho')}. "
        f"Use o mesmo nome de programa do anúncio — ex: 'Programa 15 Dias para [objetivo]'. "
        f"NUNCA mencione ebook, produto pago, lançamento, preço ou qualquer venda. "
        f"O grupo recebe dicas e atividades práticas durante 15 dias. Só isso.\n\n"
        f"ESTRUTURA OBRIGATÓRIA:\n"
        f"1. Headline principal — ex: 'Programa Gratuito de 15 Dias para [objetivo relacionado ao nicho]'\n"
        f"2. Subtítulo — o que a pessoa vai receber durante os 15 dias (conteúdo, dicas, atividades)\n"
        f"3. Seção de dor — 3 bullets descrevendo o que a pessoa sente/vive hoje\n"
        f"4. Solução — o que vai receber no grupo (conteúdo gratuito, sem mencionar produto)\n"
        f"5. Quem sou eu (autor, 2-3 linhas)\n"
        f"6. 4 benefícios com ✔ — todos sobre o conteúdo gratuito\n"
        f"7. Sugestão de elemento visual para a página\n"
        f"8. CTA: [ QUERO PARTICIPAR GRATUITAMENTE ]\n\n"
        f"REGRAS: Alinhada ao anúncio. Sem exageros. Tom direto e humano. Parece um convite, não uma venda."
    )

def system_lp():
    return ("Você é um especialista em Landing Pages de alta conversão para captura de leads. "
            "A LP promove um grupo gratuito — sem mencionar produto pago, ebook ou lançamento. "
            "Use tag HTML <strong> para negrito. Nunca asteriscos.")

def prompt_msg():
    d = st.session_state.dados
    data_lancto = d.get('data_lancto')
    preco = d.get('preco', 47)
    nome_eb = d.get('nome_eb', '')
    nicho = d.get('nicho', '')
    dor = d.get('dor', '')
    publico = d.get('publico', '')
    whatsapp_num = d.get('whatsapp_contato', 'SEU NÚMERO AQUI')
    link_venda = d.get('link_monetizze', '').strip() or '[LINK MONETIZZE]'
    bonus_resumo = d.get('bonus_resumo', '')
    bonus_lista = '\n'.join([f'🎁 Bônus {i+1} \u2013 {b.strip()}' for i, b in enumerate(bonus_resumo.split(',')) if b.strip()]) if bonus_resumo else '🎁 Bônus 1\n🎁 Bônus 2\n🎁 Bônus 3'

    return (
        f"Gere as mensagens do funil para o lançamento sobre {nicho}.\n"
        f"Ebook: {nome_eb}. Preço: R${preco}. WhatsApp: {whatsapp_num}. Nicho: {nicho}. Dor: {dor}.\n"
        f"Bônus:\n{bonus_lista}\n\n"
        f"REGRA ABSOLUTA: Textos entre === FIXO === e === FIM === devem ser copiados PALAVRA POR PALAVRA.\n"
        f"Apenas blocos com [IA] devem ser criados. Respeite os rótulos exatos.\n\n"

        f"DESCRICAO_GRUPO:\n"
        f"=== FIXO ===\n"
        f"Seja muito bem-vindo ao nosso grupo de [adapte: tema do programa sobre {nicho}]!\n"
        f"Esse não é apenas um grupo com conteúdos soltos.\n"
        f"Nos próximos dias, você vai passar por um processo simples, mas muito poderoso:\n"
        f"Primeiro, eu vou entender você.\n"
        f"Depois, vou te mostrar pequenos ajustes que já podem fazer diferença no seu dia a dia.\n"
        f"E no momento certo… eu vou te apresentar algo mais completo.\n"
        f"Tudo isso de forma leve, prática e aplicável.\n"
        f"Nosso objetivo aqui é um só: te ajudar a sair do mesmo lugar.\n"
        f"⚠️ Para manter a melhor experiência, o grupo permanecerá silencioso.\n"
        f"Assim, você recebe apenas o que realmente importa.\n"
        f"Fica atento…\n"
        f"Porque, se você acompanhar até o final, pode enxergar {nicho} de uma forma completamente diferente.\n"
        f"=== FIM ===\n\n"

        f"BOAS_VINDAS:\n"
        f"=== FIXO ===\n"
        f"Seja muito bem-vindo ao nosso grupo de [adapte: tema do programa sobre {nicho}]!\n"
        f"Se você está aqui… provavelmente já tentou melhorar em {nicho} — e não conseguiu manter.\n"
        f"E não é por falta de esforço.\n"
        f"Nos próximos dias, você vai entender exatamente o porquê.\n"
        f"Aqui, você não vai receber conteúdo aleatório.\n"
        f"Você vai receber algo simples… mas que pode destravar algo que você vem tentando há muito tempo.\n"
        f"⚠️ O grupo permanecerá silencioso\n"
        f"Pra você receber só o que realmente importa.\n"
        f"Fica atento… porque o que vem pode te surpreender.\n"
        f"=== FIM ===\n\n"

        f"DIA_7:\n"
        f"=== FIXO ===\n"
        f"Bom dia!\n"
        f"Nos próximos dias, vamos compartilhar conteúdos valiosos sobre {nicho}.\n"
        f"Teremos dicas práticas, curiosidades e insights para te ajudar a evoluir de verdade.\n"
        f"Se tiver alguma dúvida, você pode enviar uma mensagem para o nosso WhatsApp: ({whatsapp_num})\n"
        f"=== FIM ===\n\n"

        f"DIA_6:\n"
        f"=== FIXO (adapte só as 4 opções ao nicho {nicho} e dor: {dor}) ===\n"
        f"Isso aqui é importante.\n"
        f"Se você quer realmente sair desse programa com resultado, eu preciso entender você:\n"
        f"[IA: crie a pergunta da enquete e 4 opções A) B) C) D) adaptadas ao nicho {nicho} e dor {dor}]\n"
        f"Me manda no WhatsApp: ({whatsapp_num})\n"
        f"Vou ler todas — isso vai direcionar o que vou te mostrar nos próximos dias.\n"
        f"=== FIM ===\n\n"

        f"DIA_5:\n"
        f"[IA] Dica do dia sobre {nicho}. 1 ensinamento acionável agora. "
        f"Compacto, parágrafos curtos, máximo 5 linhas. Zero CTA de venda.\n\n"

        f"DIA_4:\n"
        f"[IA] Atividade rápida ligada à dor: {dor}. "
        f"Peça para responder no WhatsApp {whatsapp_num}. "
        f"Compacto, parágrafos curtos, máximo 5 linhas.\n\n"

        f"DIA_3:\n"
        f"[IA] Relato curto de alguém da turma passada que superou: {dor}. "
        f"Nome fictício, situação antes e resultado depois. "
        f"Tom humano, compacto, máximo 5 linhas.\n\n"

        f"VESPERA:\n"
        f"=== FIXO ===\n"
        f"Eu preciso ser sincero com você.\n"
        f"Depois de tudo que vocês me enviaram no meu WhatsApp…\n"
        f"Eu percebi algo que eu não esperava.\n"
        f"Existe um padrão.\n"
        f"E não é pequeno.\n"
        f"Mais de 80% das pessoas aqui estão presas exatamente nos mesmos pontos…\n"
        f"Mesmo tentando caminhos diferentes.\n"
        f"E isso me fez chegar a uma conclusão:\n"
        f"O problema não está no esforço.\n"
        f"Está no caminho que foi mostrado até hoje.\n"
        f"Foi por isso que eu decidi fazer algo diferente.\n"
        f"Algo único… pensado pra resolver isso de forma direta.\n"
        f"Mas não é só sobre entender.\n"
        f"É sobre saber exatamente o que fazer — sem dúvidas, sem excesso, sem confusão.\n"
        f"Eu organizei tudo de um jeito que praticamente qualquer pessoa aqui consiga aplicar.\n"
        f"Amanhã, eu vou te mostrar.\n"
        f"Mas já te adianto:\n"
        f"Se você ignorar… provavelmente vai continuar no mesmo lugar.\n"
        f"Fica atento.\n"
        f"=== FIM ===\n\n"

        f"VENDA_MANHA:\n"
        f"=== FIXO (adapte nome do ebook e bônus) ===\n"
        f"Hoje é o grande dia.\n"
        f"Se você continuar fazendo do jeito que sempre fez…\n"
        f"Nada muda.\n"
        f"Foi por isso que eu reuni tudo que realmente funciona em um único material:\n"
        f"📘 {nome_eb}\n"
        f"Um conteúdo direto ao ponto, simples e aplicável.\n"
        f"E pra garantir que você tenha resultado:\n"
        f"{bonus_lista}\n"
        f"Tudo isso por apenas R$ {preco}.\n"
        f"Mas atenção:\n"
        f"Esse valor estará disponível só hoje\n"
        f"👉 {link_venda}\n"
        f"⏰ Válido até 23:59\n"
        f"✅ Garantia de 7 dias\n"
        f"Agora a decisão está nas suas mãos.\n"
        f"=== FIM ===\n\n"

        f"VENDA_NOITE:\n"
        f"=== FIXO (adapte nicho) ===\n"
        f"Boa noite! 👋\n"
        f"Passando aqui de forma mais tranquila pra te lembrar:\n"
        f"Hoje eu te apresentei um material que reúne exatamente o que você precisa pra evoluir em {nicho}.\n"
        f"📘 Conteúdo direto, sem complicação\n"
        f"🎁 Com 3 bônus práticos\n"
        f"Se você ficou na dúvida, tudo bem.\n"
        f"Mas a verdade é:\n"
        f"Quem aplica o método certo, evolui muito mais rápido.\n"
        f"Se fizer sentido pra você, ainda dá tempo:\n"
        f"👉 {link_venda}\n"
        f"⏰ Até 23:59\n"
        f"✅ Garantia de 7 dias\n"
        f"Dá uma olhada com calma… e decide.\n"
        f"=== FIM ===\n"
    )
def system_msg():
    return (
        "Você é um especialista em copywriting para lançamentos no WhatsApp e Telegram. "
        "Os textos fixos devem ser reproduzidos EXATAMENTE como fornecidos — sem alterar uma vírgula. "
        "Apenas os blocos com instruções entre colchetes devem ser gerados pela IA. "
        "Respeite o formato com os rótulos exatos. Tom humano e direto em tudo que gerar."
    )

# =============================================================
# TELAS
# =============================================================

# ── LOGIN ─────────────────────────────────────────────────────
if st.session_state.etapa == "Login":
    st.title("NEXUS LAUNCHER")
    st.subheader("ACESSO RESTRITO A ASSOCIADOS DO QUIZ MAIS PRÊMIOS")
    st.markdown('<p style="margin-top:-8px;margin-bottom:20px;font-size:0.95em;">🔗 <a href="https://www.quizmaispremios.com.br" target="_blank" style="color:#00BFFF;text-decoration:none;font-weight:600;">www.quizmaispremios.com.br</a></p>', unsafe_allow_html=True)
    st.session_state.usuario = st.text_input("Nome")
    st.session_state.api_key = st.text_input("Chave Groq", type="password")
    if st.button("ENTRAR"):
        if not st.session_state.usuario.strip(): st.error("Informe seu nome.")
        elif not st.session_state.api_key.strip(): st.error("Informe sua chave de API.")
        else: st.session_state.etapa = "Formulario"; st.rerun()

# ── FORMULÁRIO ───────────────────────────────────────────────
elif st.session_state.etapa == "Formulario":
    barra_navegacao()
    st.title("PREENCHA O FORMULÁRIO")
    d = st.session_state.dados

    st.markdown("#### Começar com um exemplo pronto")
    st.caption("Escolha um nicho de exemplo e preencha tudo automaticamente.")
    cols = st.columns(len(EXEMPLOS))
    for i, (nome_ex, vals) in enumerate(EXEMPLOS.items()):
        with cols[i]:
            st.markdown('<div class="exemplo-btn">', unsafe_allow_html=True)
            if st.button(f"📋 {nome_ex}", key=f"ex_{nome_ex}", use_container_width=True):
                for k, v in vals.items(): st.session_state.dados[k] = v
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    st.markdown("#### Ou deixe a IA preencher pelo nicho")
    nicho_rapido = st.text_input("Digite só o assunto do seu ebook:", placeholder="ex: meditação, finanças pessoais, culinária saudável")
    if st.button("✨ PREENCHER COM IA"):
        if nicho_rapido.strip():
            with st.spinner("IA preenchendo o formulário..."):
                resultado_ia = chamar_ia(
                    f"Preencha os campos para um ebook digital sobre '{nicho_rapido}'. "
                    f"Responda EXATAMENTE neste formato:\nNICHO: ...\nPUBLICO: ...\nNOME_EB: ...\nDOR: ...\nATUAL: ...\nDESEJADA: ...\nPROMESSA: ...\nDIFERENCIAL: ...",
                    "Você é especialista em marketing digital e lançamentos. Seja direto e prático."
                )
                mapa = {}
                for linha in resultado_ia.strip().split('\n'):
                    if ':' in linha:
                        chave, _, valor = linha.partition(':')
                        mapa[chave.strip()] = valor.strip()
                if mapa:
                    st.session_state.dados.update({'nicho': mapa.get('NICHO',''), 'publico': mapa.get('PUBLICO',''),
                        'nome_eb': mapa.get('NOME_EB',''), 'dor': mapa.get('DOR',''), 'atual': mapa.get('ATUAL',''),
                        'desejada': mapa.get('DESEJADA',''), 'promessa': mapa.get('PROMESSA',''), 'diferencial': mapa.get('DIFERENCIAL','')})
                    st.rerun()
        else: st.warning("Digite o assunto do ebook antes de continuar.")

    st.divider()
    st.markdown("#### Revise ou preencha manualmente")
    d['nicho']       = st.text_input("Nicho:", value=d.get('nicho',''), help="ex: emagrecimento, renda extra")
    d['publico']     = st.text_input("Público-alvo:", value=d.get('publico',''))
    d['nome_eb']     = st.text_input("Nome do e-book:", value=d.get('nome_eb',''))
    d['dor']         = st.text_input("Principal dor que resolve:", value=d.get('dor',''))
    d['atual']       = st.text_area("Situação atual da pessoa:", value=d.get('atual',''))
    d['desejada']    = st.text_area("Situação desejada:", value=d.get('desejada',''))
    d['promessa']    = st.text_input("Transformação do programa:", value=d.get('promessa',''), help="Qual mudança real o público vai viver durante os 15 dias? (usado no anúncio e na LP)")
    d['diferencial'] = st.text_input("Diferencial:", value=d.get('diferencial',''))
    d['preco']       = st.number_input("Preço do e-book (R$):", min_value=9, max_value=997, value=int(d.get('preco',47)), step=1)

    st.divider()
    st.markdown("#### Link de venda (Monetizze)")
    st.caption("Cole o link aqui e ele entrará automaticamente nas mensagens de lançamento — sem precisar editar depois.")
    d['link_monetizze'] = st.text_input("Link da Monetizze:", value=d.get('link_monetizze',''), placeholder="ex: https://go.monetizze.com.br/...")

    st.divider()
    st.markdown("#### Suas credenciais como autor")
    st.caption("Aparecem na Landing Page e nas Mensagens do grupo.")
    d['autor_nome']        = st.text_input("Seu nome:", value=d.get('autor_nome',''), placeholder="ex: João Silva")
    d['autor_experiencia'] = st.text_area("Sua experiência com o tema:", value=d.get('autor_experiencia',''), placeholder="ex: Invisto em criptomoedas há 4 anos.")
    d['autor_credenciais'] = st.text_area("Resultados ou conquistas:", value=d.get('autor_credenciais',''), placeholder="ex: Já ajudei mais de 200 pessoas.")

    st.divider()
    st.markdown("#### WhatsApp para receber respostas da enquete")
    st.markdown("""<div style="background:#FEF9C3;border:1px solid #FDE047;border-radius:8px;padding:12px 16px;margin-bottom:12px;color:#713F12;font-size:0.88em;line-height:1.6;">
    ⚠️ <strong>ATENÇÃO: use um número DIFERENTE do grupo.</strong><br>
    O grupo ficará fechado para mensagens — os membros não conseguem responder lá dentro.<br>
    Por isso, as respostas da enquete e dúvidas devem ir para um número pessoal ou comercial separado.<br>
    <strong>Pode ser seu celular pessoal, um chip extra ou um número de atendimento.</strong><br><br>
    💡 <strong>Configure uma resposta automática nesse número:</strong><br>
    <em style="background:#FFFDE7;padding:2px 6px;border-radius:4px;">"Recebi sua mensagem. Eu e minha equipe já estamos analisando 🙏"</em>
    </div>""", unsafe_allow_html=True)
    d['whatsapp_contato'] = st.text_input("Número para receber respostas (diferente do grupo):", value=d.get('whatsapp_contato',''), placeholder="ex: (11) 99999-9999")

    data_sugerida = d.get('data_lancto', date.today() + timedelta(days=15))
    d['data_lancto'] = st.date_input("Data de lançamento", value=data_sugerida, min_value=date.today(),
        help="💡 Sugerimos 15 dias: 1 semana para encher o grupo e 1 semana para aquecer.")
    st.caption("💡 Dica: Use os primeiros 7 dias para encher o grupo e os próximos 7 para aquecer. Lance no 15º dia.")

    st.divider()
    st.markdown("#### Calculadora de faturamento")
    col_a, col_b, col_c = st.columns(3)
    with col_a: leads = st.number_input("Pessoas no grupo:", min_value=100, max_value=100000, value=1000, step=100)
    with col_b: conversao = st.slider("Taxa de conversão (%):", min_value=1, max_value=30, value=10)
    with col_c: st.metric("Preço definido", f"R${d.get('preco',47)}")
    vendas = int(leads * conversao / 100)
    faturamento = vendas * d.get('preco', 47)
    lucro = faturamento - int(leads * 1.5)
    col1, col2, col3 = st.columns(3)
    col1.metric("Vendas estimadas", f"{vendas}")
    col2.metric("Faturamento bruto", f"R${faturamento:,.0f}".replace(',','.'))
    col3.metric("Lucro estimado", f"R${lucro:,.0f}".replace(',','.'), delta="após tráfego ~R$1,50/lead")

    campos_obrigatorios = ['nicho','publico','nome_eb','dor','atual','desejada','promessa','diferencial']
    tudo_preenchido = all(d.get(c,'').strip() for c in campos_obrigatorios)

    if tudo_preenchido:
        st.divider()
        st.markdown("#### Resumo do que será gerado")
        st.markdown(f"""<div class="preview-box">
        📚 <strong>E-book:</strong> {d.get('nome_eb')} — 60 cartões educativos<br>
        🎁 <strong>3 E-books Bônus</strong> complementares<br>
        📣 <strong>1 Anúncio</strong> alinhado com a landing page<br>
        🌐 <strong>1 Landing Page</strong> alinhada com o anúncio<br>
        💬 <strong>Funil completo de Mensagens</strong> — boas-vindas + aquecimento + véspera + venda<br>
        🚀 <strong>Lançamento:</strong> {d['data_lancto'].strftime('%d/%m/%Y')}
        </div>""", unsafe_allow_html=True)

    if st.button("AVANÇAR →"):
        faltando = [c for c in campos_obrigatorios if not d.get(c,'').strip()]
        if faltando: st.warning("Preencha todos os campos antes de avançar.")
        else: st.session_state.etapa = "Gerar_Ebook"; st.rerun()

# ── E-BOOK ───────────────────────────────────────────────────
elif st.session_state.etapa == "Gerar_Ebook":
    barra_navegacao()
    st.title("📚 GERAR E-BOOK PROFISSIONAL")
    if st.button("GERAR E-BOOK – 60 CARTÕES"):
        with st.spinner("Gerando e-book com IA..."):
            st.session_state.dados['ebook_cont'] = chamar_ia(prompt_ebook(), system_ebook())
    if 'ebook_cont' in st.session_state.dados:
        bloco_conteudo('ebook_cont', 'E-book', prompt_ebook, system_ebook)
        if st.button("AVANÇAR →"): st.session_state.etapa = "Gerar_Bonus"; st.rerun()

# ── BÔNUS ────────────────────────────────────────────────────
elif st.session_state.etapa == "Gerar_Bonus":
    barra_navegacao()
    st.title("🎁 GERAR 3 E-BOOKS BÔNUS")
    st.caption("Os bônus serão complementares ao ebook principal e incluídos automaticamente na Mensagem de Lançamento.")
    if st.button("GERAR 3 EBOOKS BÔNUS"):
        with st.spinner("Gerando ebooks bônus com IA..."):
            st.session_state.dados['bonus_cont'] = chamar_ia(prompt_bonus(), system_bonus())
            nomes = []
            for linha in st.session_state.dados['bonus_cont'].split('\n'):
                num, nome_b = _linha_e_marcador_bonus(linha)
                if num is not None and nome_b: nomes.append(nome_b)
            if nomes: st.session_state.dados['bonus_resumo'] = ', '.join(nomes)
            st.rerun()
    if 'bonus_cont' in st.session_state.dados:
        bloco_conteudo('bonus_cont', 'Bônus', prompt_bonus, system_bonus)
        if st.button("AVANÇAR →"): st.session_state.etapa = "Copy_Face"; st.rerun()

# ── ANÚNCIO ───────────────────────────────────────────────────
elif st.session_state.etapa == "Copy_Face":
    barra_navegacao()
    st.title("📣 ANÚNCIO")
    st.caption("Um anúncio completo e alinhado com a landing page — mesma promessa, mesmo tom, mesma linguagem.")
    if st.button("GERAR ANÚNCIO"):
        with st.spinner("Gerando anúncio com IA..."):
            st.session_state.dados['fb_copy'] = chamar_ia(prompt_fb(), system_fb())
    if 'fb_copy' in st.session_state.dados:
        bloco_conteudo('fb_copy', 'Anúncio', prompt_fb, system_fb)
        if st.button("AVANÇAR →"): st.session_state.etapa = "Copy_LP"; st.rerun()

# ── LANDING PAGE ──────────────────────────────────────────────
elif st.session_state.etapa == "Copy_LP":
    barra_navegacao()
    st.title("🌐 LANDING PAGE")
    st.caption("Uma landing page completa — alinhada com o anúncio gerado. Mesma promessa, mesma jornada.")
    if st.button("GERAR LANDING PAGE"):
        with st.spinner("Gerando landing page com IA..."):
            st.session_state.dados['lp_copy'] = chamar_ia(prompt_lp(), system_lp())
    if 'lp_copy' in st.session_state.dados:
        bloco_conteudo('lp_copy', 'Landing Page', prompt_lp, system_lp)
        if st.button("AVANÇAR →"): st.session_state.etapa = "Mensagens_Grupo"; st.rerun()

# ── MENSAGENS DO GRUPO ────────────────────────────────────────
elif st.session_state.etapa == "Mensagens_Grupo":
    barra_navegacao()
    st.title("💬 MENSAGENS DO GRUPO")

    st.markdown("""<div class="preview-box">
    <strong>Funil completo — 10 peças prontas para copiar e enviar:</strong><br><br>
    📋 Descrição (bio) → 💬 D-8 Boas-vindas → 📅 D-9 Abertura →
    🎯 D-10 Enquete → 🔥 D-11 Dica → 📌 D-12 Atividade →
    💡 D-13 Prova social → ⏳ D-14 Véspera → 🚀 Manhã da venda → ⏰ Noite (19h)
    </div>""", unsafe_allow_html=True)

    st.markdown("""<div style="background:#FEF3C7;border:1px solid #FCD34D;border-radius:8px;padding:12px 16px;margin-bottom:8px;color:#78350F;font-size:0.87em;line-height:1.6;">
    ⚠️ <strong>Atenção antes de usar:</strong><br>
    Os textos em destaque são <strong>fixos</strong> — copiados palavra por palavra do modelo aprovado.<br>
    Apenas <strong>D-10 (enquete), D-11 (dica), D-12 (atividade) e D-13 (prova social)</strong> são gerados pela IA.<br>
    <strong>Revise esses 4 blocos antes de enviar.</strong>
    </div>""", unsafe_allow_html=True)

    if not st.session_state.dados.get('whatsapp_contato'):
        st.warning("⚠️ Você não preencheu o WhatsApp de contato no formulário. As mensagens usam esse número para receber respostas da enquete.")

    st.markdown('<div class="btn-verde15">', unsafe_allow_html=True)
    gerar_msg = st.button("💬 GERAR FUNIL COMPLETO DE MENSAGENS")
    st.markdown('</div>', unsafe_allow_html=True)

    if gerar_msg:
        with st.spinner("Gerando o funil completo de mensagens..."):
            st.session_state.dados['msg_grupo'] = chamar_ia(prompt_msg(), system_msg())
            st.rerun()

    if 'msg_grupo' in st.session_state.dados:
        st.divider()
        st.markdown("#### Suas mensagens prontas para enviar")
        st.caption("Cada bloco corresponde a um dia. Copie e envie no momento certo.")
        bloco_conteudo('msg_grupo', 'Mensagens', prompt_msg, system_msg)
        st.divider()
        if st.button("💾 SALVAR PROJETO"):
            nome_projeto = st.session_state.dados.get('nome_eb', 'Sem nome')
            st.session_state.projetos[nome_projeto] = st.session_state.dados.copy()
            st.session_state.etapa = "Visualizacao"; st.rerun()

# ── VISUALIZAÇÃO FINAL ────────────────────────────────────────
elif st.session_state.etapa == "Visualizacao":
    barra_navegacao()
    nome_projeto = st.session_state.dados.get('nome_eb', 'Projeto')
    st.title(f"PROJETO: {nome_projeto}")
    d = st.session_state.dados

    texto_completo = f"""NEXUS LAUNCHER — PROJETO COMPLETO
{'='*50}
E-BOOK: {d.get('nome_eb','')}
NICHO: {d.get('nicho','')}
PÚBLICO: {d.get('publico','')}
DATA DE LANÇAMENTO: {d.get('data_lancto','')}
PREÇO: R${d.get('preco',47)}
{'='*50}

📚 E-BOOK PRINCIPAL
{'-'*40}
{limpar_html(d.get('ebook_cont','Não gerado.'))}

🎁 E-BOOKS BÔNUS
{'-'*40}
{limpar_html(d.get('bonus_cont','Não gerado.'))}

📣 ANÚNCIO
{'-'*40}
{limpar_html(d.get('fb_copy','Não gerado.'))}

🌐 LANDING PAGE
{'-'*40}
{limpar_html(d.get('lp_copy','Não gerado.'))}

💬 MENSAGENS DO GRUPO (FUNIL COMPLETO)
{'-'*40}
{limpar_html(d.get('msg_grupo','Não gerado.'))}""".strip()

    st.markdown('<div class="btn-verde">', unsafe_allow_html=True)
    st.download_button(label="⬇️ BAIXAR PROJETO COMPLETO (.txt)", data=texto_completo,
        file_name=f"{nome_projeto.replace(' ','_')}_lancamento.txt", mime="text/plain", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    with st.expander("📚 E-BOOK"):
        bloco_conteudo('ebook_cont','E-book',prompt_ebook,system_ebook)
    with st.expander("🎁 E-BOOKS BÔNUS"):
        bloco_conteudo('bonus_cont','Bônus',prompt_bonus,system_bonus)
    with st.expander("📣 ANÚNCIO"):
        bloco_conteudo('fb_copy','Anúncio',prompt_fb,system_fb)
    with st.expander("🌐 LANDING PAGE"):
        bloco_conteudo('lp_copy','Landing Page',prompt_lp,system_lp)
    with st.expander("💬 MENSAGENS DO GRUPO — FUNIL COMPLETO"):
        st.caption("Boas-vindas → D-7 a D-1 → Venda manhã → Lembrete noturno")
        bloco_conteudo('msg_grupo','Mensagens',prompt_msg,system_msg)

    # ── DICA MESTRE ──────────────────────────────────────────
    st.divider()
    with st.expander("🧠 DICA MESTRE — O QUE FAZER DEPOIS DO LANÇAMENTO"):
        st.markdown("""<div style="background:#F0FDF4;border:2px solid #22C55E;border-radius:12px;padding:22px 26px;color:#14532D;line-height:1.7;font-size:0.92em;">
        <strong style="font-size:1.05em;">Não apague esse grupo. E evite reabrir para conversas.</strong><br><br>
        Aqui dentro, você construiu algo extremamente valioso: atenção e interesse de pessoas reais.<br>
        Esse grupo é um ativo.<br>
        Se bem utilizado, ele pode gerar novos resultados sem que você precise investir mais nenhum centavo em tráfego.<br><br>
        <strong>Mas existe um ponto importante: evite excesso.</strong><br>
        O ideal é realizar novos lançamentos com equilíbrio — aproximadamente 1 vez por mês.<br>
        Assim, você mantém o interesse das pessoas, sem gerar desgaste ou perda de atenção.<br><br>
        Use esse grupo com estratégia… e ele pode continuar gerando resultados por muito tempo.
        </div>""", unsafe_allow_html=True)

        # ── CHECKLIST ─────────────────────────────────────────────
    st.divider()
    with st.expander("✅ CHECKLIST DE LANÇAMENTO — O QUE FAZER AGORA"):
        data_lancto = d.get('data_lancto', date.today())
        dlf  = data_lancto.strftime('%d/%m/%Y') if hasattr(data_lancto,'strftime') else str(data_lancto)
        dm1  = (data_lancto - timedelta(days=1)).strftime('%d/%m/%Y') if hasattr(data_lancto,'strftime') else ''
        d7   = (data_lancto - timedelta(days=7)).strftime('%d/%m/%Y') if hasattr(data_lancto,'strftime') else ''
        d6   = (data_lancto - timedelta(days=6)).strftime('%d/%m/%Y') if hasattr(data_lancto,'strftime') else ''
        d5   = (data_lancto - timedelta(days=5)).strftime('%d/%m/%Y') if hasattr(data_lancto,'strftime') else ''
        d4   = (data_lancto - timedelta(days=4)).strftime('%d/%m/%Y') if hasattr(data_lancto,'strftime') else ''
        d3   = (data_lancto - timedelta(days=3)).strftime('%d/%m/%Y') if hasattr(data_lancto,'strftime') else ''
        d2   = (data_lancto - timedelta(days=2)).strftime('%d/%m/%Y') if hasattr(data_lancto,'strftime') else ''

        fases = [
            {"fase":"FASE 1 — HOJE: Preparação","cor":"#0EA5E9","items":[
                ("Hoje","Baixe o projeto completo (.txt)"),
                ("Hoje","Cadastre o e-book + 3 bônus na Monetizze — configure o checkout"),
                (f"Hoje",f"Preço: R${d.get('preco',47)} — salve o link de venda"),
                ("Hoje","Crie o grupo: 'Programa [X] Dias para [Objetivo]'"),
                ("Hoje","Cole a DESCRIÇÃO DO GRUPO no campo de informações do WhatsApp/Telegram"),
                ("Hoje","Configure a mensagem de BOAS-VINDAS automática ao entrar"),
                ("Hoje","Suba o ANÚNCIO apontando para a LANDING PAGE"),
                ("Hoje","Configure a LANDING PAGE com CTA apontando para o grupo"),
                ("Hoje","Configure RESPOSTA AUTOMÁTICA no WhatsApp de contato: 'Recebi sua mensagem. Eu e minha equipe já estamos analisando 🙏'"),
            ]},
            {"fase":"FASE 2 — SEMANA 1: Encher o grupo","cor":"#8B5CF6","items":[
                ("Dias 1 a 8","Anúncios rodando — objetivo: 500 a 1.000 pessoas no grupo"),
                ("Diariamente","Monitore custo por lead — meta: até R$2,00 por pessoa"),
                ("Automático","Mensagem de boas-vindas já configurada — enviada a cada novo membro"),
            ]},
            {"fase":"FASE 3 — SEMANA 2: Aquecimento (D-7 a D-1)","cor":"#059669","items":[
                (f"{d7} — D-7","Envie: Abertura do programa"),
                (f"{d6} — D-6","Envie: Enquete — peça para responder no WhatsApp de contato"),
                (f"{d5} — D-5","Envie: Dica prática"),
                (f"{d4} — D-4","Envie: Atividade rápida"),
                (f"{d3} — D-3","Envie: Relato de resultado (prova social)"),
                (f"{dm1} — D-1","Envie: Véspera da venda"),
                (f"{dm1}","Confirme se o link da Monetizze está funcionando"),
            ]},
            {"fase":f"FASE 4 — {dlf}: Dia da venda","cor":"#22C55E","items":[
                (f"{dlf} — manhã","Envie a mensagem de lançamento com o link da Monetizze"),
                (f"{dlf}","Fique disponível no WhatsApp de contato para responder dúvidas"),
                (f"{dlf} — 19h","Envie o lembrete noturno"),
            ]},
            {"fase":"FASE 5 — PÓS-LANÇAMENTO","cor":"#64748B","items":[
                ("Após","Anote: pessoas no grupo, compradores, taxa de conversão"),
                ("Após","ROI: faturamento ÷ custo de tráfego"),
                ("Após","Entregue o e-book e os bônus para quem comprou"),
                ("Próximo mês","Use o mesmo grupo para o próximo lançamento — sem custo de tráfego"),
            ]},
        ]
        for fase in fases:
            st.markdown(f'<div style="margin:18px 0 8px 0;padding:8px 14px;background:{fase["cor"]};border-radius:8px;color:white;font-weight:600;font-size:0.85em;letter-spacing:0.5px">{fase["fase"]}</div>', unsafe_allow_html=True)
            for quando, acao in fase['items']:
                st.markdown(f'<div class="checklist-item"><div style="width:10px;height:10px;border-radius:50%;background:{fase["cor"]};margin-top:5px;flex-shrink:0"></div><div><div style="font-size:0.72em;color:#64748B;font-weight:600;text-transform:uppercase;letter-spacing:0.5px">{quando}</div><div style="font-size:0.92em;color:#1E293B">{acao}</div></div></div>', unsafe_allow_html=True)

    # ── CALCULADORA ───────────────────────────────────────────
    st.divider()
    with st.expander("📊 CALCULADORA DE FATURAMENTO"):
        col_a, col_b = st.columns(2)
        with col_a:
            leads_v = st.number_input("Pessoas no grupo:", min_value=100, max_value=100000, value=1000, step=100, key="leads_vis")
            conv_v  = st.slider("Taxa de conversão (%):", 1, 30, 10, key="conv_vis")
        with col_b:
            preco_v = st.number_input("Preço (R$):", min_value=9, max_value=997, value=int(d.get('preco',47)), key="preco_vis")
            custo_v = st.number_input("Custo de tráfego (R$):", min_value=0, max_value=50000, value=int(leads_v*1.5), key="custo_vis")
        vendas_v = int(leads_v * conv_v / 100)
        fat_v = vendas_v * preco_v
        lucro_v = fat_v - custo_v
        c1, c2, c3 = st.columns(3)
        c1.metric("Vendas", f"{vendas_v}")
        c2.metric("Faturamento", f"R${fat_v:,.0f}".replace(',','.'))
        c3.metric("Lucro", f"R${lucro_v:,.0f}".replace(',','.'))

    # ── LAUNCERBOT ────────────────────────────────────────────
    st.divider()
    st.markdown("### 🤖 Launcerbot")
    st.caption(f"Olá, {st.session_state.usuario}! Pode me perguntar qualquer coisa sobre seu lançamento.")

    # Show history first (oldest to newest)
    if st.session_state.chat_hist:
        for q, r in st.session_state.chat_hist:
            st.markdown(f"**Você:** {q}")
            st.markdown(f"<div class='chat-bubble'>{r}</div>", unsafe_allow_html=True)
        st.markdown("")

    # Input always at bottom
    pergunta = st.text_input("Sua pergunta:", key=f"chat_input_{st.session_state.chat_input_key}", label_visibility="collapsed", placeholder="Digite sua pergunta aqui...")
    if st.button("ENVIAR"):
        if pergunta.strip():
            with st.spinner("Launcerbot pensando..."):
                system = (f"Você é o Launcerbot, assistente especialista em lançamentos digitais. "
                          f"Usuário: {st.session_state.usuario}. "
                          f"Projeto: nicho={d.get('nicho')}, ebook={d.get('nome_eb')}, público={d.get('publico')}.")
                try:
                    client = Groq(api_key=st.session_state.api_key)
                    messages = [{"role": "system", "content": system}]
                    for q_hist, r_hist in st.session_state.chat_hist:
                        messages.append({"role": "user", "content": q_hist})
                        messages.append({"role": "assistant", "content": r_hist})
                    messages.append({"role": "user", "content": pergunta})
                    response = client.chat.completions.create(messages=messages, model="llama-3.3-70b-versatile")
                    resp = response.choices[0].message.content
                except Exception as e:
                    resp = f"⚠️ Erro na API: {e}"
                st.session_state.chat_hist.append((pergunta, resp))
                st.session_state.chat_input_key += 1
                st.rerun()
        else: st.warning("Digite uma pergunta antes de enviar.")

# --- RODAPÉ ---
st.markdown("<div class='footer'>© 2026 Nexus Launcher – Lançamento digital inteligente</div>", unsafe_allow_html=True)
