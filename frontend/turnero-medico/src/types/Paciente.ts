// turnero-medico/src/types/Paciente.ts

export interface Alergia {
  id: number;
  nombre: string;
}

export interface Antecedente {
  id: number;
  descripcion: string;
}

export interface GrupoSanguineo {
  nombre: string;
}

export interface ObraSocialMini {
  nombre: string;
  porcentaje_cobertura: number;
  nombre_tipo: string;
}

export interface TurnoPaciente {
  id: number;
  fecha: string;
  horario: string;
  consultorio: string;
}

export interface Paciente {
  dni: number;
  nombre: string;
  apellido: string;
  fecha_nacimiento: string;
  email: string;
  telefono: string;

  nombre_grupo_sanguineo: string;
  nombre_obra_social?: string | null;

  grupo_sanguineo: GrupoSanguineo;
  obra_social?: ObraSocialMini | null;

  alergias: Alergia[];
  antecedentes: Antecedente[];
  turnos: TurnoPaciente[];
}

/* ===========================
      CREATE
=========================== */

export interface PacienteCreate {
  dni: number;
  nombre: string;
  apellido: string;
  fecha_nacimiento: string;
  email: string;
  telefono: string;

  nombre_grupo_sanguineo: string;
  nombre_obra_social?: string | null;

  ids_alergias?: number[];
  ids_antecedentes?: number[];
}

/* ===========================
      UPDATE
=========================== */

export interface PacienteUpdate {
  nombre?: string;
  apellido?: string;
  fecha_nacimiento?: string;
  email?: string;
  telefono?: string;

  nombre_grupo_sanguineo?: string | null;
  nombre_obra_social?: string | null;

  ids_alergias?: number[] | null;
  ids_antecedentes?: number[] | null;
}
