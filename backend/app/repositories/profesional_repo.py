from typing import Optional
from sqlmodel import select
from app.domain.models import Profesional
from .base import BaseRepository

class ProfesionalRepository(BaseRepository[Profesional]):
    
    def get_by_nombre(self, nombre: str) -> Optional[Profesional]:
        statement = select(Profesional).where(Profesional.nombre == nombre)
        return self.session.exec(statement).first()
    
    def get_by_especialidad(self, especialidad: str) -> list[Profesional]:
        statement = select(Profesional).where(Profesional.especialidad == especialidad)
        return list(self.session.exec(statement).all())