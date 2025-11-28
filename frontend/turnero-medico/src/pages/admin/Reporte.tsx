import { useEffect, useState } from 'react';
import Navbar from '@/components/ui/Navbar';
import AdminMenu from '@/components/menu/AdminMenu';
import pageStyles from '@/styles/pages/principal.module.css';
export default function Reporte() {
    const [mensaje, setMensaje] = useState('');
    const [menuOpen, setMenuOpen] = useState(false);
    const openMenu = () => setMenuOpen(true);
    const closeMenu = () => setMenuOpen(false);
    const generarReporte = async () => {
        try {
            const response = await fetch('http://localhost:8000/reportes/generar');

            if (response.status === 200) {
                setMensaje('Reporte generado con éxito');
            } else {
                setMensaje('');
            }
        } catch (error) {
            console.error(error);
            setMensaje('Error en la generación de reporte'); // no mostrar mensaje si hubo error
        }
    };

    useEffect(() => {
        generarReporte();
    }, []);

    return (
        <div>
            <Navbar title="Reportes" onMenuClick={openMenu} />
            {menuOpen && (
                <div className={pageStyles.overlay} onClick={closeMenu}></div>
            )}

            <AdminMenu isOpen={menuOpen} onClose={closeMenu} />

            {mensaje && (
                <p style={{ background: 'lightgreen', padding: '10px' }}>{mensaje}</p>
            )}
        </div>
    );
}
