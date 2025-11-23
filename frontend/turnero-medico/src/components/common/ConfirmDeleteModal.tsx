import React from 'react';
import styles from '@/styles/components/confirmModal.module.css';

type Props = {
  message: string;
  onCancel: () => void;
  onConfirm: () => void;
};

export default function ConfirmDeleteModal({
  message,
  onCancel,
  onConfirm,
}: Props) {
  return (
    <div className={styles.overlay}>
      <div className={styles.box}>
        <p className={styles.message}>{message}</p>

        <div className={styles.buttonsRow}>
          <button className={styles.danger} onClick={onCancel}>
            Cancelar
          </button>
          <button className={styles.primary} onClick={onConfirm}>
            Aceptar
          </button>
        </div>
      </div>
    </div>
  );
}
