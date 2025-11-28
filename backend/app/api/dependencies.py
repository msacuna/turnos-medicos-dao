from fastapi import Depends
from sqlmodel import Session
from app.core.database import get_session
from app.services import *
from app.repositories import *
from app.domain.models import *


# SIMILAR AL CONTENEDOR DE JAVA SPRING (Manejo de Beans y Dependencias internamente)

def get_especialidad_repo(session: Session = Depends(get_session)) -> EspecialidadRepository:
    return EspecialidadRepository(model=Especialidad, session=session)
def get_especialidad_service(repo: EspecialidadRepository = Depends(get_especialidad_repo)) -> EspecialidadService:
    return EspecialidadService(repo)

def get_laboratorio_repo(session: Session = Depends(get_session)) -> LaboratorioRepository:
    return LaboratorioRepository(model=Laboratorio, session=session)
def get_laboratorio_service(repo: LaboratorioRepository = Depends(get_laboratorio_repo)) -> LaboratorioService:
    return LaboratorioService(repo)

def get_medicamento_repo(session: Session = Depends(get_session)) -> MedicamentoRepository:
    return MedicamentoRepository(model=Medicamento, session=session)
def get_medicamento_service(
            repo: MedicamentoRepository = Depends(get_medicamento_repo),
            laboratorio_service: LaboratorioService = Depends(get_laboratorio_service)) -> MedicamentoService:
    return MedicamentoService(repo, laboratorio_service)

    

def get_alergia_repo(session: Session = Depends(get_session)) -> AlergiaRepository:
    return AlergiaRepository(model=Alergia, session=session)
def get_alergia_service(repo: AlergiaRepository = Depends(get_alergia_repo)) -> AlergiaService:
    return AlergiaService(repo)

def get_antecedente_repo(session: Session = Depends(get_session)) -> AntecedenteRepository:
    return AntecedenteRepository(model=Antecedente, session=session)
def get_antecedente_service(repo: AntecedenteRepository = Depends(get_antecedente_repo)) -> AntecedenteService:
    return AntecedenteService(repo)

def get_obra_social_repo(session: Session = Depends(get_session)) -> ObraSocialRepository:
    return ObraSocialRepository(model=ObraSocial, session=session)
def get_obra_social_service(repo: ObraSocialRepository = Depends(get_obra_social_repo)) -> ObraSocialService:
    return ObraSocialService(repo)

def get_grupo_sanguineo_repo(session: Session = Depends(get_session)) -> GrupoSanguineoRepository:
    return GrupoSanguineoRepository(model=GrupoSanguineo, session=session)
def get_grupo_sanguineo_service(repo: GrupoSanguineoRepository = Depends(get_grupo_sanguineo_repo)) -> GrupoSanguineoService:
    return GrupoSanguineoService(repo)

def get_paciente_repo(session: Session = Depends(get_session)) -> PacienteRepository:
    return PacienteRepository(model=Paciente, session=session)
def get_paciente_service(
            repo: PacienteRepository = Depends(get_paciente_repo),
            alergia_service: AlergiaService = Depends(get_alergia_service),
            antecedente_service: AntecedenteService = Depends(get_antecedente_service),
            grupo_sanguineo_service: GrupoSanguineoService = Depends(get_grupo_sanguineo_service),
            obra_social_service: ObraSocialService = Depends(get_obra_social_service)) -> PacienteService:
    return PacienteService(repo, alergia_service, antecedente_service, grupo_sanguineo_service, obra_social_service)

def get_profesional_repo(session: Session = Depends(get_session)) -> ProfesionalRepository:
    return ProfesionalRepository(model=Profesional, session=session)

def get_profesional_service(
            repo: ProfesionalRepository = Depends(get_profesional_repo),
            especialidad_service: EspecialidadService = Depends(get_especialidad_service)) -> ProfesionalService:
    return ProfesionalService(repo, especialidad_service)


def get_horario_atencion_repo(session: Session = Depends(get_session)) -> HorarioAtencionRepository:
    return HorarioAtencionRepository(model=HorarioAtencion, session=session)
def get_horario_profesional_service(
            horario_repo: HorarioAtencionRepository = Depends(get_horario_atencion_repo),
            profesional_repo: ProfesionalRepository = Depends(get_profesional_repo)) -> HorarioProfesionalService:
    return HorarioProfesionalService(horario_repo, profesional_repo)

def get_estado_turno_repo(session: Session = Depends(get_session)) -> EstadoTurnoRepository:
    return EstadoTurnoRepository(model=EstadoTurno, session=session)

def get_estado_turno_service(repo: EstadoTurnoRepository = Depends(get_estado_turno_repo)) -> EstadoTurnoService:
    return EstadoTurnoService(repo)

def get_detalle_receta_repo(session: Session = Depends(get_session)) -> DetalleRecetaRepository:
    return DetalleRecetaRepository(model=DetalleReceta, session=session)
def get_detalle_receta_service(
            repo: DetalleRecetaRepository = Depends(get_detalle_receta_repo),
            medicamento_service: MedicamentoService = Depends(get_medicamento_service)) -> DetalleRecetaService:
    return DetalleRecetaService(repo, medicamento_service)

def get_receta_repo(session: Session = Depends(get_session)) -> RecetaRepository:
    return RecetaRepository(model=Receta, session=session)
def get_receta_service(
            repo: RecetaRepository = Depends(get_receta_repo),
            detalle_receta_service: DetalleRecetaService = Depends(get_detalle_receta_service)) -> RecetaService:
    return RecetaService(repo, detalle_receta_service)

def get_consulta_repo(session: Session = Depends(get_session)) -> ConsultaRepository:
    return ConsultaRepository(model=Consulta, session=session)
def get_consulta_service(
            consulta_repository: ConsultaRepository = Depends(get_consulta_repo),
            receta_service: RecetaService = Depends(get_receta_service),
            detalle_receta_service: DetalleRecetaService = Depends(get_detalle_receta_service)) -> ConsultaService:
    return ConsultaService(consulta_repository, receta_service, detalle_receta_service)

def get_turno_repo(session: Session = Depends(get_session)) -> TurnoRepository:
    return TurnoRepository(model=Turno, session=session)
def get_turno_service(
            repo: TurnoRepository = Depends(get_turno_repo),
            estado_turno_service: EstadoTurnoService = Depends(get_estado_turno_service),
            paciente_service: PacienteService = Depends(get_paciente_service),
            consulta_service: ConsultaService = Depends(get_consulta_service)) -> TurnoService:
    return TurnoService(repo, estado_turno_service, paciente_service, consulta_service)

def get_agenda_profesional_repo(session: Session = Depends(get_session)) -> AgendaProfesionalRepo:
    return AgendaProfesionalRepo(model=AgendaProfesional, session=session)
def get_agenda_profesional_service(
            repo: AgendaProfesionalRepo = Depends(get_agenda_profesional_repo),
            horario_profesional_service: HorarioProfesionalService = Depends(get_horario_profesional_service),
            profesional_service: ProfesionalService = Depends(get_profesional_service),
            turno_service: TurnoService = Depends(get_turno_service)) -> AgendaProfesionalService:
    return AgendaProfesionalService(repo, horario_profesional_service, profesional_service, turno_service)

def get_reporte_repo(session: Session = Depends(get_session)) -> ReporteRepository:
    return ReporteRepository(session=session)
def get_reporte_service(repo: ReporteRepository = Depends(get_reporte_repo)) -> ReporteService:
    return ReporteService(repo)