from pydantic import BaseModel, ConfigDict
from app.domain.models import TipoObraSocialEnum

class ObraSocialBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nombre: str
    cuit: str
    porcentaje_cobertura: float
    nombre_tipo: TipoObraSocialEnum

class ObraSocialCreate(ObraSocialBase):
    pass

class ObraSocialUpdate(ObraSocialBase):
    pass

class ObraSocialRead(ObraSocialBase):
    id: int