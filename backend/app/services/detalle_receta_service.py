from app.domain.models import DetalleReceta
from backend.app.domain.schemas.detalle_receta import DetalleRecetaCreate, DetalleRecetaRead, DetalleRecetaUpdate
from backend.app.repositories.detalle_receta_repo import DetalleRecetaRepository
from .medicamento_service import MedicamentoService



class DetalleRecetaService:
    def __init__(self, detalle_receta_repository: DetalleRecetaRepository, medicamento_service: MedicamentoService):
        self.detalle_receta_repository = detalle_receta_repository
        self.medicamento_service = medicamento_service

    def crear_detalle_receta(self, detalle_receta: DetalleRecetaCreate) -> DetalleReceta:
        # Verificar si el medicamento existe
        if not self.medicamento_service.existe_medicamento(detalle_receta.nombre_medicamento):
            raise ValueError(f"No se encontró el medicamento con nombre {detalle_receta.nombre_medicamento}.")

        # Crear el detalle de receta
        detalle_creado = self.detalle_receta_repository.create(detalle_receta)
        return detalle_creado