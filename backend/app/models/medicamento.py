from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from .links import MedicamentoLaboratorioLink

if TYPE_CHECKING:
    from .laboratorio import Laboratorio
    from .detalle_receta import DetalleReceta

class Medicamento(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100)
    descripcion: Optional[str] = Field(default=None, max_length=255)

    laboratorios: list["Laboratorio"] = Relationship(back_populates="medicamentos", link_model=MedicamentoLaboratorioLink)
    detalles_receta: list["DetalleReceta"] = Relationship(back_populates="medicamento")