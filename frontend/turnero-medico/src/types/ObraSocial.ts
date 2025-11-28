export type TipoObraSocialEnum = 'Nacional' | 'Provincial' | 'Jubilado';

export interface ObraSocial {
  id: number;
  cuit: string;
  nombre: string;
  porcentaje_cobertura: number;
  nombre_tipo: TipoObraSocialEnum;
}

export interface ObraSocialCreate {
  cuit: string;
  nombre: string;
  porcentaje_cobertura: number;
  nombre_tipo: TipoObraSocialEnum;
}
export interface ObraSocialUpdate {
  cuit?: string;
  nombre?: string;
  porcentaje_cobertura?: number;
  nombre_tipo?: TipoObraSocialEnum;
}

export type ObraSocialPayload = ObraSocialCreate | ObraSocialUpdate;
