from pydantic import BaseModel, ConfigDict

class EspecialidadBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nombre: str

class EspecialidadCreate(EspecialidadBase):
    pass

class EspecialidadUpdate(EspecialidadBase):
    pass

class EspecialidadRead(EspecialidadBase):
    id: int