

from typing import TYPE_CHECKING

from app.core.exceptions import ReglaDeNegocioException, RecursoNoEncontradoException
from app.repositories.agenda_profesional_repo import AgendaProfesionalRepo
from app.services.horario_profesional_service import HorarioProfesionalService
from app.domain.models import Profesional
from app.services.interfaces.sujeto_turno import SujetoTurno
from app.services.notificador_email import NotificadorEmail
from app.services.notificador_sms import NotificadorSMS
from app.domain.schemas.agenda_profesional import AgendaProfesionalRead
if TYPE_CHECKING:
    from app.services.profesional_service import ProfesionalService
from app.domain.models.agenda_profesional import AgendaProfesional
from app.services.turno_service import TurnoService
from app.domain.schemas.turno import TurnoCreate, TurnoRead
from datetime import date, time, timedelta, datetime
from app.domain.models.horario_atencion import DiaSemanaEnum
import calendar


class AgendaProfesionalService(SujetoTurno):

    

    def __init__(self, agenda_repo: AgendaProfesionalRepo, horarios_profesional_service: HorarioProfesionalService,
                 profesional_service: "ProfesionalService", turno_service: TurnoService):
        self.agenda_repo = agenda_repo
        self.horarios_profesional_service = horarios_profesional_service
        self.profesional_service = profesional_service
        self.turno_service = turno_service
        self.suscriptores: list = []

    def agregar_suscriptor(self, suscriptor):
        self.suscriptores.append(suscriptor)

    def eliminar_suscriptor(self, suscriptor):
        return self.suscriptores.remove(suscriptor)

    def notificar(self, pacientes: list[list[str]]):
        for suscriptor in self.suscriptores:
            suscriptor.actualizar(pacientes)

    def crear_agenda(self, id_profesional: int, mes: int ):
        # 1. Validar que el mes está en el rango correcto (1-12)
        if mes < 1 or mes > 12:
            raise ReglaDeNegocioException(f"El mes debe estar entre 1 y 12. Valor recibido: {mes}")
        
        # 2. Validar que el mes no sea menor al mes actual
        fecha_actual = date.today()
        if mes < fecha_actual.month:
            raise ReglaDeNegocioException(f"No se puede crear una agenda para un mes anterior al actual. Mes actual: {fecha_actual.month}, mes solicitado: {mes}")
        
        # 3. Validar que el profesional existe
        profesional = self.profesional_service.profesional_repo.get_by_id(id_profesional)
        if not profesional:
            raise RecursoNoEncontradoException(f"No se encontró el profesional con ID {id_profesional}")
        
        # 4. Obtener horarios del profesional
        horarios = self.horarios_profesional_service.get_by_profesional(id_profesional)
        if not horarios:
            raise ReglaDeNegocioException(f"El profesional con ID {id_profesional} no tiene horarios asignados.")

        # 5. Calcular el año correspondiente (siempre el año actual para meses >= mes actual)
        anio_agenda = fecha_actual.year
        
        # 6. Verificar que no exista una agenda para ese profesional, año y mes
        agenda_existente = self.agenda_repo.get_agenda_by_profesional_anio_mes(
            id_profesional, anio_agenda, mes
        )
        if agenda_existente:
            raise ReglaDeNegocioException(f"Ya existe una agenda para el profesional {id_profesional} en {mes}/{anio_agenda}")
        
        # 7. Crear la agenda para el mes solicitado
        nueva_agenda = AgendaProfesional(
            id_profesional=id_profesional,
            anio=anio_agenda,
            mes=mes
        )
        agenda_creada = self.agenda_repo.add(nueva_agenda)
        
        # 8. Generar turnos para cada día del mes según horarios
        self._generar_turnos_del_mes(agenda_creada.id, profesional.id_especialidad, horarios, anio_agenda, mes)
        
        return agenda_creada
    
    def _generar_turnos_del_mes(self, id_agenda: int, id_especialidad: int, horarios, anio: int, mes: int):
        """Genera turnos de 30 minutos para cada día del mes según los horarios del profesional"""
        
        # Mapeo de días de semana
        dias_semana_map = {
            0: DiaSemanaEnum.Lunes,
            1: DiaSemanaEnum.Martes, 
            2: DiaSemanaEnum.Miercoles,
            3: DiaSemanaEnum.Jueves,
            4: DiaSemanaEnum.Viernes,
            5: DiaSemanaEnum.Sabado,
            6: None  # Domingo no está en el enum
        }
        
        # Obtener todos los días del mes
        _, ultimo_dia = calendar.monthrange(anio, mes)
        
        for dia in range(1, ultimo_dia + 1):
            fecha_actual = date(anio, mes, dia)
            dia_semana_num = fecha_actual.weekday()
            
            # Saltar domingo (no está en el enum)
            if dias_semana_map[dia_semana_num] is None:
                continue
                
            dia_semana = dias_semana_map[dia_semana_num]
            
            # Buscar horario para este día
            horario_del_dia = None
            for horario in horarios:
                if horario.dia_semana == dia_semana:
                    horario_del_dia = horario
                    break
            
            # Si no hay horario para este día, continuar
            if not horario_del_dia:
                continue
                
            # Generar turnos de 30 minutos para este día
            self._crear_turnos_del_dia(
                id_agenda=id_agenda,
                id_especialidad=id_especialidad,
                fecha=fecha_actual,
                hora_inicio=horario_del_dia.hora_inicio,
                hora_fin=horario_del_dia.hora_fin
            )
    
    def _crear_turnos_del_dia(self, id_agenda: int, id_especialidad: int, fecha: date, 
                             hora_inicio: time, hora_fin: time):
        """Crea turnos de 30 minutos para un día específico"""
        
        # Convertir time a datetime para facilitar cálculos
        fecha_inicio = datetime.combine(fecha, hora_inicio)
        fecha_fin = datetime.combine(fecha, hora_fin)
        
        # Generar turnos de 30 minutos
        hora_actual = fecha_inicio
        while hora_actual + timedelta(minutes=30) <= fecha_fin:
            hora_fin_turno = hora_actual + timedelta(minutes=30)
            
            # Crear el turno
            turno_data = TurnoCreate(
                fecha=fecha,
                hora_inicio=hora_actual.time(),
                hora_fin_estimada=hora_fin_turno.time(),
                dni_paciente=None,  # Disponible
                id_especialidad=id_especialidad,
                id_agenda_profesional=id_agenda
            )
            
            # Guardar el turno usando el servicio
            self.turno_service.crear_turno(turno_data)
            
            # Avanzar 30 minutos
            hora_actual = hora_fin_turno

    def cancelar_turnos(self, id_agenda: int, dias: list[int]) -> None:
        """
        Cancela turnos de una agenda para días específicos del mes.
        
        Args:
            id_agenda: ID de la agenda profesional
            dias: Lista de días del mes (ej: [5, 10, 15])
            
        Returns:
            Matriz con formato [[email, telefono, fecha_hora], ...] donde fecha_hora es "YYYY-MM-DD HH:MM:SS"
        """
        # 1. Obtener turnos de la agenda para los días especificados
        turnos = self.turno_service.repository.get_by_agenda_and_days(id_agenda, dias)
        
        # 2. Matriz para almacenar los datos de notificación
        datos_notificacion = []
        
        # 3. Cancelar cada turno y recopilar datos
        for turno in turnos:
            # Solo procesar turnos que tengan paciente asignado
            if turno.estado.nombre == "Agendado":
                # Obtener email del paciente
                email_paciente = turno.paciente.email

                # Obtener telefono del paciente
                telefono_paciente = turno.paciente.telefono
                
                # Formatear fecha y hora como string
                fecha_hora = f"{turno.fecha} {turno.hora_inicio}"
                
                
                # Agregar a la matriz de notificación
                datos_notificacion.append([email_paciente, telefono_paciente, fecha_hora])
                
                # Cancelar el turno usando el servicio
                self.turno_service.cancelar_turno(turno.id)
            elif turno.estado.nombre == "Disponible":
                # Cancelar el turno usando el servicio
                self.turno_service.cancelar_turno(turno.id)

        # 4. Notificar a los suscriptores sobre los turnos cancelados --> Patron Observer

        self.agregar_suscriptor(NotificadorEmail())
        self.agregar_suscriptor(NotificadorSMS())
        self.notificar(datos_notificacion)
        for suscriptor in self.suscriptores:
            self.eliminar_suscriptor(suscriptor)

        return datos_notificacion

        
    # def get_agenda_actual_por_profesional(self, id_profesional: int) -> AgendaProfesionalRead:
    #     """Obtiene la agenda del mes actual para un profesional dado"""
    #     fecha_actual = date.today()
    #     anio_actual = fecha_actual.year
    #     mes_actual = fecha_actual.month
        
    #     agenda = self.agenda_repo.get_agenda_by_profesional_anio_mes(
    #         id_profesional, anio_actual, mes_actual
    #     )

    #     if not agenda:
    #         raise ValueError(f"No se encontró una agenda para el profesional {id_profesional} en {mes_actual}/{anio_actual}")
        
    #     return AgendaProfesionalRead.model_validate(agenda)
    
    # def get_agenda_siguiente_por_profesional(self, id_profesional: int) -> AgendaProfesionalRead:
    #     """Obtiene la agenda del mes siguiente para un profesional dado"""
    #     fecha_actual = date.today()
    #     anio_siguiente = fecha_actual.year
    #     mes_siguiente = fecha_actual.month + 1
        
    #     # Si es diciembre, pasar al siguiente año
    #     if mes_siguiente > 12:
    #         mes_siguiente = 1
    #         anio_siguiente += 1
        
    #     agenda = self.agenda_repo.get_agenda_by_profesional_anio_mes(
    #         id_profesional, anio_siguiente, mes_siguiente
    #     )

    #     if not agenda:
    #         raise ValueError(f"No se encontró una agenda para el profesional {id_profesional} en {mes_siguiente}/{anio_siguiente}")
        
    #     return AgendaProfesionalRead.model_validate(agenda)
    
    
    def get_turnos_de_agenda(self, id_profesional:int, id_agenda: int) -> list[TurnoRead]:
        """Obtiene todos los turnos asociados a una agenda profesional"""
        agenda = self.agenda_repo.get_by_id(id_agenda)

        if not agenda:
            raise RecursoNoEncontradoException(f"No se encontró la agenda profesional con ID {id_agenda}")
        if agenda.id_profesional != id_profesional:
            raise ValueError(f"La agenda con ID {id_agenda} no pertenece al profesional con ID {id_profesional}")
        
        turnos = self.turno_service.obtener_turnos_by_agenda(id_agenda)
        return [TurnoRead.model_validate(turno) for turno in turnos]

    def get_agenda_por_profesional_y_mes(self, id_profesional: int, mes: int) -> AgendaProfesionalRead: 
        """Obtiene la agenda de un profesional para un mes específico del año actual"""
        fecha_actual = date.today()
        anio_actual = fecha_actual.year
        
        agenda = self.agenda_repo.get_agenda_by_profesional_anio_mes(
            id_profesional, anio_actual, mes
        )

        if not agenda:  
            raise RecursoNoEncontradoException(f"No se encontró una agenda para el profesional {id_profesional} en {mes}/{anio_actual}")
        
        return AgendaProfesionalRead.model_validate(agenda)
    
    