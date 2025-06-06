from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.core.blockchain_service import BlockchainService

router = APIRouter()

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


class RechargeRequest(BaseModel):
    session_id: int
    energy_consumed: int
    cost: int

class PaymentRequest(BaseModel):
    session_id: int
    value: int

@router.post("/finalizar-recarga")
def finish_recharge(
    request: RechargeRequest, 
    blockchain_service: BlockchainService = Depends(get_blockchain_service)
):
    try:
        blockchain_service.finish_recharge(request.session_id, request.energy_consumed, request.cost)
        return {"message": "Recharge finished and registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/pagamento")
def make_payment(
    request: PaymentRequest, 
    blockchain_service: BlockchainService = Depends(get_blockchain_service)
):
    try:
        blockchain_service.make_payment(request.session_id, request.value)
        return {"message": "Payment made successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))