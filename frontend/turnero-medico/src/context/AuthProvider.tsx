import { useState, useEffect } from 'react';
import { AuthContext } from './AuthContext';
import type { User, AuthContextType } from './AuthContext';

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);

  // Al iniciar, leer usuario desde localStorage
  useEffect(() => {
    const saved = localStorage.getItem('user');
    if (saved) {
      setUser(JSON.parse(saved));
    }
  }, []);

  const login = (usuario: string, role: string, id: number) => {
    const newUser = { usuario, role, id };
    setUser(newUser);
    localStorage.setItem('user', JSON.stringify(newUser));
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('user');
  };

  const value: AuthContextType = { user, login, logout };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
