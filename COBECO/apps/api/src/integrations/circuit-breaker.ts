import { ProviderError } from './provider-error';

interface CircuitBreakerOptions {
  failureThreshold?: number;
  resetTimeoutMs?: number;
  now?: () => number;
}

export class CircuitBreaker {
  private failures = 0;
  private openedAt: number | null = null;
  private halfOpenRequest = false;
  private readonly failureThreshold: number;
  private readonly resetTimeoutMs: number;
  private readonly now: () => number;

  constructor(options: CircuitBreakerOptions = {}) {
    this.failureThreshold = options.failureThreshold ?? 3;
    this.resetTimeoutMs = options.resetTimeoutMs ?? 30_000;
    this.now = options.now ?? Date.now;
  }

  async execute<T>(action: () => Promise<T>): Promise<T> {
    if (this.isOpen()) {
      if (!this.canTryAgain()) {
        throw new ProviderError('PROVIDER_CIRCUIT_OPEN', 'A fonte foi pausada temporariamente após falhas consecutivas.');
      }
      if (this.halfOpenRequest) {
        throw new ProviderError('PROVIDER_CIRCUIT_OPEN', 'A fonte ainda está em recuperação.');
      }
      this.halfOpenRequest = true;
    }

    try {
      const result = await action();
      this.reset();
      return result;
    } catch (error) {
      this.recordFailure();
      throw error;
    } finally {
      this.halfOpenRequest = false;
    }
  }

  private isOpen(): boolean {
    return this.openedAt !== null;
  }

  private canTryAgain(): boolean {
    return this.openedAt !== null && this.now() - this.openedAt >= this.resetTimeoutMs;
  }

  private recordFailure(): void {
    this.failures += 1;
    if (this.failures >= this.failureThreshold) this.openedAt = this.now();
  }

  private reset(): void {
    this.failures = 0;
    this.openedAt = null;
  }
}
