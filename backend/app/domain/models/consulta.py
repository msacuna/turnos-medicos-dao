from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .turno import Turno
    from .motivo_consulta import MotivoConsulta
    from .receta import Receta

class Consulta(SQLModel, table=True):
    __tablename__ = 'consulta' # type: ignore
    id: Optional[int] = Field(default=None, primary_key=True)
    observaciones: Optional[str] = Field(default=None, max_length=255)
    id_turno: int = Field(foreign_key="turno.id")
    nombre_motivo_consulta: str = Field(foreign_key="motivo_consulta.nombre")
    id_receta: Optional[int] = Field(default=None, foreign_key="receta.id")

    turno: "Turno" = Relationship(back_populates="consultas")
    motivo_consulta: "MotivoConsulta" = Relationship(back_populates="consultas")
    receta: Optional["Receta"] = Relationship(back_populates="consultas")