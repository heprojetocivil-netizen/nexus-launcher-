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
    .btn-fio>button     { background-color: #D97706 !important; height: 3.5em !important; }
    .btn-fio>button:hover { background-color: #B45309 !important; }
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

    .aquecimento-dia-header { background: linear-gradient(135deg, #7C3AED, #5B21B6); color: white; border-radius: 8px; padding: 12px 18px; margin-bottom: 12px; font-family: 'Rajdhani', sans-serif; font-size: 1.05em; font-weight: 700; letter-spacing: 0.5px; }
    .aquecimento-conteudo { background: #FFFFFF; border: 1px solid #EDE9FE; border-radius: 8px; padding: 16px 20px; color: #334155; font-size: 0.88em; line-height: 1.7; white-space: pre-wrap; }
    .aquecimento-gancho { background: #EDE9FE; border-left: 4px solid #7C3AED; border-radius: 0 6px 6px 0; padding: 10px 16px; margin-top: 12px; color: #4C1D95; font-size: 0.85em; font-style: italic; }

    /* FIO CONDUTOR */
    .fio-card { background: #FFFBEB; border: 2px solid #F59E0B; border-radius: 14px; padding: 24px 28px; margin-bottom: 20px; }
    .fio-secao { background: #FFFFFF; border-left: 4px solid #F59E0B; border-radius: 0 8px 8px 0; padding: 14px 18px; margin-bottom: 14px; color: #1E293B; font-size: 0.9em; line-height: 1.7; }
    .fio-label { font-family: 'Rajdhani', sans-serif; font-size: 0.75em; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: #92400E; margin-bottom: 6px; }
    .fio-alerta { background: #FEF3C7; border: 1px solid #FCD34D; border-radius: 8px; padding: 12px 16px; color: #78350F; font-size: 0.85em; margin-bottom: 16px; }

    /* PROGRAMA 15 DIAS */
    .p15-header { background: linear-gradient(135deg, #059669, #047857); color: white; border-radius: 10px; padding: 16px 22px; margin-bottom: 16px; font-family: 'Rajdhani', sans-serif; font-size: 1.15em; font-weight: 700; letter-spacing: 0.5px; }
    .p15-dia-header { background: linear-gradient(135deg, #10B981, #059669); color: white; border-radius: 8px; padding: 10px 16px; margin: 14px 0 8px 0; font-family: 'Rajdhani', sans-serif; font-size: 0.95em; font-weight: 700; letter-spacing: 0.5px; }
    .p15-bloco { background: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 10px; padding: 18px 22px; margin-bottom: 18px; }
    .p15-conteudo { background: #FFFFFF; border: 1px solid #D1FAE5; border-radius: 8px; padding: 14px 18px; color: #1E293B; font-size: 0.88em; line-height: 1.75; white-space: pre-wrap; }
    .p15-alerta { background: #ECFDF5; border: 1px solid #6EE7B7; border-radius: 8px; padding: 12px 16px; color: #064E3B; font-size: 0.85em; margin-bottom: 16px; }
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
    "Formulario":        "1. Formulário",
    "Fio_Condutor":      "2. Fio Condutor",
    "Gerar_Ebook":       "3. E-book",
    "Gerar_Bonus":       "4. Bônus",
    "Gerar_Aquecimento": "5. Aquecimento",
    "Prog15Dias":        "6. Prog. 15 Dias",
    "Copy_Face":         "7. Anúncio",
    "Copy_LP":           "8. Landing Page",
    "Mensagens_Grupo":   "9. Mensagens",
    "Visualizacao":      "10. Projeto Final",
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

def fio() -> str:
    return st.session_state.dados.get('fio_condutor', '')

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
def parsear_fio(texto: str) -> list:
    secoes_chave = ["PROMESSA_CALIBRADA","TOM_E_VOZ","PONTO_A","PONTO_B","MECANISMO","ANCORA_DA_OFERTA","FRASE_DO_ANUNCIO","HEADLINE_LP"]
    labels_legiveis = {
        "PROMESSA_CALIBRADA": "🎯 Promessa calibrada",
        "TOM_E_VOZ":          "🗣️ Tom e voz do autor",
        "PONTO_A":            "😔 Ponto A — situação atual",
        "PONTO_B":            "✨ Ponto B — situação desejada",
        "MECANISMO":          "⚙️ Mecanismo (como o ebook resolve)",
        "ANCORA_DA_OFERTA":   "🔗 Âncora da oferta",
        "FRASE_DO_ANUNCIO":   "📣 Frase-chave do anúncio",
        "HEADLINE_LP":        "🌐 Headline da Landing Page",
    }
    linhas = texto.split('\n')
    secoes, atual_label, atual_linhas = [], None, []
    for linha in linhas:
        ls = linha.strip()
        achou = False
        for chave in secoes_chave:
            if ls.upper().startswith(chave + ":"):
                if atual_label:
                    secoes.append({"label": labels_legiveis.get(atual_label, atual_label), "chave": atual_label, "conteudo": '\n'.join(atual_linhas).strip()})
                atual_label = chave
                atual_linhas = [ls[len(chave)+1:].strip()]
                achou = True
                break
        if not achou and atual_label:
            atual_linhas.append(ls)
    if atual_label:
        secoes.append({"label": labels_legiveis.get(atual_label, atual_label), "chave": atual_label, "conteudo": '\n'.join(atual_linhas).strip()})
    if not secoes:
        secoes = [{"label": "Fio Condutor", "chave": "RAW", "conteudo": texto.strip()}]
    return secoes

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

def parsear_aquecimento(texto: str) -> list:
    linhas = texto.split("\n"); marcadores = []
    for idx, linha in enumerate(linhas):
        ls = linha.strip(); lu = ls.upper()
        for num in ("1","2","3","4","5"):
            for pref in (f"DIA {num}:", f"DIA {num} -", f"DIA{num}:", f"📅 DIA {num}", f"📅DIA {num}"):
                if lu.startswith(pref.upper()):
                    marcadores.append((idx, num, ls[len(pref):].strip(" :-")))
                    break
    if not marcadores: return [{"dia": "Dia 1", "titulo": "Aquecimento", "conteudo": texto.strip(), "gancho": ""}]
    dias_list = []
    for i, (idx_ini, num, titulo_dia) in enumerate(marcadores):
        idx_fim = marcadores[i+1][0] if i+1 < len(marcadores) else len(linhas)
        bloco = linhas[idx_ini+1:idx_fim]
        conteudo_partes, gancho_partes, estado = [], [], "conteudo"
        for linha in bloco:
            ls = linha.strip(); lu = ls.upper()
            if not ls and estado == "conteudo" and not conteudo_partes: continue
            if lu.startswith("GANCHO") and ":" in ls:
                estado = "gancho"
                parte = ls[ls.index(":")+1:].strip()
                if parte: gancho_partes.append(parte)
                continue
            if estado == "conteudo": conteudo_partes.append(linha)
            elif estado == "gancho": gancho_partes.append(ls)
        dias_list.append({"dia": f"Dia {num}", "titulo": titulo_dia, "conteudo": "\n".join(conteudo_partes).strip(), "gancho": " ".join(gancho_partes).strip()})
    return dias_list

def parsear_prog15(texto: str) -> list:
    """
    Divide o Programa 15 Dias em blocos por seção.
    Detecta cabeçalhos como: ANUNCIO:, LP:, BOAS_VINDAS:, DIA_X:, VENDA_MANHA:, VENDA_NOITE:
    """
    SECOES = ["ANUNCIO","LP","BOAS_VINDAS","DIA_7","DIA_6","DIA_5","DIA_4","DIA_3","DIA_2","VESPERA","VENDA_MANHA","VENDA_TARDE"]
    LABELS = {
        "ANUNCIO":      "📣 Anúncio",
        "LP":           "🌐 Página de Captura (LP)",
        "BOAS_VINDAS":  "💬 Mensagem de Boas-vindas",
        "DIA_7":        "📅 Dia 7 — Abertura do programa",
        "DIA_6":        "🎯 Dia 6 — Atividade interativa",
        "DIA_5":        "🔥 Dia 5 — Dica prática",
        "DIA_4":        "📌 Dia 4 — Atividade rápida",
        "DIA_3":        "💡 Dia 3 — Conteúdo de valor",
        "DIA_2":        "📈 Dia 2 — Prova social / depoimento",
        "VESPERA":      "⏳ Véspera da venda",
        "VENDA_MANHA":  "🚀 Dia da venda — Manhã",
        "VENDA_TARDE":  "⏰ Dia da venda — Lembrete noturno",
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
        secoes = [{"label": "Programa 15 Dias", "chave": "RAW", "conteudo": texto.strip()}]
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

    elif chave == 'aquecimento_cont':
        emojis = ["🔥","💡","🎯","⚡","🚀"]
        for i, d in enumerate(parsear_aquecimento(conteudo)):
            st.markdown(f"<div class='aquecimento-dia-header'>{emojis[i%len(emojis)]} {d['dia']}{' — '+d['titulo'] if d['titulo'] else ''}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='aquecimento-conteudo'>{normalizar_markdown(d['conteudo'])}</div>", unsafe_allow_html=True)
            if d['gancho']:
                st.markdown(f"<div class='aquecimento-gancho'>🔗 <strong>Gancho para amanhã:</strong> {d['gancho']}</div>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

    elif chave == 'fio_condutor':
        for s in parsear_fio(conteudo):
            st.markdown(f"<div class='fio-label'>{s['label']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='fio-secao'>{normalizar_markdown(s['conteudo'])}</div>", unsafe_allow_html=True)

    elif chave == 'prog15_cont':
        secoes = parsear_prog15(conteudo)
        for s in secoes:
            st.markdown(f"<div class='p15-dia-header'>{s['label']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='p15-conteudo'>{normalizar_markdown(s['conteudo'])}</div>", unsafe_allow_html=True)
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

def prompt_fio_condutor():
    d = st.session_state.dados
    return (
        f"Você vai criar o FIO CONDUTOR de um lançamento digital. "
        f"Esse documento é a espinha dorsal de toda a comunicação — "
        f"anúncio, landing page, aquecimento e mensagem de lançamento vão usar ele como base. "
        f"Seja preciso, realista e coerente com o que um ebook pode entregar.\n\n"
        f"DADOS DO PRODUTO:\n"
        f"- Nicho: {d.get('nicho')}\n- Público-alvo: {d.get('publico')}\n"
        f"- Nome do ebook: {d.get('nome_eb')}\n- Dor principal: {d.get('dor')}\n"
        f"- Situação atual: {d.get('atual')}\n- Situação desejada: {d.get('desejada')}\n"
        f"- Promessa bruta: {d.get('promessa')}\n- Diferencial: {d.get('diferencial')}\n"
        f"- Preço: R${d.get('preco',47)}\n- Autor: {d.get('autor_nome','não informado')}\n"
        f"- Experiência do autor: {d.get('autor_experiencia','não informada')}\n\n"
        f"Gere EXATAMENTE neste formato, sem texto extra antes ou depois:\n\n"
        f"PROMESSA_CALIBRADA: [promessa real e crível que um ebook pode cumprir]\n\n"
        f"TOM_E_VOZ: [como o autor deve soar em toda comunicação. Máximo 2 frases.]\n\n"
        f"PONTO_A: [situação atual do público — o que sentem, pensam, já tentaram. Máximo 3 frases.]\n\n"
        f"PONTO_B: [transformação específica e realista que o ebook proporciona. Máximo 3 frases.]\n\n"
        f"MECANISMO: [método central do ebook em 1 frase]\n\n"
        f"ANCORA_DA_OFERTA: [como posicionar o ebook como próximo passo natural do que foi aprendido grátis. 2 frases.]\n\n"
        f"FRASE_DO_ANUNCIO: [frase de abertura poderosa para os anúncios — crível e coerente com o ebook]\n\n"
        f"HEADLINE_LP: [headline principal para a landing page — baseada na promessa calibrada]\n"
    )

def system_fio_condutor():
    return (
        "Você é um estrategista de lançamentos digitais. Crie a narrativa central de forma que todas as peças "
        "contem a mesma história de ângulos diferentes. Seja realista: o produto é um ebook. "
        "A coerência entre as peças é mais valiosa do que promessas grandiosas. "
        "Responda APENAS no formato solicitado, sem introduções ou comentários extras."
    )

def prompt_ebook():
    d = st.session_state.dados
    fio_ctx = f"\n\nFIO CONDUTOR (use como referência de tom e promessa):\n{fio()}" if fio() else ""
    return (f"Gere 60 cartões educativos numerados para o e-book '{d['nome_eb']}'. "
            f"Público-alvo: {d['publico']}. Dor principal: {d['dor']}. "
            f"Diferencial: {d['diferencial']}. Cada cartão deve ter título e conteúdo útil.{fio_ctx}")

def system_ebook():
    return "Você é um especialista em conteúdo digital educativo. Seja objetivo e prático."

def prompt_bonus():
    d = st.session_state.dados
    fio_ctx = f"\n\nFIO CONDUTOR (mantenha coerência de tom e promessa):\n{fio()}" if fio() else ""
    return (
        f"Crie 3 ebooks bônus complementares para quem comprou o ebook principal sobre {d.get('nicho')}. "
        f"Ebook principal: {d.get('nome_eb')}. Publico-alvo: {d.get('publico')}. "
        f"Dor principal: {d.get('dor')}. Promessa: {d.get('promessa')}. "
        f"Para cada ebook bonus, gere EXATAMENTE neste formato:\n\n"
        f"BONUS 1: [Nome]\nDescricao: [2 linhas]\nConteudo: [20 cartoes educativos numerados]\n\n"
        f"BONUS 2: [Nome]\nDescricao: [2 linhas]\nConteudo: [20 cartoes educativos numerados]\n\n"
        f"BONUS 3: [Nome]\nDescricao: [2 linhas]\nConteudo: [20 cartoes educativos numerados]"
        f"{fio_ctx}"
    )

def system_bonus():
    return "Você é um especialista em conteúdo digital educativo. Crie ebooks bônus práticos que agreguem valor real ao produto principal."

def prompt_aquecimento():
    d = st.session_state.dados
    data_fmt = d['data_lancto'].strftime('%d/%m/%Y') if d.get('data_lancto') else 'em breve'
    fio_ctx = f"\n\nFIO CONDUTOR (use TOM_E_VOZ, PONTO_A e MECANISMO para guiar cada mensagem):\n{fio()}" if fio() else ""
    return (
        f"Crie 5 mensagens de aquecimento para um grupo de WhatsApp/Telegram sobre {d.get('nicho')}.\n\n"
        f"CONTEXTO: Público: {d.get('publico')}. Dor: {d.get('dor')}. "
        f"Ebook: {d.get('nome_eb')}. Promessa: {d.get('promessa')}. Lançamento: {data_fmt}.\n"
        f"{fio_ctx}\n\n"
        f"OBJETIVO: Entregar valor real ANTES de qualquer venda. Cada mensagem cobre temas que o ebook aprofunda — "
        f"assim a oferta parecerá o próximo passo natural, não uma surpresa.\n\n"
        f"Gere EXATAMENTE neste formato:\n\n"
        f"DIA 1: [Título]\n[Mensagem prática, máximo 10 linhas, 1 dica acionável hoje]\nGancho: [1 frase criando expectativa]\n\n"
        f"DIA 2: [Título]\n[Mensagem]\nGancho: [frase]\n\n"
        f"DIA 3: [Título]\n[Mensagem]\nGancho: [frase]\n\n"
        f"DIA 4: [Título]\n[Mensagem]\nGancho: [frase]\n\n"
        f"DIA 5: [Título — toque que algo especial vem aí]\n[Mensagem de encerramento]\n"
        f"Gancho: [Amanhã tem uma novidade especial — fique de olho neste grupo]\n\n"
        f"REGRAS: Tom humano. Cada dia ensina algo diferente. ZERO CTA de venda."
    )

def system_aquecimento():
    return ("Você é um especialista em marketing de conteúdo e lançamentos digitais. "
            "O conteúdo gratuito deve ser a antessala natural do produto pago. "
            "Escreva como um ser humano, não como um robô de vendas.")

# ── PROMPT PROGRAMA 15 DIAS ──────────────────────────────────
def prompt_prog15():
    d = st.session_state.dados
    nicho       = d.get('nicho', '')
    publico     = d.get('publico', '')
    nome_eb     = d.get('nome_eb', '')
    dor         = d.get('dor', '')
    promessa    = d.get('promessa', '')
    preco       = d.get('preco', 47)
    bonus_resumo = d.get('bonus_resumo', '')
    data_lancto = d.get('data_lancto')
    data_fmt    = data_lancto.strftime('%d/%m/%Y') if data_lancto else 'em breve'
    autor_nome  = d.get('autor_nome', 'o criador')
    whatsapp_num = d.get('whatsapp_contato', 'SEU NÚMERO AQUI')

    bonus_lista = ''
    if bonus_resumo:
        bonus_lista = '\n'.join([f'🎁 Bônus {i+1} – {b.strip()}' for i, b in enumerate(bonus_resumo.split(',')) if b.strip()])
    else:
        bonus_lista = '🎁 Bônus 1 – [Nome]\n🎁 Bônus 2 – [Nome]\n🎁 Bônus 3 – [Nome]'

    fio_ctx = f"\n\nFIO CONDUTOR (use TOM_E_VOZ, PROMESSA_CALIBRADA e ANCORA_DA_OFERTA em todas as peças):\n{fio()}" if fio() else ""

    return (
        f"Crie o PROGRAMA 15 DIAS completo para o lançamento do ebook sobre {nicho}.\n\n"
        f"CONTEXTO DO LANÇAMENTO:\n"
        f"- Nicho: {nicho}\n"
        f"- Público-alvo: {publico}\n"
        f"- Nome do ebook: {nome_eb}\n"
        f"- Dor principal: {dor}\n"
        f"- Promessa: {promessa}\n"
        f"- Preço de lançamento: R${preco}\n"
        f"- Bônus: {bonus_resumo if bonus_resumo else 'serão 3 bônus complementares'}\n"
        f"- Data do lançamento: {data_fmt}\n"
        f"- Autor: {autor_nome}\n"
        f"- WhatsApp de contato para DM: {whatsapp_num}\n"
        f"{fio_ctx}\n\n"
        f"CONCEITO CENTRAL: Você não chama de lançamento. Você chama de 'Programa gratuito de 15 dias para [objetivo]'. "
        f"O grupo, o anúncio e a LP ficam todos alinhados a esse conceito. A venda acontece naturalmente no final.\n\n"
        f"Gere EXATAMENTE neste formato (use os rótulos exatamente como estão, seguidos de dois pontos):\n\n"
        f"ANUNCIO:\n"
        f"[Headline: 🚀 Participe gratuitamente do Programa 15 Dias para [objetivo adaptado ao nicho]\n"
        f"Texto do anúncio: Durante os próximos 15 dias você vai receber dicas práticas, atividades simples e orientações para conquistar [objetivo]. "
        f"✅ Gratuito ✅ Grupo fechado ✅ Conteúdo diário ✅ Vagas limitadas\n"
        f"Adapte ao nicho {nicho} e ao público {publico}. Tom humano e direto.]\n\n"
        f"LP:\n"
        f"[Headline: Programa 15 Dias para [objetivo]\n"
        f"Subheadline explicando o que receberão nos 15 dias.\n"
        f"Lista de 4 benefícios com ✔.\n"
        f"Botão: QUERO PARTICIPAR\n"
        f"Adapte ao nicho {nicho}.]\n\n"
        f"BOAS_VINDAS:\n"
        f"[Mensagem automática ao entrar no grupo. Calorosa, curta, sem mencionar venda. "
        f"Adapte ao nicho {nicho}.]\n\n"
        f"DIA_7:\n"
        f"[Bom dia + apresentação do programa. Diga que durante os próximos dias receberão conteúdos práticos sobre {nicho}. "
        f"Mencione que responderá mensagens pessoalmente pelo WhatsApp {whatsapp_num}. Máximo 8 linhas.]\n\n"
        f"DIA_6:\n"
        f"[Atividade interativa: enquete sobre a maior dificuldade do público em relação a {nicho}. "
        f"4 opções numeradas. Peça para responder no WhatsApp {whatsapp_num} — explique que o grupo é fechado. "
        f"Máximo 8 linhas.]\n\n"
        f"DIA_5:\n"
        f"[Dica prática + mini conteúdo real sobre {nicho}. 1 ensinamento acionável hoje. Máximo 8 linhas.]\n\n"
        f"DIA_4:\n"
        f"[Atividade rápida + engajamento. Pode ser uma pergunta reflexiva ou desafio simples. Máximo 8 linhas.]\n\n"
        f"DIA_3:\n"
        f"[Conteúdo de valor sobre {nicho}. Aprofunda um ponto ligado à dor '{dor}'. Máximo 8 linhas.]\n\n"
        f"DIA_2:\n"
        f"[Simule um depoimento de alguém da 'turma passada' que superou a dor '{dor}' e alcançou resultados relacionados à promessa '{promessa}'. "
        f"Apresente como conquista real, de forma humana. Máximo 8 linhas.]\n\n"
        f"VESPERA:\n"
        f"[Mensagem da véspera da venda. Diga que durante esses dias recebeu centenas de mensagens no WhatsApp e entendeu que mais de 80% "
        f"enfrentam os mesmos obstáculos. Por isso criou o '{nome_eb}'. Será lançado amanhã, em primeira mão, com valor promocional e 3 bônus especiais. "
        f"Não revele o preço ainda. Grande abraço. Máximo 10 linhas.]\n\n"
        f"VENDA_MANHA:\n"
        f"[Mensagem do dia da venda — manhã. Anuncie o lançamento do '{nome_eb}'. "
        f"De R${preco*2} por apenas R${preco} hoje. "
        f"Mencione que amanhã estará disponível em plataformas como Amazon por valor maior. "
        f"Liste os bônus:\n{bonus_lista}\n"
        f"👉 [LINK MONETIZZE]\n"
        f"⏰ Promoção válida até 23:59 de hoje. ✅ Garantia de 7 dias pela Monetizze. "
        f"Máximo 15 linhas.]\n\n"
        f"VENDA_TARDE:\n"
        f"[Lembrete noturno. Curto e direto. Lembra que a promoção encerra hoje à meia-noite. "
        f"Reforça a garantia de 7 dias. Máximo 5 linhas.]\n"
    )

def system_prog15():
    return (
        "Você é um especialista em lançamentos digitais e copywriting para grupos de WhatsApp e Telegram. "
        "Crie o Programa 15 Dias de forma que a venda pareça a conclusão natural de uma jornada de valor — "
        "não um lançamento forçado. Tom humano, direto, sem parecer robô. "
        "Responda APENAS no formato solicitado com os rótulos exatos pedidos."
    )

def prompt_fb():
    d = st.session_state.dados
    fio_ctx = (
        f"\n\nFIO CONDUTOR — USE OBRIGATORIAMENTE:\n{fio()}\n\n"
        f"INSTRUÇÕES: Use FRASE_DO_ANUNCIO como ponto de partida. Use TOM_E_VOZ definido. "
        f"A promessa deve ser a PROMESSA_CALIBRADA. CTA leva para grupo gratuito."
    ) if fio() else ""
    return (
        f"Crie 5 variações de copy curta para Facebook Ads. "
        f"Nicho: {d['nicho']}. Público: {d['publico']}. Dor: {d['dor']}. "
        f"Lançamento: {d['data_lancto'].strftime('%d/%m/%Y')}. "
        f"OBRIGATÓRIO: 1. Título em negrito HTML <strong>. 2. Sugestão de criativo visual. "
        f"3. Finalize com: ⬇️ Clique abaixo e descubra como. 4. Parágrafos separados.{fio_ctx}"
    )

def system_fb():
    return ("Você é um copywriter especialista em Facebook Ads. "
            "Escreva copies críveis, coerentes com o que um ebook pode entregar. "
            "Use tags HTML <strong> para negrito, nunca asteriscos.")

def prompt_lp():
    d = st.session_state.dados
    secao_autor = ''
    if d.get('autor_nome') or d.get('autor_experiencia'):
        secao_autor = (f"Autor: {d.get('autor_nome','')}, Experiência: {d.get('autor_experiencia','')}, "
                       f"Credenciais: {d.get('autor_credenciais','')}.  ")
    fio_ctx = (
        f"\n\nFIO CONDUTOR — USE OBRIGATORIAMENTE:\n{fio()}\n\n"
        f"INSTRUÇÕES: Use HEADLINE_LP como headline principal. PONTO_A para seção de dor. "
        f"PONTO_B para seção de solução. Promessa = PROMESSA_CALIBRADA. "
        f"CTA: [ ENTRAR NO GRUPO GRATUITO ]. TOM_E_VOZ consistente do início ao fim."
    ) if fio() else ""
    return (
        f"Crie 5 variações de copy completa para Landing Page. "
        f"Situação atual: {d['atual']}. Desejada: {d['desejada']}. "
        f"Promessa: {d['promessa']}. Diferencial: {d['diferencial']}. {secao_autor}"
        f"Cada variação: headline, subtítulo, seção de dor, solução, 'Quem sou eu', benefícios, "
        f"sugestões visuais. Finalizar com: [ ENTRAR NO GRUPO GRATUITO ].{fio_ctx}"
    )

def system_lp():
    return ("Você é um especialista em Landing Pages de alta conversão. "
            "Crie LPs coerentes com a promessa real do produto. "
            "Use tag HTML <strong> para negrito. Nunca asteriscos.")

def prompt_msg():
    d = st.session_state.dados
    data   = d['data_lancto'].strftime('%d/%m/%Y')
    data_d1 = (d['data_lancto'] - timedelta(days=1)).strftime('%d/%m/%Y')
    preco  = d.get('preco', 47)
    nome_eb = d.get('nome_eb', '')
    bonus_resumo = d.get('bonus_resumo', '')
    bonus_list = '\n'.join([f'  🎁 {b.strip()}' for b in bonus_resumo.split(',') if b.strip()]) if bonus_resumo else '  🎁 Bônus complementares inclusos'
    fio_ctx = (
        f"\n\nFIO CONDUTOR — USE OBRIGATORIAMENTE:\n{fio()}\n\n"
        f"INSTRUÇÕES: Mensagem 1 usa TOM_E_VOZ. Mensagem 2 referencia jornada das mini-aulas e PONTO_A. "
        f"Mensagem 3 usa ANCORA_DA_OFERTA — ebook é próximo passo natural. Promessa = PROMESSA_CALIBRADA."
    ) if fio() else ""
    return (
        f"Crie 3 mensagens para grupo de WhatsApp/Telegram de lançamento.\n\n"
        f"DADOS: Nicho: {d['nicho']}. Público: {d['publico']}. Ebook: {nome_eb}. "
        f"Dor: {d['dor']}. Promessa: {d['promessa']}. Preço: R${preco}. "
        f"Bônus: {bonus_resumo}. Lançamento: {data}. Véspera: {data_d1}.\n"
        f"{fio_ctx}\n\n"
        f"REGRAS: Mensagens 1 e 2 curtas (máx 5 linhas). Mensagem 3 compacta (máx 15 linhas). Tom humano.\n\n"
        f"**Descrição do grupo:**\nEste grupo é silencioso. Aqui você receberá apenas conteúdos e avisos sobre {d['nicho']}.\n\n---\n\n"
        f"**📩 Mensagem 1 – Boas-vindas**\n[Boas-vindas curta. Grupo de conteúdo gratuito sobre {d['nicho']}. Em {data} libera algo especial. Máx 5 linhas.]\n\n---\n\n"
        f"**⏳ Mensagem 2 – Aquecimento ({data_d1})**\n[Antecipação. Conecte com jornada das mini-aulas. 'Você aprendeu X, agora vem o próximo passo'. Máx 5 linhas.]\n\n---\n\n"
        f"**🚀 Mensagem 3 – Lançamento ({data})**\n"
        f"[🔥 frase conectando com o que o grupo aprendeu\n\n"
        f"📘 *{nome_eb}*\n[linha com PROMESSA_CALIBRADA]\n\n"
        f"🎁 *Bônus inclusos:*\n{bonus_list}\n\n"
        f"💰 Preço de lançamento: R${preco}\n✅ Garantia: 7 dias\n\n"
        f"👉 [LINK DA MONETIZZE]\n\n⚠️ Válido só hoje, {data}.]"
    )

def system_msg():
    return ("Você é um especialista em copywriting para lançamentos no WhatsApp e Telegram. "
            "A oferta deve parecer o próximo passo lógico da jornada, não uma surpresa. "
            "Use linguagem simples e direta.")

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
    st.caption("Aparecem na Landing Page, no Fio Condutor e no Programa 15 Dias.")
    d['autor_nome']        = st.text_input("Seu nome:", value=d.get('autor_nome',''), placeholder="ex: João Silva")
    d['autor_experiencia'] = st.text_area("Sua experiência com o tema:", value=d.get('autor_experiencia',''), placeholder="ex: Invisto em criptomoedas há 4 anos.")
    d['autor_credenciais'] = st.text_area("Resultados ou conquistas:", value=d.get('autor_credenciais',''), placeholder="ex: Já ajudei mais de 200 pessoas.")

    st.divider()
    st.markdown("#### WhatsApp para contato direto")
    st.caption("Usado no Programa 15 Dias para receber respostas da enquete e dúvidas pessoais.")
    d['whatsapp_contato'] = st.text_input("Seu número de WhatsApp:", value=d.get('whatsapp_contato',''), placeholder="ex: (11) 99999-9999")

    from datetime import date
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
        🧵 <strong>Fio Condutor</strong> — narrativa central coerente em todas as peças<br>
        📚 <strong>E-book:</strong> {d.get('nome_eb')} — 60 cartões educativos<br>
        🎁 <strong>3 E-books Bônus</strong> complementares<br>
        🔥 <strong>5 Mini-aulas de Aquecimento</strong> alinhadas ao produto<br>
        🟢 <strong>Programa 15 Dias</strong> — funil completo sem parecer lançamento<br>
        💬 <strong>5 Anúncios</strong> com promessa calibrada<br>
        🌐 <strong>5 variações de Landing Page</strong> coerentes com o anúncio<br>
        📩 <strong>3 Mensagens de grupo</strong> conectando jornada à oferta<br>
        🚀 <strong>Lançamento:</strong> {d['data_lancto'].strftime('%d/%m/%Y')}
        </div>""", unsafe_allow_html=True)

    if st.button("AVANÇAR →"):
        faltando = [c for c in campos_obrigatorios if not d.get(c,'').strip()]
        if faltando: st.warning("Preencha todos os campos antes de avançar.")
        else: st.session_state.etapa = "Fio_Condutor"; st.rerun()

# ── FIO CONDUTOR ─────────────────────────────────────────────
elif st.session_state.etapa == "Fio_Condutor":
    barra_navegacao()
    st.title("🧵 FIO CONDUTOR DO LANÇAMENTO")
    st.markdown("""<div class="fio-card">
    <strong style="color:#92400E;font-size:1.05em;">O que é o Fio Condutor?</strong><br><br>
    É a <strong>espinha dorsal</strong> de todo o seu lançamento. Gerado uma única vez, ele define a promessa calibrada,
    o tom do autor, o arco de transformação e a âncora da oferta.<br><br>
    <strong>Todos os outros conteúdos usam o Fio como referência obrigatória</strong> — garantindo que o cliente viva
    uma jornada coerente do anúncio até a compra.
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="btn-fio">', unsafe_allow_html=True)
    gerar_fio = st.button("🧵 GERAR FIO CONDUTOR")
    st.markdown('</div>', unsafe_allow_html=True)

    if gerar_fio:
        with st.spinner("Criando a narrativa central do seu lançamento..."):
            st.session_state.dados['fio_condutor'] = chamar_ia(prompt_fio_condutor(), system_fio_condutor())
            st.rerun()

    if 'fio_condutor' in st.session_state.dados:
        st.divider()
        st.markdown("#### Sua narrativa central")
        st.markdown("""<div class="fio-alerta">
        ⚠️ <strong>Revise antes de avançar.</strong> Se algo parecer exagerado ou não representar bem o produto,
        clique em Regenerar. O Fio Condutor define o tom de tudo que vem depois.
        </div>""", unsafe_allow_html=True)
        for s in parsear_fio(st.session_state.dados['fio_condutor']):
            st.markdown(f"<div class='fio-label'>{s['label']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='fio-secao'>{normalizar_markdown(s['conteudo'])}</div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(label="📋 Copiar como .txt", data=limpar_html(st.session_state.dados['fio_condutor']),
                file_name="fio_condutor.txt", mime="text/plain", key="copy_fio", use_container_width=True)
        with col2:
            st.markdown('<div class="btn-secundario">', unsafe_allow_html=True)
            if st.button("🔄 Regenerar Fio Condutor", key="regen_fio", use_container_width=True):
                with st.spinner("Regenerando..."):
                    st.session_state.dados['fio_condutor'] = chamar_ia(prompt_fio_condutor(), system_fio_condutor())
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        st.divider()
        if st.button("AVANÇAR →"): st.session_state.etapa = "Gerar_Ebook"; st.rerun()

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
    st.caption("Os bônus serão complementares ao ebook principal e incluídos automaticamente na Mensagem de Lançamento e no Programa 15 Dias.")
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
        if st.button("AVANÇAR →"): st.session_state.etapa = "Gerar_Aquecimento"; st.rerun()

# ── AQUECIMENTO ──────────────────────────────────────────────
elif st.session_state.etapa == "Gerar_Aquecimento":
    barra_navegacao()
    st.title("🔥 MINI-AULAS DE AQUECIMENTO")
    st.markdown("""<div class="preview-box">
    <strong>Por que isso importa?</strong><br><br>
    As mini-aulas cobrem exatamente os temas que o ebook aprofunda — assim, quando a oferta chegar,
    o produto parecerá o <em>próximo passo natural</em>, não uma surpresa.
    O Fio Condutor garante coerência de tom com o anúncio e a LP.
    </div>""", unsafe_allow_html=True)
    st.markdown("""<div style="background:#F5F3FF;border:1px solid #DDD6FE;border-radius:10px;padding:16px 20px;margin-bottom:20px;">
    <strong style="color:#5B21B6;">📅 Como usar:</strong><br>
    <span style="color:#4C1D95;font-size:0.9em;">Envie 1 por dia nos 5 dias antes do lançamento.<br>
    Dia 1 → Dia 2 → Dia 3 → Dia 4 → Dia 5 → 🚀 Lançamento</span></div>""", unsafe_allow_html=True)
    st.markdown('<div class="btn-roxo">', unsafe_allow_html=True)
    gerar_btn = st.button("🔥 GERAR 5 MINI-AULAS DE AQUECIMENTO")
    st.markdown('</div>', unsafe_allow_html=True)
    if gerar_btn:
        with st.spinner("Criando conteúdo alinhado ao Fio Condutor..."):
            st.session_state.dados['aquecimento_cont'] = chamar_ia(prompt_aquecimento(), system_aquecimento())
            st.rerun()
    if 'aquecimento_cont' in st.session_state.dados:
        st.divider()
        st.markdown("#### Suas 5 mini-aulas prontas para enviar")
        bloco_conteudo('aquecimento_cont', 'Aquecimento', prompt_aquecimento, system_aquecimento)
        st.divider()
        if st.button("AVANÇAR →"): st.session_state.etapa = "Prog15Dias"; st.rerun()

# ── PROGRAMA 15 DIAS ─────────────────────────────────────────
elif st.session_state.etapa == "Prog15Dias":
    barra_navegacao()
    st.title("🟢 PROGRAMA 15 DIAS")

    st.markdown("""<div class="p15-bloco">
    <strong style="color:#065F46;font-size:1.05em;">O que é o Programa 15 Dias?</strong><br><br>
    É uma estratégia onde você <strong>não chama de lançamento</strong> — você chama de
    <em>"Programa gratuito de 15 dias para [objetivo]"</em>.<br><br>
    O anúncio, a página de captura e o grupo ficam todos alinhados a esse conceito.
    A venda acontece no último dia de forma <strong>natural e coerente</strong> com tudo que a pessoa recebeu antes.
    O cliente não sente que foi "vendido" — sente que encontrou a solução que estava esperando.
    </div>""", unsafe_allow_html=True)

    st.markdown("""<div class="p15-alerta">
    📅 <strong>Estrutura dos 15 dias:</strong><br>
    Dias 1–8: Encher o grupo com anúncios → Dia 8: Boas-vindas →
    Dia 9 (D-7): Abertura do programa → Dia 10 (D-6): Enquete →
    Dia 11 (D-5): Dica prática → Dia 12 (D-4): Atividade →
    Dia 13 (D-3): Conteúdo de valor → Dia 14 (D-2): Depoimento →
    Dia 14 (D-1): Véspera da venda → Dia 15: 🚀 Venda
    </div>""", unsafe_allow_html=True)

    if not st.session_state.dados.get('whatsapp_contato'):
        st.warning("⚠️ Você não preencheu o WhatsApp de contato no formulário. O Programa 15 Dias usa esse número para receber respostas da enquete. Você pode voltar ao formulário para preencher.")

    st.markdown('<div class="btn-verde15">', unsafe_allow_html=True)
    gerar_p15 = st.button("🟢 GERAR PROGRAMA 15 DIAS COMPLETO")
    st.markdown('</div>', unsafe_allow_html=True)

    if gerar_p15:
        with st.spinner("Gerando o funil completo do Programa 15 Dias..."):
            st.session_state.dados['prog15_cont'] = chamar_ia(prompt_prog15(), system_prog15())
            st.rerun()

    if 'prog15_cont' in st.session_state.dados:
        st.divider()
        st.markdown("#### Seu funil completo — pronto para copiar e enviar")
        st.caption("Cada bloco abaixo corresponde a uma peça do funil. Copie e use no dia certo.")

        secoes = parsear_prog15(st.session_state.dados['prog15_cont'])
        for s in secoes:
            st.markdown(f"<div class='p15-dia-header'>{s['label']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='p15-conteudo'>{normalizar_markdown(s['conteudo'])}</div>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.download_button(label="📋 Copiar como .txt", data=limpar_html(st.session_state.dados['prog15_cont']),
                file_name="programa_15_dias.txt", mime="text/plain", key="copy_p15", use_container_width=True)
        with col2:
            st.markdown('<div class="btn-secundario">', unsafe_allow_html=True)
            if st.button("🔄 Regenerar Programa 15 Dias", key="regen_p15", use_container_width=True):
                with st.spinner("Regenerando..."):
                    st.session_state.dados['prog15_cont'] = chamar_ia(prompt_prog15(), system_prog15())
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        st.divider()
        if st.button("AVANÇAR →"): st.session_state.etapa = "Copy_Face"; st.rerun()

# ── COPY FACEBOOK ─────────────────────────────────────────────
elif st.session_state.etapa == "Copy_Face":
    barra_navegacao()
    st.title("📱 COPY PARA O FACEBOOK")
    if fio():
        st.markdown("""<div class="fio-alerta">🧵 <strong>Fio Condutor ativo.</strong>
        Os anúncios usarão a FRASE_DO_ANUNCIO e PROMESSA_CALIBRADA — garantindo coerência com LP e aquecimento.</div>""", unsafe_allow_html=True)
    if st.button("GERAR 5 VARIAÇÕES"):
        with st.spinner("Gerando copies com IA..."):
            st.session_state.dados['fb_copy'] = chamar_ia(prompt_fb(), system_fb())
    if 'fb_copy' in st.session_state.dados:
        bloco_conteudo('fb_copy', 'Anúncios', prompt_fb, system_fb)
        if st.button("AVANÇAR →"): st.session_state.etapa = "Copy_LP"; st.rerun()

# ── LANDING PAGE ──────────────────────────────────────────────
elif st.session_state.etapa == "Copy_LP":
    barra_navegacao()
    st.title("🌐 COPY PARA A LANDING PAGE")
    if fio():
        st.markdown("""<div class="fio-alerta">🧵 <strong>Fio Condutor ativo.</strong>
        HEADLINE_LP e PONTO_A/PONTO_B do Fio serão usados como base para todas as variações.</div>""", unsafe_allow_html=True)
    if st.button("GERAR 5 VARIAÇÕES LP"):
        with st.spinner("Gerando landing pages com IA..."):
            st.session_state.dados['lp_copy'] = chamar_ia(prompt_lp(), system_lp())
    if 'lp_copy' in st.session_state.dados:
        bloco_conteudo('lp_copy', 'Landing Page', prompt_lp, system_lp)
        if st.button("AVANÇAR →"): st.session_state.etapa = "Mensagens_Grupo"; st.rerun()

# ── MENSAGENS DO GRUPO ────────────────────────────────────────
elif st.session_state.etapa == "Mensagens_Grupo":
    barra_navegacao()
    st.title("📌 MENSAGENS PARA O GRUPO")
    if fio():
        st.markdown("""<div class="fio-alerta">🧵 <strong>Fio Condutor ativo.</strong>
        A Mensagem 3 usará a ANCORA_DA_OFERTA para posicionar o ebook como próximo passo natural.</div>""", unsafe_allow_html=True)
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

🧵 FIO CONDUTOR
{'-'*40}
{limpar_html(d.get('fio_condutor','Não gerado.'))}

📚 E-BOOK PRINCIPAL
{'-'*40}
{limpar_html(d.get('ebook_cont','Não gerado.'))}

🎁 E-BOOKS BÔNUS
{'-'*40}
{limpar_html(d.get('bonus_cont','Não gerado.'))}

🔥 MINI-AULAS DE AQUECIMENTO
{'-'*40}
{limpar_html(d.get('aquecimento_cont','Não gerado.'))}

🟢 PROGRAMA 15 DIAS
{'-'*40}
{limpar_html(d.get('prog15_cont','Não gerado.'))}

🎬 ANÚNCIOS (FACEBOOK)
{'-'*40}
{limpar_html(d.get('fb_copy','Não gerado.'))}

🌐 LANDING PAGE
{'-'*40}
{limpar_html(d.get('lp_copy','Não gerado.'))}

📌 MENSAGENS DO GRUPO
{'-'*40}
{limpar_html(d.get('msg_grupo','Não gerado.'))}""".strip()

    st.markdown('<div class="btn-verde">', unsafe_allow_html=True)
    st.download_button(label="⬇️ BAIXAR PROJETO COMPLETO (.txt)", data=texto_completo,
        file_name=f"{nome_projeto.replace(' ','_')}_lancamento.txt", mime="text/plain", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    with st.expander("🧵 FIO CONDUTOR"):
        st.caption("A narrativa central que conecta todas as peças.")
        bloco_conteudo('fio_condutor','Fio Condutor',prompt_fio_condutor,system_fio_condutor)
    with st.expander("📚 E-BOOK"):
        bloco_conteudo('ebook_cont','E-book',prompt_ebook,system_ebook)
    with st.expander("🎁 E-BOOKS BÔNUS"):
        bloco_conteudo('bonus_cont','Bônus',prompt_bonus,system_bonus)
    with st.expander("🔥 MINI-AULAS DE AQUECIMENTO"):
        st.caption("Envie uma por dia nos 5 dias antes do lançamento.")
        bloco_conteudo('aquecimento_cont','Aquecimento',prompt_aquecimento,system_aquecimento)
    with st.expander("🟢 PROGRAMA 15 DIAS"):
        st.caption("Funil completo: anúncio → LP → grupo → aquecimento → venda.")
        bloco_conteudo('prog15_cont','Programa 15 Dias',prompt_prog15,system_prog15)
    with st.expander("🎬 ANÚNCIO (Facebook)"):
        bloco_conteudo('fb_copy','Anúncios',prompt_fb,system_fb)
    with st.expander("🌐 LANDING PAGE"):
        bloco_conteudo('lp_copy','Landing Page',prompt_lp,system_lp)
    with st.expander("📌 MENSAGENS DO GRUPO"):
        bloco_conteudo('msg_grupo','Mensagens',prompt_msg,system_msg)

    # ── CHECKLIST ─────────────────────────────────────────────
    st.divider()
    with st.expander("✅ CHECKLIST DE LANÇAMENTO — O QUE FAZER AGORA"):
        from datetime import date, timedelta as td
        data_lancto = d.get('data_lancto', date.today())
        dlf  = data_lancto.strftime('%d/%m/%Y') if hasattr(data_lancto,'strftime') else str(data_lancto)
        dm2  = (data_lancto - td(days=1)).strftime('%d/%m/%Y') if hasattr(data_lancto,'strftime') else ''
        dai  = (data_lancto - td(days=6)).strftime('%d/%m') if hasattr(data_lancto,'strftime') else ''
        daf  = (data_lancto - td(days=2)).strftime('%d/%m') if hasattr(data_lancto,'strftime') else ''
        dbv  = (data_lancto - td(days=7)).strftime('%d/%m/%Y') if hasattr(data_lancto,'strftime') else ''

        fases = [
            {"fase":"FASE 1 — HOJE: Preparação","cor":"#0EA5E9","items":[
                ("Hoje","Salve e baixe todo o conteúdo gerado (.txt)"),
                ("Hoje","Crie o grupo: 'Programa 15 Dias para [Objetivo]'"),
                ("Hoje","Configure a descrição do grupo com o texto de boas-vindas gerado"),
                ("Hoje","Cadastre o e-book + 3 bônus na Monetizze e configure o checkout"),
                ("Hoje",f"Defina o preço: R${d.get('preco',47)} e salve o link da Monetizze"),
                ("Hoje","Suba os anúncios usando a copy do Programa 15 Dias gerada"),
                ("Hoje","Aponte os anúncios para o link do grupo (WhatsApp/Telegram)"),
            ]},
            {"fase":"FASE 2 — SEMANA 1: Encher o grupo","cor":"#8B5CF6","items":[
                ("Dias 1 a 7","Anúncios rodando — objetivo: 500 a 1.000 pessoas no grupo"),
                ("Diariamente","Monitore custo por lead (meta: até R$2,00 por pessoa)"),
                (f"{dbv}","Envie a Mensagem de Boas-vindas — primeira comunicação com o grupo"),
                ("Importante","NÃO mencione produto ou preço ainda"),
            ]},
            {"fase":f"FASE 3 — AQUECIMENTO ({dai} a {daf}): Programa 15 Dias","cor":"#059669","items":[
                (f"{dai} — D-7","Envie: Abertura do programa — conteúdo gratuito começa hoje"),
                ("D-6","Enquete interativa — peça para responder no WhatsApp"),
                ("D-5","Dica prática + mini conteúdo real"),
                ("D-4","Atividade rápida + engajamento"),
                ("D-3","Conteúdo de valor aprofundando a dor"),
                (f"{dm2} — D-2","Depoimento de alguém da 'turma passada'"),
                (f"{dm2} — D-1","Véspera: anuncie que amanhã vem algo especial. Não revele o preço."),
                (f"{dm2}","Confirme se o link da Monetizze está funcionando"),
            ]},
            {"fase":f"FASE 4 — DIA DO LANÇAMENTO ({dlf}): Vender","cor":"#22C55E","items":[
                (f"{dlf} — manhã","Envie a mensagem de lançamento com o link da Monetizze"),
                (f"{dlf}","Pause os anúncios ou redirecione para o link de venda"),
                (f"{dlf}","Fique online respondendo dúvidas no WhatsApp"),
                (f"{dlf} — noite","Envie lembrete: 'Encerra hoje à meia-noite'"),
            ]},
            {"fase":"FASE 5 — PÓS-LANÇAMENTO: Escalar","cor":"#64748B","items":[
                ("Após","Anote: pessoas no grupo, compradores, taxa de conversão"),
                ("Após","ROI: faturamento ÷ custo de tráfego"),
                ("Próximos dias","Entregue o e-book e os bônus para quem comprou"),
                ("Próxima semana","Use a base para o próximo lançamento sem custo de tráfego"),
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
                fio_ctx = f"\nFio Condutor:\n{fio()}" if fio() else ""
                system = (f"Você é o Launcerbot, assistente especialista em lançamentos digitais. "
                          f"Usuário: {st.session_state.usuario}. "
                          f"Projeto: nicho={d.get('nicho')}, ebook={d.get('nome_eb')}, público={d.get('publico')}.{fio_ctx}")
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
