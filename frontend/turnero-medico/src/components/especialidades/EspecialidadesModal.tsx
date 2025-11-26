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
            <svg
              xmlns="http://www.w3.org/2000/svg"
              height="24px"
              viewBox="0 -960 960 960"
              width="24px"
              fill="#000000"
            >
              <path d="m256-200-56-56 224-224-224-224 56-56 224 224 224-224 56 56-224 224 224 224-56 56-224-224-224 224Z" />
            </svg>
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
