from typing import Optional
from sqlmodel import select
from app.domain.models import GrupoSanguineo
from .base import BaseRepository

# Hereda de BaseRepository
class GrupoSanguineoRepository(BaseRepository[GrupoSanguineo]):
    
    def get_by_nombre(self, nombre: str) -> Optional[GrupoSanguineo]:
        statement = select(GrupoSanguineo).where(GrupoSanguineo.nombre == nombre)
        return self.session.exec(statement).first()