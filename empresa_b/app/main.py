from fastapi import FastAPI
from routers import reserva
from empresa import Empresa

app = FastAPI()

empresa = Empresa(nome="Empresa B", localizacao="Maceió", pontos=["MC1", "JP1"])
reserva.set_empresa(empresa)
app.include_router(reserva.router)
