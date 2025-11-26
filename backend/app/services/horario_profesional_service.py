from app.domain.models import HorarioAtencion
from typing import Optional
from datetime import time
from app.repositories import HorarioAtencionRepository, ProfesionalRepository
from app.domain.models import DiaSemanaEnum
from app.domain.schemas import HorarioProfesionalRead

class HorarioProfesionalService:

    def __init__(self, 
                 horario_repo: HorarioAtencionRepository, 
                 profesional_repo: ProfesionalRepository):
        self.horario_repo = horario_repo
        self.profesional_repo = profesional_repo

    def get_by_profesional(self, profesional_id: int) -> list[HorarioProfesionalRead]:
        """Obtiene todos los horarios de un profesional"""
        profesional = self.profesional_repo.get_by_id(profesional_id)
        if not profesional:
            raise ValueError(f"Profesional con ID {profesional_id} no encontrado")
        
        horarios_response = []
        for horario in profesional.horarios_atencion:
            horarios_response.append(HorarioProfesionalRead.model_validate({
                'horario_id': horario.id,
                'dia_semana': horario.dia_semana,
                'hora_inicio': horario.hora_inicio,
                'hora_fin': horario.hora_fin,
                'profesional_id': profesional_id
            }))
        
        return horarios_response
    
    def configurar_horario_dia(
        self, 
        profesional_id: int, 
        dia: DiaSemanaEnum, 
        inicio: time | None, 
        fin: time | None, 
        trabaja: bool
    ) -> Optional[HorarioProfesionalRead]:
        
        # 1. Verificar profesional
        if not self.profesional_repo.get_by_id(profesional_id):
            raise ValueError(f"Profesional {profesional_id} no encontrado")

        # 2. Lógica de Negocio
        if not trabaja:
            # Si no trabaja, nos aseguramos de borrar cualquier registro existente para ese día
            self.horario_repo.delete_by_dia_y_profesional(profesional_id, dia)
            return None

        if inicio is None or fin is None:
            raise ValueError("Si trabaja, debe indicar hora de inicio y fin")
        
        if inicio >= fin:
             raise ValueError("La hora de inicio debe ser anterior a la de fin")

        # 3. Buscar registro existente (Upsert)
        horario_existente = self.horario_repo.get_by_dia_y_profesional(profesional_id, dia)

        if horario_existente:
            # ACTUALIZAR (Update)
            # Modificamos el objeto existente y el repositorio base guarda los cambios
            horario_existente.hora_inicio = inicio
            horario_existente.hora_fin = fin
            # BaseRepository.update suele recibir un dict o el objeto modificado+add
            horario_guardado = self.horario_repo.add(horario_existente) 
        else:
            # CREAR (Insert)
            nuevo_horario = HorarioAtencion(
                id_profesional=profesional_id, # Vinculación directa
                dia_semana=dia,
                hora_inicio=inicio,
                hora_fin=fin
            )
            horario_guardado = self.horario_repo.add(nuevo_horario)

        return HorarioProfesionalRead.model_validate({
            'profesional_id': profesional_id,
            'horario_id': horario_guardado.id,
            'dia_semana': horario_guardado.dia_semana,
            'hora_inicio': horario_guardado.hora_inicio,
            'hora_fin': horario_guardado.hora_fin
        })

    def eliminar_horario_dia(self, profesional_id: int, dia: DiaSemanaEnum) -> bool:
        """Elimina el horario de un profesional para un día específico"""
        return self.configurar_horario_dia(profesional_id, dia, None, None, False) is None