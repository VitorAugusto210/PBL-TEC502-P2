# Dentro de empresa_comum/app/main.py
from fastapi import FastAPI
from routers import reserva  # Supondo que gerar_todas_rotas é usado por reserva.py
from empresa import Empresa
import os # Importe o módulo os

app = FastAPI()

# Ler configuracoes das variaveis de ambiente
NOME_EMPRESA = os.getenv("EMPRESA_NOME", "Empresa Desconhecida")
LOCALIZACAO_EMPRESA = os.getenv("EMPRESA_LOCAL", "Local Desconhecido")
# Para pontos, pode ser uma string JSON ou separada por virgulas
PONTOS_EMPRESA_STR = os.getenv("EMPRESA_PONTOS", '[]')
try:
    # Se for uma string JSON (ex: '["P1", "P2"]')
    import json
    PONTOS_EMPRESA = json.loads(PONTOS_EMPRESA_STR)
except json.JSONDecodeError:
    # Se for separada por virgulas (ex: 'P1,P2')
    PONTOS_EMPRESA = [p.strip() for p in PONTOS_EMPRESA_STR.split(',') if p.strip()]

empresa_obj = Empresa(nome=NOME_EMPRESA, localizacao=LOCALIZACAO_EMPRESA, pontos=PONTOS_EMPRESA)
reserva.set_empresa(empresa_obj) # A função set_empresa já existe nos seus routers/reserva.py
app.include_router(reserva.router)

# (Opcional) Adicionar um endpoint para verificar a configuracao da empresa
@app.get("/info")
async def info():
    return {
        "nome_empresa": NOME_EMPRESA,
        "localizacao": LOCALIZACAO_EMPRESA,
        "pontos": PONTOS_EMPRESA
    }