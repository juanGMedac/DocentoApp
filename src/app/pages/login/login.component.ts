import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { ThemeService } from '../../services/theme.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css',
})
export class LoginComponent {
  private authService = inject(AuthService);
  private router = inject(Router);
  themeService = inject(ThemeService);

  email = '';
  password = '';
  errorMessage = '';
  isLoading = false;
  currentYear = new Date().getFullYear();

  async onEmailLogin(): Promise<void> {
    if (!this.email || !this.password) {
      this.errorMessage = 'Por favor, completa todos los campos.';
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';

    try {
      await this.authService.loginWithEmail(this.email, this.password);
    } catch (error: any) {
      this.errorMessage = this.mapFirebaseError(error.code);
    } finally {
      this.isLoading = false;
    }
  }

  async onGoogleLogin(): Promise<void> {
    this.isLoading = true;
    this.errorMessage = '';

    try {
      await this.authService.loginWithGoogle();
    } catch (error: any) {
      this.errorMessage = this.mapFirebaseError(error.code);
    } finally {
      this.isLoading = false;
    }
  }

  private mapFirebaseError(code: string): string {
    const errors: Record<string, string> = {
      'auth/user-not-found': 'No existe una cuenta con este correo electrónico.',
      'auth/wrong-password': 'La contraseña es incorrecta.',
      'auth/invalid-email': 'El formato del correo electrónico no es válido.',
      'auth/too-many-requests': 'Demasiados intentos. Inténtalo de nuevo más tarde.',
      'auth/popup-closed-by-user': 'Se canceló el inicio de sesión con Google.',
      'auth/invalid-credential': 'Las credenciales proporcionadas no son válidas.',
      'auth/network-request-failed': 'Error de red. Comprueba tu conexión a Internet.',
    };
    return errors[code] ?? 'Ha ocurrido un error inesperado. Inténtalo de nuevo.';
  }
}
