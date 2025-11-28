

from http.client import HTTPException
from app.api.dependencies import obtener_motivos_consulta_service
from app.domain.models import MotivoConsulta
from app.domain.schemas import MotivoConsultaRead, MotivoConsultaCreate, MotivoConsultaUpdate
from fastapi import APIRouter, Depends


router = APIRouter(prefix="/motivos-consulta", tags=["Motivos de Consulta"])


@router.get("/", response_model=list[MotivoConsultaRead])
def obtener_motivos_consulta(service = Depends(obtener_motivos_consulta_service)):
    try:
        return service.obtener_todos()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
