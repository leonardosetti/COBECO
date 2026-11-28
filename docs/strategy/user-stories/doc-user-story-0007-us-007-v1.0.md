---
id: doc-user-story-0007-us-007-v1.0
type: doc-user-story
title: DOC USER STORY — Us 007
version: v1.0
status: ratificado
canonical: false
canonical_slug: us-007
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
# User Story — doc-user-story-0007-us-007

**Título:** Salvar Lista (Persistir no Banco)  
**ID Único:** doc-user-story-0007-us-007  
**Status:** Done  
**Sprint:** S2 | **Milestone:** S2: Listas e Catálogo  
**Prioridade:** P0  
**Story Points:** 5  
**Autor:** Leonardo Setti (PO)  
**Data Criação:** 15/09/2026  
**Data Atualização:** 06/10/2026  
**Rastreabilidade:** RF08, UC14, spec-004

---

## 1. História

Como **usuário autenticado**,  
eu quero **salvar minha lista efêmera no banco de dados**,  
para **tê-la persistida, acessível em "Minhas Listas" e compartilhável via PDF**.

---

## 2. Critérios de Aceite — Gherkin

### Cenário 1: Salvar lista efêmera autenticado
```gherkin
Dado que sou usuário autenticado
E tenho uma lista efêmera em sessionStorage com nome "Compras" e 3 itens
Quando clico em "Salvar Lista"
Então o sistema faz POST /v1/listas com {nome: "Compras", itens: [...]}
E usa transação MySQL: BEGIN → INSERT listas → INSERT itens_lista → COMMIT
E retorna 201 com {id: 123, nome: "Compras", criado_em: "..."}
E limpa a lista efêmera do sessionStorage
E redireciona para "Minhas Listas" com toast "Lista salva com sucesso"
```

### Cenário 2: Validação — categorias pré-selecionadas (UC03)
```gherkin
Dado que tento salvar lista sem ter selecionado categorias no pré-filtro
Quando faço POST /v1/listas
Então retorna 400 "Selecione pelo menos uma categoria no pré-filtro antes de salvar"
E não persiste a lista
```

### Cenário 3: Lista com itens inválidos (produto inexistente)
```gherkin
Dado que minha lista efêmera tem item com produto_id que não existe no DB
Quando tento salvar
Então retorna 400 "Produto ID 999 não encontrado"
E rollback da transação
```

### Cenário 4: Erro de banco → rollback + mensagem
```gherkin
Dado que ocorre erro MySQL (ex: deadlock, constraint)
Quando salva lista
Então faz ROLLBACK
E retorna 500 "Erro ao salvar lista. Tente novamente."
E loga erro no backend
```

---

## 3. Critérios — Tabela

| # | Critério | Tipo | Auto? | Teste | Status |
|---|----------|------|-------|-------|--------|
| AC-01 | Salvar lista autenticado → transação BEGIN/COMMIT, limpa sessionStorage | Funcional | Sim | `test_salvar_lista_sucesso.py` | ✅ |
| AC-02 | Valida categorias pré-selecionadas → 400 se vazio | Funcional | Sim | `test_salvar_lista_sem_categorias.py` | ✅ |
| AC-03 | Produto inexistente → 400 + rollback | Funcional | Sim | `test_salvar_lista_produto_invalido.py` | ✅ |
| AC-04 | Erro DB → rollback + 500 + log | Não-funcional | Sim | `test_salvar_lista_db_error.py` | ✅ |
| AC-04 | Frontend: botão "Salvar" → loading, toast, redirect | Frontend | Sim (E2E) | `test_salvar_lista_frontend.py` | ✅ |

---

## 4. Tarefas Técnicas

| Task ID | Descrição | Camada | Est. | Resp. | Status | Branch |
|---------|-----------|--------|------|-------|--------|--------|
| TA-060 | Backend: POST /v1/listas — transação explícita, valida categorias, itens, FKs | Backend | 4 | Nicholas | ✅ | `feat/UC-14-salvar-lista` |
| TA-061 | Backend: Verificar categorias selecionadas (session/state) antes de persistir | Backend | 2 | Nicholas | ✅ | `feat/UC-14-salvar-lista` |
| TA-062 | Testes unit: sucesso, validações, rollback, concorrência | Backend | 3 | Nicolas | ✅ | `feat/UC-14-salvar-lista` |
| TA-063 | Frontend: Botão "Salvar" na página Nova Lista → loading, toast, redirect | Frontend | 3 | Eduardo | ✅ | `feat/UC-14-salvar-lista` |

---

## 5. DoD

- [x] Transação MySQL explícita (BEGIN/COMMIT/ROLLBACK)
- [x] Validação categorias pré-selecionadas (regra de negócio)
- [x] FK checks: usuario_id, produto_id válidos
- [x] Limpa sessionStorage `cobeco_lista_efemera` após sucesso
- [x] Testes ≥80%, Code review, CI, CCB

---

## 6. Rastreabilidade

| Artefato | ID |
|----------|-----|
| req-func-0001-requisitos-funcionais-canon.md | RF08 |
| req-use-case-0001-casos-de-uso-canon.md | UC14 |
| spec-004 | Spec ID |
| Branch | `feat/UC-14-salvar-lista` |

---

## 7. Notas

- **Transação:** `session.begin()` → `session.add(lista)` → `session.flush()` (pega ID) → `session.add_all(itens)` → `session.commit()`. Em exceção: `session.rollback()`.
- **Categorias Pré-selecionadas:** Vêm do estado do pré-filtro (doc-user-story-0012-us-012 a doc-user-story-0014-us-014). Salvas em `sessionStorage` ou context do usuário autenticado.
- **Itens:** Cada item valida `produto_id` existe + `quantidade` 1-9999.

---

**Fim doc-user-story-0007-us-007**