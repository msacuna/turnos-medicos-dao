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
          ✖
        </button>
      </div>

      {/* Opciones del médico */}
      <div className={styles.menuOptions}>
        <Link to="/ver-turnos" className={styles.menuButton}>
          Ver turnos
        </Link>

        <Link to="/registrar-horarios" className={styles.menuButton}>
          Registrar horarios
        </Link>
      </div>
    </div>
  );
}
