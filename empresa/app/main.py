from fastapi import FastAPI, Depends
from app.core.blockchain_service import BlockchainService
from app.routers import reserva, gerar_todas_rotas, recarga

# --- LÓGICA DE INICIALIZAÇÃO CORRIGIDA ---

# 1. Tenta criar a instância do serviço de blockchain.
#    Colocamos em um try/except para lidar com o caso de o blockchain não estar pronto.
try:
    blockchain_service_instance = BlockchainService()
except Exception as e:
    print(f"ERRO CRÍTICO ao inicializar o BlockchainService: {e}")
    blockchain_service_instance = None

# 2. Função que o FastAPI usará para injetar a dependência.
def get_blockchain_service():
    if blockchain_service_instance is None:
        # Se o serviço não pôde ser criado, a API vai retornar um erro claro.
        raise RuntimeError("BlockchainService não está disponível.")
    return blockchain_service_instance

# 3. Cria a aplicação FastAPI.
app = FastAPI()

# 4. Inclui os roteadores, passando a dependência para os que precisam do blockchain.
app.include_router(
    reserva.router,
    tags=["Blockchain"],
    dependencies=[Depends(get_blockchain_service)]
)
app.include_router(
    gerar_todas_rotas.router,
    tags=["Rotas"]
)
app.include_router(
    recarga.router,
    tags=["Blockchain"],
    dependencies=[Depends(get_blockchain_service)]
)

@app.get("/")
def read_root():
    return {"message": "Empresa Service is running"}