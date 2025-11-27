from typing import Optional
from sqlmodel import func, select
from sqlalchemy.orm import selectinload
from app.domain.models import Turno
from .base import BaseRepository

class TurnoRepository(BaseRepository[Turno]):
    def get_by_id_with_especialidad(self, id: int) -> Optional[Turno]:
        """Obtiene un turno por ID con la especialidad cargada para cálculo de monto"""
        statement = select(Turno).where(Turno.id == id).options(
            selectinload(Turno.especialidad)
        )
        result = self.session.exec(statement).first()
        return result
    
    def get_by_paciente(self, dni_paciente: int) -> list[Turno]:
        statement = select(Turno).where(Turno.dni_paciente == dni_paciente)
        return list(self.session.exec(statement).all())
    
    def get_by_estado(self, nombre_estado: str) -> list[Turno]:
        statement = select(Turno).where(
            func.lower(Turno.nombre_estado) == func.lower(nombre_estado)
        )
        return list(self.session.exec(statement).all())

    def get_by_agenda(self, id_agenda: int) -> list[Turno]:
        statement = select(Turno).where(Turno.id_agenda_profesional == id_agenda)
        return list(self.session.exec(statement).all())
    
    def get_by_agenda_and_days(self, id_agenda: int, dias: list[int]) -> list[Turno]:
        """Obtiene turnos de una agenda específica para los días dados del mes"""
        statement = select(Turno).where(
            Turno.id_agenda_profesional == id_agenda,
            func.extract('day', Turno.fecha).in_(dias)
        ).options(
            # Eager loading para obtener datos del paciente
            select(Turno).options(selectinload(Turno.paciente))
        )
        return list(self.session.exec(statement).all())