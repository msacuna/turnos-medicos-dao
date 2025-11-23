from app.domain.models import EstadoTurno
from app.repositories import EstadoTurnoRepository

class EstadoTurnoService:
    def __init__(self, repository: EstadoTurnoRepository):
        self.repository = repository
    
    def obtener_estado_por_nombre(self, nombre: str) -> EstadoTurno | None:
        estado = self.repository.get_by_nombre(nombre)
        if not estado:
            raise ValueError(f"No se encontró el estado de turno con nombre {nombre}.")
        return estado