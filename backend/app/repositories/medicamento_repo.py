from typing import Optional
from sqlmodel import select
from app.domain.models import Medicamento
from .base import BaseRepository

# Hereda de BaseRepository
class MedicamentoRepository(BaseRepository[Medicamento]):
    
    def get_by_nombre(self, nombre: str) -> Optional[Medicamento]:
        statement = select(Medicamento).where(Medicamento.nombre == nombre)
        return self.session.exec(statement).first()