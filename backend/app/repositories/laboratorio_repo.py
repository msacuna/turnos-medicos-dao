from typing import Optional
from sqlmodel import select
from app.domain.models import Laboratorio
from .base import BaseRepository

# Hereda de BaseRepository
class LaboratorioRepository(BaseRepository[Laboratorio]):
    
    def get_by_nombre(self, nombre: str) -> Optional[Laboratorio]:
        statement = select(Laboratorio).where(Laboratorio.nombre == nombre)
        return self.session.exec(statement).first()