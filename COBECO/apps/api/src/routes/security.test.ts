import { afterAll, beforeAll, describe, expect, it } from 'vitest';
import type { Server } from 'http';
import type { AddressInfo } from 'net';
import { createApp } from '../app';

/**
 * Cobre o rate limiting de autenticação (RNF13/UC27) e a exclusão lógica de
 * listas (RF09). Cada bloco sobe a própria instância, porque a contagem do
 * limitador vive na aplicação e não deve vazar entre testes.
 */
async function startServer(): Promise<{ server: Server; baseUrl: string }> {
  const server = createApp().listen(0);
  await new Promise((resolve) => server.once('listening', resolve));
  return { server, baseUrl: `http://127.0.0.1:${(server.address() as AddressInfo).port}` };
}

function client(baseUrl: string) {
  return async (path: string, init: RequestInit = {}) => {
    const response = await fetch(`${baseUrl}${path}`, {
      ...init,
      headers: { 'Content-Type': 'application/json', ...(init.headers || {}) },
    });
    const text = await response.text();
    return { status: response.status, body: text ? JSON.parse(text) : null };
  };
}

describe('rate limiting de autenticação (RNF13)', () => {
  let server: Server;
  let call: ReturnType<typeof client>;

  beforeAll(async () => {
    const started = await startServer();
    server = started.server;
    call = client(started.baseUrl);
  });

  afterAll(async () => {
    await new Promise((resolve) => server.close(resolve));
  });

  it('bloqueia o login após 5 tentativas na mesma janela', async () => {
    const attempt = () =>
      call('/api/auth/login', {
        method: 'POST',
        body: JSON.stringify({ identifier: 'ninguem@example.com', password: 'Senha1234!' }),
      });

    for (let index = 0; index < 5; index += 1) {
      expect((await attempt()).status).toBe(401);
    }

    const blocked = await attempt();
    expect(blocked.status).toBe(429);
    expect(blocked.body.error.code).toBe('RATE_LIMIT_EXCEEDED');
    expect(blocked.body.error.message).toMatch(/tente novamente em/i);
  });
});

describe('exclusão lógica de listas (RF09)', () => {
  let server: Server;
  let call: ReturnType<typeof client>;

  const credentials = {
    name: 'Pessoa Soft Delete',
    username: 'soft_delete',
    email: 'soft.delete@example.com',
    password: 'Senha1234!',
    consent: true,
  };

  beforeAll(async () => {
    const started = await startServer();
    server = started.server;
    call = client(started.baseUrl);
  });

  afterAll(async () => {
    await new Promise((resolve) => server.close(resolve));
  });

  it('some com a lista excluída sem apagar o registro do usuário', async () => {
    await call('/api/auth/sign-up', { method: 'POST', body: JSON.stringify(credentials) });
    const login = await call('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ identifier: credentials.username, password: credentials.password }),
    });
    const auth = { Authorization: `Bearer ${login.body.accessToken}` };

    const created = await call('/api/platform/lists', {
      method: 'POST',
      headers: auth,
      body: JSON.stringify({ name: 'Lista descartável' }),
    });
    const listId: string = created.body.id;

    expect((await call('/api/platform/lists', { headers: auth })).body).toHaveLength(1);

    const removed = await call(`/api/platform/lists/${listId}`, { method: 'DELETE', headers: auth });
    expect(removed.status).toBe(200);

    expect((await call('/api/platform/lists', { headers: auth })).body).toHaveLength(0);

    const quote = await call(`/api/platform/lists/${listId}/quote`, {
      method: 'POST',
      headers: auth,
      body: JSON.stringify({ supplierIds: ['supplier-a', 'supplier-b'] }),
    });
    expect(quote.status).toBe(404);
    expect(quote.body.error.code).toBe('LIST_NOT_FOUND');
  });
});
