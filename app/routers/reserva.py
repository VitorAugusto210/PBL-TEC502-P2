import requests
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

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

class TrechoRota(BaseModel):
    empresa_url: str
    ponto_id: str
    janela_inicio: str
    janela_fim: str

class RotaRequest(BaseModel):
    carro_id: str
    roteiro: List[TrechoRota] 

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

@router.post("/reserva/rota")
def reservar_rota(req: RotaRequest):
    reservas_confirmadas = []
    for trecho in req.roteiro:
        try:
            resposta = requests.post(
                f"{trecho.empresa_url}/reserva",
                json={
                    "carro_id": req.carro_id,
                    "ponto_id": trecho.ponto_id,
                    "janela_inicio": trecho.janela_inicio,
                    "janela_fim": trecho.janela_fim
                },
                timeout=5
            )

            if resposta.status_code != 200:
                raise Exception(f"Falha em {trecho.empresa_url}")

            reservas_confirmadas.append(trecho)

        except Exception as e:
            for r in reservas_confirmadas:
                try:
                    requests.post(
                        f"{r.empresa_url}/cancelar",
                        json={"carro_id": req.carro_id, "ponto_id": r.ponto_id},
                        timeout=5
                    )
                except:
                    pass 
            return {"erro": f"Reserva falhou em {trecho.empresa_url}. Rollback realizado."}

    return {"mensagem": "Rota reservada com sucesso", "reservas": [r.dict() for r in reservas_confirmadas]}
