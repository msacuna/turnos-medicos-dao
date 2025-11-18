from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models import Base

class GrupoSanguineo(Base):
    __tablename__ = "grupo_sanguineo"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(5), nullable=False, unique=True)

    # Relaciones inversas
    pacientes = relationship("Paciente", back_populates="grupo_sanguineo")