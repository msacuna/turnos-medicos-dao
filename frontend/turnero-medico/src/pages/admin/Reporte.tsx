import { useEffect, useState } from 'react';

export default function Reporte() {
  const [mensaje, setMensaje] = useState('');

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
      <h1>Reportes</h1>

      {mensaje && (
        <p style={{ background: 'lightgreen', padding: '10px' }}>{mensaje}</p>
      )}
    </div>
  );
}
