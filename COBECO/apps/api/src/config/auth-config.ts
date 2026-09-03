import { randomBytes } from 'crypto';

/**
 * Valores que já circularam em `.env.example` ou em código de exemplo.
 * Nunca podem ser aceitos como segredo real.
 */
const PLACEHOLDER_SECRETS = new Set([
  'secret',
  'change-me',
  'your-access-secret-key-change-in-production',
  'your-refresh-secret-key-change-in-production',
]);

const MIN_SECRET_LENGTH = 32;

interface AuthSecrets {
  accessSecret: string;
  refreshSecret: string;
}

let cached: AuthSecrets | null = null;

function isUsable(value: string | undefined): value is string {
  if (!value) return false;
  const trimmed = value.trim();
  return trimmed.length >= MIN_SECRET_LENGTH && !PLACEHOLDER_SECRETS.has(trimmed);
}

function resolveSecret(variableName: 'JWT_ACCESS_SECRET' | 'JWT_REFRESH_SECRET'): string {
  const configured = process.env[variableName];
  if (isUsable(configured)) return configured.trim();

  if (process.env.NODE_ENV === 'production') {
    throw new Error(
      `${variableName} ausente ou inseguro. Defina um segredo próprio com pelo menos ${MIN_SECRET_LENGTH} caracteres antes de iniciar em produção.`
    );
  }

  console.warn(
    `[auth] ${variableName} ausente ou com valor de exemplo. Um segredo aleatório foi gerado para esta execução; as sessões serão invalidadas ao reiniciar a API.`
  );
  return randomBytes(48).toString('hex');
}

/**
 * Lê e valida os segredos de assinatura dos tokens.
 * Em produção falha na inicialização; em desenvolvimento gera segredos efêmeros.
 */
export function getAuthSecrets(): AuthSecrets {
  if (!cached) {
    const accessSecret = resolveSecret('JWT_ACCESS_SECRET');
    const refreshSecret = resolveSecret('JWT_REFRESH_SECRET');

    if (accessSecret === refreshSecret) {
      throw new Error(
        'JWT_ACCESS_SECRET e JWT_REFRESH_SECRET devem ser diferentes; caso contrário um refresh token é aceito como token de acesso.'
      );
    }

    cached = { accessSecret, refreshSecret };
  }

  return cached;
}

/** Apenas para testes: descarta os segredos memorizados. */
export function resetAuthSecretsCache(): void {
  cached = null;
}
