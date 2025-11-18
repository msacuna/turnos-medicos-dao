from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models import Base


class Laboratorio(Base):
    __tablename__ = "laboratorio"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)

    # Relaciones Many-to-Many
    medicamentos = relationship(
        "Medicamento",
        secondary="medicamento_laboratorio",
        back_populates="laboratorios"
    )