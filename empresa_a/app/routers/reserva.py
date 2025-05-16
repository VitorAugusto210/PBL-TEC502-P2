from fastapi import APIRouter
from pydantic import BaseModel
import requests

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

@router.post("/rota")
def reservar_rota(reqs: list[ReservaRequest]):
    respostas = []
    try:
        for req in reqs:
            # Suponha que o campo ponto_id venha com uma URL base da empresa, como:
            # http://empresa_a:8000, http://empresa_b:8000 etc
            base_url = req.ponto_id.split("#")[0]
            ponto = req.ponto_id.split("#")[1]

            data = {
                "carro_id": req.carro_id,
                "ponto_id": ponto,
                "janela_inicio": req.janela_inicio,
                "janela_fim": req.janela_fim
            }
            res = requests.post(f"{base_url}/reserva", json=data)
            if res.status_code != 200:
                raise Exception(res.json())
            respostas.append((base_url, ponto))
        return {"status": "toda_rota_reservada"}

    except Exception as e:
        # rollback
        for base_url, ponto in respostas:
            requests.post(f"{base_url}/cancelar", json={
                "carro_id": reqs[0].carro_id,
                "ponto_id": ponto
            })
        return {"erro": "Reserva falhou, rollback executado", "detalhes": str(e)}


@router.post("/cancelar")
def cancelar_reserva(req: CancelarRequest):
    return empresa.cancelar_reserva(req.carro_id, req.ponto_id)

@router.post("/disponibilidade")
def consultar_disponibilidade(req: DisponibilidadeRequest):
    return empresa.verificar_disponibilidade(req.ponto_id, req.janela_inicio, req.janela_fim)