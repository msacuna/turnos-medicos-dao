import type { AgendaProfesional, DiaAgenda, Turno } from '../types/Agenda';

const API_BASE = 'http://localhost:8000/profesionales';

export const agendaService = {
    // Obtener agenda de un profesional para un mes específico
    obtenerAgenda: async (
        idProfesional: number,
        anio: number,
        mes: number
    ): Promise<AgendaProfesional | null> => {
        try {
            const response = await fetch(
                `${API_BASE}/${idProfesional}/agenda/${mes}`
            );
            if (!response.ok) return null;
            const data: AgendaProfesional = await response.json();
            return data;
        } catch (error) {
            console.error('Error obteniendo agenda:', error);
            return null;
        }
    },

    // Guardar/actualizar un día de la agenda
    guardarDia: async (
        idProfesional: number,
        anio: number,
        mes: number, // lo podés ignorar si no lo usa el backend
        diaAgenda: DiaAgenda
    ): Promise<DiaAgenda | null> => {
        try {
            const dia = diaAgenda.dia; // número del día
            const turno = diaAgenda.turnos[0]; // asumimos un solo rango
            const response = await fetch(
                `${API_BASE}/${idProfesional}/horarios/${dia}`,
                {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        hora_inicio: turno.desde,
                        hora_fin: turno.hasta,
                        trabaja: true, // siempre true si definimos horario
                    }),
                }
            );
            if (!response.ok) return null;
            const data: DiaAgenda = await response.json();
            return data;
        } catch (error) {
            console.error('Error guardando dia:', error);
            return null;
        }
    },

    // Obtener todos los turnos de una agenda
    obtenerTurnos: async (idAgenda: number): Promise<Turno[]> => {
        try {
            const response = await fetch(
                `${API_BASE}/{profesional_id}/agenda/${idAgenda}/turnos`
            );
            if (!response.ok) return [];
            const data: Turno[] = await response.json();
            return data;
        } catch (error) {
            console.error('Error obteniendo turnos:', error);
            return [];
        }
    },

    // Obtener la lista de profesionales
    obtenerProfesionales: async (): Promise<{ id: string; nombre: string }[]> => {
        try {
            const response = await fetch(`${API_BASE}/`);
            if (!response.ok) return [];
            const data: { id: string; nombre: string }[] = await response.json();
            return data;
        } catch (error) {
            console.error('Error obteniendo profesionales:', error);
            return [];
        }
    },

    // Cancelar turnos para días seleccionados
    cancelarTurnos: async (
        idProfesional: string,
        dias: Date[]
    ): Promise<void> => {
        try {
            const response = await fetch(
                `${API_BASE}/${idProfesional}/cancelar-turnos`,
                {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        dias: dias.map((dia) => dia.toISOString().split('T')[0]),
                    }),
                }
            );
            if (!response.ok) {
                throw new Error('Error cancelando turnos');
            }
        } catch (error) {
            console.error('Error cancelando turnos:', error);
        }
    },
};
