import { useEffect, useState } from 'react';
import styles from '../../styles/pages/antecedentes.module.css';
import AntecedentesModal from '../../components/antecedentes/AntecedentesModal';

type Antecedente = {
  id?: number;
  nombre: string;
};

export default function Antecedentes() {
  const [antecedentes, setAntecedentes] = useState<Antecedente[]>([]);
  const [selected, setSelected] = useState<Antecedente | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Simulación — reemplazar con API real
  useEffect(() => {
    setAntecedentes([
      { id: 1, nombre: 'Hipertensión' },
      { id: 2, nombre: 'Diabetes' },
    ]);
  }, []);

  const handleCreate = () => {
    setSelected(null);
    setIsModalOpen(true);
  };

  const handleEdit = (item: Antecedente) => {
    setSelected(item);
    setIsModalOpen(true);
  };

  const handleDelete = (id: number) => {
    setAntecedentes((prev) => prev.filter((a) => a.id !== id));
  };

  const handleSave = (item: Antecedente) => {
    if (item.id !== undefined) {
      setAntecedentes((prev) => prev.map((a) => (a.id === item.id ? item : a)));
    } else {
      const newId = Math.max(...antecedentes.map((a) => a.id ?? 0), 0) + 1;
      setAntecedentes((prev) => [...prev, { ...item, id: newId }]);
    }
    setIsModalOpen(false);
  };

  return (
    <div className={styles.container}>
      <h1>Antecedentes</h1>

      <button className={styles.createButton} onClick={handleCreate}>
        + Agregar Antecedente
      </button>

      <table className={styles.table}>
        <thead>
          <tr>
            <th>Nombre</th>
            <th className={styles.actionsColumn}>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {antecedentes.map((item) => (
            <tr key={item.id ?? item.nombre}>
              <td>{item.nombre}</td>
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
        <AntecedentesModal
          onClose={() => setIsModalOpen(false)}
          onSave={handleSave}
          data={selected}
        />
      )}
    </div>
  );
}
