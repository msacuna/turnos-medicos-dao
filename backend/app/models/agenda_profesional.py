from sqlalchemy import CheckConstraint, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models import Base


class AgendaProfesional(Base):
    __tablename__ = "agenda_profesional"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_profesional = Column(Integer, ForeignKey("profesional.id"), nullable=False)
    anio = Column(Integer, nullable=False)
    mes = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint('mes >= 1 AND mes <= 12', name='chk_mes_valido'),
    )

    turnos = relationship("Turno", back_populates="agenda_profesional")

    # Relaciones directas
    profesional = relationship("Profesional", back_populates="agendas_profesionales")