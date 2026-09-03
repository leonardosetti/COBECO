export type ProviderErrorCode =
  | 'PROVIDER_TIMEOUT'
  | 'PROVIDER_RATE_LIMIT'
  | 'PROVIDER_UNAVAILABLE'
  | 'PROVIDER_UNAUTHORIZED'
  | 'PROVIDER_INVALID_RESPONSE'
  | 'PROVIDER_CIRCUIT_OPEN';

export class ProviderError extends Error {
  constructor(
    public readonly code: ProviderErrorCode,
    message: string,
    public readonly cause?: unknown
  ) {
    super(message);
    this.name = 'ProviderError';
  }
}

export function isProviderError(error: unknown): error is ProviderError {
  return error instanceof ProviderError;
}
