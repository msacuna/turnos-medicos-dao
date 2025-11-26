from ..base import BaseRepository
from ...domain.models import Finalizado
from sqlmodel import select
from typing import Optional

class FinalizadoRepository(BaseRepository[Finalizado]):
    def get_by_nombre(self, nombre: str) -> Optional[Finalizado]:
        statement = select(Finalizado).where(Finalizado.nombre == nombre)
        return self.session.exec(statement).first()