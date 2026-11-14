---
id: doc-user-story-005-us-005-v1.0
type: doc-user-story
title: DOC USER STORY — Us 005
version: v1.0
status: ratificado
canonical: false
canonical_slug: us-005
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
# User Story — doc-user-story-005-us-005

**Título:** Criar Lista em Memória (Efêmera)  
**ID Único:** doc-user-story-005-us-005  
**Status:** Done  
**Sprint:** S2 | **Milestone:** S2: Listas e Catálogo  
**Prioridade:** P0  
**Story Points:** 5  
**Autor:** Leonardo Setti (PO)  
**Data Criação:** 15/09/2026  
**Data Atualização:** 06/10/2026  
**Rastreabilidade:** RF07, UC01, spec-008

---

## 1. História

Como **usuário (autenticado ou visitante)**,  
eu quero **criar uma lista de compras em memória (sessionStorage) adicionando/removendo itens com autocomplete**,  
para **montar minha lista rapidamente sem precisar cadastrar/login primeiro**.

---

## 2. Critérios de Aceite — Gherkin

### Cenário 1: Criar lista vazia e adicionar itens
```gherkin
Dado que estou na página "Nova Lista" (autenticado ou não)
Quando digito nome da lista "Compras da Semana"
E busco produto "Arroz" no autocomplete (mín 2 chars, debounce 300ms)
E seleciono "Arroz tipo 1 5kg" da lista
E defino quantidade 2
E clico "Adicionar"
Então o item aparece na lista com nome, quantidade, subtotal
E o total da lista atualiza
E os dados persistem no sessionStorage (sobrevive a refresh/F5)
```

### Cenário 2: Validação quantidade 1-9999
```gherkin
Dado que tenho item "Arroz" na lista
Quando tento definir quantidade 0
Então o sistema impede e mostra erro "Quantidade deve ser entre 1 e 9999"
Quando defino quantidade 10000
Então impede "Quantidade deve ser entre 1 e 9999"
Quando defino quantidade 5
Então aceita e atualiza subtotal
```

### Cenário 3: Soma quantidades mesmo produto
```gherkin
Dado que já tenho "Arroz tipo 1 5kg" qtd 2 na lista
Quando adiciono novamente "Arroz tipo 1 5kg" qtd 3
Então o sistema soma quantidades → qtd 5 (não duplica linha)
E atualiza subtotal e total
```

### Cenário 4: Remover item da lista
```gherkin
Dado que tenho itens na lista
Quando clico no ícone "Remover" do item "Feijão"
Então o item é removido da lista
E o total atualiza
E sessionStorage atualizado
```

### Cenário 5: Lista efêmera survives navegação
```gherkin
Dado que tenho lista em memória com 3 itens
Quando navego para "Comparação" e volto para "Minhas Listas"
Então minha lista efêmera ainda está lá com os 3 itens
```

---

## 3. Critérios — Tabela

| # | Critério | Tipo | Auto? | Teste | Status |
|---|----------|------|-------|-------|--------|
| AC-01 | Criar lista em memória, adicionar itens via autocomplete | Funcional | Sim (E2E) | `test_lista_memoria_adicionar.py` | ✅ |
| AC-02 | Validação qtd 1-9999 | Funcional | Sim | `test_lista_qtd_validacao.py` | ✅ |
| AC-03 | Soma quantidades mesmo produto | Funcional | Sim | `test_lista_soma_qtd.py` | ✅ |
| AC-04 | Remover item | Funcional | Sim | `test_lista_remover.py` | ✅ |
| AC-05 | Persistência sessionStorage (refresh F5) | Não-funcional | Sim (E2E) | `test_lista_sessionstorage.py` | ✅ |
| AC-06 | Autocomplete debounce 300ms, normalização acentos/case | Funcional | Sim | `test_autocomplete_debounce.py` | ✅ |

---

## 4. Tarefas Técnicas

| Task ID | Descrição | Camada | Est. | Resp. | Status | Branch |
|---------|-----------|--------|------|-------|--------|--------|
| TA-040 | Estado lista em memória: sessionStorage key `cobeco_lista_efemera` (JSON) | Frontend | 3 | Eduardo | ✅ | `feat/UC-01-lista-memoria` |
| TA-041 | Componente Autocomplete: fetch /v1/produtos/busca?q=, debounce 300ms, normalização | Frontend | 4 | Eduardo | ✅ | `feat/UC-02-autocomplete` |
| TA-042 | Lógica soma qtd mesmo produto (ID), validação 1-9999, remover, total | Frontend | 4 | Eduardo | ✅ | `feat/UC-01-lista-memoria` |
| TA-043 | UI: Página "Nova Lista" — input nome, tabela itens, autocomplete, botões | Frontend | 4 | Eduardo | ✅ | `feat/UC-01-lista-memoria` |
| TA-044 | Testes E2E Playwright: fluxo completo criar + adicionar + remover + refresh | Frontend | 3 | Nicolas | ✅ | `feat/UC-01-lista-memoria` |

---

## 5. DoD

- [x] Clean Architecture (Frontend: módulos JS), PT-BR
- [x] sessionStorage survives refresh/navegação
- [x] Autocomplete: debounce 300ms, normalização (remover acentos, lowerCase)
- [x] Validação qtd 1-9999 client + server (quando persistir)
- [x] Soma qtd mesmo produto por ID
- [x] Testes E2E + unitários ≥80%
- [x] Code review + CI + CCB

---

## 6. Rastreabilidade

| Artefato | ID |
|----------|-----|
| req-func-0001-requisitos-funcionais-canon.md | RF07 |
| req-use-case-0001-casos-de-uso-canon.md | UC01 |
| spec-008 | Spec ID |
| Branch | `feat/UC-01-lista-memoria`, `feat/UC-02-autocomplete` |

---

## 7. Notas

- **Visitante vs Autenticado:** Mesmo comportamento. Se autenticado, botão "Salvar" envia para backend (doc-user-story-008-us-008). Se visitante, só "Exportar PDF" (doc-user-story-019-us-019).
- **Autocomplete Endpoint:** `GET /v1/produtos/busca?q={termo}&limit=10` — retorna `[{id, nome, categoria, unidade}]`.
- **Normalização:** `termo.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase()` tanto client quanto server.

---

**Fim doc-user-story-005-us-005**