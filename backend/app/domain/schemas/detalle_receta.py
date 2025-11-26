

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
                "id_receta": 1,
                "id_medicamento": 2,
                "cantidad": 30,
                "indicaciones": "Tomar una cápsula cada 8 horas después de las comidas."
            }
        }
    )
    id_receta: int
    id_medicamento: int
    cantidad: int
    indicaciones: Optional[str] = None

class DetalleRecetaRead(DetalleRecetaBase):
    medicamento: Optional[MedicamentoRead] = None

class DetalleRecetaUpdate(BaseModel):
    id_medicamento: Optional[int] = None
    cantidad: Optional[int] = None
    indicaciones: Optional[str] = None