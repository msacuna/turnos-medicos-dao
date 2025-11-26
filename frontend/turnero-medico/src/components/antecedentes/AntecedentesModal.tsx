import { useState, useEffect } from 'react';
import styles from '../../styles/pages/antecedentes.module.css';

type Antecedente = {
  id?: number;
  nombre: string;
};

type Props = {
  data: Antecedente | null;
  onClose: () => void;
  onSave: (item: Antecedente) => void;
};

export default function AntecedentesModal({ data, onClose, onSave }: Props) {
  const [nombre, setNombre] = useState('');

  useEffect(() => {
    if (data) {
      setNombre(data.nombre);
    }
  }, [data]);

  const handleSubmit = () => {
    if (!nombre.trim()) return;
    onSave({ id: data?.id, nombre });
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
