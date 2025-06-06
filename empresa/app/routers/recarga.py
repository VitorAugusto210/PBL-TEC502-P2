from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.blockchain_service import blockchain_service

router = APIRouter()

class RechargeRequest(BaseModel):
    session_id: int
    energy_consumed: int # Em Wh
    cost: int # Em Wei

@router.post("/finalizar-recarga")
def finish_recharge(request: RechargeRequest):
    try:
        blockchain_service.finish_recharge(request.session_id, request.energy_consumed, request.cost)
        return {"message": "Recharge finished and registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class PaymentRequest(BaseModel):
    session_id: int
    value: int # Em Wei

@router.post("/pagamento")
def make_payment(request: PaymentRequest):
    try:
        blockchain_service.make_payment(request.session_id, request.value)
        return {"message": "Payment made successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))