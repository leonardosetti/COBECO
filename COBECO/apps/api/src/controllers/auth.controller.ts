import { Request, Response, NextFunction } from 'express';
import { AuthService } from '../services/auth.service';
import { AppError } from '../types';

const REFRESH_COOKIE = 'refreshToken';

function refreshCookieOptions() {
  return {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax' as const,
    path: '/',
    maxAge: 30 * 60 * 1000,
  };
}

export class AuthController {
  constructor(private authService: AuthService) {}

  async signUp(req: Request, res: Response, next: NextFunction) {
    try {
      const { name, username, email, password, consent } = req.body;
      const user = await this.authService.signUp(name, username, email, password, consent);
      res.status(201).json(user);
    } catch (error) {
      next(error);
    }
  }

  async login(req: Request, res: Response, next: NextFunction) {
    try {
      // RF02: o corpo traz `identifier` (e-mail ou username); `email` segue
      // aceito para clientes anteriores à v2.1.
      const { identifier, email, password } = req.body;
      const result = await this.authService.login(identifier || email, password);

      res.cookie(REFRESH_COOKIE, result.refreshToken, refreshCookieOptions());

      res.json({
        accessToken: result.accessToken,
        user: result.user,
      });
    } catch (error) {
      next(error);
    }
  }

  async refresh(req: Request, res: Response, next: NextFunction) {
    try {
      const result = await this.authService.refresh(req.cookies?.[REFRESH_COOKIE]);

      // Rotaciona o refresh token a cada renovação.
      res.cookie(REFRESH_COOKIE, result.refreshToken, refreshCookieOptions());

      res.json({
        accessToken: result.accessToken,
        user: result.user,
      });
    } catch (error) {
      res.clearCookie(REFRESH_COOKIE, { path: '/' });
      next(error);
    }
  }

  async logout(_req: Request, res: Response, next: NextFunction) {
    try {
      res.clearCookie(REFRESH_COOKIE, { path: '/' });
      res.json({ message: 'Desconectado com sucesso' });
    } catch (error) {
      next(error);
    }
  }

  async requestPasswordReset(req: Request, res: Response, next: NextFunction) {
    try {
      const { email } = req.body;
      const result = await this.authService.requestPasswordReset(email);
      res.json(result);
    } catch (error) {
      next(error);
    }
  }

  async resetPassword(req: Request, res: Response, next: NextFunction) {
    try {
      const { token, newPassword } = req.body;
      const result = await this.authService.resetPassword(token, newPassword);
      res.json(result);
    } catch (error) {
      next(error);
    }
  }

  async deleteAccount(req: Request, res: Response, next: NextFunction) {
    try {
      if (!req.user?.id) {
        throw new AppError('UNAUTHORIZED', 'Usuário não autenticado', 401);
      }

      const result = await this.authService.deleteAccount(req.user.id);
      res.clearCookie(REFRESH_COOKIE, { path: '/' });
      res.json(result);
    } catch (error) {
      next(error);
    }
  }
}
