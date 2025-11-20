from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from pydantic import model_validator

if TYPE_CHECKING:
    from .profesional import Profesional
    from .turno import Turno

class AgendaProfesional(SQLModel, table=True):
    __tablename__ = "agenda_profesional" # type: ignore
    id: Optional[int] = Field(default=None, primary_key=True)
    id_profesional: int = Field(foreign_key="profesional.id")
    anio: int
    mes: int

    profesional: "Profesional" = Relationship(back_populates="agendas_profesionales")
    turnos: list["Turno"] = Relationship(back_populates="agenda_profesional")

    @model_validator(mode="after")
    def validar_mes_anio(self):
        if not (1 <= self.mes <= 12):
            raise ValueError("El mes debe estar entre 1 y 12")
        if self.anio < 1900:
            raise ValueError("El año debe ser mayor o igual a 1900")
        return self