export interface Especialidad {
  id: number;
  nombre: string;
  precio: number;
}

export interface EspecialidadCreate {
  nombre: string;
  precio: number;
}

export interface EspecialidadUpdate {
  nombre?: string;
  precio?: number;
}
