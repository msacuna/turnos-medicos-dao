from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from .links import MedicamentoLaboratorioLink

if TYPE_CHECKING:
    from .medicamento import Medicamento

class Laboratorio(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100)

    medicamentos: list["Medicamento"] = Relationship(
        back_populates="laboratorios", link_model=MedicamentoLaboratorioLink
    )