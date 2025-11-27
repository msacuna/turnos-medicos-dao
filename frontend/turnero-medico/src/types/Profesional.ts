export interface ProfesionalBase {
  nombre: string;
  apellido: string;
  matricula: string;
  email: string;
  telefono: string;
  id_especialidad: number;
}

export interface Profesional extends ProfesionalBase {
  id: number;
}

export type ProfesionalCreate = ProfesionalBase;

export type ProfesionalUpdate = ProfesionalBase & { id: number };
