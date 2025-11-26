import { useState } from 'react';
import { Link } from 'react-router-dom';

import sideStyles from '../../styles/pages/principal.module.css';
import styles from '../../styles/components/menu.module.css';

type AdminMenuProps = {
  isOpen: boolean;
  onClose: () => void;
};

export default function AdminMenu({ isOpen, onClose }: AdminMenuProps) {
  const [openOrg, setOpenOrg] = useState(false);

  return (
    <div className={`${sideStyles.sideMenu} ${isOpen ? sideStyles.open : ''}`}>
      {/* Encabezado con botón de cerrar */}
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

      {/* Sección Organización */}
      <div className={styles.section}>
        <button
          className={styles.sectionHeader}
          onClick={() => setOpenOrg(!openOrg)}
        >
          Organización
          <span className={styles.arrow}>{openOrg ? '▲' : '▼'}</span>
        </button>

        {openOrg && (
          <div className={styles.dropdownContent}>
            <Link
              to="/admin/especialidades"
              className={styles.menuButton}
              onClick={onClose}
            >
              Especialidades
            </Link>
            <Link
              to="/admin/obrasSociales"
              className={styles.menuButton}
              onClick={onClose}
            >
              Obras Sociales
            </Link>
            <Link
              to="/admin/alergias"
              className={styles.menuButton}
              onClick={onClose}
            >
              Alergias
            </Link>
            <Link
              to="/admin/antecedentes"
              className={styles.menuButton}
              onClick={onClose}
            >
              Antecedentes
            </Link>
            <Link
              to="/admin/medicamentos"
              className={styles.menuButton}
              onClick={onClose}
            >
              Medicamentos
            </Link>
          </div>
        )}
      </div>

      <div className={styles.menuOptions}>
        {/* Otros enlaces */}
        <Link to="/registrar-turno" className={styles.menuButton}>
          Registrar turno
        </Link>

        <Link to="/admin/RegistroPacientes" className={styles.menuButton}>
          Registrar paciente
        </Link>

        <Link to="/admin/RegistroProfesional" className={styles.menuButton}>
          Registrar profesional
        </Link>
      </div>
    </div>
  );
}
