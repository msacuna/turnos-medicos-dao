from pydantic import BaseModel, ConfigDict
from .turno import TurnoRead

class AgendaProfesionalBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    id_profesional: int
    anio: int
    mes: int 


class AgendaProfesionalRead(AgendaProfesionalBase):
    model_config = ConfigDict(from_attributes=True, json_schema_extra={
        "example": {
            "id": 1,
            "id_profesional": 123,
            "anio": 2024,
            "mes": 7
        }
    })  