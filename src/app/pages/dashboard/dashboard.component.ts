import { Component, inject, OnInit } from '@angular/core';
import { CommonModule, AsyncPipe } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { AuthService } from '../../services/auth.service';
import { ThemeService } from '../../services/theme.service';
import { GruposService } from '../../services/grupos.service';
import { GrupoResponse } from '../../models/grupo.model';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, AsyncPipe, HttpClientModule],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css',
})
export class DashboardComponent implements OnInit {
  authService = inject(AuthService);
  themeService = inject(ThemeService);
  http = inject(HttpClient);
  gruposService = inject(GruposService);

  backendMessage: string = 'Conectando con el servidor...';
  grupos: GrupoResponse[] = [];
  isDarkMode: boolean = false;
  isMobileMenuOpen: boolean = false;

  toggleMobileMenu() {
    this.isMobileMenuOpen = !this.isMobileMenuOpen;
  }

  coloresCorporativos = [
    'bg-blue-600',
    'bg-indigo-500',
    'bg-violet-500',
    'bg-purple-600',
    'bg-fuchsia-500',
    'bg-pink-500',
    'bg-rose-500',
    'bg-red-500',
    'bg-orange-500',
    'bg-amber-500',
    'bg-yellow-500',
    'bg-lime-500',
    'bg-green-500',
    'bg-emerald-500',
    'bg-teal-500',
    'bg-cyan-500',
    'bg-sky-500',
  ];

  cambiarColor(grupo: GrupoResponse) {
    const colorAnterior = grupo.color || 'bg-blue-600';
    const currentIndex = this.coloresCorporativos.indexOf(colorAnterior);
    const nextIndex = (currentIndex + 1) % this.coloresCorporativos.length;
    const nuevoColor = this.coloresCorporativos[nextIndex];

    // Actualización optimista: cambia la UI de inmediato
    grupo.color = nuevoColor;

    // Persiste en la base de datos
    this.gruposService.updateColor(grupo.id, nuevoColor).subscribe({
      error: (err) => {
        // Rollback si falla el servidor
        console.error('Error guardando el color:', err);
        grupo.color = colorAnterior;
      }
    });
  }

  ngOnInit() {
    this.http.get<{ status: string; message: string }>('http://127.0.0.1:8000/api/status')
      .subscribe({
        next: (response) => {
          this.backendMessage = response.message;
        },
        error: (error) => {
          this.backendMessage = 'Error al conectar con el servidor backend.';
          console.error('Error fetching backend status:', error);
        }
      });

    this.gruposService.getGrupos().subscribe({
      next: (data) => {
        this.grupos = data;
      },
      error: (error) => {
        console.error('Error fetching grupos:', error);
      }
    });
  }

  toggleDarkMode() {
    this.isDarkMode = !this.isDarkMode;
    if (this.isDarkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }
}
