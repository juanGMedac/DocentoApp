export interface AlumnoResponse {
  id: number;
  nombre: string;
  email: string;
  id_grupo: number;
}

export interface GrupoResponse {
  id: number;
  nombre: string;
  ciclo: string;
  curso: string;
  profesor_id: number;
  color?: string;
  alumnos: AlumnoResponse[];
}

export interface GrupoUpdateColor {
  color: string;
}
