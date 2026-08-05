import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { Auth, user } from '@angular/fire/auth';
import { map, take } from 'rxjs';

/**
 * Guard funcional que protege rutas privadas.
 * Redirige a /login si el usuario no está autenticado.
 */
export const authGuard: CanActivateFn = () => {
  const auth = inject(Auth);
  const router = inject(Router);

  return user(auth).pipe(
    take(1),
    map((u) => {
      if (u) return true;
      return router.createUrlTree(['/login']);
    }),
  );
};

/**
 * Guard funcional que protege la pantalla de login.
 * Redirige a /dashboard si el usuario ya está autenticado.
 */
export const publicGuard: CanActivateFn = () => {
  const auth = inject(Auth);
  const router = inject(Router);

  return user(auth).pipe(
    take(1),
    map((u) => {
      if (!u) return true;
      return router.createUrlTree(['/dashboard']);
    }),
  );
};
