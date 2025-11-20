from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from .links import HorarioProfesionalLink, ObraSocialProfesionalLink

if TYPE_CHECKING:
    from .especialidad import Especialidad
    from .agenda_profesional import AgendaProfesional
    from .horario_atencion import HorarioAtencion
    from .obra_social import ObraSocial

class Profesional(SQLModel, table=True):
    __tablename__ = "profesional" # type: ignore
    id: Optional[int] = Field(default=None, primary_key=True)
    matricula: str = Field(unique=True, max_length=50)
    nombre: str = Field(max_length=100)
    apellido: str = Field(max_length=100)
    email: str = Field(unique=True, max_length=255)
    telefono: str = Field(max_length=20)
    id_especialidad: int = Field(foreign_key="especialidad.id")

    especialidad: Optional["Especialidad"] = Relationship(back_populates="profesionales")
    agendas_profesionales: list["AgendaProfesional"] = Relationship(back_populates="profesional")
    horario_atenciones: list["HorarioAtencion"] = Relationship(back_populates="profesionales", link_model=HorarioProfesionalLink)
    obras_sociales: list["ObraSocial"] = Relationship(back_populates="profesionales", link_model=ObraSocialProfesionalLink)