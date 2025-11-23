import React from 'react';
import styles from '../styles/components/modal.module.css';

type ModalProps = {
  open: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
};

export default function Modal({ open, onClose, title, children }: ModalProps) {
  if (!open) return null;

  return (
    <div className={styles.backdrop} onClick={onClose}>
      <div
        className={styles.modal}
        onClick={(e) => e.stopPropagation()} // evita que cierre al tocar adentro
      >
        {/* Navbar */}
        <div className={styles.header}>
          <h2 className={styles.title}>{title}</h2>

          <button className={styles.closeBtn} onClick={onClose}>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              height="26px"
              viewBox="0 -960 960 960"
              width="26px"
              fill="black"
            >
              <path d="m256-200-56-57 224-223-224-224 56-56 224 224 224-224 56 56-224 224 224 223-56 57-224-224-224 224Z" />
            </svg>
          </button>
        </div>

        <div className={styles.content}>{children}</div>
      </div>
    </div>
  );
}
