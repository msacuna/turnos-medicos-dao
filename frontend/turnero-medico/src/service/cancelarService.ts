import axios from 'axios';

const API_BASE = 'http://localhost:8000/profesionales';

interface Profesional {
  id: number;
  nombre: string;
  apellido: string;
  email: string;
  matricula: string;
  telefono: string;
  id_especialidad: number;
}

interface Agenda {
  id: number;
  id_profesional: number;
  mes: number;
  anio: number;
}

interface Turno {
  id: number;
  fecha: string;
  hora_inicio: string;
  hora_fin_estimada: string;
  dni_paciente: number;
  nombre_estado: string;
  id_especialidad: number;
  id_agenda_profesional: number;
  monto: number;
}

interface CancelarTurnosResponse {
  mensaje: string;
  contactos_notificados: unknown[];
}

export const cancelarService = {
  // Obtener todos los profesionales
  obtenerProfesionales: async (): Promise<Profesional[]> => {
    const response = await axios.get(`${API_BASE}`);
    return response.data;
  },

  // Obtener agenda de un profesional por mes
  obtenerAgenda: async (idProfesional: number, mes: number): Promise<Agenda> => {
    const response = await axios.get(`${API_BASE}/${idProfesional}/agenda/${mes}`);
    return response.data;
  },

  // Obtener turnos de una agenda
  obtenerTurnos: async (idProfesional: number, idAgenda: number): Promise<Turno[]> => {
    try {
      console.log('Obteniendo turnos:', { idProfesional, idAgenda });
      console.log('URL:', `${API_BASE}/${idProfesional}/agenda/${idAgenda}/turnos`);
      const response = await axios.get(`${API_BASE}/${idProfesional}/agenda/${idAgenda}/turnos`);
      console.log('Turnos obtenidos:', response.data);
      return response.data;
    } catch (error: any) {
      console.error('Error detallado:', {
        status: error.response?.status,
        data: error.response?.data,
        message: error.message
      });
      throw error;
    }
  },

  // Cancelar turnos
  cancelarTurnos: async (idAgenda: number, dias: number[]): Promise<CancelarTurnosResponse> => {
    const response = await axios.patch(`${API_BASE}/agenda/${idAgenda}/cancelar-turnos`, dias);
    return response.data;
  },
};