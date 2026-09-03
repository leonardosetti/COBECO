import { describe, expect, it, vi } from 'vitest';
import { fetchJson } from './http-client';

describe('fetchJson', () => {
  it('maps HTTP 429 to the rate-limit provider error', async () => {
    const fetchImplementation = vi.fn(async () => new Response('{}', { status: 429 })) as unknown as typeof fetch;

    await expect(
      fetchJson('https://example.test', { fetchImplementation, timeoutMs: 100 })
    ).rejects.toMatchObject({ code: 'PROVIDER_RATE_LIMIT' });
  });

  it('aborts requests that exceed the configured timeout', async () => {
    const fetchImplementation = vi.fn(
      (_url: string, init?: RequestInit) =>
        new Promise<Response>((_resolve, reject) => {
          init?.signal?.addEventListener('abort', () => reject(new Error('aborted')), { once: true });
        })
    ) as unknown as typeof fetch;

    await expect(
      fetchJson('https://example.test', { fetchImplementation, timeoutMs: 5 })
    ).rejects.toMatchObject({ code: 'PROVIDER_TIMEOUT' });
  });
});
