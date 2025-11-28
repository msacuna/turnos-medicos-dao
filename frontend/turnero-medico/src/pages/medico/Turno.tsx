// src/pages/medico/Turno.tsx

import React, { useEffect, useState } from 'react';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';
import styles from '@/styles/pages/turno.module.css';

import type { Turno } from '@/types/Turno';
import turnoService from '@/service/turnoService';
import FinalizarConsultaModal from '@/components/consultas/FinalizarConsultaModal';

import { format } from 'date-fns';

export default function TurnoPage() {
  const [turnos, setTurnos] = useState<Turno[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedDate, setSelectedDate] = useState<Date>(new Date());
  const [selectedDayTurnos, setSelectedDayTurnos] = useState<Turno[]>([]);
  const [selectedTurno, setSelectedTurno] = useState<Turno | null>(null);
  const [modalFinalizarVisible, setModalFinalizarVisible] = useState(false);

  useEffect(() => {
    const load = async () => {
      try {
        setLoading(true);
        const data = await turnoService.listar();
        setTurnos(data);
      } catch (err) {
        console.error('Error cargando turnos:', err);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  useEffect(() => {
    const yyyy = selectedDate.getFullYear();
    const mm = String(selectedDate.getMonth() + 1).padStart(2, '0');
    const dd = String(selectedDate.getDate()).padStart(2, '0');
    const dateStr = `${yyyy}-${mm}-${dd}`;

    const filtered = turnos
      .filter((t) => t.fecha === dateStr)
      .sort((a, b) => (a.hora_inicio > b.hora_inicio ? 1 : -1));

    setSelectedDayTurnos(filtered);
    setSelectedTurno(null);
  }, [selectedDate, turnos]);

  const handleDayClick = (value: unknown) => {
    if (value instanceof Date) {
      setSelectedDate(value);
      return;
    }
    if (Array.isArray(value) && value[0] instanceof Date) {
      setSelectedDate(value[0]);
    }
  };

  const cambiarEstadoTurno = async (
    nuevoEstado:
      | 'Disponible'
      | 'Agendado'
      | 'Finalizado'
      | 'Cancelado'
      | 'En Proceso'
  ) => {
    if (!selectedTurno) return;

    try {
      switch (nuevoEstado) {
        case 'Agendado': {
          const dni = Number(prompt('DNI del paciente:'));
          if (!dni) return;
          await turnoService.agendar(selectedTurno.id, dni);
          break;
        }
        case 'Disponible':
          await turnoService.liberar(selectedTurno.id);
          break;
        case 'Cancelado':
          await turnoService.cancelar(selectedTurno.id);
          break;
        case 'En Proceso':
          await turnoService.iniciar(selectedTurno.id);
          break;
      }

      const refreshed = await turnoService.listar();
      setTurnos(refreshed);
      setSelectedTurno(null);
    } catch (err) {
      console.error(err);
      alert('Error cambiando estado del turno');
    }
  };

  const fmtTime = (timeStr: string) => {
    if (!timeStr) return '';
    const [h, m] = timeStr.split(':');
    return `${h}:${m}`;
  };

  return (
    <div className={styles.container}>
      <div className={styles.calendarColumn}>
        <h2>Calendario</h2>
        <Calendar
          onChange={handleDayClick}
          value={selectedDate}
          selectRange={false}
          calendarType="iso8601"
          tileContent={({ date, view }) => {
            if (view === 'month') {
              const yyyy = date.getFullYear();
              const mm = String(date.getMonth() + 1).padStart(2, '0');
              const dd = String(date.getDate()).padStart(2, '0');
              const dateStr = `${yyyy}-${mm}-${dd}`;
              const count = turnos.filter((t) => t.fecha === dateStr).length;
              if (count > 0)
                return <div className={styles.dotCount}>{count}</div>;
            }
            return null;
          }}
        />
        {loading && <p>Cargando turnos...</p>}
      </div>

      <div className={styles.sidePanel}>
        <h3>{format(selectedDate, 'EEEE, dd MMMM yyyy')}</h3>

        <div className={styles.slotList}>
          {selectedDayTurnos.length === 0 ? (
            <p>No hay turnos para este día</p>
          ) : (
            selectedDayTurnos.map((t) => (
              <div
                key={t.id}
                className={`${styles.slot} ${
                  t.nombre_estado === 'Disponible'
                    ? styles.available
                    : styles.booked
                } ${selectedTurno?.id === t.id ? styles.selected : ''}`}
                onClick={() => setSelectedTurno(t)}
              >
                <div className={styles.slotTime}>
                  {fmtTime(t.hora_inicio)} - {fmtTime(t.hora_fin_estimada)}
                </div>
                <div className={styles.slotInfo}>
                  <div className={styles.especialidad}>
                    {t.especialidad?.nombre ??
                      `Especialidad ${t.id_especialidad}`}
                  </div>
                  <div className={styles.estado}>{t.nombre_estado}</div>
                </div>
              </div>
            ))
          )}
        </div>

        {selectedTurno && (
          <div className={styles.detailBox}>
            <h4>Turno {selectedTurno.id}</h4>
            <p>
              <strong>Hora:</strong> {fmtTime(selectedTurno.hora_inicio)} -{' '}
              {fmtTime(selectedTurno.hora_fin_estimada)}
            </p>
            <p>
              <strong>Estado:</strong> {selectedTurno.nombre_estado}
            </p>
            <p>
              <strong>Especialidad:</strong>{' '}
              {selectedTurno.especialidad?.nombre ??
                selectedTurno.id_especialidad}
            </p>
            <p>
              <strong>Monto:</strong> $
              {selectedTurno.monto?.toFixed(2) ?? '0.00'}
            </p>

            {/* ✅ Aquí va un solo div con todos los botones dinámicos */}
            <div className={styles.detailActions}>
              {selectedTurno.nombre_estado === 'Disponible' && (
                <button onClick={() => cambiarEstadoTurno('Agendado')}>
                  Agendar
                </button>
              )}
              {selectedTurno.nombre_estado === 'Agendado' && (
                <>
                  <button onClick={() => cambiarEstadoTurno('Disponible')}>
                    Liberar
                  </button>
                  <button onClick={() => cambiarEstadoTurno('Cancelado')}>
                    Cancelar
                  </button>
                  <button onClick={() => cambiarEstadoTurno('En Proceso')}>
                    Iniciar
                  </button>
                </>
              )}
              {selectedTurno.nombre_estado === 'En Proceso' && (
                <button onClick={() => setModalFinalizarVisible(true)}>
                  Finalizar
                </button>
              )}
            </div>
          </div>
        )}
      </div>
      {/* ✅ Modal condicional */}
      {modalFinalizarVisible && selectedTurno && (
        <FinalizarConsultaModal
          turno={selectedTurno}
          onClose={() => setModalFinalizarVisible(false)}
          onFinalizado={async (consultaData) => {
            if (!selectedTurno) return;
            try {
              await turnoService.finalizar(selectedTurno.id, consultaData); // PASAR consultaData
              const refreshed = await turnoService.listar();
              setTurnos(refreshed);
              setSelectedTurno(null);
              setModalFinalizarVisible(false);
            } catch (err) {
              console.error(err);
              alert('Error finalizando turno');
            }
          }}
        />
      )}
    </div>
  );
}
