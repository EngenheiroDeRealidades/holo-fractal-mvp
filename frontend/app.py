import streamlit as st
import requests
import os
from datetime import datetime

# 🔮 Estética dimensional
st.set_page_config(
    page_title="HoloFractal MVP",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🧿",
    theme={"base": "dark"}
)
st.markdown("# 🧿 Painel Fractal · MVP")

backend_url = os.environ.get("BACKEND_URL", "http://localhost:8000")

# 🌐 Estado da sessão
if 'step' not in st.session_state:
    st.session_state.step = 'identify'
if 'session_id' not in st.session_state:
    st.session_state.session_id = None
if 'logs' not in st.session_state:
    st.session_state.logs = []

def log_call(endpoint, status):
    ts = datetime.now().strftime('%H:%M:%S · %d/%m/%Y')
    st.session_state.logs.append({'time': ts, 'route': endpoint, 'status': status})

with st.sidebar:
    st.markdown("## ⏳ Sessão Interdimensional")
    for e in st.session_state.logs:
        st.write(f"🔸 `{e['time']}` — `{e['route']}` — {e['status']}")

def validate_identify(data):
    missing = []
    if not data['astro_chart']['date']:   missing.append('Data')
    if not data['astro_chart']['time']:   missing.append('Hora')
    if not data['astro_chart']['place']:  missing.append('Local')
    if not data['hrv_data']:              missing.append('HRV')
    if not data['archetype_answers']:     missing.append('Arquétipos')
    return missing

# 🧠 1) IDENTIFY
if st.session_state.step == 'identify':
    st.markdown("### 🌠 Invocação Inicial — Mapa Astral")
    with st.form('f1'):
        birth = st.date_input("📅 Data de Nascimento")
        time_ = st.time_input("⏰ Hora de Nascimento")
        place = st.text_input("🗺️ Local (cidade, país)")
        hrv = st.text_area("💓 HRV (JSON array ou CSV)")
        arche = st.multiselect("🔮 Arquétipos", ["Vítima","Herói","Sábio","Rebelde"])
        if st.form_submit_button("🌀 Invocar /identify"):
            payload = {
                "astro_chart": {
                    "date": str(birth),
                    "time": str(time_),
                    "place": place
                },
                "hrv_data": hrv,
                "archetype_answers": arche
            }
            missing = validate_identify(payload)
            if missing:
                st.warning("⚠️ Campos incompletos: " + ", ".join(missing))
            else:
                with st.spinner("🌌 Alinhando coordenadas cósmicas..."):
                    try:
                        res = requests.post(f"{backend_url}/identify", json=payload, timeout=10)
                        res.raise_for_status()
                        st.success("✅ Portal Astral Aberto")
                        st.json(res.json())
                        log_call("/identify", "ok")
                        st.session_state.step = 'configure'
                    except Exception as ex:
                        st.error(f"💥 Erro: {ex}")
                        log_call("/identify", "error")

# 🧬 2) CONFIGURE
elif st.session_state.step == 'configure':
    st.markdown("### ⚙️ Configuração Fractal")
    with st.form('f2'):
        sid = st.text_input("🆔 Session ID (deixe em branco para novo)", value=st.session_state.session_id or "")
        goals = st.multiselect("🎯 Objetivos", ["Prosperidade","Cura","Insight"])
        keys  = st.multiselect("🗝️ Chaves Prioritárias", list(range(1,12)))
        if st.form_submit_button("🧩 Codificar /configure"):
            payload = {
                "session_id": sid or None,
                "goals": goals,
                "priority_keys": keys
            }
            with st.spinner("🔧 Gravando frequências no núcleo simbólico..."):
                try:
                    res = requests.post(f"{backend_url}/configure", json=payload, timeout=10)
                    res.raise_for_status()
                    data = res.json()
                    st.success("✅ Frequência configurada")
                    st.write("🆔 Session ID:", data['session_id'])
                    st.session_state.session_id = data['session_id']
                    log_call("/configure", "ok")
                    st.session_state.step = 'execute'
                except Exception as ex:
                    st.error(f"💥 Erro: {ex}")
                    log_call("/configure", "error")

# ⚡ 3) EXECUTE
elif st.session_state.step == 'execute':
    st.markdown("### 🔱 Execução Energética")
    if st.button("🧠 Canalizar /execute"):
        with st.spinner("⚡ Conectando aos campos vibracionais..."):
            try:
                res = requests.post(
                    f"{backend_url}/execute",
                    json={"session_id": st.session_state.session_id},
                    timeout=10
                )
                res.raise_for_status()
                st.success("🧬 Diagnóstico energizado")
                st.json(res.json())
                log_call("/execute", "ok")
                st.session_state.step = 'alter'
            except Exception as ex:
                st.error(f"💥 Erro: {ex}")
                log_call("/execute", "error")

# 🔺 4) ALTER
elif st.session_state.step == 'alter':
    st.markdown("### 🌀 Geração de Fractal")
    if st.button("🔮 Gerar Fractal"):
        with st.spinner("✨ Analisando padrão geométrico da essência..."):
            try:
                res = requests.post(
                    f"{backend_url}/alter",
                    json={"session_id": st.session_state.session_id},
                    timeout=10
                )
                res.raise_for_status()
                data = res.json()
                st.success("🧿 Fractal gerado com sucesso")
                st.download_button(
                    label="📥 Baixar SVG Fractal",
                    data=data['fractal_svg'],
                    file_name="fractal.svg",
                    mime="image/svg+xml"
                )
                log_call("/alter", "ok")
            except Exception as ex:
                st.error(f"💥 Erro: {ex}")
                log_call("/alter", "error")

else:
    st.balloons()
    st.markdown("🎉 Ritual completo! Sua assinatura vibracional está disponível.")
