// src/types/Turno.ts

export type EstadosTurno =
  | 'Agendado'
  | 'Cancelado'
  | 'Finalizado'
  | 'Ausente'
  | 'Disponible'
  | 'En Proceso';

export interface Turno {
  id: number;
  fecha: string; // "YYYY-MM-DD"
  hora_inicio: string; // "HH:MM:SS"
  hora_fin_estimada: string; // "HH:MM:SS"
  dni_paciente?: number | null;
  nombre_estado: EstadosTurno;
  id_especialidad: number;
  id_agenda_profesional: number;
  monto: number;
  especialidad?: {
    id: number;
    nombre: string;
  } | null;
  // consultas opcional
  consultas?: Array<unknown>;
}
