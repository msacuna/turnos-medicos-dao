from app.domain.models import ObraSocial, TipoObraSocialEnum
from app.domain.schemas import ObraSocialCreate, ObraSocialUpdate, ObraSocialRead
from app.repositories import ObraSocialRepository

class ObraSocialService:
    def __init__(self, repo: ObraSocialRepository):
        self.repo = repo

    def obtener_todas(self) -> list[ObraSocialRead]:
        obras_sociales = self.repo.get_all()
        return [ObraSocialRead.model_validate(o) for o in obras_sociales]
    
    def obtener_por_nombre(self, nombre: str) -> ObraSocialRead | None:
        obra_social = self.repo.get_by_nombre(nombre)
        if not obra_social:
            raise ValueError(f"No se encontró la obra social con nombre {nombre}.")
        return ObraSocialRead.model_validate(obra_social)
    
    def obtener_modelo_por_nombre(self, nombre: str) -> ObraSocial | None:
        obra_social = self.repo.get_by_nombre(nombre)
        if not obra_social:
            raise ValueError(f"No se encontró la obra social con nombre {nombre}.")
        return obra_social

    def crear_obra_social(self, obra_social_in: ObraSocialCreate) -> ObraSocialRead:
        obra_social = ObraSocial.model_validate(obra_social_in)
        if self.repo.get_by_nombre(obra_social.nombre):
            raise ValueError(f"La obra social con nombre '{obra_social.nombre}' ya existe.")
        if self.repo.get_by_cuit(obra_social.cuit):
            raise ValueError(f"La obra social con CUIT '{obra_social.cuit}' ya existe.")
        
        return ObraSocialRead.model_validate(self.repo.add(obra_social))

    def actualizar(self, id: int, data: ObraSocialUpdate) -> ObraSocial | None:
        obra_social_actual = self.repo.get_by_id(id)
        if not obra_social_actual:
            raise ValueError(f"No se encontró la obra social con ID {id}.")
        
        if data.nombre and data.nombre != obra_social_actual.nombre:
            if self.repo.get_by_nombre(data.nombre):
                raise ValueError(f"La obra social con nombre '{data.nombre}' ya existe.")
        
        if data.cuit and data.cuit != obra_social_actual.cuit:
            if self.repo.get_by_cuit(data.cuit):
                raise ValueError(f"La obra social con CUIT '{data.cuit}' ya existe.")
        
        datos_limpios = data.model_dump(exclude_unset=True)
        for key, value in datos_limpios.items():
            if not hasattr(obra_social_actual, key):
                raise ValueError(f"El atributo {key} no existe en ObraSocial.")
            setattr(obra_social_actual, key, value)
        
        return self.repo.update(obra_social_actual)