import { useState, useEffect } from 'react';
import Modal from '../ui/Modal';

interface AlergiasModalProps {
  initialData?: { nombre: string } | null;
  onSave: (data: { nombre: string }) => void;
  onClose: () => void;
}

export default function AlergiasModal({
  initialData,
  onSave,
  onClose,
}: AlergiasModalProps) {
  const [nombre, setNombre] = useState(initialData?.nombre || '');

  useEffect(() => {
    setNombre(initialData?.nombre || '');
  }, [initialData]);

  const handleSubmit = () => {
    if (!nombre.trim()) return;
    if (initialData && initialData.nombre === nombre.trim()) {
      onClose();
      return;
    }
    onSave({ nombre: nombre.trim() });
  };

  return (
    <Modal
      open={true}
      title={initialData ? 'Editar Alergia' : 'Nueva Alergia'}
      onClose={onClose}
    >
      <div>
        <label>Nombre</label>
        <input
          type="text"
          value={nombre}
          onChange={(e) => setNombre(e.target.value)}
          style={{ width: '100%', padding: '8px', marginTop: '4px' }}
        />
      </div>

      <div
        style={{
          marginTop: '20px',
          display: 'flex',
          justifyContent: 'flex-end',
          gap: '10px',
        }}
      >
        <button onClick={onClose} className="btn-cancel">
          Cancelar
        </button>
        <button onClick={handleSubmit} className="btn-save">
          Guardar
        </button>
      </div>
    </Modal>
  );
}
