---
id: doc-user-story-014-us-014-v1.0
type: doc-user-story
title: DOC USER STORY — Us 014
version: v1.0
status: ratificado
canonical: false
canonical_slug: us-014
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
# User Story — doc-user-story-014-us-014

**Título:** Filtrar por Disponibilidade (Slider 0-100%)  
**ID Único:** doc-user-story-014-us-014  
**Status:** Done  
**Sprint:** S3 | **Milestone:** S3: Pré-filtro e Comparação  
**Prioridade:** P1  
**Story Points:** 2  
**Autor:** Leonardo Setti (PO)  
**Data Criação:** 15/09/2026  
**Data Atualização:** 13/10/2026  
**Rastreabilidade:** RF14, UC05, spec-008

---

## 1. História

Como **usuário selecionando fornecedores**,  
eu quero **filtrar a lista por % disponibilidade usando slider 0-100%**,  
para **ver apenas fornecedores que têm a maioria dos produtos que preciso**.

---

## 2. Critérios de Aceite — Gherkin

### Cenário 1: Slider atualiza lista em tempo real
```gherkin
Dado que estou na tela "Selecionar Fornecedores" com 10 fornecedores listados
Quando movo o slider de "Disponibilidade mínima" para 60%
Então a lista refiltra instantaneamente (debounce 100ms)
E mostra apenas fornecedores com % disponibilidade ≥ 60%
E as seleções de checkboxes já feitas são MANTIDAS (se fornecedor selecionado cai fora, fica desmarcado automaticamente)
E contador "X de Y fornecedores" atualiza
```

### Cenário 2: Slider 0% → mostra todos
```gherkin
Dado que slider está em 60% (mostrando 4 de 10)
Quando movo slider para 0%
Então mostra todos 10 fornecedores novamente
E seleções anteriores restauradas se possível
```

### Cenário 3: Slider 100% → só 100% disponibilidade
```gherkin
Dado que movo slider para 100%
Então mostra apenas fornecedores com 100% disponibilidade
E se nenhum tem 100%, mostra "Nenhum fornecedor com 100% disponibilidade"
```

---

## 3. Critérios — Tabela

| # | Critério | Tipo | Auto? | Teste | Status |
|---|----------|------|-------|-------|--------|
| AC-01 | Slider 0-100% → refiltra tempo real (debounce 100ms) | Funcional | Sim | `test_disponibilidade_slider.py` | ✅ |
| AC-02 | Seleções checkbox mantidas (se fornecedor some, desmarca auto) | Funcional | Sim | `test_disponibilidade_mantem_selecao.py` | ✅ |
| AC-03 | 0% = todos, 100% = só 100% | Funcional | Sim | `test_disponibilidade_extremos.py` | ✅ |
| AC-04 | Contador "X de Y fornecedores" atualiza | Funcional | Sim | `test_disponibilidade_contador.py` | ✅ |
| AC-05 | Frontend: Slider input range, debounce, contador, acessível | Frontend | Sim (E2E) | `test_disponibilidade_frontend.py` | ✅ |

---

## 4. Tarefas Técnicas

| Task ID | Descrição | Camada | Est. | Resp. | Status | Branch |
|---------|-----------|--------|------|-------|--------|--------|
| TA-130 | Frontend: Componente SliderDisponibilidade — input type=range, debounce 100ms, refiltra array local | Frontend | 3 | Eduardo | ✅ | `feat/UC-05-disponibilidade` |
| TA-131 | Frontend: Lógica mantém seleções — se fornecedor filtrado estava selecionado, desmarca + toast "Fornecedor X removido por disponibilidade" | Frontend | 2 | Eduardo | ✅ | `feat/UC-05-disponibilidade` |
| TA-132 | Testes: slider, debounce, mantém seleção, extremos | Frontend | 1 | Nicolas | ✅ | `feat/UC-05-disponibilidade` |

---

## 5. DoD

- [x] Slider nativo `<input type="range" min=0 max=100 step=5>`
- [x] Debounce 100ms (não chama backend — filtra array local já carregado)
- [x] Mantém seleções válidas, remove inválidas com feedback
- [x] Contador dinâmico
- [x] Acessível (ARIA, teclado)
- [x] Testes ≥80%, Code review, CI, CCB

---

## 6. Rastreabilidade

| Artefato | ID |
|----------|-----|
| req-func-0001-requisitos-funcionais-canon.md | RF14 |
| req-use-case-0001-casos-de-uso-canon.md | UC05 |
| spec-008 | Spec ID |
| Branch | `feat/UC-05-disponibilidade` |

---

## 7. Notas

- **Filtro Local:** Não chama backend — usa array de fornecedores já carregado no doc-user-story-012-us-012/doc-user-story-013-us-013. Performance instantânea.
- **Step:** 5% (0, 5, 10, ..., 100).
- **Feedback Visual:** Toast sutil quando fornecedor selecionado é removido pelo filtro.

---

**Fim doc-user-story-014-us-014**