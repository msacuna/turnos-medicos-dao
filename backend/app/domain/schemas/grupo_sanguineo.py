from pydantic import BaseModel, ConfigDict

class GrupoSanguineoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, json_schema_extra={
        "example": {
            "id": 1,
            "nombre": "A+"
        }
    })
    nombre: str