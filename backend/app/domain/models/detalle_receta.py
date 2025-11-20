from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from pydantic import model_validator

if TYPE_CHECKING:
    from .receta import Receta
    from .medicamento import Medicamento

class DetalleReceta(SQLModel, table=True):
    __tablename__ = "detalle_receta" # type: ignore
    item: Optional[int] = Field(default=None, primary_key=True)
    id_receta: int = Field(foreign_key="receta.id", primary_key=True)
    id_medicamento: int = Field(foreign_key="medicamento.id")
    cantidad: int
    indicaciones: Optional[str] = Field(default=None, max_length=255)

    receta: "Receta" = Relationship(back_populates="detalles_receta")
    medicamento: "Medicamento" = Relationship(back_populates="detalles_receta")

    @model_validator(mode="after")
    def check_cantidad_positiva(self):
        if self.cantidad <= 0:
            raise ValueError("La cantidad debe ser un número positivo.")
        return self