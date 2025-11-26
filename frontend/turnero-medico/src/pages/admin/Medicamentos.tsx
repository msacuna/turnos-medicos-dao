import { useEffect, useState } from 'react';
import styles from '../../styles/pages/medicamentos.module.css';
import MedicamentosModal from '../../components/medicamentos/MedicamentosModal';

type Medicamento = {
  id?: number;
  nombre: string;
  descripcion: string;
};

export default function Medicamentos() {
  const [medicamentos, setMedicamentos] = useState<Medicamento[]>([]);
  const [selected, setSelected] = useState<Medicamento | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Simulación de carga inicial — luego reemplazar con API real
  useEffect(() => {
    setMedicamentos([
      { id: 1, nombre: 'Ibuprofeno', descripcion: 'Antiinflamatorio' },
      {
        id: 2,
        nombre: 'Paracetamol',
        descripcion: 'Analgésico y antipirético',
      },
    ]);
  }, []);

  const handleCreate = () => {
    setSelected(null);
    setIsModalOpen(true);
  };

  const handleEdit = (item: Medicamento) => {
    setSelected(item);
    setIsModalOpen(true);
  };

  const handleDelete = (id: number) => {
    setMedicamentos((prev) => prev.filter((m) => m.id !== id));
  };

  const handleSave = (item: Medicamento) => {
    if (item.id !== undefined) {
      // Editar
      setMedicamentos((prev) => prev.map((m) => (m.id === item.id ? item : m)));
    } else {
      // Crear
      const newId = Math.max(...medicamentos.map((m) => m.id ?? 0), 0) + 1;

      setMedicamentos((prev) => [...prev, { ...item, id: newId }]);
    }
    setIsModalOpen(false);
  };

  return (
    <div className={styles.container}>
      <h1>Medicamentos</h1>

      <button className={styles.createButton} onClick={handleCreate}>
        + Agregar Medicamento
      </button>

      <table className={styles.table}>
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Descripción</th>
            <th className={styles.actionsColumn}>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {medicamentos.map((item) => (
            <tr key={item.id ?? item.nombre}>
              <td>{item.nombre}</td>
              <td>{item.descripcion}</td>
              <td className={styles.actions}>
                <button
                  className={styles.editButton}
                  onClick={() => handleEdit(item)}
                >
                  Editar
                </button>
                <button
                  className={styles.deleteButton}
                  onClick={() => item.id !== undefined && handleDelete(item.id)}
                >
                  Eliminar
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {isModalOpen && (
        <MedicamentosModal
          onClose={() => setIsModalOpen(false)}
          onSave={handleSave}
          data={selected}
        />
      )}
    </div>
  );
}
