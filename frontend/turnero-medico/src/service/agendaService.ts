import type { AgendaProfesional, DiaAgenda, Turno } from '../types/Agenda';

const API_BASE = 'http://localhost:8000/profesionales';

// Normaliza día de semana para FastAPI
const mapDiaSemana = (d: Date): string => {
    const dia = d.toLocaleDateString('es-ES', { weekday: 'long' });
    return dia
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '') // quitar tildes (miércoles → miercoles)
        .toLowerCase(); // lunes, martes, miercoles...
};

export const agendaService = {
    // Obtener o crear agenda del mes
    obtenerAgenda: async (
        idProfesional: number,
        mes: number
    ): Promise<AgendaProfesional | null> => {
        try {
            const url = `${API_BASE}/${idProfesional}/agenda/${mes}`;

            const response = await fetch(url, {
                method: 'GET',
                mode: 'cors',
                headers: { 'Content-Type': 'application/json' },
            });

            // Si la agenda NO existe → creamos una nueva
            if (response.status === 404) {
                const createRes = await fetch(url, {
                    method: 'POST',
                    mode: 'cors',
                    headers: { 'Content-Type': 'application/json' },
                });
                if (!createRes.ok) return null;
                return await createRes.json();
            }

            if (!response.ok) return null;

            return await response.json();
        } catch (e) {
            console.error('Error obteniendo agenda:', e);
            return null;
        }
    },

    // Guardar horario de un DÍA SEMANAL
    guardarDia: async (
        idProfesional: number,
        fecha: Date,
        desde: string,
        hasta: string
    ) => {
        try {
            const diaSemana = mapDiaSemana(fecha);

            const response = await fetch(
                `${API_BASE}/${idProfesional}/horarios/${diaSemana}`,
                {
                    method: 'PUT',
                    mode: 'cors',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        hora_inicio: desde,
                        hora_fin: hasta,
                        trabaja: true,
                    }),
                }
            );

            if (!response.ok) return null;

            return await response.json();
        } catch (e) {
            console.error('Error guardando horario:', e);
            return null;
        }
    },

    obtenerTurnos: async (
        idProfesional: number,
        idAgenda: number
    ): Promise<Turno[]> => {
        try {
            const response = await fetch(
                `${API_BASE}/${idProfesional}/agenda/${idAgenda}/turnos`,
                {
                    method: 'GET',
                    mode: 'cors',
                    headers: { 'Content-Type': 'application/json' },
                }
            );

            if (!response.ok) return [];

            return await response.json();
        } catch (e) {
            console.error('Error obteniendo turnos:', e);
            return [];
        }
    },
};
