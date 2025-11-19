from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .turno import Turno

class EstadoTurno(SQLModel, table=True):
    nombre: str = Field(primary_key=True)

    turnos: list["Turno"] = Relationship(back_populates="estado")