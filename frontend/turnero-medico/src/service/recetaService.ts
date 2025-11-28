import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const BASE = `${API_BASE}/recetas`;

const recetaService = {
  async crear(
    turnoId: number,
    medicamentos: { id: number; cantidad: number }[]
  ) {
    const res = await axios.post(`${BASE}/turno/${turnoId}`, { medicamentos });
    return res.data;
  },
  async listarPorTurno(turnoId: number) {
    const res = await axios.get(`${BASE}/recetas/turno/${turnoId}`);
    return res.data;
  },
};

export default recetaService;
