from pydantic import BaseModel, ConfigDict

class EspecialidadBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nombre: str
    precio: float

class EspecialidadCreate(EspecialidadBase):
    model_config = ConfigDict(from_attributes=True, 
        json_schema_extra={
            "example": {
                "nombre": "Cardiología",
                "precio": 1500.0
            }
        }
    )
    pass

class EspecialidadUpdate(EspecialidadBase):
    pass

class EspecialidadRead(EspecialidadBase):
    model_config = ConfigDict(from_attributes=True, json_schema_extra={
        "example": {
            "id": 1,
            "nombre": "Cardiología",
            "precio": 1500.0
        }
    })
    id: int