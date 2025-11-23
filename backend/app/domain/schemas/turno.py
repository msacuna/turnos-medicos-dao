
from .especialidad import EspecialidadRead
from .consulta import ConsultaRead
from datetime import date, time
from typing import Literal, Optional
from pydantic import BaseModel, ConfigDict

EstadosTurno = Literal["AGENDADO", "CANCELADO", "FINALIZADO", "AUSENTE", "DISPONIBLE", "EN_PROCESO"]

class TurnoBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None
    fecha: date
    hora_inicio: time
    hora_fin_estimada: time
    dni_paciente: int
    nombre_estado: EstadosTurno
    id_especialidad: int
    id_agenda_profesional: int

class TurnoCreate(TurnoBase):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "fecha": "2024-07-15",
                "hora_inicio": "14:30:00",
                "hora_fin_estimada": "15:00:00",
                "dni_paciente": 12345678,
                "nombre_estado": "AGENDADO",
                "id_especialidad": 1,
                "id_agenda_profesional": 2
            }
        }
    )

    hora_fin_estimada: Optional[time] = None
    dni_paciente: Optional[int] = None
    nombre_estado: Optional[EstadosTurno] = None

class TurnoUpdate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "fecha": "2024-07-16",
                "hora_inicio": "15:00:00",
                "hora_fin_estimada": "15:30:00",
                "dni_paciente": 87654321,
                "nombre_estado": "CANCELADO",
                "id_especialidad": 2,
                "id_agenda_profesional": 3
            }
        }
    )
    id: int
    fecha: Optional[date] = None
    hora_inicio: Optional[time] = None
    hora_fin_estimada: Optional[time] = None
    dni_paciente: Optional[int] = None
    nombre_estado: Optional[EstadosTurno] = None
    id_especialidad: Optional[int] = None
    id_agenda_profesional: Optional[int] = None

class TurnoRead(TurnoBase):
    id: int
    nombre_estado: EstadosTurno
    especialidad: Optional[EspecialidadRead] = None
    consultas: list[Optional[ConsultaRead]] = []

