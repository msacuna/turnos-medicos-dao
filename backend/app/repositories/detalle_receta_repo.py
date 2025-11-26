from sqlalchemy import select
from .base import BaseRepository
from app.domain.models.detalle_receta import DetalleReceta

class DetalleRecetaRepository(BaseRepository[DetalleReceta]):
    def get_by_receta_id(self, receta_id: int) -> list[DetalleReceta]:
        statement = select(DetalleReceta).where(DetalleReceta.receta_id == receta_id)
        return self.session.exec(statement).all()