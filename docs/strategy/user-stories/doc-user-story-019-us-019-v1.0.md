---
id: doc-user-story-019-us-019-v1.0
type: doc-user-story
title: DOC USER STORY — Us 019
version: v1.0
status: ratificado
canonical: false
canonical_slug: us-019
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
domain: strategy
layer: user-story
tags: []
lgpd_class: n/a
workflow:
  stage: rascunho
  reviewer: null
  reviewed_at: null
  approval_hash: null
  board_url: null
---
# User Story — doc-user-story-019-us-019

**Título:** Visualizar Perfil  
**ID Único:** doc-user-story-019-us-019  
**Status:** Done  
**Sprint:** S4 | **Milestone:** S4: Export, Perfil e Polish  
**Prioridade:** P1  
**Story Points:** 2  
**Autor:** Leonardo Setti (PO)  
**Data Criação:** 15/09/2026  
**Data Atualização:** 20/10/2026  
**Rastreabilidade:** RF05, UC18, spec-004

---

## 1. História

Como **usuário autenticado**,  
eu quero **visualizar meus dados de perfil (nome de usuário read-only, email, nome, data de criação)**,  
para **confirmar minhas informações cadastradas**.

---

## 2. Critérios de Aceite — Gherkin

### Cenário 1: Visualizar perfil próprio
```gherkin
Dado que sou usuário autenticado
Quando acesso GET /v1/perfil
Então retorna 200 com JSON:
{
  "nome_usuario": "joao123",
  "email": "joao@email.com",
  "nome": "João Silva",
  "criado_em": "2026-09-22T10:30:00Z"
}
E campos: nome_usuario (read-only), email, nome, criado_em
E NÃO retorna: senha_hash, pergunta_seguranca, resposta_hash, deletado_em
```

### Cenário 2: Não autenticado → 401
```gherkin
Dado que não estou autenticado
Quando acesso GET /v1/perfil
Então retorna 401 "Não autenticado"
```

### Cenário 3: Frontend — Página Perfil somente leitura
```gherkin
Dado que estou autenticado e acesso página "Meu Perfil"
Quando a página carrega
Então exibe: Nome de Usuário (desabilitado), Email, Nome, Data de Cadastro
E botão "Editar Perfil" leva para página de edição (doc-user-story-020-us-020)
E NÃO mostra senha, pergunta segurança, resposta
```

---

## 3. Critérios — Tabela

| # | Critério | Tipo | Auto? | Teste | Status |
|---|----------|------|-------|-------|--------|
| AC-01 | GET /v1/perfil → 200 com nome_usuario, email, nome, criado_em | Funcional | Sim | `test_visualizar_perfil.py` | ✅ |
| AC-02 | Não retorna campos sensíveis (senha, pergunta, resposta) | Segurança | Sim | `test_visualizar_perfil_sem_sensiveis.py` | ✅ |
| AC-03 | Não autenticado → 401 | Segurança | Sim | `test_visualizar_perfil_401.py` | ✅ |
| AC-04 | Frontend: Página read-only com botão Editar | Frontend | Sim (E2E) | `test_visualizar_perfil_frontend.py` | ✅ |

---

## 4. Tarefas Técnicas

| Task ID | Descrição | Camada | Est. | Resp. | Status | Branch |
|---------|-----------|--------|------|-------|--------|--------|
| TA-180 | Backend: GET /v1/perfil — select campos permitidos, exclui sensíveis | Backend | 1 | Fabrício | ✅ | `feat/UC-18-visualizar-perfil` |
| TA-181 | Testes: campos retornados, sensíveis ausentes, 401 | Backend | 1 | Nicolas | ✅ | `feat/UC-18-visualizar-perfil` |
| TA-182 | Frontend: Página Perfil — cards read-only, botão "Editar" → /perfil/editar | Frontend | 2 | Eduardo | ✅ | `feat/UC-18-visualizar-perfil` |

---

## 5. DoD

- [x] Endpoint GET /v1/perfil autenticado (JWT)
- [x] Retorna apenas: nome_usuario, email, nome, criado_em
- [x] Exclui: senha_hash, pergunta_seguranca, resposta_hash, deletado_em
- [x] 401 se não autenticado
- [x] Frontend: layout limpo, botão Editar
- [x] Testes ≥80%, Code review, CI, CCB

---

## 6. Rastreabilidade

| Artefato | ID |
|----------|-----|
| req-func-0001-requisitos-funcionais-canon.md | RF05 |
| req-use-case-0001-casos-de-uso-canon.md | UC18 |
| spec-004 | Spec ID |
| Branch | `feat/UC-18-visualizar-perfil` |

---

## 7. Notas

- **nome_usuario Read-only:** Não pode ser alterado (regra de negócio — identidade única).
- **Email/Nome Editáveis:** Via doc-user-story-020-us-020 (Gerenciar Perfil).
- **Criado_em:** Timestamp imutável do cadastro.

---

**Fim doc-user-story-019-us-019**