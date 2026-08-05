import { Injectable, signal, effect } from '@angular/core';

export type Theme = 'light' | 'dark';

@Injectable({ providedIn: 'root' })
export class ThemeService {
  private readonly STORAGE_KEY = 'docento-theme';

  /** Signal reactivo con el tema actual. */
  readonly theme = signal<Theme>(this.getInitialTheme());

  constructor() {
    // Efecto que sincroniza la clase `dark` en <html> y persiste en localStorage
    effect(() => {
      const current = this.theme();
      const root = document.documentElement;

      if (current === 'dark') {
        root.classList.add('dark');
      } else {
        root.classList.remove('dark');
      }

      localStorage.setItem(this.STORAGE_KEY, current);
    });
  }

  /** Alterna entre modo claro y oscuro. */
  toggleTheme(): void {
    this.theme.update((t) => (t === 'light' ? 'dark' : 'light'));
  }

  /** Establece un tema concreto. */
  setTheme(theme: Theme): void {
    this.theme.set(theme);
  }

  /* ──────────────────────────────────────────────
   *  Determina el tema inicial:
   *  1. Revisa localStorage
   *  2. Si no hay, respeta prefers-color-scheme del SO
   *  3. Por defecto: light
   * ────────────────────────────────────────────── */
  private getInitialTheme(): Theme {
    if (typeof window === 'undefined') return 'light';

    const stored = localStorage.getItem(this.STORAGE_KEY) as Theme | null;
    if (stored === 'light' || stored === 'dark') return stored;

    return window.matchMedia('(prefers-color-scheme: dark)').matches
      ? 'dark'
      : 'light';
  }
}
