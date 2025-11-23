import React, { useState, useEffect } from 'react';
import styles from '@/styles/components/modal.module.css';

type Props = {
  especialidad: { id: number; nombre: string } | null;
  onClose: () => void;
  onSave: (nombre: string) => void;
};

export default function EspecialidadesModal({
  especialidad,
  onClose,
  onSave,
}: Props) {
  const [nombre, setNombre] = useState('');

  useEffect(() => {
    if (especialidad) setNombre(especialidad.nombre);
  }, [especialidad]);

  return (
    <div className={styles.backdrop} onClick={onClose}>
      <div
        className={styles.modal}
        onClick={(e) => e.stopPropagation()} // evita cerrar si hacés click dentro
      >
        <div className={styles.header}>
          <h3 className={styles.title}>
            {especialidad ? 'Editar Especialidad' : 'Nueva Especialidad'}
          </h3>
          <button className={styles.closeBtn} onClick={onClose}>
            ×
          </button>
        </div>

        <div className={styles.content}>
          <label className={styles.label}>Nombre</label>
          <input
            type="text"
            className={styles.input}
            value={nombre}
            onChange={(e) => setNombre(e.target.value)}
          />
        </div>

        <div className={styles.buttonsRow}>
          <button className={styles.danger} onClick={onClose}>
            Cancelar
          </button>
          <button className={styles.primary} onClick={() => onSave(nombre)}>
            Aceptar
          </button>
        </div>
      </div>
    </div>
  );
}
