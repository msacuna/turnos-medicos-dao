import React, { useState } from 'react';
import Navbar from '../components/ui/Navbar';
import { useAuth } from '../hooks/useAuth';

import AdminMenu from '../components/menu/AdminMenu';
import MedicoMenu from '../components/menu/MedicoMenu';

import styles from '../styles/pages/principal.module.css';

export default function Principal() {
  const { user } = useAuth();
  console.log('USER EN PRINCIPAL:', user);

  const [menuOpen, setMenuOpen] = useState(false);

  const openMenu = () => setMenuOpen(true);
  const closeMenu = () => setMenuOpen(false);

  return (
    <div className={styles.page}>
      <Navbar title="Inicio" onMenuClick={openMenu} />

      {/* Overlay oscuro */}
      {menuOpen && <div className={styles.overlay} onClick={closeMenu}></div>}

      {/* Menú lateral */}
      {user?.role === 'administrador' && (
        <AdminMenu isOpen={menuOpen} onClose={closeMenu} />
      )}

      {user?.role === 'medico' && (
        <MedicoMenu isOpen={menuOpen} onClose={closeMenu} />
      )}

      {/* Contenido */}
      <div className={styles.container}>
        <div className={styles.content}>
          <img src="/logo-sin-fondo.png" alt="logo" className={styles.logo} />
          <h1 className={styles.title}>¡Bienvenido!</h1>
        </div>
      </div>
    </div>
  );
}
