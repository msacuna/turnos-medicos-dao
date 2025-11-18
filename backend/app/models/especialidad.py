from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models import Base

class Especialidad(Base):
    __tablename__ = 'especialidad'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)

    profesionales = relationship("Profesional", back_populates="especialidad")
    turnos = relationship("Turno", back_populates="especialidad")