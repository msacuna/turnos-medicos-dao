import { useState, useEffect } from 'react';
import 'react-calendar/dist/Calendar.css';
import '../../styles/global.css';




import { useAuth } from '../../hooks/useAuth';
import {
    getHorariosProfesional,
    updateHorarioProfesional,
} from '../../service/agendaService';
import Navbar from '@/components/ui/Navbar';
import MedicoMenu from '@/components/menu/MedicoMenu';
import pageStyles from '@/styles/pages/principal.module.css';
import styles from '@/styles/pages/agenda.module.css';

// Días que mostrará el frontend
const DIAS = [
    { front: 'LUNES', backend: 'Lunes', color: '#6366f1' },
    { front: 'MARTES', backend: 'Martes', color: '#8b5cf6' },
    { front: 'MIÉRCOLES', backend: 'Miercoles', color: '#ec4899' },
    { front: 'JUEVES', backend: 'Jueves', color: '#f43f5e' },
    { front: 'VIERNES', backend: 'Viernes', color: '#f97316' },
    { front: 'SÁBADO', backend: 'Sabado', color: '#14b8a6' },
];

export default function Agenda() {
    const { user } = useAuth();

    const profesionalId = user?.id ?? null;

    const [horarios, setHorarios] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [guardando, setGuardando] = useState<string | null>(null);
    const [menuOpen, setMenuOpen] = useState(false);
    const openMenu = () => setMenuOpen(true);
    const closeMenu = () => setMenuOpen(false);

    useEffect(() => {
        if (!profesionalId) return;

        const loadHorarios = async () => {
            try {
                const data = await getHorariosProfesional(profesionalId);

                // Normalizamos los datos para que coincidan con los días del frontend
                const map = DIAS.map(({ front, backend, color }) => {
                    const encontrado = data.find((h) => h.dia_semana === backend);
                    return encontrado
                        ? {
                            dia_front: front,
                            dia_back: backend,
                            color,
                            trabaja: true,
                            hora_inicio: encontrado.hora_inicio.slice(0, 5),
                            hora_fin: encontrado.hora_fin.slice(0, 5),
                        }
                        : {
                            dia_front: front,
                            dia_back: backend,
                            color,
                            trabaja: false,
                            hora_inicio: '',  // string vacío en lugar de null
                            hora_fin: '',     // string vacío en lugar de null
                        };
                });

                setHorarios(map);
            } catch (e) {
                console.error('Error cargando horarios:', e);
            } finally {
                setLoading(false);
            }
        };

        loadHorarios();
    }, [profesionalId]);

    const actualizarCampo = (dia_front: string, campo: string, valor: any) => {
        setHorarios((prev) =>
            prev.map((h) =>
                h.dia_front === dia_front 
                    ? { 
                        ...h, 
                        [campo]: valor,
                        // Si se desactiva trabaja, limpiar las horas
                        ...(campo === 'trabaja' && !valor && {
                            hora_inicio: '',
                            hora_fin: ''
                        })
                    } 
                    : h
            )
        );
    };

    const guardarCambios = async (dia_front: string) => {
        const horario = horarios.find((h) => h.dia_front === dia_front);
        if (!horario) return;

        setGuardando(dia_front);

        try {
            await updateHorarioProfesional(profesionalId!, horario.dia_front, {
                trabaja: horario.trabaja,
                hora_inicio: horario.trabaja ? horario.hora_inicio : null,
                hora_fin: horario.trabaja ? horario.hora_fin : null,
            });

            // Éxito - el mensaje visual ya está en el estado de guardando
            setTimeout(() => setGuardando(null), 1000);
        } catch (e) {
            console.error('Error guardando horario:', e);
            alert('Error al guardar horario');
            setGuardando(null);
        }
    };

    if (loading) {
        return (
            <div className={styles.loadingContainer}>
                <div className={styles.spinner}></div>
                <p>Cargando horarios del profesional...</p>
            </div>
        );
    }

    return (
        <div className={styles.pageContainer}>
            <Navbar title="Horarios del Profesional" onMenuClick={openMenu} />
            {menuOpen && (
                <div className={pageStyles.overlay} onClick={closeMenu}></div>
            )}

            <MedicoMenu isOpen={menuOpen} onClose={closeMenu} />

            <div className={styles.container}>
                <div className={styles.header}>
                    <h2>Configura tu disponibilidad</h2>
                    <p>
                        Establece los horarios en los que estarás disponible para consultas
                    </p>
                </div>

                <div className={styles.scheduleGrid}>
                    {horarios.map((h) => (
                        <div
                            key={h.dia_front}
                            className={`${styles.dayCard} ${h.trabaja ? styles.active : ''}`}
                        >
                            <div
                                className={styles.dayHeader}
                                style={{
                                    borderLeftColor: h.color,
                                    backgroundColor: h.trabaja ? `${h.color}15` : '#f8f9fa',
                                }}
                            >
                                <div className={styles.dayTitle}>
                                    <div
                                        className={styles.dayIndicator}
                                        style={{ backgroundColor: h.color }}
                                    ></div>
                                    <h3>{h.dia_front}</h3>
                                </div>

                                <label className={styles.toggleSwitch}>
                                    <input
                                        type="checkbox"
                                        checked={h.trabaja}
                                        onChange={(e) =>
                                            actualizarCampo(h.dia_front, 'trabaja', e.target.checked)
                                        }
                                    />
                                    <span className={styles.slider}></span>
                                </label>
                            </div>

                            {h.trabaja && (
                                <div className={styles.timeInputsContainer}>
                                    <div className={styles.timeInputGroup}>
                                        <label>Hora de Inicio</label>
                                        <div className={styles.timeInput}>
                                            <svg
                                                className={styles.clockIcon}
                                                viewBox="0 0 24 24"
                                                fill="none"
                                                stroke="currentColor"
                                            >
                                                <circle cx="12" cy="12" r="10" strokeWidth="2" />
                                                <path
                                                    d="M12 6v6l4 2"
                                                    strokeWidth="2"
                                                    strokeLinecap="round"
                                                />
                                            </svg>
                                            <input
                                                type="time"
                                                value={h.hora_inicio || ''}
                                                onChange={(e) =>
                                                    actualizarCampo(
                                                        h.dia_front,
                                                        'hora_inicio',
                                                        e.target.value
                                                    )
                                                }
                                            />
                                        </div>
                                    </div>

                                    <div className={styles.timeInputGroup}>
                                        <label>Hora de Fin</label>
                                        <div className={styles.timeInput}>
                                            <svg
                                                className={styles.clockIcon}
                                                viewBox="0 0 24 24"
                                                fill="none"
                                                stroke="currentColor"
                                            >
                                                <circle cx="12" cy="12" r="10" strokeWidth="2" />
                                                <path
                                                    d="M12 6v6l4 2"
                                                    strokeWidth="2"
                                                    strokeLinecap="round"
                                                />
                                            </svg>
                                            <input
                                                type="time"
                                                value={h.hora_fin}
                                                onChange={(e) =>
                                                    actualizarCampo(
                                                        h.dia_front,
                                                        'hora_fin',
                                                        e.target.value
                                                    )
                                                }
                                            />
                                        </div>
                                    </div>
                                </div>
                            )}

                            <button
                                onClick={() => guardarCambios(h.dia_front)}
                                disabled={guardando === h.dia_front}
                                className={`${styles.saveButton} ${guardando === h.dia_front ? styles.saving : ''
                                    }`}
                                style={{
                                    backgroundColor: h.trabaja ? h.color : '#94a3b8',
                                }}
                            >
                                {guardando === h.dia_front ? (
                                    <>
                                        <span className={styles.buttonSpinner}></span>
                                        Guardando...
                                    </>
                                ) : (
                                    <>
                                        <svg
                                            className={styles.saveIcon}
                                            viewBox="0 0 24 24"
                                            fill="none"
                                            stroke="currentColor"
                                        >
                                            <path
                                                d="M19 21H5a2 2 0 01-2-2V5a2 2 0 012-2h11l5 5v11a2 2 0 01-2 2z"
                                                strokeWidth="2"
                                            />
                                            <path d="M7 3v6h10" strokeWidth="2" />
                                            <path d="M9 13h6" strokeWidth="2" />
                                            <path d="M9 17h6" strokeWidth="2" />
                                        </svg>
                                        Guardar Cambios
                                    </>
                                )}
                            </button>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}
