from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import date
from .links import PacienteAlergiaLink, PacienteAntecedenteLink

if TYPE_CHECKING:
    from .grupo_sanguineo import GrupoSanguineo
    from .obra_social import ObraSocial
    from .alergia import Alergia
    from .antecedente import Antecedente
    from .turno import Turno

class Paciente(SQLModel, table=True):
    __tablename__ = "paciente" # type: ignore
    dni: int = Field(primary_key=True)
    nombre: str = Field(max_length=100)
    apellido: str = Field(max_length=100)
    fecha_nacimiento: date
    email: str = Field(max_length=255, unique=True)
    telefono: str = Field(max_length=20)
    nombre_grupo_sanguineo: str = Field(foreign_key="grupo_sanguineo.nombre", max_length=5)
    nombre_obra_social: Optional[str] = Field(default=None, foreign_key="obra_social.nombre")

    grupo_sanguineo: "GrupoSanguineo" = Relationship(back_populates="pacientes")
    obra_social: Optional["ObraSocial"] = Relationship(back_populates="pacientes")
    alergias: list["Alergia"] = Relationship(back_populates="pacientes", link_model=PacienteAlergiaLink)
    antecedentes: list["Antecedente"] = Relationship(back_populates="pacientes", link_model=PacienteAntecedenteLink)
    turnos: list["Turno"] = Relationship(back_populates="paciente")