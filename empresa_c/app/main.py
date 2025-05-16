from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
import httpx

app = FastAPI()

EMPRESA_NOME = "Empresa C"
EMPRESA_LOCAL = "Sergipe"
EMPRESA_PONTOS = ["SE2", "FS1"]

pontos: Dict[str, Dict] = {
    ponto: {"reservado": False, "carro": None} for ponto in EMPRESA_PONTOS
}

class ReservaRequest(BaseModel):
    ponto: str
    carro_id: str

@app.get("/pontos")
def listar_pontos():
    return {
        "empresa": EMPRESA_NOME,
        "local": EMPRESA_LOCAL,
        "pontos": pontos
    }

@app.post("/reserva")
def reservar_ponto(req: ReservaRequest):
    if req.ponto not in pontos:
        raise HTTPException(status_code=404, detail="Ponto não encontrado")

    if pontos[req.ponto]["reservado"]:
        raise HTTPException(status_code=400, detail="Ponto já reservado")

    pontos[req.ponto] = {"reservado": True, "carro": req.carro_id}
    return {"mensagem": f"Ponto {req.ponto} reservado com sucesso para {req.carro_id}"}

@app.post("/cancelar_reserva")
def cancelar_reserva(req: ReservaRequest):
    if req.ponto not in pontos:
        raise HTTPException(status_code=404, detail="Ponto não encontrado")

    if not pontos[req.ponto]["reservado"]:
        raise HTTPException(status_code=400, detail="Ponto já está livre")

    if pontos[req.ponto]["carro"] != req.carro_id:
        raise HTTPException(status_code=403, detail="Reserva feita por outro carro")

    pontos[req.ponto] = {"reservado": False, "carro": None}
    return {"mensagem": f"Reserva cancelada para ponto {req.ponto}"}
