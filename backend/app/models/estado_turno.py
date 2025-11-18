from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models import Base

class EstadoTurno(Base):
    __tablename__ = 'estado_turno'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True) # Podría ser la PK

    turnos = relationship("Turno", back_populates="estado")