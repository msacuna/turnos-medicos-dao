
from sqlmodel import SQLModel, Field


class EstadoTurno(SQLModel, table=True):
    __tablename__ = "estados_turno"
    nombre: str = Field(primary_key=True)

