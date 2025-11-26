import { useState, useEffect } from 'react';
import type { FormEvent } from 'react';
import Modal from '../ui/Modal';
import inputStyles from '../../styles/components/input.module.css';
import buttonStyles from '../../styles/components/button.module.css';

interface ObraSocialData {
  cuit: string;
  nombre: string;
}

interface ObrasSocialesModalProps {
  onClose: () => void;
  onSave: (data: ObraSocialData) => void;
  initialData: ObraSocialData | null;
}

export default function ObrasSocialesModal({
  onClose,
  onSave,
  initialData,
}: ObrasSocialesModalProps) {
  const [cuit, setCuit] = useState<string>('');
  const [nombre, setNombre] = useState<string>('');

  useEffect(() => {
    if (initialData) {
      setCuit(initialData.cuit);
      setNombre(initialData.nombre);
    }
  }, [initialData]);

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    onSave({ cuit, nombre });
  };

  return (
    <Modal
      open={true}
      title={initialData ? 'Editar Obra social' : 'Nueva Obra Social'}
      onClose={onClose}
    >
      <h2>{initialData ? 'Editar Obra Social' : 'Nueva Obra Social'}</h2>

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
