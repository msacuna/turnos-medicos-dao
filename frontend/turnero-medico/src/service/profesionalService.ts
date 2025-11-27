// src/service/profesionalService.ts

import api from 'axios';
import {
  type Profesional,
  type ProfesionalCreate,
  type ProfesionalUpdate,
} from '@/types/Profesional';

// Obtener todos los profesionales
export const obtenerProfesionales = async (): Promise<Profesional[]> => {
  const response = await api.get('/profesionales/');
  return response.data;
};

// Obtener profesional por ID
export const obtenerProfesionalPorId = async (
  id: number
): Promise<Profesional> => {
  const response = await api.get(`/profesionales/${id}`);
  return response.data;
};

// Crear profesional
export const crearProfesional = async (
  data: ProfesionalCreate
): Promise<Profesional> => {
  const response = await api.post('/profesionales/crear', data);
  return response.data;
};

// PREPARADO: actualizar cuando tengas endpoint en backend
export const actualizarProfesional = async (
  data: ProfesionalUpdate
): Promise<Profesional> => {
  const response = await api.put(`/profesionales/${data.id}`, data);
  return response.data;
};

// PREPARADO: eliminar cuando agregues endpoint
export const eliminarProfesional = async (id: number): Promise<void> => {
  await api.delete(`/profesionales/${id}`);
};
