import { useState, useEffect } from 'react';
import styles from '../../styles/pages/antecedentes.module.css';
import { type Antecedente, type AntecedentePayload } from '@/types/Antecedente';

type Props = {
  data: Antecedente | null;
  onClose: () => void;
  onSave: (item: AntecedentePayload) => void;
};

export default function AntecedentesModal({ data, onClose, onSave }: Props) {
  const [nombre, setNombre] = useState('');

  useEffect(() => {
    if (data) {
      setNombre(data.nombre);
    } else {
      setNombre('');
    }
  }, [data]);

  const handleSubmit = () => {
    const trimmed = nombre.trim();
    if (!trimmed) return;

    // Evitar guardar si no hubo cambios
    if (data && data.nombre === trimmed) {
      onClose();
      return;
    }

    onSave({ id: data?.id, nombre: trimmed });
    onClose();
  };

  return (
    <div className={styles.modalBackdrop}>
      <div className={styles.modal}>
        <h2>{data ? 'Editar Antecedente' : 'Nuevo Antecedente'}</h2>

        <div className={styles.formGroup}>
          <label>Nombre</label>
          <input
            type="text"
            value={nombre}
            onChange={(e) => setNombre(e.target.value)}
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
