import { useState, useEffect } from 'react';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';
import '../../styles/global.css';

import styles from '../../styles/pages/agenda.module.css';
import { agendaService } from '../../service/agendaService';
import type { DiaAgenda } from '../../types/Agenda';

import { useAuth } from '../../hooks/useAuth';

export default function Agenda() {
  const { user } = useAuth();
  const idProfesional = user?.id;

  const [fechaSeleccionada, setFechaSeleccionada] = useState<Date | null>(null);
  const [horarioDesde, setHorarioDesde] = useState('08:00');
  const [horarioHasta, setHorarioHasta] = useState('17:00');
  const [dias, setDias] = useState<DiaAgenda[]>([]);

  const mesActual = new Date().getMonth() + 1;
  const [mes, setMes] = useState<number>(mesActual);

  useEffect(() => {
    if (!idProfesional) return; // El user aún no está cargado

    agendaService.obtenerAgenda(idProfesional, mes).then((agenda) => {
      if (agenda) setDias(agenda.dias);
      else setDias([]);
    });
  }, [idProfesional, mes]); // ← AGREGADO idProfesional

  const handleClickDay = (value: Date | Date[] | null) => {
    if (!value || Array.isArray(value)) return;

    const date = value;
    setFechaSeleccionada(date);

    const diaNum = date.getDate();
    const diaAgenda = dias.find((d) => d.dia === diaNum);
    if (diaAgenda && diaAgenda.turnos.length > 0) {
      setHorarioDesde(diaAgenda.turnos[0].desde);
      setHorarioHasta(diaAgenda.turnos[0].hasta);
    } else {
      setHorarioDesde('08:00');
      setHorarioHasta('17:00');
    }
  };

  const handleGuardar = () => {
    if (!fechaSeleccionada || !idProfesional) return;

    agendaService
      .guardarDia(idProfesional, fechaSeleccionada, horarioDesde, horarioHasta)
      .then(() => {
        const diaNum = fechaSeleccionada.getDate();
        const nuevoDia: DiaAgenda = {
          dia: diaNum,
          turnos: [{ desde: horarioDesde, hasta: horarioHasta }],
        };

        const otrasDias = dias.filter((d) => d.dia !== diaNum);
        setDias([...otrasDias, nuevoDia]);
        alert('Horario guardado!');
      });
  };

  const handleCancelar = () => {
    setFechaSeleccionada(null);
    setHorarioDesde('08:00');
    setHorarioHasta('17:00');
  };

  const horas = Array.from(
    { length: 24 },
    (_, i) => `${i.toString().padStart(2, '0')}:00`
  );

  const horasHasta = horas.filter((h) => h > horarioDesde);

  const diaActual = fechaSeleccionada?.getDate() || 0;
  const diaAgenda = dias.find((d) => d.dia === diaActual);

  if (!idProfesional) return <p>Cargando datos del profesional...</p>;

  return (
    <div className={styles.container}>
      <h1>Agenda del médico</h1>

      <Calendar
        key={`${mes}`}
        onClickDay={handleClickDay}
        value={fechaSeleccionada}
        defaultActiveStartDate={new Date(new Date().getFullYear(), mes - 1, 1)}
      />

      {fechaSeleccionada && (
        <div className={styles.detalles}>
          <h2>Definir horarios disponibles:</h2>

          {diaAgenda && diaAgenda.turnos.length > 0 && (
            <div className={styles.turnosGuardados}>
              <h3>Turnos ya guardados:</h3>
              <ul>
                {diaAgenda.turnos.map((t, idx) => (
                  <li key={idx}>
                    {t.desde} - {t.hasta}
                  </li>
                ))}
              </ul>
            </div>
          )}

          <div className={styles.selects}>
            <label>
              Desde:
              <select
                value={horarioDesde}
                onChange={(e) => setHorarioDesde(e.target.value)}
              >
                {horas.map((h) => (
                  <option key={h} value={h}>
                    {h}
                  </option>
                ))}
              </select>
            </label>

            <label>
              Hasta:
              <select
                value={horarioHasta}
                onChange={(e) => setHorarioHasta(e.target.value)}
              >
                {horasHasta.map((h) => (
                  <option key={h} value={h}>
                    {h}
                  </option>
                ))}
              </select>
            </label>
          </div>

          <div className={styles.botones}>
            <button onClick={handleCancelar}>Cancelar</button>
            <button onClick={handleGuardar}>Guardar cambios</button>
          </div>
        </div>
      )}
    </div>
  );
}
