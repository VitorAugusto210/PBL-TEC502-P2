from fastapi import FastAPI
from routers import reserva
from empresa import Empresa
import json 
import os 

app = FastAPI()

nome        = os.getenv("EMPRESA_NOME", "Empresa Default")
cidade      = os.getenv("EMPRESA_LOCAL", "Cidade X")
pontos_json = os.getenv("EMPRESA_PONTOS", '[]')         
pontos      = json.loads(pontos_json)

empresa = Empresa(nome=nome, localizacao=cidade, pontos=pontos)
reserva.set_empresa(empresa)
app.include_router(reserva.router)
