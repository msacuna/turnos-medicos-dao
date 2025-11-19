from sqlmodel import SQLModel, Field

class MedicamentoLaboratorioLink(SQLModel, table=True):
    id_medicamento: int = Field(default=None, foreign_key="medicamento.id", primary_key=True)
    id_laboratorio: int = Field(default=None, foreign_key="laboratorio.id", primary_key=True)

class ObraSocialProfesionalLink(SQLModel, table=True):
    id_obra_social: int = Field(default=None, foreign_key="obra_social.id", primary_key=True)
    id_profesional: int = Field(default=None, foreign_key="profesional.id", primary_key=True)
    vigente: bool = Field(default=True)

class PacienteAlergiaLink(SQLModel, table=True):
    dni_paciente: int = Field(default=None, foreign_key="paciente.dni", primary_key=True)
    id_alergia: int = Field(default=None, foreign_key="alergia.id", primary_key=True)


class PacienteAntecedenteLink(SQLModel, table=True):
    dni_paciente: int = Field(default=None, foreign_key="paciente.dni", primary_key=True)
    id_antecedente: int = Field(default=None, foreign_key="antecedente.id", primary_key=True)


class HorarioProfesionalLink(SQLModel, table=True):
    id_horario_atencion: int = Field(default=None, foreign_key="horario_atencion.id", primary_key=True)
    id_profesional: int = Field(default=None, foreign_key="profesional.id", primary_key=True)
    vigente: bool = Field(default=True)