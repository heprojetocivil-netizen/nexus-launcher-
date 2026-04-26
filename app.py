import streamlit as st
from groq import Groq
from datetime import timedelta, date, datetime
import re
import json
import urllib.request

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
    .btn-laranja>button { background-color: #f97316 !important; height: 3.5em !important; }
    .btn-laranja>button:hover { background-color: #ea580c !important; }

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

    /* PREVIEW WHATSAPP */
    .wpp-screen {
        background: #E5DDD5;
        background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23c8bdb1' fill-opacity='0.3'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        border-radius: 12px; padding: 16px; margin: 10px 0 20px 0;
    }
    .wpp-header {
        background: #075E54; color: white; border-radius: 8px 8px 0 0;
        padding: 10px 14px; display: flex; align-items: center; gap: 10px;
        font-family: 'Inter', sans-serif; font-size: 0.9em; font-weight: 600;
        margin-bottom: 0;
    }
    .wpp-avatar {
        width: 36px; height: 36px; background: #25D366; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.1em; flex-shrink: 0;
    }
    .wpp-bubble {
        background: #FFFFFF; border-radius: 0 8px 8px 8px;
        padding: 10px 14px 22px 14px; margin: 6px 40px 0 0;
        position: relative; box-shadow: 0 1px 2px rgba(0,0,0,0.15);
        font-size: 0.88em; line-height: 1.6; color: #1E293B;
        white-space: pre-wrap; font-family: 'Inter', sans-serif;
        max-width: 85%;
    }
    .wpp-bubble::before {
        content: ''; position: absolute; top: 0; left: -8px;
        border-width: 0 8px 8px 0; border-style: solid;
        border-color: transparent #FFFFFF transparent transparent;
    }
    .wpp-time {
        position: absolute; bottom: 4px; right: 8px;
        font-size: 0.7em; color: #8696A0;
    }

    /* AGENDADOR */
    .agenda-aviso { background: #FFF7ED; border: 1px solid #FED7AA; border-radius: 10px; padding: 16px 20px; color: #7C2D12; font-size: 0.88em; line-height: 1.7; margin-bottom: 16px; }
    .agenda-row { display: flex; align-items: center; gap: 10px; padding: 8px 0; border-bottom: 1px solid #F1F5F9; }
    .agenda-data { color: #64748B; font-size: 0.78em; font-weight: 600; min-width: 48px; }
    .agenda-label { color: #1E293B; font-size: 0.88em; flex: 1; }

    /* LINK MONETIZZE */
    .monetizze-box { background: linear-gradient(135deg, #F0FDF4, #DCFCE7); border: 2px solid #22C55E; border-radius: 12px; padding: 20px 24px; margin: 20px 0; }
    .monetizze-box-title { font-family: 'Rajdhani', sans-serif; font-size: 1.1em; font-weight: 700; color: #14532D; margin-bottom: 6px; letter-spacing: 0.5px; }
    .monetizze-box-sub { font-size: 0.85em; color: #166534; margin-bottom: 14px; line-height: 1.6; }
    .monetizze-tag { display: inline-block; background: #22C55E; color: white; border-radius: 6px; padding: 2px 10px; font-size: 0.78em; font-weight: 700; font-family: 'Rajdhani', sans-serif; letter-spacing: 0.5px; margin-bottom: 10px; }
    .monetizze-aplicado { background: #F0FDF4; border: 1px solid #86EFAC; border-radius: 8px; padding: 10px 14px; color: #14532D; font-size: 0.85em; display: flex; align-items: center; gap: 8px; margin-top: 8px; }

    /* DIAGNÓSTICO */
    .diag-card { background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 18px 20px; margin-bottom: 14px; }
    .diag-titulo { font-family: 'Rajdhani', sans-serif; font-weight: 700; font-size: 1.05em; color: #1E293B; margin-bottom: 10px; letter-spacing: 0.3px; }
    .diag-vs { display: flex; gap: 10px; align-items: center; font-size: 0.88em; }
    .diag-est { color: #64748B; }
    .diag-real { color: #059669; font-weight: 700; }
    .diag-arrow { color: #CBD5E1; }

    /* RELANÇAMENTO */
    .relanc-box { background: linear-gradient(135deg, #FDF4FF, #FAE8FF); border: 2px solid #A855F7; border-radius: 12px; padding: 20px 24px; margin: 16px 0; }

    /* STORIES */
    .story-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; padding: 18px 20px; margin-bottom: 14px; color: white; }
    .story-titulo { font-family: 'Rajdhani', sans-serif; font-size: 1.05em; font-weight: 700; letter-spacing: 0.5px; margin-bottom: 8px; opacity: 0.85; }
    .story-conteudo { font-size: 0.88em; line-height: 1.7; white-space: pre-wrap; }

    /* STORIES EXPLAINER */
    .stories-explainer { background: linear-gradient(135deg, #FFF7ED, #FEF3C7); border: 1px solid #FCD34D; border-radius: 10px; padding: 16px 20px; color: #78350F; font-size: 0.88em; line-height: 1.8; }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO DE ESTADO ---
_one_time = {
    'etapa': "Login", 'dados': {}, 'projetos': {},
    'chat_hist': [], 'usuario': '', 'api_key': '', 'chat_input_key': 0,
    'wpp_preview_idx': None,
}
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
    "Agendador":       "7. Agendador",
    "Visualizacao":    "8. Projeto Final",
    "Diagnostico":     "9. Diagnóstico",
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

# =============================================================
# UTILITÁRIOS
# =============================================================

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

def texto_para_md(chave: str, titulo: str, conteudo: str) -> str:
    limpo = limpar_html(conteudo)
    linhas = limpo.split('\n')
    md = [f"# {titulo}", ""]
    for l in linhas:
        ls = l.strip()
        if not ls:
            md.append("")
            continue
        if re.match(r'^\d+[\.\)]', ls):
            md.append(f"- {ls}")
        elif ls.startswith(('✅','🎁','📘','👉','⏰','🔥','📌','💡','⏳','🚀','💬','📋','🎯')):
            md.append(ls)
        else:
            md.append(ls)
    return '\n'.join(md)

def projeto_para_json(dados: dict) -> str:
    def converter(obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        raise TypeError(f"Não serializável: {type(obj)}")
    return json.dumps(dados, ensure_ascii=False, indent=2, default=converter)

def json_para_projeto(texto_json: str) -> dict:
    dados = json.loads(texto_json)
    if 'data_lancto' in dados and isinstance(dados['data_lancto'], str):
        try:
            dados['data_lancto'] = date.fromisoformat(dados['data_lancto'])
        except Exception:
            pass
    return dados

def validar_link(url: str) -> tuple[bool, str]:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}, method='HEAD')
        with urllib.request.urlopen(req, timeout=5) as resp:
            code = resp.getcode()
            if code < 400:
                return True, f"✅ Link válido (HTTP {code})"
            else:
                return False, f"⚠️ Link retornou HTTP {code}"
    except Exception as e:
        return False, f"❌ Link não respondeu: {e}"

def data_lancto_formatada(d: dict) -> str:
    dl = d.get('data_lancto')
    if not dl:
        return "23:59"
    dias_semana = ['segunda-feira','terça-feira','quarta-feira','quinta-feira','sexta-feira','sábado','domingo']
    nome_dia = dias_semana[dl.weekday()]
    return f"{nome_dia}, {dl.strftime('%d/%m')} às 23:59"

def gerar_ics(eventos: list) -> str:
    linhas = [
        'BEGIN:VCALENDAR','VERSION:2.0',
        'PRODID:-//Nexus Launcher//Agendador//PT',
        'CALSCALE:GREGORIAN','METHOD:PUBLISH',
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
            'BEGIN:VEVENT', f"UID:{uid}",
            f"DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}",
            f"DTSTART:{dt_start.strftime('%Y%m%dT%H%M%S')}",
            f"DTEND:{dt_end.strftime('%Y%m%dT%H%M%S')}",
            f"SUMMARY:{ev['titulo']}", f"DESCRIPTION:{desc}",
            'BEGIN:VALARM','TRIGGER:-PT30M','ACTION:DISPLAY',
            f"DESCRIPTION:Lembrete: {ev['titulo']}",'END:VALARM','END:VEVENT',
        ]
    linhas.append('END:VCALENDAR')
    return '\r\n'.join(linhas)

# =============================================================
# PARSERS
# =============================================================

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
    SECOES = [
        "DESCRICAO_GRUPO","BOAS_VINDAS","DIA_9","DIA_10","DIA_11",
        "DIA_12","DIA_13","DIA_14_MANHA","DIA_14_NOITE","VESPERA",
        "VENDA_MANHA","VENDA_NOITE"
    ]
    LABELS = {
        "DESCRICAO_GRUPO":  "📋 Descrição do grupo (bio)",
        "BOAS_VINDAS":      "💬 D-8 — Boas-vindas (início real)",
        "DIA_9":            "🎯 D-9 — Envolvimento",
        "DIA_10":           "🔎 D-10 — Consciência (dica)",
        "DIA_11":           "🔥 D-11 — Micro diagnóstico",
        "DIA_12":           "💬 D-12 — Diagnóstico direto",
        "DIA_13":           "🔥 D-13 — Ajuste revelador",
        "DIA_14_MANHA":     "📌 D-14 — Ativação",
        "DIA_14_NOITE":     "💡 D-14 (Noite) — Prova + Ponte",
        "VESPERA":          "⏳ D-14 (Final) — Véspera / Mistério",
        "VENDA_MANHA":      "🚀 Dia do lançamento — Manhã",
        "VENDA_NOITE":      "⏰ Dia do lançamento — Noite",
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

# =============================================================
# AGENDA DEF
# =============================================================
AGENDA_DEF = [
    {"chave": "DESCRICAO_GRUPO", "label": "📋 Descrição do grupo (bio)",        "offset": -15, "hora_pad": "08:00"},
    {"chave": "BOAS_VINDAS",     "label": "💬 D-8 Boas-vindas",                 "offset": -8,  "hora_pad": "08:00"},
    {"chave": "DIA_9",           "label": "🎯 D-9 Envolvimento",                "offset": -7,  "hora_pad": "08:00"},
    {"chave": "DIA_10",          "label": "🔎 D-10 Consciência",                "offset": -6,  "hora_pad": "08:00"},
    {"chave": "DIA_11",          "label": "🔥 D-11 Micro diagnóstico",          "offset": -5,  "hora_pad": "08:00"},
    {"chave": "DIA_12",          "label": "💬 D-12 Diagnóstico direto",         "offset": -4,  "hora_pad": "08:00"},
    {"chave": "DIA_13",          "label": "🔥 D-13 Ajuste revelador",           "offset": -3,  "hora_pad": "08:00"},
    {"chave": "DIA_14_MANHA",    "label": "📌 D-14 Ativação (manhã)",           "offset": -2,  "hora_pad": "08:00"},
    {"chave": "DIA_14_NOITE",    "label": "💡 D-14 Prova + Ponte (noite)",      "offset": -2,  "hora_pad": "19:00"},
    {"chave": "VESPERA",         "label": "⏳ D-14 Véspera / Mistério",         "offset": -1,  "hora_pad": "21:00"},
    {"chave": "VENDA_MANHA",     "label": "🚀 Lançamento — Manhã",              "offset":  0,  "hora_pad": "08:00"},
    {"chave": "VENDA_NOITE",     "label": "⏰ Lançamento — Noite",              "offset":  0,  "hora_pad": "19:00"},
]

# =============================================================
# BLOCOS REUTILIZÁVEIS
# =============================================================

def bloco_link_monetizze(prefixo_key="mon"):
    d = st.session_state.dados
    link_atual = d.get('link_monetizze', '').strip()

    st.markdown("""
    <div class="monetizze-box">
        <div class="monetizze-tag">🔗 PASSO IMPORTANTE</div>
        <div class="monetizze-box-title">Insira o link da Monetizze</div>
        <div class="monetizze-box-sub">
            Cadastre o e-book na Monetizze, copie o link de checkout e cole abaixo.<br>
            O link será inserido <strong>exatamente no lugar certo</strong> dentro das mensagens de venda.
        </div>
    """, unsafe_allow_html=True)

    col_link, col_val, col_btn = st.columns([4, 1, 1])
    with col_link:
        link_input = st.text_input(
            "Link Monetizze", value=link_atual,
            placeholder="https://go.monetizze.com.br/...",
            label_visibility="collapsed",
            key=f"link_mon_input_{prefixo_key}",
        )
    with col_val:
        if st.button("🔍 Validar", use_container_width=True, key=f"btn_val_{prefixo_key}"):
            if link_input.strip():
                with st.spinner("Verificando..."):
                    ok, msg = validar_link(link_input.strip())
                st.session_state[f"val_result_{prefixo_key}"] = (ok, msg)
            else:
                st.warning("Cole o link primeiro.")
    with col_btn:
        aplicar = st.button("✅ Aplicar", use_container_width=True, key=f"btn_mon_{prefixo_key}")

    st.markdown("</div>", unsafe_allow_html=True)

    val = st.session_state.get(f"val_result_{prefixo_key}")
    if val:
        ok, msg = val
        if ok:
            st.success(msg)
        else:
            st.warning(msg)

    if aplicar:
        link_limpo = link_input.strip()
        if not link_limpo:
            st.warning("Cole o link antes de aplicar.")
        else:
            d['link_monetizze'] = link_limpo
            # Substitui placeholder nas mensagens já geradas
            if d.get('msg_grupo'):
                d['msg_grupo'] = d['msg_grupo'].replace('[LINK MONETIZZE]', link_limpo)
                d['msg_grupo'] = d['msg_grupo'].replace('(SEU LINK)', link_limpo)
                d['msg_grupo'] = d['msg_grupo'].replace('SEU LINK', link_limpo)
            st.rerun()

    if link_atual:
        st.markdown(
            f"<div class='monetizze-aplicado'>✅ <strong>Link aplicado:</strong>&nbsp;"
            f"<span style='color:#166534;word-break:break-all;'>{link_atual}</span></div>",
            unsafe_allow_html=True
        )

def preview_whatsapp(secoes: list, prefixo: str = "wpp"):
    st.markdown("#### 📱 Preview — como aparece no WhatsApp")
    st.caption("Clique em uma mensagem para expandir o preview visual.")
    for i, s in enumerate(secoes):
        texto_limpo = limpar_html(s['conteudo'])
        with st.expander(f"👁️ Ver preview: {s['label']}", expanded=False):
            hora_sim = "19:07" if "NOITE" in s['chave'] or "VESPERA" in s['chave'] else "08:32"
            st.markdown(f"""
            <div class="wpp-header">
                <div class="wpp-avatar">📢</div>
                <div>
                    <div style="font-weight:700;font-size:0.95em;">Programa Gratuito</div>
                    <div style="font-size:0.75em;opacity:0.8;">Grupo · você e mais membros</div>
                </div>
            </div>
            <div class="wpp-screen">
                <div class="wpp-bubble">
                    {texto_limpo.replace(chr(10), '<br>')}
                    <span class="wpp-time">{hora_sim} ✓✓</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

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
            col_cp, col_md = st.columns(2)
            with col_cp:
                st.download_button(
                    label="📋 Copiar esta mensagem",
                    data=texto_limpo,
                    file_name=f"{s['chave'].lower()}.txt",
                    mime="text/plain",
                    key=f"copy_msg_{i}_{chave}",
                    use_container_width=True,
                )
            with col_md:
                st.download_button(
                    label="📝 Exportar .md",
                    data=texto_para_md(s['chave'], s['label'], s['conteudo']),
                    file_name=f"{s['chave'].lower()}.md",
                    mime="text/markdown",
                    key=f"md_msg_{i}_{chave}",
                    use_container_width=True,
                )
            st.markdown("<br>", unsafe_allow_html=True)
        st.divider()
        preview_whatsapp(secoes, prefixo=chave)

    else:
        st.markdown(f"<div class='caixa-texto'>{normalizar_markdown(conteudo)}</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.download_button(
            label="📋 Copiar como .txt",
            data=limpar_html(conteudo), file_name=f"{chave}.txt",
            mime="text/plain", key=f"copy_{chave}", use_container_width=True
        )
    with col2:
        st.download_button(
            label="📝 Exportar .md",
            data=texto_para_md(chave, titulo, conteudo),
            file_name=f"{chave}.md", mime="text/markdown",
            key=f"md_{chave}", use_container_width=True
        )
    with col3:
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
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("➕ INICIAR NOVO PROJETO"):
            st.session_state.dados = {}
            st.session_state.chat_hist = []
            st.session_state.etapa = "Formulario"
            st.rerun()
    with col2:
        with st.expander("📂 MEUS PROJETOS"):
            arq = st.file_uploader("📥 Importar projeto (.json)", type="json", key="import_proj")
            if arq is not None:
                try:
                    dados_imp = json_para_projeto(arq.read().decode('utf-8'))
                    nome_imp = dados_imp.get('nome_eb', 'Projeto importado')
                    st.session_state.projetos[nome_imp] = dados_imp
                    st.success(f"Projeto '{nome_imp}' importado!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao importar: {e}")

            if not st.session_state.projetos:
                st.write("Nenhum projeto salvo.")
            for nome in list(st.session_state.projetos.keys()):
                c_abrir, c_exp, c_del = st.columns([3, 1, 1])
                if c_abrir.button(f"📄 {nome}", key=f"abrir_{nome}"):
                    st.session_state.dados = st.session_state.projetos[nome].copy()
                    st.session_state.etapa = "Visualizacao"
                    st.rerun()
                c_exp.download_button(
                    "💾", data=projeto_para_json(st.session_state.projetos[nome]),
                    file_name=f"{nome.replace(' ','_')}.json", mime="application/json",
                    key=f"exp_{nome}", help="Exportar projeto como JSON"
                )
                st.markdown('<div class="btn-perigo">', unsafe_allow_html=True)
                if c_del.button("🗑️", key=f"del_{nome}", help="Excluir"):
                    del st.session_state.projetos[nome]; st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        if st.session_state.dados.get('nome_eb'):
            st.markdown('<div class="btn-laranja">', unsafe_allow_html=True)
            if st.button("🔄 RELANÇAR PROJETO"):
                st.session_state.etapa = "Relancar"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

def bloco_agendador(prefixo_key="agd"):
    d = st.session_state.dados
    data_lancto = d.get('data_lancto')
    if not data_lancto:
        st.warning("Defina a data de lançamento no formulário para usar o agendador.")
        return
    if not d.get('msg_grupo'):
        st.info("Gere as mensagens primeiro para usar o agendador.")
        return

    st.markdown("""
    <div class="agenda-aviso">
        <strong>⚠️ Como funciona o agendador — leia antes de usar</strong><br><br>
        O agendador <strong>NÃO envia as mensagens automaticamente.</strong><br>
        Cria um arquivo <strong>.ics</strong> que você importa no Google Calendar, Apple Calendar ou Outlook.<br>
        Na hora certa, o celular te notifica — você copia o texto e cola no grupo.<br><br>
        🟢 <strong>Vantagem:</strong> simples, gratuito e funciona em qualquer celular.<br>
        🔴 <strong>Limitação:</strong> o envio ainda depende de você.
    </div>
    """, unsafe_allow_html=True)

    secoes_map = {s['chave']: limpar_html(s['conteudo']) for s in parsear_mensagens(d['msg_grupo'])}
    horas_config = d.get('agenda_horas', {})

    st.markdown("**Configure o horário de cada mensagem:**")
    st.caption("O lembrete chegará 30 minutos antes com o texto pronto para copiar e colar.")

    cols_h = st.columns([3, 1])
    cols_h[0].markdown("**Mensagem**")
    cols_h[1].markdown("**Horário**")

    for item in AGENDA_DEF:
        chave = item['chave']
        data_msg = data_lancto + timedelta(days=item['offset'])
        data_str = data_msg.strftime('%d/%m')
        col_label, col_hora = st.columns([3, 1])
        with col_label:
            st.markdown(
                f"<div style='padding:6px 0;font-size:0.88em;color:#1E293B;'>"
                f"<span style='color:#64748B;font-size:0.8em;font-weight:600;'>{data_str}&nbsp;&nbsp;</span>"
                f"{item['label']}</div>", unsafe_allow_html=True
            )
        with col_hora:
            hora_val = horas_config.get(chave, item['hora_pad'])
            hora_input = st.text_input("h", value=hora_val, key=f"{prefixo_key}_{chave}",
                label_visibility="collapsed", placeholder="HH:MM")
            horas_config[chave] = hora_input

    d['agenda_horas'] = horas_config

    if st.button("📅 GERAR ARQUIVO DE CALENDÁRIO (.ics)", use_container_width=True, key=f"btn_ics_{prefixo_key}"):
        eventos = []
        for item in AGENDA_DEF:
            chave = item['chave']
            data_msg = data_lancto + timedelta(days=item['offset'])
            hora = horas_config.get(chave, item['hora_pad'])
            texto = secoes_map.get(chave, '')
            if not texto: continue
            eventos.append({'chave': chave, 'titulo': f"[Nexus] {item['label']}",
                'data': data_msg, 'hora': hora, 'descricao': texto})
        ics_content = gerar_ics(eventos)
        nome_eb = d.get('nome_eb', 'lancamento').replace(' ', '_')
        st.download_button(label="⬇️ Baixar arquivo .ics", data=ics_content.encode('utf-8'),
            file_name=f"{nome_eb}.ics", mime="text/calendar",
            use_container_width=True, key=f"dl_ics_{prefixo_key}")
        st.success("✅ Arquivo gerado! Baixe e importe no seu calendário.")

    st.markdown("""
    <div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;padding:12px 16px;margin-top:12px;color:#64748B;font-size:0.8em;line-height:1.8;">
    <strong>📲 Como importar:</strong><br>
    <strong>Google Calendar:</strong> calendar.google.com → ⚙️ Configurações → Importar<br>
    <strong>iPhone:</strong> Abra o arquivo → "Adicionar ao Calendário"<br>
    <strong>Outlook:</strong> Arquivo → Abrir e Exportar → Importar/Exportar
    </div>
    """, unsafe_allow_html=True)

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
        f"CONTEXTO:\n- Nicho: {d['nicho']}\n- Público: {d['publico']}\n- Dor principal: {d['dor']}\n\n"
        f"CONCEITO OBRIGATÓRIO: O anúncio convida para um PROGRAMA GRATUITO DE 15 DIAS sobre {d['nicho']}. "
        f"Use um nome atrativo — ex: 'Programa 15 Dias para [objetivo]'. "
        f"NUNCA mencione ebook, produto pago, lançamento, preço ou qualquer venda.\n\n"
        f"ESTRUTURA OBRIGATÓRIA:\n"
        f"1. Título chamativo em <strong>negrito HTML</strong>\n"
        f"2. Texto principal (máx 5 linhas) — foca na dor e no que vão receber grátis\n"
        f"3. Lista: ✅ Gratuito ✅ Grupo fechado ✅ Dicas diárias ✅ Vagas limitadas\n"
        f"4. Sugestão de criativo visual (1 linha)\n"
        f"5. CTA: ⬇️ Clique abaixo e garanta sua vaga\n\n"
        f"Tom: 100% GRATUITO em destaque. Humano, parece convite, não anúncio."
    )

def system_fb():
    return ("Você é um copywriter especialista em Facebook Ads. "
            "O anúncio convida para um grupo gratuito. Nunca mencione produto pago. "
            "Use tags HTML <strong> para negrito, nunca asteriscos.")

def prompt_lp():
    d = st.session_state.dados
    secao_autor = ''
    if d.get('autor_nome') or d.get('autor_experiencia'):
        secao_autor = (f"Autor: {d.get('autor_nome','')}, Experiência: {d.get('autor_experiencia','')}, "
                       f"Credenciais: {d.get('autor_credenciais','')}.  ")
    return (
        f"Crie UMA landing page completa para capturar leads para um grupo gratuito.\n\n"
        f"CONTEXTO:\n- Nicho: {d.get('nicho')}\n- Público: {d.get('publico')}\n"
        f"- Dor principal: {d['dor']}\n- Situação atual: {d['atual']}\n"
        f"- Objetivo: {d['desejada']}\n- {secao_autor}\n\n"
        f"CONCEITO: PROGRAMA GRATUITO DE 15 DIAS sobre {d.get('nicho')}. NUNCA mencione produto pago.\n\n"
        f"ESTRUTURA:\n1. Headline principal\n2. Subtítulo — o que receberão\n"
        f"3. 3 bullets de dor\n4. O que vai receber no grupo\n5. Quem sou eu (2-3 linhas)\n"
        f"6. 4 benefícios com ✔\n7. Sugestão visual\n8. CTA: [ QUERO PARTICIPAR GRATUITAMENTE ]\n\n"
        f"Tom direto e humano. Parece convite, não venda."
    )

def system_lp():
    return ("Você é um especialista em Landing Pages de alta conversão. "
            "A LP promove um grupo gratuito. Nunca mencione produto pago. "
            "Use tag HTML <strong> para negrito. Nunca asteriscos.")

def _tom_instrucao(d: dict) -> str:
    tom = d.get('tom_mensagens', 'Direto')
    mapa = {
        'Direto':   "Tom direto e objetivo. Frases curtas. Vai ao ponto. Zero rodeios.",
        'Empático': "Tom empático e acolhedor. Mostra que entende a dor antes de apresentar a solução. Cria conexão.",
        'Urgente':  "Tom de urgência e escassez. Palavras que ativam FOMO. Prazos e vagas limitadas em destaque.",
    }
    return mapa.get(tom, mapa['Direto'])

def prompt_msg():
    d = st.session_state.dados
    preco = d.get('preco', 47)
    nome_eb = d.get('nome_eb', '')
    nicho = d.get('nicho', '')
    dor = d.get('dor', '')
    whatsapp_num = d.get('whatsapp_contato', 'SEU NÚMERO AQUI')
    link_venda = d.get('link_monetizze', '').strip() or '[LINK MONETIZZE]'
    bonus_resumo = d.get('bonus_resumo', '')
    bonus_lista = '\n'.join([f'🎁 Bônus {i+1} – {b.strip()}' for i, b in enumerate(bonus_resumo.split(',')) if b.strip()]) if bonus_resumo else '🎁 Bônus 1\n🎁 Bônus 2\n🎁 Bônus 3'
    prazo_str = data_lancto_formatada(d)

    # Dica DIA 10 gerada pela IA — contraintuitiva e não popular
    dica_dia10_prompt = (
        f"Crie UMA dica surpreendente e contraintuitiva sobre {nicho} para o público: {d.get('publico')}.\n"
        f"REGRAS ABSOLUTAS:\n"
        f"- NUNCA mencione: beber água, dormir bem, fazer exercício, comer menos, força de vontade, disciplina, dieta, cardápio\n"
        f"- A dica deve parecer que a maioria das pessoas NÃO sabe\n"
        f"- Deve ser baseada em comportamento, psicologia ou fisiologia\n"
        f"- Deve gerar a reação: 'nunca pensei nisso assim antes'\n"
        f"- Máximo 5 linhas. Tom de conversa direta\n"
        f"- Termine com uma pergunta curta que convide a responder no WhatsApp: {whatsapp_num}\n"
        f"Retorne APENAS o texto da dica, sem títulos ou rótulos."
    )

    return (
        f"Gere as mensagens do funil abaixo para o lançamento sobre {nicho}.\n"
        f"Ebook: {nome_eb}. Preço: R${preco}. WhatsApp: {whatsapp_num}. Nicho: {nicho}. Dor: {dor}.\n"
        f"Bônus:\n{bonus_lista}\n\n"
        f"REGRA ABSOLUTA: Reproduza os blocos fixos PALAVRA POR PALAVRA, apenas adaptando os trechos indicados entre colchetes.\n"
        f"Apenas blocos com [IA] devem ser criados livremente. Respeite os rótulos exatos abaixo.\n\n"

        # ── DESCRIÇÃO DO GRUPO ──────────────────────────────────────────────
        f"DESCRICAO_GRUPO:\n"
        f"Seja bem-vindo ao Programa 15 Dias para [adapte: tema do programa sobre {nicho}]!\n"
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
        f"Porque, se você acompanhar até o final, pode enxergar {nicho} de uma forma completamente diferente.\n\n"

        # ── BOAS-VINDAS ─────────────────────────────────────────────────────
        f"BOAS_VINDAS:\n"
        f"Seja bem-vindo ao Programa 15 Dias para [adapte: objetivo relacionado a {nicho}].\n"
        f"Se você está aqui, provavelmente já tentou [adapte: ação comum do nicho {nicho}] antes…\n"
        f"já começou animado, fez dieta, tentou treinar…\n"
        f"mas não conseguiu manter.\n"
        f"E isso não acontece por falta de força de vontade.\n"
        f"Na maioria dos casos, o problema é outro:\n"
        f"você nunca entendeu exatamente o que está travando seu resultado.\n"
        f"E é exatamente isso que vamos descobrir aqui.\n"
        f"Durante os próximos dias, eu vou analisar seus hábitos e identificar padrões que podem estar te impedindo.\n"
        f"⚠️ Importante:\n"
        f"Esse grupo é focado em diagnóstico — não em solução.\n"
        f"No final, você vai ter clareza total sobre o seu caso.\n"
        f"Fica atento… porque isso pode mudar completamente sua visão.\n\n"

        # ── DIA 9 — ENVOLVIMENTO ────────────────────────────────────────────
        f"DIA_9:\n"
        f"Me diz uma coisa…\n"
        f"Você se identifica mais com qual situação?\n"
        f"[IA: crie 4 opções A, B, C, D relacionadas à dor '{dor}' no nicho {nicho}]\n"
        f"📲 Me responde no WhatsApp: ({whatsapp_num})\n"
        f"Isso já começa a mostrar um padrão importante.\n\n"

        # ── DIA 10 — CONSCIÊNCIA / DICA CONTRAINTUITIVA ─────────────────────
        f"DIA_10:\n"
        f"Existe algo que quase ninguém percebe:\n"
        f"[IA: crie UMA dica SURPREENDENTE e CONTRAINTUITIVA sobre {nicho}. "
        f"Deve gerar a reação 'nunca pensei nisso assim antes'. "
        f"PROIBIDO mencionar: água, sono, exercício, dieta, força de vontade, disciplina, cardápio. "
        f"Base: psicologia comportamental, fisiologia ou padrão inconsciente. Máximo 5 linhas.]\n"
        f"📲 Isso faz sentido pra você? Me conta no WhatsApp: ({whatsapp_num})\n\n"

        # ── DIA 11 — MICRO DIAGNÓSTICO ──────────────────────────────────────
        f"DIA_11:\n"
        f"Teste rápido:\n"
        f"Hoje, observa isso:\n"
        f"👉 Em qual momento do dia você sente mais vontade de sair do controle com {nicho}?\n"
        f"Manhã?\n"
        f"Tarde?\n"
        f"Noite?\n"
        f"📲 Me manda sua resposta no WhatsApp: ({whatsapp_num})\n"
        f"Isso ajuda a entender melhor seu padrão.\n\n"

        # ── DIA 12 — DIAGNÓSTICO DIRETO ─────────────────────────────────────
        f"DIA_12:\n"
        f"Agora preciso que você seja direto:\n"
        f"Qual é seu maior desafio hoje com {nicho}?\n"
        f"[IA: crie 4 opções A, B, C, D específicas para o nicho {nicho} e dor '{dor}']\n"
        f"📲 Me manda a letra no WhatsApp: ({whatsapp_num})\n"
        f"Isso faz parte do seu diagnóstico.\n\n"

        # ── DIA 13 — AJUSTE REVELADOR ───────────────────────────────────────
        f"DIA_13:\n"
        f"Existe um erro simples que pode estar travando seu resultado em {nicho}…\n"
        f"[IA: revele UM erro comportamental específico do nicho {nicho} que a maioria não percebe. "
        f"Não pode ser óbvio. Base em psicologia ou comportamento. Máximo 4 linhas.]\n"
        f"Mas não precisa mudar tudo.\n"
        f"Só testa isso:\n"
        f"[IA: sugira UMA micro-ação simples de 1 frase que a pessoa pode fazer agora]\n"
        f"📲 Depois me conta no WhatsApp: ({whatsapp_num})\n\n"

        # ── DIA 14 MANHÃ — ATIVAÇÃO ─────────────────────────────────────────
        f"DIA_14_MANHA:\n"
        f"Quero te propor algo rápido — leva menos de 2 minutos.\n"
        f"[IA: crie uma atividade simples de observação relacionada a {nicho} que a pessoa possa fazer agora com o celular. "
        f"Não muda rotina. Só registrar ou observar algo.]\n"
        f"Esse gesto simples ativa algo poderoso: quando a gente observa, automaticamente começa a fazer escolhas melhores.\n"
        f"📲 Me manda o resultado no WhatsApp: ({whatsapp_num}). Vou te dar um retorno personalizado.\n\n"

        # ── DIA 14 NOITE — PROVA + PONTE ────────────────────────────────────
        f"DIA_14_NOITE:\n"
        f"[IA: crie uma história curta de prova social com nome fictício, "
        f"mostrando alguém que passou pelo mesmo processo no nicho {nicho}. "
        f"Inclua: tentativas anteriores, o que mudou, resultado concreto e realista. Máximo 6 linhas.]\n"
        f"Mas só entender não resolveu.\n"
        f"O que mudou foi quando ela aplicou o caminho certo.\n\n"

        # ── VÉSPERA — MISTÉRIO ───────────────────────────────────────────────
        f"VESPERA:\n"
        f"Depois de analisar tudo que vocês me enviaram…\n"
        f"eu encontrei um padrão que me chamou muita atenção.\n"
        f"Mais de 80% das pessoas aqui estão travadas exatamente pelos mesmos motivos.\n"
        f"Mesmo tentando…\n"
        f"mesmo se esforçando…\n"
        f"o resultado não vem.\n"
        f"E o mais curioso:\n"
        f"👉 esses motivos quase ninguém percebe\n"
        f"👉 e não são tão óbvios quanto parecem\n"
        f"Foi por isso que eu tomei uma decisão.\n"
        f"Eu organizei tudo de forma clara e simples.\n"
        f"Um passo a passo direto…\n"
        f"Amanhã eu vou te mostrar.\n"
        f"Mas já te adianto:\n"
        f"Se ignorar isso…\n"
        f"provavelmente continua no mesmo ciclo.\n\n"

        # ── VENDA MANHÃ ──────────────────────────────────────────────────────
        f"VENDA_MANHA:\n"
        f"Hoje é o dia.\n"
        f"Durante esses dias, eu analisei tudo que você me enviou…\n"
        f"e encontrei padrões que explicam exatamente por que a maioria não consegue evoluir em {nicho}.\n"
        f"E como eu disse ontem — isso não é óbvio.\n"
        f"Por isso organizei tudo em um método simples:\n\n"
        f"📘 {nome_eb}\n\n"
        f"Aqui você vai entender:\n"
        f"👉 o que está travando seu resultado\n"
        f"👉 e o que fazer exatamente\n"
        f"Sem tentativa e erro.\n\n"
        f"{bonus_lista}\n\n"
        f"Tudo isso por apenas R$ {preco}.\n\n"
        f"👉 Acesse agora e garanta a sua vaga: {link_venda}\n\n"
        f"⏰ Só hoje, até {prazo_str}\n"
        f"✅ Garantia de 7 dias — se não gostar, devolvemos tudo.\n\n"

        # ── VENDA NOITE ──────────────────────────────────────────────────────
        f"VENDA_NOITE:\n"
        f"Boa noite 👋\n"
        f"Só passando pra te lembrar:\n"
        f"Você já entendeu que existe um problema.\n"
        f"Agora precisa decidir se vai resolver…\n"
        f"ou continuar como está.\n\n"
        f"📘 {nome_eb}\n"
        f"{bonus_lista}\n\n"
        f"👉 {link_venda}\n\n"
        f"⏰ Encerra hoje {prazo_str}\n"
        f"✅ Garantia de 7 dias\n"
    )

def system_msg():
    d = st.session_state.dados
    tom_inst = _tom_instrucao(d)
    return (
        f"Você é um especialista em copywriting para lançamentos no WhatsApp e Telegram. "
        f"Reproduza os blocos fixos EXATAMENTE como fornecidos, adaptando apenas os trechos entre colchetes. "
        f"Apenas blocos com instrução [IA] devem ser criados livremente. "
        f"Respeite os rótulos exatos (DESCRICAO_GRUPO:, BOAS_VINDAS:, DIA_9:, DIA_10:, DIA_11:, "
        f"DIA_12:, DIA_13:, DIA_14_MANHA:, DIA_14_NOITE:, VESPERA:, VENDA_MANHA:, VENDA_NOITE:). "
        f"NUNCA omita nenhum rótulo. {tom_inst}"
    )

def prompt_stories():
    d = st.session_state.dados
    nicho = d.get('nicho', '')
    dor = d.get('dor', '')
    autor = d.get('autor_nome', 'você')
    return (
        f"Crie 5 roteiros de stories para Instagram/TikTok para os primeiros 7 dias de divulgação "
        f"de um programa gratuito sobre {nicho}.\n\n"
        f"Contexto: {autor} está rodando tráfego para encher um grupo gratuito. "
        f"A dor do público: {dor}.\n\n"
        f"REGRAS:\n"
        f"- Cada story é um vídeo curto de 30 a 60 segundos\n"
        f"- Nunca mencione produto pago ou lançamento\n"
        f"- O objetivo é gerar curiosidade e fazer a pessoa clicar no link da bio para entrar no grupo\n"
        f"- Tom humano, como se {autor} estivesse falando para a câmera\n\n"
        f"Para cada story, entregue EXATAMENTE neste formato:\n\n"
        f"STORY 1 — [Nome/tema]\n"
        f"GANCHO: [primeira frase que prende em 2 segundos]\n"
        f"ROTEIRO: [o que falar, linha por linha, tom de conversa]\n"
        f"CTA FINAL: [o que pedir no final]\n\n"
        f"Repita para STORY 2, 3, 4 e 5."
    )

def system_stories():
    return ("Você é um especialista em conteúdo para redes sociais e funis de lançamento. "
            "Crie roteiros de stories autênticos, sem soar como anúncio. "
            "Tom de conversa direta com o espectador.")

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
                    st.session_state.dados.update({
                        'nicho': mapa.get('NICHO',''), 'publico': mapa.get('PUBLICO',''),
                        'nome_eb': mapa.get('NOME_EB',''), 'dor': mapa.get('DOR',''),
                        'atual': mapa.get('ATUAL',''), 'desejada': mapa.get('DESEJADA',''),
                        'promessa': mapa.get('PROMESSA',''), 'diferencial': mapa.get('DIFERENCIAL','')
                    })
                    st.rerun()
        else: st.warning("Digite o assunto do ebook antes de continuar.")

    st.divider()
    st.markdown("#### Revise ou preencha manualmente")
    d['nicho']       = st.text_input("Nicho:", value=d.get('nicho',''))
    d['publico']     = st.text_input("Público-alvo:", value=d.get('publico',''))
    d['nome_eb']     = st.text_input("Nome do e-book:", value=d.get('nome_eb',''))
    d['dor']         = st.text_input("Principal dor que resolve:", value=d.get('dor',''))
    d['atual']       = st.text_area("Situação atual da pessoa:", value=d.get('atual',''))
    d['desejada']    = st.text_area("Situação desejada:", value=d.get('desejada',''))
    d['promessa']    = st.text_input("Transformação do programa:", value=d.get('promessa',''))
    d['diferencial'] = st.text_input("Diferencial:", value=d.get('diferencial',''))
    d['preco']       = st.number_input("Preço do e-book (R$):", min_value=9, max_value=997, value=int(d.get('preco',47)), step=1)

    st.divider()
    st.markdown("#### Tom das mensagens do grupo")
    st.caption("Define como as mensagens de aquecimento e venda serão escritas.")
    tom_opcoes = ['Direto', 'Empático', 'Urgente']
    tom_atual = d.get('tom_mensagens', 'Direto')
    tom_idx = tom_opcoes.index(tom_atual) if tom_atual in tom_opcoes else 0
    d['tom_mensagens'] = st.radio(
        "Escolha o tom:",
        tom_opcoes,
        index=tom_idx,
        horizontal=True,
        captions=[
            "Frases curtas, vai ao ponto",
            "Cria conexão antes de vender",
            "FOMO e escassez em destaque"
        ]
    )

    st.divider()
    st.markdown("#### Suas credenciais como autor")
    d['autor_nome']        = st.text_input("Seu nome:", value=d.get('autor_nome',''))
    d['autor_experiencia'] = st.text_area("Sua experiência com o tema:", value=d.get('autor_experiencia',''))
    d['autor_credenciais'] = st.text_area("Resultados ou conquistas:", value=d.get('autor_credenciais',''))

    st.divider()
    st.markdown("#### WhatsApp para receber respostas da enquete")
    st.markdown("""<div style="background:#FEF9C3;border:1px solid #FDE047;border-radius:8px;padding:12px 16px;margin-bottom:12px;color:#713F12;font-size:0.88em;line-height:1.6;">
    ⚠️ <strong>ATENÇÃO: use um número DIFERENTE do grupo.</strong><br>
    O grupo ficará fechado — membros não conseguem responder lá dentro.<br>
    <strong>Pode ser seu celular pessoal, chip extra ou número de atendimento.</strong><br><br>
    💡 Configure resposta automática: <em>"Recebi sua mensagem. Já estamos analisando 🙏"</em>
    </div>""", unsafe_allow_html=True)
    d['whatsapp_contato'] = st.text_input("Número (diferente do grupo):", value=d.get('whatsapp_contato',''), placeholder="ex: (11) 99999-9999")

    data_sugerida = d.get('data_lancto', date.today() + timedelta(days=15))
    d['data_lancto'] = st.date_input("Data de lançamento", value=data_sugerida, min_value=date.today())
    st.caption("💡 Use os primeiros 7 dias para encher o grupo e os próximos 7 para aquecer. Lance no 15º dia.")

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

    d['est_leads'] = leads
    d['est_vendas'] = vendas
    d['est_faturamento'] = faturamento

    campos_obrigatorios = ['nicho','publico','nome_eb','dor','atual','desejada','promessa','diferencial']
    tudo_preenchido = all(d.get(c,'').strip() for c in campos_obrigatorios)

    if tudo_preenchido:
        st.divider()
        st.markdown(f"""<div class="preview-box">
        📚 <strong>E-book:</strong> {d.get('nome_eb')} — 60 cartões educativos<br>
        🎁 <strong>3 E-books Bônus</strong> complementares<br>
        📣 <strong>1 Anúncio</strong> alinhado com a landing page<br>
        🌐 <strong>1 Landing Page</strong> alinhada com o anúncio<br>
        📸 <strong>5 Roteiros de Stories</strong> para encher o grupo<br>
        💬 <strong>Funil completo de Mensagens</strong> — boas-vindas + aquecimento + véspera + venda<br>
        📅 <strong>Agendador</strong> — calendário com lembrete 30 min antes<br>
        🗣️ <strong>Tom:</strong> {d.get('tom_mensagens','Direto')} &nbsp;|&nbsp;
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
        st.divider()
        bloco_link_monetizze(prefixo_key="bonus_etapa")
        st.divider()
        if st.button("AVANÇAR →"): st.session_state.etapa = "Copy_Face"; st.rerun()

# ── ANÚNCIO ───────────────────────────────────────────────────
elif st.session_state.etapa == "Copy_Face":
    barra_navegacao()
    st.title("📣 ANÚNCIO")
    st.caption("Um anúncio completo e alinhado com a landing page.")
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
    st.caption("Uma landing page completa alinhada com o anúncio.")
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
    d = st.session_state.dados

    st.markdown("### 📸 Roteiros de Stories — Semana 1 (encher o grupo)")

    # ── EXPLICAÇÃO DOS STORIES EM ABA EXPANSÍVEL ──────────────────────────
    with st.expander("💡 O que são os Stories e para que servem? (clique para entender)", expanded=False):
        st.markdown("""
        <div class="stories-explainer">
            <strong>📲 Para que servem os Stories?</strong><br><br>
            Os Stories servem para <strong>encher o grupo gratuito antes do lançamento</strong>.<br><br>
            Você precisa de pessoas no grupo para ter para quem vender.<br>
            Os <strong>5 roteiros gerados</strong> são vídeos curtos (30–60 segundos) para você
            <strong>gravar e postar no Instagram ou TikTok</strong> durante a semana de captação,
            com o objetivo de fazer as pessoas <strong>clicarem no link da bio e entrarem no grupo</strong>.<br><br>
            🎯 <strong>Como usar:</strong><br>
            1. Grave cada story no celular, olhando para a câmera, com tom de conversa<br>
            2. Poste 1 story por dia nos primeiros 5 a 7 dias<br>
            3. Coloque o link do grupo na <strong>bio do Instagram/TikTok</strong><br>
            4. Combine com tráfego pago para encher mais rápido<br><br>
            ⚠️ <strong>Nunca mencione produto pago ou preço nos stories</strong> — o objetivo é só fazer a pessoa entrar no grupo.
        </div>
        """, unsafe_allow_html=True)

    st.caption("5 roteiros prontos para gravar e postar durante a semana de captação. Nunca mencionam produto ou venda.")
    col_s1, col_s2 = st.columns([3,1])
    with col_s2:
        st.markdown('<div class="btn-roxo">', unsafe_allow_html=True)
        gerar_st = st.button("📸 GERAR STORIES", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if gerar_st:
        with st.spinner("Criando roteiros de stories..."):
            d['stories_cont'] = chamar_ia(prompt_stories(), system_stories())
            st.rerun()

    if d.get('stories_cont'):
        secoes_st = []
        bloco_atual, titulo_atual = [], "Stories"
        for linha in d['stories_cont'].split('\n'):
            ls = linha.strip()
            m = re.match(r'^STORY\s*(\d+)\s*[—\-–]?\s*(.*)', ls, re.IGNORECASE)
            if m:
                if bloco_atual:
                    secoes_st.append({"titulo": titulo_atual, "conteudo": '\n'.join(bloco_atual).strip()})
                titulo_atual = f"📸 Story {m.group(1)}" + (f" — {m.group(2)}" if m.group(2) else "")
                bloco_atual = []
            else:
                bloco_atual.append(linha)
        if bloco_atual:
            secoes_st.append({"titulo": titulo_atual, "conteudo": '\n'.join(bloco_atual).strip()})

        for s in secoes_st:
            st.markdown(f"<div class='story-card'><div class='story-titulo'>{s['titulo']}</div><div class='story-conteudo'>{s['conteudo']}</div></div>", unsafe_allow_html=True)

        col_dl, col_regen = st.columns(2)
        with col_dl:
            st.download_button("📋 Baixar todos os stories (.txt)", data=limpar_html(d['stories_cont']),
                file_name="stories.txt", mime="text/plain", use_container_width=True)
        with col_regen:
            st.markdown('<div class="btn-secundario">', unsafe_allow_html=True)
            if st.button("🔄 Regenerar Stories", use_container_width=True):
                with st.spinner("Regenerando..."):
                    d['stories_cont'] = chamar_ia(prompt_stories(), system_stories())
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    st.markdown("### 💬 Funil de Mensagens do Grupo")
    st.markdown("""<div class="preview-box">
    <strong>12 peças prontas para copiar e enviar:</strong><br>
    📋 Bio → 💬 D-8 Boas-vindas → 🎯 D-9 Envolvimento →
    🔎 D-10 Consciência → 🔥 D-11 Micro diagnóstico → 💬 D-12 Diagnóstico →
    🔥 D-13 Ajuste → 📌 D-14 Ativação → 💡 D-14 Prova →
    ⏳ Véspera/Mistério → 🚀 Manhã da venda → ⏰ Noite (19h)
    </div>""", unsafe_allow_html=True)

    st.markdown("""<div style="background:#FEF3C7;border:1px solid #FCD34D;border-radius:8px;padding:12px 16px;margin-bottom:8px;color:#78350F;font-size:0.87em;line-height:1.6;">
    ⚠️ Os blocos <strong>D-9, D-10, D-12, D-13, D-14 e a prova social</strong> têm partes criadas pela IA adaptadas ao seu nicho. Os demais seguem roteiro fixo.
    </div>""", unsafe_allow_html=True)

    tom_atual = d.get('tom_mensagens', 'Direto')
    st.markdown(f"<div style='margin-bottom:8px;'><span style='background:#EDE9FE;color:#5B21B6;border-radius:6px;padding:3px 10px;font-size:0.8em;font-weight:700;'>🗣️ Tom: {tom_atual}</span> — <a href='#' style='font-size:0.8em;color:#64748B;'>alterar no formulário</a></div>", unsafe_allow_html=True)

    link_ja_cadastrado = d.get('link_monetizze', '').strip()
    if link_ja_cadastrado:
        st.markdown(f"<div class='monetizze-aplicado' style='margin-bottom:12px;'>✅ <strong>Link Monetizze cadastrado</strong> — entrará automaticamente nas mensagens de venda: <span style='color:#166534;word-break:break-all;'>{link_ja_cadastrado}</span></div>", unsafe_allow_html=True)
    else:
        st.info("💡 Cadastre o link da Monetizze na etapa de Bônus para ele entrar automaticamente.")

    prazo = data_lancto_formatada(d)
    st.caption(f"📅 Prazo da oferta nas mensagens de venda: **{prazo}** (calculado automaticamente pela data de lançamento)")

    st.markdown('<div class="btn-verde15">', unsafe_allow_html=True)
    gerar_msg = st.button("💬 GERAR FUNIL COMPLETO DE MENSAGENS")
    st.markdown('</div>', unsafe_allow_html=True)

    if gerar_msg:
        with st.spinner("Gerando o funil completo de mensagens..."):
            d['msg_grupo'] = chamar_ia(prompt_msg(), system_msg())
            # Garante substituição do placeholder de link nas mensagens geradas
            if link_ja_cadastrado:
                d['msg_grupo'] = d['msg_grupo'].replace('[LINK MONETIZZE]', link_ja_cadastrado)
                d['msg_grupo'] = d['msg_grupo'].replace('(SEU LINK)', link_ja_cadastrado)
                d['msg_grupo'] = d['msg_grupo'].replace('SEU LINK', link_ja_cadastrado)
            st.rerun()

    if d.get('msg_grupo'):
        st.divider()
        bloco_conteudo('msg_grupo', 'Mensagens', prompt_msg, system_msg)

        if not link_ja_cadastrado:
            st.divider()
            bloco_link_monetizze(prefixo_key="msg_etapa")

        st.divider()
        if st.button("AVANÇAR → AGENDADOR"):
            st.session_state.etapa = "Agendador"
            st.rerun()

# ── AGENDADOR ─────────────────────────────────────────────────
elif st.session_state.etapa == "Agendador":
    barra_navegacao()
    st.title("📅 AGENDADOR DE MENSAGENS")
    bloco_agendador(prefixo_key="agd_etapa")
    st.divider()
    if st.button("💾 SALVAR E VER PROJETO FINAL"):
        nome_projeto = st.session_state.dados.get('nome_eb', 'Sem nome')
        st.session_state.projetos[nome_projeto] = st.session_state.dados.copy()
        st.session_state.etapa = "Visualizacao"
        st.rerun()

# ── RELANÇAMENTO ──────────────────────────────────────────────
elif st.session_state.etapa == "Relancar":
    barra_navegacao()
    d = st.session_state.dados
    st.title(f"🔄 RELANÇAR: {d.get('nome_eb','')}")
    st.markdown("""
    <div class="relanc-box">
        <strong style="font-size:1.05em;font-family:'Rajdhani',sans-serif;color:#6B21A8;">♻️ Modo Relançamento</strong><br><br>
        Você vai reaproveitar o mesmo e-book, bônus, anúncio e landing page.<br>
        Apenas as <strong>mensagens do grupo serão regeneradas com variações</strong> —
        para o público não receber textos idênticos ao lançamento anterior.<br><br>
        Defina uma nova data de lançamento e clique em Relançar.
    </div>
    """, unsafe_allow_html=True)

    nova_data = st.date_input(
        "Nova data de lançamento:",
        value=date.today() + timedelta(days=15),
        min_value=date.today(),
        key="nova_data_relanc"
    )

    tom_opcoes = ['Direto', 'Empático', 'Urgente']
    tom_atual = d.get('tom_mensagens', 'Direto')
    novo_tom = st.radio(
        "Tom das mensagens desta rodada:",
        tom_opcoes,
        index=tom_opcoes.index(tom_atual) if tom_atual in tom_opcoes else 0,
        horizontal=True,
        key="tom_relanc"
    )

    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.markdown('<div class="btn-roxo">', unsafe_allow_html=True)
        if st.button("🚀 RELANÇAR — Regenerar mensagens", use_container_width=True):
            d['data_lancto'] = nova_data
            d['tom_mensagens'] = novo_tom
            d['msg_grupo'] = ''
            d['stories_cont'] = ''
            d['agenda_horas'] = {}
            with st.spinner("Regenerando mensagens para o relançamento..."):
                d['msg_grupo'] = chamar_ia(prompt_msg(), system_msg())
                # Garante link nos relançamentos
                link_mon = d.get('link_monetizze', '').strip()
                if link_mon:
                    d['msg_grupo'] = d['msg_grupo'].replace('[LINK MONETIZZE]', link_mon)
                    d['msg_grupo'] = d['msg_grupo'].replace('(SEU LINK)', link_mon)
                    d['msg_grupo'] = d['msg_grupo'].replace('SEU LINK', link_mon)
                d['stories_cont'] = chamar_ia(prompt_stories(), system_stories())
            nome_proj = d.get('nome_eb', 'Sem nome')
            st.session_state.projetos[nome_proj] = d.copy()
            st.success("✅ Mensagens regeneradas! Avance para o Agendador para configurar as novas datas.")
            st.session_state.etapa = "Agendador"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with col_r2:
        if st.button("← Voltar ao projeto", use_container_width=True):
            st.session_state.etapa = "Visualizacao"
            st.rerun()

# ── VISUALIZAÇÃO FINAL ────────────────────────────────────────
elif st.session_state.etapa == "Visualizacao":
    barra_navegacao()
    d = st.session_state.dados
    nome_projeto = d.get('nome_eb', 'Projeto')
    st.title(f"PROJETO: {nome_projeto}")

    def gerar_md_completo(d):
        partes = [
            f"# {d.get('nome_eb','')} — Projeto Completo\n",
            f"**Nicho:** {d.get('nicho','')}  \n**Público:** {d.get('publico','')}  \n"
            f"**Lançamento:** {d.get('data_lancto','')}  \n**Preço:** R${d.get('preco',47)}\n\n---\n",
            f"## 📚 E-Book Principal\n\n{limpar_html(d.get('ebook_cont','Não gerado.'))}\n\n---\n",
            f"## 🎁 E-Books Bônus\n\n{limpar_html(d.get('bonus_cont','Não gerado.'))}\n\n---\n",
            f"## 📸 Stories\n\n{limpar_html(d.get('stories_cont','Não gerado.'))}\n\n---\n",
            f"## 📣 Anúncio\n\n{limpar_html(d.get('fb_copy','Não gerado.'))}\n\n---\n",
            f"## 🌐 Landing Page\n\n{limpar_html(d.get('lp_copy','Não gerado.'))}\n\n---\n",
            f"## 💬 Mensagens do Grupo\n\n{limpar_html(d.get('msg_grupo','Não gerado.'))}\n",
        ]
        return ''.join(partes)

    col_txt, col_md, col_json = st.columns(3)
    texto_completo = (
        f"NEXUS LAUNCHER — PROJETO COMPLETO\n{'='*50}\n"
        f"E-BOOK: {d.get('nome_eb','')}\nNICHO: {d.get('nicho','')}\n"
        f"PÚBLICO: {d.get('publico','')}\nDATA DE LANÇAMENTO: {d.get('data_lancto','')}\n"
        f"PREÇO: R${d.get('preco',47)}\n{'='*50}\n\n"
        f"📚 E-BOOK PRINCIPAL\n{'-'*40}\n{limpar_html(d.get('ebook_cont','Não gerado.'))}\n\n"
        f"🎁 E-BOOKS BÔNUS\n{'-'*40}\n{limpar_html(d.get('bonus_cont','Não gerado.'))}\n\n"
        f"📸 STORIES\n{'-'*40}\n{limpar_html(d.get('stories_cont','Não gerado.'))}\n\n"
        f"📣 ANÚNCIO\n{'-'*40}\n{limpar_html(d.get('fb_copy','Não gerado.'))}\n\n"
        f"🌐 LANDING PAGE\n{'-'*40}\n{limpar_html(d.get('lp_copy','Não gerado.'))}\n\n"
        f"💬 MENSAGENS DO GRUPO\n{'-'*40}\n{limpar_html(d.get('msg_grupo','Não gerado.'))}"
    ).strip()

    with col_txt:
        st.markdown('<div class="btn-verde">', unsafe_allow_html=True)
        st.download_button("⬇️ Baixar .txt", data=texto_completo,
            file_name=f"{nome_projeto.replace(' ','_')}.txt", mime="text/plain", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col_md:
        st.markdown('<div class="btn-verde">', unsafe_allow_html=True)
        st.download_button("📝 Baixar .md (Notion)", data=gerar_md_completo(d),
            file_name=f"{nome_projeto.replace(' ','_')}.md", mime="text/markdown", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col_json:
        st.markdown('<div class="btn-roxo">', unsafe_allow_html=True)
        st.download_button("💾 Salvar projeto (.json)", data=projeto_para_json(d),
            file_name=f"{nome_projeto.replace(' ','_')}.json", mime="application/json", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    with st.expander("📸 STORIES — Semana de captação"):
        if d.get('stories_cont'):
            st.text(d['stories_cont'])
            st.download_button("📋 Copiar stories", data=limpar_html(d['stories_cont']),
                file_name="stories.txt", mime="text/plain", key="dl_stories_vis")
        else:
            st.info("Stories não gerados — vá para Mensagens e clique em 'Gerar Stories'.")
    with st.expander("📚 E-BOOK"):
        bloco_conteudo('ebook_cont','E-book',prompt_ebook,system_ebook)
    with st.expander("🎁 E-BOOKS BÔNUS"):
        bloco_conteudo('bonus_cont','Bônus',prompt_bonus,system_bonus)
    with st.expander("📣 ANÚNCIO"):
        bloco_conteudo('fb_copy','Anúncio',prompt_fb,system_fb)
    with st.expander("🌐 LANDING PAGE"):
        bloco_conteudo('lp_copy','Landing Page',prompt_lp,system_lp)
    with st.expander("💬 MENSAGENS DO GRUPO — FUNIL COMPLETO"):
        bloco_conteudo('msg_grupo','Mensagens',prompt_msg,system_msg)
    with st.expander("📅 AGENDADOR"):
        bloco_agendador(prefixo_key="agd_vis")

    st.divider()
    st.markdown('<div class="btn-laranja">', unsafe_allow_html=True)
    if st.button("📊 REGISTRAR RESULTADO DO LANÇAMENTO", use_container_width=True):
        st.session_state.etapa = "Diagnostico"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    with st.expander("🧠 DICA MESTRE — O QUE FAZER DEPOIS DO LANÇAMENTO"):
        st.markdown("""<div style="background:#F0FDF4;border:2px solid #22C55E;border-radius:12px;padding:22px 26px;color:#14532D;line-height:1.7;font-size:0.92em;">
        <strong>Não apague esse grupo.</strong><br><br>
        Você construiu atenção e interesse de pessoas reais. Esse grupo é um ativo.<br>
        Realize novos lançamentos com equilíbrio — aproximadamente 1 vez por mês.<br>
        Use o botão <strong>🔄 Relançar Projeto</strong> no topo para reaproveitar tudo sem custo de tráfego.
        </div>""", unsafe_allow_html=True)

    with st.expander("✅ CHECKLIST DE LANÇAMENTO"):
        data_lancto = d.get('data_lancto', date.today())
        dlf = data_lancto.strftime('%d/%m/%Y') if hasattr(data_lancto,'strftime') else str(data_lancto)
        dm1 = (data_lancto - timedelta(days=1)).strftime('%d/%m/%Y') if hasattr(data_lancto,'strftime') else ''
        d7  = (data_lancto - timedelta(days=7)).strftime('%d/%m/%Y') if hasattr(data_lancto,'strftime') else ''
        d6  = (data_lancto - timedelta(days=6)).strftime('%d/%m/%Y') if hasattr(data_lancto,'strftime') else ''
        d5  = (data_lancto - timedelta(days=5)).strftime('%d/%m/%Y') if hasattr(data_lancto,'strftime') else ''
        d4  = (data_lancto - timedelta(days=4)).strftime('%d/%m/%Y') if hasattr(data_lancto,'strftime') else ''
        d3  = (data_lancto - timedelta(days=3)).strftime('%d/%m/%Y') if hasattr(data_lancto,'strftime') else ''
        fases = [
            {"fase":"FASE 1 — HOJE: Preparação","cor":"#0EA5E9","items":[
                ("Hoje","Baixe o projeto completo (.txt ou .md)"),
                ("Hoje","Cadastre o e-book + 3 bônus na Monetizze"),
                ("Hoje","Cole o link da Monetizze na etapa de Bônus"),
                ("Hoje","Crie o grupo: 'Programa [X] Dias para [Objetivo]'"),
                ("Hoje","Cole a DESCRIÇÃO DO GRUPO no WhatsApp/Telegram"),
                ("Hoje","Configure BOAS-VINDAS automática ao entrar"),
                ("Hoje","Suba o ANÚNCIO → LANDING PAGE → grupo"),
                ("Hoje","Importe o .ics no seu calendário"),
                ("Hoje","Configure RESPOSTA AUTOMÁTICA no WhatsApp de contato"),
                ("Hoje","Grave os 5 STORIES e poste no Instagram/TikTok"),
            ]},
            {"fase":"FASE 2 — SEMANA 1: Encher o grupo","cor":"#8B5CF6","items":[
                ("Dias 1 a 8","Anúncios rodando — meta: 500 a 1.000 pessoas"),
                ("Diariamente","Monitore custo por lead — meta: até R$2,00"),
                ("Diariamente","Poste stories orgânicos para reforçar o tráfego pago"),
            ]},
            {"fase":"FASE 3 — SEMANA 2: Aquecimento","cor":"#059669","items":[
                (f"{d7} — D-7","Envolvimento"),
                (f"{d6} — D-6","Consciência / dica"),
                (f"{d5} — D-5","Micro diagnóstico"),
                (f"{d4} — D-4","Diagnóstico direto"),
                (f"{d3} — D-3","Ajuste revelador"),
                (f"{dm1} — D-1","Ativação + Prova social + Véspera/Mistério"),
                (f"{dm1}","Confirme se o link da Monetizze está funcionando"),
            ]},
            {"fase":f"FASE 4 — {dlf}: Dia da venda","cor":"#22C55E","items":[
                (f"{dlf} — manhã","Mensagem de lançamento"),
                (f"{dlf}","Fique disponível no WhatsApp"),
                (f"{dlf} — 19h","Lembrete noturno"),
            ]},
            {"fase":"FASE 5 — PÓS-LANÇAMENTO","cor":"#64748B","items":[
                ("Após","Registre o resultado no Diagnóstico (botão acima)"),
                ("Após","Entregue o e-book e bônus para quem comprou"),
                ("Próximo mês","Use 🔄 Relançar para a próxima rodada"),
            ]},
        ]
        for fase in fases:
            st.markdown(f'<div style="margin:18px 0 8px 0;padding:8px 14px;background:{fase["cor"]};border-radius:8px;color:white;font-weight:600;font-size:0.85em;">{fase["fase"]}</div>', unsafe_allow_html=True)
            for quando, acao in fase['items']:
                st.markdown(f'<div class="checklist-item"><div style="width:10px;height:10px;border-radius:50%;background:{fase["cor"]};margin-top:5px;flex-shrink:0"></div><div><div style="font-size:0.72em;color:#64748B;font-weight:600;text-transform:uppercase;">{quando}</div><div style="font-size:0.92em;color:#1E293B">{acao}</div></div></div>', unsafe_allow_html=True)

    st.divider()
    st.markdown("### 🤖 Launcerbot")
    st.caption(f"Olá, {st.session_state.usuario}! Pode me perguntar qualquer coisa sobre seu lançamento.")
    if st.session_state.chat_hist:
        for q, r in st.session_state.chat_hist:
            st.markdown(f"**Você:** {q}")
            st.markdown(f"<div class='chat-bubble'>{r}</div>", unsafe_allow_html=True)
    pergunta = st.text_input("Sua pergunta:", key=f"chat_input_{st.session_state.chat_input_key}",
        label_visibility="collapsed", placeholder="Digite sua pergunta aqui...")
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

# ── DIAGNÓSTICO PÓS-LANÇAMENTO ────────────────────────────────
elif st.session_state.etapa == "Diagnostico":
    barra_navegacao()
    d = st.session_state.dados
    st.title("📊 DIAGNÓSTICO PÓS-LANÇAMENTO")
    st.caption("Registre os números reais e veja o que funcionou — e o que melhorar na próxima rodada.")

    st.markdown("#### Informe os resultados reais")
    col1, col2, col3 = st.columns(3)
    with col1:
        real_leads = st.number_input("Pessoas que entraram no grupo:", min_value=0, max_value=100000,
            value=int(d.get('real_leads', d.get('est_leads', 1000))), step=10, key="d_leads")
    with col2:
        real_vendas = st.number_input("Vendas realizadas:", min_value=0, max_value=10000,
            value=int(d.get('real_vendas', 0)), step=1, key="d_vendas")
    with col3:
        real_custo = st.number_input("Custo total de tráfego (R$):", min_value=0, max_value=50000,
            value=int(d.get('real_custo', 0)), step=10, key="d_custo")

    preco = d.get('preco', 47)
    real_fat = real_vendas * preco
    real_lucro = real_fat - real_custo
    real_conv = round(real_vendas / real_leads * 100, 2) if real_leads > 0 else 0
    real_cpl = round(real_custo / real_leads, 2) if real_leads > 0 else 0
    real_roi = round((real_lucro / real_custo) * 100, 1) if real_custo > 0 else 0

    est_leads = d.get('est_leads', 1000)
    est_vendas = d.get('est_vendas', 0)
    est_fat = d.get('est_faturamento', 0)

    st.divider()
    st.markdown("#### Resultados vs Estimativa")

    metricas = [
        ("👥 Pessoas no grupo", est_leads, real_leads, "pessoas"),
        ("🛒 Vendas", est_vendas, real_vendas, "vendas"),
        ("💰 Faturamento", est_fat, real_fat, "R$"),
    ]
    cols_m = st.columns(len(metricas))
    for i, (label, est, real, unidade) in enumerate(metricas):
        with cols_m[i]:
            delta_pct = round((real - est) / est * 100) if est > 0 else 0
            delta_str = f"+{delta_pct}%" if delta_pct >= 0 else f"{delta_pct}%"
            fmt = lambda v: f"R${v:,.0f}".replace(',','.') if unidade == "R$" else f"{v:,}".replace(',','.')
            st.metric(label, fmt(real), delta=f"{delta_str} vs estimativa")

    st.divider()
    st.markdown("#### Indicadores de desempenho")
    col_a, col_b, col_c, col_d = st.columns(4)
    col_a.metric("Taxa de conversão", f"{real_conv}%",
        delta="bom" if real_conv >= 5 else "abaixo de 5%")
    col_b.metric("Custo por lead (CPL)", f"R${real_cpl}",
        delta="✅ dentro do ideal" if real_cpl <= 2.0 else "⚠️ acima de R$2,00",
        delta_color="normal" if real_cpl <= 2.0 else "inverse")
    col_c.metric("Lucro real", f"R${real_lucro:,.0f}".replace(',','.'))
    col_d.metric("ROI", f"{real_roi}%",
        delta="✅ positivo" if real_roi > 0 else "❌ negativo",
        delta_color="normal" if real_roi > 0 else "inverse")

    st.divider()
    st.markdown("#### 🤖 Análise automática com IA")
    if st.button("GERAR ANÁLISE E RECOMENDAÇÕES"):
        prompt_diag = (
            f"Analise os resultados de um lançamento digital:\n"
            f"Nicho: {d.get('nicho')}. Ebook: {d.get('nome_eb')}. Preço: R${preco}.\n"
            f"Pessoas no grupo: {real_leads}. Vendas: {real_vendas}. Custo: R${real_custo}.\n"
            f"Faturamento: R${real_fat}. Lucro: R${real_lucro}. CPL: R${real_cpl}. Conv: {real_conv}%.\n\n"
            f"Dê uma análise direta em 3 partes:\n"
            f"1. O QUE FUNCIONOU (máx 3 pontos)\n"
            f"2. O QUE MELHORAR (máx 3 pontos práticos)\n"
            f"3. META PARA O PRÓXIMO LANÇAMENTO (1 número específico a bater)"
        )
        with st.spinner("Analisando resultados..."):
            analise = chamar_ia(prompt_diag, "Você é um consultor especialista em lançamentos digitais. Seja direto e prático.")
        d['diag_analise'] = analise
        d['real_leads'] = real_leads
        d['real_vendas'] = real_vendas
        d['real_custo'] = real_custo
        nome_proj = d.get('nome_eb', 'Sem nome')
        st.session_state.projetos[nome_proj] = d.copy()
        st.rerun()

    if d.get('diag_analise'):
        st.markdown(f"<div class='caixa-texto'>{normalizar_markdown(d['diag_analise'])}</div>", unsafe_allow_html=True)
        st.download_button("📋 Baixar análise (.txt)", data=limpar_html(d['diag_analise']),
            file_name="diagnostico.txt", mime="text/plain")

    st.divider()
    col_v, col_r = st.columns(2)
    with col_v:
        if st.button("← Voltar ao projeto", use_container_width=True):
            st.session_state.etapa = "Visualizacao"
            st.rerun()
    with col_r:
        st.markdown('<div class="btn-laranja">', unsafe_allow_html=True)
        if st.button("🔄 PLANEJAR PRÓXIMO LANÇAMENTO", use_container_width=True):
            st.session_state.etapa = "Relancar"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- RODAPÉ ---
st.markdown("<div class='footer'>© 2026 Nexus Launcher – Lançamento digital inteligente</div>", unsafe_allow_html=True)
