from sqlmodel import Relationship, SQLModel, Field
from typing import TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from .obra_social import ObraSocial

class TipoObraSocialEnum(Enum):
    Nacional = "Nacional"
    Provincial = "Provincial"
    Jubilado = "Jubilado"

class TipoObraSocial(SQLModel, table=True):
    __tablename__ = "tipo_obra_social" # type: ignore
    nombre: str = Field(max_length=100, primary_key=True)

    obras_sociales: list["ObraSocial"] = Relationship(back_populates="tipo")