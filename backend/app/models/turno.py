from sqlalchemy import CheckConstraint, Column, Integer, ForeignKey, Date, Time
from sqlalchemy.orm import relationship
from app.models import Base

class Turno(Base):
    __tablename__ = "turno"

    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(Date, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fin_estimada = Column(Time, nullable=False)
    dni_paciente = Column(Integer, ForeignKey("paciente.dni"), nullable=False)
    id_estado = Column(Integer, ForeignKey("estado_turno.id"), nullable=False)
    id_especialidad = Column(Integer, ForeignKey("especialidad.id"), nullable=False)
    id_agenda_profesional = Column(Integer, ForeignKey("agenda_profesional.id"), nullable=False)

    __table_args__ = (
        CheckConstraint('hora_fin_estimada > hora_inicio', name='chk_hora_fin_mayor_hora_inicio'),
    )

    # Relaciones directas
    paciente = relationship("Paciente", back_populates="turnos")
    estado = relationship("EstadoTurno", back_populates="turnos")
    especialidad = relationship("Especialidad", back_populates="turnos")
    agenda_profesional = relationship("AgendaProfesional", back_populates="turnos")

    consultas = relationship("Consulta", back_populates="turno")