from app.domain.models import GrupoSanguineo
from app.repositories import GrupoSanguineoRepository

class GrupoSanguineoService:
    def __init__(self, repository: GrupoSanguineoRepository):
        self.repository = repository
    
    def obtener_por_nombre(self, nombre: str) -> GrupoSanguineo | None:
        return self.repository.get_by_nombre(nombre)