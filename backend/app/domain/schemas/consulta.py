

from typing import Literal, Optional
from pydantic import BaseModel, ConfigDict
from .receta import RecetaRead

TipoConsulta = Literal["Consulta General", "Control", "Urgencia", "Seguimiento"]

class ConsultaBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None
    observaciones: Optional[str] = None
    id_turno: int
    nombre_motivo_consulta: TipoConsulta
    id_receta: Optional[int] = None

class ConsultaCreate(ConsultaBase):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "observaciones": "Paciente presenta síntomas leves.",
                "id_turno": 1,
                "nombre_motivo_consulta": "Consulta General",
                "id_receta": 2
            }
        }
    )

class ConsultaUpdate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "observaciones": "Actualización: síntomas mejorando.",
                "id_turno": 1,
                "nombre_motivo_consulta": "Seguimiento",
                "id_receta": 3
            }
        }
    )
    id: int
    observaciones: Optional[str] = None
    id_turno: Optional[int] = None
    nombre_motivo_consulta: Optional[TipoConsulta] = None
    id_receta: Optional[int] = None

class ConsultaRead(ConsultaBase):
    receta: Optional[RecetaRead] = None
