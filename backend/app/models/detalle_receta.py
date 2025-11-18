from sqlalchemy import Column, Integer, ForeignKey, String, CheckConstraint
from sqlalchemy.orm import relationship
from app.models import Base


class DetalleReceta(Base):
    __tablename__ = "detalle_receta"

    # Clave primaria compuesta según BD: (item, id_receta)
    item = Column(Integer, primary_key=True, autoincrement=True)
    id_receta = Column(Integer, ForeignKey("receta.id"), primary_key=True, nullable=False)
    
    id_medicamento = Column(Integer, ForeignKey("medicamento.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    indicaciones = Column(String(255), nullable=True)

    __table_args__ = (
        CheckConstraint('cantidad > 0', name='chk_cantidad_positiva'),
    )

    # Relaciones directas
    receta = relationship("Receta", back_populates="detalles_receta")
    medicamento = relationship("Medicamento", back_populates="detalles_receta")