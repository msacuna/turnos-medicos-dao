import { useEffect, useState } from 'react';
import styles from '../../styles/pages/registroProfesional.module.css';

import {
  especialidadesData,
  type Especialidad,
} from '../../data/especialidadesData';

export default function RegistroProfesional() {
  const [especialidades, setEspecialidades] = useState<Especialidad[]>([]);

  // Datos del formulario
  const [nombre, setNombre] = useState('');
  const [apellido, setApellido] = useState('');
  const [matricula, setMatricula] = useState('');
  const [telefono, setTelefono] = useState('');
  const [email, setEmail] = useState('');
  const [especialidad, setEspecialidad] = useState<number | ''>('');

  useEffect(() => {
    setEspecialidades(especialidadesData);
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const profesional = {
      nombre,
      apellido,
      matricula,
      telefono,
      email,
      especialidad,
    };

    console.log('Profesional registrado:', profesional);
  };

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Registrar profesional</h1>

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
            value={especialidad}
            onChange={(e) => setEspecialidad(Number(e.target.value))}
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
            onClick={() => window.history.back()}
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
