from app.domain.models import Medicamento
from app.domain.schemas import MedicamentoCreate, MedicamentoUpdate, MedicamentoRead
from app.repositories import MedicamentoRepository
from .laboratorio_service import LaboratorioService

class MedicamentoService:
    def __init__(self, medicamento_repo: MedicamentoRepository, laboratorio_service: LaboratorioService):
        self.repo = medicamento_repo
        self.laboratorio_service = laboratorio_service

    def obtener_todos(self) -> list[MedicamentoRead]:
        medicamentos = self.repo.get_all()
        return [MedicamentoRead.model_validate(m) for m in medicamentos]
    
    def obtener_por_id(self, id: int) -> MedicamentoRead | None:
        medicamento = self.repo.get_by_id(id)
        if not medicamento:
            raise ValueError(f"No se encontró el medicamento con ID {id}.")
        return MedicamentoRead.model_validate(medicamento)

    def crear_medicamento(self, medicamento_in: MedicamentoCreate) -> MedicamentoRead:
        medicamento = Medicamento.model_validate(medicamento_in)

        if medicamento_in.ids_laboratorios:
            laboratorios = []
            for lab_id in medicamento_in.ids_laboratorios:
                laboratorio = self.laboratorio_service.obtener_modelo_por_id(lab_id)
                if not laboratorio:
                    raise ValueError(f"No se encontró el laboratorio con ID {lab_id}.")
                laboratorios.append(laboratorio)

            medicamento.laboratorios = laboratorios
        return MedicamentoRead.model_validate(self.repo.add(medicamento))

    def actualizar(self, id: int, data: MedicamentoUpdate) -> Medicamento | None:
        medicamento_actual = self.repo.get_by_id(id)
        if not medicamento_actual:
            raise ValueError(f"No se encontró el medicamento con ID {id}.")
        
        datos_simples = data.model_dump(exclude={"ids_laboratorios"}, exclude_unset=True) # Devuelve un dict
        for key, value in datos_simples.items():
            if not hasattr(medicamento_actual, key):
                raise ValueError(f"El atributo {key} no existe en Medicamento.")
            setattr(medicamento_actual, key, value)
        
        if data.ids_laboratorios is not None:
            nuevos_laboratorios = []
            for lab_id in data.ids_laboratorios:
                laboratorio = self.laboratorio_service.obtener_modelo_por_id(lab_id)
                if not laboratorio:
                    raise ValueError(f"No se encontró el laboratorio con ID {lab_id}.")
                nuevos_laboratorios.append(laboratorio)
            medicamento_actual.laboratorios = nuevos_laboratorios
        
        return self.repo.update(medicamento_actual)