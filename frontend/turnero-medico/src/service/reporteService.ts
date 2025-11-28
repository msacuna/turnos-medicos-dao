const API_BASE = 'http://localhost:8000/reportes';

export const reporteService = {
  turnosPorEspecialidad: async () => {
    return await fetch(`${API_BASE}/turnos-por-especialidad`);
  },

  pacientesPorObraSocial: async () => {
    return await fetch(`${API_BASE}/pacientes-por-obra-social`);
  },

  montosPorEspecialidad: async () => {
    return await fetch(`${API_BASE}/montos-por-especialidad`);
  },

  turnosPorPeriodo: async (anio?: number, mesInicio = 1, mesFin = 12) => {
    const params = new URLSearchParams({
      mes_inicio: mesInicio.toString(),
      mes_fin: mesFin.toString(),
    });

    if (anio) params.append('anio', anio.toString());

    return await fetch(`${API_BASE}/turnos-por-periodo?${params.toString()}`);
  },

  profesionalesPorEspecialidad: async () => {
    return await fetch(`${API_BASE}/profesionales-por-especialidad`);
  },
};
