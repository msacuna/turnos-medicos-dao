from .especialidad import EspecialidadCreate, EspecialidadUpdate, EspecialidadRead
from .medicamento import MedicamentoCreate, MedicamentoUpdate, MedicamentoRead
from .laboratorio import LaboratorioCreate, LaboratorioUpdate, LaboratorioRead
from .alergia import AlergiaCreate, AlergiaUpdate, AlergiaRead
from .antecedente import AntecedenteCreate, AntecedenteUpdate, AntecedenteRead
from .obra_social import ObraSocialCreate, ObraSocialUpdate, ObraSocialRead
from .paciente import PacienteCreate, PacienteUpdate, PacienteRead
from .grupo_sanguineo import GrupoSanguineoRead
from .motivo_consulta import MotivoConsultaCreate, MotivoConsultaUpdate, MotivoConsultaRead
from .horario_atencion import HorarioProfesionalCreate, HorarioProfesionalUpdate, HorarioProfesionalRead
from .horario import HorarioDiaInput
from .profesional import ProfesionalRead, ProfesionalCreate, ProfesionalUpdate
from .detalle_receta import DetalleRecetaCreate, DetalleRecetaRead, DetalleRecetaUpdate
from .receta import RecetaCreate, RecetaRead, RecetaUpdate
from .consulta import ConsultaCreate, ConsultaRead, ConsultaUpdate
from .turno import TurnoRead, TurnoCreate, TurnoUpdate
from .agenda_profesional import AgendaProfesionalRead

# Rebuild models to resolve forward references
RecetaRead.model_rebuild()
ConsultaRead.model_rebuild()
TurnoRead.model_rebuild()
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
    "HorarioProfesionalCreate",
    "HorarioProfesionalUpdate",
    "HorarioProfesionalRead",
    "HorarioDiaInput",
    "ProfesionalRead",
    "ProfesionalCreate",
    "ProfesionalUpdate",
    "DetalleRecetaCreate",
    "DetalleRecetaRead", 
    "DetalleRecetaUpdate",
    "RecetaCreate",
    "RecetaRead",
    "RecetaUpdate",
    "ConsultaCreate",
    "ConsultaRead",
    "ConsultaUpdate",
    "TurnoRead",
    "TurnoCreate",
    "TurnoUpdate",
    "AgendaProfesionalRead",
]