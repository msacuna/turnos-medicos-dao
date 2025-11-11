import React from 'react';
import './navbar.css';
import BackButton from '../BackButton/BackButton';
import MenuIcon from '@mui/icons-material/Menu';

const Navbar = ({ title, onMenuClick }) => {
  return (
    <nav className="navbar">
      <div className="navbar-left">
        <BackButton />
      </div>
      <h1 className="navbar-title">{title}</h1>
      <div className="navbar-right">
        <button
          className="menu-button"
          onClick={onMenuClick}
          title="Abrir menú"
        >
          <MenuIcon />
        </button>
      </div>
    </nav>
  );
};

export default Navbar;
