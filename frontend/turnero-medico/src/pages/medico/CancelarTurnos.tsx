import { useState, useEffect } from 'react';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';
import '../../styles/global.css';

import styles from '../../styles/pages/agenda.module.css';
import { agendaService } from '../../service/agendaService';
import Navbar from '@/components/ui/Navbar';
import MedicoMenu from '@/components/menu/MedicoMenu';
import pageStyles from '@/styles/pages/principal.module.css';
import { useAuth } from '../../hooks/useAuth';

// Define types
interface Profesional {
    id: number;
    nombre: string;
    apellido: string;
}

interface Turno {
    fecha: string;
    nombre_estado: string;
}

interface CancelarTurnosResponse {
    mensaje: string;
    contactos_notificados: unknown[];
}

export default function CancelarTurnos() {
    const { user } = useAuth();
    const [profesionales, setProfesionales] = useState<Profesional[]>([]);
    const [idProfesional, setIdProfesional] = useState<number | null>(null);
    const [agendaId, setAgendaId] = useState<number | null>(null);
    const [diasSeleccionados, setDiasSeleccionados] = useState<number[]>([]);
    const [turnosPorDia, setTurnosPorDia] = useState<Record<number, number>>({});
    const [menuOpen, setMenuOpen] = useState(false);

    const openMenu = () => setMenuOpen(true);
    const closeMenu = () => setMenuOpen(false);

    useEffect(() => {
        // Obtener la lista de profesionales
        agendaService.obtenerProfesionales().then((data) => {
            const formattedProfesionales = data.map((profesional) => ({
                id: profesional.id,
                nombre: profesional.nombre,
                apellido: profesional.apellido,
            }));
            setProfesionales(formattedProfesionales);
            if (formattedProfesionales.length > 0) setIdProfesional(formattedProfesionales[0].id);
        });
    }, []);

    useEffect(() => {
        if (!idProfesional) return;
        const mesActual = new Date().getMonth() + 1; // Mes actual
        agendaService.obtenerAgenda(idProfesional, new Date().getFullYear(), mesActual).then((agenda) => {
            if (agenda) setAgendaId(agenda.id);
        });
    }, [idProfesional]);

    useEffect(() => {
        if (!agendaId || !idProfesional) return;
        agendaService.obtenerTurnos(agendaId).then((turnos) => {
            const turnosPorDia = turnos.reduce((acc: Record<number, number>, turno: Turno) => {
                const dia = new Date(turno.fecha).getDate();
                acc[dia] = (acc[dia] || 0) + 1;
                return acc;
            }, {});
            setTurnosPorDia(turnosPorDia);
        });
    }, [agendaId, idProfesional]);

    const handleClickDay = (value: Date | Date[] | null) => {
        if (!value || Array.isArray(value)) return;

        const dia = value.getDate();
        if (diasSeleccionados.includes(dia)) {
            setDiasSeleccionados(diasSeleccionados.filter((d) => d !== dia));
        } else {
            setDiasSeleccionados([...diasSeleccionados, dia]);
        }
    };

    const handleCancelarTurnos = () => {
        if (!agendaId || diasSeleccionados.length === 0) return;
        agendaService.cancelarTurnos(String(agendaId), diasSeleccionados).then((response: CancelarTurnosResponse) => {
            if (response && response.mensaje) {
                alert(response.mensaje);
            }
            setDiasSeleccionados([]);
        });
    };

    if (!user) return <p>Cargando datos del usuario...</p>;

    return (
        <div>
            <Navbar title="Cancelar Turnos" onMenuClick={openMenu} />
            {menuOpen && (
                <div className={pageStyles.overlay} onClick={closeMenu}></div>
            )}
            <div className={styles.container}>
                <MedicoMenu isOpen={menuOpen} onClose={closeMenu} />

                <div className={styles.calendarContainer}>
                    <Calendar
                        onClickDay={handleClickDay}
                        tileClassName={({ date }) => {
                            const dia = date.getDate();
                            if (diasSeleccionados.includes(dia)) {
                                return styles.diaSeleccionado;
                            }
                            return turnosPorDia[dia] ? styles.diaConTurnos : '';
                        }}
                        tileDisabled={({ date }) => {
                            const mesActual = new Date().getMonth() + 1;
                            return date.getMonth() + 1 !== mesActual;
                        }}
                    />
                </div>

                <div className={styles.controls}>
                    <select
                        className={styles.profesionalSelect}
                        value={idProfesional || ''}
                        onChange={(e) => setIdProfesional(Number(e.target.value))}
                    >
                        {profesionales.map((profesional) => (
                            <option key={profesional.id} value={profesional.id}>
                                {`Dr/a ${profesional.nombre} ${profesional.apellido}`}
                            </option>
                        ))}
                    </select>
                    <button
                        className={styles.cancelButton}
                        onClick={handleCancelarTurnos}
                    >
                        Cancelar turnos
                    </button>
                </div>
            </div>
        </div>
    );
}


