from app.domain.models import Alergia
from app.domain.schemas import AlergiaCreate, AlergiaUpdate, AlergiaRead
from app.repositories import AlergiaRepository

class AlergiaService:
    def __init__(self, repo: AlergiaRepository):
        self.repo = repo

    def obtener_todas(self) -> list[AlergiaRead]:
        alergias = self.repo.get_all()
        return [AlergiaRead.model_validate(a) for a in alergias]
    
    def obtener_por_id(self, id: int) -> AlergiaRead | None:
        alergia = self.repo.get_by_id(id)
        if not alergia:
            raise ValueError(f"No se encontró la alergia con ID {id}.")
        return AlergiaRead.model_validate(alergia)
    
    def obtener_modelo_por_id(self, id: int) -> Alergia | None:
        alergia = self.repo.get_by_id(id)
        if not alergia:
            raise ValueError(f"No se encontró la alergia con ID {id}.")
        return alergia

    def crear_alergia(self, alergia_in: AlergiaCreate) -> AlergiaRead:
        alergia = Alergia.model_validate(alergia_in)
        return AlergiaRead.model_validate(self.repo.add(alergia))
    
    def actualizar(self, id: int, data: AlergiaUpdate) -> Alergia | None:
        alergia_actual = self.repo.get_by_id(id)
        if not alergia_actual:
            return None
        
        datos_limpios = data.model_dump(exclude_unset=True)
        return self.repo.update(alergia_actual, datos_limpios)