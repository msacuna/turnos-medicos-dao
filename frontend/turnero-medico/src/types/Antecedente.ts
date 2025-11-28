// src/types/Antecedente.ts

export interface Antecedente {
  id: number;
  nombre: string;
}

export interface AntecedenteCreate {
  nombre: string;
}

export interface AntecedenteUpdate {
  nombre?: string; // opcional porque en el backend usa exclude_unset
}

export type AntecedentePayload = {
  id?: number; // opcional porque solo existe en edición
  nombre: string;
};
