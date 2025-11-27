

from app.domain.models.detalle_receta import DetalleReceta
from app.domain.schemas.receta import RecetaCreate, RecetaRead, RecetaUpdate
from app.repositories.receta_repo import RecetaRepository
from app.domain.models import Receta
from .detalle_receta_service import DetalleRecetaService

class RecetaService:
    def __init__(self, receta_repository: RecetaRepository, detalle_receta_service: DetalleRecetaService):
        self.receta_repository = receta_repository
        self.detalle_receta_service = detalle_receta_service


    def crear_receta(self, receta: RecetaCreate) -> Receta:

        # 1. Crear la receta sin los detalles primero
        receta_sin_detalles = Receta.model_validate({
            **receta.model_dump(exclude={"detalles_receta"})
        })
        receta_creada = self.receta_repository.add(receta_sin_detalles)

        # 2. Crear cada detalle de receta asociado a la receta creada
        for detalle_data in receta.detalles_receta:
            # Obtener los datos del detalle y actualizar el id_receta
            detalle_dict = detalle_data.model_dump()
            detalle_dict['id_receta'] = receta_creada.id
            
            # Crear el objeto DetalleRecetaCreate con el id_receta correcto
            detalle_create = type(detalle_data)(**detalle_dict)
            self.detalle_receta_service.crear_detalle_receta(detalle_create)

        return receta_creada