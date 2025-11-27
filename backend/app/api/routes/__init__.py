from .especialidad import router as especialidad_router
from .medicamento import router as medicamentos_router
from .laboratorio import router as laboratorios_router
from .alergia import router as alergias_router
from .antecedente import router as antecedentes_router
from .obra_social import router as obras_sociales_router
from .paciente import router as pacientes_router
from .profesional import router as profesionales_router
from .turno import router as turnos_router
from .reportes import router as reportes_router

__all__ = [
    "especialidad_router",
    "medicamentos_router",
    "laboratorios_router",
    "alergias_router",
    "antecedentes_router",
    "obras_sociales_router",
    "pacientes_router",
    "profesionales_router",
    "turnos_router",
    "reportes_router",
]