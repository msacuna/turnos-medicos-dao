from estado_turno_abs import EstadoTurnoAbs
from sqlmodel import SQLModel, Field
from typing import Optional

class Finalizado(EstadoTurnoAbs, SQLModel, table=True):
    __tablename__ = "finalizado"
    id: Optional[int] = Field(primary_key=True, default=None)
    nombre: str = Field(default="Finalizado")

    def es_finalizado(self) -> bool:
        return True