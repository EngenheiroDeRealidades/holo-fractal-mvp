from typing import List, Optional
import uuid
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="HoloFractal API")

# Memória simples de sessões em memória
SESSIONS: dict[str, dict] = {}

# Payload para coleta/diagnóstico existente
class IdentifyPayload(BaseModel):
    astro_chart: dict = None
    hrv_data: list = None
    archetype_answers: list = None

@app.post("/identify")
async def identify(payload: IdentifyPayload):
    return {"status": "received", "payload": payload}

# Health check
@app.get("/health")
async def health():
    return {"status": "ok"}

# Novo payload para configuração de sessão
class ConfigurePayload(BaseModel):
    session_id: Optional[str] = None
    goals: List[str]
    priority_keys: List[int]

@app.post("/configure")
async def configure(payload: ConfigurePayload):
    # Gera ou reutiliza session_id
    sid = payload.session_id or str(uuid.uuid4())
    session = payload.dict()
    session["session_id"] = sid
    SESSIONS[sid] = session
    return {"status": "configured", "session_id": sid, "session": session}

# (Próximos endpoints: /execute, /alter, etc.)
