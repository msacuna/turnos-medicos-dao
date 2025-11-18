from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models import Base

class Medicamento(Base):
    __tablename__ = "medicamento"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255), nullable=True)

    # Relaciones Many-to-Many
    laboratorios = relationship(
        "Laboratorio",
        secondary="medicamento_laboratorio",
        back_populates="medicamentos"
    )

    detalles_receta = relationship("DetalleReceta", back_populates="medicamento")