from app.domain.models import DetalleReceta
from app.domain.schemas.detalle_receta import DetalleRecetaCreate, DetalleRecetaRead, DetalleRecetaUpdate
from app.repositories.detalle_receta_repo import DetalleRecetaRepository
from .medicamento_service import MedicamentoService



class DetalleRecetaService:
    def __init__(self, detalle_receta_repository: DetalleRecetaRepository, medicamento_service: MedicamentoService):
        self.detalle_receta_repository = detalle_receta_repository
        self.medicamento_service = medicamento_service

    def crear_detalle_receta(self, detalle_receta: DetalleRecetaCreate) -> DetalleReceta:
        # Verificar que el medicamento existe
        medicamento_read = self.medicamento_service.obtener_por_id(detalle_receta.id_medicamento)
        if not medicamento_read:
            raise ValueError(f"No se encontró el medicamento con ID {detalle_receta.id_medicamento}.")

        # Construir las indicaciones a partir de los campos del schema
        indicaciones_parts = []
        if detalle_receta.dosis:
            indicaciones_parts.append(f"Dosis: {detalle_receta.dosis}")
        if detalle_receta.frecuencia:
            indicaciones_parts.append(f"Frecuencia: {detalle_receta.frecuencia}")
        if detalle_receta.duracion_dias:
            indicaciones_parts.append(f"Duración: {detalle_receta.duracion_dias} días")
        if detalle_receta.indicaciones:
            indicaciones_parts.append(f"Instrucciones: {detalle_receta.indicaciones}")
        
        indicaciones_completas = " | ".join(indicaciones_parts) if indicaciones_parts else None

        # Crear el modelo de DetalleReceta
        detalle_modelo = DetalleReceta(
            id_receta=detalle_receta.id_receta,
            id_medicamento=detalle_receta.id_medicamento,  # Usar el ID directamente del schema
            cantidad=detalle_receta.cantidad,
            indicaciones=indicaciones_completas
        )
        
        # Crear el detalle de receta
        detalle_creado = self.detalle_receta_repository.add(detalle_modelo)
        return detalle_creado