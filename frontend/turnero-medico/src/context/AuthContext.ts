import { createContext } from 'react';

export type User = {
  usuario: string;
  role: string;
} | null;

export type AuthContextType = {
  user: User;
  login: (usuario: string, role: string) => void;
  logout: () => void;
};

export const AuthContext = createContext<AuthContextType | null>(null);
