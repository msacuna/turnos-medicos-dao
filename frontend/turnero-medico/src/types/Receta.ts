// src/types/Receta.ts

export interface DetalleReceta {
  id_medicamento: number; // ID del medicamento
  dosis: string; // ejemplo: "500mg"
  frecuencia: string; // ejemplo: "Cada 8 horas"
  duracion_dias: number; // cantidad de días
  cantidad: number; // cantidad total de unidades
  indicaciones?: string; // opcional, instrucciones adicionales
}

export interface RecetaCreate {
  fecha: string; // ISO date string, ejemplo: "2024-07-10"
  detalles_receta: DetalleReceta[];
}
