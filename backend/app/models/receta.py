from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import date

if TYPE_CHECKING:
    from .detalle_receta import DetalleReceta
    from .consulta import Consulta

class Receta(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    fecha: date
    dispensada: bool = Field(default=False)
    
    detalles_receta: list["DetalleReceta"] = Relationship(back_populates="receta")
    consultas: list["Consulta"] = Relationship(back_populates="receta")