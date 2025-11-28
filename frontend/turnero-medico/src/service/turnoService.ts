// src/service/turnoService.ts

import axios from 'axios';
import type { Turno } from '@/types/Turno';
import type { Profesional } from '@/types/Profesional';

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

  // Obtener turnos por profesional y agenda
  async obtenerTurnosDeAgenda(profesionalId: number, agendaId: number) {
    const res = await axios.get<Turno[]>(
      `${API_BASE}/profesionales/${profesionalId}/agenda/${agendaId}/turnos`
    );
    return res.data;
  },

  async buscarPacientePorDni(dni: string) {
    const res = await axios.get(`${API_BASE}/pacientes/${dni}`);
    return res.data;
  },

  async obtenerEspecialidades() {
    const res = await axios.get(`${API_BASE}/especialidades`);
    return res.data;
  },

  async obtenerProfesionalesPorEspecialidad(idEsp: string) {
  const res = await axios.get<Profesional[]>(`${API_BASE}/profesionales/`);
  // Filtrar por id_especialidad del lado del cliente
  return res.data.filter((prof: Profesional) => prof.id_especialidad === parseInt(idEsp));
},

  async obtenerTurnosAgenda(idProfesional: string, agendaId?: number) {
    try {
      // Si se proporciona un agendaId específico, usarlo
      if (agendaId) {
        const res = await axios.get<Turno[]>(
          `${API_BASE}/profesionales/${idProfesional}/agenda/${agendaId}/turnos`
        );
        return res.data;
      }
      
      // Si no, intentar obtener la agenda del mes actual
      const fechaActual = new Date();
      const mes = fechaActual.getMonth() + 1;
      
      const agendaResponse = await axios.get(
        `${API_BASE}/profesionales/${idProfesional}/agenda/${mes}`
      );
      
      const agenda = agendaResponse.data;
      const turnosResponse = await axios.get<Turno[]>(
        `${API_BASE}/profesionales/${idProfesional}/agenda/${agenda.id}/turnos`
      );
      
      return turnosResponse.data;
      
    } catch (error: unknown) {
      // Lanzar un error específico que el componente pueda identificar
      if (axios.isAxiosError(error) && error.response?.status === 404) {
        throw new Error('AGENDA_NO_DISPONIBLE');
      }
      // Re-lanzar otros errores
      throw error;
    }
  },

  async iniciar(turnoId: number) {
    const res = await axios.patch(`${BASE}/${turnoId}/iniciar`);
    return res.data;
  },

  async finalizar(turnoId: number, consultaData: unknown) {
    const res = await axios.patch(`${BASE}/${turnoId}/finalizar`, consultaData);
    return res.data;
  },

  async cancelar(turnoId: number) {
    // Si querés, podés agregar un endpoint `/cancelar` en backend o usar liberar
    const res = await axios.patch(`${BASE}/${turnoId}/liberar`);
    return res.data;
  },
};

export default turnoService;
