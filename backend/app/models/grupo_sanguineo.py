from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .paciente import Paciente

class GrupoSanguineo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=5, unique=True)

    pacientes: list["Paciente"] = Relationship(back_populates="grupo_sanguineo")