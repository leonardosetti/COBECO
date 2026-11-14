import { Page, APIResponse } from '@playwright/test';

export const API_BASE = '/v1';

export async function apiRequest(
  page: Page,
  method: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH',
  endpoint: string,
  data?: unknown,
  token?: string
): Promise<APIResponse> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  return page.request.fetch(`${API_BASE}${endpoint}`, {
    method,
    headers,
    data: data ? JSON.stringify(data) : undefined,
  });
}

export async function loginViaApi(page: Page, usuario: string, senha: string): Promise<string> {
  const response = await apiRequest(page, 'POST', '/auth/login', { nome_usuario: usuario, senha });
  const body = await response.json();
  return body.access_token;
}

export async function cadastrarViaApi(page: Page, data: {
  nome_usuario: string;
  email: string;
  nome: string;
  senha: string;
  pergunta_seguranca: string;
  resposta_seguranca: string;
}): Promise<APIResponse> {
  return apiRequest(page, 'POST', '/auth/cadastrar', data);
}

export async function getPerfilViaApi(page: Page, token: string): Promise<APIResponse> {
  return apiRequest(page, 'GET', '/auth/perfil', undefined, token);
}

export async function atualizarPerfilViaApi(page: Page, token: string, data: {
  email?: string;
  nome?: string;
  senha_atual?: string;
  nova_senha?: string;
}): Promise<APIResponse> {
  return apiRequest(page, 'PUT', '/auth/perfil', data, token);
}

export async function criarListaViaApi(page: Page, token: string, data: {
  titulo: string;
  descricao?: string;
  publica?: boolean;
}): Promise<APIResponse> {
  return apiRequest(page, 'POST', '/listas', data, token);
}

export async function listarMinhasListasViaApi(page: Page, token: string): Promise<APIResponse> {
  return apiRequest(page, 'GET', '/listas/minhas', undefined, token);
}

export async function obterListaViaApi(page: Page, token: string, listaId: string): Promise<APIResponse> {
  return apiRequest(page, 'GET', `/listas/${listaId}`, undefined, token);
}

export async function atualizarListaViaApi(page: Page, token: string, listaId: string, data: {
  titulo?: string;
  descricao?: string;
  publica?: boolean;
}): Promise<APIResponse> {
  return apiRequest(page, 'PUT', `/listas/${listaId}`, data, token);
}

export async function excluirListaViaApi(page: Page, token: string, listaId: string): Promise<APIResponse> {
  return apiRequest(page, 'DELETE', `/listas/${listaId}`, undefined, token);
}

export function generateTestUser(suffix?: string): {
  nome_usuario: string;
  email: string;
  nome: string;
  senha: string;
  confirmar_senha: string;
  pergunta_seguranca: string;
  resposta_seguranca: string;
} {
  const ts = suffix || Date.now().toString();
  return {
    nome_usuario: `test_${ts}`,
    email: `test_${ts}@example.com`,
    nome: `Test User ${ts}`,
    senha: 'Senha@123',
    confirmar_senha: 'Senha@123',
    pergunta_seguranca: 'nome_mae',
    resposta_seguranca: 'Maria Silva',
  };
}

export function generateListaData(suffix?: string): {
  titulo: string;
  descricao: string;
  publica: boolean;
} {
  const ts = suffix || Date.now().toString();
  return {
    titulo: `Lista de Teste ${ts}`,
    descricao: `Descrição da lista de teste ${ts}`,
    publica: false,
  };
}

export async function waitForToast(page: Page, message?: string, timeout = 5000): Promise<void> {
  const toast = page.locator('.toast, [role="alert"], .alert').first();
  await expect(toast).toBeVisible({ timeout });
  if (message) {
    await expect(toast).toContainText(message);
  }
}

import { expect } from '@playwright/test';