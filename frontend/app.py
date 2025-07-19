import streamlit as st
import requests
from datetime import datetime

# --- Configurações iniciais ---
st.set_page_config(page_title="HoloFractal MVP", layout="wide")
st.markdown("# 🔍 Coleta & Diagnóstico — MVP")

# Estado
if 'step' not in st.session_state:
    st.session_state.step = 'identify'
if 'session_id' not in st.session_state:
    st.session_state.session_id = None
if 'logs' not in st.session_state:
    st.session_state.logs = []

def log_call(endpoint, status):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    st.session_state.logs.append({'time': ts, 'route': endpoint, 'status': status})

with st.sidebar:
    st.markdown("## 📝 Histórico de Sessão")
    for e in st.session_state.logs:
        st.write(f"{e['time']} — `{e['route']}` — {e['status']}")

def validate_identify(data):
    missing = []
    if not data['astro_chart']['date']:   missing.append('Data')
    if not data['astro_chart']['time']:   missing.append('Hora')
    if not data['astro_chart']['place']:  missing.append('Local')
    if not data['hrv_data']:              missing.append('HRV')
    if not data['archetype_answers']:     missing.append('Arquétipos')
    return missing

# 1) Identify
if st.session_state.step == 'identify':
    with st.form('f1'):
        birth = st.date_input("Data de Nascimento")
        time_ = st.time_input("Hora de Nascimento")
        place = st.text_input("Local (cidade, país)")
        hrv = st.text_area("HRV (JSON array ou CSV)")
        arche = st.multiselect("Arquétipos", ["Vítima","Herói","Sábio","Rebelde"])
        if st.form_submit_button("Enviar /identify"):
            payload = {"astro_chart": {"date":str(birth),"time":str(time_),"place":place}, "hrv_data":hrv, "archetype_answers":arche}
            m = validate_identify(payload)
            if m:
                st.warning("Preencha: " + ", ".join(m))
            else:
                try:
                    res = requests.post("http://localhost:8000/identify", json=payload, timeout=10)
                    res.raise_for_status()
                    st.success("Identify OK")
                    st.json(res.json())
                    log_call('/identify','ok')
                    st.session_state.step = 'configure'
                except Exception as ex:
                    st.error(f"Erro: {ex}")
                    log_call('/identify','error')

# 2) Configure
elif st.session_state.step == 'configure':
    st.markdown("## 🔧 2. Configure")
    with st.form('f2'):
        sid = st.text_input("Session ID (deixe em branco para novo)", value=st.session_state.session_id or "")
        goals = st.multiselect("Objetivos", ["Prosperidade","Cura","Insight"])
        keys  = st.multiselect("Chaves Prioritárias", list(range(1,12)))
        if st.form_submit_button("Enviar /configure"):
            payload = {"session_id":sid or None,"goals":goals,"priority_keys":keys}
            try:
                res = requests.post("http://localhost:8000/configure", json=payload, timeout=10)
                res.raise_for_status()
                data = res.json()
                st.success("Configure OK")
                st.write("Session ID:", data['session_id'])
                log_call('/configure','ok')
                st.session_state.session_id = data['session_id']
                st.session_state.step = 'execute'
            except Exception as ex:
                st.error(f"Erro: {ex}")
                log_call('/configure','error')

# 3) Execute
elif st.session_state.step == 'execute':
    st.markdown("## ▶️ 3. Execute")
    if st.button("Iniciar /execute"):
        try:
            res = requests.post("http://localhost:8000/execute", json={"session_id":st.session_state.session_id}, timeout=10)
            res.raise_for_status()
            st.success("Execute OK")
            st.json(res.json())
            log_call('/execute','ok')
            st.session_state.step = 'alter'
        except Exception as ex:
            st.error(f"Erro: {ex}")
            log_call('/execute','error')

# 4) Alter
elif st.session_state.step == 'alter':
    st.markdown("## ✨ 4. Alter")
    if st.button("Gerar Fractal"):
        try:
            res = requests.post("http://localhost:8000/alter", json={"session_id":st.session_state.session_id}, timeout=10)
            res.raise_for_status()
            data = res.json()
            st.success("Alter OK — baixe SVG abaixo")
            st.download_button("Download SVG", data=data['fractal_svg'], file_name="fractal.svg", mime="image/svg+xml")
            log_call('/alter','ok')
        except Exception as ex:
            st.error(f"Erro: {ex}")
            log_call('/alter','error')

else:
    st.write("✅ Fluxo concluído! Reinicie o app para começar de novo.")
