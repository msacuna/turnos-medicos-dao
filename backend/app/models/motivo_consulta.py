from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models import Base

class MotivoConsulta(Base):
    __tablename__ = 'motivo_consulta'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)

    consultas = relationship("Consulta", back_populates="motivo_consulta")