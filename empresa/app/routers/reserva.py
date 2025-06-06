from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.core.blockchain_service import BlockchainService

router = APIRouter()

class ReservationRequest(BaseModel):
    user_address: str
    station_id: int
try:
    blockchain_service_instance = BlockchainService()
except Exception as e:
    print(f"ERRO CRÍTICO ao inicializar o BlockchainService: {e}")
    blockchain_service_instance = None
    
def get_blockchain_service():
    if blockchain_service_instance is None:
        # Se o serviço não pôde ser criado, a API vai retornar um erro claro.
        raise RuntimeError("BlockchainService não está disponível.")
    return blockchain_service_instance

@router.post("/reserva")
def create_reserva(
    request: ReservationRequest, 
    blockchain_service: BlockchainService = Depends(get_blockchain_service)
):
    try:
        session_id = blockchain_service.create_reservation(request.user_address, request.station_id)
        return {"message": "Reservation created successfully on blockchain", "session_id": session_id}
    except Exception as e:
        # Captura exceções e retorna um erro HTTP claro
        raise HTTPException(status_code=500, detail=str(e))