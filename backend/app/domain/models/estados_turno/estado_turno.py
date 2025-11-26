
from pydantic import Field
from sqlmodel import SQLModel


class EstadoTurno(SQLModel, table=True):
    __tablename__ = "estados_turno"
    nombre: str = Field(primary_key=True, default=None)

