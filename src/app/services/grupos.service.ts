import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { GrupoResponse, GrupoUpdateColor } from '../models/grupo.model';

@Injectable({
  providedIn: 'root'
})
export class GruposService {
  private http = inject(HttpClient);
  private apiUrl = 'http://localhost:8000/api/grupos';

  getGrupos(): Observable<GrupoResponse[]> {
    return this.http.get<GrupoResponse[]>(this.apiUrl);
  }

  updateColor(grupoId: number, color: string): Observable<GrupoResponse> {
    return this.http.patch<GrupoResponse>(`${this.apiUrl}/${grupoId}/color`, { color });
  }
}
