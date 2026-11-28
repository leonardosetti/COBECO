---
id: doc-adr-0003-remocao-busca-semantica-categorias-v1.0
type: decision-adr
title: ADR — Remoção da busca semântica de categorias (RF20) para trabalho futuro
version: v1.0
status: ratificado
canonical: true
canonical_slug: remocao-busca-semantica-categorias
created: '2026-11-27'
updated: '2026-11-27'
author: Leonardo Setti (@leonardosetti)
owner: CCB
ratified_by: gh-sig:owner:leonardosetti:14863508
ratified_at: '2026-11-27'
supersedes: null
superseded_by: null
trace:
  constitution: [Art. 3.1, Art. 3.2]
  req_func: [RF20]
  req_nfunc: []
  use_cases: [UC03]
  specs: [req-func-0002-requisitos-cobertura-categorias-semantica.md]
  handoffs: []
  adrs: [doc-adr-0002-busca-fulltext-v1.0.md]
  code: [backend/src/adapters/api/catalogo.py, frontend/src/app.js]
  tests: [backend/tests/unit/adapters/test_catalogo_busca.py]
domain: architecture
layer: architecture
tags: [busca-semantica, categorias, remocao, RF20, futuro, stash]
lgpd_class: n/a
workflow:
  stage: ratificado
  reviewer: null
  reviewed_at: null
  approval_hash: null
  board_url: null
---

# ADR-0003 — Remoção da busca semântica de categorias (RF20) para trabalho futuro

**Status:** Ratificado  
**Data:** 27/11/2026  
**Decisores:** CCB (Change Control Board) — FATEC Taquaritinga ADS  
**Autor:** Leonardo Setti (@leonardosetti)  
**Revisores:** Tech Lead, Arquiteto de Software

---

## Contexto

O requisito RF20 (Busca semântica de categorias por termo com sinônimos) foi implementado nas rondas de desenvolvimento do catálogo, incluindo:

- Backend: mapa `CATEGORIA_GATILHOS`, método `buscar_por_termo`, endpoint `GET /catalogo/categorias/busca?q=`, schema `CategoriaBuscaResponse`.
- Frontend: campo `#busca-cat` no Passo 1 (UC03), `ApiClient.buscarCategorias`, função `buscarCategoriasUI`, estado `categoriaBusca`, `preserveFocus` em `atualizarCategoriasVisiveis`.
- Testes: `backend/tests/unit/adapters/test_catalogo_busca.py` (classe `TestCategoriaBuscaSemantica`).

O campo de busca semântica das categorias **não está funcionando corretamente** (perda de foco a cada caractere, re-render completo da view, recall/precisão baixa). A correção exigiria debounce + atualização parcial do DOM (já parcialmente implementada) e enriquecimento da taxonomia de sinônimos, o que consome tempo que não está disponível para o escopo MVP atual.

---

## Decisão

Remover a busca semântica de categorias (RF20) do escopo ativo do MVP e guardar a feature em stash para trabalho futuro.

### O que foi removido

| Camada | Artefatos removidos |
|--------|---------------------|
| Backend (`backend/src/adapters/api/catalogo.py`) | Mapa `CATEGORIA_GATILHOS` (11 categorias + chaves genéricas), método `buscar_por_termo`, endpoint `GET /categorias/busca`, schema `CategoriaBuscaResponse` |
| Frontend (`frontend/src/app.js`) | Estado `categoriaBusca`, `ApiClient.buscarCategorias`, campo `#busca-cat`, handler `busca-cat`, função `buscarCategoriasUI`, `preserveFocus` em `atualizarCategoriasVisiveis` |
| Testes (`backend/tests/unit/adapters/test_catalogo_busca.py`) | Classe `TestCategoriaBuscaSemantica` e assert `test_gatilhos_cobrem_exemplos_requisitados` |

### O que permanece

- RF19 (Produtos restritos às categorias selecionadas) — continua ativo.
- Listagem de categorias via `GET /categorias` (nome direto) — continua ativa, sem busca nem sinônimos.
- RF14 (Filtro de disponibilidade) — continua ativo.

### Stash (backup para trabalho futuro)

Cópias dos 3 arquivos antes da remoção estão em `.stash/semantic-cat-search-20261127/`:
- `app.js`
- `catalogo.py`
- `test_catalogo_busca.py`

---

## Alternativas consideradas

| Alternativa | Prós | Contras | Motivo da não escolha |
|-------------|------|---------|-----------------------|
| Manter RF20 e corrigir (debounce + DOM parcial + taxonomia) | Funcionalidade completa de busca semântica | Tempo de desenvolvimento não disponível; recall/precisão baixo sem enriquecimento de dados | Escopo MVP não comporta; prioridade maior em RFs críticos |
| Substituir por busca simples por nome (LIKE no /categorias) | Simples, já existe via `GET /categorias` | Não oferece sinônimos ("roupas" não acha Vestuário) | Aceitável para MVP; busca semântica fica para futura rodada |

---

## Consequências

### Positivas
- Reduz complexidade do frontend (sem estado de busca, sem debounce, sem `preserveFocus`).
- Elimina bug de perda de foco no campo de busca (re-raiz do problema reportado).
- Foco do time em RFs críticos do MVP (RF12, RF13, RF14, RF15, RF16, RF19).
- KISS (Art. 3.1 da Constitution): menos código, menos camadas, menos pontos de falha.

### Negativas (mitigadas)
- Usuário não pode buscar categorias por sinônimo (ex.: "roupas" → Vestuário). Mitigação: continua podendo navegar pelas grandes áreas e marcar categorias diretamente no Passo 1.
- Endpoint `/categorias/busca` não existe mais. Mitigação: cliente usa `GET /categorias` e filtra localmente se necessário.
- Trabalho futuro precisará restaurar do stash e reimplementar com testes.

---

## Conformidade com a Constitution

| Artigo | Requisito | Conforme? | Observação |
|--------|-----------|-----------|------------|
| Art. 3.1 | KISS | Sim | Remove feature não funcional, reduz complexidade |
| Art. 3.2 | YAGNI | Sim | Não mantém funcionalidade não necessária ao MVP |
| Art. 8.1 | Cobertura ≥80% | Sim | Testes de RF20 removidos junto com a feature |

---

## Rastreabilidade

- **Origem:** Relatório de bug — campo de busca semântica das categorias não funciona (perda de foco a cada caractere).
- **Requisitos:** RF20 (removido do escopo ativo; fica para futura rodada).
- **Casos de Uso:** UC03 (Selecionar Categorias — continua sem busca semântica).
- **Especificações SDD:** `req-func-0002` — ronde 3 (RF20) marcada como removida/adiada.
- **Constituição:** Art. 3.1 (KISS), Art. 3.2 (YAGNI), Art. 8.1 (cobertura).

---

## Aprovação

| Papel | Nome | Assinatura | Data |
|-------|------|------------|------|
| CCB Chair / Product Owner | | | |
| Tech Lead | | | |
| Arquiteto de Software | | | |

---

**Fim do ADR-0003**
