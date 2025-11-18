from sqlalchemy import CheckConstraint, Column, Integer, Time, Enum
from sqlalchemy.orm import relationship
from app.models import Base
import enum

# Crear enum de Python
class DiaSemana(enum.Enum):
    LUNES = 'Lunes'
    MARTES = 'Martes'
    MIERCOLES = 'Miercoles'
    JUEVES = 'Jueves'
    VIERNES = 'Viernes'
    SABADO = 'Sabado'

class HorarioAtencion(Base):
    __tablename__ = 'horario_atencion'

    id = Column(Integer, primary_key=True, autoincrement=True)
    dia_semana = Column(Enum(DiaSemana), nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)

    __table_args__ = (
        CheckConstraint('hora_fin > hora_inicio', name='chk_hora_fin_mayor_hora_inicio'),
    )

    # Relaciones directas
    horario_profesionales = relationship("HorarioProfesional", back_populates="horario_atencion")

    # Acceder directamente a los profesionales con horario vigente
    @property
    def profesionales_vigentes(self):
        return [hp.profesional for hp in self.horario_profesionales if hp.vigente]