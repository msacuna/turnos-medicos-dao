import axios from 'axios';
import {
  type Profesional,
  type ProfesionalCreate,
  type ProfesionalUpdate,
} from '@/types/Profesional';

const API_BASE = 'http://localhost:8000';

// Obtener todos los profesionales
export const obtenerProfesionales = async (): Promise<Profesional[]> => {
  const response = await axios.get(`${API_BASE}/profesionales/`);
  return response.data;
};

// Obtener profesional por ID
export const obtenerProfesionalPorId = async (
  id: number
): Promise<Profesional> => {
  const response = await axios.get(`${API_BASE}/profesionales/${id}`);
  return response.data;
};

// Crear profesional
export const crearProfesional = async (
  data: ProfesionalCreate
): Promise<Profesional> => {
  const response = await axios.post(`${API_BASE}/profesionales/crear`, data);
  return response.data;
};

// Actualizar profesional
export const actualizarProfesional = async (
  data: ProfesionalUpdate
): Promise<Profesional> => {
  const response = await axios.put(
    `${API_BASE}/profesionales/${data.id}`,
    data
  );
  return response.data;
};

// Eliminar profesional
export const eliminarProfesional = async (id: number): Promise<void> => {
  await axios.delete(`${API_BASE}/profesionales/${id}`);
};
