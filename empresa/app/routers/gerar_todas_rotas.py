from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter()

class Localizacao(BaseModel):
    latitude: float
    longitude: float

class RotaRequest(BaseModel):
    localizacao_atual: Localizacao
    localizacao_destino: Localizacao

# O endpoint original foi mantido, mas agora dentro de um router
@router.post("/gerar_rota")
def gerar_rota(data: RotaRequest):
    # A lógica de geração de rota continua a mesma
    # Aqui, apenas retornamos um exemplo estático como no original
    return {
        "rota": f"Rota de {data.localizacao_atual} para {data.localizacao_destino}"
    }

# Mantive a função original de gerar todas as rotas se você precisar dela
# mas ela não é mais usada diretamente como um endpoint aqui.
def gerar_todas_rotas(carros, empresa):
    todas_rotas = []
    for carro in carros:
        rota = empresa.gerar_rota(carro.localizacao_atual, carro.localizacao_destino)
        todas_rotas.append(rota)
    return todas_rotas