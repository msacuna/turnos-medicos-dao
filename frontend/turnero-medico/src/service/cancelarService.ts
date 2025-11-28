const API_BASE = 'http://localhost:8000/profesionales';

export const cancelarService = {
    cancelarTurnos: async (idAgenda: number, dias: number[]): Promise<{ mensaje: string; contactos_notificados: unknown[] } | null> => {
        try {
            const response = await fetch(`${API_BASE}/agenda/${idAgenda}/cancelar-turnos`, {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(dias),
            });

            if (!response.ok) {
                throw new Error('Error cancelando turnos');
            }

            const data: { mensaje: string; contactos_notificados: unknown[] } = await response.json();
            return data;
        } catch (error) {
            console.error('Error en cancelarTurnos:', error);
            return null;
        }
    },
};