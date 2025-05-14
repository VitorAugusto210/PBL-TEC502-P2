from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

class PontoDeRecarga(Base):
    __tablename__ = "pontos_de_recarga"

    id = Column(Integer, primary_key=True, index=True)
    cidade = Column(String, index=True)
    estado = Column(String)
    ocupado = Column(Boolean, default=False)