import React, { useEffect, useState } from 'react';
import Navbar from '@/components/ui/Navbar';
import AdminMenu from '@/components/menu/AdminMenu';
import EspecialidadesModal from '@/components/especialidades/EspecialidadesModal';
import ConfirmDeleteModal from '@/components/common/ConfirmDeleteModal';
import styles from '@/styles/pages/especialidades.module.css';
import pageStyles from '@/styles/pages/principal.module.css';

type Especialidad = {
  id: number;
  nombre: string;
};

export default function Especialidades() {
  const [especialidades, setEspecialidades] = useState<Especialidad[]>([]);
  const [search, setSearch] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);
  const [editing, setEditing] = useState<Especialidad | null>(null);
  const [deletingId, setDeletingId] = useState<number | null>(null);
  const [menuOpen, setMenuOpen] = useState(false);

  const openMenu = () => setMenuOpen(true);
  const closeMenu = () => setMenuOpen(false);

  /** Obtener lista inicial */
  useEffect(() => {
    fetchEspecialidades();
  }, []);

  const fetchEspecialidades = async () => {
    // 🚨 Cuando tengas los endpoints, reemplazo esto por fetch real
    setEspecialidades([
      { id: 1, nombre: 'Cardiología' },
      { id: 2, nombre: 'Dermatología' },
    ]);
  };

  /** Abrir modal para crear */
  const handleCreate = () => {
    setEditing(null);
    setShowModal(true);
  };

  /** Abrir modal para editar */
  const handleEdit = (esp: Especialidad) => {
    setEditing(esp);
    setShowModal(true);
  };

  /** Abrir confirmación de eliminar */
  const handleDelete = (id: number) => {
    setDeletingId(id);
    setShowConfirm(true);
  };

  /** Confirmar eliminación */
  const confirmDelete = () => {
    if (deletingId !== null) {
      setEspecialidades((prev) => prev.filter((e) => e.id !== deletingId));
    }
    setShowConfirm(false);
  };

  return (
    <>
      <Navbar title="Especialidades" onMenuClick={openMenu} />
      {menuOpen && (
        <div className={pageStyles.overlay} onClick={closeMenu}></div>
      )}

      <AdminMenu isOpen={menuOpen} onClose={closeMenu} />

      <div className={styles.container}>
        {/* Buscador + botón agregar */}
        <div className={styles.headerRow}>
          <input
            type="text"
            className={styles.searchInput}
            placeholder="Buscar especialidad..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />

          <button className={styles.addButton} onClick={handleCreate}>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              height="24px"
              viewBox="0 -960 960 960"
              width="24px"
              fill="#e3e3e3"
            >
              <path d="M440-440H200v-80h240v-240h80v240h240v80H520v240h-80v-240Z" />
            </svg>
          </button>
        </div>

        {/* Tabla */}
        <table className={styles.table}>
          <thead>
            <tr>
              <th>Especialidades</th>
              <th>Acciones</th>
            </tr>
          </thead>

          <tbody>
            {especialidades
              .filter((e) =>
                e.nombre.toLowerCase().includes(search.toLowerCase())
              )
              .map((esp) => (
                <tr key={esp.id}>
                  <td>{esp.nombre}</td>
                  <td className={styles.actions}>
                    <button
                      className={styles.actionButton}
                      onClick={() => handleEdit(esp)}
                    >
                      {/* Editar */}
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        height="24px"
                        viewBox="0 -960 960 960"
                        width="24px"
                        fill="#e3e3e3"
                      >
                        <path d="M200-200h57l391-391-57-57-391 391v57Z..." />
                      </svg>
                    </button>

                    <button
                      className={styles.actionButton}
                      onClick={() => handleDelete(esp.id)}
                    >
                      {/* Eliminar */}
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        height="24px"
                        viewBox="0 -960 960 960"
                        width="24px"
                        fill="#e3e3e3"
                      >
                        <path d="M280-120q-33 0-56.5-23.5T200-200v-520..." />
                      </svg>
                    </button>
                  </td>
                </tr>
              ))}
          </tbody>
        </table>
      </div>

      {/* Modal Crear/Editar */}
      {showModal && (
        <EspecialidadesModal
          especialidad={editing}
          onClose={() => setShowModal(false)}
          onSave={(nombre) => {
            if (editing) {
              setEspecialidades((prev) =>
                prev.map((e) => (e.id === editing.id ? { ...e, nombre } : e))
              );
            } else {
              setEspecialidades((prev) => [
                ...prev,
                { id: prev.length + 1, nombre },
              ]);
            }
            setShowModal(false);
          }}
        />
      )}

      {/* Confirmación de eliminar */}
      {showConfirm && (
        <ConfirmDeleteModal
          message="¿Estás seguro que deseas dar de baja esta especialidad?"
          onCancel={() => setShowConfirm(false)}
          onConfirm={confirmDelete}
        />
      )}
    </>
  );
}
