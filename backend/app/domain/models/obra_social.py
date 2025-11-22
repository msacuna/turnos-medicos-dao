from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from .links import ObraSocialProfesionalLink
from .tipo_obra_social import TipoObraSocialEnum

if TYPE_CHECKING:
    from .tipo_obra_social import TipoObraSocial
    from .paciente import Paciente
    from .profesional import Profesional

class ObraSocial(SQLModel, table=True):
    __tablename__ = "obra_social" # type: ignore
    nombre: str = Field(max_length=100, primary_key=True)
    cuit: str = Field(max_length=11, unique=True)
    porcentaje_cobertura: float = Field(ge=0, le=100)
    nombre_tipo: TipoObraSocialEnum = Field(foreign_key="tipo_obra_social.nombre")

    tipo: Optional["TipoObraSocial"] = Relationship(back_populates="obras_sociales")
    pacientes: list["Paciente"] = Relationship(back_populates="obra_social")
    profesionales: list["Profesional"] = Relationship(back_populates="obras_sociales", link_model=ObraSocialProfesionalLink)