import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import turnoService from '../../service/turnoService';
import styles from '../../styles/pages/registroTurno.module.css';
import Calendar from 'react-calendar'; // npm install react-calendar
import 'react-calendar/dist/Calendar.css';
import type { Paciente } from '../../types/Paciente';
import type { Turno } from '../../types/Turno';
import type { Profesional } from '../../types/Profesional';
import type { Especialidad } from '../../types/Especialidad';

export default function RegistroTurno() {
  const [dni, setDni] = useState('');
  const [noEncontrado, setNoEncontrado] = useState(false);

  const [especialidades, setEspecialidades] = useState<Especialidad[]>([]);
  const [profesionales, setProfesionales] = useState<Profesional[]>([]);

  const [, setIdEspecialidad] = useState('');
  const [idProfesional, setIdProfesional] = useState('');

  const [turnos, setTurnos] = useState<Turno[]>([]);
  const [turnosFiltrados, setTurnosFiltrados] = useState<Turno[]>([]);

  const [mostrarCalendario, setMostrarCalendario] = useState(false);
  const [paciente, setPaciente] = useState<Paciente | null>(null);

  const navigate = useNavigate();

  // ------------------ BUSCAR PACIENTE ------------------
  const buscarPaciente = async () => {
    if (!dni) {
      alert('Por favor, ingrese un DNI');
      return;
    }

    try {
      const encontrado = await turnoService.buscarPacientePorDni(dni);

      if (!encontrado) {
        setPaciente(null);
        setNoEncontrado(true);
        return;
      }

      setPaciente(encontrado);
      setNoEncontrado(false);

      // Cargar especialidades
      const esp = await turnoService.obtenerEspecialidades();
      setEspecialidades(esp);

    } catch (error: unknown) {
      console.error('Error buscando paciente:', error);
      
      // Manejar diferentes tipos de errores
      if (error && typeof error === 'object' && 'response' in error) {
        const axiosError = error as import('axios').AxiosError;
        
        if (axiosError.response?.status === 404) {
          // Paciente no encontrado
          setPaciente(null);
          setNoEncontrado(true);
        } else {
          // Otros errores (500, network, etc.)
          alert('Error al buscar el paciente. Por favor, verifique la conexión e intente nuevamente.');
        }
      } else {
        // Error de red u otro tipo
        alert('Error de conexión. Por favor, intente nuevamente.');
      }
    }
  };

  // ------------------ BUSCAR PROFESIONALES ------------------
  const cargarProfesionales = async (idEsp: string) => {
    setIdEspecialidad(idEsp);
    const prof = await turnoService.obtenerProfesionalesPorEspecialidad(idEsp);
    setProfesionales(prof);
  };

  // ------------------ BUSCAR TURNOS ------------------
  const obtenerTurnosAgenda = async () => {
  if (!idProfesional) return;

  try {
    const agendaId = 1; // Mantener la lógica original como fallback
    const t = await turnoService.obtenerTurnosAgenda(idProfesional, agendaId);
    
    if (!t || t.length === 0) {
      alert('El profesional seleccionado no tiene turnos disponibles en este momento.');
      return;
    }
    
    setTurnos(t);
    setMostrarCalendario(true);

  } catch (error: unknown) {
    console.error('Error obteniendo turnos:', error);
    
    let mensaje = 'No se pudieron obtener los turnos del profesional seleccionado.';
    
    if (error instanceof Error) {
      // Error específico de agenda no disponible
      if (error.message === 'AGENDA_NO_DISPONIBLE') {
        mensaje = 'El profesional seleccionado no tiene agenda disponible para este período.';
      }
      // Error de red/CORS
      else if (error.message === 'Network Error' || error.message.includes('CORS')) {
        mensaje = 'Hay un problema de conexión. El profesional seleccionado podría no tener agenda configurada.';
      }
    }
    
    // Si es un error de axios
    if (error && typeof error === 'object' && 'response' in error) {
      const axiosError = error as import('axios').AxiosError;
      if (axiosError.response?.status === 404) {
        mensaje = 'El profesional seleccionado no tiene agenda disponible.';
      } else if (axiosError.response?.status === 500) {
        mensaje = 'Error del servidor. El profesional seleccionado podría no tener agenda configurada.';
      }
    }
    
    alert(mensaje + '\n\nPor favor, seleccione otro profesional o intente más tarde.');
  }
};

  // ------------------ FILTRAR TURNOS POR FECHA ------------------
  const filtrarTurnosPorDia = (fecha: Date) => {
    const dateStr = fecha.toISOString().split('T')[0];
    const t = turnos.filter((tu) => tu.fecha === dateStr);
    setTurnosFiltrados(t);
  };

  // ------------------ AGENDAR ------------------
  const agendar = async (turnoId: number) => {
    if (!paciente) return;
    
    try {
      // Agendar el turno
      await turnoService.agendar(turnoId, paciente.dni);
      
      // Mostrar mensaje de éxito
      alert('Turno registrado con éxito');

      // Resetear todo el estado para volver al inicio
      setDni('');
      setNoEncontrado(false);
      setPaciente(null);
      setEspecialidades([]);
      setProfesionales([]);
      setIdProfesional('');
      setTurnos([]);
      setTurnosFiltrados([]);
      setMostrarCalendario(false);
      
    } catch (error) {
      console.error('Error agendando turno:', error);
      alert('Error al agendar el turno. Por favor, intente nuevamente.');
    }
  };

  return (
    <div className={styles.container}>
      <h1>Registrar turno</h1>

      {/* BUSCAR PACIENTE */}
      <div className={styles.card}>
        <label>Paciente (DNI)</label>
        <input
          type="text"
          value={dni}
          onChange={(e) => setDni(e.target.value)}
        />

        <div className={styles.actionsRow}>
          <button onClick={() => navigate(-1)}>Cancelar</button>
          <button onClick={buscarPaciente}>Buscar</button>
        </div>
      </div>

      {/* PACIENTE NO ENCONTRADO */}
      {noEncontrado && (
        <div className={styles.noFound}>
          <p>Paciente no registrado</p>

          <div className={styles.actionsRow}>
            <button onClick={() => setNoEncontrado(false)}>Cancelar</button>
            <button onClick={() => navigate('/admin/pacientes')}>
              Registrar
            </button>
          </div>
        </div>
      )}

      {/* PACIENTE ENCONTRADO */}
      {paciente && (
        <div className={styles.card}>
          <h3>Datos del paciente</h3>
          <p>
            <strong>Nombre:</strong> {paciente.nombre}
          </p>
          <p>
            <strong>Apellido:</strong> {paciente.apellido}
          </p>
          <p>
            <strong>DNI:</strong> {paciente.dni}
          </p>

          {/* SELECT ESPECIALIDAD */}
          <label>Especialidad</label>
          <select onChange={(e) => cargarProfesionales(e.target.value)}>
            <option value="">Seleccione...</option>
            {especialidades.map((esp) => (
              <option key={esp.id} value={esp.id}>
                {esp.nombre}
              </option>
            ))}
          </select>

          {/* SELECT PROFESIONAL */}
          {profesionales.length > 0 && (
            <>
              <label>Profesional</label>
              <select onChange={(e) => setIdProfesional(e.target.value)}>
                <option value="">Seleccione...</option>
                {profesionales.map((prof) => (
                  <option key={prof.id} value={prof.id}>
                    {prof.nombre} {prof.apellido}
                  </option>
                ))}
              </select>
            </>
          )}

          <div className={styles.actionsRow}>
            <button onClick={() => navigate(-1)}>Cancelar</button>
            <button onClick={obtenerTurnosAgenda}>Buscar</button>
          </div>
        </div>
      )}

      {/* CALENDARIO */}
      {mostrarCalendario && (
        <div className={styles.calendarContainer}>
          <Calendar onClickDay={(value) => filtrarTurnosPorDia(value)} />

          <h2>Turnos del día</h2>

          {turnosFiltrados.length === 0 && <p>No hay turnos</p>}

          {turnosFiltrados.map((t) => (
            <div
              key={t.id}
              className={`${styles.turno} ${
                t.dni_paciente ? styles.ocupado : styles.libre
              }`}
              onClick={() => {
                // Solo permitir click en turnos libres
                if (!t.dni_paciente) {
                  agendar(t.id);
                }
              }}
              style={{ 
                cursor: t.dni_paciente ? 'not-allowed' : 'pointer' 
              }}
            >
              <span>
                {t.hora_inicio?.substring(0, 5) || 'N/A'} - {t.hora_fin_estimada?.substring(0, 5) || 'N/A'}
              </span>

              {t.dni_paciente && <strong>OCUPADO</strong>}
              {!t.dni_paciente && <em>Disponible</em>}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}