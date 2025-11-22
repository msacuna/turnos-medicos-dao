from .especialidad import EspecialidadCreate, EspecialidadUpdate, EspecialidadRead
from .medicamento import MedicamentoCreate, MedicamentoUpdate, MedicamentoRead
from .laboratorio import LaboratorioCreate, LaboratorioUpdate, LaboratorioRead
from .alergia import AlergiaCreate, AlergiaUpdate, AlergiaRead
from .antecedente import AntecedenteCreate, AntecedenteUpdate, AntecedenteRead
from .obra_social import ObraSocialCreate, ObraSocialUpdate, ObraSocialRead
from .paciente import PacienteCreate, PacienteUpdate, PacienteRead
from .grupo_sanguineo import GrupoSanguineoRead
from .motivo_consulta import MotivoConsultaCreate, MotivoConsultaUpdate, MotivoConsultaRead

__all__ = [
    "EspecialidadCreate",
    "EspecialidadUpdate",
    "EspecialidadRead",
    "MedicamentoCreate",
    "MedicamentoUpdate",
    "MedicamentoRead",
    "LaboratorioCreate",
    "LaboratorioUpdate",
    "LaboratorioRead",
    "AlergiaCreate",
    "AlergiaUpdate",
    "AlergiaRead",
    "AntecedenteCreate",
    "AntecedenteUpdate",
    "AntecedenteRead",
    "ObraSocialCreate",
    "ObraSocialUpdate",
    "ObraSocialRead",
    "PacienteCreate",
    "PacienteUpdate",
    "PacienteRead",
    "GrupoSanguineoRead",
    "MotivoConsultaCreate",
    "MotivoConsultaUpdate",
    "MotivoConsultaRead",
]