

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING, Optional
from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from .consulta import ConsultaRead

from .detalle_receta import DetalleRecetaRead, DetalleRecetaCreate

class RecetaBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    fecha: date
    dispensada: bool

class RecetaCreate(BaseModel):
    # ✅ EJEMPLO PARA SWAGGER POST
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "fecha": "2024-07-10",
                "detalles_receta": [
                    {
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
    )
    fecha: date
    dispensada: bool = False
    detalles_receta: list[DetalleRecetaCreate] = []
    dispensada: bool = Field(exclude=True, default=False)

class RecetaRead(RecetaBase):
    detalles_receta: list[DetalleRecetaRead] = []


class RecetaUpdate(BaseModel):
    fecha: Optional[date] = None
    dispensada: Optional[bool] = None
