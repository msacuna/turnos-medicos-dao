from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .paciente import Paciente


class GrupoSanguineo(SQLModel, table=True):
    __tablename__ = "grupo_sanguineo" # type: ignore
    nombre: str = Field(max_length=5, primary_key=True)  # 'A+', '0-'

    pacientes: list["Paciente"] = Relationship(back_populates="grupo_sanguineo")