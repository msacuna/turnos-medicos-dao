from typing import Optional
from sqlmodel import func, select
from app.domain.models import Turno
from .base import BaseRepository

class TurnoRepository(BaseRepository[Turno]):
    def get_by_paciente(self, dni_paciente: int) -> list[Turno]:
        statement = select(Turno).where(Turno.dni_paciente == dni_paciente)
        return list(self.session.exec(statement).all())
    
    def get_by_estado(self, nombre_estado: str) -> list[Turno]:
        statement = select(Turno).where(
            func.lower(Turno.nombre_estado) == func.lower(nombre_estado)
        )
        return list(self.session.exec(statement).all())
