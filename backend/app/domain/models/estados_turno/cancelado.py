from estado_turno_abs import EstadoTurnoAbs
from sqlmodel import SQLModel, Field
from typing import Optional

class Cancelado(EstadoTurnoAbs, SQLModel, table=True):
    __tablename__ = "cancelado"
    id: Optional[int] = Field(primary_key=True, default=None)
    nombre: str = Field(default="Cancelado")

    def es_cancelado(self) -> bool:
        return True