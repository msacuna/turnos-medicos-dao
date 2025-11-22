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