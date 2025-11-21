from pydantic import BaseModel, ConfigDict

class AlergiaBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nombre: str

class AlergiaCreate(AlergiaBase):
    pass

class AlergiaUpdate(AlergiaBase):
    pass

class AlergiaRead(AlergiaBase):
    id: int