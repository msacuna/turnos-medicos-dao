export interface TurnoPorEspecialidad {
  especialidad: string;
  cantidad: number;
  id_especialidad?: number;
}

export interface PacientePorObraSocial {
  obra_social: string;
  cantidad: number;
  id_obra_social?: number;
}

export interface MontoPorEspecialidad {
  especialidad: string;
  monto_total: number;
  cantidad_turnos?: number;
  id_especialidad?: number;
}

export interface TurnoPorPeriodo {
  periodo: string;
  cantidad: number;
  mes?: number;
  anio?: number;
}

export interface ProfesionalPorEspecialidad {
  especialidad: string;
  cantidad_profesionales: number;
  profesionales?: string[];
  id_especialidad?: number;
}

export interface ReporteData {
  turnosPorEspecialidad: TurnoPorEspecialidad[];
  pacientesPorObraSocial: PacientePorObraSocial[];
  montosPorEspecialidad: MontoPorEspecialidad[];
  turnosPorPeriodo: TurnoPorPeriodo[];
  profesionalesPorEspecialidad: ProfesionalPorEspecialidad[];
}