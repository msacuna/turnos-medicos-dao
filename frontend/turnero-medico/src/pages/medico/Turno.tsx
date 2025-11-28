// src/pages/medico/Turno.tsx

import React, { useEffect, useState } from 'react';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css'; // estilos por defecto (puedes sobrescribir)
import styles from '@/styles/pages/turno.module.css';

import type { Turno } from '@/types/Turno';
import turnoService from '@/service/turnoService';

import { format } from 'date-fns';

import Navbar from '@/components/ui/Navbar';
import MedicoMenu from '@/components/menu/MedicoMenu';
import pageStyles from '@/styles/pages/principal.module.css';


export default function TurnoPage() {
    const [turnos, setTurnos] = useState<Turno[]>([]);
    const [loading, setLoading] = useState(false);
    const [selectedDate, setSelectedDate] = useState<Date>(new Date());
    const [selectedDayTurnos, setSelectedDayTurnos] = useState<Turno[]>([]);
    const [selectedTurno, setSelectedTurno] = useState<Turno | null>(null);

    const [menuOpen, setMenuOpen] = useState(false);
    const openMenu = () => setMenuOpen(true);
    const closeMenu = () => setMenuOpen(false);

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

    // cuando cambie la fecha seleccionada, actualizar lista lateral
    useEffect(() => {
        const sel = selectedDate;
        const yyyy = sel.getFullYear();
        const mm = String(sel.getMonth() + 1).padStart(2, '0');
        const dd = String(sel.getDate()).padStart(2, '0');
        const dateStr = `${yyyy}-${mm}-${dd}`; // formato yyyy-mm-dd

        const filtered = turnos
            .filter((t) => t.fecha === dateStr)
            .sort((a, b) => (a.hora_inicio > b.hora_inicio ? 1 : -1));

        setSelectedDayTurnos(filtered);
        setSelectedTurno(null);
    }, [selectedDate, turnos]);

    // no dependemos del type exportado de la lib: aceptamos value como unknown
    const handleDayClick = (value: unknown) => {
        // si la librería pasa un array (range) o null no rompes nada
        if (value instanceof Date) {
            setSelectedDate(value);
            return;
        }

        // si usás selectRange en algún momento:
        if (Array.isArray(value) && value[0] instanceof Date) {
            setSelectedDate(value[0]);
            return;
        }

        // si value es null o distinto, no hacemos nada
    };

    const fmtTime = (timeStr: string) => {
        // timeStr expected "HH:MM:SS"
        if (!timeStr) return '';
        const [h, m] = timeStr.split(':');
        return `${h}:${m}`;
    };

    return (
        <div>
            <Navbar title="Agenda de turnos" onMenuClick={openMenu} />
            {menuOpen && (
                <div className={pageStyles.overlay} onClick={closeMenu}></div>
            )}

            <MedicoMenu isOpen={menuOpen} onClose={closeMenu} />


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

                                if (count > 0) {
                                    return <div className={styles.dotCount}>{count}</div>;
                                }
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
                                    className={`${styles.slot} ${t.nombre_estado === 'Disponible'
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

                            <div className={styles.detailActions}>
                                {/* Aquí podés poner botones para agendar/liberar/iniciar según estado */}
                                {selectedTurno.nombre_estado === 'Disponible' && (
                                    <button
                                        onClick={async () => {
                                            const dni = Number(prompt('DNI del paciente:'));
                                            if (!dni) return;
                                            try {
                                                await turnoService.agendar(selectedTurno.id, dni);
                                                const refreshed = await turnoService.listar();
                                                setTurnos(refreshed);
                                            } catch (err) {
                                                console.error(err);
                                                alert('Error agendando turno');
                                            }
                                        }}
                                    >
                                        Agendar
                                    </button>
                                )}
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
