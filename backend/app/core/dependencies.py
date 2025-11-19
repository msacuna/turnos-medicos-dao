# app/core/dependencies.py
from fastapi import Depends
from sqlmodel import Session
from .database import get_db

# Services
from app.services import EspecialidadService

# ESTO ES PARA INYECTAR DEPENDENCIAS NECESARIAS EN LOS SERVICIOS (db Session)
# Factory functions para cada servicio
def get_especialidad_service(db: Session = Depends(get_db)) -> EspecialidadService:
    return EspecialidadService(db)
