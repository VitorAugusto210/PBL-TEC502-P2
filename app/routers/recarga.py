from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/disponiveis", response_model=list[schemas.PontoDeRecarga])
def listar_disponiveis(db: Session = Depends(get_db)):
    return db.query(models.PontoDeRecarga).filter_by(ocupado=False).all()

@router.post("/reservar/{ponto_id}", response_model=schemas.PontoDeRecarga)
def reservar_ponto(ponto_id: int, db: Session = Depends(get_db)):
    ponto = db.query(models.PontoDeRecarga).filter_by(id=ponto_id).first()
    if not ponto:
        raise HTTPException(status_code=404, detail="Ponto não encontrado")
    if ponto.ocupado:
        raise HTTPException(status_code=400, detail="Ponto já ocupado")
    ponto.ocupado = True
    db.commit()
    db.refresh(ponto)
    return ponto

@router.post("/criar", response_model=schemas.PontoDeRecarga)
def criar_ponto(ponto: schemas.PontoDeRecargaCreate, db: Session = Depends(get_db)):
    novo = models.PontoDeRecarga(cidade=ponto.cidade, estado=ponto.estado)
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo