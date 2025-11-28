import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthProvider';
import { useAuth } from './hooks/useAuth';
import type { ReactNode } from 'react';

import Login from './pages/Login';
import Principal from './pages/Principal';

import RoleRoute from './components/layout/RoleRoute';
import Especialidades from './pages/admin/Especialidades';
import Alergias from './pages/admin/Alergias';
import ObrasSociales from './pages/admin/ObrasSociales';
import Antecedentes from './pages/admin/Antecedentes';
import Medicamentos from './pages/admin/Medicamentos';

import RegistroPacientes from './pages/admin/RegistroPacientes';
import RegistroProfesional from './pages/admin/RegistroProfesional';
import Pacientes from './pages/admin/Pacientes';
import Profesional from './pages/admin/Profesional';
import Turno from './pages/medico/Turno';
import Agenda from './pages/medico/Agenda';
import Reporte from './pages/admin/Reporte';
import RegistroTurno from './pages/admin/RegistroTurno';

function PrivateRoute({ children }: { children: ReactNode }) {
  const { user } = useAuth();
  return user ? children : <Navigate to="/login" replace />;
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          {/* LOGIN */}
          <Route path="/login" element={<Login />} />

          {/* PRINCIPAL */}
          <Route
            path="/principal"
            element={
              <PrivateRoute>
                <Principal />
              </PrivateRoute>
            }
          />

          {/* ADMIN → ESPECIALIDADES */}
          <Route
            path="/admin/especialidades"
            element={
              <RoleRoute allowed={['administrador']}>
                <Especialidades />
              </RoleRoute>
            }
          />

          {/* ADMIN → ALERGIAS */}
          <Route
            path="/admin/alergias"
            element={
              <RoleRoute allowed={['administrador']}>
                <Alergias />
              </RoleRoute>
            }
          />

          {/* ADMIN → OBRAS SOCIALES */}
          <Route
            path="/admin/obrasSociales"
            element={
              <RoleRoute allowed={['administrador']}>
                <ObrasSociales />
              </RoleRoute>
            }
          />

          {/* ADMIN → ANTECEDENTES */}
          <Route
            path="/admin/antecedentes"
            element={
              <RoleRoute allowed={['administrador']}>
                <Antecedentes />
              </RoleRoute>
            }
          />

          {/* ADMIN → MEDICAMENTOS */}
          <Route
            path="/admin/medicamentos"
            element={
              <RoleRoute allowed={['administrador']}>
                <Medicamentos />
              </RoleRoute>
            }
          />

          {/* ADMIN → REGISTRO PACIENTES */}
          <Route
            path="/admin/RegistroPacientes"
            element={
              <RoleRoute allowed={['administrador']}>
                <RegistroPacientes />
              </RoleRoute>
            }
          />

          {/* ADMIN → REGISTRO PROFESIONAL */}
          <Route
            path="/admin/RegistroProfesional"
            element={
              <RoleRoute allowed={['administrador']}>
                <RegistroProfesional />
              </RoleRoute>
            }
          />

          {/* ADMIN → PACIENTES */}
          <Route
            path="/admin/pacientes"
            element={
              <RoleRoute allowed={['administrador']}>
                <Pacientes />
              </RoleRoute>
            }
          />

          {/* ADMIN → PROFESIONAL */}
          <Route
            path="/admin/profesionales"
            element={
              <RoleRoute allowed={['administrador']}>
                <Profesional />
              </RoleRoute>
            }
          />

          {/* MEDICO → TURNOS */}
          <Route
            path="/medico/turno"
            element={
              <RoleRoute allowed={['medico']}>
                <Turno />
              </RoleRoute>
            }
          />

          {/* MEDICO → AGENDA */}
          <Route
            path="/medico/agenda"
            element={
              <RoleRoute allowed={['medico']}>
                <Agenda />
              </RoleRoute>
            }
          />

          {/* ADMIN → REPORTES */}
          <Route
            path="/admin/reportes"
            element={
              <RoleRoute allowed={['administrador']}>
                <Reporte />
              </RoleRoute>
            }
          />

          {/* ADMIN → REGISTRO TURNOS */}
          <Route
            path="/admin/registroTurno"
            element={
              <RoleRoute allowed={['administrador']}>
                <RegistroTurno />
              </RoleRoute>
            }
          />

          {/* DEFAULT */}
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}
