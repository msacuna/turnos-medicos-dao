from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.models import Base


class Consulta(Base):
    __tablename__ = 'consulta'

    id = Column(Integer, primary_key=True, autoincrement=True)
    observaciones = Column(String(255), nullable=True)
    id_turno = Column(Integer, ForeignKey("turno.id"), nullable=False)
    id_motivo_consulta = Column(Integer, ForeignKey("motivo_consulta.id"), nullable=False)
    id_receta = Column(Integer, ForeignKey("receta.id"), nullable=True)

    # Relaciones directas
    turno = relationship("Turno", back_populates="consulta")
    receta = relationship("Receta", back_populates="consulta")
    motivo_consulta = relationship("MotivoConsulta", back_populates="consulta")