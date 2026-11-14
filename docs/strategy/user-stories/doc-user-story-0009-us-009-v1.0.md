---
id: doc-user-story-0009-us-009-v1.0
type: doc-user-story
title: DOC USER STORY — Us 009
version: v1.0
status: ratificado
canonical: false
canonical_slug: us-009
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
# User Story — doc-user-story-0009-us-009

**Título:** Listar Minhas Listas  
**ID Único:** doc-user-story-0009-us-009  
**Status:** Done  
**Sprint:** S2 | **Milestone:** S2: Listas e Catálogo  
**Prioridade:** P0  
**Story Points:** 3  
**Autor:** Leonardo Setti (PO)  
**Data Criação:** 15/09/2026  
**Data Atualização:** 06/10/2026  
**Rastreabilidade:** RF09, UC15, spec-004

---

## 1. História

Como **usuário autenticado**,  
eu quero **ver todas as minhas listas salvas com paginação, ordenação e filtro por nome**,  
para **encontrar e acessar rapidamente qualquer lista**.

---

## 2. Critérios de Aceite — Gherkin

### Cenário 1: Listar com paginação (20/página)
```gherkin
Dado que tenho 25 listas salvas
Quando acesso GET /v1/listas?page=1&size=20
Então retorna 20 listas + metadados {total: 25, page: 1, size: 20, total_pages: 2}
E cada lista: {id, nome, criado_em, atualizado_em, total_itens, valor_estimado}
```

### Cenário 2: Ordenação por criado_em DESC (padrão)
```gherkin
Dado que tenho listas de datas diferentes
Quando listo sem ordenação explícita
Então retorna ordenado por `criado_em DESC` (mais nova primeiro)
```

### Cenário 3: Filtro por nome (busca parcial, case-insensitive)
```gherkin
Dado que tenho listas "Compras Semana", "Compras Mês", "Farmácia"
Quando busco GET /v1/listas?nome=semana
Então retorna apenas "Compras Semana"
E busca é case-insensitive e parcial (ILIKE %termo%)
```

### Cenário 4: Soft delete — listas deletadas não aparecem
```gherkin
Dado que tenho lista "Antiga" com `deletado_em` preenchido
Quando listo minhas listas
Então "Antiga" NÃO aparece na resposta
```

### Cenário 5: Página 2
```gherkin
Dado que tenho 25 listas (20 por página)
Quando acesso GET /v1/listas?page=2&size=20
Então retorna 5 listas (página 2)
E metadados {total: 25, page: 2, size: 20, total_pages: 2}
```

---

## 3. Critérios — Tabela

| # | Critério | Tipo | Auto? | Teste | Status |
|---|----------|------|-------|-------|--------|
| AC-01 | Paginação 20/página + metadados total/pages | Funcional | Sim | `test_listar_paginacao.py` | ✅ |
| AC-02 | Ordenação padrão criado_em DESC | Funcional | Sim | `test_listar_ordenacao.py` | ✅ |
| AC-03 | Filtro nome ILIKE %termo% case-insensitive | Funcional | Sim | `test_listar_filtro_nome.py` | ✅ |
| AC-04 | Soft delete: `deletado_em` não nulo → excluído | Funcional | Sim | `test_listar_soft_delete.py` | ✅ |
| AC-05 | Frontend: Dashboard com tabela, paginação, input busca | Frontend | Sim (E2E) | `test_listar_frontend.py` | ✅ |

---

## 4. Tarefas Técnicas

| Task ID | Descrição | Camada | Est. | Resp. | Status | Branch |
|---------|-----------|--------|------|-------|--------|--------|
| TA-080 | Backend: GET /v1/listas — query params page, size, nome, ordenação, filtro deletado_em | Backend | 3 | Nicholas | ✅ | `feat/UC-15-listar-listas` |
| TA-081 | Backend: Índice composto (usuario_id, criado_em) + índice nome para busca | Backend | 1 | Nicholas | ✅ | `feat/UC-15-listar-listas` |
| TA-082 | Testes: paginação, ordenação, filtro, soft delete, vazia | Backend | 2 | Nicolas | ✅ | `feat/UC-15-listar-listas` |
| TA-083 | Frontend: Dashboard — tabela listas, paginação (botões Anterior/Próximo), input busca tempo real | Frontend | 4 | Eduardo | ✅ | `feat/UC-15-listar-listas` |

---

## 5. DoD

- [x] Query parameterizada, índices otimizados
- [x] Paginação 20 fixa (configurável via config-env-0001-env-example-v1.0 futuro)
- [x] Ordenação DESC created_em padrão
- [x] Filtro nome ILIKE %termo%
- [x] Soft delete respeitado (`deletado_em IS NULL`)
- [x] Testes ≥80%, Code review, CI, CCB

---

## 6. Rastreabilidade

| Artefato | ID |
|----------|-----|
| req-func-0001-requisitos-funcionais-canon.md | RF09 |
| req-use-case-0001-casos-de-uso-canon.md | UC15 |
| spec-004 | Spec ID |
| Branch | `feat/UC-15-listar-listas` |

---

## 7. Notas

- **Response Shape:** `{data: [...], meta: {total, page, size, total_pages}}`
- **Campos Lista:** `id, nome, criado_em, atualizado_em, total_itens, valor_estimado` (calculado na query ou app).
- **Frontend:** Debounce 300ms no input busca (reusa lógica autocomplete).

---

**Fim doc-user-story-0009-us-009**