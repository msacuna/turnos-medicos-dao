// src/types/Consulta.ts

import type { RecetaCreate } from './Receta';

export type TipoConsulta =
  | 'Consulta General'
  | 'Control'
  | 'Urgencia'
  | 'Seguimiento';

export interface DetalleReceta {
  id_medicamento: number;
  dosis: string;
  frecuencia: string;
  duracion_dias: number;
  cantidad: number;
  indicaciones?: string;
}

export interface ConsultaCreate {
  diagnostico: string; // obligatorio
  observaciones?: string;
  nombre_motivo_consulta: TipoConsulta;
  receta: RecetaCreate; // obligatorio
}
