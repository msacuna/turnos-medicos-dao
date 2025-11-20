from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from .turno import Turno
    
class EstadoTurnoEnum(str, Enum):
    AGENDADO = "Agendado"
    CANCELADO = "Cancelado"
    EN_PROCESO = "En proceso"
    AUSENTE = "Ausente"
    FINALIZADO = "Finalizado"
    CONFIRMADO = "Confirmado"

class EstadoTurno(SQLModel, table=True):
    __tablename__ = 'estado_turno' # type: ignore
    nombre: str = Field(primary_key=True)

    turnos: list["Turno"] = Relationship(back_populates="estado")