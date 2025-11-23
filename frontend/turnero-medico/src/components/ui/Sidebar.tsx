import React from 'react';
import styles from '../../styles/components/sidebar.module.css';
import AdminMenu from '../menu/AdminMenu';
import MedicoMenu from '../menu/MedicoMenu';
import { useAuth } from '../../hooks/useAuth';

type SidebarProps = {
  isOpen: boolean;
  onClose: () => void;
};

export default function Sidebar({ isOpen, onClose }: SidebarProps) {
  const { user } = useAuth();

  return (
    <>
      {/* Overlay oscuro */}
      <div
        className={`${styles.overlay} ${isOpen ? styles.overlayVisible : ''}`}
        onClick={onClose}
      />

      {/* Sidebar */}
      <aside className={`${styles.sidebar} ${isOpen ? styles.open : ''}`}>
        <h3 className={styles.title}>Menú</h3>

        {/* Menú según rol */}
        {user?.role === 'admin' && <AdminMenu />}
        {user?.role === 'medico' && <MedicoMenu />}
      </aside>
    </>
  );
}
