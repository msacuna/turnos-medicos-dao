import React from 'react';
import styles from '../../styles/components/navbar.module.css';

type NavbarProps = {
  title: string;
  onMenuClick?: () => void;
};

export default function Navbar({ title, onMenuClick }: NavbarProps) {
  return (
    <>
      <header className={styles.navbar}>
        <button className={styles.menuButton} onClick={onMenuClick}>
          {/* Ícono SVG de 3 rayas horizontales */}
          <svg
            xmlns="http://www.w3.org/2000/svg"
            height="28px"
            viewBox="0 -960 960 960"
            width="28px"
            fill="black"
          >
            <path d="M120-240v-80h720v80H120Zm0-200v-80h720v80H120Zm0-200v-80h720v80H120Z" />
          </svg>
        </button>

        <h2 className={styles.title}>{title}</h2>

        {/* Para mantener el título centrado, agregamos un div vacío del mismo ancho que el botón */}
        <div className={styles.placeholder}></div>
        <div className={styles.divider}></div>
      </header>
    </>
  );
}
