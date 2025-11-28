import { useEffect, useState } from 'react';
import { useAuth } from '../../hooks/useAuth';
import {
  getHorariosProfesional,
  updateHorarioProfesional,
} from '../../service/agendaService';
import Navbar from '@/components/ui/Navbar';

import MedicoMenu from '@/components/menu/MedicoMenu';
import pageStyles from '@/styles/pages/principal.module.css';

// Días que mostrará el frontend
const DIAS = [
  { front: 'LUNES', backend: 'Lunes' },
  { front: 'MARTES', backend: 'Martes' },
  { front: 'MIERCOLES', backend: 'Miercoles' },
  { front: 'JUEVES', backend: 'Jueves' },
  { front: 'VIERNES', backend: 'Viernes' },
  { front: 'SABADO', backend: 'Sabado' },
];

export default function Agenda() {
  const { user } = useAuth();

  const profesionalId = user?.id ?? null;

  const [horarios, setHorarios] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [guardando, setGuardando] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const openMenu = () => setMenuOpen(true);
  const closeMenu = () => setMenuOpen(false);

  useEffect(() => {
    if (!profesionalId) return;

    const loadHorarios = async () => {
      try {
        const data = await getHorariosProfesional(profesionalId);

        // Normalizamos los datos para que coincidan con los días del frontend
        const map = DIAS.map(({ front, backend }) => {
          const encontrado = data.find((h) => h.dia_semana === backend);
          return encontrado
            ? {
                dia_front: front,
                dia_back: backend,
                trabaja: true,
                hora_inicio: encontrado.hora_inicio.slice(0, 5),
                hora_fin: encontrado.hora_fin.slice(0, 5),
              }
            : {
                dia_front: front,
                dia_back: backend,
                trabaja: false,
                hora_inicio: '',
                hora_fin: '',
              };
        });

        setHorarios(map);
      } catch (e) {
        console.error('Error cargando horarios:', e);
      } finally {
        setLoading(false);
      }
    };

    loadHorarios();
  }, [profesionalId]);

  const actualizarCampo = (dia_front: string, campo: string, valor: any) => {
    setHorarios((prev) =>
      prev.map((h) =>
        h.dia_front === dia_front ? { ...h, [campo]: valor } : h
      )
    );
  };

  const guardarCambios = async (dia_front: string) => {
    const horario = horarios.find((h) => h.dia_front === dia_front);
    if (!horario) return;

    setGuardando(true);

    try {
      await updateHorarioProfesional(profesionalId!, horario.dia_back, {
        trabaja: horario.trabaja,
        hora_inicio: horario.trabaja ? horario.hora_inicio : null,
        hora_fin: horario.trabaja ? horario.hora_fin : null,
      });

      alert('Horario actualizado correctamente');
    } catch (e) {
      console.error('Error guardando horario:', e);
      alert('Error al guardar horario');
    } finally {
      setGuardando(false);
    }
  };

  if (loading) return <p>Cargando horarios del profesional...</p>;

  return (
    <div>
      <Navbar title="Horarios del Profesional" onMenuClick={openMenu} />
      {menuOpen && (
        <div className={pageStyles.overlay} onClick={closeMenu}></div>
      )}

      <MedicoMenu isOpen={menuOpen} onClose={closeMenu} />

      {horarios.map((h) => (
        <div
          key={h.dia_front}
          style={{ border: '1px solid #ccc', padding: 10, marginBottom: 10 }}
        >
          <h3>{h.dia_front}</h3>

          <label>
            <input
              type="checkbox"
              checked={h.trabaja}
              onChange={(e) =>
                actualizarCampo(h.dia_front, 'trabaja', e.target.checked)
              }
            />
            Trabaja este día
          </label>

          {h.trabaja && (
            <div style={{ marginTop: 10 }}>
              <label>
                Inicio:
                <input
                  type="time"
                  value={h.hora_inicio}
                  onChange={(e) =>
                    actualizarCampo(h.dia_front, 'hora_inicio', e.target.value)
                  }
                />
              </label>

              <label style={{ marginLeft: 20 }}>
                Fin:
                <input
                  type="time"
                  value={h.hora_fin}
                  onChange={(e) =>
                    actualizarCampo(h.dia_front, 'hora_fin', e.target.value)
                  }
                />
              </label>
            </div>
          )}

          <button
            onClick={() => guardarCambios(h.dia_front)}
            disabled={guardando}
            style={{ marginTop: 10 }}
          >
            Guardar {h.dia_front}
          </button>
        </div>
      ))}
    </div>
  );
}
