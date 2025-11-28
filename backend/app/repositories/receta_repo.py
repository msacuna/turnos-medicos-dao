import select
from .base import BaseRepository
from app.domain.models.receta import Receta

class RecetaRepository(BaseRepository[Receta]):
    def get_receta_by_consulta_id(self, consulta_id: int) -> list[Receta] | None:
        statement = select(Receta).where(Receta.consulta_id == consulta_id)
        return self.session.exec(statement).all()