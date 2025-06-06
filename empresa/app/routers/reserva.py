from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.blockchain_service import blockchain_service

router = APIRouter()

class ReservationRequest(BaseModel):
    user_address: str
    station_id: int

@router.post("/reserva")
def create_reserva(request: ReservationRequest):
    try:
        session_id = blockchain_service.create_reservation(request.user_address, request.station_id)
        return {"message": "Reservation created successfully on blockchain", "session_id": session_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))