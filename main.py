from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import uuid

app = FastAPI()

# Simulando banco de dados em memória
postos = {
    "posto1": {"id": "posto1", "cidade": "Joao Pessoa", "reservado": False, "reserva_ate": None},
    "posto2": {"id": "posto2", "cidade": "Maceio", "reservado": False, "reserva_ate": None},
    "posto3": {"id": "posto3", "cidade": "Sergipe", "reservado": False, "reserva_ate": None},
}

class ReservaRequest(BaseModel):
    id_carro: str
    id_posto: str
    duracao_min: int  # tempo que precisa reservar

class CancelamentoRequest(BaseModel):
    id_posto: str

@app.get("/postos_disponiveis")
def listar_postos():
    livres = [p for p in postos.values() if not p["reservado"] or (p["reserva_ate"] and p["reserva_ate"] < datetime.now())]
    return {"postos_livres": livres}

@app.post("/reservar_posto")
def reservar_posto(req: ReservaRequest):
    posto = postos.get(req.id_posto)
    if not posto:
        raise HTTPException(status_code=404, detail="Posto nao encontrado")

    if posto["reservado"] and posto["reserva_ate"] > datetime.now():
        raise HTTPException(status_code=409, detail="Posto já reservado")

    posto["reservado"] = True
    posto["reserva_ate"] = datetime.now() + timedelta(minutes=req.duracao_min)
    return {"mensagem": "Reserva efetuada", "reserva_valida_ate": posto["reserva_ate"]}

@app.post("/cancelar_reserva")
def cancelar_reserva(req: CancelamentoRequest):
    posto = postos.get(req.id_posto)
    if not posto:
        raise HTTPException(status_code=404, detail="Posto nao encontrado")
    
    posto["reservado"] = False
    posto["reserva_ate"] = None
    return {"mensagem": "Reserva cancelada"}
