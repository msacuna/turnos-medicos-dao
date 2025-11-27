import { useState, useEffect } from 'react';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';
import styles from '../../styles/pages/agenda.module.css';
import { agendaService } from '../../service/agendaService';
import type { DiaAgenda } from '../../types/Agenda';

interface AgendaProps {
  idProfesional: number;
}

export default function Agenda({ idProfesional }: AgendaProps) {
  const [fechaSeleccionada, setFechaSeleccionada] = useState<Date | null>(null);
  const [horarioDesde, setHorarioDesde] = useState('08:00');
  const [horarioHasta, setHorarioHasta] = useState('17:00');
  const [dias, setDias] = useState<DiaAgenda[]>([]);

  const [anio, setAnio] = useState<number>(new Date().getFullYear());
  const [mes, setMes] = useState<number>(new Date().getMonth() + 2); // mes siguiente

  useEffect(() => {
    if (mes > 12) {
      setMes(1);
      setAnio(anio + 1);
    }
    agendaService.obtenerAgenda(idProfesional, anio, mes).then((agenda) => {
      if (agenda) setDias(agenda.dias);
    });
  }, [idProfesional, anio, mes]);

  const handleClickDay = (
    value: Date | Date[] | null,
    _event?: React.MouseEvent<HTMLButtonElement>
  ) => {
    if (!value) return;
    if (Array.isArray(value)) return; // ignorar rangos

    const date: Date = value; // ya es Date
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
    if (!fechaSeleccionada) return;
    const diaNum = fechaSeleccionada.getDate();
    const nuevoDia: DiaAgenda = {
      dia: diaNum,
      turnos: [{ desde: horarioDesde, hasta: horarioHasta }],
    };

    agendaService.guardarDia(idProfesional, anio, mes, nuevoDia).then(() => {
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

  // Filtra las horas de "Hasta" para que sean posteriores a "Desde"
  const horasHasta = horas.filter((h) => h > horarioDesde);

  const diaActual = fechaSeleccionada?.getDate() || 0;
  const diaAgenda = dias.find((d) => d.dia === diaActual);

  return (
    <div className={styles.container}>
      <h1>Agenda del médico</h1>
      <Calendar
        onClickDay={handleClickDay}
        value={fechaSeleccionada}
        activeStartDate={new Date(anio, mes - 1, 1)}
        tileDisabled={({ date, view }) =>
          view === 'month' && date.getMonth() !== mes - 1
        }
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
