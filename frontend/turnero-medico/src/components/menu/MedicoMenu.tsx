import { Link } from 'react-router-dom';

import sideStyles from '../../styles/pages/principal.module.css';
import styles from '../../styles/components/menu.module.css';

type MedicoMenuProps = {
    isOpen: boolean;
    onClose: () => void;
};

export default function MedicoMenu({ isOpen, onClose }: MedicoMenuProps) {
    return (
        <div className={`${sideStyles.sideMenu} ${isOpen ? sideStyles.open : ''}`}>
            {/* Header del menú */}
            <div className={styles.header}>
                <h2 className={styles.title}>Menú</h2>
                <button className={styles.closeButton} onClick={onClose}>
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        height="24px"
                        viewBox="0 -960 960 960"
                        width="24px"
                        fill="#000000"
                    >
                        <path d="m256-200-56-56 224-224-224-224 56-56 224 224 224-224 56 56-224 224 224 224-56 56-224-224-224 224Z" />
                    </svg>
                </button>
            </div>

            {/* Opciones del médico */}
            <div className={styles.menuOptions}>
                <Link to="/medico/turno" className={styles.menuButton}>
                    Ver turnos
                </Link>

                <Link to="/medico/agenda" className={styles.menuButton}>
                    Registrar agenda
                </Link>

                <Link to="/medico/cancelar-turnos" className={styles.menuButton}>
                    Cancelar turnos
                </Link>
            </div>
        </div>
    );
}
