export interface Turno {
  desde: string; // "08:00"
  hasta: string; // "12:00"
}

export interface DiaAgenda {
  dia: number; // día del mes
  turnos: Turno[];
}

export interface AgendaProfesional {
  id: number;
  idProfesional: number;
  anio: number;
  mes: number; // 1-12
  dias: DiaAgenda[];
}
