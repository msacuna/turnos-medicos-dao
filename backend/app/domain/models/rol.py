from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .usuario import Usuario

class Rol(SQLModel, table=True):
    __tablename__ = "rol" # type: ignore
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(unique=True, max_length=100)

    usuarios: List["Usuario"] = Relationship(back_populates="rol")