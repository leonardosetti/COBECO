---
id: doc-auth-guide-0001-autenticacao-v1.0
type: doc-auth-guide
title: DOC AUTH GUIDE — Autenticacao
version: v1.0
status: ratificado
canonical: false
canonical_slug: autenticacao
created: '2026-11-14'
updated: '2026-11-14'
author: Leonardo Setti (@leonardosetti)
owner: CCB
ratified_by: null
ratified_at: null
supersedes: null
superseded_by: null
trace:
  constitution: []
  req_func: []
  req_nfunc: []
  use_cases: []
  specs: []
  handoffs: []
  adrs: []
  code: []
  tests: []
domain: operation
layer: guide
tags: []
lgpd_class: n/a
workflow:
  stage: rascunho
  reviewer: null
  reviewed_at: null
  approval_hash: null
  board_url: null
---
# Guia de Autenticação — COBECO MVP

**Público:** Desenvolvedores do projeto COBECO  
**Versão:** 1.0  
**Data:** 13/11/2026  
**Status:** Vigente

---

## 1. O que este documento cobre

Este guia explica como funciona a autenticação do COBECO MVP, com foco no botão **Authorize** do Swagger UI, quem se autentica, fluxo de tokens JWT e exemplos reprodutíveis.

---

## 2. Quem se autentica?

### ✅ Usuário da aplicação COBECO

A autenticação é **do usuário final da aplicação COBECO** (Visitante ou Usuário Autenticado), cadastrado no banco de dados (`tabela usuarios`).

### ❌ Não é autenticação de desenvolvedor

O desenvolvedor usa o Swagger para **testar como se fosse um usuário comum** da aplicação. Não existe "login de admin do desenvolvedor". Se não houver um usuário cadastrado no banco, não é possível autenticar.

---

## 3. O botão "Authorize" do Swagger

### O que é

O botão **Authorize** (ícone de cadeado 🔒) no topo do Swagger UI (`/v1/docs`) permite inserir o **token de acesso (JWT)** obtido após login. Uma vez autorizado, o Swagger envia automaticamente:

```
Authorization: Bearer <seu_token_jwt>
```

em todas as requisições de endpoints protegidos.

### Como usar (passo a passo)

```bash
# Passo 1: Cadastre um usuário (se ainda não tiver)
curl -X POST http://localhost:8380/v1/auth/cadastrar \
  -H "Content-Type: application/json" \
  -d '{"nome_usuario":"devtest","email":"dev@test.com","nome":"Dev Teste","senha":"Senha@123","confirmar_senha":"Senha@123","pergunta_seguranca":"Qual o nome do seu pet?","resposta_seguranca":"Fluffy"}'

# Passo 2: Faça login e obtenha o access_token
curl -X POST http://localhost:8380/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"nome_usuario":"devtest","senha":"Senha@123"}'

# Resposta:
# {"access_token":"eyJhbG...","refresh_token":"...","token_type":"bearer","expires_in":900}

# Passo 3: No Swagger UI (http://localhost:8380/v1/docs):
# 1. Clique no botão "Authorize" (🔒)
# 2. Cole: Bearer eyJhbG... (apenas o access_token)
# 3. Clique em "Authorize" e depois em "Close"
# 4. Teste endpoints protegidos (ex: POST /v1/listas)
```

---

## 4. Endpoints protegidos vs públicos

### 🔓 Públicos (sem cadeado)

| Método | Endpoint |
|--------|----------|
| POST | `/v1/auth/cadastrar` |
| POST | `/v1/auth/login` |
| POST | `/v1/auth/recuperar-senha/solicitar` |
| POST | `/v1/auth/recuperar-senha/confirmar` |
| GET | `/v1/catalogo/categorias` |
| GET | `/v1/catalogo/fornecedores` |
| GET | `/v1/catalogo/produtos/autocomplete` |
| GET | `/v1/health` |
| GET | `/v1/openapi.json` |

### 🔒 Protegidos (com cadeado — exigem token válido)

