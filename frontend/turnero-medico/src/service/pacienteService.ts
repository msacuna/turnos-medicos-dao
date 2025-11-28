// turnero-medico/src/service/pacienteService.ts

import axios from 'axios';
import {
  type Paciente,
  type PacienteCreate,
  type PacienteUpdate,
} from '../types/Paciente';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const BASE_URL = `${API_BASE}/pacientes`;

export default {
  async listar(): Promise<Paciente[]> {
    const res = await axios.get<Paciente[]>(BASE_URL);
    return res.data;
  },

  async obtener(dni: number): Promise<Paciente> {
    const res = await axios.get<Paciente>(`${BASE_URL}/${dni}`);
    return res.data;
  },

  async crear(data: PacienteCreate): Promise<Paciente> {
    const res = await axios.post<Paciente>(BASE_URL, data);
    return res.data;
  },

  async actualizar(dni: number, data: PacienteUpdate): Promise<Paciente> {
    const res = await axios.put<Paciente>(`${BASE_URL}/${dni}`, data);
    return res.data;
  },

  async eliminar(dni: number): Promise<void> {
    await axios.delete(`${BASE_URL}/${dni}`);
  },
};
