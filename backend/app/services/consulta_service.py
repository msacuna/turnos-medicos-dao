from app.domain.models import MotivoConsulta, Consulta, Receta, DetalleReceta
from app.repositories.consulta_repo import ConsultaRepository
from app.domain.schemas.consulta import ConsultaCreate, ConsultaRead, ConsultaUpdate
from app.services.receta_service import RecetaService
from app.services.detalle_receta_service import DetalleRecetaService

class ConsultaService:
    def __init__(self, consulta_repository: ConsultaRepository, receta_service: RecetaService, detalle_receta_service: DetalleRecetaService):
        self.consulta_repository = consulta_repository
        self.receta_service = receta_service
        self.detalle_receta_service = detalle_receta_service

    def crear_consulta(self, consulta: ConsultaCreate) -> ConsultaRead:
        # 1. Crear la receta primero si existe
        id_receta_creada = None
        if consulta.receta:
            receta_creada = self.receta_service.crear_receta(consulta.receta)
            id_receta_creada = receta_creada.id
        
        # 2. Crear la consulta con el ID de receta
        datos_consulta = consulta.model_dump(exclude={"receta"})
        datos_consulta["id_receta"] = id_receta_creada
        nueva_consulta = Consulta.model_validate(datos_consulta)
        consulta_creada = self.consulta_repository.create(nueva_consulta)
        return ConsultaRead.model_validate(consulta_creada)
        
      
        
        