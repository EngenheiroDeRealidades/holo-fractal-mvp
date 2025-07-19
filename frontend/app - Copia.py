import streamlit as st
import requests

st.set_page_config(page_title="HoloFractal MVP", layout="wide")
st.title("🔍 Coleta & Diagnóstico — MVP")

# 1) Astrologia
with st.expander("1. Dados Astrológicos", expanded=True):
    birth = st.date_input("Data de Nascimento")
    time  = st.time_input("Hora de Nascimento")
    place = st.text_input("Local (cidade, país)")

# 2) HRV
with st.expander("2. Dados Fisiológicos"):
    hrv = st.text_area("Cole a sequência de HRV (JSON ou CSV)")

# 3) Arquétipos
with st.expander("3. Questionário Arquetípico"):
    arche = st.multiselect(
        "Marque seus arquétipos ativos",
        ["Vítima", "Herói", "Sábio", "Rebelde"]
    )

if st.button("Enviar para API"):
    payload = {
        "astro_chart": {
            "date":  str(birth),
            "time":  str(time),
            "place": place
        },
        "hrv_data": hrv if hrv else [],
        "archetype_answers": arche
    }
    try:
        res = requests.post("http://localhost:8000/identify", json=payload)
        res.raise_for_status()
        data = res.json()
        # Exibe confirmação
        st.success("✅ Diagnóstico recebido com sucesso!")

        # Exibe payload enviado
        st.subheader("📤 Payload Enviado")
        st.json(data.get("payload", {}))

        # Exibe trânsitos astronômicos
        transits = data.get("transits")
        if transits:
            st.subheader("🌞 Trânsitos Astronômicos em {}".format(payload["astro_chart"]["date"]))
            sun = transits.get("sun")
            moon = transits.get("moon")
            st.markdown(f"**Sol**: {sun[0][0]:.2f}° (velocidade {sun[0][3]:.2f}°/dia)")
            st.markdown(f"**Lua**: {moon[0][0]:.2f}° (velocidade {moon[0][3]:.2f}°/dia)")
        else:
            st.info("⚠️ Módulo de trânsitos não disponível.")

    except requests.exceptions.RequestException as e:
        st.error(f"❌ Erro ao chamar API: {e}")
