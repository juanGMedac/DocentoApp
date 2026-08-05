import { Component, inject, OnInit } from '@angular/core';
import { CommonModule, AsyncPipe } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { AuthService } from '../../services/auth.service';
import { ThemeService } from '../../services/theme.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, AsyncPipe],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css',
})
export class DashboardComponent implements OnInit {
  authService = inject(AuthService);
  themeService = inject(ThemeService);
  http = inject(HttpClient);

  backendMessage: string = 'Conectando con el servidor...';

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
  }
}
