from typing import Optional
from sqlmodel import select
from app.domain.models import Antecedente
from .base import BaseRepository

# Hereda de BaseRepository
class AntecedenteRepository(BaseRepository[Antecedente]):
    
    def get_by_nombre(self, nombre: str) -> Optional[Antecedente]:
        statement = select(Antecedente).where(Antecedente.nombre == nombre)
        return self.session.exec(statement).first()