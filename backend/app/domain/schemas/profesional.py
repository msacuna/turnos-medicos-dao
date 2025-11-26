

from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class ProfesionalBase(BaseModel):
    id: Optional[int] = None
    nombre: str
    apellido: str
    matricula: str
    especialidad_id: int
    email: str
    telefono: str
    id_especialidad: int


class ProfesionalRead(ProfesionalBase):
    model_config = ConfigDict(from_attributes=True,
                              json_schema_extra={
                                 "example": {
                                     "id": 1,
                                     "nombre": "Juan",
                                     "apellido": "Pérez",
                                     "matricula": "12345",
                                     "especialidad_id": 2,
                                     "email": "juan.perez@example.com",
                                     "telefono": "123-456-7890",
                                     "id_especialidad": 2
                                 }
                              })
    

class ProfesionalCreate(ProfesionalBase):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nombre": "Juan",
                "apellido": "Pérez",
                "matricula": "12345",
                "especialidad_id": 2,
                "email": "juan.perez@example.com",
                "telefono": "123-456-7890",
                "id_especialidad": 2
            }
        }
    )


class ProfesionalUpdate(ProfesionalBase):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nombre": "Juan",
                "apellido": "Pérez",
                "matricula": "12345",
                "especialidad_id": 2,
                "email": "juan.perez@example.com",
                "telefono": "123-456-7890",
                "id_especialidad": 2
            }
        }
    )