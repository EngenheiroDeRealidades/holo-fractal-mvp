# 🧿 HoloFractal MVP — Portal Hacker-Místico

Este é o projeto HoloFractal: uma interface interdimensional que coleta dados astrais, bioenergéticos e simbólicos para gerar uma assinatura fractal única.  
Rodando como aplicativo web com interface visual em **Streamlit**, e lógica backend via **FastAPI**.

---

## 🔮 Funcionalidades

- Coleta de dados astrológicos e HRV
- Escolha de arquétipos e chaves simbólicas
- Sessões com identificação única
- Geração de fractal personalizado (SVG)
- Interface narrativa com estética hacker-mística

---

## 🚀 Como rodar localmente

```bash
cd holo-fractal-mvp
python -m venv .venv
source .venv/bin/activate        # ou .venv\Scripts\Activate.ps1 no Windows
pip install -r requirements.txt

# Iniciar backend:
uvicorn backend.main:app --reload

# Iniciar frontend:
streamlit run frontend/app.py
