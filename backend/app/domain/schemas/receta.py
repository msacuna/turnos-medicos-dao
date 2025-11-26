

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING, Optional
from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from app.domain.schemas.consulta import ConsultaRead

from app.domain.schemas.detalle_receta import DetalleRecetaRead
from .detalle_receta import DetalleRecetaCreate

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
    )
    fecha: date
    dispensada: bool = False
    detalles_receta: list[DetalleRecetaCreate] = []
    dispensada: bool = Field(exclude=True, default=False)

class RecetaRead(RecetaBase):
    detalles_receta: list[DetalleRecetaRead] = []
    consultas: list[ConsultaRead] = []

class RecetaUpdate(BaseModel):
    fecha: Optional[date] = None
    dispensada: Optional[bool] = None
