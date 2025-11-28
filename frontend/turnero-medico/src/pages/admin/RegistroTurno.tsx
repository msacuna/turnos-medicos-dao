import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import turnoService from '../../service/turnoService';
import styles from '../../styles/pages/registroTurno.module.css';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';
import '../../styles/global.css';
import type { Paciente } from '../../types/Paciente';
import type { Turno } from '../../types/Turno';
import type { Profesional } from '../../types/Profesional';
import type { Especialidad } from '../../types/Especialidad';
import Navbar from '@/components/ui/Navbar';
import AdminMenu from '@/components/menu/AdminMenu';
import pageStyles from '@/styles/pages/principal.module.css';

export default function RegistroTurno() {
  const [dni, setDni] = useState('');
  const [noEncontrado, setNoEncontrado] = useState(false);
  
  const [especialidades, setEspecialidades] = useState<Especialidad[]>([]);
  const [profesionales, setProfesionales] = useState<Profesional[]>([]);
  
  const [idEspecialidad, setIdEspecialidad] = useState('');
  const [idProfesional, setIdProfesional] = useState('');
  
  const [turnos, setTurnos] = useState<Turno[]>([]);
  const [turnosFiltrados, setTurnosFiltrados] = useState<Turno[]>([]);
  
  const [mostrarCalendario, setMostrarCalendario] = useState(false);
  const [paciente, setPaciente] = useState<Paciente | null>(null);
  const [fechaSeleccionada, setFechaSeleccionada] = useState<Date | null>(null);
  
  // Estados para loading y mensajes
  const [loading, setLoading] = useState({
    paciente: false,
    profesionales: false,
    turnos: false,
    agendando: false
  });
  
  const [mensaje, setMensaje] = useState<{tipo: 'success' | 'error' | 'info', texto: string} | null>(null);

  const navigate = useNavigate();
  const [menuOpen, setMenuOpen] = useState(false);
  const openMenu = () => setMenuOpen(true);
  const closeMenu = () => setMenuOpen(false);

  // Función para mostrar mensajes temporales
  const mostrarMensaje = (tipo: 'success' | 'error' | 'info', texto: string, duracion = 5000) => {
    setMensaje({ tipo, texto });
    setTimeout(() => setMensaje(null), duracion);
  };

  // Reiniciar todo el flujo
  const reiniciarFormulario = () => {
    setDni('');
    setNoEncontrado(false);
    setPaciente(null);
    setEspecialidades([]);
    setProfesionales([]);
    setIdEspecialidad('');
    setIdProfesional('');
    setTurnos([]);
    setTurnosFiltrados([]);
    setMostrarCalendario(false);
    setFechaSeleccionada(null);
    setMensaje(null);
  };

  // ------------------ BUSCAR PACIENTE ------------------
  const buscarPaciente = async () => {
    if (!dni.trim()) {
      mostrarMensaje('error', 'Por favor, ingrese un DNI válido');
      return;
    }

    setLoading(prev => ({ ...prev, paciente: true }));
    
    try {
      const encontrado = await turnoService.buscarPacientePorDni(dni);

      if (!encontrado) {
        setPaciente(null);
        setNoEncontrado(true);
        return;
      }

      setPaciente(encontrado);
      setNoEncontrado(false);
      mostrarMensaje('success', `Paciente ${encontrado.nombre} ${encontrado.apellido} encontrado`);

      // Cargar especialidades automáticamente
      const esp = await turnoService.obtenerEspecialidades();
      setEspecialidades(esp);

    } catch (error: unknown) {
      console.error('Error buscando paciente:', error);
      
      if (error && typeof error === 'object' && 'response' in error) {
        const axiosError = error as import('axios').AxiosError;
        
        if (axiosError.response?.status === 404) {
          setPaciente(null);
          setNoEncontrado(true);
        } else {
          mostrarMensaje('error', 'Error al buscar el paciente. Verifique la conexión e intente nuevamente.');
        }
      } else {
        mostrarMensaje('error', 'Error de conexión. Por favor, intente nuevamente.');
      }
    } finally {
      setLoading(prev => ({ ...prev, paciente: false }));
    }
  };

  // ------------------ BUSCAR PROFESIONALES ------------------
  const cargarProfesionales = async (idEsp: string) => {
    setIdEspecialidad(idEsp);
    setProfesionales([]);
    setIdProfesional('');
    setMostrarCalendario(false);
    
    if (!idEsp) return;
    
    setLoading(prev => ({ ...prev, profesionales: true }));
    
    try {
      const prof = await turnoService.obtenerProfesionalesPorEspecialidad(idEsp);
      setProfesionales(prof);
      
      if (prof.length === 0) {
        mostrarMensaje('info', 'No hay profesionales disponibles para esta especialidad');
      }
    } catch (error) {
      console.error('Error cargando profesionales:', error);
      mostrarMensaje('error', 'Error al cargar profesionales');
    } finally {
      setLoading(prev => ({ ...prev, profesionales: false }));
    }
  };

  // ------------------ BUSCAR TURNOS ------------------
  const obtenerTurnosAgenda = async () => {
    if (!idProfesional) return;

    setLoading(prev => ({ ...prev, turnos: true }));

    try {
      const agendaId = 1;
      const t = await turnoService.obtenerTurnosAgenda(idProfesional, agendaId);
      
      if (!t || t.length === 0) {
        mostrarMensaje('info', 'El profesional seleccionado no tiene turnos disponibles');
        return;
      }
      
      setTurnos(t);
      setMostrarCalendario(true);
      mostrarMensaje('success', `Se encontraron ${t.length} turnos disponibles. Seleccione una fecha en el calendario.`);

    } catch (error: unknown) {
      console.error('Error obteniendo turnos:', error);
      
      let mensaje = 'No se pudieron obtener los turnos del profesional seleccionado.';
      
      if (error instanceof Error) {
        if (error.message === 'AGENDA_NO_DISPONIBLE') {
          mensaje = 'El profesional no tiene agenda disponible para este período.';
        } else if (error.message === 'Network Error' || error.message.includes('CORS')) {
          mensaje = 'El profesional podría no tener agenda configurada.';
        }
      }
      
      if (error && typeof error === 'object' && 'response' in error) {
        const axiosError = error as import('axios').AxiosError;
        if (axiosError.response?.status === 404) {
          mensaje = 'El profesional no tiene agenda disponible.';
        } else if (axiosError.response?.status === 500) {
          mensaje = 'Error del servidor. El profesional podría no tener agenda configurada.';
        }
      }
      
      mostrarMensaje('error', mensaje);
    } finally {
      setLoading(prev => ({ ...prev, turnos: false }));
    }
  };

  // ------------------ FILTRAR TURNOS POR FECHA ------------------
  const filtrarTurnosPorDia = (fecha: Date) => {
    setFechaSeleccionada(fecha);
    const dateStr = fecha.toISOString().split('T')[0];
    const t = turnos.filter((tu) => tu.fecha === dateStr);
    setTurnosFiltrados(t);
    
    if (t.length === 0) {
      mostrarMensaje('info', 'No hay turnos disponibles para esta fecha');
    } else {
      const disponibles = t.filter(turno => !turno.dni_paciente).length;
      mostrarMensaje('info', `${disponibles} turnos disponibles para ${fecha.toLocaleDateString()}`);
    }
  };

  // ------------------ AGENDAR ------------------
  const agendar = async (turnoId: number) => {
    if (!paciente) return;
    
    setLoading(prev => ({ ...prev, agendando: true }));
    
    try {
      await turnoService.agendar(turnoId, paciente.dni);
      
      mostrarMensaje('success', '¡Turno registrado exitosamente! Redirigiendo...', 3000);
      
      // Esperar un poco antes de reiniciar para que se vea el mensaje
      setTimeout(() => {
        reiniciarFormulario();
      }, 2000);
      
    } catch (error) {
      console.error('Error agendando turno:', error);
      mostrarMensaje('error', 'Error al agendar el turno. Por favor, intente nuevamente.');
    } finally {
      setLoading(prev => ({ ...prev, agendando: false }));
    }
  };

  // Progreso del flujo
  const progreso = paciente ? (idEspecialidad ? (idProfesional ? (mostrarCalendario ? 4 : 3) : 2) : 1) : 0;
  const pasos = ['Buscar Paciente', 'Seleccionar Especialidad', 'Seleccionar Profesional', 'Seleccionar Turno'];

  return (
    <div className={styles.container}>
      <Navbar title="Registrar Turno" onMenuClick={openMenu} />
      {menuOpen && (
        <div className={pageStyles.overlay} onClick={closeMenu}></div>
      )}

      <AdminMenu isOpen={menuOpen} onClose={closeMenu} />

      {/* INDICADOR DE PROGRESO */}
      <div className={styles.progressContainer}>
        <h2>Proceso de Registro de Turno</h2>
        <div className={styles.progressBar}>
          {pasos.map((paso, index) => (
            <div 
              key={index} 
              className={`${styles.progressStep} ${index <= progreso ? styles.active : ''}`}
            >
              <div className={styles.stepNumber}>{index + 1}</div>
              <span className={styles.stepLabel}>{paso}</span>
            </div>
          ))}
        </div>
      </div>

      {/* MENSAJES */}
      {mensaje && (
        <div className={`${styles.mensaje} ${styles[mensaje.tipo]}`}>
          <span>{mensaje.texto}</span>
          <button onClick={() => setMensaje(null)}>×</button>
        </div>
      )}

      {/* PASO 1: BUSCAR PACIENTE */}
      <div className={`${styles.card} ${progreso >= 0 ? styles.activeCard : ''}`}>
        <div className={styles.cardHeader}>
          <h3>📋 Paso 1: Buscar Paciente</h3>
          {paciente && (
            <button 
              className={styles.editButton}
              onClick={() => {
                setPaciente(null);
                setEspecialidades([]);
                setProfesionales([]);
                setMostrarCalendario(false);
              }}
            >
              Cambiar Paciente
            </button>
          )}
        </div>
        
        {!paciente ? (
          <div className={styles.cardContent}>
            <label htmlFor="dni">DNI del Paciente</label>
            <input
              id="dni"
              type="text"
              value={dni}
              onChange={(e) => setDni(e.target.value)}
              placeholder="Ingrese el DNI del paciente"
              onKeyPress={(e) => e.key === 'Enter' && buscarPaciente()}
            />

            <div className={styles.actionsRow}>
              <button 
                onClick={() => navigate('/admin')} 
                className={styles.secondaryButton}
              >
                Cancelar
              </button>
              <button 
                onClick={buscarPaciente}
                disabled={loading.paciente}
                className={styles.primaryButton}
              >
                {loading.paciente ? 'Buscando...' : 'Buscar Paciente'}
              </button>
            </div>
          </div>
        ) : (
          <div className={styles.cardContent}>
            <div className={styles.pacienteInfo}>
              <h4>✅ Paciente Encontrado</h4>
              <p><strong>Nombre:</strong> {paciente.nombre} {paciente.apellido}</p>
              <p><strong>DNI:</strong> {paciente.dni}</p>
            </div>
          </div>
        )}
      </div>

      {/* PACIENTE NO ENCONTRADO */}
      {noEncontrado && (
        <div className={styles.noFound}>
          <div className={styles.noFoundContent}>
            <h3>❌ Paciente no encontrado</h3>
            <p>No se encontró un paciente registrado con el DNI: <strong>{dni}</strong></p>
            
            <div className={styles.actionsRow}>
              <button 
                onClick={() => setNoEncontrado(false)}
                className={styles.secondaryButton}
              >
                Buscar Otro
              </button>
              <button 
                onClick={() => navigate('/admin/RegistroPacientes')}
                className={styles.primaryButton}
              >
                Registrar Paciente
              </button>
            </div>
          </div>
        </div>
      )}

      {/* PASO 2: SELECCIONAR ESPECIALIDAD */}
      {paciente && (
        <div className={`${styles.card} ${progreso >= 1 ? styles.activeCard : ''}`}>
          <div className={styles.cardHeader}>
            <h3>🏥 Paso 2: Seleccionar Especialidad</h3>
          </div>
          
          <div className={styles.cardContent}>
            <label htmlFor="especialidad">Especialidad Médica</label>
            <select 
              id="especialidad"
              value={idEspecialidad}
              onChange={(e) => cargarProfesionales(e.target.value)}
              disabled={loading.profesionales}
            >
              <option value="">-- Seleccione una especialidad --</option>
              {especialidades.map((esp) => (
                <option key={esp.id} value={esp.id}>
                  {esp.nombre}
                </option>
              ))}
            </select>
            
            {loading.profesionales && (
              <p className={styles.loading}>Cargando profesionales...</p>
            )}
          </div>
        </div>
      )}

      {/* PASO 3: SELECCIONAR PROFESIONAL */}
      {profesionales.length > 0 && (
        <div className={`${styles.card} ${progreso >= 2 ? styles.activeCard : ''}`}>
          <div className={styles.cardHeader}>
            <h3>👨‍⚕️ Paso 3: Seleccionar Profesional</h3>
          </div>
          
          <div className={styles.cardContent}>
            <label htmlFor="profesional">Profesional Médico</label>
            <select 
              id="profesional"
              value={idProfesional}
              onChange={(e) => setIdProfesional(e.target.value)}
            >
              <option value="">-- Seleccione un profesional --</option>
              {profesionales.map((prof) => (
                <option key={prof.id} value={prof.id}>
                  Dr/a. {prof.nombre} {prof.apellido}
                </option>
              ))}
            </select>
            
            <div className={styles.actionsRow}>
              <button 
                onClick={obtenerTurnosAgenda}
                disabled={!idProfesional || loading.turnos}
                className={styles.primaryButton}
              >
                {loading.turnos ? 'Cargando turnos...' : 'Ver Turnos Disponibles'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* PASO 4: SELECCIONAR TURNO */}
      {mostrarCalendario && (
        <div className={`${styles.card} ${styles.activeCard}`}>
          <div className={styles.cardHeader}>
            <h3>📅 Paso 4: Seleccionar Fecha y Turno</h3>
          </div>
          
          <div className={styles.cardContent}>
            <div className={styles.calendarSection}>
              <div className={styles.calendarContainer}>
                <h4>Seleccione una fecha:</h4>
                <Calendar 
                  onClickDay={filtrarTurnosPorDia}
                  value={fechaSeleccionada}
                  minDate={new Date()}
                  locale="es-ES"
                />
              </div>

              {fechaSeleccionada && (
                <div className={styles.turnosSection}>
                  <h4>Turnos para {fechaSeleccionada.toLocaleDateString('es-ES', { 
                    weekday: 'long', 
                    year: 'numeric', 
                    month: 'long', 
                    day: 'numeric' 
                  })}</h4>

                  {turnosFiltrados.length === 0 ? (
                    <div className={styles.noTurnos}>
                      <p>No hay turnos disponibles para esta fecha</p>
                    </div>
                  ) : (
                    <div className={styles.turnosList}>
                      {turnosFiltrados.map((t) => (
                        <div
                          key={t.id}
                          className={`${styles.turnoCard} ${
                            t.dni_paciente ? styles.ocupado : styles.disponible
                          }`}
                          onClick={() => {
                            if (!t.dni_paciente && !loading.agendando) {
                              agendar(t.id);
                            }
                          }}
                        >
                          <div className={styles.turnoHora}>
                            {t.hora_inicio?.substring(0, 5) || 'N/A'} - {t.hora_fin_estimada?.substring(0, 5) || 'N/A'}
                          </div>
                          <div className={styles.turnoEstado}>
                            {t.dni_paciente ? (
                              <span className={styles.ocupado}>🔴 OCUPADO</span>
                            ) : (
                              <span className={styles.disponible}>
                                {loading.agendando ? '⏳ Agendando...' : '🟢 DISPONIBLE - Haga clic para agendar'}
                              </span>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* BOTÓN PARA EMPEZAR DE NUEVO */}
      {(paciente || noEncontrado) && (
        <div className={styles.resetSection}>
          <button 
            onClick={reiniciarFormulario}
            className={styles.resetButton}
          >
            🔄 Registrar Otro Turno
          </button>
        </div>
      )}
    </div>
  );
}