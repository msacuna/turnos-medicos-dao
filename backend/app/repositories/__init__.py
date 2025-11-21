from .base import BaseRepository
from .especialidad_repo import EspecialidadRepository
from .medicamento_repo import MedicamentoRepository
from .alergia_repo import AlergiaRepository
from .antecedente_repo import AntecedenteRepository
from .laboratorio_repo import LaboratorioRepository
from .obra_social_repo import ObraSocialRepository

__all__ = [
    "BaseRepository",
    "EspecialidadRepository",
    "MedicamentoRepository",
    "AlergiaRepository",
    "AntecedenteRepository",
    "LaboratorioRepository",
    "ObraSocialRepository",
]