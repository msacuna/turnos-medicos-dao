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

  const [idEspecialidad, setIdEspecialidad] = useState('');
  const [idProfesional, setIdProfesional] = useState('');

  const [turnos, setTurnos] = useState<Turno[]>([]);
  const [turnosFiltrados, setTurnosFiltrados] = useState<Turno[]>([]);

  const [mostrarCalendario, setMostrarCalendario] = useState(false);
  const [paciente, setPaciente] = useState<Paciente | null>(null);

  const navigate = useNavigate();

  // ------------------ BUSCAR PACIENTE ------------------
  const buscarPaciente = async () => {
    if (!dni) return;
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

    // El backend debería devolverte una agenda, pero vos me diste el endpoint tipo:
    // GET /profesionales/{profesional_id}/agenda/{agenda_id}/turnos
    // Para este ejemplo, voy a asumir agendaId = 1
    const agendaId = 1; // <- Cambialo cuando tengas el real

    const t = await turnoService.obtenerTurnosAgenda(idProfesional, agendaId);
    setTurnos(t);
    setMostrarCalendario(true);
  };

  // ------------------ FILTRAR TURNOS POR FECHA ------------------
  const filtrarTurnosPorDia = (fecha: Date) => {
    const dateStr = fecha.toISOString().split('T')[0];
    const t = turnos.filter((tu) => tu.fecha === dateStr);
    setTurnosFiltrados(t);
  };

  // ------------------ AGENDAR ------------------
  const agendar = async (turnoId: number) => {
    if (!paciente) return; // protección
    await turnoService.agendar(turnoId, paciente.dni);
    alert('Turno registrado con éxito');
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
            <button onClick={buscarTurnos}>Buscar</button>
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
              onClick={() => !t.dni_paciente && agendar(t.id)}
            >
              <span>
                {t.hora_inicio.substring(0, 5)} - {t.hora_fin.substring(0, 5)}
              </span>

              {t.dni_paciente && <strong>OCUPADO</strong>}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
