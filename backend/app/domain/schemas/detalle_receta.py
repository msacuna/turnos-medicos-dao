

from typing import Optional
from pydantic import BaseModel, ConfigDict

from app.domain.schemas.medicamento import MedicamentoRead


class DetalleRecetaBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    item: int
    id_receta: int
    id_medicamento: int
    cantidad: int
    indicaciones: Optional[str] = None

class DetalleRecetaCreate(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id_medicamento": 1,
                "dosis": "500mg",
                "frecuencia": "Cada 8 horas",
                "duracion_dias": 5,
                "cantidad": 30,
                "indicaciones": "Tomar una cápsula cada 8 horas después de las comidas."
            }
        }
    )
    id_medicamento: int
    dosis: str
    frecuencia: str
    duracion_dias: int
    cantidad: int = 1  # Valor por defecto
    indicaciones: Optional[str] = None
    id_receta: Optional[int] = None  # Se asignará internamente

class DetalleRecetaRead(DetalleRecetaBase):
    medicamento: Optional[MedicamentoRead] = None

class DetalleRecetaUpdate(BaseModel):
    id_medicamento: Optional[int] = None
    cantidad: Optional[int] = None
    indicaciones: Optional[str] = None