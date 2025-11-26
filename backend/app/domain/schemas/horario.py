from pydantic import BaseModel, model_validator, ConfigDict
from datetime import time
from typing import Optional

class HorarioDiaInput(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "hora_inicio": "08:00",
                "hora_fin": "12:00",
                "trabaja": True
            }
        }
    )
    hora_inicio: Optional[time] = None
    hora_fin: Optional[time] = None
    trabaja: bool = True

    @model_validator(mode='after')
    def validar_consistencia(self):
        if self.trabaja:
            if not self.hora_inicio or not self.hora_fin:
                raise ValueError("Si trabaja=true, debe indicar hora de inicio y fin")
            if self.hora_inicio >= self.hora_fin:
                raise ValueError("La hora de inicio debe ser anterior a la de fin")
        return self