// src/types/Medicamento.ts

export interface Laboratorio {
  id: number;
  nombre: string;
}

export interface Medicamento {
  id: number;
  nombre: string;
  descripcion?: string;
  laboratorios: Laboratorio[]; // Siempre llega como lista (puede ser vacía)
}

export interface MedicamentoCreate {
  nombre: string;
  descripcion?: string;
  ids_laboratorios: number[]; // el backend espera SIEMPRE lista, incluso vacía
}

export interface MedicamentoUpdate {
  nombre?: string;
  descripcion?: string;
  ids_laboratorios?: number[];
}

export interface MedicamentoPayload {
  id?: number;
  nombre: string;
  descripcion?: string;
  ids_laboratorios?: number[];
}
