// src/components/consultas/FinalizarConsultaModal.tsx
import React, { useState, useEffect } from 'react';
import type { Turno } from '@/types/Turno';
import type { ConsultaCreate } from '@/types/Consulta';
import type { RecetaCreate } from '@/types/Receta';
import styles from '@/styles/components/modal.module.css';
import medicamentoService from '@/service/medicamentoService';

interface Props {
  turno: Turno;
  onClose: () => void;
  onFinalizado: (consultaData: ConsultaCreate) => void;
}

export default function FinalizarConsultaModal({
  turno,
  onClose,
  onFinalizado,
}: Props) {
  const [diagnostico, setDiagnostico] = useState('');
  const [observaciones, setObservaciones] = useState('');

  // Inicializamos receta con fecha actual y un detalle vacío
  const [receta, setReceta] = useState<RecetaCreate>({
    fecha: new Date().toISOString().slice(0, 10),
    detalles_receta: [
      {
        id_medicamento: 0,
        dosis: '',
        frecuencia: '',
        duracion_dias: 1,
        cantidad: 1,
        indicaciones: '',
      },
    ],
  });

  const [medicamentos, setMedicamentos] = useState<
    { id: number; nombre: string }[]
  >([]);

  // Cargar lista de medicamentos al abrir modal
  useEffect(() => {
    const load = async () => {
      try {
        const data = await medicamentoService.getAll();
        setMedicamentos(data);
      } catch (err) {
        console.error('Error cargando medicamentos:', err);
      }
    };
    load();
  }, []);

  const handleAgregarMedicamento = () => {
    setReceta((prev) => ({
      ...prev,
      detalles_receta: [
        ...prev.detalles_receta,
        {
          id_medicamento: 0,
          dosis: '',
          frecuencia: '',
          duracion_dias: 1,
          cantidad: 1,
          indicaciones: '',
        },
      ],
    }));
  };

  const handleCambiarDetalle = (
    index: number,
    campo: 'id_medicamento' | 'cantidad',
    valor: number
  ) => {
    setReceta((prev) => {
      const nuevosDetalles = [...prev.detalles_receta];
      nuevosDetalles[index][campo] = valor;
      return { ...prev, detalles_receta: nuevosDetalles };
    });
  };

  const handleFinalizar = () => {
    // Validar diagnóstico
    if (!diagnostico.trim()) {
      alert('El diagnóstico es obligatorio');
      return;
    }

    // Validar receta
    for (const detalle of receta.detalles_receta) {
      if (detalle.id_medicamento === 0 || detalle.cantidad <= 0) {
        alert(
          'Todos los medicamentos deben estar seleccionados con cantidad válida'
        );
        return;
      }
    }

    // Enviar datos completos
    onFinalizado({
      diagnostico,
      observaciones,
      receta,
      nombre_motivo_consulta: 'Consulta General', // o dejar que el backend lo complete
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
        {receta.detalles_receta.map((detalle, index) => (
          <div
            key={index}
            style={{ display: 'flex', gap: '8px', marginBottom: '8px' }}
          >
            <select
              value={detalle.id_medicamento}
              onChange={(e) =>
                handleCambiarDetalle(
                  index,
                  'id_medicamento',
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
              value={detalle.cantidad}
              onChange={(e) =>
                handleCambiarDetalle(index, 'cantidad', Number(e.target.value))
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
