import { createContext } from 'react';

export type User = {
  usuario: string;
  role: string;
  id: number;
} | null;

export type AuthContextType = {
  user: User;
  login: (usuario: string, role: string, id: number) => void;
  logout: () => void;
};

export const AuthContext = createContext<AuthContextType | null>(null);
