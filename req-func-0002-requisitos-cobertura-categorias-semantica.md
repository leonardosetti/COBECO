---
id: req-func-0002-requisitos-cobertura-categorias-semantica
type: req-func
title: REQ FUNC — Cobertura, Produtos por Categoria e Busca Semântica
version: '1.0'
status: proposta
canonical: false
canonical_slug: requisitos-cobertura-categorias-semantica
created: '2026-11-25'
author: Leonardo Setti (@leonardosetti)
owner: CCB
trace:
  constitution: []
  req_func: [req-func-0001]
  req_nfunc: []
  use_cases: [UC03, UC04, UC05, UC06, UC07]
  specs: [SPECS.md]
  handoffs: []
  adrs: []
  code: [backend/src/adapters/api/catalogo.py, frontend/src/app.js]
  tests: [backend/tests/unit/adapters/test_catalogo_busca.py]
domain: requirements
layer: requirements
tags: []
lgpd_class: n/a
workflow:
  stage: proposta
  reviewer: null
  reviewed_at: null
  approval_hash: null
  board_url: null
---

# 📋 req-func-0002 — Cobertura de Fornecedores, Produtos por Categoria e Busca Semântica

**Base:** SPECS.md v3.3 + req-func-0001 v3.2 + BUG-0001 (cobertura 0%).  
**Objetivo:** três ajustes de especificação no fluxo de comparação (Passos 1–4).

---

## 1. Contexto e avaliação da condição atual

| Item | Estado implementado (SPECS v3.3) | Gap identificado |
|------|----------------------------------|------------------|
| RF14 — Filtro de disponibilidade | Slider 0–100%, default 0%, aplica no cálculo e desabilita checkbox abaixo do piso | Não **omite** fornecedores com 0% de cobertura da listagem; abaixo do piso o card continua renderizado (`.off`) |
| RF12/RF13 — Categorias → Fornecedores | Fornecedores filtrados pelas categorias selecionadas (união) | **Produtos não são filtrados** por categoria: o catálogo de escolha (Passo 2) expõe todos os produtos, incluindo itens alheios às categorias |
| Busca de categorias | `GET /catalogo/categorias` lista todas, sem busca nem sinônimos | Não existe busca semântica: "roupas" não acha Vestuário; "pá/rastelo" não acha Jardinagem/Ferramentas |
| IA/Taxonomia/Gestalt | 11 categorias macro, lista plana | Sem consolidação de categorias semelhantes, sem hierarquia/breadcrumb, sem heurísticas de findability |

Condição ótima para prosseguir: sim. Os três gaps são ortogonais, bem delimitados e implementáveis em rodadas independentes sem alterar o contrato de cálculo de orçamento (RF15/RF16) nem o modelo de dados existente (sem migração obrigatória na v1).

---

## 2. Requisitos Funcionais (novos + alterados)

### RF14 — Filtrar por Disponibilidade (ALTERADO)

| Campo | Conteúdo |
|-------|----------|
| ID | **RF14** (altera req-func-0001) |
| Requisito | Filtrar por Disponibilidade com omissão de 0% de cobertura |
| Descrição | O slider 0–100% define o **piso de cobertura** da listagem de fornecedores. Fornecedores com **0% de cobertura são sempre omitidos** da listagem de seleção (não aparecem, não apenas desabilitados). Quando o usuário define piso > 60%, fornecedores com ≤ 59% são omitidos da listagem. |
| Guard-Rails | Default do slider: 0% (mostra todos com cobertura > 0). Somente fornecedores com cobertura > 0 e ≥ piso são elegíveis para seleção. Mínimo 2 fornecedores elegíveis para habilitar "Calcular orçamento". Se o filtro deixar < 2 elegíveis, exibe toast e desabilita cálculo. |
| Prioridade | P0 |

### RF19 — Produtos Escolhidos Restritos às Categorias Selecionadas (NOVO)

| Campo | Conteúdo |
|-------|----------|
| ID | **RF19** |
| Requisito | Catálogo de produtos restrito às categorias do pré-filtro |
| Descrição | Após o usuário selecionar categorias (Passo 1, UC03/RF12), apenas produtos relacionados a essas categorias ficam disponíveis como escolha no Passo 2 (lista). Exemplo: categorias Vestuário + Livros → somente roupas e livros; nada de martelo, arroz, sorvete, café, processador, placa de vídeo. |
| Guard-Rails | Relação produto→categoria derivada do existente: fornecedor↔categoria (N:N) + fornecedor↔produto (N:N). Sem nova tabela. União: produto aparece se for vendido por ao menos um fornecedor de uma categoria selecionada. Mudar categorias recarrega o catálogo de produtos e o autocomplete. |
| Prioridade | P0 |

