// src/pages/medicamentos/Medicamentos.tsx

import { useEffect, useState } from 'react';
import styles from '../../styles/pages/medicamentos.module.css';
import MedicamentosModal from '../../components/medicamentos/MedicamentosModal';

import { type Medicamento, type MedicamentoPayload } from '@/types/Medicamento';

import { MedicamentoService } from '@/service/medicamentoService';
import Navbar from '@/components/ui/Navbar';
import AdminMenu from '@/components/menu/AdminMenu';
import pageStyles from '@/styles/pages/principal.module.css';



export default function Medicamentos() {
    const [medicamentos, setMedicamentos] = useState<Medicamento[]>([]);
    const [selected, setSelected] = useState<Medicamento | null>(null);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [menuOpen, setMenuOpen] = useState(false);
    const openMenu = () => setMenuOpen(true);
    const closeMenu = () => setMenuOpen(false);
    // 🔹 Obtener lista inicial
    useEffect(() => {
        const fetchData = async () => {
            try {
                const data = await MedicamentoService.getAll();
                setMedicamentos(data);
            } catch (error) {
                console.error('Error cargando medicamentos:', error);
            }
        };

        fetchData();
    }, []);

    const handleCreate = () => {
        setSelected(null);
        setIsModalOpen(true);
    };

    const handleEdit = (item: Medicamento) => {
        setSelected(item);
        setIsModalOpen(true);
    };

    const handleDelete = async (id: number) => {
        try {
            await MedicamentoService.delete(id);
            setMedicamentos((prev) => prev.filter((m) => m.id !== id));
        } catch (error) {
            console.error('Error eliminando medicamento:', error);
        }
    };

    const handleSave = async (item: MedicamentoPayload) => {
        try {
            if (item.id !== undefined) {
                // 🔹 EDITAR
                const updated = await MedicamentoService.update(item.id, {
                    nombre: item.nombre,
                    descripcion: item.descripcion,
                    ids_laboratorios: item.ids_laboratorios,
                });

                setMedicamentos((prev) =>
                    prev.map((m) => (m.id === updated.id ? updated : m))
                );
            } else {
                // 🔹 CREAR
                const created = await MedicamentoService.create({
                    nombre: item.nombre,
                    descripcion: item.descripcion,
                    ids_laboratorios: item.ids_laboratorios ?? [],
                });

                setMedicamentos((prev) => [...prev, created]);
            }
        } catch (error) {
            console.error('Error guardando medicamento:', error);
        }

        setIsModalOpen(false);
    };

    return (
        <div className={styles.container}>
            <Navbar title="Medicamentos" onMenuClick={openMenu} />
            {menuOpen && (
                <div className={pageStyles.overlay} onClick={closeMenu}></div>
            )}

            <AdminMenu isOpen={menuOpen} onClose={closeMenu} />


            <button className={styles.createButton} onClick={handleCreate}>
                + Agregar Medicamento
            </button>

            <table className={styles.table}>
                <thead>
                    <tr>
                        <th>Nombre</th>
                        <th>Descripción</th>
                        <th className={styles.actionsColumn}>Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    {medicamentos.map((item) => (
                        <tr key={item.id}>
                            <td>{item.nombre}</td>
                            <td>{item.descripcion}</td>
                            <td className={styles.actions}>
                                <button
                                    className={styles.editButton}
                                    onClick={() => handleEdit(item)}
                                >
                                    Editar
                                </button>

                                <button
                                    className={styles.deleteButton}
                                    onClick={() => handleDelete(item.id)}
                                >
                                    Eliminar
                                </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>

            {isModalOpen && (
                <MedicamentosModal
                    onClose={() => setIsModalOpen(false)}
                    onSave={handleSave}
                    data={
                        selected
                            ? {
                                ...selected,
                                descripcion: selected.descripcion || '',
                                ids_laboratorios:
                                    selected.laboratorios?.map((l) => l.id) ?? [],
                            }
                            : null
                    }
                />
            )}
        </div>
    );
}
