export interface ObraSocial {
  id: number;
  cuit: string;
  nombre: string;
  porcentaje_cobertura: number;
  nombre_tipo: string;
}

export interface ObraSocialCreate {
  cuit: string;
  nombre: string;
  porcentaje_cobertura: number;
  nombre_tipo: string;
}

export interface ObraSocialUpdate extends ObraSocialCreate {
  id: number;
}

export type ObraSocialPayload = ObraSocialCreate | ObraSocialUpdate;
