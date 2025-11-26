

from __future__ import annotations

from typing import Literal, Optional, TYPE_CHECKING
from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    from .receta import RecetaCreate, RecetaRead


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
                "id_receta": 2,
                "receta": {
                    "fecha": "2024-07-10",
                    "detalles_receta": [
                        {
                            "nombre_medicamento": "Paracetamol",
                            "dosis": "500mg",
                            "frecuencia": "Cada 8 horas",
                            "duracion_dias": 5
                        },
                        {
                            "nombre_medicamento": "Ibuprofeno",
                            "dosis": "200mg",
                            "frecuencia": "Cada 12 horas",
                            "duracion_dias": 3
                        }
                    ]
                }

            }
        }
    )
    receta: RecetaCreate


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
