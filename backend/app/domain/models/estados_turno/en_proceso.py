from estado_turno_abs import EstadoTurnoAbs
from sqlmodel import SQLModel, Field
from typing import Optional

class EnProceso(EstadoTurnoAbs, SQLModel, table=True):
    __tablename__ = "en_proceso"
    id: Optional[int] = Field(primary_key=True, default=None)
    nombre: str = Field(default="En Proceso")

    def es_en_proceso(self) -> bool:
        return True