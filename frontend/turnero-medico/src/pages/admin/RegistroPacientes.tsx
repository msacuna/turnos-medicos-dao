import { useEffect, useState } from 'react';
import styles from '../../styles/pages/registroPacientes.module.css';

import {
  obrasSocialesData,
  type ObraSocial,
} from '../../data/ObrasSocialesData';

import {
  antecedentesData,
  type Antecedente,
} from '../../data/antecedentesData';

export default function RegistroPacientes() {
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

  useEffect(() => {
    // Cargar datos desde los módulos
    setObrasSociales(obrasSocialesData);
    setAntecedentes(antecedentesData);
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const paciente = {
      nombre,
      apellido,
      fechaNacimiento,
      dni,
      email,
      telefono,
      obraSocial,
      grupoSanguineo,
      antecedente,
    };

    console.log('Paciente registrado:', paciente);
  };

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Registrar paciente</h1>

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
