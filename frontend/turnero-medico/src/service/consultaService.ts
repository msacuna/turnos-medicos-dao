import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const BASE = `${API_BASE}/consultas`;

const consultaService = {
  async crear(turnoId: number, data: unknown) {
    const res = await axios.post(`${BASE}/turno/${turnoId}`, data);
    return res.data;
  },
  async listarPorTurno(turnoId: number) {
    const res = await axios.get(`${BASE}/turno/${turnoId}`);
    return res.data;
  },
};

export default consultaService;
