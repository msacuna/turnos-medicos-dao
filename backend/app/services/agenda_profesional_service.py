

from backend.app.repositories.agenda_profesional_repo import AgendaProfesionalRepo
from backend.app.services.horario_profesional_service import HorarioProfesionalService
from app.domain.models import Profesional
from backend.app.services.interfaces.sujeto_turno import SujetoTurno
from backend.app.services.notificador_email import NotificadorEmail
from backend.app.services.notificador_sms import NotificadorSMS
from backend.app.services.profesional_service import ProfesionalService
from app.domain.models.agenda_profesional import AgendaProfesional
from backend.app.services.turno_service import TurnoService
from backend.app.domain.schemas.turno import TurnoCreate
from datetime import date, time, timedelta, datetime
from app.domain.models.horario_atencion import DiaSemanaEnum
import calendar


class AgendaProfesionalService(SujetoTurno):

    

    def __init__(self, agenda_repo: AgendaProfesionalRepo, horarios_profesional_service: HorarioProfesionalService,
                 profesional_service: ProfesionalService, turno_service: TurnoService):
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

    def crear_agenda(self, id_profesional: int):
        # 1. Validar que el profesional existe
        profesional = self.profesional_service.profesional_repo.get_by_id(id_profesional)
        if not profesional:
            raise ValueError(f"No se encontró el profesional con ID {id_profesional}")
        
        # 2. Obtener horarios del profesional
        horarios = self.horarios_profesional_service.get_by_profesional(id_profesional)
        if not horarios:
            raise ValueError(f"El profesional con ID {id_profesional} no tiene horarios asignados.")
        


        # 3. Calcular el mes siguiente
        fecha_actual = date.today()
        anio_siguiente = fecha_actual.year
        mes_siguiente = fecha_actual.month + 1
        
        # Si es diciembre, pasar al siguiente año
        if mes_siguiente > 12:
            mes_siguiente = 1
            anio_siguiente += 1
        
        # 4. Verificar que no exista una agenda para ese profesional, año y mes
        agenda_existente = self.agenda_repo.get_agenda_by_profesional_anio_mes(
            id_profesional, anio_siguiente, mes_siguiente
        )
        if agenda_existente:
            raise ValueError(f"Ya existe una agenda para el profesional {id_profesional} en {mes_siguiente}/{anio_siguiente}")
        
        # 5. Crear la agenda para el mes siguiente
        nueva_agenda = AgendaProfesional(
            id_profesional=id_profesional,
            anio=anio_siguiente,
            mes=mes_siguiente
        )
        agenda_creada = self.agenda_repo.create(nueva_agenda)
        
        # 5. Generar turnos para cada día del mes según horarios
        self._generar_turnos_del_mes(agenda_creada.id, profesional.id_especialidad, horarios, anio_siguiente, mes_siguiente)
        
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
        turnos = self.turno_service.obtener_turnos_by_agenda_and_days(id_agenda, dias)
        
        # 2. Matriz para almacenar los datos de notificación
        datos_notificacion = []
        
        # 3. Cancelar cada turno y recopilar datos
        for turno in turnos:
            # Solo procesar turnos que tengan paciente asignado
            if turno.dni_paciente and turno.paciente:
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

        # 4. Notificar a los suscriptores sobre los turnos cancelados --> Patron Observer

        self.agregar_suscriptor(NotificadorEmail())
        self.agregar_suscriptor(NotificadorSMS())
        self.notificar(datos_notificacion)
        self.eliminar_suscriptor(NotificadorEmail())
        self.eliminar_suscriptor(NotificadorSMS())
        
        