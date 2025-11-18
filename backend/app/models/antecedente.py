from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models import Base

class Antecedente(Base):
    __tablename__ = "antecedente"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)

    # Relaciones Many-to-Many
    pacientes = relationship(
        "Paciente",
        secondary="paciente_antecedente",
        back_populates="antecedentes"
    )