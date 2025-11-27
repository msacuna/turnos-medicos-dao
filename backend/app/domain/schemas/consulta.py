

from __future__ import annotations

from typing import Literal, Optional, TYPE_CHECKING
from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    from .receta import RecetaRead

from .receta import RecetaCreate


TipoConsulta = Literal["Consulta General", "Control", "Urgencia", "Seguimiento"]

class ConsultaBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None
    observaciones: Optional[str] = None
    id_turno: Optional[int] = None
    nombre_motivo_consulta: TipoConsulta
    id_receta: Optional[int] = None

class ConsultaCreate(ConsultaBase):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "observaciones": "Paciente presenta síntomas leves.",
                "nombre_motivo_consulta": "Consulta General",
                "receta": {
                    "fecha": "2024-07-10",
                    "detalles_receta": [
                        {
                            "id_medicamento": 1,
                            "id_medicamento": 1,
                            "dosis": "500mg",
                            "frecuencia": "Cada 8 horas",
                            "duracion_dias": 5,
                            "cantidad": 30,
                            "indicaciones": "Tomar una cápsula cada 8 horas después de las comidas."
                        },
                        {
                            "id_medicamento": 1,
                            "dosis": "500mg",
                            "frecuencia": "Cada 8 horas",
                            "duracion_dias": 5,
                            "cantidad": 30,
                            "indicaciones": "Tomar una cápsula cada 8 horas después de las comidas."
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
    receta: Optional['RecetaRead'] = None
