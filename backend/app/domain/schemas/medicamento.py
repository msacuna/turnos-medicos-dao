from pydantic import BaseModel, ConfigDict
from typing import Optional
from .laboratorio import LaboratorioRead

class MedicamentoBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nombre: str
    descripcion: Optional[str] = None

class MedicamentoCreate(MedicamentoBase):
    ids_laboratorios: list[int] = []

class MedicamentoUpdate(MedicamentoBase):
    nombre: str
    descripcion: Optional[str] = None
    ids_laboratorios: Optional[list[int]] = None

class MedicamentoRead(MedicamentoBase):
    id: int
    laboratorios: list[LaboratorioRead] = []