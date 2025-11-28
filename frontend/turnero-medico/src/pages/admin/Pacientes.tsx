import { useEffect, useState } from 'react';
import pacienteService from '../../service/pacienteService';
import { type Paciente } from '../../types/Paciente';
import styles from '../../styles/pages/paciente.module.css'; // reutilizamos estilos
import { useNavigate } from 'react-router-dom';
import Navbar from '@/components/ui/Navbar';
import AdminMenu from '@/components/menu/AdminMenu';
import pageStyles from '@/styles/pages/principal.module.css';
export default function Pacientes() {
    const [pacientes, setPacientes] = useState<Paciente[]>([]);
    const navigate = useNavigate();
    const [menuOpen, setMenuOpen] = useState(false);
    const openMenu = () => setMenuOpen(true);
    const closeMenu = () => setMenuOpen(false);
    // Cargar pacientes del backend
    const fetchPacientes = async () => {
        try {
            const res = await pacienteService.listar();
            console.log('DEVUELVE EL BACK:', res);

            setPacientes(res);
        } catch (error) {
            console.error('Error al cargar pacientes:', error);
        }
    };

    useEffect(() => {
        fetchPacientes();
    }, []);

    // Dar de baja (eliminar)
    const handleDelete = async (dni: number) => {
        if (!confirm('¿Seguro que desea eliminar este paciente?')) return;

        try {
            await pacienteService.eliminar(dni);
            fetchPacientes();
        } catch (error) {
            console.error('Error al eliminar paciente:', error);
        }
    };

    return (
        <div className={styles.container}>
            <Navbar title="" onMenuClick={openMenu} />
            {menuOpen && (
                <div className={pageStyles.overlay} onClick={closeMenu}></div>
            )}

            <AdminMenu isOpen={menuOpen} onClose={closeMenu} />
            <h1 className={styles.title}>Pacientes</h1>

            <button
                className={styles.addButton}
                onClick={() => navigate('/admin/RegistroPacientes')}
            >
                + Nuevo paciente
            </button>

            <table className={styles.table}>
                <thead>
                    <tr>
                        <th>DNI</th>
                        <th>Nombre completo</th>
                        <th>Obra social</th>
                        <th>Grupo sanguíneo</th>
                        <th>Email</th>
                        <th>Teléfono</th>
                        <th>Acciones</th>
                    </tr>
                </thead>

                <tbody>
                    {pacientes.map((p) => (
                        <tr key={p.dni}>
                            <td>{p.dni}</td>
                            <td>
                                {p.nombre} {p.apellido}
                            </td>
                            <td>{p.obra_social?.nombre ?? 'Sin obra social'}</td>
                            <td>{p.nombre_grupo_sanguineo}</td>
                            <td>{p.email}</td>
                            <td>{p.telefono}</td>

                            <td>
                                <button
                                    className={styles.editButton}
                                    onClick={() =>
                                        navigate(`/admin/RegistroPacientes?dni=${p.dni}`)
                                    }
                                >
                                    Editar
                                </button>

                                <button
                                    className={styles.deleteButton}
                                    onClick={() => handleDelete(p.dni)}
                                >
                                    Baja
                                </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}
