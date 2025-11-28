// src/components/consultas/FinalizarConsultaModal.tsx
import React, { useState, useEffect } from 'react';
import type { Turno } from '@/types/Turno';
import type { ConsultaCreate } from '@/types/Consulta';
import type { RecetaCreate } from '@/types/Receta';
import Modal from '@/components/ui/Modal';
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

    const handleEliminarMedicamento = (index: number) => {
        setReceta((prev) => ({
            ...prev,
            detalles_receta: prev.detalles_receta.filter((_, i) => i !== index),
        }));
    };

    const handleCambiarDetalle = (
        index: number,
        campo: keyof RecetaCreate['detalles_receta'][0],
        valor: number | string
    ) => {
        setReceta((prev) => {
            const nuevosDetalles = [...prev.detalles_receta];
            const detalle = nuevosDetalles[index];

            if (campo === 'id_medicamento' || campo === 'cantidad' || campo === 'duracion_dias') {
                (detalle[campo] as number) = valor as number;
            } else {
                (detalle[campo] as string) = valor as string;
            }

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
            nombre_motivo_consulta: 'Consulta General',
        });
    };

    return (
        <Modal open={true} onClose={onClose} title={`Finalizar Turno #${turno.id}`}>
            {/* Diagnóstico */}
            <div style={{ marginBottom: '20px' }}>
                <label className={styles.label}>
                    Diagnóstico <span style={{ color: 'red' }}>*</span>
                </label>
                <input
                    type="text"
                    className={styles.input}
                    value={diagnostico}
                    onChange={(e) => setDiagnostico(e.target.value)}
                    placeholder="Ingrese el diagnóstico"
                />
            </div>

            {/* Observaciones */}
            <div style={{ marginBottom: '20px' }}>
                <label className={styles.label}>Observaciones</label>
                <textarea
                    className={styles.input}
                    value={observaciones}
                    onChange={(e) => setObservaciones(e.target.value)}
                    placeholder="Observaciones adicionales (opcional)"
                    rows={3}
                    style={{ resize: 'vertical' }}
                />
            </div>

            {/* Receta */}
            <div style={{ marginBottom: '20px' }}>
                <label className={styles.label}>Receta Médica</label>

                {receta.detalles_receta.map((detalle, index) => (
                    <div
                        key={index}
                        style={{
                            padding: '12px',
                            border: '1px solid #e0e0e0',
                            borderRadius: '8px',
                            marginBottom: '12px',
                            backgroundColor: '#f9f9f9',
                        }}
                    >
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                            <strong>Medicamento #{index + 1}</strong>
                            {receta.detalles_receta.length > 1 && (
                                <button
                                    type="button"
                                    onClick={() => handleEliminarMedicamento(index)}
                                    style={{
                                        background: '#ff4444',
                                        color: 'white',
                                        border: 'none',
                                        borderRadius: '4px',
                                        padding: '4px 8px',
                                        cursor: 'pointer',
                                        fontSize: '12px',
                                    }}
                                >
                                    Eliminar
                                </button>
                            )}
                        </div>

                        {/* Selector de medicamento */}
                        <select
                            className={styles.input}
                            value={detalle.id_medicamento}
                            onChange={(e) =>
                                handleCambiarDetalle(
                                    index,
                                    'id_medicamento',
                                    Number(e.target.value)
                                )
                            }
                            style={{ marginBottom: '8px' }}
                        >
                            <option value={0}>Seleccionar medicamento</option>
                            {medicamentos.map((m) => (
                                <option key={m.id} value={m.id}>
                                    {m.nombre}
                                </option>
                            ))}
                        </select>

                        {/* Cantidad y Dosis */}
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px', marginBottom: '8px' }}>
                            <div>
                                <label style={{ fontSize: '13px', color: '#555' }}>Cantidad</label>
                                <input
                                    type="number"
                                    className={styles.input}
                                    min={1}
                                    value={detalle.cantidad}
                                    onChange={(e) =>
                                        handleCambiarDetalle(index, 'cantidad', Number(e.target.value))
                                    }
                                    style={{ marginTop: '4px' }}
                                />
                            </div>
                            <div>
                                <label style={{ fontSize: '13px', color: '#555' }}>Dosis</label>
                                <input
                                    type="text"
                                    className={styles.input}
                                    value={detalle.dosis}
                                    onChange={(e) =>
                                        handleCambiarDetalle(index, 'dosis', e.target.value)
                                    }
                                    placeholder="ej: 500mg"
                                    style={{ marginTop: '4px' }}
                                />
                            </div>
                        </div>

                        {/* Frecuencia y Duración */}
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px', marginBottom: '8px' }}>
                            <div>
                                <label style={{ fontSize: '13px', color: '#555' }}>Frecuencia</label>
                                <input
                                    type="text"
                                    className={styles.input}
                                    value={detalle.frecuencia}
                                    onChange={(e) =>
                                        handleCambiarDetalle(index, 'frecuencia', e.target.value)
                                    }
                                    placeholder="ej: Cada 8 horas"
                                    style={{ marginTop: '4px' }}
                                />
                            </div>
                            <div>
                                <label style={{ fontSize: '13px', color: '#555' }}>Duración (días)</label>
                                <input
                                    type="number"
                                    className={styles.input}
                                    min={1}
                                    value={detalle.duracion_dias}
                                    onChange={(e) =>
                                        handleCambiarDetalle(index, 'duracion_dias', Number(e.target.value))
                                    }
                                    style={{ marginTop: '4px' }}
                                />
                            </div>
                        </div>

                        {/* Indicaciones */}
                        <div>
                            <label style={{ fontSize: '13px', color: '#555' }}>Indicaciones</label>
                            <textarea
                                className={styles.input}
                                value={detalle.indicaciones}
                                onChange={(e) =>
                                    handleCambiarDetalle(index, 'indicaciones', e.target.value)
                                }
                                placeholder="Indicaciones especiales"
                                rows={2}
                                style={{ marginTop: '4px', resize: 'vertical' }}
                            />
                        </div>
                    </div>
                ))}

                <button
                    type="button"
                    onClick={handleAgregarMedicamento}
                    style={{
                        width: '100%',
                        padding: '10px',
                        background: '#4CAF50',
                        color: 'white',
                        border: 'none',
                        borderRadius: '8px',
                        cursor: 'pointer',
                        fontSize: '14px',
                        fontWeight: '600',
                    }}
                >
                    + Agregar otro medicamento
                </button>
            </div>

            {/* Footer con botones */}
            <div className={styles.buttonsRow}>
                <button className={styles.danger} onClick={onClose}>
                    Cancelar
                </button>
                <button className={styles.primary} onClick={handleFinalizar}>
                    Finalizar Consulta
                </button>
            </div>
        </Modal>
    );
}