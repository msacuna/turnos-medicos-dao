# app/core/dependencies.py
from fastapi import Depends
from sqlmodel import Session
from app.core.database import get_session

from app.services import *
from app.repositories import *
from app.domain.models import *

def get_especialidad_repo(session: Session = Depends(get_session)) -> EspecialidadRepository:
    return EspecialidadRepository(session, model=Especialidad)
def get_especialidad_service(repo: EspecialidadRepository = Depends(get_especialidad_repo)) -> EspecialidadService:
    return EspecialidadService(repo)