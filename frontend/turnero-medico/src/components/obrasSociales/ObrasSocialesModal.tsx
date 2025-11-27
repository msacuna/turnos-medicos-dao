import { useState, useEffect, type FormEvent } from 'react';
import Modal from '../ui/Modal';
import inputStyles from '../../styles/components/input.module.css';
import buttonStyles from '../../styles/components/button.module.css';

import {
  type ObraSocialCreate,
  type ObraSocialUpdate,
  type ObraSocialPayload,
  type ObraSocial,
} from '../../types/ObraSocial';

interface Props {
  onClose: () => void;
  onSave: (data: ObraSocialPayload) => Promise<void>;

  initialData: ObraSocial | null;
}

export default function ObrasSocialesModal({
  onClose,
  onSave,
  initialData,
}: Props) {
  const [cuit, setCuit] = useState('');
  const [nombre, setNombre] = useState('');
  const [porcentajeCobertura, setPorcentajeCobertura] = useState<number>(0);
  const [nombreTipo, setNombreTipo] = useState<string>('GENERAL');

  const ES_EDIT = Boolean(initialData);

  useEffect(() => {
    if (initialData) {
      setCuit(initialData.cuit);
      setNombre(initialData.nombre);
      setPorcentajeCobertura(initialData.porcentaje_cobertura);
      setNombreTipo(initialData.nombre_tipo);
    }
  }, [initialData]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    const payload: ObraSocialCreate | ObraSocialUpdate = {
      cuit,
      nombre,
      porcentaje_cobertura: porcentajeCobertura,
      nombre_tipo: nombreTipo,
    };

    try {
      await onSave(payload); // el padre decide cuándo cerrar
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <Modal
      open={true}
      title={ES_EDIT ? 'Editar Obra Social' : 'Nueva Obra Social'}
      onClose={onClose}
    >
      <h2>{ES_EDIT ? 'Editar Obra Social' : 'Nueva Obra Social'}</h2>

      <form onSubmit={handleSubmit}>
        <label>CUIT</label>
        <input
          type="text"
          className={inputStyles.input}
          value={cuit}
          onChange={(e) => setCuit(e.target.value)}
          required
        />

        <label>Nombre</label>
        <input
          type="text"
          className={inputStyles.input}
          value={nombre}
          onChange={(e) => setNombre(e.target.value)}
          required
        />

        <label>Porcentaje de cobertura (%)</label>
        <input
          type="number"
          className={inputStyles.input}
          value={porcentajeCobertura}
          onChange={(e) => setPorcentajeCobertura(Number(e.target.value))}
          min={0}
          max={100}
          required
        />

        <label>Tipo de Obra Social</label>
        <select
          className={inputStyles.input}
          value={nombreTipo}
          onChange={(e) => setNombreTipo(e.target.value)}
          required
        >
          <option value="GENERAL">GENERAL</option>
          <option value="SINDICAL">SINDICAL</option>
          <option value="PREPAGA">PREPAGA</option>
          <option value="PARTICULAR">PARTICULAR</option>
        </select>

        <div className={buttonStyles.modalButtons}>
          <button
            type="button"
            className={buttonStyles.cancel}
            onClick={onClose}
          >
            Cancelar
          </button>

          <button type="submit" className={buttonStyles.save}>
            Guardar
          </button>
        </div>
      </form>
    </Modal>
  );
}
