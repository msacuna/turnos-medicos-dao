from estado_turno_abs import EstadoTurnoAbs
from sqlmodel import Field, SQLModel
from typing import Optional


class Ausente(EstadoTurnoAbs, SQLModel, table=True):
    __tablename__ = "ausente"
    id: Optional[int] = Field(primary_key=True, default=None)
    nombre: str = Field(default="Ausente")

    def es_ausente(self) -> bool:
        return True
