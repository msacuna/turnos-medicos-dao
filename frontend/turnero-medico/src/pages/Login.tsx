import React, { useState } from 'react';
import Input from '../components/ui/Input';
import Button from '../components/ui/Button';
import styles from '../styles/pages/login.module.css';
import { useAuth } from '../hooks/useAuth';
import { useNavigate } from 'react-router-dom';

export default function Login() {
  const [usuario, setUsuario] = useState('');
  const [contrasena, setContrasena] = useState('');
  const [error, setError] = useState('');

  const { login } = useAuth();
  const navigate = useNavigate();

  const handleLogin = () => {
    console.log('DEBUG LOGIN:', usuario, contrasena);
    // ADMIN
    if (usuario === 'admin' && contrasena === '1234') {
      console.log('ENTRÓ COMO ADMIN');
      login('admin', 'administrador');
      navigate('/principal');
      return;
    }

    // MÉDICO
    if (usuario === 'medico' && contrasena === '1234') {
      console.log('ENTRÓ COMO MÉDICO');
      login('medico', 'medico');
      navigate('/principal');
      return;
    }

    setError('Usuario o contraseña incorrectos');
  };

  return (
    <div className={styles.container}>
      <div className={styles.card}>
        {/* Logo */}
        <img src="/logo-sin-fondo.png" alt="logo" className={styles.logo} />

        <h1 className={styles.title}>CLÍNICA SANAR</h1>
        <p className={styles.subtitle}>Salud y Bienestar Integral</p>

        <div className={styles.wrapper}>
          <label>Usuario</label>
          <Input
            placeholder="Usuario"
            value={usuario}
            onChange={(e) => setUsuario(e.target.value)}
          />

          <label>Contraseña</label>
          <Input
            placeholder="Contraseña"
            type="password"
            value={contrasena}
            onChange={(e) => setContrasena(e.target.value)}
          />
        </div>

        {error && <p className={styles.error}>{error}</p>}

        <Button variant="primary" onClick={handleLogin}>
          Iniciar sesión
        </Button>

        <p className={styles.registerText}>
          ¿No tienes cuenta?{' '}
          <span className={styles.link}>Regístrate aquí</span>
        </p>
      </div>
    </div>
  );
}
