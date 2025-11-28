import { useEffect, useState } from 'react';
import styles from '../../styles/pages/alergias.module.css';

import AlergiasModal from '../../components/alergias/AlergiasModal';
import ConfirmDeleteModal from '../../components/common/ConfirmDeleteModal';

import { AlergiaService } from '../../service/alergiaService';
import type {
  Alergia,
  AlergiaCreate,
  AlergiaUpdate,
} from '../../types/Alergia';

export default function Alergias() {
  const [alergias, setAlergias] = useState<Alergia[]>([]);
  const [selected, setSelected] = useState<Alergia | null>(null);
  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
  const [deleteId, setDeleteId] = useState<number | null>(null);

  // 🔹 Cargar alergias del backend
  const loadAlergias = async () => {
    try {
      const data = await AlergiaService.getAll();
      setAlergias(data);
    } catch (error) {
      console.error('Error cargando alergias:', error);
    }
  };

  useEffect(() => {
    loadAlergias();
  }, []);

  // 🔹 Abrir modal para crear
  const openCreate = () => {
    setSelected(null);
    setIsModalOpen(true);
  };

  // 🔹 Abrir modal para editar
  const openEdit = (item: Alergia) => {
    setSelected(item);
    setIsModalOpen(true);
  };

  // 🔹 Guardar (Crear o Editar)

  const handleSave = async (data: AlergiaCreate | AlergiaUpdate) => {
    try {
      if (selected) {
        // EDITAR
        await AlergiaService.update(selected.id, data);
      } else {
        // CREAR
        await AlergiaService.create(data);
      }

      await loadAlergias(); // Recargar lista
      setIsModalOpen(false); // Cerrar modal
      setSelected(null); // Resetear seleccionado
    } catch (error) {
      console.error('Error guardando alergia:', error);
    }
  };

  const handleDelete = async () => {
    try {
      if (!deleteId) return;

      await AlergiaService.delete(deleteId);

      setAlergias((prev) => prev.filter((e) => e.id !== deleteId));
      setDeleteId(null);
    } catch (error) {
      console.error('Error eliminando alergia:', error);
    }
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
          onClose={() => {
            setIsModalOpen(false);
            setSelected(null);
          }}
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
