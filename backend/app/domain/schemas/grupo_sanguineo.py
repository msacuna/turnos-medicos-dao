from pydantic import BaseModel, ConfigDict

class GrupoSanguineoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nombre: str