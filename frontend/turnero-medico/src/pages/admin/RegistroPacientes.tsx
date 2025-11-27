import { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import styles from '../../styles/pages/registroPacientes.module.css';

import obraSocialService from '../../service/obraSocialService';
import { AntecedenteService } from '../../service/antecedenteService';
import pacienteService from '../../service/pacienteService';

import { type ObraSocial } from '../../types/ObraSocial';
import { type Antecedente } from '../../types/Antecedente';
import {
  type PacienteCreate,
  type PacienteUpdate,
  type Paciente,
} from '../../types/Paciente';

export default function RegistroPacientes() {
  const navigate = useNavigate();
  const [params] = useSearchParams();
  const dniParam = params.get('dni'); // si existe → modo edición

  const [obrasSociales, setObrasSociales] = useState<ObraSocial[]>([]);
  const [antecedentes, setAntecedentes] = useState<Antecedente[]>([]);

  // Datos del formulario
  const [nombre, setNombre] = useState('');
  const [apellido, setApellido] = useState('');
  const [fechaNacimiento, setFechaNacimiento] = useState('');
  const [dni, setDni] = useState('');
  const [email, setEmail] = useState('');
  const [telefono, setTelefono] = useState('');
  const [obraSocial, setObraSocial] = useState<number | ''>('');
  const [grupoSanguineo, setGrupoSanguineo] = useState('');
  const [antecedente, setAntecedente] = useState<number | ''>('');

  const isEdit = Boolean(dniParam);

  // Cargar obras sociales y antecedentes
  useEffect(() => {
    const fetchData = async () => {
      const os = await obraSocialService.listar();
      const ant = await AntecedenteService.getAll();

      setObrasSociales(os);
      setAntecedentes(ant);
    };

    fetchData();
  }, []);

  // Si estamos en modo editar → cargar paciente
  useEffect(() => {
    if (!isEdit) return;

    const fetchPaciente = async () => {
      try {
        const paciente: Paciente = await pacienteService.obtener(
          Number(dniParam)
        );

        setNombre(paciente.nombre);
        setApellido(paciente.apellido);
        setFechaNacimiento(paciente.fecha_nacimiento);
        setDni(String(paciente.dni));
        setEmail(paciente.email);
        setTelefono(paciente.telefono);
        setObraSocial(paciente.obra_social ? Number(paciente.obra_social) : '');
        setGrupoSanguineo(String(paciente.grupo_sanguineo));
        setAntecedente(paciente.antecedentes?.[0]?.id ?? '');
      } catch (error) {
        console.error('Error cargando paciente', error);
        alert('No se pudo cargar el paciente.');
      }
    };

    fetchPaciente();
  }, [dniParam, isEdit]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const data: PacienteCreate | PacienteUpdate = {
      nombre,
      apellido,
      fecha_nacimiento: fechaNacimiento,
      dni: Number(dni),
      email,
      telefono,
      nombre_grupo_sanguineo: grupoSanguineo,
      nombre_obra_social: obraSocial
        ? obrasSociales.find((os) => os.id === obraSocial)?.nombre ?? null
        : null,
      ids_antecedentes: antecedente !== '' ? [Number(antecedente)] : [],
    };

    try {
      if (isEdit) {
        // EDITAR
        await pacienteService.actualizar(Number(dniParam), data);
      } else {
        // CREAR
        await pacienteService.crear(data as PacienteCreate);
      }

      navigate('/admin/pacientes');
    } catch (error) {
      console.error(error);
      alert('Error al guardar el paciente');
    }
  };

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>
        {isEdit ? 'Editar paciente' : 'Registrar paciente'}
      </h1>

      <form className={styles.form} onSubmit={handleSubmit}>
        <div className={styles.row}>
          <label>Nombre</label>
          <input
            type="text"
            value={nombre}
            onChange={(e) => setNombre(e.target.value)}
            required
          />
        </div>

        <div className={styles.row}>
          <label>Apellido</label>
          <input
            type="text"
            value={apellido}
            onChange={(e) => setApellido(e.target.value)}
            required
          />
        </div>

        <div className={styles.row}>
          <label>Fecha de nacimiento</label>
          <input
            type="date"
            value={fechaNacimiento}
            onChange={(e) => setFechaNacimiento(e.target.value)}
            required
          />
        </div>

        <div className={styles.row}>
          <label>DNI</label>
          <input
            type="number"
            value={dni}
            onChange={(e) => setDni(e.target.value)}
            required
            disabled={isEdit} // no se puede editar el DNI si ya existe
          />
        </div>

        <div className={styles.row}>
          <label>Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        <div className={styles.row}>
          <label>Teléfono</label>
          <input
            type="tel"
            value={telefono}
            onChange={(e) => setTelefono(e.target.value)}
            required
          />
        </div>

        <div className={styles.row}>
          <label>Obra social</label>
          <select
            value={obraSocial}
            onChange={(e) => setObraSocial(Number(e.target.value))}
            required
          >
            <option value="">Seleccione...</option>
            {obrasSociales.map((os) => (
              <option key={os.id} value={os.id}>
                {os.nombre}
              </option>
            ))}
          </select>
        </div>

        <div className={styles.row}>
          <label>Grupo sanguíneo</label>
          <select
            value={grupoSanguineo}
            onChange={(e) => setGrupoSanguineo(e.target.value)}
            required
          >
            <option value="">Seleccione...</option>
            <option value="A+">A+</option>
            <option value="A-">A-</option>
            <option value="B+">B+</option>
            <option value="B-">B-</option>
            <option value="AB+">AB+</option>
            <option value="AB-">AB-</option>
            <option value="O+">O+</option>
            <option value="O-">O-</option>
          </select>
        </div>

        <div className={styles.row}>
          <label>Antecedentes</label>
          <select
            value={antecedente}
            onChange={(e) => setAntecedente(Number(e.target.value))}
            required
          >
            <option value="">Seleccione...</option>
            {antecedentes.map((a) => (
              <option key={a.id} value={a.id}>
                {a.nombre}
              </option>
            ))}
          </select>
        </div>

        <div className={styles.buttons}>
          <button
            type="button"
            className={styles.cancel}
            onClick={() => navigate('/admin/pacientes')}
          >
            Cancelar
          </button>

          <button type="submit" className={styles.accept}>
            Aceptar
          </button>
        </div>
      </form>
    </div>
  );
}
