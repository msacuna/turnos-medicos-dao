from datetime import time
from typing import Optional
from sqlmodel import select
from app.domain.models import HorarioAtencion, DiaSemanaEnum
from .base import BaseRepository

class HorarioAtencionRepository(BaseRepository[HorarioAtencion]):
    
    def get_by_dia(self, dia: DiaSemanaEnum) -> Optional[HorarioAtencion]:
        statement = select(HorarioAtencion).where(HorarioAtencion.dia_semana == dia)
        return self.session.exec(statement).first()
    
    def get_by_profesional(self, profesional_id: int) -> list[HorarioAtencion]:
        statement = select(HorarioAtencion).where(HorarioAtencion.id_profesional == profesional_id)
        return list(self.session.exec(statement).all())
    
    def get_by_dia_y_profesional(self, profesional_id: int, dia: DiaSemanaEnum) -> HorarioAtencion | None:
        # Busca si el médico ya tiene horario ese día específico
        statement = select(HorarioAtencion).where(
            HorarioAtencion.id_profesional == profesional_id,
            HorarioAtencion.dia_semana == dia
        )
        return self.session.exec(statement).first()
    
    def delete_by_dia_y_profesional(self, profesional_id: int, dia: DiaSemanaEnum) -> bool:
        """Borra el horario de un día específico si existe (ej: dejar de trabajar los martes)"""
        horario = self.get_by_dia_y_profesional(profesional_id, dia)
        if horario:
            self.session.delete(horario)
            self.session.commit()
            return True
        return False