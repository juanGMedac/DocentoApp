import { Injectable, inject } from '@angular/core';
import { Router } from '@angular/router';
import {
  Auth,
  signInWithEmailAndPassword,
  signInWithPopup,
  signOut,
  GoogleAuthProvider,
  user,
  User,
} from '@angular/fire/auth';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private auth = inject(Auth);
  private router = inject(Router);

  /** Observable del usuario autenticado (null si no hay sesión). */
  readonly user$: Observable<User | null> = user(this.auth);

  /* ──────────────────────────────────────────────
   *  Inicio de sesión con email y contraseña
   * ────────────────────────────────────────────── */
  async loginWithEmail(email: string, password: string): Promise<void> {
    await signInWithEmailAndPassword(this.auth, email, password);
    this.router.navigate(['/dashboard']);
  }

  /* ──────────────────────────────────────────────
   *  Inicio de sesión con Google
   * ────────────────────────────────────────────── */
  async loginWithGoogle(): Promise<void> {
    const provider = new GoogleAuthProvider();
    await signInWithPopup(this.auth, provider);
    this.router.navigate(['/dashboard']);
  }

  /* ──────────────────────────────────────────────
   *  Cerrar sesión
   * ────────────────────────────────────────────── */
  async logout(): Promise<void> {
    await signOut(this.auth);
    this.router.navigate(['/login']);
  }
}
