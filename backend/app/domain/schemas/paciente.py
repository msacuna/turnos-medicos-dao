from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal
from datetime import date
from .alergia import AlergiaRead
from .antecedente import AntecedenteRead
from .obra_social import ObraSocialRead
from .grupo_sanguineo import GrupoSanguineoRead

GrupoSanguineoType = Literal["A+", "A-", "B+", "B-", "AB+", "AB-", "0+", "0-"]

class PacienteBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    dni: int
    nombre: str
    apellido: str
    fecha_nacimiento: date
    email: str
    telefono: str

class PacienteCreate(PacienteBase):
    # ✅ EJEMPLO PARA SWAGGER POST
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "dni": 12345678,
                "nombre": "Juan Carlos",
                "apellido": "Pérez García",
                "fecha_nacimiento": "1990-05-15",
                "email": "juan.perez@email.com",
                "telefono": "+54911234567",
                "nombre_grupo_sanguineo": "A+",
                "nombre_obra_social": "OSDE",
                "ids_alergias": [1, 2],
                "ids_antecedentes": [1]
            }
        }
    )
    
    ids_alergias: Optional[list[int]] = None
    ids_antecedentes: Optional[list[int]] = None
    nombre_obra_social: Optional[str] = None
    nombre_grupo_sanguineo: GrupoSanguineoType

class PacienteUpdate(BaseModel):
    # ✅ EJEMPLO PARA SWAGGER PUT
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nombre": "Juan Carlos Actualizado",
                "apellido": "Pérez García",
                "fecha_nacimiento": "1990-05-15",
                "email": "juan.actualizado@email.com",
                "telefono": "+54911234567",
                "nombre_grupo_sanguineo": "B+",
                "nombre_obra_social": "Swiss Medical",
                "ids_alergias": [1],
                "ids_antecedentes": []
            }
        }
    )
    
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    nombre_grupo_sanguineo: Optional[GrupoSanguineoType] = None
    nombre_obra_social: Optional[str] = None
    ids_alergias: Optional[list[int]] = None
    ids_antecedentes: Optional[list[int]] = None

class PacienteRead(PacienteBase):
    alergias: list[AlergiaRead] = []
    antecedentes: list[AntecedenteRead] = []
    obra_social: Optional[ObraSocialRead] = None
    grupo_sanguineo: Optional[GrupoSanguineoRead] = None