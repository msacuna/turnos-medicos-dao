import { useEffect, useState } from 'react';
import styles from '@/styles/pages/tabla.module.css';

import {
  type Profesional,
  type ProfesionalCreate,
  type ProfesionalUpdate,
} from '@/types/Profesional';
import {
  obtenerProfesionales,
  crearProfesional,
  actualizarProfesional,
  eliminarProfesional,
} from '@/service/profesionalService';

import RegistroProfesional from '@/pages/admin/RegistroProfesional';

export default function ProfesionalPage() {
  const [profesionales, setProfesionales] = useState<Profesional[]>([]);
  const [modalOpen, setModalOpen] = useState(false);
  const [selected, setSelected] = useState<Profesional | null>(null);

  // Cargar lista al iniciar
  const fetchData = async () => {
    const data = await obtenerProfesionales();
    setProfesionales(data);
  };

  useEffect(() => {
    fetchData();
  }, []);

  // Abrir modal para crear
  const handleCreate = () => {
    setSelected(null);
    setModalOpen(true);
  };

  // Abrir modal para editar
  const handleEdit = (item: Profesional) => {
    setSelected(item);
    setModalOpen(true);
  };

  // Guardar (crear o actualizar)
  const handleSave = async (payload: ProfesionalCreate | ProfesionalUpdate) => {
    if ('id' in payload) {
      await actualizarProfesional(payload);
    } else {
      await crearProfesional(payload);
    }

    setModalOpen(false);
    await fetchData();
  };

  // Eliminar
  const handleDelete = async (id: number) => {
    if (!confirm('¿Seguro que querés eliminar este profesional?')) return;
    await eliminarProfesional(id);
    await fetchData();
  };

  return (
    <div className={styles.container}>
      <h1>Profesionales</h1>

      <button className={styles.createButton} onClick={handleCreate}>
        + Nuevo Profesional
      </button>

      <table className={styles.table}>
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Apellido</th>
            <th>Matrícula</th>
            <th>Email</th>
            <th>Teléfono</th>
            <th>Especialidad</th>
            <th>Acciones</th>
          </tr>
        </thead>

        <tbody>
          {profesionales.map((p) => (
            <tr key={p.id}>
              <td>{p.nombre}</td>
              <td>{p.apellido}</td>
              <td>{p.matricula}</td>
              <td>{p.email}</td>
              <td>{p.telefono}</td>
              <td>{p.id_especialidad}</td>
              <td>
                <button
                  className={styles.editButton}
                  onClick={() => handleEdit(p)}
                >
                  Editar
                </button>

                <button
                  className={styles.deleteButton}
                  onClick={() => handleDelete(p.id)}
                >
                  Eliminar
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {modalOpen && (
        <RegistroProfesional
          data={selected}
          onClose={() => setModalOpen(false)}
          onSave={handleSave}
        />
      )}
    </div>
  );
}
