from pydantic import BaseModel

class PontoDeRecargaBase(BaseModel):
    cidade: str
    estado: str

class PontoDeRecargaCreate(PontoDeRecargaBase):
    pass

class PontoDeRecarga(PontoDeRecargaBase):
    id: int
    ocupado: bool

    class Config:
        orm_mode = True