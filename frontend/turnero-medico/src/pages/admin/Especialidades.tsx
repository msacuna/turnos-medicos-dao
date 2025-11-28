import React, { useEffect, useState } from 'react';
import Navbar from '@/components/ui/Navbar';
import AdminMenu from '@/components/menu/AdminMenu';
import EspecialidadesModal from '@/components/especialidades/EspecialidadesModal';
import ConfirmDeleteModal from '@/components/common/ConfirmDeleteModal';

import styles from '@/styles/pages/especialidades.module.css';
import pageStyles from '@/styles/pages/principal.module.css';

import { EspecialidadService } from '@/service/especialidadService';
import type {
    Especialidad,
    EspecialidadCreate,
    EspecialidadUpdate,
} from '@/types/Especialidad';

export default function Especialidades() {
    const [especialidades, setEspecialidades] = useState<Especialidad[]>([]);
    const [search, setSearch] = useState('');
    const [showModal, setShowModal] = useState(false);
    const [editing, setEditing] = useState<Especialidad | null>(null);
    const [deletingId, setDeletingId] = useState<number | null>(null);
    const [menuOpen, setMenuOpen] = useState(false);
    const [loading, setLoading] = useState(false);

    const openMenu = () => setMenuOpen(true);
    const closeMenu = () => setMenuOpen(false);

    /** 🔹 Cargar desde backend */
    const loadEspecialidades = async () => {
        try {
            setLoading(true);
            const data = await EspecialidadService.getAll();
            setEspecialidades(data);
        } catch (e) {
            console.error('Error cargando especialidades:', e);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadEspecialidades();
    }, []);

    /** 🔹 Abrir modal para crear */
    const handleCreate = () => {
        setEditing(null);
        setShowModal(true);
    };

    /** 🔹 Abrir modal para editar */
    const handleEdit = (esp: Especialidad) => {
        setEditing(esp);
        setShowModal(true);
    };

    /** 🔹 Guardar en backend (crear o editar) */
    const handleSave = async (nombre: string, precio: number) => {
        try {
            if (editing) {
                const updated = await EspecialidadService.update(editing.id, {
                    nombre,
                    precio,
                } as EspecialidadUpdate);

                setEspecialidades((prev) =>
                    prev.map((e) => (e.id === editing.id ? updated : e))
                );
            } else {
                const created = await EspecialidadService.create({
                    nombre,
                    precio,
                } as EspecialidadCreate);

                setEspecialidades((prev) => [...prev, created]);
            }

            setShowModal(false);
        } catch (e) {
            console.error('Error guardando especialidad:', e);
        }
    };

    /** 🔹 Confirmación de eliminar */
    const confirmDelete = async () => {
        if (!deletingId) return;

        try {
            await EspecialidadService.delete(deletingId);

            setEspecialidades((prev) => prev.filter((e) => e.id !== deletingId));

            setDeletingId(null);
        } catch (e) {
            console.error('Error eliminando especialidad:', e);
        }
    };

    return (
        <>
            <div className={styles.container}>

                <Navbar title="Especialidades" onMenuClick={openMenu} />
                {menuOpen && (
                    <div className={pageStyles.overlay} onClick={closeMenu}></div>
                )}

                <AdminMenu isOpen={menuOpen} onClose={closeMenu} />

                {/* 🔎 Buscador + botón agregar */}
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
                            <th>Nombre</th>
                            <th>Precio</th>
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
                                    <td>${esp.precio}</td>
                                    <td className={styles.actions}>
                                        {/* Editar */}
                                        <button
                                            className={styles.actionButton}
                                            onClick={() => handleEdit(esp)}
                                        >
                                            <svg
                                                xmlns="http://www.w3.org/2000/svg"
                                                height="24px"
                                                viewBox="0 -960 960 960"
                                                width="24px"
                                                fill="#e3e3e3"
                                            >
                                                <path d="M200-200h57l391-391-57-57-391 391v57Z" />
                                            </svg>
                                        </button>

                                        {/* Eliminar */}
                                        <button
                                            className={styles.actionButton}
                                            onClick={() => setDeletingId(esp.id)}
                                        >
                                            <svg
                                                xmlns="http://www.w3.org/2000/svg"
                                                height="24px"
                                                viewBox="0 -960 960 960"
                                                width="24px"
                                                fill="#e3e3e3"
                                            >
                                                <path d="M280-120q-33 0-56.5-23.5T200-200v-520h-40v-80h200v-40h240v40h200v80h-40v520q0 33-23.5 56.5T680-120H280Z" />
                                            </svg>
                                        </button>
                                    </td>
                                </tr>
                            ))}
                    </tbody>
                </table>

                {loading && <p>Cargando...</p>}
            </div>

            {/* Modal Crear/Editar */}
            {showModal && (
                <EspecialidadesModal
                    especialidad={editing}
                    onClose={() => setShowModal(false)}
                    onSave={handleSave}
                />
            )}

            {/* Confirmación de eliminar */}
            {deletingId !== null && (
                <ConfirmDeleteModal
                    message="¿Estás seguro que deseas eliminar esta especialidad?"
                    onCancel={() => setDeletingId(null)}
                    onConfirm={confirmDelete}
                />
            )}
        </>
    );
}
