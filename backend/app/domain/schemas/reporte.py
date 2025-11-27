from pydantic import BaseModel

class ReporteTurnoPorEspecialidad(BaseModel):
    especialidad: str
    cantidad_turnos: int