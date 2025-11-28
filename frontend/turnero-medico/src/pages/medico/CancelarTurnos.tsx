import { useState, useEffect } from 'react';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';
import Navbar from '@/components/ui/Navbar';
import MedicoMenu from '@/components/menu/MedicoMenu';
import { useAuth } from '../../hooks/useAuth';
import pageStyles from '@/styles/pages/principal.module.css';
import { cancelarService } from '../../service/cancelarService';

interface Profesional {
    id: number;
    nombre: string;
    apellido: string;
    email: string;
    matricula: string;
    telefono: string;
    id_especialidad: number;
}

interface Turno {
    id: number;
    fecha: string;
    hora_inicio: string;
    hora_fin_estimada: string;
    dni_paciente: number;
    nombre_estado: string;
    id_especialidad: number;
    id_agenda_profesional: number;
    monto: number;
}

export default function CancelarTurnos() {
    const { user } = useAuth();
    const [profesionales, setProfesionales] = useState<Profesional[]>([]);
    const [idProfesional, setIdProfesional] = useState<number | null>(null);
    const [agendaId, setAgendaId] = useState<number | null>(null);
    const [diasSeleccionados, setDiasSeleccionados] = useState<number[]>([]);
    const [turnosPorDia, setTurnosPorDia] = useState<Record<number, number>>({});
    const [menuOpen, setMenuOpen] = useState(false);
    const [loading, setLoading] = useState(false);
    const [pacientesNotificados, setPacientesNotificados] = useState<any[]>([]);

    const mesActual = new Date().getMonth() + 1;
    const anioActual = new Date().getFullYear();

    const openMenu = () => setMenuOpen(true);
    const closeMenu = () => setMenuOpen(false);

    // Obtener profesionales
    useEffect(() => {
        cancelarService
            .obtenerProfesionales()
            .then((data: Profesional[]) => {
                setProfesionales(data);
                if (data.length > 0) {
                    setIdProfesional(data[0].id);
                }
            })
            .catch((err) => {
                console.error('Error obteniendo profesionales:', err);
                alert('Error al cargar los profesionales');
            });
    }, []);

    // Obtener agenda cuando cambia el profesional
    useEffect(() => {
        if (!idProfesional) return;

        // Resetear datos cuando cambia el profesional
        setAgendaId(null);
        setTurnosPorDia({});
        setDiasSeleccionados([]);

        cancelarService
            .obtenerAgenda(idProfesional, mesActual)
            .then((agenda) => {
                setAgendaId(agenda.id);
            })
            .catch((err) => {
                console.error('Error obteniendo agenda:', err);
                if (err.response?.status === 404) {
                    alert('El profesional seleccionado no tiene agenda para el mes actual');
                } else {
                    alert('Error al obtener la agenda del profesional');
                }
                setAgendaId(null);
                setTurnosPorDia({});
            });
    }, [idProfesional, mesActual]);

    // Obtener turnos cuando cambia la agenda
    useEffect(() => {
        // IMPORTANTE: Solo ejecutar si tenemos agenda Y profesional
        if (!agendaId || !idProfesional) {
            setTurnosPorDia({});
            return;
        }

        console.log('Cargando turnos para:', { idProfesional, agendaId });

        cancelarService
            .obtenerTurnos(idProfesional, agendaId)
            .then((turnos: Turno[]) => {
                // Filtrar solo turnos Disponibles o Agendados
                const turnosFiltrados = turnos.filter(
                    (t) => t.nombre_estado === 'Disponible' || t.nombre_estado === 'Agendado'
                );

                // Contar turnos por día - IMPORTANTE: parsear fecha correctamente
                const conteo = turnosFiltrados.reduce((acc: Record<number, number>, turno) => {
                    // Extraer el día directamente del string "YYYY-MM-DD" sin convertir a Date
                    const [year, month, day] = turno.fecha.split('-');
                    const dia = parseInt(day, 10);

                    console.log('Turno fecha:', turno.fecha, '-> día:', dia);

                    acc[dia] = (acc[dia] || 0) + 1;
                    return acc;
                }, {});

                console.log('Turnos por día:', conteo);
                setTurnosPorDia(conteo);
            })
            .catch((err) => {
                console.error('Error obteniendo turnos:', err);
                // No mostrar alert aquí si es por cambio de profesional
                setTurnosPorDia({});
            });
    }, [agendaId, idProfesional]);

    const handleClickDay = (value: Date) => {
        // Crear una fecha en la zona horaria local para evitar problemas de conversión
        const fecha = new Date(value.getFullYear(), value.getMonth(), value.getDate());
        const dia = fecha.getDate();

        console.log('Día seleccionado:', { fecha, dia, mesActual, anioActual });

        // Solo permitir seleccionar días del mes actual
        if (value.getMonth() + 1 !== mesActual || value.getFullYear() !== anioActual) {
            return;
        }

        if (diasSeleccionados.includes(dia)) {
            setDiasSeleccionados(diasSeleccionados.filter((d) => d !== dia));
        } else {
            setDiasSeleccionados([...diasSeleccionados, dia]);
        }
    };

    const handleCancelarTurnos = async () => {
        if (!agendaId || diasSeleccionados.length === 0) {
            alert('Por favor selecciona al menos un día');
            return;
        }

        console.log('Días a cancelar:', diasSeleccionados);

        setLoading(true);

        try {
            const data = await cancelarService.cancelarTurnos(agendaId, diasSeleccionados);

            console.log('Respuesta del backend:', data);

            // Los contactos vienen como array de arrays: [email, telefono, fecha_hora]
            setPacientesNotificados(data.contactos_notificados);

            // Limpiar selección
            setDiasSeleccionados([]);

            // Recargar turnos
            if (idProfesional) {
                const turnos = await cancelarService.obtenerTurnos(idProfesional, agendaId);
                const turnosFiltrados = turnos.filter(
                    (t: Turno) => t.nombre_estado === 'Disponible' || t.nombre_estado === 'Agendado'
                );
                const conteo = turnosFiltrados.reduce((acc: Record<number, number>, turno: Turno) => {
                    // Extraer el día directamente del string sin convertir a Date
                    const [year, month, day] = turno.fecha.split('-');
                    const dia = parseInt(day, 10);
                    acc[dia] = (acc[dia] || 0) + 1;
                    return acc;
                }, {});
                setTurnosPorDia(conteo);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Hubo un error al cancelar los turnos');
        } finally {
            setLoading(false);
        }
    };

    if (!user) return <p>Cargando datos del usuario...</p>;

    return (
        <div style={{ minHeight: '100vh', background: '#f5f5f5' }}>
            <Navbar title="Cancelar Turnos" onMenuClick={openMenu} />

            {menuOpen && <div className={pageStyles.overlay} onClick={closeMenu} />}

            <MedicoMenu isOpen={menuOpen} onClose={closeMenu} />

            <div
                style={{
                    maxWidth: '1200px',
                    margin: '0 auto',
                    padding: '2rem',
                }}
            >
                <style>{`
          .react-calendar {
            width: 100%;
            border: none;
            font-family: inherit;
          }
          .react-calendar__navigation {
            display: flex;
            margin-bottom: 1rem;
          }
          .react-calendar__navigation button {
            min-width: 44px;
            background: none;
            font-size: 16px;
            border: none;
            cursor: pointer;
          }
          .react-calendar__navigation button:disabled {
            opacity: 0.3;
            cursor: not-allowed;
          }
          .react-calendar__tile {
            padding: 1rem;
            background: none;
            text-align: center;
            border: 1px solid #e0e0e0;
            cursor: pointer;
            transition: all 0.2s;
          }
          .react-calendar__tile:hover:not(:disabled) {
            background: #f0f0f0;
          }
          .react-calendar__tile--active {
            background: #1976d2;
            color: white;
          }
          .react-calendar__tile--now {
            background: #fff9c4;
          }
          .react-calendar__tile:disabled {
            opacity: 0.3;
            cursor: not-allowed;
          }
          .dia-seleccionado {
            background: #f44336 !important;
            color: white !important;
            font-weight: bold;
          }
          .dia-con-turnos {
            background: #4caf50 !important;
            color: white !important;
            position: relative;
          }
          .dia-con-turnos::after {
            content: attr(data-turnos);
            position: absolute;
            top: 4px;
            right: 4px;
            background: rgba(255,255,255,0.9);
            color: #4caf50;
            border-radius: 50%;
            width: 20px;
            height: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 11px;
            font-weight: bold;
          }
          .dia-seleccionado.dia-con-turnos::after {
            background: rgba(255,255,255,0.9);
            color: #f44336;
          }
        `}</style>

                <div
                    style={{
                        display: 'flex',
                        gap: '2rem',
                        alignItems: 'flex-start',
                        flexWrap: 'wrap',
                    }}
                >
                    {/* Calendario */}
                    <div
                        style={{
                            flex: '1',
                            minWidth: '350px',
                            background: 'white',
                            borderRadius: '12px',
                            padding: '1.5rem',
                            boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
                        }}
                    >
                        <Calendar
                            value={new Date(anioActual, mesActual - 1, 1)}
                            onClickDay={handleClickDay}
                            tileClassName={({ date }) => {
                                const dia = date.getDate();
                                const classes = [];

                                if (
                                    diasSeleccionados.includes(dia) &&
                                    date.getMonth() + 1 === mesActual &&
                                    date.getFullYear() === anioActual
                                ) {
                                    classes.push('dia-seleccionado');
                                }

                                if (
                                    turnosPorDia[dia] &&
                                    date.getMonth() + 1 === mesActual &&
                                    date.getFullYear() === anioActual
                                ) {
                                    classes.push('dia-con-turnos');
                                }

                                return classes.join(' ');
                            }}
                            tileContent={({ date }) => {
                                const dia = date.getDate();
                                if (
                                    turnosPorDia[dia] &&
                                    date.getMonth() + 1 === mesActual &&
                                    date.getFullYear() === anioActual
                                ) {
                                    return <span data-turnos={turnosPorDia[dia]} />;
                                }
                                return null;
                            }}
                            tileDisabled={({ date }) => {
                                return date.getMonth() + 1 !== mesActual || date.getFullYear() !== anioActual;
                            }}
                            showNavigation={true}
                            nextLabel={null}
                            prevLabel={null}
                            next2Label={null}
                            prev2Label={null}
                        />

                        <div
                            style={{
                                marginTop: '1rem',
                                display: 'flex',
                                gap: '1rem',
                                fontSize: '14px',
                            }}
                        >
                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                <div
                                    style={{
                                        width: '20px',
                                        height: '20px',
                                        background: '#4caf50',
                                        borderRadius: '4px',
                                    }}
                                />
                                <span>Días con turnos</span>
                            </div>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                <div
                                    style={{
                                        width: '20px',
                                        height: '20px',
                                        background: '#f44336',
                                        borderRadius: '4px',
                                    }}
                                />
                                <span>Días seleccionados</span>
                            </div>
                        </div>
                    </div>

                    {/* Panel de control */}
                    <div
                        style={{
                            flex: '0 0 300px',
                            display: 'flex',
                            flexDirection: 'column',
                            gap: '1rem',
                        }}
                    >
                        {/* Selector de profesional */}
                        <div
                            style={{
                                background: 'rgba(255, 255, 255, 0.95)',
                                backdropFilter: 'blur(10px)',
                                borderRadius: '12px',
                                padding: '1.5rem',
                                boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
                                border: '1px solid rgba(255, 255, 255, 0.2)',
                            }}
                        >
                            <label
                                style={{
                                    display: 'block',
                                    marginBottom: '0.5rem',
                                    fontWeight: '600',
                                    color: '#333',
                                    fontSize: '14px',
                                }}
                            >
                                Seleccionar Profesional
                            </label>
                            <select
                                value={idProfesional || ''}
                                onChange={(e) => {
                                    setIdProfesional(Number(e.target.value));
                                    setDiasSeleccionados([]);
                                }}
                                style={{
                                    width: '100%',
                                    padding: '0.75rem',
                                    borderRadius: '8px',
                                    border: '2px solid #e0e0e0',
                                    fontSize: '15px',
                                    background: 'white',
                                    cursor: 'pointer',
                                    transition: 'all 0.2s',
                                    outline: 'none',
                                }}
                                onFocus={(e) => (e.target.style.borderColor = '#1976d2')}
                                onBlur={(e) => (e.target.style.borderColor = '#e0e0e0')}
                            >
                                {profesionales.map((prof) => (
                                    <option key={prof.id} value={prof.id}>
                                        Dr/a {prof.nombre} {prof.apellido}
                                    </option>
                                ))}
                            </select>
                        </div>

                        {/* Botón de cancelar */}
                        <button
                            onClick={handleCancelarTurnos}
                            disabled={loading || diasSeleccionados.length === 0}
                            style={{
                                width: '100%',
                                padding: '1rem',
                                background: diasSeleccionados.length === 0 ? '#ccc' : '#f44336',
                                color: 'white',
                                border: 'none',
                                borderRadius: '12px',
                                fontSize: '16px',
                                fontWeight: '600',
                                cursor: diasSeleccionados.length === 0 ? 'not-allowed' : 'pointer',
                                transition: 'all 0.2s',
                                boxShadow:
                                    diasSeleccionados.length === 0 ? 'none' : '0 4px 12px rgba(244, 67, 54, 0.3)',
                                opacity: loading ? 0.7 : 1,
                            }}
                            onMouseEnter={(e) => {
                                if (diasSeleccionados.length > 0 && !loading) {
                                    e.currentTarget.style.background = '#d32f2f';
                                    e.currentTarget.style.transform = 'translateY(-2px)';
                                    e.currentTarget.style.boxShadow = '0 6px 16px rgba(244, 67, 54, 0.4)';
                                }
                            }}
                            onMouseLeave={(e) => {
                                if (diasSeleccionados.length > 0) {
                                    e.currentTarget.style.background = '#f44336';
                                    e.currentTarget.style.transform = 'translateY(0)';
                                    e.currentTarget.style.boxShadow = '0 4px 12px rgba(244, 67, 54, 0.3)';
                                }
                            }}
                        >
                            {loading ? 'Cancelando...' : `Cancelar Turnos (${diasSeleccionados.length})`}
                        </button>

                        {/* Info adicional */}
                        {diasSeleccionados.length > 0 && (
                            <div
                                style={{
                                    background: 'rgba(244, 67, 54, 0.1)',
                                    borderLeft: '4px solid #f44336',
                                    padding: '1rem',
                                    borderRadius: '8px',
                                    fontSize: '14px',
                                    color: '#d32f2f',
                                }}
                            >
                                <strong>⚠️ Atención:</strong>
                                <p style={{ margin: '0.5rem 0 0 0' }}>
                                    Se cancelarán los turnos de {diasSeleccionados.length} día(s) seleccionado(s).
                                </p>
                            </div>
                        )}
                    </div>
                </div>

                {/* Lista de pacientes notificados */}
                {pacientesNotificados.length > 0 && (
                    <div
                        style={{
                            marginTop: '2rem',
                            background: 'white',
                            borderRadius: '12px',
                            padding: '1.5rem',
                            boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
                        }}
                    >
                        <h3
                            style={{
                                margin: '0 0 1rem 0',
                                fontSize: '18px',
                                fontWeight: '600',
                                color: '#333',
                            }}
                        >
                            Pacientes notificados con turnos cancelados
                        </h3>

                        <div style={{ overflowX: 'auto' }}>
                            <table
                                style={{
                                    width: '100%',
                                    borderCollapse: 'collapse',
                                    fontSize: '14px',
                                }}
                            >
                                <thead>
                                    <tr style={{ background: '#f5f5f5' }}>
                                        <th
                                            style={{
                                                padding: '0.75rem',
                                                textAlign: 'left',
                                                fontWeight: '600',
                                                borderBottom: '2px solid #e0e0e0',
                                            }}
                                        >
                                            Email
                                        </th>
                                        <th
                                            style={{
                                                padding: '0.75rem',
                                                textAlign: 'left',
                                                fontWeight: '600',
                                                borderBottom: '2px solid #e0e0e0',
                                            }}
                                        >
                                            Teléfono
                                        </th>
                                        <th
                                            style={{
                                                padding: '0.75rem',
                                                textAlign: 'left',
                                                fontWeight: '600',
                                                borderBottom: '2px solid #e0e0e0',
                                            }}
                                        >
                                            Fecha y Hora
                                        </th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {pacientesNotificados.map((contacto, index) => {
                                        // contacto es un array: [email, telefono, fecha_hora]
                                        const [email, telefono, fechaHora] = contacto;

                                        return (
                                            <tr
                                                key={index}
                                                style={{
                                                    borderBottom: '1px solid #e0e0e0',
                                                    transition: 'background 0.2s',
                                                }}
                                                onMouseEnter={(e) => (e.currentTarget.style.background = '#f9f9f9')}
                                                onMouseLeave={(e) => (e.currentTarget.style.background = 'white')}
                                            >
                                                <td style={{ padding: '0.75rem' }}>{email || 'Sin email'}</td>
                                                <td style={{ padding: '0.75rem' }}>{telefono || 'Sin teléfono'}</td>
                                                <td style={{ padding: '0.75rem' }}>
                                                    {fechaHora ? new Date(fechaHora).toLocaleString('es-AR', {
                                                        day: '2-digit',
                                                        month: '2-digit',
                                                        year: 'numeric',
                                                        hour: '2-digit',
                                                        minute: '2-digit'
                                                    }) : 'Sin fecha'}
                                                </td>
                                            </tr>
                                        );
                                    })}
                                </tbody>
                            </table>
                        </div>

                        <div
                            style={{
                                marginTop: '1.5rem',
                                padding: '1rem',
                                background: '#e3f2fd',
                                borderRadius: '8px',
                                borderLeft: '4px solid #2196f3',
                            }}
                        >
                            <p
                                style={{
                                    margin: 0,
                                    fontSize: '16px',
                                    fontWeight: '600',
                                    color: '#1565c0',
                                }}
                            >
                                ✓ Se cancelaron {pacientesNotificados.length} turno
                                {pacientesNotificados.length !== 1 ? 's' : ''}
                            </p>
                        </div>

                        <button
                            onClick={() => setPacientesNotificados([])}
                            style={{
                                marginTop: '1rem',
                                padding: '0.5rem 1rem',
                                background: '#f5f5f5',
                                border: '1px solid #e0e0e0',
                                borderRadius: '6px',
                                cursor: 'pointer',
                                fontSize: '14px',
                                transition: 'all 0.2s',
                            }}
                            onMouseEnter={(e) => (e.currentTarget.style.background = '#e0e0e0')}
                            onMouseLeave={(e) => (e.currentTarget.style.background = '#f5f5f5')}
                        >
                            Cerrar lista
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
}