from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .rol import Rol

class Usuario(SQLModel, table=True):
    __tablename__ = "usuario" # type: ignore
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, max_length=100)
    password: str = Field(max_length=100) # Aquí guardaremos el HASH, no texto plano
    id_rol: int = Field(foreign_key="rol.id")

    rol: Optional["Rol"] = Relationship(back_populates="usuarios")