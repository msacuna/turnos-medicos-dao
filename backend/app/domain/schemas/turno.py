
from .especialidad import EspecialidadRead
from .consulta import ConsultaRead
from datetime import date, time
from typing import Literal, Optional
from pydantic import BaseModel, ConfigDict, Field

EstadosTurno = Literal["Agendado", "Cancelado", "Finalizado", "Ausente", "Disponible", "En Proceso"]

class TurnoBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None
    fecha: date
    hora_inicio: time
    hora_fin_estimada: time
    dni_paciente: Optional[int] = None
    estado_nombre: EstadosTurno
    id_especialidad: int
    id_agenda_profesional: int
    monto: float

class TurnoCreate(TurnoBase):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "fecha": "2024-07-15",
                "hora_inicio": "14:30:00",
                "hora_fin_estimada": "15:00:00",
                "dni_paciente": 12345678,
                "id_especialidad": 1,
                "id_agenda_profesional": 2
            }
        }
    )

    hora_fin_estimada: Optional[time] = None
    dni_paciente: Optional[int] = None
    estado_nombre: EstadosTurno = Field(default="Disponible", exclude=True)
    monto: float = Field(default=0.0, exclude=True)

class TurnoUpdate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "fecha": "2024-07-16",
                "hora_inicio": "15:00:00",
                "hora_fin_estimada": "15:30:00",
                "dni_paciente": 87654321,
                "estado_nombre": "Cancelado",
                "id_especialidad": 2,
                "id_agenda_profesional": 3
            }
        }
    )
    fecha: Optional[date] = None
    hora_inicio: Optional[time] = None
    hora_fin_estimada: Optional[time] = None
    dni_paciente: Optional[int] = None
    estado_nombre: Optional[EstadosTurno] = None
    id_especialidad: Optional[int] = None
    id_agenda_profesional: Optional[int] = None
    monto: float = Field(default=0.0, exclude=True)

class TurnoRead(TurnoBase):
    id: int
    estado_nombre: EstadosTurno
    especialidad: Optional[EspecialidadRead] = None
    consultas: list[Optional[ConsultaRead]] = []
    dni_paciente: Optional[int] = None

