// COBECO Performance Tests — k6 Script
// Teste de carga para Comparação de Preços (RNF11: <10s para 100 itens × 10 fornecedores)
// Teste de carga para Exportação PDF (RNF11: <5s para 100 itens)

import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

// Configuração do teste
export const options = {
  stages: [
    { duration: '30s', target: 10 },   // Ramp up
    { duration: '1m', target: 20 },    // Carga sustentada
    { duration: '30s', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<10000'],      // RNF11: comparação < 10s (p95)
    http_req_failed: ['rate<0.01'],          // < 1% falhas
    'comparacao_duration': ['p(95)<10000'],  // Métrica customizada
    'pdf_generation_duration': ['p(95)<5000'], // RNF11: PDF < 5s
  },
};

// Métricas customizadas
const comparacaoDuration = new Trend('comparacao_duration');
const pdfGenerationDuration = new Trend('pdf_generation_duration');
const errorRate = new Rate('errors');

// Configuração base
const BASE_URL = __ENV.BASE_URL || 'http://localhost:8380';
const API_BASE = `${BASE_URL}/v1`;

// Headers comuns
const headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
};

// Estado compartilhado
let authToken = null;
let refreshToken = null;
let userId = null;
let listaId = null;
let fornecedorIds = [];

export function setup() {
  // Setup: cria usuário, login, lista e obtém IDs necessários
  const userData = {
    nome_usuario: `k6_user_${Date.now()}`,
    email: `k6_${Date.now()}@test.com`,
    nome: 'K6 Test User',
    senha: 'Senha@123',
    confirmar_senha: 'Senha@123',
    pergunta_seguranca: 'nome_mae',
    resposta_seguranca: 'Maria Silva',
  };

  // 1. Cadastra usuário
  let res = http.post(`${API_BASE}/auth/cadastrar`, JSON.stringify({
    nome_usuario: `k6_user_${Date.now()}`,
    email: `k6_${Date.now()}@test.com`,
    nome: 'K6 Test User',
    senha: 'Senha@123',
    confirmar_senha: 'Senha@123',
    pergunta_seguranca: 'nome_mae',
    resposta_seguranca: 'Maria Silva',
  }), { headers: { 'Content-Type': 'application/json' } });

  if (res.status !== 201) {
    throw new Error(`Falha ao cadastrar usuário: ${res.status} ${res.body}`);
  }

  // 2. Login
  res = http.post(`${API_BASE}/auth/login`, JSON.stringify({
    nome_usuario: `k6_user_${Date.now()}`,
    senha: 'Senha@123',
  }), { headers: { 'Content-Type': 'application/json' } });

  if (res.status !== 200) {
    throw new Error(`Falha no login: ${res.status} ${res.body}`);
  }

  const loginData = res.json();
  const token = loginData.access_token;
  const refresh = loginData.refresh_token;

  // 3. Obtém produtos para criar lista
  const headers = { 
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
  };

  let prodRes = http.get(`${API_BASE}/catalogo/produtos?limit=20`, { headers });
  const produtos = prodRes.json().items || [];

  if (produtos.length < 5) {
    throw new Error('Não há produtos suficientes no catálogo');
  }

  // 4. Cria lista com itens
  const itens = produtos.slice(0, 10).map((p, i) => ({
    produto_id: p.id,
    quantidade: (i % 5) + 1,
  }));

  const listaRes = http.post(`${API_BASE}/listas`, JSON.stringify({
    nome: `Lista K6 Performance ${Date.now()}`,
    itens: itens,
  }), { headers: { ...headers, 'Content-Type': 'application/json' } });

  if (listaRes.status !== 201) {
    throw new Error(`Falha ao criar lista: ${listaRes.status} ${listaRes.body}`);
  }

  const lista = listaRes.json();

  // 5. Obtém fornecedores
  const fornRes = http.get(`${API_BASE}/catalogo/fornecedores`, { headers });
  const fornecedores = fornRes.json() || [];
  const fornecedorIds = fornecedores.slice(0, 10).map(f => f.id);

  return {
    token,
    refreshToken: refresh,
    listaId: lista.id,
    fornecedorIds: fornecedorIds.slice(0, 10),
  };
}

