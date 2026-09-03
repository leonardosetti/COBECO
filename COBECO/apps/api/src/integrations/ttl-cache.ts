interface CacheEntry<T> {
  value: T;
  expiresAt: number;
}

export class TtlCache<T> {
  private readonly entries = new Map<string, CacheEntry<T>>();
  private readonly inFlight = new Map<string, Promise<T>>();

  constructor(private readonly ttlMs: number, private readonly now: () => number = Date.now) {}

  async getOrSet(key: string, loader: () => Promise<T>): Promise<T> {
    const cached = this.entries.get(key);
    if (cached && cached.expiresAt > this.now()) return cached.value;
    if (cached) this.entries.delete(key);

    const pending = this.inFlight.get(key);
    if (pending) return pending;

    const request = loader()
      .then((value) => {
        this.entries.set(key, { value, expiresAt: this.now() + this.ttlMs });
        return value;
      })
      .finally(() => this.inFlight.delete(key));

    this.inFlight.set(key, request);
    return request;
  }

  clear(): void {
    this.entries.clear();
    this.inFlight.clear();
  }

  size(): number {
    return this.entries.size;
  }
}
