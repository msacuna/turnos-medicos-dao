// src/service/turnoService.ts

import axios from 'axios';
import type { Turno } from '@/types/Turno';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const BASE = `${API_BASE}/turnos`;

const turnoService = {
  // Obtener todos los turnos (ajustá si tu backend tiene otro endpoint)
  async listar(): Promise<Turno[]> {
    const res = await axios.get<Turno[]>(BASE);
    return res.data;
  },

  async obtenerPorId(id: number): Promise<Turno> {
    const res = await axios.get<Turno>(`${BASE}/${id}`);
    return res.data;
  },

  // otros helpers si necesitás (agendar, liberar, etc)
  async agendar(turnoId: number, dniPaciente: number) {
    const res = await axios.patch(`${BASE}/${turnoId}/agendar/${dniPaciente}`);
    return res.data;
  },

  async liberar(turnoId: number) {
    const res = await axios.patch(`${BASE}/${turnoId}/liberar`);
    return res.data;
  },

  // ...y los demás endpoints de tu router (iniciar, finalizar, cancelar)
};

export default turnoService;
