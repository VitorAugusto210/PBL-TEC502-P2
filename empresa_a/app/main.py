from fastapi import FastAPI
from routers import reserva
from empresa import Empresa

app = FastAPI()

empresa = Empresa(nome="Empresa A", localizacao="João Pessoa", pontos=["SE2", "FS1"])
reserva.set_empresa(empresa)
app.include_router(reserva.router)
