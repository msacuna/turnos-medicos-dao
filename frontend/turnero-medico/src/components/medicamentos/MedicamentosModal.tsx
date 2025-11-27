import { useEffect, useState } from 'react';
import styles from '../../styles/pages/medicamentos.module.css';

import { type MedicamentoPayload } from '@/types/Medicamento';

type Props = {
  data: MedicamentoPayload | null;
  onClose: () => void;
  onSave: (item: MedicamentoPayload) => void;
};

export default function MedicamentosModal({ data, onClose, onSave }: Props) {
  const [nombre, setNombre] = useState('');
  const [descripcion, setDescripcion] = useState('');

  useEffect(() => {
    if (data) {
      setNombre(data.nombre);
      setDescripcion(data.descripcion ?? '');
    }
  }, [data]);

  const handleSubmit = () => {
    if (!nombre.trim()) return;

    onSave({
      id: data?.id,
      nombre,
      descripcion: descripcion.trim() || undefined,
    });
  };

  return (
    <div className={styles.modalBackdrop}>
      <div className={styles.modal}>
        <h2>{data ? 'Editar Medicamento' : 'Nuevo Medicamento'}</h2>

        <div className={styles.formGroup}>
          <label>Nombre</label>
          <input
            type="text"
            value={nombre}
            onChange={(e) => setNombre(e.target.value)}
          />
        </div>

        <div className={styles.formGroup}>
          <label>Descripción</label>
          <textarea
            value={descripcion}
            onChange={(e) => setDescripcion(e.target.value)}
          />
        </div>

        <div className={styles.buttons}>
          <button className={styles.saveButton} onClick={handleSubmit}>
            Guardar
          </button>
          <button className={styles.cancelButton} onClick={onClose}>
            Cancelar
          </button>
        </div>
      </div>
    </div>
  );
}
