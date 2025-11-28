from pydantic import BaseModel, ConfigDict
from app.domain.models import DiaSemanaEnum
from datetime import time

class HorarioProfesionalBase(BaseModel):
    model_config = ConfigDict(
    from_attributes=True, # Para que sea compatible con ORM si usas model_validate
    json_schema_extra={
        "example": {
            "profesional_id": 1,
            "horario_id": 25,
            "dia_semana": "Lunes",
            "hora_inicio": "09:00",
            "hora_fin": "17:00"
        }
    })

    dia_semana: DiaSemanaEnum
    hora_inicio: time
    hora_fin: time
    profesional_id: int

class HorarioProfesionalCreate(HorarioProfesionalBase):
    pass

class HorarioProfesionalUpdate(HorarioProfesionalBase):
    pass

class HorarioProfesionalRead(HorarioProfesionalBase):
    horario_id: int