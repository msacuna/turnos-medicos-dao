// src/service/obraSocialService.ts

import axios from 'axios';
import {
  type ObraSocial,
  type ObraSocialCreate,
  type ObraSocialUpdate,
} from '../types/ObraSocial';

const API_URL = 'http://localhost:8000/obras-sociales';

const obraSocialService = {
  listar: async (): Promise<ObraSocial[]> => {
    const response = await axios.get(API_URL + '/');
    return response.data;
  },

  obtenerPorId: async (id: number): Promise<ObraSocial> => {
    const response = await axios.get(`${API_URL}/${id}`);
    return response.data;
  },

  crear: async (data: ObraSocialCreate): Promise<ObraSocial> => {
    const response = await axios.post(API_URL + '/', data);
    return response.data;
  },

  actualizar: async (
    id: number,
    data: ObraSocialUpdate
  ): Promise<ObraSocial> => {
    const response = await axios.put(`${API_URL}/${id}`, data);
    return response.data;
  },

  eliminar: async (id: number): Promise<void> => {
    await axios.delete(`${API_URL}/${id}`);
  },
};

export default obraSocialService;
