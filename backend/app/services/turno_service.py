from sqlalchemy import func
from app.domain.models import Turno
from app.repositories.turno_repo import TurnoRepository
from app.domain.schemas.turno import TurnoCreate, TurnoUpdate, TurnoRead
from app.services.estado_turno_service import EstadoTurnoService
from app.services.paciente_service import PacienteService
from app.services.consulta_service import ConsultaService
from app.domain.schemas.consulta import ConsultaCreate


class TurnoService:
    def __init__(self, 
                repository: TurnoRepository,
                estado_turno_service: EstadoTurnoService,
                paciente_service: PacienteService,
                consulta_service: ConsultaService):
        
        self.repository = repository
        self.estado_turno_service = estado_turno_service
        self.paciente_service = paciente_service
        self.consulta_service = consulta_service
    

    def obtener_todos(self) -> list[TurnoRead]:
        turnos = self.repository.get_all()
        return [TurnoRead.model_validate(t) for t in turnos]
    
    def obtener_por_id(self, id: int) -> TurnoRead:
        turno = self.repository.get_by_id(id)
        if not turno:
            raise ValueError(f"No se encontró el turno con ID {id}.")
        return TurnoRead.model_validate(turno)

    def obtener_turno(self, id: int) -> Turno:
        turno = self.repository.get_by_id_with_especialidad(id)
        if not turno:
            raise ValueError(f"No se encontró el turno con ID {id}.")
        return turno

    def crear_turno(self, turno_in: TurnoCreate) -> TurnoRead:
        datos_turno = turno_in.model_dump()
        turno = Turno.model_validate(datos_turno)
        turno_creado = self.repository.add(turno)
        return TurnoRead.model_validate(turno_creado)
    
    def obtener_turnos_por_paciente(self, dni_paciente: int) -> list[TurnoRead]:
        turnos = self.repository.get_by_paciente(dni_paciente)
        return [TurnoRead.model_validate(t) for t in turnos]
    
    def obtener_turnos_por_estado(self, nombre_estado: str) -> list[TurnoRead]:
        turnos = self.repository.get_by_estado(nombre_estado)
        return [TurnoRead.model_validate(t) for t in turnos]
    
    def liberar_turno(self, id: int) -> TurnoRead:
        
        turno = self.obtener_turno(id)
        turno.liberar()
        turno_actualizado = self.repository.update(turno)
        return TurnoRead.model_validate(turno_actualizado)
    
    def agendar_turno(self, id: int, dni_paciente: int) -> TurnoRead:
        turno = self.obtener_turno(id)

        if not self.paciente_service.existe_paciente(dni_paciente):
            raise ValueError(f"No se encontró el paciente con DNI {dni_paciente}.")
        
        paciente = self.paciente_service.obtener_por_id(dni_paciente)
        cobertura = paciente.obra_social.porcentaje_cobertura if paciente and paciente.obra_social else 0.0

        turno.agendar(dni_paciente, cobertura)
        turno_actualizado = self.repository.update(turno)
        return TurnoRead.model_validate(turno_actualizado)
    
    def iniciar_turno(self, id: int) -> TurnoRead:
        turno = self.obtener_turno(id)
        turno.iniciar()
        turno_actualizado = self.repository.update(turno)
        return TurnoRead.model_validate(turno_actualizado)
    
    def finalizar_turno(self, id: int, consulta: ConsultaCreate) -> TurnoRead:
        turno = self.obtener_turno(id)
        # Asignar el id_turno a la consulta
        consulta.id_turno = id
        self.consulta_service.crear_consulta(consulta)
        turno.finalizar()
        turno_actualizado = self.repository.update(turno)
        return TurnoRead.model_validate(turno_actualizado)
    
    def cancelar_turno(self, id: int) -> TurnoRead:
        turno = self.obtener_turno(id)
        turno.cancelar()
        turno_actualizado = self.repository.update(turno)
        return TurnoRead.model_validate(turno_actualizado) 
    
    def obtener_turnos_by_agenda(self, id_agenda: int) -> list[TurnoRead]:
        turnos = self.repository.get_by_agenda(id_agenda)
        if not turnos:
            raise ValueError(f"No se encontraron turnos para la agenda con ID {id_agenda}.")
        return [TurnoRead.model_validate(t) for t in turnos]
    
    def obtener_turnos_by_agenda_and_days(self, id_agenda: int, dias: list[int]) -> list[TurnoRead]:
        turnos = self.repository.get_by_agenda_and_days(id_agenda, dias)
        if not turnos:
            raise ValueError(f"No se encontraron turnos para la agenda con ID {id_agenda} en los días {dias}.")
        return [TurnoRead.model_validate(t) for t in turnos]
    
    def marcar_inasistencia(self, id: int) -> TurnoRead:
        turno = self.obtener_turno(id)
        turno.marcar_inasistencia()
        turno_actualizado = self.repository.update(turno)
        return TurnoRead.model_validate(turno_actualizado)