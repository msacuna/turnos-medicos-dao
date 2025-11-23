from sqlalchemy import func
from app.domain.models import Turno
from app.repositories.turno_repo import TurnoRepository
from app.domain.schemas.turno import TurnoCreate, TurnoUpdate, TurnoRead
from app.services import EstadoTurnoService
from app.services.paciente_service import PacienteService

class TurnoService:
    def __init__(self, 
                repository: TurnoRepository,
                estado_turno_service: EstadoTurnoService,
                paciente_service: PacienteService):
        
        self.repository = repository
        self.estado_turno_service = estado_turno_service
        self.paciente_service = paciente_service
    
    
    def obtener_todos(self) -> list[TurnoRead]:
        turnos = self.repository.get_all()
        return [TurnoRead.model_validate(t) for t in turnos]
    
    def obtener_por_id(self, id: int) -> TurnoRead | None:
        turno = self.repository.get_by_id(id)
        if not turno:
            raise ValueError(f"No se encontró el turno con ID {id}.")
        return TurnoRead.model_validate(turno)

    def obtener_turno(self, id: int) -> Turno | None:
        turno = self.repository.get_by_id(id)
        if not turno:
            raise ValueError(f"No se encontró el turno con ID {id}.")
        return turno

    def crear_turno(self, turno_in: TurnoCreate) -> TurnoRead:
        datos_turno = turno_in.model_dump()
        turno = Turno.model_validate(datos_turno)

        # Validar estado del turno
        estado = self.estado_turno_service.obtener_modelo_por_nombre(turno_in.nombre_estado)
        if not estado:
            raise ValueError(f"No se encontró el estado de turno con nombre {turno_in.nombre_estado}.")
        turno.estado = estado

        turno_creado = self.repository.create(turno)
        return TurnoRead.model_validate(turno_creado)
    
    def obtener_turnos_por_paciente(self, dni_paciente: int) -> list[TurnoRead]:
        turnos = self.repository.get_by_paciente(dni_paciente)
        return [TurnoRead.model_validate(t) for t in turnos]
    
    def obtener_turnos_por_estado(self, nombre_estado: str) -> list[TurnoRead]:
        turnos = self.repository.get_by_estado(nombre_estado)
        return [TurnoRead.model_validate(t) for t in turnos]
    
    def liberar_turno(self, id: int) -> TurnoRead:
        
        turno = self.obtener_turno(id)

        estado_liberado = self.estado_turno_service.obtener_modelo_por_nombre("liberado")
        if not estado_liberado:
            raise ValueError("No se encontró el estado 'liberado'.")

        turno.nombre_estado = estado_liberado.nombre
        turno.estado = estado_liberado
        turno.dni_paciente = None

        turno_actualizado = self.repository.update(turno)
        return TurnoRead.model_validate(turno_actualizado)
    
    def agendar_turno(self, id: int, dni_paciente: int) -> TurnoRead:
        turno = self.obtener_turno(id)

        estado_agendado = self.estado_turno_service.obtener_estado_por_nombre("agendado")
        
        if not self.paciente_service.existe_paciente(dni_paciente):
            raise ValueError(f"No se encontró el paciente con DNI {dni_paciente}.")

        turno.nombre_estado = estado_agendado.nombre
        turno.estado = estado_agendado
        turno.dni_paciente = dni_paciente

        turno_actualizado = self.repository.update(turno)
        return TurnoRead.model_validate(turno_actualizado)
    
    def iniciar_turno(self, id: int) -> TurnoRead:
        turno = self.obtener_turno(id)
        estado_en_progreso = self.estado_turno_service.obtener_estado_por_nombre("en_progreso")

        turno.nombre_estado = estado_en_progreso.nombre
        turno.estado = estado_en_progreso
        turno.hora_inicio = func.now()

        turno_actualizado = self.repository.update(turno)
        return TurnoRead.model_validate(turno_actualizado)
    
    def finalizar_turno(self, id: int) -> TurnoRead:
        turno = self.obtener_turno(id)
        estado_finalizado = self.estado_turno_service.obtener_estado_por_nombre("finalizado")

        turno.nombre_estado = estado_finalizado.nombre
        turno.estado = estado_finalizado
        turno.hora_fin_estimada = func.now()

        turno_actualizado = self.repository.update(turno)
        return TurnoRead.model_validate(turno_actualizado)