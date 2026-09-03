import { Router } from 'express';
import { AuthController } from '../controllers/auth.controller';
import { validateBody } from '../middleware/validation.middleware';
import {
  createAuthRateLimiter,
  createPasswordResetRateLimiter,
} from '../middleware/rate-limit.middleware';
import {
  signUpSchema,
  loginSchema,
  requestPasswordResetSchema,
  resetPasswordSchema,
} from '../validators/auth.validator';

export function createAuthRoutes(authController: AuthController): Router {
  const router = Router();

  // RNF13/UC27: cada limitador tem contagem própria, para que o cadastro não
  // consuma a janela do login.
  const signUpLimiter = createAuthRateLimiter();
  const loginLimiter = createAuthRateLimiter();
  const passwordResetLimiter = createPasswordResetRateLimiter();

  router.post('/sign-up', signUpLimiter, validateBody(signUpSchema), (req, res, next) =>
    authController.signUp(req, res, next)
  );

  router.post('/login', loginLimiter, validateBody(loginSchema), (req, res, next) =>
    authController.login(req, res, next)
  );

  router.post('/refresh', (req, res, next) => authController.refresh(req, res, next));

  router.post('/logout', (req, res, next) => authController.logout(req, res, next));

  router.post(
    '/request-password-reset',
    validateBody(requestPasswordResetSchema),
    passwordResetLimiter,
    (req, res, next) => authController.requestPasswordReset(req, res, next)
  );

  router.post('/reset-password', validateBody(resetPasswordSchema), (req, res, next) =>
    authController.resetPassword(req, res, next)
  );

  return router;
}
