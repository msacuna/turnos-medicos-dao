from sqlalchemy import Column, Integer, Date, Boolean
from sqlalchemy.orm import relationship
from app.models import Base

class Receta(Base):
    __tablename__ = 'receta'

    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(Date, nullable=False)
    dispensada = Column(Boolean, nullable=False, default=False)

    detalles_receta = relationship("DetalleReceta", back_populates="receta")
    consultas = relationship("Consulta", back_populates="receta")