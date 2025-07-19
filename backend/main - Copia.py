from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import datetime
import sys
import os

# Adiciona o diretório scripts ao path para importar astro
scripts_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts'))
if scripts_dir not in sys.path:
    sys.path.append(scripts_dir)

try:
    from astro import get_transits
except ImportError:
    get_transits = None

app = FastAPI(title="HoloFractal API")

class IdentifyPayload(BaseModel):
    astro_chart: dict = None  # espera {'date': 'YYYY-MM-DD'}
    hrv_data: list = None
    archetype_answers: list = None

@app.post("/identify")
async def identify(payload: IdentifyPayload):
    # Valida payload
    if payload.astro_chart is None or 'date' not in payload.astro_chart:
        raise HTTPException(status_code=400, detail="astro_chart.date é obrigatório no formato YYYY-MM-DD")

    # Converte data
    try:
        date = datetime.datetime.strptime(payload.astro_chart['date'], "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de data inválido, use YYYY-MM-DD")

    # Gera trânsitos se módulo estiver disponível
    transits = None
    if get_transits:
        transits = get_transits(date)

    # Monta resposta
    response = {
        "status": "received",
        "payload": payload.dict(),
        "transits": transits,
    }
    return response

@app.get("/health")
async def health():
    return {"status": "ok"}
