// src/components/FinalizarConsultaModal.tsx
import React, { useState } from 'react';
import type { Turno } from '@/types/Turno';
import type { ConsultaCreate } from '@/types/Consulta'; // definí esta interfaz según tu backend
import styles from '@/styles/components/modal.module.css';
import medicamentoService from '@/service/medicamentoService';

interface Props {
  turno: Turno;
  onClose: () => void;
  onFinalizado: (consultaData: ConsultaCreate) => void;
}

interface RecetaItem {
  medicamentoId: number;
  cantidad: number;
}

export default function FinalizarConsultaModal({
  turno,
  onClose,
  onFinalizado,
}: Props) {
  const [diagnostico, setDiagnostico] = useState('');
  const [observaciones, setObservaciones] = useState('');
  const [receta, setReceta] = useState<RecetaItem[]>([
    { medicamentoId: 0, cantidad: 1 },
  ]);
  const [medicamentos, setMedicamentos] = useState<
    { id: number; nombre: string }[]
  >([]);

  // cargar medicamentos al abrir modal
  React.useEffect(() => {
    const load = async () => {
      const data = await medicamentoService.listar();
      setMedicamentos(data);
    };
    load();
  }, []);

  const handleAgregarMedicamento = () => {
    setReceta([...receta, { medicamentoId: 0, cantidad: 1 }]);
  };

  const handleCambiarMedicamento = (
    index: number,
    campo: 'medicamentoId' | 'cantidad',
    valor: number
  ) => {
    const nuevaReceta = [...receta];
    nuevaReceta[index][campo] = valor;
    setReceta(nuevaReceta);
  };

  const handleFinalizar = () => {
    if (!diagnostico) {
      alert('El diagnóstico es obligatorio');
      return;
    }

    // validar receta
    for (const item of receta) {
      if (item.medicamentoId === 0 || item.cantidad <= 0) {
        alert(
          'Todos los medicamentos deben estar seleccionados con cantidad válida'
        );
        return;
      }
    }

    onFinalizado({
      diagnostico,
      observaciones,
      receta,
    });
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

        <h4>Receta</h4>
        {receta.map((item, index) => (
          <div
            key={index}
            style={{ display: 'flex', gap: '8px', marginBottom: '8px' }}
          >
            <select
              value={item.medicamentoId}
              onChange={(e) =>
                handleCambiarMedicamento(
                  index,
                  'medicamentoId',
                  Number(e.target.value)
                )
              }
            >
              <option value={0}>Seleccionar medicamento</option>
              {medicamentos.map((m) => (
                <option key={m.id} value={m.id}>
                  {m.nombre}
                </option>
              ))}
            </select>

            <input
              type="number"
              min={1}
              value={item.cantidad}
              onChange={(e) =>
                handleCambiarMedicamento(
                  index,
                  'cantidad',
                  Number(e.target.value)
                )
              }
            />
          </div>
        ))}
        <button type="button" onClick={handleAgregarMedicamento}>
          Agregar medicamento
        </button>

        <div className={styles.modalActions} style={{ marginTop: '16px' }}>
          <button onClick={handleFinalizar}>Finalizar</button>
          <button onClick={onClose}>Cancelar</button>
        </div>
      </div>
    </div>
  );
}
