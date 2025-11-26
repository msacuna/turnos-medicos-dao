from fastapi import Depends

from app.services import *
from app.repositories import *
from app.domain.models import *

# SIMILAR AL CONTENEDOR DE JAVA SPRING (Manejo de Beans y Dependencias internamente)

def get_especialidad_repo() -> EspecialidadRepository:
    return EspecialidadRepository(model=Especialidad)
def get_especialidad_service(repo: EspecialidadRepository = Depends(get_especialidad_repo)) -> EspecialidadService:
    return EspecialidadService(repo)

def get_laboratorio_repo() -> LaboratorioRepository:
    return LaboratorioRepository(model=Laboratorio)
def get_laboratorio_service(repo: LaboratorioRepository = Depends(get_laboratorio_repo)) -> LaboratorioService:
    return LaboratorioService(repo)

def get_medicamento_repo() -> MedicamentoRepository:
    return MedicamentoRepository(model=Medicamento)
def get_medicamento_service(
            repo: MedicamentoRepository = Depends(get_medicamento_repo),
            laboratorio_service: LaboratorioService = Depends(get_laboratorio_service)) -> MedicamentoService:
    return MedicamentoService(repo, laboratorio_service)

def get_alergia_repo() -> AlergiaRepository:
    return AlergiaRepository(model=Alergia)
def get_alergia_service(repo: AlergiaRepository = Depends(get_alergia_repo)) -> AlergiaService:
    return AlergiaService(repo)

def get_antecedente_repo() -> AntecedenteRepository:
    return AntecedenteRepository(model=Antecedente)
def get_antecedente_service(repo: AntecedenteRepository = Depends(get_antecedente_repo)) -> AntecedenteService:
    return AntecedenteService(repo)

def get_obra_social_repo() -> ObraSocialRepository:
    return ObraSocialRepository(model=ObraSocial)
def get_obra_social_service(repo: ObraSocialRepository = Depends(get_obra_social_repo)) -> ObraSocialService:
    return ObraSocialService(repo)

def get_grupo_sanguineo_repo() -> GrupoSanguineoRepository:
    return GrupoSanguineoRepository(model=GrupoSanguineo)
def get_grupo_sanguineo_service(repo: GrupoSanguineoRepository = Depends(get_grupo_sanguineo_repo)) -> GrupoSanguineoService:
    return GrupoSanguineoService(repo)

def get_paciente_repo() -> PacienteRepository:
    return PacienteRepository(model=Paciente)
def get_paciente_service(
            repo: PacienteRepository = Depends(get_paciente_repo),
            alergia_service: AlergiaService = Depends(get_alergia_service),
            antecedente_service: AntecedenteService = Depends(get_antecedente_service),
            grupo_sanguineo_service: GrupoSanguineoService = Depends(get_grupo_sanguineo_service),
            obra_social_service: ObraSocialService = Depends(get_obra_social_service)) -> PacienteService:
    return PacienteService(repo, alergia_service, antecedente_service, grupo_sanguineo_service, obra_social_service)

def get_profesional_repo() -> ProfesionalRepository:
    return ProfesionalRepository(model=Profesional)
def get_horario_atencion_repo() -> HorarioAtencionRepository:
    return HorarioAtencionRepository(model=HorarioAtencion)
def get_horario_profesional_service(
            horario_repo: HorarioAtencionRepository = Depends(get_horario_atencion_repo),
            profesional_repo: ProfesionalRepository = Depends(get_profesional_repo)) -> HorarioProfesionalService:
    return HorarioProfesionalService(horario_repo, profesional_repo)