| Método | Endpoint |
|--------|----------|
| GET | `/v1/auth/perfil` |
| PUT | `/v1/auth/perfil` |
| POST | `/v1/auth/logout` |
| POST | `/v1/listas` |
| GET | `/v1/listas` |
| GET | `/v1/listas/{id}` |
| PUT | `/v1/listas/{id}` |
| DELETE | `/v1/listas/{id}` |
| POST | `/v1/listas/promover-efemera` |
| POST | `/v1/comparacao/calcular` |
| GET | `/v1/comparacao/visualizar/{id}` |
| POST | `/v1/export/pdf` |

> Sem token válido, a resposta é `401 Unauthorized`.

---

## 5. Tokens: Access vs Refresh

| Tipo | Onde fica | Validade | Uso |
|------|-----------|----------|-----|
| **Access Token** | `localStorage` (frontend) / colado no Swagger | 15 min | `Authorization: Bearer` em cada requisição protegida |
| **Refresh Token** | Cookie `httpOnly` + `SameSite=Strict` | 7 dias | Renovação automática do access token |

> Se o access token expirar, faça login novamente e cole o novo token no "Authorize" do Swagger.

---

## 6. Exemplo reprodutível (curl completo)

```bash
# 1. Cadastro
curl -s -X POST http://localhost:8380/v1/auth/cadastrar \
  -H "Content-Type: application/json" \
  -d '{"nome_usuario":"devjoao","email":"joao@test.com","nome":"João Silva","senha":"Senha@123","confirmar_senha":"Senha@123","pergunta_seguranca":"Qual o nome do seu primeiro cachorro?","resposta_seguranca":"Rex"}'

# 2. Login e extração do token
TOKEN=$(curl -s -X POST http://localhost:8380/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"nome_usuario":"devjoao","senha":"Senha@123"}' | \
  python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

# 3. Acesso a endpoint protegido
curl -s -X POST http://localhost:8380/v1/listas \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"nome":"Minha Lista","itens":[{"produto_id":1,"quantidade":2}]}'
```

---

## 7. Exemplo reprodutível (JavaScript / Fetch)

```javascript
async function cobecoFetch(endpoint, options = {}) {
  const token = localStorage.getItem('cobeco_access_token');
  const headers = { 'Content-Type': 'application/json', ...options.headers };
  if (token) headers['Authorization'] = `Bearer ${token}`;
  const response = await fetch(`http://localhost:8380/v1${endpoint}`, {
    ...options, headers, credentials: 'include',
  });
  if (response.status === 401) {
    localStorage.removeItem('cobeco_access_token');
    window.location.href = '/#/login';
    throw new Error('Sessão expirada');
  }
  return response;
}

// Uso:
await cobecoFetch('/listas', {
  method: 'POST',
  body: JSON.stringify({ nome: 'Lista da Semana', itens: [{ produto_id: 1, quantidade: 2 }] }),
});
```

---

## 8. Regras de validação (RF01)

| Campo | Regra |
|-------|-------|
| `nome_usuario` | 3-30 chars, alfanumérico (`^[a-zA-Z0-9]+$`), único |
| `email` | Válido, único |
| `nome` | 2-100 caracteres |
| `senha` | Mín. 8 chars, 1 maiúscula, 1 minúscula, 1 número, 1 especial |
| `pergunta_seguranca` | Mín. 5 caracteres |
| `resposta_seguranca` | Mín. 3 caracteres |

---

## 9. Regras de segurança

- Não commite tokens reais
- Não compartilhe access tokens (valem 15 min)
- Use cookies `httpOnly` para refresh tokens
- Valide propriedade da lista (usuário A não edita lista do Usuário B)
- Rate limiting: 6 req/15min no login

---

## 10. Links úteis

| Recurso | Link |
|---------|------|
| Swagger UI | http://localhost:8380/v1/docs |
| OpenAPI JSON | http://localhost:8380/v1/openapi.json |
| Frontend | http://localhost:8380/ |
| Health Check | http://localhost:8380/health |

---

**Fim do documento.**  
Dúvidas: abra uma issue no repositório ou consulte o Tech Lead.