import { useEffect, useState } from 'react';
import styles from '../../styles/pages/obrasSociales.module.css';

import ObrasSocialesModal from '../../components/obrasSociales/ObrasSocialesModal';
import ConfirmDeleteModal from '../../components/common/ConfirmDeleteModal';

import obraSocialService from '../../service/obraSocialService';
import {
  type ObraSocial,
  type ObraSocialPayload,
  type TipoObraSocialEnum,
} from '../../types/ObraSocial';

export default function ObrasSociales() {
  const [obras, setObras] = useState<ObraSocial[]>([]);
  const [selected, setSelected] = useState<ObraSocial | null>(null);
  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
  const [deleteId, setDeleteId] = useState<number | null>(null);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // 🔹 Cargar desde el backend
  const fetchObras = async () => {
    try {
      setLoading(true);
      const data = await obraSocialService.listar();
      setObras(data);
    } catch (err: unknown) {
      setError('Error al cargar obras sociales');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchObras();
  }, []);

  const openCreate = () => {
    setSelected(null);
    setIsModalOpen(true);
  };

  const openEdit = (obra: ObraSocial) => {
    setSelected(obra);
    setIsModalOpen(true);
  };

  // 🔹 Crear o actualizar con backend
  const handleSave = async (data: ObraSocialPayload) => {
    try {
      if (selected) {
        // EDITAR
        const updated = await obraSocialService.actualizar(selected.id!, {
          nombre: data.nombre,
          cuit: data.cuit,
          porcentaje_cobertura: data.porcentaje_cobertura,
          nombre_tipo: data.nombre_tipo as TipoObraSocialEnum,
        });

        setObras((prev) =>
          prev.map((o) => (o.id === updated.id ? updated : o))
        );
      } else {
        // CREAR
        const created = await obraSocialService.crear({
          nombre: data.nombre!,
          cuit: data.cuit!,
          porcentaje_cobertura: data.porcentaje_cobertura!,
          nombre_tipo: data.nombre_tipo!,
        });

        setObras((prev) => [...prev, created]);
      }

      setIsModalOpen(false);
    } catch (err) {
      console.error(err);
      alert('Error al guardar la obra social');
    }
  };

  // 🔹 Eliminar — tu backend NO tiene DELETE, así que esto se deja listo
  const handleDelete = async () => {
    if (deleteId === null) return; // seguridad: no hacer nada si no hay ID
    setObras((prev) => prev.filter((o) => o.id !== deleteId));
    setDeleteId(null);

    // Si en el futuro agregás DELETE:
    // await obraSocialService.eliminar(deleteId!)
    // fetchObras()
  };

  if (loading) return <p>Cargando obras sociales...</p>;
  if (error) return <p className={styles.error}>{error}</p>;

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Obras Sociales</h1>

      <button className={styles.createButton} onClick={openCreate}>
        Nueva Obra Social
      </button>

      <table className={styles.table}>
        <thead>
          <tr>
            <th>CUIT</th>
            <th>Nombre</th>
            <th>Tipo</th>
            <th>Cobertura (%)</th>
            <th>Acciones</th>
          </tr>
        </thead>

        <tbody>
          {obras.map((obra) => (
            <tr key={obra.id}>
              <td>{obra.cuit}</td>
              <td>{obra.nombre}</td>
              <td>{obra.nombre_tipo}</td>
              <td>{obra.porcentaje_cobertura}%</td>

              <td>
                <button
                  className={styles.editButton}
                  onClick={() => openEdit(obra)}
                >
                  Editar
                </button>

                <button
                  className={styles.deleteButton}
                  onClick={() => setDeleteId(obra.id)}
                >
                  Eliminar
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {isModalOpen && (
        <ObrasSocialesModal
          onClose={() => setIsModalOpen(false)}
          onSave={handleSave}
          initialData={selected}
        />
      )}

      {deleteId !== null && (
        <ConfirmDeleteModal
          message="¿Estás seguro de que deseas eliminar esta obra social?"
          onCancel={() => setDeleteId(null)}
          onConfirm={handleDelete}
        />
      )}
    </div>
  );
}
