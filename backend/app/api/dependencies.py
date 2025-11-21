from fastapi import Depends
from sqlmodel import Session
from app.core.database import get_session

from app.services import *
from app.repositories import *
from app.domain.models import *

# SIMILAR AL CONTENEDOR DE JAVA SPRING (Manejo de Beans y Dependencias internamente)

def get_especialidad_repo(session: Session = Depends(get_session)) -> EspecialidadRepository:
    return EspecialidadRepository(session, model=Especialidad)
def get_especialidad_service(repo: EspecialidadRepository = Depends(get_especialidad_repo)) -> EspecialidadService:
    return EspecialidadService(repo)

def get_laboratorio_repo(session: Session = Depends(get_session)) -> LaboratorioRepository:
    return LaboratorioRepository(session, model=Laboratorio)
def get_laboratorio_service(repo: LaboratorioRepository = Depends(get_laboratorio_repo)) -> LaboratorioService:
    return LaboratorioService(repo)

def get_medicamento_repo(session: Session = Depends(get_session)) -> MedicamentoRepository:
    return MedicamentoRepository(session, model=Medicamento)
def get_medicamento_service(
        repo: MedicamentoRepository = Depends(get_medicamento_repo),
        laboratorio_repo: LaboratorioRepository = Depends(get_laboratorio_repo)) -> MedicamentoService:
    return MedicamentoService(repo, laboratorio_repo)

def get_alergia_repo(session: Session = Depends(get_session)) -> AlergiaRepository:
    return AlergiaRepository(session, model=Alergia)
def get_alergia_service(repo: AlergiaRepository = Depends(get_alergia_repo)) -> AlergiaService:
    return AlergiaService(repo)

def get_antecedente_repo(session: Session = Depends(get_session)) -> AntecedenteRepository:
    return AntecedenteRepository(session, model=Antecedente)
def get_antecedente_service(repo: AntecedenteRepository = Depends(get_antecedente_repo)) -> AntecedenteService:
    return AntecedenteService(repo)