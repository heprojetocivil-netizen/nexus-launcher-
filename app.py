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
defaults = {
    'etapa': "Login", 'dados': {}, 'projetos': {},
    'chat_hist': [], 'usuario': '', 'api_key': '', 'chat_input_key': 0,
}
for k, v in defaults.items():
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
    SECOES = ["BOAS_VINDAS","DIA_7","DIA_6","DIA_5","DIA_4","DIA_3","DIA_2","VESPERA","VENDA_MANHA","VENDA_NOITE"]
    LABELS = {
        "BOAS_VINDAS":  "💬 Boas-vindas ao grupo",
        "DIA_7":        "📅 D-7 — Abertura do programa",
        "DIA_6":        "🎯 D-6 — Enquete interativa",
        "DIA_5":        "🔥 D-5 — Dica prática",
        "DIA_4":        "📌 D-4 — Atividade rápida",
        "DIA_3":        "💡 D-3 — Conteúdo de valor",
        "DIA_2":        "📈 D-2 — Prova social",
        "VESPERA":      "⏳ D-1 — Véspera da venda",
        "VENDA_MANHA":  "🚀 Dia da venda — Manhã",
        "VENDA_NOITE":  "⏰ Dia da venda — Lembrete noturno",
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
        for s in secoes:
            st.markdown(f"<div class='msg-dia-header'>{s['label']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='msg-conteudo'>{normalizar_markdown(s['conteudo'])}</div>", unsafe_allow_html=True)
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
            st.session_state.dados = {}; st.session_state.etapa = "Formulario"; st.rerun()
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
        f"REGRAS: Sem exageros. Tom humano. Parece um convite, não um anúncio de produto."
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
    data_fmt = data_lancto.strftime('%d/%m/%Y') if data_lancto else 'em breve'
    data_d1 = (data_lancto - timedelta(days=1)).strftime('%d/%m/%Y') if data_lancto else ''
    preco = d.get('preco', 47)
    nome_eb = d.get('nome_eb', '')
    nicho = d.get('nicho', '')
    dor = d.get('dor', '')
    publico = d.get('publico', '')
    promessa = d.get('promessa', '')
    whatsapp_num = d.get('whatsapp_contato', 'SEU NÚMERO AQUI')
    bonus_resumo = d.get('bonus_resumo', '')
    bonus_lista = '\n'.join([f'🎁 Bônus {i+1} – {b.strip()}' for i, b in enumerate(bonus_resumo.split(',')) if b.strip()]) if bonus_resumo else '🎁 Bônus 1\n🎁 Bônus 2\n🎁 Bônus 3'

    return (
        f"Crie as mensagens completas do funil de WhatsApp/Telegram para um lançamento digital.\n\n"
        f"CONTEXTO:\n"
        f"- Nicho: {nicho}\n- Público: {publico}\n- Dor: {dor}\n"
        f"- Ebook: {nome_eb}\n- Promessa: {promessa}\n"
        f"- Preço: R${preco}\n- Data de lançamento: {data_fmt}\n"
        f"- WhatsApp direto: {whatsapp_num}\n"
        f"- Bônus: {bonus_resumo}\n\n"
        f"CONCEITO: O grupo é chamado de 'Programa gratuito de X dias para [objetivo]'. "
        f"A venda é a conclusão natural — o cliente não sente que foi vendido, sente que encontrou a resposta.\n\n"
        f"Gere EXATAMENTE neste formato (rótulos exatos seguidos de dois pontos):\n\n"

        f"BOAS_VINDAS:\n"
        f"[Mensagem automática ao entrar. Calorosa, curta, sem mencionar venda. "
        f"Diga que durante os próximos dias o grupo recebe conteúdo gratuito sobre {nicho}. "
        f"Máximo 5 linhas.]\n\n"

        f"DIA_7:\n"
        f"[Bom dia + abertura do programa. Apresente o tema dos próximos dias. "
        f"Diga que quem tiver dúvidas pode mandar mensagem no WhatsApp {whatsapp_num}. "
        f"Máximo 8 linhas. Zero menção a produto.]\n\n"

        f"DIA_6:\n"
        f"[Enquete interativa sobre a maior dificuldade do público com {nicho}. "
        f"Apresente 4 opções numeradas. "
        f"IMPORTANTE: NÃO prometa responder pessoalmente. Escreva apenas: "
        f"'Manda aqui no WhatsApp ({whatsapp_num}) qual é a sua — quero entender sua maior dificuldade.' "
        f"Tom curioso, sem compromisso de retorno individual. Máximo 8 linhas.]\n\n"

        f"DIA_5:\n"
        f"[Dica prática acionável sobre {nicho}. 1 ensinamento real que a pessoa pode aplicar hoje. "
        f"Máximo 8 linhas. Zero CTA de venda.]\n\n"

        f"DIA_4:\n"
        f"[Atividade rápida ou pergunta reflexiva ligada à dor '{dor}'. "
        f"Gera engajamento sem revelar que existe produto. Máximo 8 linhas.]\n\n"

        f"DIA_3:\n"
        f"[Conteúdo de valor aprofundando um ponto ligado à dor '{dor}'. "
        f"Ensina algo concreto. Máximo 8 linhas.]\n\n"

        f"DIA_2:\n"
        f"[Simule um relato curto de alguém que superou a dor '{dor}' e alcançou a promessa '{promessa}'. "
        f"Apresente como conquista real de alguém da 'turma passada'. Tom humano. Máximo 8 linhas.]\n\n"

        f"VESPERA:\n"
        f"[Mensagem da véspera da venda. "
        f"ESCREVA EXATAMENTE ASSIM — sem fugir desse roteiro:\n"
        f"1. Abertura: diga que nos últimos dias recebeu muitas mensagens no WhatsApp e ficou impressionado.\n"
        f"2. A dor específica: nomeie EXATAMENTE a dificuldade que as pessoas relataram — '{dor}'. "
        f"Use a dor textualmente, não de forma vaga. Exemplo: "
        f"'A maioria de vocês falou sobre [COLOQUE AQUI A DOR EXATA: {dor}]. "
        f"Li essas mensagens e percebi que é sempre o mesmo obstáculo aparecendo.'\n"
        f"3. Reação: diga que isso te fez parar e pensar em como ajudar de forma mais completa.\n"
        f"4. Antecipação: amanhã vai compartilhar algo preparado como resposta direta a isso — sem revelar o quê, sem revelar preço.\n"
        f"PROIBIDO: palavras genéricas como 'obstáculos', 'dificuldades', 'desafios' sem especificar qual. "
        f"PROIBIDO: mencionar equipe, produto, ebook ou qualquer coisa paga. "
        f"Tom: humano, de quem realmente leu e está respondendo. Máximo 10 linhas.]\n\n"

        f"VENDA_MANHA:\n"
        f"[Mensagem do dia da venda — manhã. "
        f"COMECE assim: faça referência direta à dúvida/dificuldade que as pessoas mandaram no WhatsApp — "
        f"'Lembra daquela mensagem que você me mandou sobre [dor]?' ou similar. "
        f"Diga que criou o '{nome_eb}' como resposta coletiva a tudo que recebeu. "
        f"Apresente como a resposta que eles estavam esperando, não como produto pronto de prateleira. "
        f"De R${preco*2} por apenas R${preco} hoje. "
        f"Liste os bônus:\n{bonus_lista}\n"
        f"👉 [LINK MONETIZZE]\n"
        f"⏰ Promoção válida até 23:59 de hoje. ✅ Garantia de 7 dias pela Monetizze. "
        f"Máximo 15 linhas.]\n\n"

        f"VENDA_NOITE:\n"
        f"[Lembrete noturno. Curto e direto. Lembra que encerra hoje à meia-noite. "
        f"Reforça a garantia de 7 dias. Máximo 5 linhas.]\n"
    )

def system_msg():
    return (
        "Você é um especialista em copywriting para lançamentos no WhatsApp e Telegram. "
        "A oferta deve parecer o próximo passo lógico da jornada que a pessoa viveu no grupo — não uma surpresa. "
        "A véspera deve soar como alguém que realmente leu as mensagens e está respondendo a elas. "
        "A mensagem de venda deve começar conectando com o que as pessoas compartilharam — não com energia de vendedor. "
        "Use linguagem simples, humana e direta. Respeite o formato solicitado com os rótulos exatos."
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
    d['promessa']    = st.text_input("Promessa do e-book:", value=d.get('promessa',''))
    d['diferencial'] = st.text_input("Diferencial:", value=d.get('diferencial',''))
    d['preco']       = st.number_input("Preço do e-book (R$):", min_value=9, max_value=997, value=int(d.get('preco',47)), step=1)

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
    <strong>Pode ser seu celular pessoal, um chip extra ou um número de atendimento.</strong>
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
    <strong>Funil completo de mensagens — 10 peças prontas para copiar e enviar:</strong><br><br>
    💬 Boas-vindas → 📅 D-7 Abertura → 🎯 D-6 Enquete → 🔥 D-5 Dica →
    📌 D-4 Atividade → 💡 D-3 Conteúdo → 📈 D-2 Prova social →
    ⏳ D-1 Véspera → 🚀 Manhã da venda → ⏰ Lembrete noturno
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
                ("Hoje","Salve e baixe todo o conteúdo gerado (.txt)"),
                ("Hoje","Crie o grupo: 'Programa [X] Dias para [Objetivo]'"),
                ("Hoje","Configure a descrição do grupo com o texto de boas-vindas gerado"),
                ("Hoje",f"Cadastre o e-book + 3 bônus na Monetizze — preço: R${d.get('preco',47)}"),
                ("Hoje","Suba o anúncio apontando para a landing page"),
                ("Hoje","Configure a landing page com o CTA apontando para o grupo"),
            ]},
            {"fase":"FASE 2 — SEMANA 1: Encher o grupo","cor":"#8B5CF6","items":[
                ("Dias 1 a 7","Anúncios rodando — objetivo: 500 a 1.000 pessoas no grupo"),
                ("Diariamente","Monitore custo por lead (meta: até R$2,00 por pessoa)"),
                ("Ao entrar","Mensagem de boas-vindas automática já está configurada"),
            ]},
            {"fase":"FASE 3 — SEMANA 2: Aquecimento","cor":"#059669","items":[
                (f"{d7} — D-7","Envie: Abertura do programa"),
                (f"{d6} — D-6","Envie: Enquete — peça para responder no WhatsApp"),
                (f"{d5} — D-5","Envie: Dica prática"),
                (f"{d4} — D-4","Envie: Atividade rápida"),
                (f"{d3} — D-3","Envie: Conteúdo de valor"),
                (f"{d2} — D-2","Envie: Prova social / relato"),
                (f"{dm1} — D-1","Envie: Véspera da venda"),
                (f"{dm1}","Confirme se o link da Monetizze está funcionando"),
            ]},
            {"fase":f"FASE 4 — {dlf}: Vender","cor":"#22C55E","items":[
                (f"{dlf} — manhã","Envie a mensagem de lançamento com o link da Monetizze"),
                (f"{dlf}","Fique online respondendo dúvidas no WhatsApp"),
                (f"{dlf} — noite","Envie lembrete: 'Encerra hoje à meia-noite'"),
            ]},
            {"fase":"FASE 5 — PÓS-LANÇAMENTO","cor":"#64748B","items":[
                ("Após","Anote: pessoas no grupo, compradores, taxa de conversão"),
                ("Após","ROI: faturamento ÷ custo de tráfego"),
                ("Próximos dias","Entregue o e-book e os bônus para quem comprou"),
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
    st.info(f"**Olá, {st.session_state.usuario}! 👋** Eu sou o **Launcerbot**. Pode me perguntar qualquer coisa sobre seu lançamento 👇")
    pergunta = st.text_input("Sua pergunta:", key=f"chat_input_{st.session_state.chat_input_key}")
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
    if st.session_state.chat_hist:
        st.markdown("---")
        for q, r in reversed(st.session_state.chat_hist):
            st.markdown(f"**Você:** {q}")
            st.markdown(f"<div class='chat-bubble'>{r}</div>", unsafe_allow_html=True)

# --- RODAPÉ ---
st.markdown("<div class='footer'>© 2026 Nexus Launcher – Lançamento digital inteligente</div>", unsafe_allow_html=True)
