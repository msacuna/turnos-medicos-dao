import { useEffect, useState } from 'react';
import styles from '../../styles/pages/antecedentes.module.css';
import AntecedentesModal from '../../components/antecedentes/AntecedentesModal';
import { type Antecedente, type AntecedentePayload } from '@/types/Antecedente';
import { AntecedenteService } from '@/service/antecedenteService';
import Navbar from '@/components/ui/Navbar';
import AdminMenu from '@/components/menu/AdminMenu';
import pageStyles from '@/styles/pages/principal.module.css';



export default function Antecedentes() {
    const [antecedentes, setAntecedentes] = useState<Antecedente[]>([]);
    const [selected, setSelected] = useState<Antecedente | null>(null);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [menuOpen, setMenuOpen] = useState(false);
    const openMenu = () => setMenuOpen(true);
    const closeMenu = () => setMenuOpen(false);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const data = await AntecedenteService.getAll();
                setAntecedentes(data);
            } catch (error) {
                console.error('Error al cargar antecedentes', error);
            }
        };

        fetchData();
    }, []);

    const handleCreate = () => {
        setSelected(null);
        setIsModalOpen(true);
    };

    const handleEdit = (item: Antecedente) => {
        setSelected(item);
        setIsModalOpen(true);
    };

    const handleDelete = async (id: number) => {
        try {
            await AntecedenteService.delete(id);

            setAntecedentes((prev) => prev.filter((a) => a.id !== id));
        } catch (error) {
            console.error('Error al eliminar antecedente', error);
        }
    };

    const handleSave = async (item: AntecedentePayload) => {
        try {
            if (item.id !== undefined) {
                // EDITAR
                const updated = await AntecedenteService.update(item.id, {
                    nombre: item.nombre,
                });

                setAntecedentes((prev) =>
                    prev.map((a) => (a.id === updated.id ? updated : a))
                );
            } else {
                // CREAR
                const created = await AntecedenteService.create({
                    nombre: item.nombre,
                });

                setAntecedentes((prev) => [...prev, created]);
            }

            setIsModalOpen(false);
        } catch (error) {
            console.error('Error al guardar el antecedente', error);
        }
    };

    return (
        <div className={styles.container}>
            <Navbar title="Antecedentes" onMenuClick={openMenu} />
            {menuOpen && (
                <div className={pageStyles.overlay} onClick={closeMenu}></div>
            )}

            <AdminMenu isOpen={menuOpen} onClose={closeMenu} />


            <button className={styles.createButton} onClick={handleCreate}>
                + Agregar Antecedente
            </button>

            <table className={styles.table}>
                <thead>
                    <tr>
                        <th>Nombre</th>
                        <th className={styles.actionsColumn}>Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    {antecedentes.map((item) => (
                        <tr key={item.id ?? item.nombre}>
                            <td>{item.nombre}</td>
                            <td className={styles.actions}>
                                <button
                                    className={styles.editButton}
                                    onClick={() => handleEdit(item)}
                                >
                                    Editar
                                </button>
                                <button
                                    className={styles.deleteButton}
                                    onClick={() => item.id !== undefined && handleDelete(item.id)}
                                >
                                    Eliminar
                                </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>

            {isModalOpen && (
                <AntecedentesModal
                    onClose={() => setIsModalOpen(false)}
                    onSave={handleSave}
                    data={selected}
                />
            )}
        </div>
    );
}
