from fastapi import FastAPI
from routers import reserva
from empresa import Empresa

app = FastAPI()

empresa = Empresa(nome="Empresa C", localizacao="Feira de Santana")
reserva.set_empresa(empresa)
app.include_router(reserva.router)
