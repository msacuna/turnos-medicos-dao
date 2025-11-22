from pydantic import BaseModel, ConfigDict

class MotivoConsultaBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nombre: str

class MotivoConsultaCreate(MotivoConsultaBase):
    pass

class MotivoConsultaUpdate(MotivoConsultaBase):
    pass

class MotivoConsultaRead(MotivoConsultaBase):
    pass