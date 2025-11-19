from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from pydantic import model_validator
from datetime import time
import enum
from .links import HorarioProfesionalLink

if TYPE_CHECKING:
    from .profesional import Profesional

class DiaSemana(enum.Enum): # nativo de python
    LUNES = 'Lunes'
    MARTES = 'Martes'
    MIERCOLES = 'Miercoles'
    JUEVES = 'Jueves'
    VIERNES = 'Viernes'
    SABADO = 'Sabado'

class HorarioAtencion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    dia_semana: DiaSemana = Field(index=True) # para busquedas rapidas
    hora_inicio: time
    hora_fin: time

    profesionales: list["Profesional"] = Relationship(back_populates="horario_atenciones", link_model=HorarioProfesionalLink)

    @model_validator(mode="after")
    def validar_rango_horario(self):
        # 'self' ya tiene los datos cargados
        if self.hora_inicio >= self.hora_fin:
            raise ValueError("La hora de fin debe ser posterior a la hora de inicio")
        return self