export default function (data) {
  const { token, listaId, fornecedorIds } = data;
  
  const headers = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
  };

  // ==========================================
  // TESTE 1: Comparação de Preços (RNF11: <10s)
  // ==========================================
  const comparacaoStart = new Date();
  
  const compRes = http.post(`${API_BASE}/comparacao`, JSON.stringify({
    lista_id: data.listaId,
    fornecedor_ids: fornecedorIds.slice(0, 10),
    disponibilidade_minima: 0.0,
  }), { headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${data.token}` } });

  const comparacaoDuration = new Date() - comparacaoStart;
  comparacaoDuration.add(comparacaoDuration);

  const compCheck = check(compRes, {
    'comparacao status 200': (r) => r.status === 200,
    'tem fornecedores': (r) => {
      const data = r.json();
      return data.fornecedores && data.fornecedores.length > 0;
    },
    'ordenado por preco ASC': (r) => {
      const data = r.json();
      const precos = data.fornecedores.map(f => parseFloat(f.preco_total));
      for (let i = 1; i < precos.length; i++) {
        if (precos[i] < precos[i - 1]) return false;
      }
      return true;
    },
    'tem melhor_fornecedor_id': (r) => {
      const data = r.json();
      return data.melhor_fornecedor_id !== null;
    },
  });

  errorRate.add(!compCheck);

  // ==========================================
  // TESTE 2: Exportação PDF (RNF11: <5s)
  // ==========================================
  // Pega ID de uma lista existente (cria uma nova se necessário)
  const listaId = data.listaId;
  
  const pdfStart = new Date();
  
  const pdfRes = http.get(`${BASE_URL}/v1/export/lista/${data.listaId}/pdf`, {
    headers: { 'Authorization': `Bearer ${data.token}` },
    responseType: 'binary', // Importante para binário
  });

  const pdfDuration = new Date() - pdfStart;
  pdfGenerationDuration.add(pdfDuration);

  const pdfCheck = check(pdfRes, {
    'pdf status 200': (r) => r.status === 200,
    'content-type pdf': (r) => r.headers['Content-Type'] === 'application/pdf',
    'pdf válido': (r) => r.body && r.body.startsWith('%PDF-'),
    'tamanho razoável': (r) => r.body && r.body.length > 1000,
  });

  errorRate.add(!pdfCheck);

  // ==========================================
  // TESTE 3: Login concorrente
  // ==========================================
  // (Simula múltiplos usuários logando simultaneamente)
  if (__ITER % 10 === 0) {
    const loginRes = http.post(`${API_BASE}/auth/login`, JSON.stringify({
      nome_usuario: `k6_user_${Date.now()}`,
      senha: 'Senha@123',
    }), { headers: { 'Content-Type': 'application/json' } });

    check(loginRes, {
      'login status 200': (r) => r.status === 200,
      'tem access_token': (r) => r.json().access_token !== undefined,
      'tem refresh_token cookie': (r) => r.headers['Set-Cookie']?.includes('refresh_token='),
    });
  }

  sleep(1); // Think time
}

export function teardown(data) {
  // Cleanup: revoga tokens, limpa dados de teste se necessário
  if (data.token) {
    const headers = { 'Authorization': `Bearer ${data.token}` };
    http.post(`${API_BASE}/auth/logout`, null, { headers });
  }
}

// Helper para métricas
export function handleSummary(data) {
  return {
    'stdout': textSummary(data, { indent: ' ', enableColors: true }),
    'summary.json': JSON.stringify(data, null, 2),
  };
}

function textSummary(data, options) {
  // Formata resumo para console
  let out = '\n=== K6 Performance Test Summary ===\n';
  out += `Total Requests: ${data.metrics.http_reqs?.values?.count || 0}\n`;
  out += `Failed Rate: ${(data.metrics.http_req_failed?.values?.rate * 100).toFixed(2)}%\n`;
  out += `Avg Duration: ${data.metrics.http_req_duration?.values?.avg?.toFixed(2)}ms\n`;
  out += `p95 Duration: ${data.metrics.http_req_duration?.values?.['p(95)']?.toFixed(2)}ms\n`;
  
  if (data.metrics.comparacao_duration) {
    out += `\nComparação p95: ${data.metrics.comparacao_duration.values['p(95)']?.toFixed(2)}ms (RNF11: <10000ms)\n`;
  }
  
  if (data.metrics.pdf_generation_duration) {
    out += `PDF Generation p95: ${data.metrics.pdf_generation_duration.values['p(95)']?.toFixed(2)}ms (RNF11: <5000ms)\n`;
  }
  
  out += '\nThresholds:\n';
  for (const [name, threshold] of Object.entries(data.thresholds)) {
    const passed = threshold.ok ? '✅ PASS' : '❌ FAIL';
    out += `  ${name}: ${passed}\n`;
  }
  
  return out;
}