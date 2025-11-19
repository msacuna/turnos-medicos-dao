from sqlmodel import Relationship, SQLModel, Field
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .obra_social import ObraSocial

class TipoObraSocial(SQLModel, table=True):
    __tablename__ = "tipo_obra_social" # type: ignore
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100)

    obras_sociales: list["ObraSocial"] = Relationship(back_populates="tipo")