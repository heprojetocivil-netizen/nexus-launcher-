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

    /* Cards para os bônus individuais */
    .bonus-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 24px;
    }

    .bonus-card-header {
        background: linear-gradient(135deg, #0EA5E9, #0284C7);
        color: white;
        border-radius: 8px;
        padding: 12px 18px;
        margin-bottom: 16px;
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.1em;
        font-weight: 700;
        letter-spacing: 0.5px;
    }

    .bonus-descricao {
        background: #EFF6FF;
        border-left: 4px solid #0EA5E9;
        border-radius: 6px;
        padding: 12px 16px;
        margin-bottom: 14px;
        color: #1E3A5F;
        font-size: 0.92em;
        line-height: 1.6;
    }

    .bonus-conteudo {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 16px 20px;
        color: #334155;
        font-size: 0.88em;
        line-height: 1.7;
        white-space: pre-wrap;
    }

    /* ── ESTILOS: cards de aquecimento ── */
    .aquecimento-dia-header {
        background: linear-gradient(135deg, #7C3AED, #5B21B6);
        color: white;
        border-radius: 8px;
        padding: 12px 18px;
        margin-bottom: 12px;
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.05em;
        font-weight: 700;
        letter-spacing: 0.5px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .aquecimento-card {
        background: #F5F3FF;
        border: 1px solid #DDD6FE;
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 20px;
    }

    .aquecimento-conteudo {
        background: #FFFFFF;
        border: 1px solid #EDE9FE;
        border-radius: 8px;
        padding: 16px 20px;
        color: #334155;
        font-size: 0.88em;
        line-height: 1.7;
        white-space: pre-wrap;
    }

    .aquecimento-gancho {
        background: #EDE9FE;
        border-left: 4px solid #7C3AED;
        border-radius: 0 6px 6px 0;
        padding: 10px 16px;
        margin-top: 12px;
        color: #4C1D95;
        font-size: 0.85em;
        font-style: italic;
    }

    .btn-roxo>button {
        background-color: #7C3AED !important;
        height: 3.5em !important;
    }
    .btn-roxo>button:hover {
        background-color: #5B21B6 !important;
    }

    /* ── ESTILOS: anúncio único e LP única ── */
    .anuncio-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 28px 32px;
        margin-bottom: 20px;
    }

    .anuncio-header {
        background: linear-gradient(135deg, #F59E0B, #D97706);
        color: white;
        border-radius: 8px;
        padding: 12px 18px;
        margin-bottom: 18px;
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.15em;
        font-weight: 700;
        letter-spacing: 0.5px;
    }

    .anuncio-corpo {
        background: #FFFBEB;
        border-left: 4px solid #F59E0B;
        border-radius: 0 8px 8px 0;
        padding: 16px 20px;
        color: #1C1917;
        font-size: 0.95em;
        line-height: 1.75;
        white-space: pre-wrap;
    }

    .anuncio-imagem-dica {
        background: #FEF3C7;
        border: 1px dashed #F59E0B;
        border-radius: 8px;
        padding: 12px 16px;
        margin-top: 14px;
        color: #92400E;
        font-size: 0.82em;
        font-style: italic;
    }

    .lp-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 28px 32px;
        margin-bottom: 20px;
    }

    .lp-section-header {
        background: linear-gradient(135deg, #10B981, #059669);
        color: white;
        border-radius: 6px;
        padding: 8px 14px;
        margin: 16px 0 10px 0;
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.95em;
        font-weight: 700;
        letter-spacing: 0.5px;
        display: inline-block;
    }

    .lp-headline {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.6em;
        font-weight: 700;
        color: #0F172A;
        line-height: 1.3;
        margin: 10px 0 6px 0;
    }

    .lp-subtitulo {
        color: #475569;
        font-size: 1em;
        line-height: 1.6;
        margin-bottom: 12px;
    }

    .lp-dor {
        background: #FFF1F2;
        border-left: 4px solid #F43F5E;
        border-radius: 0 8px 8px 0;
        padding: 14px 18px;
        color: #881337;
        font-size: 0.92em;
        line-height: 1.65;
        margin: 10px 0;
    }

    .lp-solucao {
        background: #F0FDF4;
        border-left: 4px solid #22C55E;
        border-radius: 0 8px 8px 0;
        padding: 14px 18px;
        color: #14532D;
        font-size: 0.92em;
        line-height: 1.65;
        margin: 10px 0;
    }

    .lp-autor {
        background: #EFF6FF;
        border: 1px solid #BFDBFE;
        border-radius: 10px;
        padding: 16px 20px;
        color: #1E3A5F;
        font-size: 0.92em;
        line-height: 1.65;
        margin: 10px 0;
    }

    .lp-beneficios {
        background: #FAFAFA;
        border: 1px solid #E5E7EB;
        border-radius: 10px;
        padding: 16px 20px;
        color: #1E293B;
        font-size: 0.9em;
        line-height: 1.8;
        margin: 10px 0;
    }

    .lp-cta {
        background: linear-gradient(135deg, #00BFFF, #0099CC);
        color: white;
        border-radius: 10px;
        padding: 18px;
        text-align: center;
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.2em;
        font-weight: 700;
        letter-spacing: 1px;
        margin-top: 18px;
    }

    /* ── ESTILOS: mensagens de grupo ── */
    .msg-card {
        border-radius: 14px;
        padding: 22px 26px;
        margin-bottom: 18px;
    }

    .msg-card-bv {
        background: #F0FDF4;
        border: 1px solid #BBF7D0;
        border-left: 5px solid #22C55E;
    }

    .msg-card-desafio {
        background: #FFF7ED;
        border: 1px solid #FED7AA;
        border-left: 5px solid #F59E0B;
    }

    .msg-card-aquec {
        background: #F5F3FF;
        border: 1px solid #DDD6FE;
        border-left: 5px solid #7C3AED;
    }

    .msg-card-lancto {
        background: #FFF1F2;
        border: 1px solid #FECDD3;
        border-left: 5px solid #F43F5E;
    }

    .msg-card-desc {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-left: 5px solid #64748B;
    }

    .msg-label {
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.8em;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 10px;
        display: block;
    }

    .msg-body {
        font-size: 0.93em;
        line-height: 1.75;
        color: #1E293B;
        white-space: pre-wrap;
    }

    .desafio-box {
        background: #FFFBEB;
        border: 1px dashed #F59E0B;
        border-radius: 8px;
        padding: 14px 18px;
        margin-top: 12px;
        color: #78350F;
        font-size: 0.88em;
        line-height: 1.7;
    }

    /* ── CRONOGRAMA VISUAL ── */
    .cronograma-wrapper {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        border-radius: 16px;
        padding: 28px 32px;
        margin: 20px 0;
    }

    .cronograma-title {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.3em;
        font-weight: 700;
        color: #00BFFF;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 24px;
        text-align: center;
    }

    .cron-item {
        display: flex;
        align-items: flex-start;
        gap: 16px;
        margin-bottom: 16px;
    }

    .cron-badge {
        min-width: 90px;
        background: rgba(0,191,255,0.15);
        border: 1px solid rgba(0,191,255,0.4);
        border-radius: 6px;
        padding: 4px 10px;
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.78em;
        font-weight: 700;
        color: #00BFFF;
        text-align: center;
        flex-shrink: 0;
    }

    .cron-badge.lancto {
        background: rgba(244,63,94,0.2);
        border-color: rgba(244,63,94,0.5);
        color: #F43F5E;
    }

    .cron-texto {
        color: #CBD5E1;
        font-size: 0.88em;
        line-height: 1.5;
    }

    .cron-texto strong {
        color: #F1F5F9;
    }

    .cron-divisor {
        border: none;
        border-top: 1px solid rgba(255,255,255,0.08);
        margin: 12px 0;
    }

    /* ── BANNER DE LANÇAMENTO ── */
    .banner-lancamento {
        background: linear-gradient(135deg, #0F172A 0%, #1a1040 50%, #0F172A 100%);
        border: 1px solid rgba(0,191,255,0.3);
        border-radius: 16px;
        padding: 32px;
        margin: 20px 0;
        text-align: center;
        position: relative;
        overflow: hidden;
    }

    .banner-lancamento::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #00BFFF, #7C3AED, #F43F5E, #F59E0B, #22C55E);
    }

    .banner-titulo {
        font-family: 'Rajdhani', sans-serif;
        font-size: 2em;
        font-weight: 700;
        color: #F1F5F9;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .banner-subtitulo {
        color: #94A3B8;
        font-size: 0.9em;
        letter-spacing: 1px;
    }

    .badge-fase {
        display: inline-block;
        background: linear-gradient(135deg, #F59E0B, #D97706);
        color: white;
        border-radius: 999px;
        padding: 3px 14px;
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.75em;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 16px;
    }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO DE ESTADO ---
DATA_PADRAO = date.today() + timedelta(days=15)

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
ETAPAS = ["Formulario", "Gerar_Ebook", "Gerar_Bonus", "Gerar_Aquecimento", "Copy_Face", "Copy_LP", "Mensagens_Grupo", "Visualizacao"]
ETAPAS_LABELS = {
    "Formulario":        "1. Formulário",
    "Gerar_Ebook":       "2. E-book",
    "Gerar_Bonus":       "3. Bônus",
    "Gerar_Aquecimento": "4. Aquecimento",
    "Copy_Face":         "5. Anúncio",
    "Copy_LP":           "6. Landing Page",
    "Mensagens_Grupo":   "7. Mensagens",
    "Visualizacao":      "8. Projeto Final",
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

# --- PARSEAR BÔNUS EM 3 BLOCOS SEPARADOS ---
def _linha_e_marcador_bonus(linha):
    l = linha.strip().replace("🎁", "").strip()
    lu = l.upper()
    for num in ("1", "2", "3"):
        for pref in (f"BONUS {num}:", f"BONUS{num}:", f"BONUS {num} -", f"BONUS{num} -"):
            if lu.startswith(pref):
                nome = l[len(pref):].strip(" :-")
                return num, nome
        for pref in (f"BÔNUS {num}:", f"BÔNUS{num}:", f"BÔNUS {num} -"):
            if lu.startswith(pref.upper()):
                nome = l[len(pref):].strip(" :-")
                return num, nome
    return None, None


def parsear_bonus(texto: str) -> list:
    linhas = texto.split("\n")
    marcadores = []
    for idx, linha in enumerate(linhas):
        num, nome = _linha_e_marcador_bonus(linha)
        if num is not None:
            marcadores.append((idx, num, nome))

    if not marcadores:
        return [{"titulo": "🎁 Bônus", "descricao": "", "conteudo": texto.strip()}]

    bonus_list = []
    for i, (idx_ini, num, nome_bonus) in enumerate(marcadores):
        idx_fim = marcadores[i + 1][0] if i + 1 < len(marcadores) else len(linhas)
        bloco = linhas[idx_ini + 1: idx_fim]

        titulo = "🎁 BÔNUS " + num + (": " + nome_bonus if nome_bonus else "")
        descricao_partes = []
        conteudo_partes = []
        estado = "cabecalho"

        for linha in bloco:
            ls = linha.strip()
            lu = ls.upper()

            if estado == "cabecalho" and not ls:
                continue

            if lu.startswith("DESCRI") and ":" in ls:
                estado = "descricao"
                parte = ls[ls.index(":") + 1:].strip()
                if parte:
                    descricao_partes.append(parte)
                continue

            if lu.startswith("CONTE") and ":" in ls:
                estado = "conteudo"
                parte = ls[ls.index(":") + 1:].strip()
                if parte:
                    conteudo_partes.append(parte)
                continue

            if estado == "descricao":
                descricao_partes.append(ls)
            elif estado == "conteudo":
                conteudo_partes.append(linha)
            else:
                conteudo_partes.append(linha)

        descricao = "\n".join(descricao_partes).strip()
        conteudo = "\n".join(conteudo_partes).strip()
        if not conteudo and not descricao:
            conteudo = "\n".join(bloco).strip()

        bonus_list.append({"titulo": titulo, "descricao": descricao, "conteudo": conteudo})

    return bonus_list


# --- PARSEAR DIAS DE AQUECIMENTO ---
def parsear_aquecimento(texto: str) -> list:
    linhas = texto.split("\n")
    marcadores = []

    for idx, linha in enumerate(linhas):
        ls = linha.strip()
        lu = ls.upper()
        for num in ("1", "2", "3", "4", "5"):
            for pref in (f"DIA {num}:", f"DIA {num} -", f"DIA{num}:", f"📅 DIA {num}", f"📅DIA {num}"):
                if lu.startswith(pref.upper()):
                    nome = ls[len(pref):].strip(" :-")
                    marcadores.append((idx, num, nome))
                    break

    if not marcadores:
        return [{"dia": "Dia 1", "titulo": "Aquecimento", "conteudo": texto.strip(), "gancho": ""}]

    dias_list = []
    for i, (idx_ini, num, titulo_dia) in enumerate(marcadores):
        idx_fim = marcadores[i + 1][0] if i + 1 < len(marcadores) else len(linhas)
        bloco = linhas[idx_ini + 1: idx_fim]

        conteudo_partes = []
        gancho_partes = []
        estado = "conteudo"

        for linha in bloco:
            ls = linha.strip()
            lu = ls.upper()

            if not ls and estado == "conteudo" and not conteudo_partes:
                continue

            if lu.startswith("GANCHO") and ":" in ls:
                estado = "gancho"
                parte = ls[ls.index(":") + 1:].strip()
                if parte:
                    gancho_partes.append(parte)
                continue

            if estado == "conteudo":
                conteudo_partes.append(linha)
            elif estado == "gancho":
                gancho_partes.append(ls)

        conteudo = "\n".join(conteudo_partes).strip()
        gancho = " ".join(gancho_partes).strip()

        dias_list.append({
            "dia": f"Dia {num}",
            "titulo": titulo_dia,
            "conteudo": conteudo,
            "gancho": gancho,
        })

    return dias_list


# ── PARSEAR MENSAGENS ESTRUTURADAS ───────────────────────────────────────────
def parsear_mensagens(texto: str) -> dict:
    resultado = {
        "descricao": "",
        "msg1": "",
        "msg2_desafio": "",
        "msg3_aquec": "",
        "msg4_lancto": "",
    }

    blocos = re.split(r'\n\s*---+\s*\n', texto)

    for bloco in blocos:
        bl = bloco.strip()
        blu = bl.upper()

        if "DESCRIÇÃO DO GRUPO" in blu or "DESCRICAO DO GRUPO" in blu:
            linhas = bl.split('\n')
            corpo = '\n'.join(l for l in linhas if not (
                'DESCRI' in l.upper() and 'GRUPO' in l.upper()
            )).strip()
            resultado["descricao"] = corpo

        elif "MENSAGEM 1" in blu or "MSG 1" in blu or "BOAS-VINDAS" in blu:
            linhas = bl.split('\n')
            corpo = '\n'.join(l for l in linhas[1:]).strip()
            resultado["msg1"] = corpo

        elif "MENSAGEM 2" in blu or "MSG 2" in blu or "DESAFIO" in blu:
            linhas = bl.split('\n')
            corpo = '\n'.join(l for l in linhas[1:]).strip()
            resultado["msg2_desafio"] = corpo

        elif "MENSAGEM 3" in blu or "MSG 3" in blu or "AQUECIMENTO" in blu:
            linhas = bl.split('\n')
            corpo = '\n'.join(l for l in linhas[1:]).strip()
            resultado["msg3_aquec"] = corpo

        elif "MENSAGEM 4" in blu or "MSG 4" in blu or "LANÇAMENTO" in blu or "LANCAMENTO" in blu:
            linhas = bl.split('\n')
            corpo = '\n'.join(l for l in linhas[1:]).strip()
            resultado["msg4_lancto"] = corpo

    if not any(resultado.values()):
        resultado["msg1"] = texto

    return resultado


# ── PARSEAR ANÚNCIO E LP ──────────────────────────────────────────────────────
def parsear_anuncio(texto: str) -> dict:
    resultado = {"corpo": texto.strip(), "imagem": ""}
    m = re.search(r'(imagem sugerida|sugest[aã]o de imagem)[:\s]+(.+?)(?:\n|$)', texto, re.IGNORECASE)
    if m:
        resultado["imagem"] = m.group(2).strip()
        resultado["corpo"] = texto[:m.start()].strip() + "\n" + texto[m.end():].strip()
        resultado["corpo"] = resultado["corpo"].strip()
    return resultado


def parsear_lp(texto: str) -> dict:
    campos = {
        "headline": "",
        "subtitulo": "",
        "dor": "",
        "solucao": "",
        "autor": "",
        "beneficios": "",
        "imagens": "",
        "cta": "[ ENTRAR NO GRUPO GRATUITO ]",
    }
    linhas = texto.split('\n')
    estado = None

    for linha in linhas:
        ls = linha.strip()
        lu = ls.upper()

        if lu.startswith("HEADLINE:") or lu.startswith("TÍTULO:") or lu.startswith("TITULO:"):
            campos["headline"] = ls.split(":", 1)[1].strip() if ":" in ls else ""
            estado = "headline"
        elif lu.startswith("SUBTÍT") or lu.startswith("SUBTIT"):
            campos["subtitulo"] = ls.split(":", 1)[1].strip() if ":" in ls else ""
            estado = "subtitulo"
        elif "DOR" in lu and estado not in ("beneficios",):
            parte = ls.split(":", 1)[1].strip() if ":" in ls else ""
            campos["dor"] = parte
            estado = "dor"
        elif "SOLU" in lu:
            parte = ls.split(":", 1)[1].strip() if ":" in ls else ""
            campos["solucao"] = parte
            estado = "solucao"
        elif "QUEM" in lu or "AUTOR" in lu:
            parte = ls.split(":", 1)[1].strip() if ":" in ls else ""
            campos["autor"] = parte
            estado = "autor"
        elif "BENEF" in lu:
            parte = ls.split(":", 1)[1].strip() if ":" in ls else ""
            campos["beneficios"] = parte
            estado = "beneficios"
        elif "IMAGEM" in lu or "VISUAL" in lu:
            parte = ls.split(":", 1)[1].strip() if ":" in ls else ""
            campos["imagens"] = parte
            estado = "imagens"
        elif "ENTRAR NO GRUPO" in lu or "CTA" in lu:
            estado = None
        elif estado and ls:
            campos[estado] = (campos[estado] + "\n" + ls).strip()

    if not any(v for k, v in campos.items() if k not in ("cta",)):
        campos["dor"] = texto.strip()

    return campos


# --- COMPONENTE: BLOCO COM BOTÕES DE COPIAR E REGENERAR ---
def bloco_conteudo(chave: str, titulo: str, prompt_fn=None, system_fn=None):
    conteudo = st.session_state.dados.get(chave, '')
    if not conteudo:
        st.info(f"{titulo} ainda não foi gerado.")
        return

    if chave == 'fb_copy':
        parsed = parsear_anuncio(conteudo)
        st.markdown("<div class='anuncio-header'>📣 ANÚNCIO — VERSÃO FINAL</div>", unsafe_allow_html=True)
        corpo_html = normalizar_markdown(parsed["corpo"])
        st.markdown(f"<div class='anuncio-corpo'>{corpo_html}</div>", unsafe_allow_html=True)
        if parsed["imagem"]:
            st.markdown(
                f"<div class='anuncio-imagem-dica'>🖼️ <strong>Sugestão de imagem:</strong> {parsed['imagem']}</div>",
                unsafe_allow_html=True
            )

    elif chave == 'lp_copy':
        lp = parsear_lp(conteudo)
        st.markdown("<div class='lp-card'>", unsafe_allow_html=True)

        if lp["headline"]:
            st.markdown("<span class='lp-section-header'>HEADLINE</span>", unsafe_allow_html=True)
            st.markdown(f"<div class='lp-headline'>{lp['headline']}</div>", unsafe_allow_html=True)

        if lp["subtitulo"]:
            st.markdown(f"<div class='lp-subtitulo'>{lp['subtitulo']}</div>", unsafe_allow_html=True)

        if lp["dor"]:
            st.markdown("<span class='lp-section-header'>😣 SEÇÃO DE DOR</span>", unsafe_allow_html=True)
            st.markdown(f"<div class='lp-dor'>{normalizar_markdown(lp['dor'])}</div>", unsafe_allow_html=True)

        if lp["solucao"]:
            st.markdown("<span class='lp-section-header'>✅ SOLUÇÃO</span>", unsafe_allow_html=True)
            st.markdown(f"<div class='lp-solucao'>{normalizar_markdown(lp['solucao'])}</div>", unsafe_allow_html=True)

        if lp["autor"]:
            st.markdown("<span class='lp-section-header'>👤 QUEM SOU EU</span>", unsafe_allow_html=True)
            st.markdown(f"<div class='lp-autor'>{normalizar_markdown(lp['autor'])}</div>", unsafe_allow_html=True)

        if lp["beneficios"]:
            st.markdown("<span class='lp-section-header'>🎯 BENEFÍCIOS</span>", unsafe_allow_html=True)
            st.markdown(f"<div class='lp-beneficios'>{normalizar_markdown(lp['beneficios'])}</div>", unsafe_allow_html=True)

        if lp["imagens"]:
            st.markdown(
                f"<div class='anuncio-imagem-dica'>🖼️ <strong>Sugestões visuais:</strong> {lp['imagens']}</div>",
                unsafe_allow_html=True
            )

        st.markdown(f"<div class='lp-cta'>{lp['cta']}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    elif chave == 'msg_grupo':
        _renderizar_mensagens(conteudo)

    elif chave == 'bonus_cont':
        bonus_list = parsear_bonus(conteudo)
        for b in bonus_list:
            st.markdown(f"<div class='bonus-card-header'>{b['titulo']}</div>", unsafe_allow_html=True)
            if b['descricao']:
                st.markdown(f"<div class='bonus-descricao'><strong>Descrição:</strong><br>{b['descricao']}</div>", unsafe_allow_html=True)
            conteudo_html = normalizar_markdown(b['conteudo'])
            st.markdown(f"<div class='bonus-conteudo'>{conteudo_html}</div>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

    elif chave == 'aquecimento_cont':
        dias_list = parsear_aquecimento(conteudo)
        emojis = ["🔥", "💡", "🎯", "⚡", "🚀"]
        for i, d in enumerate(dias_list):
            emoji = emojis[i % len(emojis)]
            st.markdown(
                f"<div class='aquecimento-dia-header'>{emoji} {d['dia']}"
                f"{' — ' + d['titulo'] if d['titulo'] else ''}</div>",
                unsafe_allow_html=True
            )
            conteudo_html = normalizar_markdown(d['conteudo'])
            st.markdown(f"<div class='aquecimento-conteudo'>{conteudo_html}</div>", unsafe_allow_html=True)
            if d['gancho']:
                st.markdown(
                    f"<div class='aquecimento-gancho'>🔗 <strong>Gancho para amanhã:</strong> {d['gancho']}</div>",
                    unsafe_allow_html=True
                )
            st.markdown("<br>", unsafe_allow_html=True)

    else:
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


def _renderizar_mensagens(texto: str):
    parsed = parsear_mensagens(texto)
    d = st.session_state.dados
    data_lancto = d.get('data_lancto', date.today() + timedelta(days=15))
    data_bv      = (data_lancto - timedelta(days=7)).strftime('%d/%m/%Y')
    data_desafio = (data_lancto - timedelta(days=4)).strftime('%d/%m/%Y')
    data_msg3    = (data_lancto - timedelta(days=1)).strftime('%d/%m/%Y')
    data_lancto_fmt = data_lancto.strftime('%d/%m/%Y') if hasattr(data_lancto, 'strftime') else str(data_lancto)

    if parsed["descricao"]:
        st.markdown(
            f"<div class='msg-card msg-card-desc'>"
            f"<span class='msg-label' style='color:#64748B;'>📋 Descrição do Grupo</span>"
            f"<div class='msg-body'>{parsed['descricao']}</div>"
            f"</div>",
            unsafe_allow_html=True
        )

    if parsed["msg1"]:
        st.markdown(
            f"<div class='msg-card msg-card-bv'>"
            f"<span class='msg-label' style='color:#16A34A;'>📩 Mensagem 1 — Boas-vindas (enviar em {data_bv} — 7 dias antes)</span>"
            f"<div class='msg-body'>{normalizar_markdown(parsed['msg1'])}</div>"
            f"</div>",
            unsafe_allow_html=True
        )

    if parsed["msg2_desafio"]:
        st.markdown(
            f"<div class='msg-card msg-card-desafio'>"
            f"<span class='msg-label' style='color:#D97706;'>🏆 Mensagem 2 — Desafio Interativo (enviar em {data_desafio} — 4 dias antes)</span>"
            f"<div class='msg-body'>{normalizar_markdown(parsed['msg2_desafio'])}</div>"
            f"</div>",
            unsafe_allow_html=True
        )

    if parsed["msg3_aquec"]:
        st.markdown(
            f"<div class='msg-card msg-card-aquec'>"
            f"<span class='msg-label' style='color:#7C3AED;'>⏳ Mensagem 3 — Aquecimento (enviar em {data_msg3} — véspera do lançamento)</span>"
            f"<div class='msg-body'>{normalizar_markdown(parsed['msg3_aquec'])}</div>"
            f"</div>",
            unsafe_allow_html=True
        )

    if parsed["msg4_lancto"]:
        st.markdown(
            f"<div class='msg-card msg-card-lancto'>"
            f"<span class='msg-label' style='color:#E11D48;'>🚀 Mensagem 4 — Lançamento (enviar em {data_lancto_fmt})</span>"
            f"<div class='msg-body'>{normalizar_markdown(parsed['msg4_lancto'])}</div>"
            f"</div>",
            unsafe_allow_html=True
        )

    if not any(parsed.values()):
        st.markdown(f"<div class='caixa-texto'>{normalizar_markdown(texto)}</div>", unsafe_allow_html=True)


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

# --- CRONOGRAMA VISUAL ---
def mostrar_cronograma(d):
    data_lancto = d.get('data_lancto', date.today() + timedelta(days=15))
    data_lancto_fmt = data_lancto.strftime('%d/%m/%Y') if hasattr(data_lancto, 'strftime') else str(data_lancto)
    data_bv         = (data_lancto - timedelta(days=7)).strftime('%d/%m')
    data_desafio    = (data_lancto - timedelta(days=4)).strftime('%d/%m')
    data_aq1        = (data_lancto - timedelta(days=6)).strftime('%d/%m')
    data_aq5        = (data_lancto - timedelta(days=2)).strftime('%d/%m')
    data_vespera    = (data_lancto - timedelta(days=1)).strftime('%d/%m')

    st.markdown(f"""
    <div class="cronograma-wrapper">
        <div class="cronograma-title">📅 Cronograma do Lançamento</div>

        <div class="cron-item">
            <div class="cron-badge">HOJE</div>
            <div class="cron-texto"><strong>Preparação</strong> — Suba o anúncio, crie o grupo, cadastre na Monetizze</div>
        </div>
        <hr class="cron-divisor">

        <div class="cron-item">
            <div class="cron-badge">DIAS 1–7</div>
            <div class="cron-texto"><strong>Encher o grupo</strong> — Anúncio rodando, objetivo: 500 a 1.000 pessoas</div>
        </div>
        <hr class="cron-divisor">

        <div class="cron-item">
            <div class="cron-badge">{data_bv}</div>
            <div class="cron-texto"><strong>📩 Boas-vindas</strong> — Mensagem 1 no grupo (7 dias antes). Apresentação calorosa, sem mencionar produto.</div>
        </div>
        <hr class="cron-divisor">

        <div class="cron-item">
            <div class="cron-badge">{data_aq1}–{data_aq5}</div>
            <div class="cron-texto"><strong>🔥 Mini-aulas de Aquecimento</strong> — 5 conteúdos gratuitos, 1 por dia. Valor real, sem venda.</div>
        </div>
        <hr class="cron-divisor">

        <div class="cron-item">
            <div class="cron-badge">{data_desafio}</div>
            <div class="cron-texto"><strong>🏆 Desafio Interativo</strong> — Mensagem 2 com 3 desafios práticos. Gera engajamento e confiança.</div>
        </div>
        <hr class="cron-divisor">

        <div class="cron-item">
            <div class="cron-badge">{data_vespera}</div>
            <div class="cron-texto"><strong>⏳ Véspera</strong> — Mensagem 3. Aquecimento máximo, cria expectativa sem revelar o produto.</div>
        </div>
        <hr class="cron-divisor">

        <div class="cron-item">
            <div class="cron-badge lancto">🚀 {data_lancto_fmt}</div>
            <div class="cron-texto"><strong>LANÇAMENTO</strong> — Mensagem 4 com link da Monetizze. Preço de lançamento válido só neste dia.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# --- PROMPTS ---
def prompt_ebook():
    d = st.session_state.dados
    return (
        f"Gere 60 cartões educativos numerados para o e-book '{d['nome_eb']}'. "
        f"Público-alvo: {d['publico']}. Dor principal: {d['dor']}. "
        f"Diferencial: {d['diferencial']}. Cada cartão deve ter título e conteúdo útil."
    )

def system_ebook():
    return "Você é um especialista em conteúdo digital educativo. Seja objetivo e prático."


def prompt_bonus():
    d = st.session_state.dados
    nicho = d.get('nicho', '')
    nome_eb = d.get('nome_eb', '')
    publico = d.get('publico', '')
    dor = d.get('dor', '')
    promessa = d.get('promessa', '')
    return (
        f"Crie 3 ebooks bônus complementares para quem comprou o ebook principal sobre {nicho}. "
        f"Ebook principal: {nome_eb}. "
        f"Publico-alvo: {publico}. Dor principal: {dor}. Promessa: {promessa}. "
        f"Para cada ebook bonus, gere EXATAMENTE neste formato:\n\n"
        f"BONUS 1: [Nome do ebook]\n"
        f"Descricao: [2 linhas explicando o que o leitor vai aprender]\n"
        f"Conteudo: [20 cartoes educativos numerados com titulo e conteudo util]\n\n"
        f"BONUS 2: [Nome do ebook]\n"
        f"Descricao: [2 linhas]\n"
        f"Conteudo: [20 cartoes educativos numerados]\n\n"
        f"BONUS 3: [Nome do ebook]\n"
        f"Descricao: [2 linhas]\n"
        f"Conteudo: [20 cartoes educativos numerados]\n\n"
        f"Os 3 bonus devem ser diferentes entre si e complementar o ebook principal de forma logica."
    )

def system_bonus():
    return "Você é um especialista em conteúdo digital educativo. Crie ebooks bônus práticos, diretos e que agreguem valor real ao produto principal."


def prompt_aquecimento():
    d = st.session_state.dados
    nicho       = d.get('nicho', '')
    publico     = d.get('publico', '')
    dor         = d.get('dor', '')
    promessa    = d.get('promessa', '')
    nome_eb     = d.get('nome_eb', '')
    diferencial = d.get('diferencial', '')
    data_lancto = d.get('data_lancto', date.today() + timedelta(days=15))
    data_fmt    = data_lancto.strftime('%d/%m/%Y') if hasattr(data_lancto, 'strftime') else 'em breve'
    data_aq1    = (data_lancto - timedelta(days=6)).strftime('%d/%m/%Y') if hasattr(data_lancto, 'strftime') else ''
    data_aq2    = (data_lancto - timedelta(days=5)).strftime('%d/%m/%Y') if hasattr(data_lancto, 'strftime') else ''
    data_aq3    = (data_lancto - timedelta(days=4)).strftime('%d/%m/%Y') if hasattr(data_lancto, 'strftime') else ''
    data_aq4    = (data_lancto - timedelta(days=3)).strftime('%d/%m/%Y') if hasattr(data_lancto, 'strftime') else ''
    data_aq5    = (data_lancto - timedelta(days=2)).strftime('%d/%m/%Y') if hasattr(data_lancto, 'strftime') else ''

    return (
        f"Crie 5 mensagens de aquecimento para um grupo de WhatsApp/Telegram sobre {nicho}.\n\n"
        f"CONTEXTO:\n"
        f"- Público: {publico}\n"
        f"- Dor principal: {dor}\n"
        f"- Ebook que será lançado: {nome_eb}\n"
        f"- Promessa do produto: {promessa}\n"
        f"- Diferencial: {diferencial}\n"
        f"- Data de lançamento: {data_fmt}\n\n"
        f"DATAS DAS MINI-AULAS:\n"
        f"- Dia 1: {data_aq1}\n"
        f"- Dia 2: {data_aq2}\n"
        f"- Dia 3: {data_aq3}\n"
        f"- Dia 4: {data_aq4}\n"
        f"- Dia 5: {data_aq5}\n\n"
        f"OBJETIVO: Entregar valor real ANTES de qualquer venda. "
        f"Cada mensagem deve ensinar algo útil sobre {nicho}, criar identificação com a dor e "
        f"construir autoridade de forma natural. NÃO mencione produto ou preço.\n\n"
        f"REGRAS IMPORTANTES:\n"
        f"- Cada mensagem será enviada à noite (ex: 19h ou 20h) do respectivo dia\n"
        f"- NUNCA use frases como 'experimente hoje', 'faça isso hoje', 'ao acordar amanhã' que criem confusão temporal\n"
        f"- Use linguagem atemporal para as dicas práticas: 'experimente esta semana', 'tente agora', 'coloque em prática'\n"
        f"- A mensagem é enviada e lida no mesmo dia — escreva como se a pessoa estivesse lendo agora\n"
        f"- Use emojis com moderação\n\n"
        f"Gere EXATAMENTE neste formato para cada dia:\n\n"
        f"DIA 1: [Título curto e poderoso]\n"
        f"[Mensagem completa: 1 ensinamento prático sobre {nicho}, em linguagem humana e direta, "
        f"máximo 10 linhas. Inclua 1 dica acionável que a pessoa pode aplicar agora ou nesta semana.]\n"
        f"Gancho: [1 frase curta criando expectativa para o próximo dia, sem revelar o produto]\n\n"
        f"DIA 2: [Título]\n"
        f"[Mensagem]\n"
        f"Gancho: [frase]\n\n"
        f"DIA 3: [Título]\n"
        f"[Mensagem]\n"
        f"Gancho: [frase]\n\n"
        f"DIA 4: [Título]\n"
        f"[Mensagem]\n"
        f"Gancho: [frase]\n\n"
        f"DIA 5: [Título — encerramento do aquecimento, toque leve que algo especial chega em breve]\n"
        f"[Mensagem de encerramento reforçando transformação possível. Pode mencionar que nos próximos dias haverá uma novidade especial para quem acompanhou até aqui.]\n"
        f"Gancho: [Nos próximos dias tem uma novidade especial pra você — fique de olho neste grupo!]\n\n"
        f"REGRAS FINAIS: Tom humano, sem parecer robô. Cada dia deve ensinar algo DIFERENTE. "
        f"Nada de 'clique aqui', 'compre agora' ou qualquer CTA de venda."
    )

def system_aquecimento():
    return (
        "Você é um especialista em marketing de conteúdo e lançamentos digitais. "
        "Sua missão é criar mensagens de aquecimento que entregam valor real, constroem confiança "
        "e criam desejo pelo produto — tudo antes de qualquer oferta. "
        "Escreva como um ser humano, não como um robô de vendas. "
        "NUNCA use frases como 'experimente hoje ao acordar' ou 'tente hoje antes de dormir' que criem "
        "incoerência temporal — as mensagens são enviadas à noite e lidas no mesmo dia. "
        "Use sempre referências atemporais como 'coloque em prática', 'tente esta semana', 'experimente agora'."
    )


def prompt_fb():
    d = st.session_state.dados
    nome_eb     = d.get('nome_eb', '')
    nicho       = d.get('nicho', '')
    publico     = d.get('publico', '')
    dor         = d.get('dor', '')
    promessa    = d.get('promessa', '')
    diferencial = d.get('diferencial', '')
    data_lancto = d.get('data_lancto', date.today() + timedelta(days=15))
    data_fmt    = data_lancto.strftime('%d/%m/%Y') if hasattr(data_lancto, 'strftime') else 'em breve'

    return (
        f"Crie UM ÚNICO anúncio para Facebook/Instagram que incentiva pessoas a entrar em um grupo gratuito sobre {nicho}.\n\n"
        f"CONTEXTO DO PRODUTO:\n"
        f"- Nicho: {nicho}\n"
        f"- Público: {publico}\n"
        f"- Dor principal: {dor}\n"
        f"- Promessa do produto que será lançado: {promessa}\n"
        f"- Diferencial: {diferencial}\n"
        f"- Nome do grupo: [Nome do grupo sobre {nicho}]\n\n"
        f"ESTRUTURA OBRIGATÓRIA DO ANÚNCIO:\n"
        f"1. Parágrafo 1: Tocar diretamente na dor '{dor}' de forma empática (1-2 linhas)\n"
        f"2. Parágrafo 2: Agitação — o que essa dor está custando para a pessoa (1-2 linhas)\n"
        f"3. Parágrafo 3: Apresentar o grupo como solução GRATUITA — mencionar que dentro do grupo a pessoa vai receber "
        f"conteúdos exclusivos, dicas práticas e brindes/materiais gratuitos relacionados a {nicho}\n"
        f"4. CTA final: ⬇️ Clique no botão abaixo e descubra como começar.\n\n"
        f"REGRAS:\n"
        f"- O anúncio NÃO menciona o ebook nem o preço — o objetivo é apenas trazer pessoas para o grupo\n"
        f"- Linguagem direta, empática, humana — sem asteriscos para negrito\n"
        f"- Tom de convite, não de venda\n"
        f"- Após o texto, adicione: 'Imagem sugerida: [descrição de imagem visual mostrando transformação positiva relacionada a {nicho}]'\n\n"
        f"Gere APENAS UM anúncio. Sem variações, sem numeração, sem título de 'Variação'."
    )

def system_fb():
    return (
        "Você é um copywriter especialista em anúncios de captação de leads para grupos de WhatsApp e Telegram. "
        "O objetivo do anúncio é atrair pessoas para um grupo GRATUITO, não vender diretamente. "
        "Escreva com empatia, toque na dor real e apresente o grupo como uma oportunidade valiosa e sem custo. "
        "Mencione que o grupo oferece conteúdos e materiais gratuitos. Linguagem humana. Nunca use asteriscos."
    )

def prompt_lp():
    d = st.session_state.dados
    nome_eb     = d.get('nome_eb', '')
    nicho       = d.get('nicho', '')
    publico     = d.get('publico', '')
    dor         = d.get('dor', '')
    promessa    = d.get('promessa', '')
    diferencial = d.get('diferencial', '')
    atual       = d.get('atual', '')
    desejada    = d.get('desejada', '')
    nome_autor  = d.get('autor_nome', '')
    experiencia = d.get('autor_experiencia', '')
    credenciais = d.get('autor_credenciais', '')

    secao_autor = ''
    if nome_autor or experiencia:
        secao_autor = (
            f"Autor: {nome_autor}. Experiência: {experiencia}. Conquistas: {credenciais}. "
        )

    return (
        f"Crie UMA ÚNICA Landing Page completa para captar membros para um grupo gratuito sobre {nicho} "
        f"(onde será lançado o ebook '{nome_eb}').\n\n"
        f"CONTEXTO DO PRODUTO:\n"
        f"- Público: {publico}\n"
        f"- Dor principal: {dor}\n"
        f"- Situação atual: {atual}\n"
        f"- Situação desejada: {desejada}\n"
        f"- Promessa do ebook: {promessa}\n"
        f"- Diferencial: {diferencial}\n"
        f"- {secao_autor}\n\n"
        f"ESTRUTURA OBRIGATÓRIA — use EXATAMENTE estes marcadores:\n\n"
        f"Headline: [título principal impactante ligado à transformação que o público busca]\n\n"
        f"Subtítulo: [subtítulo que reforça que o grupo é gratuito e entrega valor imediato]\n\n"
        f"Seção de Dor: [texto empático descrevendo a situação atual do público, tocando na dor '{dor}']\n\n"
        f"Solução: [texto apresentando o grupo gratuito como primeiro passo para a transformação — mencionar que dentro do grupo a pessoa receberá conteúdos exclusivos e brindes gratuitos antes do lançamento]\n\n"
        "Quem sou eu: [" + (secao_autor if secao_autor else "Breve apresentação do autor com credibilidade") + "]\n\n"
        f"Benefícios:\n"
        f"- [O que a pessoa vai receber/aprender no grupo — conteúdo gratuito]\n"
        f"- [Benefício 2]\n"
        f"- [Benefício 3]\n"
        f"- [Benefício 4 — ex: acesso antecipado ao ebook no lançamento]\n\n"
        f"Imagens sugeridas: [descrição de 2-3 imagens visuais alinhadas ao tema {nicho}]\n\n"
        f"Gere APENAS UMA Landing Page, sem variações. CTA deve ser: [ ENTRAR NO GRUPO GRATUITO ]"
    )

def system_lp():
    return (
        "Você é um especialista em Landing Pages de alta conversão para captação de leads em grupos. "
        "Crie uma LP coerente e persuasiva para levar pessoas a entrar em um grupo gratuito. "
        "O foco é captar membros, não vender diretamente. "
        "Use sempre os marcadores de seção exatos pedidos no prompt. "
        "Nunca use asteriscos para negrito. Nunca crie variações."
    )

def prompt_msg():
    d = st.session_state.dados
    data_lancto  = d.get('data_lancto', date.today() + timedelta(days=15))
    data_fmt     = data_lancto.strftime('%d/%m/%Y')
    data_bv      = (data_lancto - timedelta(days=7)).strftime('%d/%m/%Y')
    data_desafio = (data_lancto - timedelta(days=4)).strftime('%d/%m/%Y')
    data_d1      = (data_lancto - timedelta(days=1)).strftime('%d/%m/%Y')
    preco        = d.get('preco', 47)
    nome_eb      = d.get('nome_eb', '')
    nicho        = d.get('nicho', '')
    publico      = d.get('publico', '')
    dor          = d.get('dor', '')
    promessa     = d.get('promessa', '')
    bonus_resumo = d.get('bonus_resumo', '')

    if bonus_resumo:
        bonus_list = '\n'.join([f'  🎁 {b.strip()}' for b in bonus_resumo.split(',') if b.strip()])
    else:
        bonus_list = '  🎁 Bônus complementares inclusos'

    return (
        f"Crie 4 mensagens para um grupo de WhatsApp/Telegram de lançamento do ebook '{nome_eb}' sobre {nicho}.\n\n"
        f"DADOS DO LANÇAMENTO:\n"
        f"- Público: {publico}\n"
        f"- Dor principal: {dor}\n"
        f"- Promessa: {promessa}\n"
        f"- Preço: R${preco}\n"
        f"- Bônus: {bonus_resumo}\n"
        f"- Data de lançamento: {data_fmt}\n"
        f"- Data de boas-vindas: {data_bv} (7 dias antes)\n"
        f"- Data do desafio: {data_desafio} (4 dias antes)\n"
        f"- Data de aquecimento/véspera: {data_d1} (1 dia antes)\n\n"
        f"REGRAS GERAIS:\n"
        f"- Tom humano, direto, sem incoerências\n"
        f"- Toda mensagem deve estar 100% alinhada ao tema '{nicho}' e ao ebook '{nome_eb}'\n"
        f"- A jornada do grupo deve ser coerente: boas-vindas → desafio → aquecimento → lançamento\n"
        f"- NUNCA use frases com incoerência temporal como 'ao acordar amanhã' em mensagens noturnas\n\n"
        f"Gere EXATAMENTE nesta estrutura, com os separadores ---:\n\n"
        f"Descrição do grupo:\n"
        f"Este grupo é silencioso. Você não será incomodado. Aqui você receberá apenas conteúdos exclusivos, materiais gratuitos e avisos sobre {nicho}.\n\n"
        f"---\n\n"
        f"Mensagem 1 – Boas-vindas ({data_bv})\n"
        f"[Boas-vindas calorosas e curtas (máximo 5 linhas). Diga que o grupo foi criado para entregar "
        f"conteúdo gratuito e exclusivo sobre {nicho}. Mencione que nos próximos dias virão conteúdos valiosos. "
        f"Informe que em {data_fmt} haverá algo especial. Peça para ficarem atentos. "
        f"NÃO mencione produto ou preço.]\n\n"
        f"---\n\n"
        f"Mensagem 2 – Desafio Interativo ({data_desafio})\n"
        f"[Mensagem com 3 desafios práticos e simples que a pessoa pode fazer em casa, "
        f"diretamente relacionados ao tema {nicho} e à dor '{dor}'. "
        f"Cada desafio deve ser claro, acionável e motivador. Peça para a pessoa responder no grupo "
        f"como foi. Isso gera engajamento real. Máximo 15 linhas. Formato:\n"
        f"🏆 DESAFIO DO DIA!\n"
        f"Hoje temos 3 desafios para você experimentar:\n\n"
        f"Desafio 1: [desafio simples relacionado a {nicho}]\n"
        f"Desafio 2: [desafio simples]\n"
        f"Desafio 3: [desafio simples]\n\n"
        f"Responda aqui: conseguiu fazer? Como foi?]\n\n"
        f"---\n\n"
        f"Mensagem 3 – Aquecimento ({data_d1})\n"
        f"[Mensagem curta de antecipação (máximo 5 linhas). Amanhã é o grande dia. "
        f"Toque na dor '{dor}' de forma humana. Crie expectativa máxima sem revelar o produto ou o preço.]\n\n"
        f"---\n\n"
        f"Mensagem 4 – Lançamento ({data_fmt})\n"
        f"🔥 [frase de abertura de impacto — use: 'Hoje é o dia que você vinha esperando!']\n\n"
        f"📘 O Lançamento do meu e-book exclusivo — *{nome_eb}*\n"
        f"[uma linha direta sobre o que o leitor vai conquistar com base na promessa '{promessa}']\n\n"
        f"🎁 *Bônus inclusos:*\n"
        f"{bonus_list}\n\n"
        f"💰 Preço de lançamento: R${preco}\n"
        f"✅ Garantia: 7 dias ou seu dinheiro de volta\n\n"
        f"👉 [LINK DA MONETIZZE]\n\n"
        f"⚠️ Este preço é válido só hoje, {data_fmt}. Amanhã o valor muda."
    )

def system_msg():
    return (
        "Você é um especialista em copywriting para lançamentos digitais no WhatsApp e Telegram. "
        "Escreva mensagens naturais, humanas e 100% coerentes entre si. "
        "Toda a sequência de mensagens deve contar uma história lógica e alinhada ao produto. "
        "NUNCA escreva frases com incoerência temporal — ex: não diga 'ao acordar amanhã' em mensagem noturna. "
        "A mensagem de lançamento DEVE começar com 'Hoje é o dia que você vinha esperando!' e incluir "
        "'O Lançamento do meu e-book exclusivo —' antes do nome do ebook. "
        "Use linguagem simples e direta. "
        "Siga rigorosamente a estrutura e os separadores --- pedidos no prompt."
    )

# ============================================================
# TELA: LOGIN
# ============================================================
if st.session_state.etapa == "Login":
    st.markdown("""
    <div class="banner-lancamento">
        <div class="banner-titulo">NEXUS LAUNCHER</div>
        <div class="banner-subtitulo">PLATAFORMA DE LANÇAMENTOS DIGITAIS</div>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("ACESSO RESTRITO A ASSOCIADOS DO QUIZ MAIS PRÊMIOS")

    st.markdown(
        '<p style="margin-top:-8px; margin-bottom:20px; font-size:0.95em;">'
        '🔗 <a href="https://www.quizmaispremios.com.br" target="_blank" '
        'style="color:#00BFFF; text-decoration:none; font-weight:600;">'
        'www.quizmaispremios.com.br</a></p>',
        unsafe_allow_html=True
    )

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

    st.divider()
    st.markdown("#### Suas credenciais como autor")
    st.caption(
        "Essas informações aparecem na Landing Page na seção 'Quem sou eu' e geram confiança no leitor. "
        "Não precisa ser famoso — qualquer experiência real vale."
    )
    d['autor_nome']         = st.text_input("Seu nome (como quer aparecer):", value=d.get('autor_nome', ''), placeholder="ex: João Silva")
    d['autor_experiencia']  = st.text_area(
        "Sua experiência com o tema:",
        value=d.get('autor_experiencia', ''),
        placeholder="ex: Pratico ioga há 5 anos e já ajudei dezenas de pessoas a reduzirem a dor crônica.",
    )
    d['autor_credenciais']  = st.text_area(
        "Resultados ou conquistas que pode mencionar:",
        value=d.get('autor_credenciais', ''),
        placeholder="ex: Já orientei mais de 200 alunos iniciantes a conquistarem flexibilidade em 30 dias.",
    )

    # Data padrão: hoje + 15 dias
    data_sugerida = d.get('data_lancto', date.today() + timedelta(days=15))
    d['data_lancto'] = st.date_input(
        "Data de lançamento",
        value=data_sugerida,
        min_value=date.today(),
        help="💡 Padrão: daqui a 15 dias — 7 dias para encher o grupo + aquecimento + lançamento."
    )
    st.caption("💡 Cronograma automático: Dia 0 = anúncio no ar → Dia 8 = boas-vindas → Dias 9–13 = mini-aulas → Dia 11 = desafio → Dia 14 = aquecimento → Dia 15 = LANÇAMENTO.")

    # Cronograma visual
    if d.get('data_lancto'):
        mostrar_cronograma(d)

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

    campos_obrigatorios = ['nicho', 'publico', 'nome_eb', 'dor', 'atual', 'desejada', 'promessa', 'diferencial']
    tudo_preenchido = all(d.get(c, '').strip() for c in campos_obrigatorios)

    if tudo_preenchido:
        st.divider()
        st.markdown("#### Resumo do que será gerado")
        st.markdown(f"""
        <div class="preview-box">
        Vamos gerar um lançamento completo para você:<br><br>
        📚 <strong>E-book:</strong> {d.get('nome_eb')} — 60 cartões educativos sobre {d.get('nicho')}<br>
        🎁 <strong>3 E-books Bônus</strong> complementares ao produto principal<br>
        🔥 <strong>5 Mini-aulas de Aquecimento</strong> para o grupo — entrega valor antes de vender<br>
        🎯 <strong>Público:</strong> {d.get('publico')}<br>
        📣 <strong>1 anúncio único</strong> para captar membros para o grupo gratuito<br>
        🌐 <strong>1 Landing Page completa</strong> com CTA para o grupo gratuito<br>
        📩 <strong>4 mensagens</strong> de boas-vindas, desafio, aquecimento e lançamento<br>
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
            st.session_state.etapa = "Gerar_Bonus"
            st.rerun()

# ============================================================
# TELA: GERAR E-BOOKS BÔNUS
# ============================================================
elif st.session_state.etapa == "Gerar_Bonus":
    barra_navegacao()
    st.title("🎁 GERAR 3 E-BOOKS BÔNUS")
    st.caption("Os bônus serão complementares ao ebook principal e incluídos automaticamente na Mensagem de Lançamento.")

    if st.button("GERAR 3 EBOOKS BÔNUS"):
        with st.spinner("Gerando ebooks bônus com IA..."):
            st.session_state.dados['bonus_cont'] = chamar_ia(prompt_bonus(), system_bonus())
            bonus_texto = st.session_state.dados['bonus_cont']
            linhas = bonus_texto.split('\n')
            nomes = []
            for linha in linhas:
                num, nome_b = _linha_e_marcador_bonus(linha)
                if num is not None and nome_b:
                    nomes.append(nome_b)
            if nomes:
                st.session_state.dados['bonus_resumo'] = ', '.join(nomes)
            st.rerun()

    if 'bonus_cont' in st.session_state.dados:
        bloco_conteudo('bonus_cont', 'Bônus', prompt_bonus, system_bonus)
        if st.button("AVANÇAR →"):
            st.session_state.etapa = "Gerar_Aquecimento"
            st.rerun()

# ============================================================
# TELA: GERAR AQUECIMENTO
# ============================================================
elif st.session_state.etapa == "Gerar_Aquecimento":
    barra_navegacao()
    st.title("🔥 MINI-AULAS DE AQUECIMENTO")

    d = st.session_state.dados
    data_lancto = d.get('data_lancto', date.today() + timedelta(days=15))
    data_aq1 = (data_lancto - timedelta(days=6)).strftime('%d/%m/%Y')
    data_aq5 = (data_lancto - timedelta(days=2)).strftime('%d/%m/%Y')

    st.markdown(f"""
    <div class="preview-box">
    <strong>Por que isso importa?</strong><br><br>
    As mini-aulas são enviadas no grupo <strong>antes</strong> do lançamento, uma por dia (de {data_aq1} a {data_aq5}).
    Elas entregam valor real, constroem sua autoridade e criam desejo pelo produto —
    tudo <em>sem mencionar preço ou venda</em>.<br><br>
    Quando a mensagem de lançamento chegar, o grupo já vai confiar em você. Isso aumenta muito a conversão.
    </div>
    """, unsafe_allow_html=True)

    mostrar_cronograma(d)

    st.markdown('<div class="btn-roxo">', unsafe_allow_html=True)
    gerar_btn = st.button("🔥 GERAR 5 MINI-AULAS DE AQUECIMENTO")
    st.markdown('</div>', unsafe_allow_html=True)

    if gerar_btn:
        with st.spinner("Criando conteúdo de aquecimento personalizado..."):
            st.session_state.dados['aquecimento_cont'] = chamar_ia(prompt_aquecimento(), system_aquecimento())
            st.rerun()

    if 'aquecimento_cont' in st.session_state.dados:
        st.divider()
        st.markdown("#### Suas 5 mini-aulas prontas para enviar")
        st.caption(f"Envie uma por dia no grupo, de {data_aq1} a {data_aq5}.")
        bloco_conteudo('aquecimento_cont', 'Aquecimento', prompt_aquecimento, system_aquecimento)

        st.divider()
        if st.button("AVANÇAR →"):
            st.session_state.etapa = "Copy_Face"
            st.rerun()

# ============================================================
# TELA: ANÚNCIO ÚNICO
# ============================================================
elif st.session_state.etapa == "Copy_Face":
    barra_navegacao()
    st.title("📣 ANÚNCIO PARA FACEBOOK / INSTAGRAM")

    st.markdown("""
    <div class="preview-box">
    <strong>Anúncio de captação — grupo gratuito</strong><br><br>
    O anúncio gerado convida as pessoas para entrar no seu <strong>grupo gratuito</strong>,
    prometendo conteúdos exclusivos e brindes. O objetivo é encher o grupo — a venda acontece depois,
    dentro do grupo, no dia do lançamento.
    </div>
    """, unsafe_allow_html=True)

    if st.button("📣 GERAR ANÚNCIO"):
        with st.spinner("Gerando anúncio com IA..."):
            st.session_state.dados['fb_copy'] = chamar_ia(prompt_fb(), system_fb())

    if 'fb_copy' in st.session_state.dados:
        bloco_conteudo('fb_copy', 'Anúncio', prompt_fb, system_fb)
        if st.button("AVANÇAR →"):
            st.session_state.etapa = "Copy_LP"
            st.rerun()

# ============================================================
# TELA: LANDING PAGE ÚNICA
# ============================================================
elif st.session_state.etapa == "Copy_LP":
    barra_navegacao()
    st.title("🌐 LANDING PAGE")

    st.markdown("""
    <div class="preview-box">
    <strong>Landing Page de captação — grupo gratuito</strong><br><br>
    A LP gerada é 100% alinhada ao anúncio. Ela apresenta a dor, a solução, sua autoridade como autor
    e conduz o visitante a entrar no grupo com o botão <strong>[ ENTRAR NO GRUPO GRATUITO ]</strong>.
    </div>
    """, unsafe_allow_html=True)

    if st.button("🌐 GERAR LANDING PAGE"):
        with st.spinner("Gerando Landing Page com IA..."):
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

    d = st.session_state.dados
    data_lancto  = d.get('data_lancto', date.today() + timedelta(days=15))
    data_bv      = (data_lancto - timedelta(days=7)).strftime('%d/%m/%Y')
    data_desafio = (data_lancto - timedelta(days=4)).strftime('%d/%m/%Y')
    data_d1      = (data_lancto - timedelta(days=1)).strftime('%d/%m/%Y')
    data_fmt     = data_lancto.strftime('%d/%m/%Y')

    st.markdown(f"""
    <div class="preview-box">
    <strong>4 mensagens com jornada coerente e datas definidas</strong><br><br>
    📩 <strong>Boas-vindas</strong> → {data_bv} (7 dias antes)<br>
    🏆 <strong>Desafio Interativo</strong> → {data_desafio} (4 dias antes)<br>
    ⏳ <strong>Aquecimento / Véspera</strong> → {data_d1} (1 dia antes)<br>
    🚀 <strong>Lançamento</strong> → {data_fmt}
    </div>
    """, unsafe_allow_html=True)

    mostrar_cronograma(d)

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

    st.markdown(f"""
    <div class="banner-lancamento">
        <div class="badge-fase">PROJETO COMPLETO</div>
        <div class="banner-titulo">{nome_projeto}</div>
        <div class="banner-subtitulo">LANÇAMENTO DIGITAL PROFISSIONAL</div>
    </div>
    """, unsafe_allow_html=True)

    d = st.session_state.dados
    texto_completo = f"""
NEXUS LAUNCHER — PROJETO COMPLETO
{'='*50}
E-BOOK: {d.get('nome_eb', '')}
NICHO: {d.get('nicho', '')}
PÚBLICO: {d.get('publico', '')}
DATA DE LANÇAMENTO: {d.get('data_lancto', '')}
PREÇO: R${d.get('preco', 47)}
{'='*50}

📚 E-BOOK PRINCIPAL
{'-'*40}
{limpar_html(d.get('ebook_cont', 'Não gerado.'))}

🎁 E-BOOKS BÔNUS
{'-'*40}
{limpar_html(d.get('bonus_cont', 'Não gerado.'))}

🔥 MINI-AULAS DE AQUECIMENTO (enviar no grupo dia a dia)
{'-'*40}
{limpar_html(d.get('aquecimento_cont', 'Não gerado.'))}

📣 ANÚNCIO (FACEBOOK / INSTAGRAM)
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

    with st.expander("🎁 E-BOOKS BÔNUS"):
        bloco_conteudo('bonus_cont', 'Bônus', prompt_bonus, system_bonus)

    with st.expander("🔥 MINI-AULAS DE AQUECIMENTO"):
        data_lancto_vis = d.get('data_lancto', date.today() + timedelta(days=15))
        data_aq1_vis = (data_lancto_vis - timedelta(days=6)).strftime('%d/%m/%Y')
        data_aq5_vis = (data_lancto_vis - timedelta(days=2)).strftime('%d/%m/%Y')
        st.caption(f"Envie uma por dia no grupo de {data_aq1_vis} a {data_aq5_vis}.")
        bloco_conteudo('aquecimento_cont', 'Aquecimento', prompt_aquecimento, system_aquecimento)

    with st.expander("📣 ANÚNCIO (Facebook / Instagram)"):
        bloco_conteudo('fb_copy', 'Anúncio', prompt_fb, system_fb)

    with st.expander("🌐 LANDING PAGE"):
        bloco_conteudo('lp_copy', 'Landing Page', prompt_lp, system_lp)

    with st.expander("📌 MENSAGENS DO GRUPO"):
        bloco_conteudo('msg_grupo', 'Mensagens', prompt_msg, system_msg)

    # --- CHECKLIST DE LANÇAMENTO ---
    st.divider()
    with st.expander("✅ CHECKLIST DE LANÇAMENTO — O QUE FAZER AGORA"):
        data_lancto_ck = d.get('data_lancto', date.today() + timedelta(days=15))
        data_lancto_fmt = data_lancto_ck.strftime('%d/%m/%Y') if hasattr(data_lancto_ck, 'strftime') else str(data_lancto_ck)
        data_bv_ck      = (data_lancto_ck - timedelta(days=7)).strftime('%d/%m/%Y')
        data_desafio_ck = (data_lancto_ck - timedelta(days=4)).strftime('%d/%m/%Y')
        data_vespera_ck = (data_lancto_ck - timedelta(days=1)).strftime('%d/%m/%Y')
        data_aq1_ck     = (data_lancto_ck - timedelta(days=6)).strftime('%d/%m/%Y')
        data_aq2_ck     = (data_lancto_ck - timedelta(days=5)).strftime('%d/%m/%Y')
        data_aq3_ck     = (data_lancto_ck - timedelta(days=4)).strftime('%d/%m/%Y')
        data_aq4_ck     = (data_lancto_ck - timedelta(days=3)).strftime('%d/%m/%Y')
        data_aq5_ck     = (data_lancto_ck - timedelta(days=2)).strftime('%d/%m/%Y')

        mostrar_cronograma(d)

        fases = [
            {
                "fase": "FASE 1 — HOJE: Preparação (Dia 0)",
                "cor": "#0EA5E9",
                "items": [
                    ("Hoje", "Baixe todo o conteúdo gerado pelo Nexus Launcher (.txt)"),
                    ("Hoje", "Crie o grupo no WhatsApp ou Telegram com o nome do nicho"),
                    ("Hoje", "Configure a descrição do grupo com o texto gerado (grupo silencioso com conteúdo gratuito)"),
                    ("Hoje", "Cadastre o e-book principal + 3 bônus na Monetizze como produto"),
                    (f"Hoje", f"Defina o preço: R${d.get('preco', 47)} e configure o checkout"),
                    ("Hoje", "Copie o link da Monetizze e salve — você vai precisar dele no dia do lançamento"),
                    ("Hoje", "Suba o anúncio no Facebook/Instagram usando o copy gerado"),
                    ("Hoje", "Aponte o anúncio para o link do grupo (WhatsApp/Telegram)"),
                    ("Hoje", "Configure a landing page e aponte o CTA para o link do grupo"),
                ]
            },
            {
                "fase": "FASE 2 — DIAS 1 A 7: Encher o grupo",
                "cor": "#8B5CF6",
                "items": [
                    ("Dias 1 a 7", "Anúncio rodando — objetivo: 500 a 1.000 pessoas no grupo"),
                    ("Diariamente", "Monitore o custo por lead nos anúncios (meta: até R$2,00 por pessoa)"),
                    ("Dica", "Se o custo estiver alto, teste uma imagem diferente ou ajuste o texto do anúncio"),
                    (f"{data_bv_ck}", "Envie a Mensagem 1 (boas-vindas) — primeira comunicação com o grupo"),
                    ("Importante", "NÃO mencione produto, preço ou venda — só boas-vindas e entrega de valor gratuito"),
                ]
            },
            {
                "fase": f"FASE 3 — AQUECIMENTO ({data_aq1_ck} a {data_aq5_ck}): 5 Mini-aulas de valor",
                "cor": "#7C3AED",
                "items": [
                    (f"{data_aq1_ck} — Dia 1", "Envie a Mini-aula 1 no grupo — conteúdo gratuito, sem mencionar venda"),
                    (f"{data_aq2_ck} — Dia 2", "Envie a Mini-aula 2 — responda dúvidas e gere engajamento"),
                    (f"{data_aq3_ck} — Dia 3 / Desafio", f"Envie a Mini-aula 3 + Mensagem 2 (Desafio Interativo) — peça para responderem no grupo"),
                    (f"{data_aq4_ck} — Dia 4", "Envie a Mini-aula 4 — o grupo já confia em você, crie mais expectativa"),
                    (f"{data_aq5_ck} — Dia 5", "Envie a Mini-aula 5 — última antes do lançamento, gancho forte para o dia seguinte"),
                    ("Durante o aquecimento", "Interaja com quem responde — isso aumenta a taxa de abertura das mensagens seguintes"),
                ]
            },
            {
                "fase": f"FASE 4 — VÉSPERA ({data_vespera_ck}): Aquecimento máximo",
                "cor": "#F59E0B",
                "items": [
                    (f"{data_vespera_ck}", "Envie a Mensagem 3 (aquecimento/véspera) — crie expectativa máxima, sem revelar produto"),
                    (f"{data_vespera_ck}", "Confirme se o link da Monetizze está funcionando corretamente"),
                    (f"{data_vespera_ck}", "Teste o checkout com um valor simbólico para garantir que está tudo ok"),
                    (f"{data_vespera_ck}", "Prepare-se para estar disponível amanhã para responder dúvidas em tempo real"),
                ]
            },
            {
                "fase": f"FASE 5 — DIA DO LANÇAMENTO ({data_lancto_fmt}): VENDER",
                "cor": "#F43F5E",
                "items": [
                    (f"{data_lancto_fmt} — manhã", "Envie a Mensagem 4 (lançamento) com o link da Monetizze para o grupo"),
                    (f"{data_lancto_fmt}", "Pause o anúncio de captação ou redirecione para a página de venda direta"),
                    (f"{data_lancto_fmt}", "Fique online para responder dúvidas rapidamente no grupo e no direct"),
                    (f"{data_lancto_fmt} — tarde", "Envie um lembrete de urgência: 'Restam poucas horas para garantir o preço de lançamento'"),
                    (f"{data_lancto_fmt} — noite", "Último lembrete: 'Meia-noite o preço muda. Última chance.'"),
                    (f"{data_lancto_fmt}", "Comemore cada venda — você construiu isso do zero!"),
                ]
            },
            {
                "fase": "FASE 6 — PÓS-LANÇAMENTO: Analisar e escalar",
                "cor": "#22C55E",
                "items": [
                    ("Após lançamento", "Anote: quantas pessoas no grupo, quantas compraram, qual foi a taxa de conversão"),
                    ("Após lançamento", "Calcule o ROI: faturamento ÷ custo de tráfego"),
                    ("Próximos dias", "Entregue o e-book e os bônus para quem comprou — cumpra a promessa com excelência"),
                    ("Próxima semana", "O grupo continua ativo — use a base para o próximo lançamento sem custo de tráfego"),
                    ("Próximo lançamento", "Repita o processo: novo produto para a mesma base ou novo nicho com nova audiência"),
                    ("Dica de escala", "Com o ROI positivo, aumente o orçamento de tráfego no próximo ciclo"),
                ]
            },
        ]

        for fase in fases:
            st.markdown(f"""
            <div style="margin:18px 0 8px 0;padding:8px 14px;background:{fase['cor']};border-radius:8px;color:white;font-weight:600;font-size:0.85em;letter-spacing:0.5px">
                {fase['fase']}
            </div>
            """, unsafe_allow_html=True)
            for quando, acao in fase['items']:
                st.markdown(f"""
                <div class="checklist-item">
                    <div style="width:10px;height:10px;border-radius:50%;background:{fase['cor']};margin-top:5px;flex-shrink:0"></div>
                    <div>
                        <div style="font-size:0.72em;color:#64748B;font-weight:600;text-transform:uppercase;letter-spacing:0.5px">{quando}</div>
                        <div style="font-size:0.92em;color:#1E293B">{acao}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # --- CALCULADORA ---
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

    # --- LAUNCERBOT ---
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
