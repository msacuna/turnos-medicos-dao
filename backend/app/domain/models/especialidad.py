from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .profesional import Profesional
    from .turno import Turno

class Especialidad(SQLModel, table=True):
    __tablename__ = 'especialidad' # type: ignore
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(unique=True, max_length=100)
    precio: float

    profesionales: list["Profesional"] = Relationship(back_populates="especialidad")
    turnos: list["Turno"] = Relationship(back_populates="especialidad")