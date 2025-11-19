from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from .links import PacienteAlergiaLink

if TYPE_CHECKING:
    from .paciente import Paciente

class Alergia(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100, unique=True)

    pacientes: list["Paciente"] = Relationship(
        back_populates="alergias", link_model=PacienteAlergiaLink
    )