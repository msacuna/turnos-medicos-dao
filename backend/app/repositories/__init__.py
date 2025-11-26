from .base import BaseRepository
from .especialidad_repo import EspecialidadRepository
from .medicamento_repo import MedicamentoRepository
from .alergia_repo import AlergiaRepository
from .antecedente_repo import AntecedenteRepository
from .laboratorio_repo import LaboratorioRepository
from .obra_social_repo import ObraSocialRepository
from .paciente_repo import PacienteRepository
from .grupo_sanguineo_repo import GrupoSanguineoRepository
from .horario_atencion_repo import HorarioAtencionRepository
from .profesional_repo import ProfesionalRepository

__all__ = [
    "BaseRepository",
    "EspecialidadRepository",
    "MedicamentoRepository",
    "AlergiaRepository",
    "AntecedenteRepository",
    "LaboratorioRepository",
    "ObraSocialRepository",
    "PacienteRepository",
    "GrupoSanguineoRepository",
    "HorarioAtencionRepository",
    "ProfesionalRepository",
]