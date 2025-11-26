from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from pydantic import model_validator
from datetime import time
from enum import Enum

if TYPE_CHECKING:
    from .profesional import Profesional

class DiaSemanaEnum(str, Enum):
    Lunes = 'Lunes'
    Martes = 'Martes'
    Miercoles = 'Miercoles'
    Jueves = 'Jueves'
    Viernes = 'Viernes'
    Sabado = 'Sabado'

class HorarioAtencion(SQLModel, table=True):
    __tablename__ = "horario_atencion" # type: ignore
    id: Optional[int] = Field(default=None, primary_key=True)
    dia_semana: DiaSemanaEnum = Field(index=True) # para busquedas rapidas
    hora_inicio: time
    hora_fin: time
    id_profesional: Optional[int] = Field(default=None, foreign_key="profesional.id")

    profesional: Optional["Profesional"] = Relationship(back_populates="horarios_atencion")

    @model_validator(mode="after")
    def validar_rango_horario(self):
        # 'self' ya tiene los datos cargados
        if self.hora_inicio >= self.hora_fin:
            raise ValueError("La hora de fin debe ser posterior a la hora de inicio")
        return self