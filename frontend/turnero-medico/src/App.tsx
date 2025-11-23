import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthProvider';
import { useAuth } from './hooks/useAuth';
import type { ReactNode } from 'react';

import Login from './pages/Login';
import Principal from './pages/Principal';

import RoleRoute from './components/layout/RoleRoute';
import Especialidades from './pages/admin/Especialidades';

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

          {/* DEFAULT */}
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}
