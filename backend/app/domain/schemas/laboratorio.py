from pydantic import BaseModel, ConfigDict

class LaboratorioBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nombre: str

class LaboratorioCreate(LaboratorioBase):
    pass

class LaboratorioUpdate(LaboratorioBase):
    pass

class LaboratorioRead(LaboratorioBase):
    id: int