### RF20 — Busca Semântica de Categorias (NOVO)

| Campo | Conteúdo |
|-------|----------|
| ID | **RF20** |
| Requisito | Busca semântica de categorias por termo com sinônimos |
| Descrição | **REMOVIDA do escopo ativo (ADR-0003).** Endpoint de busca de categorias que relaciona termos do usuário a categorias mesmo sem correspondência literal no nome. Ex.: "roupas" ou "camiseta" → Vestuário; "pá" ou "rastelo" → Jardinagem e Ferramentas. Guardado em `.stash/semantic-cat-search-20261127/` para trabalho futuro. |
| Guard-Rails | Não implementado no MVP. Campo de busca por nome não existe no Passo 1; navegação apenas por grandes áreas + checkboxes diretos. |
| Prioridade | P0 → **adiada (futuro)** |

### RF21 — Organização e Consolidação de Categorias (IA / Taxonomia) (NOVO)

| Campo | Conteúdo |
|-------|----------|
| ID | **RF21** |
| Requisito | Arquitetura da informação das categorias (Nielsen + Gestalt) |
| Descrição | Consolidar categorias de propriedades muito semelhantes (evitar board com excesso de opções). Melhorar visualização por heurísticas de Nielsen (encontrabilidade, navegação, consistência) e Gestalt (proximidade, similaridade, fechamento). Incluir hierarquia, rotulagem clara e breadcrumb (trilha de migalhas) para o usuário saber onde está e voltar níveis. |
| Guard-Rails | Não prescreve lista final de categorias nesta especificação; cabe à rodada de design/IA definir a consolidação. Deve manter retrocompatibilidade com as 11 categorias existentes durante a transição. |
| Prioridade | P2 (design) |

---

## 3. Casos de Uso afetados

| UC | Título | Mudança |
|----|--------|---------|
| UC03 | Selecionar Categorias | Acrescenta busca semântica (RF20) e recarregamento de produtos (RF19) |
| UC04 | Selecionar Fornecedores | Omissão de 0% de cobertura e aplicação do piso na listagem (RF14) |
| UC05 | Filtrar por Disponibilidade | Piso passa a omitir (não só desabilitar) fornecedores abaixo do limite (RF14) |
| UC06/UC07 | Cálculo/Visualização | Sem alteração de contrato; recebe apenas fornecedores elegíveis (RF14) |

---

## 4. Regras de Negócio

| Regra | Descrição |
|-------|-----------|
| RB-COB-01 | Fornecedor com 0% de cobertura da lista nunca é exibido na listagem de seleção (Passo 3). |
| RB-COB-02 | Piso de disponibilidade (slider) remove da listagem fornecedores com cobertura < piso (ex.: piso 60 → omite ≤ 59%). |
| RB-COB-03 | Se restarem < 2 fornecedores elegíveis, "Calcular orçamento" fica desabilitado. |
| RB-PROD-01 | Catálogo de escolha de produtos (Passo 2) só inclui produtos vendidos por fornecedores de ≥1 categoria selecionada (Passo 1). |
| RB-BUSCA-01 | Busca de categorias corresponde por nome (ILIKE) ou por sinônimo cadastrado no mapa de gatilhos. |

---

## 5. Rodadas de Implementação

| Ronde | RF | Escopo | Status | Arquivos |
|-------|----|--------|--------|----------|
| 1 | RF14 | Omitir 0% de cobertura + piso de disponibilidade na listagem de fornecedores (sem desabilitar card: não renderizar) | Implementado + testado (E2E de BUG-0001 já valida cobertura real) | `frontend/src/app.js` |
| 2 | RF19 | Produtos do Passo 2 + autocomplete restritos às categorias selecionadas (derivação fornecedor↔categoria + fornecedor↔produto, sem migração) | Implementado + testes unitários | `backend/src/adapters/api/catalogo.py`, `frontend/src/app.js` |
| 3 | RF20 | Busca semântica de categorias (`/catalogo/categorias/busca?q=`) com mapa de gatilhos; UI de busca no Passo 1 | **Removida — adiada para trabalho futuro (ADR-0003).** Código guardado em `.stash/semantic-cat-search-20261127/` | `backend/src/adapters/api/catalogo.py`, `frontend/src/app.js` |
| 4 | RF21 | Design de IA/taxonomia: consolidar categorias semelhantes, hierarquia, breadcrumb, findability (Nielsen/Gestalt) | Pendente (especificado, não implementado) | design / SPECS |

**Critério de aceitação por ronde:** `pytest backend/tests/unit` verde; `node --check frontend/src/app.js` válido; fluxo Home → Categorias → Lista → Fornecedores → Comparação executa sem login.

---

**FIM DO DOCUMENTO req-func-0002**
