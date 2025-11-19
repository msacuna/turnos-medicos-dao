from fastapi import Depends, HTTPException, status
from sqlmodel import Session
from app.models import Especialidad
from app.repositories import EspecialidadRepository

class EspecialidadService:
    def __init__(self, db: Session):
        self.repository = EspecialidadRepository(db, Especialidad)

    def crear_especialidad(self, nombre: str) -> Especialidad:
        existente = self.repository.get_by_nombre(nombre)
        if existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"La especialidad '{nombre}' ya existe."
            )
        nueva = Especialidad(nombre=nombre)
        return self.repository.create(nueva)

    def obtener_todas(self) -> list[Especialidad]:
        return self.repository.get_all()
    
    def obtener_por_id(self, id: int) -> Especialidad:
        especialidad = self.repository.get_by_id(id)
        if not especialidad:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"La especialidad con ID {id} no existe."
            )
        return especialidad