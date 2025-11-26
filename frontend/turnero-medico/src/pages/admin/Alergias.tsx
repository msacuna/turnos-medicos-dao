import { useEffect, useState } from 'react';
import styles from '../../styles/pages/alergias.module.css';

import AlergiasModal from '../../components/alergias/AlergiasModal';
import ConfirmDeleteModal from '../../components/common/ConfirmDeleteModal';

interface Alergia {
  id: number;
  nombre: string;
}

export default function Alergias() {
  const [alergias, setAlergias] = useState<Alergia[]>([]);
  const [selected, setSelected] = useState<Alergia | null>(null);
  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
  const [deleteId, setDeleteId] = useState<number | null>(null);

  useEffect(() => {
    // Datos simulados – reemplazar con API real
    setAlergias([
      { id: 1, nombre: 'Polen' },
      { id: 2, nombre: 'Ácaros' },
      { id: 3, nombre: 'Penicilina' },
    ]);
  }, []);

  const openCreate = () => {
    setSelected(null);
    setIsModalOpen(true);
  };

  const openEdit = (item: Alergia) => {
    setSelected(item);
    setIsModalOpen(true);
  };

  const handleSave = (data: { nombre: string }) => {
    if (selected) {
      // Editar
      setAlergias((prev) =>
        prev.map((e) => (e.id === selected.id ? { ...e, ...data } : e))
      );
    } else {
      // Crear
      const newItem: Alergia = { id: Date.now(), ...data };
      setAlergias((prev) => [...prev, newItem]);
    }
    setIsModalOpen(false);
  };

  const handleDelete = () => {
    setAlergias((prev) => prev.filter((e) => e.id !== deleteId));
    setDeleteId(null);
  };

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Alergias</h1>

      <button className={styles.createButton} onClick={openCreate}>
        Nueva Alergia
      </button>

      <table className={styles.table}>
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Acciones</th>
          </tr>
        </thead>

        <tbody>
          {alergias.map((item) => (
            <tr key={item.id}>
              <td>{item.nombre}</td>

              <td>
                <button
                  className={styles.editButton}
                  onClick={() => openEdit(item)}
                >
                  Editar
                </button>

                <button
                  className={styles.deleteButton}
                  onClick={() => setDeleteId(item.id)}
                >
                  Eliminar
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {isModalOpen && (
        <AlergiasModal
          initialData={selected}
          onSave={handleSave}
          onClose={() => setIsModalOpen(false)}
        />
      )}

      {deleteId !== null && (
        <ConfirmDeleteModal
          message="¿Estás seguro de eliminar esta alergia?"
          onCancel={() => setDeleteId(null)}
          onConfirm={handleDelete}
        />
      )}
    </div>
  );
}
