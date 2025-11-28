from app.domain.models import Antecedente
from app.domain.schemas import AntecedenteCreate, AntecedenteUpdate, AntecedenteRead
from app.repositories import AntecedenteRepository

class AntecedenteService:
    def __init__(self, repo: AntecedenteRepository):
        self.repo = repo

    def obtener_todos(self) -> list[AntecedenteRead]:
        antecedentes = self.repo.get_all()
        return [AntecedenteRead.model_validate(a) for a in antecedentes]
    
    def obtener_por_id(self, id: int) -> AntecedenteRead | None:
        antecedente = self.repo.get_by_id(id)
        if not antecedente:
            raise ValueError(f"No se encontró el antecedente con ID {id}.")
        return AntecedenteRead.model_validate(antecedente)

    def obtener_modelo_por_id(self, id: int) -> Antecedente | None:
        antecedente = self.repo.get_by_id(id)
        if not antecedente:
            raise ValueError(f"No se encontró el antecedente con ID {id}.")
        return antecedente
    
    def crear_antecedente(self, antecedente_in: AntecedenteCreate) -> AntecedenteRead:
        antecedente = Antecedente.model_validate(antecedente_in)
        return AntecedenteRead.model_validate(self.repo.add(antecedente))
    
    def actualizar(self, id: int, data: AntecedenteUpdate) -> Antecedente | None:
        antecedente_actual = self.repo.get_by_id(id)
        if not antecedente_actual:
            return None
        
        datos_limpios = data.model_dump(exclude_unset=True)
        return self.repo.update(antecedente_actual, datos_limpios)