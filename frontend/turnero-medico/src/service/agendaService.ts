import axios from 'axios';

const API_URL = 'http://localhost:8000/profesionales';

const DIAS_MAP: Record<string, string> = {
    LUNES: 'Lunes',
    MARTES: 'Martes',
    MIERCOLES: 'Miercoles',
    JUEVES: 'Jueves',
    VIERNES: 'Viernes',
    SABADO: 'Sabado',
};

export const getHorariosProfesional = async (profesionalId: number) => {
    const response = await axios.get(`${API_URL}/${profesionalId}/horarios`);
    return response.data;
};

export const updateHorarioProfesional = async (
    profesionalId: number,
    diaFront: string, // "LUNES"
    datos: {
        trabaja: boolean;
        hora_inicio: string | null;
        hora_fin: string | null;
    }
) => {
    const diaBack = DIAS_MAP[diaFront]; // ← SE TRANSFORMA A "Lunes"

    const response = await axios.put(
        `${API_URL}/${profesionalId}/horarios/${diaBack}`,
        datos
    );

    return response.data;
};
