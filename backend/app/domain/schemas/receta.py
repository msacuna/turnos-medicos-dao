

from datetime import date
from pydantic import BaseModel, ConfigDict

from backend.app.domain.schemas.consulta import ConsultaRead
from backend.app.domain.schemas.detalle_receta import DetalleRecetaRead


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
                "dispensada": False
            }
        }
    )
    fecha: date
    dispensada: bool = False

class RecetaRead(RecetaBase):
    detalles_receta: list[DetalleRecetaRead] = []
    consultas: list[ConsultaRead] = []
