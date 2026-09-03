import { afterAll, beforeAll, describe, expect, it } from 'vitest';
import type { Server } from 'http';
import type { AddressInfo } from 'net';
import { createApp } from '../app';

/**
 * Testes de integração das rotas: sobem a aplicação inteira em uma porta
 * efêmera e falam HTTP de verdade. Só uma chamada nesta camada já teria pego o
 * `import` de um `.d.ts` que impedia a API de iniciar.
 */
describe('rotas da API', () => {
  let server: Server;
  let baseUrl: string;

  const credentials = {
    name: 'Usuária de Teste',
    username: 'rotas_teste',
    email: 'Rotas.Teste@Example.com',
    password: 'Senha1234!',
    consent: true,
  };

  /**
   * O login tem rate limit de 5 tentativas por 15 minutos (RNF13). Reaproveitar
   * o token entre os testes evita que a própria suíte estoure a janela.
   */
  let cachedToken = '';

  async function authHeaders() {
    if (!cachedToken) {
      const login = await call('/api/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email: credentials.email, password: credentials.password }),
      });
      cachedToken = login.body.accessToken;
    }
    return { Authorization: `Bearer ${cachedToken}` };
  }

  async function call(path: string, init: RequestInit = {}) {
    const response = await fetch(`${baseUrl}${path}`, {
      ...init,
      headers: { 'Content-Type': 'application/json', ...(init.headers || {}) },
    });
    const text = await response.text();
    return { status: response.status, body: text ? JSON.parse(text) : null, response };
  }

  beforeAll(async () => {
    process.env.PRICE_PROVIDERS = 'mock';
    server = createApp().listen(0);
    await new Promise((resolve) => server.once('listening', resolve));
    baseUrl = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
  });

  afterAll(async () => {
    await new Promise((resolve) => server.close(resolve));
  });

  it('sobe a aplicação e responde ao health check', async () => {
    const { status, body } = await call('/health');
    expect(status).toBe(200);
    expect(body).toEqual({ status: 'ok' });
  });

  it('serve as rotas públicas sem autenticação', async () => {
    const retailers = await call('/api/public/retailers');
    expect(retailers.status).toBe(200);
    expect(Array.isArray(retailers.body)).toBe(true);

    const testimonials = await call('/api/public/testimonials');
    expect(testimonials.status).toBe(200);
  });

  it('bloqueia as rotas da plataforma sem token', async () => {
    const { status, body } = await call('/api/platform/lists');
    expect(status).toBe(401);
    expect(body.error.code).toBe('MISSING_TOKEN');
  });

  it('recusa o cadastro sem consentimento explícito', async () => {
    const { status, body } = await call('/api/auth/sign-up', {
      method: 'POST',
      body: JSON.stringify({
        ...credentials,
        username: 'sem_consent',
        email: 'sem.consent@example.com',
        consent: false,
      }),
    });
    expect(status).toBe(400);
    expect(body.error.message).toMatch(/aceitar o tratamento/i);
  });

  it('percorre cadastro, login e uso autenticado das listas', async () => {
    const signUp = await call('/api/auth/sign-up', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
    expect(signUp.status).toBe(201);
    expect(signUp.body.email).toBe('rotas.teste@example.com');

    // Caixa diferente da usada no cadastro: o login normaliza o e-mail.
    const login = await call('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email: 'ROTAS.TESTE@example.com', password: credentials.password }),
    });
    expect(login.status).toBe(200);

    cachedToken = login.body.accessToken;
    const auth = { Authorization: `Bearer ${cachedToken}` };

    const created = await call('/api/platform/lists', {
      method: 'POST',
      headers: auth,
      body: JSON.stringify({ name: 'Lista de teste' }),
    });
    expect(created.status).toBe(201);

    const listId: string = created.body.id;

    // Regressão: a rota de duplicação não validava o corpo e quebrava com 500.
    const invalidDuplicate = await call(`/api/platform/lists/${listId}/duplicate`, {
      method: 'POST',
      headers: auth,
      body: JSON.stringify({ name: 123 }),
    });
    expect(invalidDuplicate.status).toBe(400);
    expect(invalidDuplicate.body.error.code).toBe('VALIDATION_ERROR');

    const duplicate = await call(`/api/platform/lists/${listId}/duplicate`, {
      method: 'POST',
      headers: auth,
      body: JSON.stringify({}),
    });
    expect(duplicate.status).toBe(201);
    expect(duplicate.body.name).toBe('Lista de teste (cópia)');
  });

  it('expõe o catálogo e gera os quatro grupos de paridade A-H', async () => {
    const auth = await authHeaders();
    const categories = await call('/api/platform/categories', { headers: auth });
    expect(categories.status).toBe(200);
    const categoryId = categories.body[0].id;
    const suppliers = await call(`/api/platform/categories/${categoryId}/suppliers`, {
      headers: auth,
    });
    const products = await call(`/api/platform/categories/${categoryId}/products`, {
      headers: auth,
    });
    expect(suppliers.body).toHaveLength(8);

    const created = await call('/api/platform/lists', {
      method: 'POST',
      headers: auth,
      body: JSON.stringify({ name: 'Paridade', categoryId }),
    });
    const items = products.body.slice(0, 9).map((product: { id: string; name: string }) => ({
      description: product.name,
      productId: product.id,
      quantity: 1,
    }));
    await call(`/api/platform/lists/${created.body.id}/items/bulk`, {
      method: 'POST',
      headers: auth,
      body: JSON.stringify({ items }),
    });
    const allSupplierIds = suppliers.body.map((supplier: { id: string }) => supplier.id);
    const quotation = await call(`/api/platform/lists/${created.body.id}/quote`, {
      method: 'POST',
      headers: auth,
      body: JSON.stringify({ supplierIds: allSupplierIds }),
    });
    expect(quotation.status).toBe(200);
    expect(quotation.body.groups).toHaveLength(4);
    expect(quotation.body.groups[0]).toMatchObject({ coverage: 100 });
    expect(quotation.body.bestGroupId).toBe(quotation.body.groups[0].groupId);

    // RF12: disponibilidade por fornecedor, já ordenada por nome.
    const availability = await call(`/api/platform/lists/${created.body.id}/suppliers`, {
      headers: auth,
    });
    expect(availability.status).toBe(200);
    expect(availability.body).toHaveLength(8);
    expect(availability.body[0]).toMatchObject({
      name: 'Fornecedor A',
      availableItems: 9,
      totalItems: 9,
      availability: 100,
    });
    // D cobre 6 dos 9 itens do cenário de paridade.
    const fornecedorD = availability.body.find(
      (entry: { name: string }) => entry.name === 'Fornecedor D'
    );
    expect(fornecedorD).toMatchObject({ availableItems: 6, availability: 66.67 });

    // RF11: a comparação exige de 2 a 10 fornecedores.
    const poucos = await call(`/api/platform/lists/${created.body.id}/quote`, {
      method: 'POST',
      headers: auth,
      body: JSON.stringify({ supplierIds: allSupplierIds.slice(0, 1) }),
    });
    expect(poucos.status).toBe(400);
    expect(poucos.body.error.message).toMatch(/ao menos 2 fornecedores/i);

    const demais = await call(`/api/platform/lists/${created.body.id}/quote`, {
      method: 'POST',
      headers: auth,
      body: JSON.stringify({
        supplierIds: Array.from({ length: 11 }, (_, index) => `supplier-${index}`),
      }),
    });
    expect(demais.status).toBe(400);
    expect(demais.body.error.message).toMatch(/no máximo 10 fornecedores/i);
  });

  it('autentica pelo nome de usuário, e não só pelo e-mail (RF02)', async () => {
    const login = await call('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ identifier: credentials.username, password: credentials.password }),
    });
    expect(login.status).toBe(200);
    expect(login.body.user.username).toBe('rotas_teste');
  });

  it('renova a sessão pelo cookie de refresh e rejeita o refresh como token de acesso', async () => {
    await call('/api/auth/sign-up', {
      method: 'POST',
      body: JSON.stringify({
        ...credentials,
        username: 'refresh_teste',
        email: 'refresh.teste@example.com',
      }),
    });

    const login = await call('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email: 'refresh.teste@example.com', password: credentials.password }),
    });

    const setCookie = login.response.headers.get('set-cookie') || '';
    expect(setCookie).toMatch(/refreshToken=/);
    expect(setCookie).toMatch(/HttpOnly/i);

    const cookie = setCookie.split(';')[0];
    const refreshValue = cookie.split('=')[1];

    // O refresh token não pode valer como credencial de acesso.
    const misuse = await call('/api/platform/lists', {
      headers: { Authorization: `Bearer ${refreshValue}` },
    });
    expect(misuse.status).toBe(401);

    const refreshed = await call('/api/auth/refresh', { method: 'POST', headers: { cookie } });
    expect(refreshed.status).toBe(200);
    expect(typeof refreshed.body.accessToken).toBe('string');

    const withNewToken = await call('/api/platform/lists', {
      headers: { Authorization: `Bearer ${refreshed.body.accessToken}` },
    });
    expect(withNewToken.status).toBe(200);
  });

  it('recusa o refresh sem cookie', async () => {
    const { status, body } = await call('/api/auth/refresh', { method: 'POST' });
    expect(status).toBe(401);
    expect(body.error.code).toBe('SESSION_EXPIRED');
  });

  it('aplica o teto de paginação do histórico', async () => {
    const auth = await authHeaders();

    const ok = await call('/api/platform/quotations/history?page=1&pageSize=20', { headers: auth });
    expect(ok.status).toBe(200);
    expect(ok.body.pageSize).toBe(20);

    const tooBig = await call('/api/platform/quotations/history?page=1&pageSize=999', {
      headers: auth,
    });
    expect(tooBig.status).toBe(400);
    expect(tooBig.body.error.code).toBe('VALIDATION_ERROR');
  });
});
