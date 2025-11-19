from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .consulta import Consulta

class MotivoConsulta(SQLModel, table=True):
    nombre: str = Field(primary_key=True, max_length=100)

    consultas: list["Consulta"] = Relationship(back_populates="motivo_consulta")