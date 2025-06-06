from fastapi import FastAPI
from app.routers import reserva, gerar_todas_rotas, recarga # Adicionado recarga

app = FastAPI()

app.include_router(reserva.router)
app.include_router(gerar_todas_rotas.router)
app.include_router(recarga.router) # Adicionado o novo roteador

@app.get("/")
def read_root():
    return {"message": "Empresa Service is running"}