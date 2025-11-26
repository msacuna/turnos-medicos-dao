import { useEffect, useState } from 'react';
import styles from '../../styles/pages/obrasSociales.module.css';
import ObrasSocialesModal from '../../components/obrasSociales/ObrasSocialesModal';
import ConfirmDeleteModal from '../../components/common/ConfirmDeleteModal';

interface ObraSocial {
  id: number;
  cuit: string;
  nombre: string;
}

export default function ObrasSociales() {
  const [obras, setObras] = useState<ObraSocial[]>([]);
  const [selected, setSelected] = useState<ObraSocial | null>(null);
  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
  const [deleteId, setDeleteId] = useState<number | null>(null);

  // Simulación — reemplazar por fetch a la API
  useEffect(() => {
    setObras([
      { id: 1, cuit: '30-12345678-9', nombre: 'OSDE' },
      { id: 2, cuit: '30-87654321-2', nombre: 'Swiss Medical' },
      { id: 3, cuit: '30-11112222-3', nombre: 'PAMI' },
    ]);
  }, []);

  const openCreate = () => {
    setSelected(null);
    setIsModalOpen(true);
  };

  const openEdit = (obra: ObraSocial) => {
    setSelected(obra);
    setIsModalOpen(true);
  };

  const handleSave = (data: { cuit: string; nombre: string }) => {
    if (selected) {
      // Editar
      setObras((prev) =>
        prev.map((o) => (o.id === selected.id ? { ...o, ...data } : o))
      );
    } else {
      // Crear
      const newItem: ObraSocial = {
        id: Date.now(),
        ...data,
      };
      setObras((prev) => [...prev, newItem]);
    }

    setIsModalOpen(false);
  };

  const handleDelete = () => {
    setObras((prev) => prev.filter((o) => o.id !== deleteId));
    setDeleteId(null);
  };

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Obras Sociales</h1>

      <button className={styles.createButton} onClick={openCreate}>
        Nueva Obra Social
      </button>

      <table className={styles.table}>
        <thead>
          <tr>
            <th>CUIT</th>
            <th>Nombre</th>
            <th>Acciones</th>
          </tr>
        </thead>

        <tbody>
          {obras.map((obra) => (
            <tr key={obra.id}>
              <td>{obra.cuit}</td>
              <td>{obra.nombre}</td>

              <td>
                <button
                  className={styles.editButton}
                  onClick={() => openEdit(obra)}
                >
                  Editar
                </button>

                <button
                  className={styles.deleteButton}
                  onClick={() => setDeleteId(obra.id)}
                >
                  Eliminar
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {isModalOpen && (
        <ObrasSocialesModal
          onClose={() => setIsModalOpen(false)}
          onSave={handleSave}
          initialData={selected}
        />
      )}

      {deleteId !== null && (
        <ConfirmDeleteModal
          message="¿Estás seguro de que deseas eliminar esta obra social?"
          onCancel={() => setDeleteId(null)}
          onConfirm={handleDelete}
        />
      )}
    </div>
  );
}
