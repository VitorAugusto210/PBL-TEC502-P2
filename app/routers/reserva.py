from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()
empresa = None

def set_empresa(e):
    global empresa
    empresa = e

class ReservaRequest(BaseModel):
    carro_id: str
    ponto_id: str
    janela_inicio: str
    janela_fim: str

class CancelarRequest(BaseModel):
    carro_id: str
    ponto_id: str

class DisponibilidadeRequest(BaseModel):
    ponto_id: str
    janela_inicio: str
    janela_fim: str

@router.post("/reserva")
def reservar_ponto(req: ReservaRequest):
    return empresa.reservar_ponto(
        req.carro_id, req.ponto_id, req.janela_inicio, req.janela_fim
    )

@router.get("/reservas")
def listar_reservas():
    return empresa.consultar_reservas()

@router.post("/cancelar")
def cancelar_reserva(req: CancelarRequest):
    return empresa.cancelar_reserva(req.carro_id, req.ponto_id)

@router.post("/disponibilidade")
def consultar_disponibilidade(req: DisponibilidadeRequest):
    return empresa.verificar_disponibilidade(req.ponto_id, req.janela_inicio, req.janela_fim)

