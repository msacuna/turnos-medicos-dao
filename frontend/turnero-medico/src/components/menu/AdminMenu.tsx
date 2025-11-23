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
          ✖
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
          <div className={styles.sectionContent}>
            <Link to="/admin/especialidades" className={styles.item}>
              Especialidades
            </Link>
            <Link to="/abmc-laboratorios" className={styles.item}>
              Laboratorios
            </Link>
            <Link to="/abmc-obras-sociales" className={styles.item}>
              Obras Sociales
            </Link>
            <Link to="/abmc-alergias" className={styles.item}>
              Alergias
            </Link>
            <Link to="/abmc-antecedentes" className={styles.item}>
              Antecedentes
            </Link>
          </div>
        )}
      </div>

      {/* Otros enlaces */}
      <Link to="/registrar-turno" className={styles.item}>
        Registrar turno
      </Link>

      <Link to="/registrar-paciente" className={styles.item}>
        Registrar paciente
      </Link>

      <Link to="/registrar-profesional" className={styles.item}>
        Registrar profesional
      </Link>

      <Link to="/abmc-medicamentos" className={styles.item}>
        ABMC Medicamentos
      </Link>
    </div>
  );
}
