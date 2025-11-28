from pydantic import BaseModel, ConfigDict

class AntecedenteBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nombre: str

class AntecedenteCreate(AntecedenteBase):
    pass

class AntecedenteUpdate(AntecedenteBase):
    pass

class AntecedenteRead(AntecedenteBase):
    id: int