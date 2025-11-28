from typing import Optional
from sqlmodel import select
from app.domain.models import Especialidad
from .base import BaseRepository

# Hereda de BaseRepository
class EspecialidadRepository(BaseRepository[Especialidad]):
    
    def get_by_nombre(self, nombre: str) -> Optional[Especialidad]:
        statement = select(Especialidad).where(Especialidad.nombre == nombre)
        return self.session.exec(statement).first()