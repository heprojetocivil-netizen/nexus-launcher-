import streamlit as st
from groq import Groq
from datetime import timedelta, date, datetime
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

    /* DICA DE FERRAMENTA */
    .dica-ferramenta { background: #FEF9C3; border: 1px solid #FDE047; border-radius: 10px; padding: 16px 20px; margin: 12px 0; color: #713F12; font-size: 0.87em; line-height: 1.7; }
    .dica-ferramenta strong { color: #92400E; }
    </style>
""", unsafe_allow_html=True)

# --- PERSISTÊNCIA: SUPABASE → GOOGLE SHEETS → MEMÓRIA ---
import os, json

# ── SUPABASE ──────────────────────────────────────────────────
def _get_supabase():
    try:
        url = os.environ.get("SUPABASE_URL","").strip()
        key = os.environ.get("SUPABASE_KEY","").strip()
        if not url or not key: return None
        from supabase import create_client
        return create_client(url, key)
    except Exception:
        return None

def sb_carregar(sb):
    try:
        res = sb.table("projetos").select("nome, dados").execute()
        return {r["nome"]: json.loads(r["dados"]) for r in (res.data or [])}
    except Exception: return {}

def sb_salvar(sb, nome, dados):
    try:
        sb.table("projetos").upsert({"nome": nome, "dados": json.dumps(dados, default=str)}, on_conflict="nome").execute()
        return True
    except Exception: return False

def sb_deletar(sb, nome):
    try:
        sb.table("projetos").delete().eq("nome", nome).execute()
        return True
    except Exception: return False

# ── GOOGLE SHEETS ─────────────────────────────────────────────
def _get_sheets():
    try:
        sheet_id = os.environ.get("GSHEET_ID","").strip()
        creds_json = os.environ.get("GSHEET_CREDS","").strip()
        if not sheet_id or not creds_json: return None
        import gspread
        from google.oauth2.service_account import Credentials
        scopes = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
        creds_dict = json.loads(creds_json)
        creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
        gc = gspread.authorize(creds)
        sh = gc.open_by_key(sheet_id)
        try:
            ws = sh.worksheet("projetos")
        except Exception:
            ws = sh.add_worksheet(title="projetos", rows=1000, cols=3)
            ws.append_row(["nome","dados","criado_em"])
        return ws
    except Exception:
        return None

def gs_carregar(ws):
    try:
        rows = ws.get_all_records()
        result = {}
        for r in rows:
            if r.get("nome") and r.get("dados"):
                try: result[r["nome"]] = json.loads(r["dados"])
                except: pass
        return result
    except Exception: return {}

def gs_salvar(ws, nome, dados):
    try:
        dados_str = json.dumps(dados, default=str)
        from datetime import datetime as _dt
        agora = _dt.now().strftime("%Y-%m-%d %H:%M")
        cell = None
        try: cell = ws.find(nome, in_column=1)
        except: pass
        if cell:
            ws.update(f"B{cell.row}", [[dados_str]])
        else:
            ws.append_row([nome, dados_str, agora])
        return True
    except Exception as e:
        return False

def gs_deletar(ws, nome):
    try:
        cell = ws.find(nome, in_column=1)
        if cell: ws.delete_rows(cell.row)
        return True
    except Exception: return False

# ── CACHE FALLBACK ────────────────────────────────────────────
@st.cache_resource
def get_cache_store():
    return {"projetos": {}}

_cache = get_cache_store()
_sb   = _get_supabase()
_gs   = _get_sheets() if not _sb else None

def _backend():
    if _sb:   return "supabase"
    if _gs:   return "sheets"
    return "memoria"

# ── INICIALIZAÇÃO DE ESTADO ───────────────────────────────────
_defaults = {'etapa': "Login", 'dados': {}, 'chat_hist': [],
             'usuario': '', 'api_key': '', 'chat_input_key': 0,
             'projetos': {}, '_db_carregado': False}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

if not st.session_state._db_carregado:
    if _sb:
        st.session_state.projetos = sb_carregar(_sb)
    elif _gs:
        st.session_state.projetos = gs_carregar(_gs)
    else:
        st.session_state.projetos = _cache["projetos"]
    _cache["projetos"] = st.session_state.projetos
    st.session_state._db_carregado = True

def salvar_projeto(nome, dados):
    dados_copy = dados.copy()
    if _sb:
        sb_salvar(_sb, nome, dados_copy)
    elif _gs:
        gs_salvar(_gs, nome, dados_copy)
    st.session_state.projetos[nome] = dados_copy
    _cache["projetos"][nome] = dados_copy

def deletar_projeto(nome):
    if _sb:   sb_deletar(_sb, nome)
    elif _gs: gs_deletar(_gs, nome)
    st.session_state.projetos.pop(nome, None)
    _cache["projetos"].pop(nome, None)

# ── SALVAR LOCALMENTE (download automático via botão) ─────────
def gerar_json_projeto(dados: dict) -> str:
    """Serializa o projeto inteiro em JSON para download local."""
    return json.dumps(dados, ensure_ascii=False, indent=2, default=str)


# --- ETAPAS ---
ETAPAS_LABELS = {
    "Formulario":      "1. Formulário",
    "Potencial_Nicho": "2. Potencial",
    "Gerar_Ebook":     "3. E-book",
    "Gerar_Bonus":     "4. Bônus",
    "Copy_Face":       "5. Anúncio",
    "Copy_LP":         "6. Landing Page",
    "Mensagens_Grupo": "7. Mensagens",
    "Visualizacao":    "8. Projeto Final",
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


def corrigir_texto(texto: str) -> str:
    prompt = (
        f"Corrija o texto abaixo. Corrija: ortografia, acentuação, concordância verbal e nominal, "
        f"pontuação e erros de digitação. Mantenha o tom, estilo e estrutura originais. "
        f"Não reescreva — apenas corrija os erros. Retorne SOMENTE o texto corrigido, sem comentários.\n\n"
        f"TEXTO:\n{texto}"
    )
    system = "Você é um revisor gramatical especialista em português brasileiro. Corrija apenas o necessário."
    try:
        client = Groq(api_key=st.session_state.api_key)
        resp = client.chat.completions.create(
            messages=[{"role":"system","content":system},{"role":"user","content":prompt}],
            model="llama-3.3-70b-versatile"
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Erro: {e}"

def gerar_ics(eventos: list) -> str:
    linhas = [
        'BEGIN:VCALENDAR',
        'VERSION:2.0',
        'PRODID:-//Nexus Launcher//Agendador//PT',
        'CALSCALE:GREGORIAN',
        'METHOD:PUBLISH',
    ]
    for ev in eventos:
        try:
            h, m = map(int, ev['hora'].split(':'))
        except Exception:
            h, m = 9, 0
        dt_start = datetime(ev['data'].year, ev['data'].month, ev['data'].day, h, m, 0)
        dt_end   = datetime(ev['data'].year, ev['data'].month, ev['data'].day, h, m + 30 if m <= 29 else m, 0)
        uid = f"{ev['data'].strftime('%Y%m%d')}-{ev['chave']}@nexuslauncher"
        desc = ev['descricao'].replace('\n', '\\n').replace(',', r'\,').replace(';', r'\;')[:500]
        linhas += [
            'BEGIN:VEVENT',
            f"UID:{uid}",
            f"DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}",
            f"DTSTART:{dt_start.strftime('%Y%m%dT%H%M%S')}",
            f"DTEND:{dt_end.strftime('%Y%m%dT%H%M%S')}",
            f"SUMMARY:{ev['titulo']}",
            f"DESCRIPTION:{desc}",
            'BEGIN:VALARM',
            'TRIGGER:-PT30M',
            'ACTION:DISPLAY',
            f"DESCRIPTION:Lembrete: {ev['titulo']}",
            'END:VALARM',
            'END:VEVENT',
        ]
    linhas.append('END:VCALENDAR')
    return '\r\n'.join(linhas)

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

    col1, col2, col3 = st.columns(3)
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
    with col3:
        st.markdown('<div class="btn-secundario">', unsafe_allow_html=True)
        if st.button(f"✍️ Corrigir gramática", key=f"gram_{chave}", use_container_width=True):
            with st.spinner("Revisando gramática e concordâncias..."):
                st.session_state.dados[chave] = corrigir_texto(limpar_html(conteudo))
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
            # ── PROJETOS SALVOS NA SESSÃO ─────────────────────
            if st.session_state.projetos:
                for nome in list(st.session_state.projetos.keys()):
                    c_abrir, c_deletar = st.columns([4,1])
                    if c_abrir.button(f"📄 {nome}", key=f"abrir_{nome}"):
                        st.session_state.dados = st.session_state.projetos[nome].copy()
                        st.session_state.etapa = "Visualizacao"; st.rerun()
                    st.markdown('<div class="btn-perigo">', unsafe_allow_html=True)
                    if c_deletar.button("🗑️", key=f"del_{nome}", help="Excluir projeto"):
                        deletar_projeto(nome); st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown("""<div style="background:#FEF9C3;border:1px solid #FDE047;border-radius:8px;padding:10px 12px;font-size:0.82em;color:#713F12;margin-bottom:8px;">
                Nenhum projeto na memória.<br>Carregue seu arquivo .json abaixo.
                </div>""", unsafe_allow_html=True)

            # ── CARREGAR DO COMPUTADOR ────────────────────────
            st.divider()
            st.markdown("**📥 Carregar projeto do computador**")
            st.caption("Selecione o arquivo .json que você salvou antes.")
            arq = st.file_uploader("", type=["json"], key="upload_nav", label_visibility="collapsed")
            if arq is not None:
                try:
                    dados_imp = json.load(arq)
                    nome_imp = dados_imp.get('nome_eb', arq.name)
                    st.success(f"✅ **{nome_imp}** — pronto para carregar!")
                    if st.button("📂 ABRIR ESTE PROJETO", key="btn_carregar_nav", use_container_width=True):
                        st.session_state.dados = dados_imp
                        salvar_projeto(nome_imp, dados_imp)
                        st.session_state.etapa = "Visualizacao"
                        st.rerun()
                except Exception:
                    st.error("Arquivo inválido. Use o .json gerado pelo Nexus Launcher.")

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
        f"REGRAS: Deixe BEM EXPLÍCITO que o programa é 100% GRATUITO — use essa palavra em destaque. Sem exageros. Tom humano. Parece um convite, não um anúncio de produto.\n"
        f"No CTA final, use: ⬇️ Clique no link abaixo e garanta sua vaga gratuitamente"
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
        f"Crie UMA landing page com abordagem de DIAGNÓSTICO para capturar leads.\n\n"
        f"CONTEXTO:\n"
        f"- Nicho: {d.get('nicho')}\n- Público: {d.get('publico')}\n"
        f"- Dor principal: {d['dor']}\n- Situação atual: {d['atual']}\n"
        f"- Objetivo: {d['desejada']}\n"
        f"- {secao_autor}\n\n"
        f"CONCEITO CENTRAL — DIAGNÓSTICO:\n"
        f"A LP não vende nada. Ela convida para um programa gratuito que vai DIAGNOSTICAR o problema real "
        f"da pessoa em {d.get('nicho')} e mostrar o que está travando o resultado dela.\n"
        f"Tom: 'Você sabe que algo está errado, mas não sabe exatamente o quê. "
        f"Nesses 15 dias vamos descobrir juntos — e eu vou te mostrar o caminho.'\n"
        f"NUNCA mencione ebook, produto pago, lançamento ou preço.\n\n"
        f"ESTRUTURA OBRIGATÓRIA:\n"
        f"1. Headline: promessa de diagnóstico — ex: 'Descubra o que está travando seu resultado em {d.get('nicho')}' \n"
        f"2. Subtítulo: 'Em 15 dias gratuitos, você vai entender exatamente o que está errado — e o que fazer'\n"
        f"3. Seção de dor — 3 bullets: situações que a pessoa vive e não entende por quê\n"
        f"4. O que o programa faz: diagnostica, identifica os erros, mostra o caminho — tudo grátis\n"
        f"5. Quem sou eu (autor, 2-3 linhas de credibilidade)\n"
        f"6. 4 benefícios com ✔ — focados em clareza, diagnóstico e direção\n"
        f"7. Sugestão de elemento visual\n"
        f"8. CTA: [ QUERO DESCOBRIR O QUE ESTÁ ERRADO ]\n\n"
        f"REGRAS: Tom de quem vai ajudar a pessoa a entender, não de quem vai vender. "
        f"A solução (ebook) aparece só depois, na venda. Aqui só existe o diagnóstico."
    )

def system_lp():
    return ("Você é um especialista em Landing Pages de diagnóstico. "
            "A LP cria curiosidade sobre o problema real da pessoa e posiciona o grupo gratuito "
            "como o lugar onde ela vai descobrir o que está travando seus resultados. "
            "Use tag HTML <strong> para negrito. Nunca asteriscos. Tom humano e direto.")

def prompt_msg():
    d = st.session_state.dados
    data_lancto = d.get('data_lancto')
    data_fmt = data_lancto.strftime('%d/%m/%Y') if data_lancto else 'em breve'
    preco = d.get('preco', 47)
    nome_eb = d.get('nome_eb', '')
    nicho = d.get('nicho', '')
    dor = d.get('dor', '')
    publico = d.get('publico', '')
    whatsapp_num = d.get('whatsapp_contato', 'SEU NÚMERO AQUI')
    link_venda = d.get('link_monetizze', '').strip() or '[LINK MONETIZZE]'

    # ── MODIFICAÇÃO: pede revisão dos nomes dos bônus ──────────
    bonus_resumo = d.get('bonus_resumo', '')
    if bonus_resumo:
        nomes_bonus = [b.strip() for b in bonus_resumo.split(',') if b.strip()]
        bonus_lista = '\n'.join([f'🎁 Bônus {i+1} – {nome}' for i, nome in enumerate(nomes_bonus)])
    else:
        bonus_lista = '🎁 Bônus 1\n🎁 Bônus 2\n🎁 Bônus 3'

    return (
        f"Gere as mensagens do funil de WhatsApp para o lançamento sobre {nicho}.\n"
        f"Ebook: {nome_eb}. Preço: R${preco}. WhatsApp: {whatsapp_num}. Dor: {dor}.\n\n"
        f"REGRA DE OURO — TOM DE WHATSAPP REAL:\n"
        f"- Escreva como uma pessoa real escreveria pra um grupo de amigos\n"
        f"- Saudações vivas e naturais: Bom dia, grupo! Como vocês estão? / Boa tarde, pessoal! / E aí, tudo bem?\n"
        f"- Frases curtas, uma por linha, sem parágrafos longos\n"
        f"- Reticências naturais... pausas... como na fala\n"
        f"- Emojis onde cabem de forma natural, sem exagero\n"
        f"- ZERO texto corporativo, ZERO linguagem de robô, ZERO formalidade\n"
        f"- Parece que foi digitado agora, não copiado de um template\n\n"
        f"Textos entre === FIXO === e === FIM === copie PALAVRA POR PALAVRA.\n"
        f"Blocos [IA] devem ser criados com o mesmo tom humano de WhatsApp.\n\n"

        f"DESCRICAO_GRUPO:\n"
        f"=== FIXO ===\n"
        f"Seja muito bem-vindo ao nosso grupo de [adapte: nome do programa sobre {nicho}]!\n"
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
        f"Seja muito bem-vindo ao nosso grupo de [adapte: nome do programa sobre {nicho}]!\n"
        f"Se você está aqui… provavelmente já tentou melhorar em {nicho} — e não conseguiu manter.\n"
        f"E não é por falta de esforço.\n"
        f"Nos próximos dias, você vai entender exatamente o porquê.\n"
        f"Aqui, você não vai receber conteúdo aleatório.\n"
        f"Você vai receber algo simples… mas que pode destravar algo que você vem tentando há muito tempo.\n"
        f"⚠️ O grupo permanecerá silencioso\n"
        f"Pra você receber só o que realmente importa.\n"
        f"Fica atento… porque o que vem pode te surpreender.\n"
        f"=== FIM ===\n\n"

        # ── MODIFICAÇÃO D-9: "amanhã" em vez de "nas próximas horas" ──
        f"DIA_7:\n"
        f"=== FIXO ===\n"
        f"Bom dia, grupo! ☀️\n"
        f"Como vocês estão?\n"
        f"Espero que bem!\n\n"
        f"Antes de começarmos os conteúdos sobre {nicho}...\n"
        f"Eu quero fazer algo diferente.\n\n"
        f"Quero te entender de verdade.\n\n"
        f"A maioria dos conteúdos por aí são genéricos demais.\n"
        f"E eu não quero fazer isso com vocês.\n\n"
        f"Então amanhã vou mandar um diagnóstico aqui no grupo.\n"
        f"Ele vai me ajudar a entender exatamente onde você tá travado em {nicho}.\n\n"
        f"Fica de olho amanhã 👇\n"
        f"=== FIM ===\n\n"

        f"DIA_6:\n"
        f"[IA] Saudação viva e natural de grupo de WhatsApp (ex: Bom dia, pessoal! Tudo bem por aí? 🌿)\n"
        f"Segunda linha em branco.\n"
        f"Próxima linha: Preciso muito da ajuda de vocês aqui...\n"
        f"Próxima: Quero entender melhor a situação de cada um pra poder ajudar de verdade.\n"
        f"Linha em branco.\n"
        f"Uma pergunta central de diagnóstico sobre a dor {dor} no nicho {nicho}.\n"
        f"Linha em branco.\n"
        f"4 opções A) B) C) D) — cada uma em sua própria linha, curtas e diretas.\n"
        f"Linha em branco.\n"
        f"Me manda sua resposta no WhatsApp: {whatsapp_num} 📲\n"
        f"Vou ler todas... prometo!\n"
        f"Linha em branco.\n"
        f"E em {data_fmt} eu entrego a solução detalhada, passo a passo, pra cada perfil.\n\n"

        f"DIA_5:\n"
        f"[IA] Saudação animada e diferente das anteriores (ex: Boa tarde, galera! 👋 / E aí, pessoal, tudo certo?)\n"
        f"Linha em branco.\n"
        f"Próxima linha: Deixa eu compartilhar algo que pouca gente fala sobre {nicho}...\n"
        f"Linha em branco.\n"
        f"Crie 3 dicas surpreendentes e contra-intuitivas sobre {nicho}.\n"
        f"Cada dica: *Dica X: [título impactante]* (negrito estilo WhatsApp) + 2 linhas explicando.\n"
        f"Tom: Que massa, nunca pensei nisso antes!\n"
        f"Linha em branco entre cada dica.\n"
        f"Finalize com: Aplica uma dessas e me conta o que achou 😊\n\n"

        f"DIA_4:\n"
        f"[IA] Saudação descontraída (ex: Bom dia! Acordei pensando em vocês 😄 / Boa tarde, grupo!)\n"
        f"Linha em branco.\n"
        f"Proponha uma atividade de OBSERVAÇÃO simples sobre {nicho} ligada à dor {dor}.\n"
        f"NÃO explique o motivo — mantenha o mistério.\n"
        f"Linha em branco.\n"
        f"Peça pra responder no WhatsApp {whatsapp_num} o que observaram.\n"
        f"Tom curioso e leve. Máximo 8 linhas no total.\n\n"

        f"DIA_3:\n"
        f"[IA] Saudação direta (ex: Bom dia! 👊 / Boa tarde, pessoal!)\n"
        f"Linha em branco.\n"
        f"Escreva naturalmente assim:\n"
        f"Existe um erro simples que pode estar travando o resultado em {nicho}...\n"
        f"Linha em branco.\n"
        f"Mas o problema é:\n"
        f"👉 ele não é óbvio\n"
        f"👉 e quase ninguém percebe\n"
        f"Linha em branco.\n"
        f"Por isso muita gente continua tentando... ajustando... mas sem sair do lugar.\n"
        f"Linha em branco.\n"
        f"Hoje, só faz isso:\n"
        f"[crie 1 ação de observação simples sobre {nicho} — SEM revelar a causa]\n"
        f"Linha em branco.\n"
        f"Sem mudar nada ainda.\n"
        f"Depois me conta como foi 📲\n\n"

        f"VESPERA:\n"
        f"=== FIXO ===\n"
        f"Eu preciso ser sincero com você.\n"
        f"Depois de tudo que vocês me enviaram no meu WhatsApp…\n"
        f"Eu percebi algo que eu não esperava.\n\n"
        f"Existe um padrão.\n"
        f"E não é pequeno.\n\n"
        f"Mais de 80% das pessoas aqui estão presas exatamente nos mesmos pontos…\n"
        f"Mesmo tentando caminhos diferentes.\n\n"
        f"E isso me fez chegar a uma conclusão:\n"
        f"O problema não está no esforço.\n"
        f"Está no caminho que foi mostrado até hoje.\n\n"
        f"Foi por isso que eu decidi fazer algo diferente.\n"
        f"Algo único… pensado pra resolver isso de forma direta.\n\n"
        f"Mas não é só sobre entender.\n"
        f"É sobre saber exatamente o que fazer — sem dúvidas, sem excesso, sem confusão.\n\n"
        f"Eu organizei tudo de um jeito que praticamente qualquer pessoa aqui consiga aplicar.\n\n"
        f"Amanhã, eu vou te mostrar.\n\n"
        f"Mas já te adianto:\n"
        f"Se você ignorar… provavelmente vai continuar no mesmo lugar.\n\n"
        f"Fica atento.\n"
        f"=== FIM ===\n\n"

        # ── MODIFICAÇÃO: pede revisão dos nomes dos bônus na venda ──
        f"VENDA_MANHA:\n"
        f"=== FIXO ===\n"
        f"Hoje é o dia. 🚀\n\n"
        f"Durante esses dias, eu analisei tudo que vocês me enviaram…\n"
        f"e encontrei padrões que explicam exatamente por que a maioria não consegue evoluir em {nicho}.\n\n"
        f"E como eu te disse ontem:\n"
        f"👉 isso não é óbvio\n"
        f"👉 e quase ninguém percebe sozinho\n\n"
        f"Foi por isso que eu organizei tudo em um método simples:\n\n"
        f"📘 *{nome_eb}*\n\n"
        f"Esse material é a continuação direta do que você começou aqui.\n"
        f"Aqui dentro, você vai entender:\n"
        f"👉 o que realmente está travando seu resultado\n"
        f"👉 e exatamente o que fazer pra corrigir\n\n"
        f"Sem tentativa e erro. Sem perder tempo.\n\n"
        f"E vem com 3 bônus exclusivos:\n"
        f"{bonus_lista}\n\n"
        f"⚠️ ATENÇÃO: Antes de enviar, revise se os nomes dos bônus acima estão corretos — confira com os ebooks que você criou!\n\n"
        f"Tudo isso por apenas *R$ {preco}.*\n\n"
        f"👉 {link_venda}\n\n"
        f"⏰ Só hoje até 23:59\n"
        f"✅ Garantia de 7 dias\n\n"
        f"Você pode continuar tentando ajustar sozinho…\n"
        f"ou seguir um caminho que já está organizado.\n\n"
        f"A decisão é sua.\n"
        f"=== FIM ===\n\n"

        f"VENDA_NOITE:\n"
        f"=== FIXO ===\n"
        f"Boa noite, pessoal! 👋\n\n"
        f"Passando aqui rapidinho pra não deixar vocês esquecerem...\n\n"
        f"Hoje de manhã eu compartilhei aqui algo que preparei com muito carinho pra vocês.\n\n"
        f"📘 Conteúdo direto, sem enrolação\n"
        f"🎁 Com 3 bônus práticos\n\n"
        f"Se você viu e ficou na dúvida, tudo bem.\n"
        f"Mas a verdade é:\n"
        f"Quem aplica o método certo, evolui muito mais rápido.\n\n"
        f"Ainda dá tempo hoje:\n\n"
        f"👉 {link_venda}\n\n"
        f"⏰ Só até 23:59\n"
        f"✅ Garantia de 7 dias\n\n"
        f"Dá uma olhada com calma… e decide com consciência. 🙏\n"
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
    st.subheader("ACESSO RESTRITO A ASSOCIADOS DO QUIZ COM PRÊMIOS")
    st.markdown('<p style="margin-top:-8px;margin-bottom:20px;font-size:0.95em;">🔗 <a href="https://quizcompremios.com.br/" target="_blank" style="color:#00BFFF;text-decoration:none;font-weight:600;">quizcompremios.com.br</a></p>', unsafe_allow_html=True)
    st.session_state.usuario = st.text_input("Nome")
    st.session_state.api_key = st.text_input("Chave Groq", type="password")
    with st.expander("🚀 Primeira vez aqui? Veja como funciona em 3 passos"):
        st.markdown("""
<div style="display:flex;gap:16px;flex-wrap:wrap;">
<div style="flex:1;min-width:180px;background:#EFF6FF;border-radius:10px;padding:16px;text-align:center;">
<div style="font-size:2em;">1️⃣</div>
<div style="font-weight:700;margin:8px 0 4px;font-family:Rajdhani,sans-serif;">Preencha o formulário</div>
<div style="font-size:0.82em;color:#64748B;">Nicho, público, dor, promessa. A IA preenche automaticamente se quiser.</div>
</div>
<div style="flex:1;min-width:180px;background:#F0FDF4;border-radius:10px;padding:16px;text-align:center;">
<div style="font-size:2em;">2️⃣</div>
<div style="font-weight:700;margin:8px 0 4px;font-family:Rajdhani,sans-serif;">Gere tudo com 1 clique</div>
<div style="font-size:0.82em;color:#64748B;">E-book, bônus, anúncio, landing page e funil completo de mensagens.</div>
</div>
<div style="flex:1;min-width:180px;background:#FDF4FF;border-radius:10px;padding:16px;text-align:center;">
<div style="font-size:2em;">3️⃣</div>
<div style="font-weight:700;margin:8px 0 4px;font-family:Rajdhani,sans-serif;">Salve e lance</div>
<div style="font-size:0.82em;color:#64748B;">Projetos salvos ficam disponíveis sempre. Exporte o calendário de envios.</div>
</div>
</div>
<div style="margin-top:14px;background:#FEF9C3;border-radius:8px;padding:10px 14px;font-size:0.82em;color:#713F12;">
💡 <strong>Você precisará de uma chave Groq gratuita</strong> em <a href="https://console.groq.com/keys" target="_blank">console.groq.com/keys</a> — cria conta, gera a chave e cola aqui.
</div>
        """, unsafe_allow_html=True)

    st.markdown("#### Status da API")
    col_groq, _ = st.columns(2)
    with col_groq:
        if st.session_state.api_key.strip():
            try:
                _gc = Groq(api_key=st.session_state.api_key)
                _gc.chat.completions.create(
                    messages=[{"role":"user","content":"ok"}],
                    model="llama-3.3-70b-versatile", max_tokens=1
                )
                st.markdown("""<div style="background:#ECFDF5;border:1px solid #6EE7B7;border-radius:8px;
                padding:10px 14px;font-size:0.82em;color:#064E3B;">
                🟢 <strong>Groq API:</strong> conectada<br>
                <span style="font-size:0.9em;">Chave válida. Geração de conteúdo ativa.</span>
                </div>""", unsafe_allow_html=True)
            except Exception as _e:
                err_msg = str(_e)
                if "401" in err_msg or "invalid" in err_msg.lower():
                    msg = "Chave inválida ou expirada."
                elif "rate" in err_msg.lower():
                    msg = "Limite de requisições atingido."
                else:
                    msg = err_msg[:80]
                st.markdown(f"""<div style="background:#FEF2F2;border:1px solid #FECACA;border-radius:8px;
                padding:10px 14px;font-size:0.82em;color:#7F1D1D;">
                🔴 <strong>Groq API:</strong> erro<br>
                <span style="font-size:0.9em;">{msg}</span>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""<div style="background:#F1F5F9;border:1px solid #CBD5E1;border-radius:8px;
            padding:10px 14px;font-size:0.82em;color:#64748B;">
            ⚪ <strong>Groq API:</strong> aguardando chave
            </div>""", unsafe_allow_html=True)

    st.markdown("")
    if st.button("ENTRAR"):
        if not st.session_state.usuario.strip(): st.error("Informe seu nome.")
        elif not st.session_state.api_key.strip(): st.error("Informe sua chave de API.")
        else: st.session_state.etapa = "Escolha_Tipo"; st.rerun()

# ── ESCOLHA DO TIPO DE LANÇAMENTO ─────────────────────────────
elif st.session_state.etapa == "Escolha_Tipo":
    st.title("NEXUS LAUNCHER")
    st.markdown(f"### Olá, {st.session_state.usuario}! O que você vai lançar?")
    st.markdown("")

    st.markdown("### 🗺️ Como funciona o Nexus Launcher")
    guia_nx = {
        "📚 Lançamento de E-book":    "Programa gratuito 15 dias → aquecimento no grupo → venda do e-book com funil completo de mensagens",
        "🎬 Lançamento de Videoaulas":"Método CPL: 3 vídeos estratégicos de pré-lançamento → abertura de carrinho → fechamento com urgência",
    }
    for etapa, desc in guia_nx.items():
        st.markdown(f"**{etapa}** — {desc}")
    st.markdown("")
    st.markdown("**O que é gerado automaticamente:**")
    st.markdown("📚 E-book com 60 cartões · 🎁 3 Bônus · 📣 Anúncio · 🌐 Landing Page · 💬 Funil de Mensagens completo")
    st.markdown("")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""<div style="background:#EFF6FF;border:2px solid #3B82F6;border-radius:16px;padding:30px;text-align:center;min-height:220px;">
        <div style="font-size:3em;">📚</div>
        <div style="font-family:Rajdhani,sans-serif;font-size:1.4em;font-weight:700;color:#1E3A5F;margin:10px 0 8px;">Lançamento de E-book</div>
        <div style="font-size:0.88em;color:#64748B;line-height:1.5;">Programa gratuito de 15 dias → aquecimento → venda do e-book no grupo do WhatsApp</div>
        </div>""", unsafe_allow_html=True)
        st.markdown("")
        if st.button("📚 LANÇAR E-BOOK", use_container_width=True):
            st.session_state.dados['tipo_lancamento'] = 'ebook'
            st.session_state.etapa = "Formulario"; st.rerun()
    with col2:
        st.markdown("""<div style="background:#FDF4FF;border:2px solid #A855F7;border-radius:16px;padding:30px;text-align:center;min-height:220px;">
        <div style="font-size:3em;">🎬</div>
        <div style="font-family:Rajdhani,sans-serif;font-size:1.4em;font-weight:700;color:#4A1D7A;margin:10px 0 8px;">Lançamento de Videoaulas</div>
        <div style="font-size:0.88em;color:#64748B;line-height:1.5;">Método CPL: pré-lançamento com 3 vídeos estratégicos → abertura de carrinho → fechamento com urgência</div>
        </div>""", unsafe_allow_html=True)
        st.markdown("")
        if st.button("🎬 LANÇAR VIDEOAULAS", use_container_width=True):
            st.session_state.dados['tipo_lancamento'] = 'video'
            st.session_state.etapa = "Video_Formulario"; st.rerun()

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
    d['promessa']    = st.text_input("Transformação do programa:", value=d.get('promessa',''))
    d['diferencial'] = st.text_input("Diferencial:", value=d.get('diferencial',''))
    d['preco']       = st.number_input("Preço do e-book (R$):", min_value=9, max_value=997, value=int(d.get('preco',47)), step=1)

    st.divider()
    st.markdown("#### Suas credenciais como autor")
    d['autor_nome']        = st.text_input("Seu nome:", value=d.get('autor_nome',''))
    d['autor_experiencia'] = st.text_area("Sua experiência com o tema:", value=d.get('autor_experiencia',''))
    d['autor_credenciais'] = st.text_area("Resultados ou conquistas:", value=d.get('autor_credenciais',''))

    st.divider()
    st.markdown("#### WhatsApp para receber respostas da enquete")
    st.markdown("""<div style="background:#FEF9C3;border:1px solid #FDE047;border-radius:8px;padding:12px 16px;margin-bottom:12px;color:#713F12;font-size:0.88em;line-height:1.6;">
    ⚠️ <strong>ATENÇÃO: use um número DIFERENTE do grupo.</strong><br>
    O grupo ficará fechado para mensagens — os membros não conseguem responder lá dentro.<br>
    Por isso, as respostas da enquete e dúvidas devem ir para um número pessoal ou comercial separado.
    </div>""", unsafe_allow_html=True)
    d['whatsapp_contato'] = st.text_input("Número para receber respostas:", value=d.get('whatsapp_contato',''), placeholder="ex: (11) 99999-9999")

    data_sugerida = d.get('data_lancto', date.today() + timedelta(days=15))
    d['data_lancto'] = st.date_input("Data de lançamento", value=data_sugerida, min_value=date.today())
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
        else: st.session_state.etapa = "Potencial_Nicho"; st.rerun()

# ── POTENCIAL DO NICHO ───────────────────────────────────────
elif st.session_state.etapa == "Potencial_Nicho":
    barra_navegacao()
    st.title("📊 POTENCIAL DO NICHO")
    d = st.session_state.dados

    if st.button("🔍 ANALISAR POTENCIAL DO NICHO"):
        with st.spinner("Analisando potencial de mercado..."):
            prompt_pot = (
                f"Analise o potencial de mercado para lançamento digital no nicho: {d.get('nicho')}.\n"
                f"Público-alvo: {d.get('publico')}.\n"
                f"Dor principal: {d.get('dor')}.\n\n"
                f"Responda EXATAMENTE neste formato:\n\n"
                f"NIVEL_DEMANDA: [Alta / Média / Baixa] — justifique em 1 frase\n\n"
                f"NIVEL_CONCORRENCIA: [Alta / Média / Baixa] — justifique em 1 frase\n\n"
                f"TICKET_IDEAL: [faixa de preço recomendada para ebook nesse nicho] — justifique\n\n"
                f"PUBLICO_ESTIMADO: [estimativa do tamanho do público online no Brasil]\n\n"
                f"PONTOS_FORTES: [3 vantagens desse nicho para lançamento digital]\n\n"
                f"PONTOS_ATENCAO: [3 riscos ou desafios desse nicho]\n\n"
                f"ANGULOS_VIRAIS: [3 ângulos de comunicação que tendem a performar bem nesse nicho]\n\n"
                f"VEREDICTO: [Avaliação geral em 2-3 frases — vale lançar? Por quê?]\n\n"
                f"NOTA_GERAL: [nota de 1 a 10 para o potencial desse nicho]"
            )
            system_pot = "Você é um analista de marketing digital especialista em lançamentos no Brasil. Seja direto, realista e baseado em dados de mercado."
            st.session_state.dados['potencial_nicho'] = chamar_ia(prompt_pot, system_pot)

    if st.session_state.dados.get('potencial_nicho'):
        raw = st.session_state.dados['potencial_nicho']
        import re as _re
        def pegar(chave, texto):
            pat = rf"{chave}:\s*(.+?)(?=\n[A-Z_]{{3,}}:|$)"
            m = _re.search(pat, texto, _re.DOTALL)
            return m.group(1).strip() if m else ""

        nivel_dem  = pegar("NIVEL_DEMANDA", raw)
        nivel_con  = pegar("NIVEL_CONCORRENCIA", raw)
        ticket     = pegar("TICKET_IDEAL", raw)
        pub_est    = pegar("PUBLICO_ESTIMADO", raw)
        fortes     = pegar("PONTOS_FORTES", raw)
        atencao    = pegar("PONTOS_ATENCAO", raw)
        virais     = pegar("ANGULOS_VIRAIS", raw)
        veredicto  = pegar("VEREDICTO", raw)
        nota_raw   = pegar("NOTA_GERAL", raw)
        try:
            nota = float(_re.search(r"\d+[.,]?\d*", nota_raw).group().replace(",","."))
        except:
            nota = 0

        cor_nota = "#22C55E" if nota >= 7 else "#F59E0B" if nota >= 5 else "#EF4444"
        st.markdown(
            f"<div style='display:flex;align-items:center;gap:20px;background:#F8FAFC;"
            f"border:2px solid {cor_nota};border-radius:12px;padding:18px 24px;margin-bottom:20px;'>"
            f"<div style='font-size:3em;font-weight:900;color:{cor_nota};font-family:Rajdhani,sans-serif;'>{nota:.0f}<span style='font-size:0.4em;color:#94A3B8;'>/10</span></div>"
            f"<div><div style='font-size:1.1em;font-weight:700;color:#1E293B;'>Potencial geral do nicho</div>"
            f"<div style='font-size:0.88em;color:#64748B;margin-top:4px;'>{veredicto}</div></div>"
            f"</div>", unsafe_allow_html=True
        )

        def nivel_badge(txt):
            txt = txt.split("—")[0].strip().split()[0].strip()
            cor = {"Alta":"#22C55E","Média":"#F59E0B","Baixa":"#EF4444"}.get(txt, "#94A3B8")
            return f"<span style='background:{cor};color:white;padding:2px 10px;border-radius:999px;font-size:0.8em;font-weight:700;'>{txt}</span>"

        c1, c2, c3 = st.columns(3)
        c1.markdown(f"**Demanda**<br>{nivel_badge(nivel_dem)}", unsafe_allow_html=True)
        c2.markdown(f"**Concorrência**<br>{nivel_badge(nivel_con)}", unsafe_allow_html=True)
        c3.markdown(f"**Ticket ideal**<br><span style='font-size:0.9em;color:#1E293B;'>{ticket.split('—')[0].strip()[:40]}</span>", unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**✅ Pontos fortes**")
            for linha in fortes.split("\n"):
                if linha.strip(): st.markdown(f"- {linha.strip().lstrip('123.-)')}")
            st.markdown("**🎯 Ângulos virais**")
            for linha in virais.split("\n"):
                if linha.strip(): st.markdown(f"- {linha.strip().lstrip('123.-)')}")
        with col_b:
            st.markdown("**⚠️ Pontos de atenção**")
            for linha in atencao.split("\n"):
                if linha.strip(): st.markdown(f"- {linha.strip().lstrip('123.-)')}")
            st.markdown(f"**👥 Público estimado:** {pub_est}")

        st.divider()
        if st.button("AVANÇAR → GERAR E-BOOK"): st.session_state.etapa = "Gerar_Ebook"; st.rerun()

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

        st.divider()
        st.markdown("#### 🔗 Link da Monetizze")
        st.markdown("""<div style="background:#F0FDF4;border:1px solid #86EFAC;border-radius:8px;padding:12px 16px;margin-bottom:12px;color:#14532D;font-size:0.87em;line-height:1.6;">
        ✅ <strong>Agora é o momento certo.</strong> Seu e-book e bônus estão prontos.<br>
        Cadastre-os na Monetizze, copie o link de venda e cole abaixo.<br>
        Ele entrará automaticamente nas mensagens de venda.
        </div>""", unsafe_allow_html=True)
        col_lnk, col_lbtn = st.columns([4,1])
        with col_lnk:
            lnk = st.text_input("Link da Monetizze:", value=st.session_state.dados.get('link_monetizze',''),
                placeholder="https://go.monetizze.com.br/...", label_visibility="collapsed")
        with col_lbtn:
            if st.button("💾 Salvar link", use_container_width=True):
                if lnk.strip():
                    st.session_state.dados['link_monetizze'] = lnk.strip()
                    st.success("Link salvo!")
                else:
                    st.warning("Cole o link antes de salvar.")
        if st.session_state.dados.get('link_monetizze'):
            st.caption(f"✅ Link salvo: {st.session_state.dados['link_monetizze']}")

        st.divider()
        if st.button("AVANÇAR →"): st.session_state.etapa = "Copy_Face"; st.rerun()

# ── ANÚNCIO ───────────────────────────────────────────────────
elif st.session_state.etapa == "Copy_Face":
    barra_navegacao()
    st.title("📣 ANÚNCIO")
    st.caption("Um anúncio completo e alinhado com a landing page — mesma promessa, mesmo tom, mesma linguagem.")

    # Link da LP
    st.markdown("#### 🔗 Link da sua Landing Page")
    col_lp, col_lp_btn = st.columns([4,1])
    with col_lp:
        lp_link = st.text_input("Link da Landing Page:", value=st.session_state.dados.get('link_lp',''),
            placeholder="https://sualandingpage.com.br", label_visibility="collapsed")
    with col_lp_btn:
        if st.button("💾 Salvar", key="salvar_lp_link", use_container_width=True):
            if lp_link.strip():
                st.session_state.dados['link_lp'] = lp_link.strip()
                st.success("Salvo!")
    if st.session_state.dados.get('link_lp'):
        st.caption(f"✅ Link salvo: {st.session_state.dados['link_lp']}")

    st.divider()
    if st.button("GERAR ANÚNCIO"):
        with st.spinner("Gerando anúncio com IA..."):
            st.session_state.dados['fb_copy'] = chamar_ia(prompt_fb(), system_fb())

    if 'fb_copy' in st.session_state.dados:
        bloco_conteudo('fb_copy', 'Anúncio', prompt_fb, system_fb)

        # ── MODIFICAÇÃO: segundo texto com instruções completas ──
        link_lp_atual = st.session_state.dados.get('link_lp','')
        if link_lp_atual:
            st.markdown(f"""<div style="background:#ECFDF5;border:1px solid #6EE7B7;border-radius:8px;padding:12px 16px;font-size:0.85em;color:#064E3B;margin-bottom:10px;">
            ✅ <strong>Link salvo:</strong> ao subir esse anúncio no Facebook Ads, coloque <strong>{link_lp_atual}</strong> como URL de destino do botão.
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""<div style="background:#FEF3C7;border:1px solid #FCD34D;border-radius:8px;padding:12px 16px;font-size:0.85em;color:#78350F;margin-bottom:10px;">
            ⚠️ <strong>Importante:</strong> ao subir esse anúncio no Facebook Ads, insira o link da sua landing page como URL de destino do botão CTA.
            </div>""", unsafe_allow_html=True)

        # ── NOVO: segundo bloco com workflow ChatGPT + Gamma ──
        st.markdown("""<div class="dica-ferramenta">
        <strong>📋 Próximo passo — publicar o anúncio:</strong><br><br>
        <strong>1. Copie o texto</strong> com o botão acima (Copiar como .txt)<br><br>
        <strong>2. Crie a imagem do anúncio no ChatGPT:</strong><br>
        &nbsp;&nbsp;&nbsp;• Acesse <a href="https://chat.openai.com" target="_blank" style="color:#92400E;">chat.openai.com</a> e abra uma conversa nova<br>
        &nbsp;&nbsp;&nbsp;• Cole o texto do anúncio e peça: <em>"Crie uma imagem para esse anúncio de Facebook Ads, formato quadrado 1080x1080px, visual chamativo e profissional"</em><br>
        &nbsp;&nbsp;&nbsp;• Baixe a imagem gerada<br><br>
        <strong>3. Suba no Facebook Ads Manager:</strong><br>
        &nbsp;&nbsp;&nbsp;• Cole o texto copiado no campo de texto principal<br>
        &nbsp;&nbsp;&nbsp;• Faça upload da imagem gerada pelo ChatGPT<br>
        &nbsp;&nbsp;&nbsp;• No campo de URL de destino, cole o link da sua landing page<br>
        &nbsp;&nbsp;&nbsp;• Escolha o botão CTA: <em>"Saiba mais"</em> ou <em>"Inscreva-se"</em>
        </div>""", unsafe_allow_html=True)

        # Tutorial Facebook
        st.divider()
        with st.expander("📘 TUTORIAL — Como anunciar no Facebook Ads passo a passo"):
            st.markdown("""
<div style="font-size:0.88em;line-height:1.8;color:#1E293B;">

<div style="background:#1877F2;color:white;border-radius:8px;padding:10px 16px;margin-bottom:16px;font-family:Rajdhani,sans-serif;font-size:1.05em;font-weight:700;">
📘 PASSO A PASSO — FACEBOOK ADS
</div>

**PASSO 1 — Acesse o Gerenciador de Anúncios**
Acesse: [business.facebook.com/adsmanager](https://business.facebook.com/adsmanager)

**PASSO 2 — Crie uma nova campanha**
Clique em **+ Criar** → Objetivo: **Tráfego** (direciona para sua LP)

**PASSO 3 — Configure o público**
- Localização: Brasil · Idade: seu público-alvo · Interesses: termos do nicho
- Tamanho ideal: 500 mil a 3 milhões

**PASSO 4 — Defina o orçamento**
- Orçamento diário: R$ 10 a R$ 20/dia

**PASSO 5 — Crie o anúncio**
- Formato: imagem única
- Texto principal: cole o texto gerado
- Imagem: use a gerada pelo ChatGPT (1080x1080px)
- URL de destino: link da sua landing page
- Botão CTA: "Saiba mais" ou "Inscreva-se"

**PASSO 6 — Publicar**
Revise todos os campos → **Publicar** → Facebook revisa em até 24h

**PASSO 7 — Métricas**
- CPL (Custo por Lead): meta até R$ 2,00
- CTR: meta acima de 1,5%
- CPC: meta abaixo de R$ 1,50

</div>
            """, unsafe_allow_html=True)

        if st.button("AVANÇAR →"): st.session_state.etapa = "Copy_LP"; st.rerun()

# ── LANDING PAGE ──────────────────────────────────────────────
elif st.session_state.etapa == "Copy_LP":
    barra_navegacao()
    st.title("🌐 LANDING PAGE")
    st.caption("Diagnóstico: mostra que o grupo vai descobrir o que está travando o resultado — a solução vem na venda.")

    st.markdown("#### 🔗 Link de convite do grupo (WhatsApp ou Telegram)")
    st.markdown("""<div style="background:#F0FDF4;border:1px solid #86EFAC;border-radius:8px;padding:10px 16px;margin-bottom:12px;color:#14532D;font-size:0.86em;line-height:1.6;">
    O botão CTA da landing page deve levar direto para o grupo.<br>
    Cole abaixo o link de convite do seu grupo.
    </div>""", unsafe_allow_html=True)
    col_gr, col_gr_btn = st.columns([4,1])
    with col_gr:
        grupo_link = st.text_input("Link de convite do grupo:", value=st.session_state.dados.get('link_grupo',''),
            placeholder="https://chat.whatsapp.com/...", label_visibility="collapsed")
    with col_gr_btn:
        if st.button("💾 Salvar", key="salvar_grupo_link", use_container_width=True):
            if grupo_link.strip():
                st.session_state.dados['link_grupo'] = grupo_link.strip()
                st.success("Salvo!")
    if st.session_state.dados.get('link_grupo'):
        st.caption(f"✅ Link salvo: {st.session_state.dados['link_grupo']}")

    st.divider()
    if st.button("GERAR LANDING PAGE"):
        with st.spinner("Gerando landing page com IA..."):
            st.session_state.dados['lp_copy'] = chamar_ia(prompt_lp(), system_lp())

    if 'lp_copy' in st.session_state.dados:
        bloco_conteudo('lp_copy', 'Landing Page', prompt_lp, system_lp)

        # ── MODIFICAÇÃO: segundo texto + instrução Gamma ──
        link_grupo_atual = st.session_state.dados.get('link_grupo','')
        if link_grupo_atual:
            st.markdown(f"""<div style="background:#ECFDF5;border:1px solid #6EE7B7;border-radius:8px;padding:12px 16px;font-size:0.85em;color:#064E3B;margin-bottom:10px;">
            ✅ <strong>Lembre-se:</strong> configure o botão CTA da sua landing page apontando para <strong>{link_grupo_atual}</strong>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""<div style="background:#FEF3C7;border:1px solid #FCD34D;border-radius:8px;padding:12px 16px;font-size:0.85em;color:#78350F;margin-bottom:10px;">
            ⚠️ <strong>Importante:</strong> configure o botão CTA da landing page apontando para o link de convite do seu grupo.
            </div>""", unsafe_allow_html=True)

        # ── NOVO: segundo bloco com workflow Gamma ──
        st.markdown(f"""<div class="dica-ferramenta">
        <strong>🌐 Próximo passo — transformar em site com Gamma AI:</strong><br><br>
        <strong>1. Copie o texto</strong> com o botão acima (Copiar como .txt)<br><br>
        <strong>2. Acesse o Gamma AI:</strong><br>
        &nbsp;&nbsp;&nbsp;• Abra <a href="https://gamma.app" target="_blank" style="color:#92400E;">gamma.app</a> e crie uma conta gratuita<br>
        &nbsp;&nbsp;&nbsp;• Clique em <strong>New → Page (site/landing page)</strong><br>
        &nbsp;&nbsp;&nbsp;• Cole o texto copiado no campo de geração<br>
        &nbsp;&nbsp;&nbsp;• Escolha o tema visual que combine com seu nicho<br>
        &nbsp;&nbsp;&nbsp;• Clique em <strong>Generate</strong> — o Gamma criará o site automaticamente<br><br>
        <strong>3. Configure o botão CTA:</strong><br>
        &nbsp;&nbsp;&nbsp;• No editor do Gamma, clique no botão CTA gerado<br>
        &nbsp;&nbsp;&nbsp;• Insira o link do grupo: <strong>{link_grupo_atual if link_grupo_atual else '[link do seu grupo aqui]'}</strong><br>
        &nbsp;&nbsp;&nbsp;• Clique em <strong>Publish</strong> para obter o link público do site<br><br>
        <strong>4. Use o link do site</strong> como URL de destino do seu anúncio no Facebook Ads
        </div>""", unsafe_allow_html=True)

        if st.button("AVANÇAR →"): st.session_state.etapa = "Mensagens_Grupo"; st.rerun()

# ── MENSAGENS DO GRUPO ────────────────────────────────────────
elif st.session_state.etapa == "Mensagens_Grupo":
    barra_navegacao()
    st.title("💬 MENSAGENS DO GRUPO")

    st.markdown("""<div class="preview-box">
    <strong>10 mensagens prontas — use uma por dia no grupo:</strong><br><br>
    📋 <strong>Descrição</strong> — texto da bio do grupo (configurar uma vez só)<br>
    💬 <strong>D-8</strong> — Boas-vindas automática ao entrar<br>
    📅 <strong>D-9</strong> — Abertura: cria expectativa para o diagnóstico do dia seguinte<br>
    🎯 <strong>D-10</strong> — Diagnóstico: pergunta interativa<br>
    🔥 <strong>D-11</strong> — 3 dicas surpreendentes sobre o nicho<br>
    📌 <strong>D-12</strong> — Atividade de observação (mantém mistério)<br>
    💡 <strong>D-13</strong> — Padrão oculto (sem revelar a causa)<br>
    ⏳ <strong>D-14</strong> — Véspera: texto fixo aprovado<br>
    🚀 <strong>Manhã</strong> — Lançamento: copy de venda com link<br>
    ⏰ <strong>Noite</strong> — Lembrete 19h: última chance
    </div>""", unsafe_allow_html=True)

    # ── AVISO REVISÃO BÔNUS ───────────────────────────────────
    bonus_resumo = st.session_state.dados.get('bonus_resumo','')
    if bonus_resumo:
        st.markdown(f"""<div style="background:#FEF9C3;border:1px solid #FDE047;border-radius:8px;padding:12px 16px;margin-bottom:8px;color:#713F12;font-size:0.88em;line-height:1.6;">
        ⚠️ <strong>Confira os nomes dos seus bônus antes de gerar:</strong><br>
        {bonus_resumo}<br>
        <em>Eles aparecerão na mensagem de venda. Se quiser alterar, volte em Bônus e regenere.</em>
        </div>""", unsafe_allow_html=True)

    st.markdown("""<div style="background:#FEF3C7;border:1px solid #FCD34D;border-radius:8px;padding:10px 16px;margin-bottom:8px;color:#78350F;font-size:0.85em;line-height:1.6;">
    ⚠️ <strong>Antes de enviar, revise:</strong>
    D-10 (diagnóstico) · D-11 (dicas) · D-12 (atividade) · D-13 (prova social) — gerados pela IA, os demais são texto fixo aprovado.
    </div>""", unsafe_allow_html=True)

    if not st.session_state.dados.get('whatsapp_contato'):
        st.warning("⚠️ Você não preencheu o WhatsApp de contato no formulário.")

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
        bloco_conteudo('msg_grupo', 'Mensagens', prompt_msg, system_msg)

        st.divider()
        st.markdown("#### 🔗 Inserir link da Monetizze")
        col_link, col_btn = st.columns([4, 1])
        with col_link:
            link_input = st.text_input(
                "Link:", value=st.session_state.dados.get('link_monetizze', ''),
                placeholder="https://go.monetizze.com.br/...", label_visibility="collapsed"
            )
        with col_btn:
            if st.button("✅ Aplicar", use_container_width=True):
                if link_input.strip():
                    st.session_state.dados['link_monetizze'] = link_input.strip()
                    st.session_state.dados['msg_grupo'] = st.session_state.dados['msg_grupo'].replace('[LINK MONETIZZE]', link_input.strip())
                    st.rerun()
                else:
                    st.warning("Cole o link antes de aplicar.")

        st.divider()

        # ── SALVAR NO COMPUTADOR ───────────────────────────────
        nome_projeto = st.session_state.dados.get('nome_eb', 'meu_projeto')
        nome_arquivo = nome_projeto.replace(' ', '_').lower()
        json_projeto = gerar_json_projeto(st.session_state.dados)
        salvar_projeto(nome_projeto, st.session_state.dados)

        st.markdown("""<div style="background:#F0FDF4;border:2px solid #22C55E;border-radius:12px;padding:18px 20px;margin-bottom:14px;color:#14532D;font-size:0.92em;line-height:1.8;">
        💾 <strong>Projeto pronto! Salve agora no seu computador.</strong><br>
        <span style="font-size:0.88em;">Clique no botão abaixo para baixar o arquivo. Da próxima vez que acessar o app, faça o upload do arquivo em <strong>📂 Meus Projetos → Carregar projeto (.json)</strong> e tudo estará lá do jeito que você deixou.</span>
        </div>""", unsafe_allow_html=True)

        st.markdown('<div class="btn-verde15">', unsafe_allow_html=True)
        st.download_button(
            label="💾 SALVAR PROJETO NO COMPUTADOR (.json)",
            data=json_projeto,
            file_name=f"{nome_arquivo}_nexus.json",
            mime="application/json",
            use_container_width=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)
        st.caption("📌 Guarde esse arquivo em um lugar seguro — ele contém todo o seu projeto de lançamento.")
        st.session_state.etapa = "Visualizacao"

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

    # ── SALVAR LOCAL (botão prominente no topo da visualização) ──
    nome_arquivo = nome_projeto.replace(' ', '_').lower()
    json_projeto = gerar_json_projeto(d)

    # ── BOTÃO PRINCIPAL — SALVAR NO COMPUTADOR ────────────────
    st.markdown("""<div style="background:#F0FDF4;border:2px solid #22C55E;border-radius:12px;padding:16px 20px;margin-bottom:14px;color:#14532D;font-size:0.9em;line-height:1.7;">
    💾 <strong>Salve seu projeto no computador</strong> — é a forma mais segura de guardar tudo.<br>
    <span style="font-size:0.88em;">Da próxima vez que acessar, vá em <strong>📂 Meus Projetos → Carregar projeto (.json)</strong> e continue de onde parou.</span>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="btn-verde15">', unsafe_allow_html=True)
    st.download_button(
        label="💾 SALVAR PROJETO NO COMPUTADOR (.json)",
        data=json_projeto,
        file_name=f"{nome_arquivo}_nexus.json",
        mime="application/json",
        use_container_width=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="btn-secundario">', unsafe_allow_html=True)
    st.download_button(
        label="⬇️ Baixar projeto completo em texto (.txt)",
        data=texto_completo,
        file_name=f"{nome_arquivo}_lancamento.txt",
        mime="text/plain",
        use_container_width=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # ── CARREGAR PROJETO LOCAL ────────────────────────────────
    with st.expander("📂 Meus Projetos — Carregar projeto (.json)"):
        st.caption("Selecione o arquivo .json salvo anteriormente para continuar de onde parou.")
        arquivo_json = st.file_uploader("Selecione o arquivo .json do projeto:", type=["json"], key="upload_json")
        if arquivo_json is not None:
            try:
                dados_importados = json.load(arquivo_json)
                st.success(f"✅ Arquivo reconhecido: **{dados_importados.get('nome_eb', arquivo_json.name)}**")
                if st.button("✅ Carregar este projeto"):
                    st.session_state.dados = dados_importados
                    nome_imp = dados_importados.get('nome_eb', arquivo_json.name)
                    salvar_projeto(nome_imp, dados_importados)
                    st.rerun()
            except Exception as e:
                st.error(f"Erro ao ler o arquivo: {e}")

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

    # ── AGENDADOR DE MENSAGENS ───────────────────────────────
    st.divider()
    with st.expander("📅 AGENDADOR — Calendário de envio das mensagens"):
        data_lancto = d.get('data_lancto')

        if not data_lancto:
            st.warning("Defina a data de lançamento no formulário para usar o agendador.")
        elif not d.get('msg_grupo'):
            st.info("Gere as mensagens primeiro para usar o agendador.")
        else:
            AGENDA_DEF = [
                {"chave": "DESCRICAO_GRUPO", "label": "Descrição (bio)",      "emoji": "📋", "offset": -15, "hora_pad": "08:00", "cor": "#64748B"},
                {"chave": "BOAS_VINDAS",     "label": "Boas-vindas",          "emoji": "💬", "offset": -8,  "hora_pad": "08:00", "cor": "#0EA5E9"},
                {"chave": "DIA_7",           "label": "D-9 Abertura",         "emoji": "📅", "offset": -7,  "hora_pad": "08:00", "cor": "#0EA5E9"},
                {"chave": "DIA_6",           "label": "D-10 Enquete",         "emoji": "🎯", "offset": -6,  "hora_pad": "08:00", "cor": "#8B5CF6"},
                {"chave": "DIA_5",           "label": "D-11 Dica",            "emoji": "🔥", "offset": -5,  "hora_pad": "08:00", "cor": "#8B5CF6"},
                {"chave": "DIA_4",           "label": "D-12 Atividade",       "emoji": "📌", "offset": -4,  "hora_pad": "08:00", "cor": "#8B5CF6"},
                {"chave": "DIA_3",           "label": "D-13 Prova social",    "emoji": "💡", "offset": -3,  "hora_pad": "08:00", "cor": "#8B5CF6"},
                {"chave": "VESPERA",         "label": "D-14 Véspera",         "emoji": "⏳", "offset": -1,  "hora_pad": "08:00", "cor": "#F59E0B"},
                {"chave": "VENDA_MANHA",     "label": "Lançamento manhã",     "emoji": "🚀", "offset":  0,  "hora_pad": "08:00", "cor": "#22C55E"},
                {"chave": "VENDA_NOITE",     "label": "Lançamento noite",     "emoji": "⏰", "offset":  0,  "hora_pad": "19:00", "cor": "#22C55E"},
            ]

            secoes_map = {s['chave']: limpar_html(s['conteudo']) for s in parsear_mensagens(d['msg_grupo'])}
            horas_config = st.session_state.dados.get('agenda_horas', {})

            st.markdown("#### Horários de envio")
            for item in AGENDA_DEF:
                chave = item['chave']
                data_msg = data_lancto + timedelta(days=item['offset'])
                data_str = data_msg.strftime('%d/%m')
                col_label, col_hora = st.columns([4, 1])
                with col_label:
                    st.markdown(
                        f"<div style='padding:5px 0;font-size:0.87em;color:#1E293B;'>"
                        f"<span style='display:inline-block;width:14px;height:14px;"
                        f"border-radius:3px;background:{item['cor']};margin-right:6px;"
                        f"vertical-align:middle;'></span>"
                        f"<span style='color:#64748B;font-size:0.8em;font-weight:600;"
                        f"margin-right:6px;'>{data_str}</span>"
                        f"{item['emoji']} {item['label']}</div>",
                        unsafe_allow_html=True
                    )
                with col_hora:
                    hora_val = horas_config.get(chave, item['hora_pad'])
                    hora_input = st.text_input(
                        "h", value=hora_val, key=f"hora_{chave}",
                        label_visibility="collapsed", placeholder="HH:MM"
                    )
                    horas_config[chave] = hora_input

            st.session_state.dados['agenda_horas'] = horas_config

            if st.button("📅 EXPORTAR CALENDÁRIO (.ics)", use_container_width=True):
                eventos = []
                for item in AGENDA_DEF:
                    chave    = item['chave']
                    data_msg = data_lancto + timedelta(days=item['offset'])
                    hora     = horas_config.get(chave, item['hora_pad'])
                    texto    = secoes_map.get(chave, '')
                    if not texto: continue
                    eventos.append({
                        'chave':     chave,
                        'titulo':    f"[Nexus] {item['emoji']} {item['label']}",
                        'data':      data_msg,
                        'hora':      hora,
                        'descricao': texto,
                    })
                ics_content = gerar_ics(eventos)
                st.download_button(
                    label="⬇️ Baixar arquivo .ics",
                    data=ics_content.encode('utf-8'),
                    file_name=f"lancamento_{d.get('nome_eb','').replace(' ','_')}.ics",
                    mime="text/calendar",
                    use_container_width=True,
                )
                st.success("Pronto! Importe no Google Calendar, Apple Calendar ou Outlook.")

            st.markdown("""<div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;padding:10px 14px;margin-top:10px;color:#64748B;font-size:0.78em;line-height:1.7;">
            💡 <strong>Como importar:</strong>
            Google Calendar → Configurações → Importar → selecione o .ics &nbsp;|&nbsp;
            Apple Calendar → Arquivo → Importar &nbsp;|&nbsp;
            Outlook → Arquivo → Abrir e Exportar → Importar
            </div>""", unsafe_allow_html=True)

    # ── DICA MESTRE ──────────────────────────────────────────
    st.divider()
    with st.expander("🧠 DICA MESTRE — O QUE FAZER DEPOIS DO LANÇAMENTO"):
        st.markdown("""<div style="background:#F0FDF4;border:2px solid #22C55E;border-radius:12px;padding:22px 26px;color:#14532D;line-height:1.7;font-size:0.92em;">
        <strong style="font-size:1.05em;">Não apague esse grupo.</strong><br><br>
        Aqui dentro, você construiu algo extremamente valioso: atenção e interesse de pessoas reais.
        Esse grupo é um ativo. Se bem utilizado, ele pode gerar novos resultados sem investimento em tráfego.<br><br>
        <strong>Mas existe um ponto importante: evite excesso.</strong><br>
        O ideal é realizar novos lançamentos com equilíbrio — aproximadamente 1 vez por mês.
        </div>""", unsafe_allow_html=True)

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
                ("Hoje","Baixe o projeto completo (.json e .txt)"),
                ("Hoje","Cadastre o e-book + 3 bônus na Monetizze — configure o checkout"),
                (f"Hoje",f"Preço: R${d.get('preco',47)} — salve o link de venda"),
                ("Hoje","Crie o grupo: 'Programa [X] Dias para [Objetivo]'"),
                ("Hoje","Cole a DESCRIÇÃO DO GRUPO no campo de informações do WhatsApp/Telegram"),
                ("Hoje","Configure a mensagem de BOAS-VINDAS automática ao entrar"),
                ("Hoje","Gere a imagem do anúncio no ChatGPT e suba no Facebook Ads"),
                ("Hoje","Configure a LANDING PAGE no Gamma AI com CTA apontando para o grupo"),
            ]},
            {"fase":"FASE 2 — SEMANA 1: Encher o grupo","cor":"#8B5CF6","items":[
                ("Dias 1 a 8","Anúncios rodando — objetivo: 500 a 1.000 pessoas no grupo"),
                ("Diariamente","Monitore custo por lead — meta: até R$2,00 por pessoa"),
            ]},
            {"fase":"FASE 3 — SEMANA 2: Aquecimento","cor":"#059669","items":[
                (f"{d7} — D-7","Envie: Abertura do programa"),
                (f"{d6} — D-6","Envie: Enquete — respostas no WhatsApp de contato"),
                (f"{d5} — D-5","Envie: Dica prática"),
                (f"{d4} — D-4","Envie: Atividade rápida"),
                (f"{d3} — D-3","Envie: Relato de resultado"),
                (f"{dm1} — D-1","Envie: Véspera da venda"),
                (f"{dm1}","Confirme se o link da Monetizze está funcionando"),
            ]},
            {"fase":f"FASE 4 — {dlf}: Dia da venda","cor":"#22C55E","items":[
                (f"{dlf} — manhã","Envie a mensagem de lançamento com o link"),
                (f"{dlf}","Fique disponível no WhatsApp para responder dúvidas"),
                (f"{dlf} — 19h","Envie o lembrete noturno"),
            ]},
            {"fase":"FASE 5 — PÓS-LANÇAMENTO","cor":"#64748B","items":[
                ("Após","Registre: pessoas no grupo, vendas, taxa de conversão, ROI"),
                ("Após","Verifique na Monetizze se os acessos foram entregues"),
                ("Próximo mês","Use o mesmo grupo para relançar"),
            ]},
        ]
        for fase in fases:
            st.markdown(f'<div style="margin:18px 0 8px 0;padding:8px 14px;background:{fase["cor"]};border-radius:8px;color:white;font-weight:600;font-size:0.85em;letter-spacing:0.5px">{fase["fase"]}</div>', unsafe_allow_html=True)
            for quando, acao in fase['items']:
                st.markdown(f'<div class="checklist-item"><div style="width:10px;height:10px;border-radius:50%;background:{fase["cor"]};margin-top:5px;flex-shrink:0"></div><div><div style="font-size:0.72em;color:#64748B;font-weight:600;text-transform:uppercase;letter-spacing:0.5px">{quando}</div><div style="font-size:0.92em;color:#1E293B">{acao}</div></div></div>', unsafe_allow_html=True)

    st.divider()
    with st.expander("📈 MÉTRICAS PÓS-LANÇAMENTO"):
        m = st.session_state.dados.get('metricas_pos', {})
        col1, col2, col3 = st.columns(3)
        with col1:
            m['grupo_pessoas']  = st.number_input("Pessoas no grupo", min_value=0, value=int(m.get('grupo_pessoas',0)), key="mp1")
            m['cliques_link']   = st.number_input("Cliques no link de venda", min_value=0, value=int(m.get('cliques_link',0)), key="mp2")
        with col2:
            m['vendas_reais']   = st.number_input("Vendas realizadas", min_value=0, value=int(m.get('vendas_reais',0)), key="mp3")
            m['custo_trafego']  = st.number_input("Custo de tráfego (R$)", min_value=0.0, value=float(m.get('custo_trafego',0)), key="mp4")
        with col3:
            m['reembolsos']     = st.number_input("Reembolsos / estornos", min_value=0, value=int(m.get('reembolsos',0)), key="mp5")
            m['preco_real']     = st.number_input("Preço vendido (R$)", min_value=0.0, value=float(m.get('preco_real', d.get('preco',47))), key="mp6")

        st.session_state.dados['metricas_pos'] = m

        vendas_liq   = max(0, int(m.get('vendas_reais',0)) - int(m.get('reembolsos',0)))
        faturamento  = vendas_liq * float(m.get('preco_real', d.get('preco',47)))
        custo        = float(m.get('custo_trafego',0))
        lucro        = faturamento - custo
        grupo        = int(m.get('grupo_pessoas',1)) or 1
        tx_conv      = (vendas_liq / grupo * 100) if grupo else 0
        roi          = ((lucro / custo) * 100) if custo else 0
        cpl          = (custo / grupo) if grupo else 0

        if vendas_liq > 0 or faturamento > 0:
            r1, r2, r3, r4 = st.columns(4)
            r1.metric("Faturamento líquido", f"R${faturamento:,.0f}".replace(',','.'))
            r2.metric("Lucro real", f"R${lucro:,.0f}".replace(',','.'))
            r3.metric("ROI", f"{roi:.0f}%")
            r4.metric("CPL", f"R${cpl:.2f}")
            if tx_conv < 1:
                st.info("⚠️ Abaixo de 1% — revise a mensagem de venda e o aquecimento.")
            elif tx_conv < 3:
                st.info("✅ Entre 1-3% — resultado esperado para primeiro lançamento.")
            else:
                st.info("🔥 Acima de 3% — excelente! Escale o tráfego no próximo.")

    st.divider()
    with st.expander("📊 CALCULADORA PRÉ-LANÇAMENTO"):
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

    st.divider()
    st.markdown("### 🤖 Launcerbot")
    if st.session_state.chat_hist:
        for q, r in st.session_state.chat_hist:
            st.markdown(f"**Você:** {q}")
            st.markdown(f"<div class='chat-bubble'>{r}</div>", unsafe_allow_html=True)

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

# ── LANÇAMENTO DE VIDEOAULAS ─────────────────────────────────

elif st.session_state.etapa == "Video_Formulario":
    st.title("🎬 LANÇAMENTO DE VIDEOAULAS")
    st.markdown("""<div class="preview-box">
    <strong>Método CPL — Como funciona:</strong><br>
    📣 Pré-pré-lançamento → 🎬 CPL 1 (Oportunidade) → 🎬 CPL 2 (Transformação) →
    🎬 CPL 3 (Objeções) → 🛒 Abertura de carrinho → ⏰ Fechamento com urgência
    </div>""", unsafe_allow_html=True)
    d = st.session_state.dados

    st.markdown("#### Dados do produto")
    d['v_nicho']    = st.text_input("Nicho:", value=d.get('v_nicho',''))
    d['v_publico']  = st.text_input("Público-alvo:", value=d.get('v_publico',''))
    d['v_produto']  = st.text_input("Nome do curso/videoaulas:", value=d.get('v_produto',''))
    d['v_dor']      = st.text_input("Principal dor que resolve:", value=d.get('v_dor',''))
    d['v_promessa'] = st.text_input("Promessa de transformação:", value=d.get('v_promessa',''))
    d['v_preco']    = st.number_input("Preço do curso (R$):", min_value=47, max_value=9997, value=int(d.get('v_preco',497)), step=10)
    d['v_garantia'] = st.selectbox("Garantia:", ["7 dias","14 dias","30 dias"], index=["7 dias","14 dias","30 dias"].index(d.get('v_garantia','7 dias')))
    d['v_bonus']    = st.text_input("Bônus inclusos (separe por vírgula):", value=d.get('v_bonus',''))
    d['v_autor']    = st.text_input("Seu nome:", value=d.get('v_autor',''))
    d['v_cred']     = st.text_area("Sua credencial/experiência:", value=d.get('v_cred',''))

    st.divider()
    st.markdown("#### Datas do lançamento")
    col1, col2 = st.columns(2)
    with col1:
        d['v_data_cpl1'] = st.date_input("CPL 1 — 1º vídeo:", value=d.get('v_data_cpl1', date.today() + timedelta(days=7)))
        d['v_data_cpl2'] = st.date_input("CPL 2 — 2º vídeo:", value=d.get('v_data_cpl2', date.today() + timedelta(days=11)))
        d['v_data_cpl3'] = st.date_input("CPL 3 — 3º vídeo:", value=d.get('v_data_cpl3', date.today() + timedelta(days=15)))
    with col2:
        d['v_data_abertura'] = st.date_input("Abertura do carrinho:", value=d.get('v_data_abertura', date.today() + timedelta(days=18)))
        d['v_data_fechamento'] = st.date_input("Fechamento do carrinho:", value=d.get('v_data_fechamento', date.today() + timedelta(days=21)))

    st.divider()
    if st.button("AVANÇAR → GERAR LANÇAMENTO COMPLETO"):
        if not d.get('v_nicho') or not d.get('v_produto'):
            st.warning("Preencha pelo menos nicho e nome do produto.")
        else:
            st.session_state.etapa = "Video_Gerar"; st.rerun()

elif st.session_state.etapa == "Video_Gerar":
    st.title("🎬 GERANDO SEU LANÇAMENTO DE VIDEOAULAS")
    barra_video = {"Video_Formulario":"1. Dados","Video_Gerar":"2. Conteúdo","Video_Final":"3. Projeto"}
    badges = ""
    for k,v in barra_video.items():
        cls = "ativo" if k == "Video_Gerar" else ""
        badges += f'<span class="step-badge {cls}">{v}</span>'
    st.markdown(f'<div class="step-indicator">{badges}</div>', unsafe_allow_html=True)

    d = st.session_state.dados
    n = d.get('v_nicho',''); pub = d.get('v_publico',''); prod = d.get('v_produto','')
    dor = d.get('v_dor',''); prom = d.get('v_promessa',''); preco = d.get('v_preco',497)
    garantia = d.get('v_garantia','7 dias'); bonus = d.get('v_bonus','')
    autor = d.get('v_autor',''); cred = d.get('v_cred','')
    d1 = d.get('v_data_cpl1', date.today()).strftime('%d/%m')
    d2 = d.get('v_data_cpl2', date.today()).strftime('%d/%m')
    d3 = d.get('v_data_cpl3', date.today()).strftime('%d/%m')
    da = d.get('v_data_abertura', date.today()).strftime('%d/%m/%Y')
    df = d.get('v_data_fechamento', date.today()).strftime('%d/%m/%Y')

    # PRÉ-PRÉ-LANÇAMENTO
    if not d.get('v_pre_pre'):
        if st.button("🔥 1. GERAR PRÉ-PRÉ-LANÇAMENTO (stories + posts de bastidores)"):
            with st.spinner("Gerando conteúdo de antecipação..."):
                p = (f"Crie o conteúdo de pré-pré-lançamento para o curso '{prod}' sobre {n}.\n"
                     f"Público: {pub}. Dor: {dor}.\n\n"
                     f"Gere:\n"
                     f"1. 7 STORIES progressivos (um por dia) que criam antecipação crescente.\n\n"
                     f"2. 3 POSTS para feed com bastidores.\n\n"
                     f"REGRAS: Gatilhos de antecipação, autoridade e curiosidade. Zero venda.")
                d['v_pre_pre'] = chamar_ia(p, "Você é especialista em lançamentos digitais e copywriting.")
                st.rerun()
    else:
        with st.expander("🔥 Pré-pré-lançamento — Stories e bastidores", expanded=True):
            st.markdown(f"<div class='caixa-texto'>{normalizar_markdown(d['v_pre_pre'])}</div>", unsafe_allow_html=True)
            col1,col2,col3 = st.columns(3)
            col1.download_button("📋 Copiar", data=limpar_html(d['v_pre_pre']), file_name="pre_pre.txt", mime="text/plain", key="dl_prepre")
            if col2.button("🔄 Regenerar", key="rg_prepre"): d.pop('v_pre_pre'); st.rerun()
            if col3.button("✍️ Corrigir gramática", key="gr_prepre"):
                with st.spinner("Revisando..."): d['v_pre_pre'] = corrigir_texto(limpar_html(d['v_pre_pre'])); st.rerun()

    # CPL 1
    if d.get('v_pre_pre') and not d.get('v_cpl1'):
        if st.button(f"🎬 2. GERAR CPL 1 — Oportunidade ({d1})"):
            with st.spinner("Gerando roteiro CPL 1..."):
                p = (f"Crie o CPL 1 — OPORTUNIDADE — para o curso '{prod}' sobre {n}.\n"
                     f"Público: {pub}. Dor: {dor}. Promessa: {prom}.\n\n"
                     f"ROTEIRO DO VÍDEO CPL 1 (8-12 min):\n"
                     f"- Hook · Problema · Oportunidade · Prova rápida · Teaser CPL2 · CTA\n\n"
                     f"SEQUÊNCIA DE WHATSAPP PÓS-CPL1 (3 mensagens).")
                d['v_cpl1'] = chamar_ia(p, "Você é especialista em lançamentos CPL.")
                st.rerun()
    elif d.get('v_cpl1'):
        with st.expander(f"🎬 CPL 1 — Oportunidade ({d1})", expanded=True):
            st.markdown(f"<div class='caixa-texto'>{normalizar_markdown(d['v_cpl1'])}</div>", unsafe_allow_html=True)
            col1,col2,col3 = st.columns(3)
            col1.download_button("📋 Copiar", data=limpar_html(d['v_cpl1']), file_name="cpl1.txt", mime="text/plain", key="dl_cpl1")
            if col2.button("🔄 Regenerar", key="rg_cpl1"): d.pop('v_cpl1'); st.rerun()
            if col3.button("✍️ Corrigir gramática", key="gr_cpl1"):
                with st.spinner("Revisando..."): d['v_cpl1'] = corrigir_texto(limpar_html(d['v_cpl1'])); st.rerun()

    # CPL 2
    if d.get('v_cpl1') and not d.get('v_cpl2'):
        if st.button(f"🎬 3. GERAR CPL 2 — Transformação ({d2})"):
            with st.spinner("Gerando roteiro CPL 2..."):
                p = (f"Crie o CPL 2 — TRANSFORMAÇÃO — para '{prod}' sobre {n}.\n"
                     f"Público: {pub}. Credencial: {cred}.\n\n"
                     f"ROTEIRO (8-12 min): Recap · Prova social · O método · Credencial do autor · Teaser CPL3 · CTA\n\n"
                     f"SEQUÊNCIA DE WHATSAPP PÓS-CPL2 (3 mensagens).")
                d['v_cpl2'] = chamar_ia(p, "Você é especialista em lançamentos CPL.")
                st.rerun()
    elif d.get('v_cpl2'):
        with st.expander(f"🎬 CPL 2 — Transformação ({d2})", expanded=True):
            st.markdown(f"<div class='caixa-texto'>{normalizar_markdown(d['v_cpl2'])}</div>", unsafe_allow_html=True)
            col1,col2,col3 = st.columns(3)
            col1.download_button("📋 Copiar", data=limpar_html(d['v_cpl2']), file_name="cpl2.txt", mime="text/plain", key="dl_cpl2")
            if col2.button("🔄 Regenerar", key="rg_cpl2"): d.pop('v_cpl2'); st.rerun()
            if col3.button("✍️ Corrigir gramática", key="gr_cpl2"):
                with st.spinner("Revisando..."): d['v_cpl2'] = corrigir_texto(limpar_html(d['v_cpl2'])); st.rerun()

    # CPL 3
    if d.get('v_cpl2') and not d.get('v_cpl3'):
        if st.button(f"🎬 4. GERAR CPL 3 — Quebra de objeções ({d3})"):
            with st.spinner("Gerando roteiro CPL 3..."):
                p = (f"Crie o CPL 3 — QUEBRA DE OBJEÇÕES — para '{prod}' sobre {n}.\n"
                     f"Preço: R${preco}. Data abertura: {da}.\n\n"
                     f"ROTEIRO (10-15 min): Abertura forte · 5 objeções respondidas · FAQ · Antecipação · CTA\n\n"
                     f"SEQUÊNCIA DE WHATSAPP (3 mensagens de antecipação pré-abertura).")
                d['v_cpl3'] = chamar_ia(p, "Você é especialista em quebra de objeções.")
                st.rerun()
    elif d.get('v_cpl3'):
        with st.expander(f"🎬 CPL 3 — Quebra de objeções ({d3})", expanded=True):
            st.markdown(f"<div class='caixa-texto'>{normalizar_markdown(d['v_cpl3'])}</div>", unsafe_allow_html=True)
            col1,col2,col3 = st.columns(3)
            col1.download_button("📋 Copiar", data=limpar_html(d['v_cpl3']), file_name="cpl3.txt", mime="text/plain", key="dl_cpl3")
            if col2.button("🔄 Regenerar", key="rg_cpl3"): d.pop('v_cpl3'); st.rerun()
            if col3.button("✍️ Corrigir gramática", key="gr_cpl3"):
                with st.spinner("Revisando..."): d['v_cpl3'] = corrigir_texto(limpar_html(d['v_cpl3'])); st.rerun()

    # ABERTURA DE CARRINHO
    if d.get('v_cpl3') and not d.get('v_abertura'):
        if st.button(f"🛒 5. GERAR ABERTURA DE CARRINHO ({da})"):
            with st.spinner("Gerando copy de abertura..."):
                bonus_lista = '\n'.join([f'🎁 {b.strip()}' for b in bonus.split(',') if b.strip()]) if bonus else '🎁 Bônus exclusivos'
                p = (f"Crie a copy completa de ABERTURA DE CARRINHO para '{prod}' sobre {n}.\n"
                     f"Preço: R${preco}. Garantia: {garantia}.\n\n"
                     f"Gere: E-mail de abertura · Mensagem WhatsApp manhã · Post feed · Story (3 frames)\n\n"
                     f"Bônus:\n{bonus_lista}")
                d['v_abertura'] = chamar_ia(p, "Você é especialista em copy de abertura de carrinho.")
                st.rerun()
    elif d.get('v_abertura'):
        with st.expander(f"🛒 Abertura de carrinho ({da})", expanded=True):
            st.markdown(f"<div class='caixa-texto'>{normalizar_markdown(d['v_abertura'])}</div>", unsafe_allow_html=True)
            col1,col2,col3 = st.columns(3)
            col1.download_button("📋 Copiar", data=limpar_html(d['v_abertura']), file_name="abertura_carrinho.txt", mime="text/plain", key="dl_aber")
            if col2.button("🔄 Regenerar", key="rg_aber"): d.pop('v_abertura'); st.rerun()
            if col3.button("✍️ Corrigir gramática", key="gr_aber"):
                with st.spinner("Revisando..."): d['v_abertura'] = corrigir_texto(limpar_html(d['v_abertura'])); st.rerun()

    # FECHAMENTO
    if d.get('v_abertura') and not d.get('v_fechamento'):
        if st.button(f"⏰ 6. GERAR FECHAMENTO — Urgência máxima ({df})"):
            with st.spinner("Gerando copy de fechamento..."):
                p = (f"Crie a copy de FECHAMENTO DE CARRINHO para '{prod}' sobre {n}.\n"
                     f"Carrinho fecha em {df}. Preço: R${preco}. Garantia: {garantia}.\n\n"
                     f"Gere: WhatsApp 24h antes · WhatsApp manhã do fechamento · WhatsApp 2h antes · E-mail última chance · Story contagem regressiva")
                d['v_fechamento'] = chamar_ia(p, "Você é especialista em copy de fechamento e urgência.")
                st.rerun()
    elif d.get('v_fechamento'):
        with st.expander(f"⏰ Fechamento — Urgência máxima ({df})", expanded=True):
            st.markdown(f"<div class='caixa-texto'>{normalizar_markdown(d['v_fechamento'])}</div>", unsafe_allow_html=True)
            col1,col2,col3 = st.columns(3)
            col1.download_button("📋 Copiar", data=limpar_html(d['v_fechamento']), file_name="fechamento.txt", mime="text/plain", key="dl_fech")
            if col2.button("🔄 Regenerar", key="rg_fech"): d.pop('v_fechamento'); st.rerun()
            if col3.button("✍️ Corrigir gramática", key="gr_fech"):
                with st.spinner("Revisando..."): d['v_fechamento'] = corrigir_texto(limpar_html(d['v_fechamento'])); st.rerun()

    if d.get('v_fechamento'):
        st.divider()
        st.success("✅ Lançamento CPL completo gerado!")
        nome_v = d.get('v_produto','curso').replace(' ','_')
        texto_v = f"""NEXUS LAUNCHER — LANÇAMENTO DE VIDEOAULAS
{'='*50}
CURSO: {d.get('v_produto','')}
NICHO: {d.get('v_nicho','')}
{'='*50}

PRÉ-PRÉ-LANÇAMENTO\n{'-'*40}\n{limpar_html(d.get('v_pre_pre',''))}
CPL 1\n{'-'*40}\n{limpar_html(d.get('v_cpl1',''))}
CPL 2\n{'-'*40}\n{limpar_html(d.get('v_cpl2',''))}
CPL 3\n{'-'*40}\n{limpar_html(d.get('v_cpl3',''))}
ABERTURA\n{'-'*40}\n{limpar_html(d.get('v_abertura',''))}
FECHAMENTO\n{'-'*40}\n{limpar_html(d.get('v_fechamento',''))}"""

        col_txt_v, col_json_v = st.columns(2)
        with col_txt_v:
            st.markdown('<div class="btn-verde">', unsafe_allow_html=True)
            st.download_button("⬇️ BAIXAR COMPLETO (.txt)", data=texto_v,
                file_name=f"{nome_v}_lancamento_video.txt", mime="text/plain", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col_json_v:
            st.markdown('<div class="btn-verde">', unsafe_allow_html=True)
            st.download_button("💾 SALVAR NO COMPUTADOR (.json)", data=gerar_json_projeto(d),
                file_name=f"{nome_v}_nexus.json", mime="application/json", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Agendador CPL
        st.divider()
        with st.expander("📅 AGENDADOR CPL — Calendário de envio"):
            CPL_AGENDA = [
                {"chave":"v_pre_pre",    "label":"🔥 Pré-pré-lançamento",   "data_key":"v_data_cpl1",      "offset":-7, "hora":"09:00", "cor":"#64748B"},
                {"chave":"v_cpl1",       "label":"🎬 CPL 1 — Oportunidade", "data_key":"v_data_cpl1",      "offset":0,  "hora":"10:00", "cor":"#3B82F6"},
                {"chave":"v_cpl2",       "label":"🎬 CPL 2 — Transformação","data_key":"v_data_cpl2",      "offset":0,  "hora":"10:00", "cor":"#8B5CF6"},
                {"chave":"v_cpl3",       "label":"🎬 CPL 3 — Objeções",     "data_key":"v_data_cpl3",      "offset":0,  "hora":"10:00", "cor":"#F59E0B"},
                {"chave":"v_abertura",   "label":"🛒 Abertura do carrinho", "data_key":"v_data_abertura",  "offset":0,  "hora":"08:00", "cor":"#22C55E"},
                {"chave":"v_fechamento", "label":"⏰ Fechamento",            "data_key":"v_data_fechamento","offset":0,  "hora":"08:00", "cor":"#EF4444"},
            ]
            horas_cpl = d.get('agenda_horas_cpl', {})
            for item in CPL_AGENDA:
                data_base = d.get(item["data_key"], date.today())
                data_ev = data_base + timedelta(days=item["offset"])
                col_l, col_h = st.columns([4,1])
                with col_l:
                    st.markdown(
                        f"<div style='padding:5px 0;font-size:0.87em;'>"
                        f"<span style='display:inline-block;width:12px;height:12px;border-radius:3px;"
                        f"background:{item['cor']};margin-right:6px;vertical-align:middle;'></span>"
                        f"<span style='color:#64748B;font-size:0.8em;font-weight:600;margin-right:6px;'>{data_ev.strftime('%d/%m')}</span>"
                        f"{item['label']}</div>", unsafe_allow_html=True)
                with col_h:
                    horas_cpl[item["chave"]] = st.text_input("h", value=horas_cpl.get(item["chave"], item["hora"]),
                        key=f"hcpl_{item['chave']}", label_visibility="collapsed")
            d['agenda_horas_cpl'] = horas_cpl

            if st.button("📅 EXPORTAR CALENDÁRIO CPL (.ics)", use_container_width=True):
                eventos_cpl = []
                for item in CPL_AGENDA:
                    data_base = d.get(item["data_key"], date.today())
                    data_ev = data_base + timedelta(days=item["offset"])
                    texto = limpar_html(d.get(item["chave"], ""))
                    if not texto: continue
                    eventos_cpl.append({"chave": item["chave"], "titulo": f"[Nexus CPL] {item['label']}",
                        "data": data_ev, "hora": horas_cpl.get(item["chave"], item["hora"]), "descricao": texto})
                ics = gerar_ics(eventos_cpl)
                st.download_button("⬇️ Baixar .ics", data=ics.encode('utf-8'),
                    file_name=f"{nome_v}_cpl.ics", mime="text/calendar", use_container_width=True)
                st.success("Importe no Google Calendar, Apple Calendar ou Outlook.")

        if st.button("🔙 Voltar à escolha de lançamento"):
            st.session_state.etapa = "Escolha_Tipo"; st.rerun()


# --- RODAPÉ ---
st.markdown("<div class='footer'>© 2026 Nexus Launcher – Lançamento digital inteligente</div>", unsafe_allow_html=True)
