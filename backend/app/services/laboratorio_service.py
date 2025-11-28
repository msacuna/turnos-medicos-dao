from app.domain.models import Laboratorio
from app.domain.schemas import LaboratorioCreate, LaboratorioUpdate, LaboratorioRead
from app.repositories import LaboratorioRepository

class LaboratorioService:
    def __init__(self, repo: LaboratorioRepository):
        self.repo = repo

    def obtener_todos(self) -> list[LaboratorioRead]:
        laboratorios = self.repo.get_all()
        return [LaboratorioRead.model_validate(l) for l in laboratorios]
    
    def obtener_por_id(self, id: int) -> LaboratorioRead | None:
        laboratorio = self.repo.get_by_id(id)
        if not laboratorio:
            raise ValueError(f"No se encontró el laboratorio con ID {id}.")
        return LaboratorioRead.model_validate(laboratorio)
    
    def obtener_modelo_por_id(self, id: int) -> Laboratorio | None:
        laboratorio = self.repo.get_by_id(id)
        if not laboratorio:
            raise ValueError(f"No se encontró el laboratorio con ID {id}.")
        return laboratorio
    
    def crear_laboratorio(self, laboratorio_in: LaboratorioCreate) -> LaboratorioRead:
        laboratorio = Laboratorio.model_validate(laboratorio_in)
        return LaboratorioRead.model_validate(self.repo.add(laboratorio))
    
    def actualizar(self, id: int, data: LaboratorioUpdate) -> Laboratorio | None:
        laboratorio_actual = self.repo.get_by_id(id)
        if not laboratorio_actual:
            return None
        
        datos_limpios = data.model_dump(exclude_unset=True)
        return self.repo.update(laboratorio_actual, datos_limpios)