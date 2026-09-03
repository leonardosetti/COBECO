import { NextFunction, Request, Response } from 'express';
import { AppError } from '../types';

export interface RateLimitOptions {
  /** Tamanho da janela deslizante, em milissegundos. */
  windowMs: number;
  /** Quantidade de requisições permitidas dentro da janela. */
  max: number;
  /** Chave da contagem. Por padrão o IP (RNF13); o RF04 conta por e-mail. */
  keyOf?: (req: Request) => string | undefined;
  message: string;
}

/**
 * Limitador de taxa em memória (RNF13 / UC27).
 *
 * O estado vive na closure e não no módulo: cada `createApp()` começa com a
 * contagem zerada, de modo que um teste não herde a janela aberta por outro.
 * Para uma única instância de API isso basta; múltiplas réplicas exigiriam um
 * armazenamento compartilhado (Redis), fora do escopo do MVP.
 */
export function createRateLimiter({ windowMs, max, keyOf, message }: RateLimitOptions) {
  const hits = new Map<string, number[]>();

  function recent(key: string, now: number): number[] {
    return (hits.get(key) || []).filter((timestamp) => now - timestamp < windowMs);
  }

  return (req: Request, _res: Response, next: NextFunction) => {
    const now = Date.now();
    const key = (keyOf ? keyOf(req) : req.ip) || 'desconhecido';
    const attempts = recent(key, now);

    // Descarta janelas encerradas para o mapa não crescer indefinidamente.
    if (hits.size > 500) {
      for (const [candidate, timestamps] of hits) {
        if (!timestamps.some((timestamp) => now - timestamp < windowMs)) hits.delete(candidate);
      }
    }

    if (attempts.length >= max) {
      hits.set(key, attempts);
      const minutes = Math.max(1, Math.ceil((windowMs - (now - attempts[0])) / 60_000));
      return next(
        new AppError(
          'RATE_LIMIT_EXCEEDED',
          `${message} Tente novamente em ${minutes} ${minutes === 1 ? 'minuto' : 'minutos'}.`,
          429
        )
      );
    }

    attempts.push(now);
    hits.set(key, attempts);
    next();
  };
}

/** RF02: 5 tentativas de autenticação a cada 15 minutos, por IP. */
export function createAuthRateLimiter() {
  return createRateLimiter({
    windowMs: 15 * 60 * 1000,
    max: 5,
    message: 'Muitas tentativas de autenticação.',
  });
}

/** RF04: no máximo 3 pedidos de redefinição por hora, por e-mail. */
export function createPasswordResetRateLimiter() {
  return createRateLimiter({
    windowMs: 60 * 60 * 1000,
    max: 3,
    keyOf: (req) => String(req.body?.email || '').trim().toLowerCase() || req.ip,
    message: 'Muitos pedidos de redefinição para este e-mail.',
  });
}
