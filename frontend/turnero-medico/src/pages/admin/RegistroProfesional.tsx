import { useEffect, useState } from 'react';
import styles from '../../styles/pages/registroProfesional.module.css';

import { EspecialidadService } from '../../service/especialidadService';
import type { Especialidad } from '../../types/Especialidad';

import type {
  Profesional,
  ProfesionalCreate,
  ProfesionalUpdate,
} from '../../types/Profesional';

interface Props {
  data?: Profesional | null;
  onClose?: () => void; // opcional
  onSave?: (
    payload: ProfesionalCreate | ProfesionalUpdate
  ) => Promise<void> | void; // opcional
}

export default function RegistroProfesional({ data, onClose, onSave }: Props) {
  const [especialidades, setEspecialidades] = useState<Especialidad[]>([]);

  // Datos del formulario
  const [nombre, setNombre] = useState('');
  const [apellido, setApellido] = useState('');
  const [matricula, setMatricula] = useState('');
  const [telefono, setTelefono] = useState('');
  const [email, setEmail] = useState('');
  const [id_especialidad, setIdEspecialidad] = useState<number | ''>('');

  // Cargar especialidades
  useEffect(() => {
    const fetchEspecialidades = async () => {
      try {
        const data = await EspecialidadService.getAll();
        setEspecialidades(data);
      } catch (error) {
        console.error('Error cargando especialidades:', error);
      }
    };

    fetchEspecialidades();
  }, []);

  useEffect(() => {
    if (data) {
      setNombre(data.nombre);
      setApellido(data.apellido);
      setMatricula(data.matricula);
      setTelefono(data.telefono);
      setEmail(data.email);
      setIdEspecialidad(data.id_especialidad);
    }
  }, [data]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (id_especialidad === '') {
      alert('Debe seleccionar una especialidad.');
      return;
    }

    const payload: ProfesionalCreate | ProfesionalUpdate = {
      ...(data?.id ? { id: data.id } : {}),
      nombre,
      apellido,
      matricula,
      telefono,
      email,
      id_especialidad: Number(id_especialidad),
    };

    if (onSave) onSave(payload); // solo llama si existe
  };

  return (
    <div className={styles.modalOverlay}>
      <div className={styles.modal}>
        <h1 className={styles.title}>
          {data ? 'Editar Profesional' : 'Registrar Profesional'}
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
            <label>Matrícula</label>
            <input
              type="text"
              value={matricula}
              onChange={(e) => setMatricula(e.target.value)}
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
            <label>Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className={styles.row}>
            <label>Especialidad</label>
            <select
              value={id_especialidad}
              onChange={(e) => setIdEspecialidad(Number(e.target.value))}
              required
            >
              <option value="">Seleccione...</option>
              {especialidades.map((esp) => (
                <option key={esp.id} value={esp.id}>
                  {esp.nombre}
                </option>
              ))}
            </select>
          </div>

          <div className={styles.buttons}>
            <button
              type="button"
              className={styles.cancel}
              onClick={onClose ? onClose : undefined}
            >
              Cancelar
            </button>

            <button type="submit" className={styles.accept}>
              Aceptar
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
