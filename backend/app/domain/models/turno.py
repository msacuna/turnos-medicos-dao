from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from pydantic import model_validator
from datetime import date, time
from .estado_turno import EstadoTurnoEnum

if TYPE_CHECKING:
    from .paciente import Paciente
    from .estado_turno import EstadoTurno
    from .especialidad import Especialidad
    from .agenda_profesional import AgendaProfesional
    from .consulta import Consulta

class Turno(SQLModel, table=True):
    __tablename__ = "turno" # type: ignore
    id: Optional[int] = Field(default=None, primary_key=True)
    fecha: date
    hora_inicio: time
    hora_fin_estimada: time
    dni_paciente: int = Field(foreign_key="paciente.dni")
    nombre_estado: EstadoTurnoEnum = Field(foreign_key="estado_turno.nombre", default=EstadoTurnoEnum.AGENDADO)
    id_especialidad: int = Field(foreign_key="especialidad.id")
    id_agenda_profesional: int = Field(foreign_key="agenda_profesional.id")

    paciente: Optional["Paciente"] = Relationship(back_populates="turnos")
    estado: Optional["EstadoTurno"] = Relationship(back_populates="turnos")
    especialidad: Optional["Especialidad"] = Relationship(back_populates="turnos")
    agenda_profesional: Optional["AgendaProfesional"] = Relationship(back_populates="turnos")
    consultas: list["Consulta"] = Relationship(back_populates="turno")

    @model_validator(mode="after")
    def validar_rango_horario(self):
        if self.hora_fin_estimada <= self.hora_inicio:
            raise ValueError("hora_fin_estimada debe ser mayor que hora_inicio")
        return self