// src/components/FinalizarConsultaModal.tsx
import React, { useState } from 'react';
import type { Turno } from '@/types/Turno';
import styles from '@/styles/components/modal.module.css';

interface Props {
  turno: Turno;
  onClose: () => void;
  onFinalizado: (consultaData: unknown) => void;
}

export default function FinalizarConsultaModal({
  turno,
  onClose,
  onFinalizado,
}: Props) {
  const [diagnostico, setDiagnostico] = useState('');
  const [observaciones, setObservaciones] = useState('');

  const handleFinalizar = () => {
    if (!diagnostico) {
      alert('El diagnóstico es obligatorio');
      return;
    }
    onFinalizado({ diagnostico, observaciones });
  };

  return (
    <div className={styles.modalOverlay}>
      <div className={styles.modalContent}>
        <h3>Finalizar Turno {turno.id}</h3>

        <label>
          Diagnóstico:
          <input
            type="text"
            value={diagnostico}
            onChange={(e) => setDiagnostico(e.target.value)}
          />
        </label>

        <label>
          Observaciones:
          <textarea
            value={observaciones}
            onChange={(e) => setObservaciones(e.target.value)}
          />
        </label>

        <div className={styles.modalActions}>
          <button onClick={handleFinalizar}>Finalizar</button>
          <button onClick={onClose}>Cancelar</button>
        </div>
      </div>
    </div>
  );
}
