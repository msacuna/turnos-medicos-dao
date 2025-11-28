import { useState } from 'react';
import Navbar from '@/components/ui/Navbar';
import AdminMenu from '@/components/menu/AdminMenu';
import { reporteService } from '@/service/reporteService';
import pageStyles from '@/styles/pages/principal.module.css';

export default function Reporte() {
  const [loading, setLoading] = useState<string>('');
  const [mensaje, setMensaje] = useState<{ tipo: 'success' | 'error', texto: string } | null>(null);
  
  // Estados para el formulario de período
  const [anio, setAnio] = useState<number>(new Date().getFullYear());
  const [mesInicio, setMesInicio] = useState<number>(1);
  const [mesFin, setMesFin] = useState<number>(12);
  const [mostrarFormularioPeriodo, setMostrarFormularioPeriodo] = useState(false);
  
  const [menuOpen, setMenuOpen] = useState(false);
  const openMenu = () => setMenuOpen(true);
  const closeMenu = () => setMenuOpen(false);

  const generarReporte = async (tipoReporte: string, serviceCall: () => Promise<Response>) => {
    setLoading(tipoReporte);
    setMensaje(null);
    
    try {
      const response = await serviceCall();
      
      if (response.ok) {
        try {
          const data = await response.json();
          setMensaje({ 
            tipo: 'success', 
            texto: `✅ ${data.mensaje || `Reporte "${tipoReporte}" generado exitosamente.`}` 
          });
        } catch {
          setMensaje({ 
            tipo: 'success', 
            texto: `✅ Reporte "${tipoReporte}" generado exitosamente.` 
          });
        }
      } else {
        let errorMsg = '';
        try {
          const errorData = await response.json();
          errorMsg = errorData.mensaje || errorData.error || 'Error desconocido';
        } catch {
          errorMsg = `Error HTTP ${response.status}`;
        }
        
        setMensaje({ 
          tipo: 'error', 
          texto: `❌ Error al generar "${tipoReporte}": ${errorMsg}` 
        });
      }
    } catch (error) {
      console.error(`Error generando reporte ${tipoReporte}:`, error);
      
      let errorMsg = '';
      if (error instanceof TypeError && error.message.includes('NetworkError')) {
        errorMsg = 'Error de conexión o CORS. Verifique que el servidor esté ejecutándose.';
      } else {
        errorMsg = 'Error inesperado. Consulte la consola para más detalles.';
      }
      
      setMensaje({ 
        tipo: 'error', 
        texto: `❌ Error con "${tipoReporte}": ${errorMsg}` 
      });
    } finally {
      setLoading('');
      if (tipoReporte === 'Turnos por Período') {
        setMostrarFormularioPeriodo(false);
      }
    }
  };

  const generarReportePorPeriodo = () => {
    generarReporte(
      'Turnos por Período',
      () => reporteService.turnosPorPeriodo(anio, mesInicio, mesFin)
    );
  };

  const meses = [
    { valor: 1, nombre: 'Enero' },
    { valor: 2, nombre: 'Febrero' },
    { valor: 3, nombre: 'Marzo' },
    { valor: 4, nombre: 'Abril' },
    { valor: 5, nombre: 'Mayo' },
    { valor: 6, nombre: 'Junio' },
    { valor: 7, nombre: 'Julio' },
    { valor: 8, nombre: 'Agosto' },
    { valor: 9, nombre: 'Septiembre' },
    { valor: 10, nombre: 'Octubre' },
    { valor: 11, nombre: 'Noviembre' },
    { valor: 12, nombre: 'Diciembre' }
  ];

  const reportes = [
    {
      titulo: 'Turnos por Especialidad',
      descripcion: 'Genera un reporte con la cantidad de turnos agrupados por especialidad.',
      accion: () => generarReporte('Turnos por Especialidad', reporteService.turnosPorEspecialidad),
      funciona: true
    },
    {
      titulo: 'Pacientes por Obra Social',
      descripcion: 'Genera un reporte con la cantidad de pacientes agrupados por obra social.',
      accion: () => generarReporte('Pacientes por Obra Social', reporteService.pacientesPorObraSocial),
      funciona: true
    },
    {
      titulo: 'Montos por Especialidad',
      descripcion: 'Genera un reporte con los montos totales recaudados por especialidad.',
      accion: () => generarReporte('Montos por Especialidad', reporteService.montosPorEspecialidad),
      funciona: true
    },
    {
      titulo: 'Turnos por Período',
      descripcion: 'Genera un reporte con la cantidad de turnos en un período específico.',
      accion: () => setMostrarFormularioPeriodo(true), // Mostrar formulario en lugar de ejecutar directamente
      funciona: true,
      especial: true
    },
    {
      titulo: 'Profesionales por Especialidad',
      descripcion: 'Genera un reporte con la cantidad de profesionales por especialidad.',
      accion: () => generarReporte('Profesionales por Especialidad', reporteService.profesionalesPorEspecialidad),
      funciona: true
    }
  ];

  return (
    <div>
      <Navbar title="Reportes" onMenuClick={openMenu} />
      {menuOpen && (
        <div className={pageStyles.overlay} onClick={closeMenu}></div>
      )}

      <AdminMenu isOpen={menuOpen} onClose={closeMenu} />

      <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
        
        {/* Mensaje de estado */}
        {mensaje && (
          <div style={{
            background: mensaje.tipo === 'success' ? '#e8f5e8' : '#ffebee',
            color: mensaje.tipo === 'success' ? '#2e7d32' : '#c62828',
            padding: '15px',
            borderRadius: '8px',
            marginBottom: '20px',
            border: `1px solid ${mensaje.tipo === 'success' ? '#4caf50' : '#f44336'}`
          }}>
            {mensaje.texto}
            <button 
              onClick={() => setMensaje(null)}
              style={{ 
                float: 'right', 
                background: 'transparent', 
                border: 'none', 
                fontSize: '18px', 
                cursor: 'pointer' 
              }}
            >
              ×
            </button>
          </div>
        )}

        <h2 style={{ textAlign: 'center', marginBottom: '30px', color: '#1976d2' }}>
          Generación de Reportes
        </h2>
        
        <p style={{ textAlign: 'center', marginBottom: '30px', color: '#666' }}>
          Selecciona el tipo de reporte que deseas generar. El archivo PDF se guardará automáticamente.
        </p>

        <div style={{ display: 'grid', gap: '20px' }}>
          {reportes.map((reporte, index) => (
            <div 
              key={index}
              style={{
                border: '1px solid #ddd',
                borderRadius: '8px',
                padding: '20px',
                backgroundColor: 'white',
                boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
              }}
            >
              <h3 style={{ 
                margin: '0 0 10px 0', 
                color: '#1976d2',
                fontSize: '18px'
              }}>
                {reporte.titulo}
              </h3>
              
              <p style={{ 
                margin: '0 0 15px 0', 
                color: '#666',
                fontSize: '14px'
              }}>
                {reporte.descripcion}
              </p>
              
              <button
                onClick={reporte.accion}
                disabled={loading !== '' || !reporte.funciona}
                style={{
                  padding: '12px 24px',
                  backgroundColor: !reporte.funciona ? '#ffcdd2' : (loading === reporte.titulo ? '#ccc' : '#1976d2'),
                  color: !reporte.funciona ? '#666' : 'white',
                  border: 'none',
                  borderRadius: '4px',
                  cursor: (!reporte.funciona || loading === reporte.titulo) ? 'not-allowed' : 'pointer',
                  fontSize: '14px',
                  fontWeight: 'bold',
                  width: '100%'
                }}
              >
                {!reporte.funciona ? '❌ Endpoint con problemas' : 
                 (loading === reporte.titulo ? 'Generando...' : 
                  (reporte.especial ? 'Configurar Período' : 'Generar Reporte'))}
              </button>
            </div>
          ))}
        </div>

        {/* Modal/Formulario para Turnos por Período */}
        {mostrarFormularioPeriodo && (
          <div style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: 'rgba(0,0,0,0.5)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 1000
          }}>
            <div style={{
              backgroundColor: 'white',
              padding: '30px',
              borderRadius: '8px',
              maxWidth: '500px',
              width: '90%',
              boxShadow: '0 4px 20px rgba(0,0,0,0.3)'
            }}>
              <h3 style={{ marginTop: 0, color: '#1976d2' }}>
                Configurar Período para el Reporte
              </h3>
              
              <div style={{ marginBottom: '20px' }}>
                <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
                  Año:
                </label>
                <input
                  type="number"
                  value={anio}
                  onChange={(e) => setAnio(parseInt(e.target.value))}
                  min="2020"
                  max="2030"
                  style={{
                    width: '100%',
                    padding: '8px',
                    border: '1px solid #ddd',
                    borderRadius: '4px',
                    fontSize: '14px'
                  }}
                />
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px', marginBottom: '20px' }}>
                <div>
                  <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
                    Mes Inicio:
                  </label>
                  <select
                    value={mesInicio}
                    onChange={(e) => setMesInicio(parseInt(e.target.value))}
                    style={{
                      width: '100%',
                      padding: '8px',
                      border: '1px solid #ddd',
                      borderRadius: '4px',
                      fontSize: '14px'
                    }}
                  >
                    {meses.map(mes => (
                      <option key={mes.valor} value={mes.valor}>
                        {mes.nombre}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
                    Mes Fin:
                  </label>
                  <select
                    value={mesFin}
                    onChange={(e) => setMesFin(parseInt(e.target.value))}
                    style={{
                      width: '100%',
                      padding: '8px',
                      border: '1px solid #ddd',
                      borderRadius: '4px',
                      fontSize: '14px'
                    }}
                  >
                    {meses.map(mes => (
                      <option key={mes.valor} value={mes.valor}>
                        {mes.nombre}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              <div style={{ textAlign: 'center', fontSize: '14px', color: '#666', marginBottom: '20px' }}>
                Período seleccionado: {meses[mesInicio-1].nombre} - {meses[mesFin-1].nombre} de {anio}
              </div>

              <div style={{ display: 'flex', gap: '10px', justifyContent: 'flex-end' }}>
                <button
                  onClick={() => setMostrarFormularioPeriodo(false)}
                  style={{
                    padding: '10px 20px',
                    backgroundColor: '#666',
                    color: 'white',
                    border: 'none',
                    borderRadius: '4px',
                    cursor: 'pointer'
                  }}
                >
                  Cancelar
                </button>
                <button
                  onClick={generarReportePorPeriodo}
                  disabled={mesInicio > mesFin}
                  style={{
                    padding: '10px 20px',
                    backgroundColor: mesInicio > mesFin ? '#ccc' : '#1976d2',
                    color: 'white',
                    border: 'none',
                    borderRadius: '4px',
                    cursor: mesInicio > mesFin ? 'not-allowed' : 'pointer'
                  }}
                >
                  Generar Reporte
                </button>
              </div>
              
              {mesInicio > mesFin && (
                <p style={{ color: '#c62828', fontSize: '12px', textAlign: 'center', marginTop: '10px' }}>
                  El mes de inicio debe ser menor o igual al mes de fin
                </p>
              )}
            </div>
          </div>
        )}

        {loading && (
          <div style={{ 
            textAlign: 'center', 
            marginTop: '20px',
            padding: '15px',
            backgroundColor: '#e3f2fd',
            borderRadius: '8px'
          }}>
            <p style={{ margin: 0, color: '#1976d2' }}>
              🔄 Generando reporte "{loading}"... Por favor espere.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}