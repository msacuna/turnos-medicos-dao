from .especialidad import router as especialidad_router
from .medicamento import router as medicamentos_router
from .laboratorio import router as laboratorios_router
from .alergia import router as alergias_router
from .antecedente import router as antecedentes_router

__all__ = [
    "especialidad_router",
    "medicamentos_router",
    "laboratorios_router",
    "alergias_router",
    "antecedentes_router",
]