# COBECO — Bug Tracker (Normalizado)

> Lista consolidada e sanitizada de todos os bugs conhecidos. 9 bugs normalizados (BUG-000 a BUG-008) registrados no GitHub (#81-89).
> **Status:** Todos em aberto — nenhum fix aplicado (exceto BUG-000 que tem commit `d464fb8` mas aguarda teste manual).

---

## Sumário

| ID | Título Curto | Severidade | Impacto | Prioridade | GitHub | Status |
|----|--------------|------------|---------|------------|--------|--------|
| **BUG-000** | Fornecedores exibem 0% cobertura na tela de seleção | **3.75 Alta** | **3.25 Alto** | Alta | [#89](https://github.com/leonardosetti/COBECO/issues/89) | **ABERTO** (fix commitado `d464fb8`, teste manual pendente) |
| **BUG-001** | Criação de usuário — não registrado na base | Crítica | Alto | P0 | [#87](https://github.com/leonardosetti/COBECO/issues/87) | ABERTO |
| **BUG-002** | Listas não salvas — botão sem efeito | Alta | Alto | P0 | [#88](https://github.com/leonardosetti/COBECO/issues/88) | ABERTO |
| **BUG-003** | Busca categorias perde foco ao digitar | Média | Médio | P1 | [#81](https://github.com/leonardosetti/COBECO/issues/81) | ABERTO |
| **BUG-004** | Fulltext search precário — termos insuficientes | Média | Médio | P1 | [#82](https://github.com/leonardosetti/COBECO/issues/82) | ABERTO |
| **BUG-005** | Apresentação categorias — poluição visual | Baixa | Baixo | P2 | [#83](https://github.com/leonardosetti/COBECO/issues/83) | ABERTO |
| **BUG-006** | Grandes áreas incompletas / fake data | Média | Médio | P1 | [#84](https://github.com/leonardosetti/COBECO/issues/84) | ABERTO |
| **BUG-007** | Produtos irrelevantes (0% relevância) não omitidos | Alta | Alto | P0 | [#85](https://github.com/leonardosetti/COBECO/issues/85) | ABERTO |
| **BUG-008** | Quantidade não multiplica unitário no somatório | Alta | Alto | P0 | [#86](https://github.com/leonardosetti/COBECO/issues/86) | ABERTO |

---

## BUG-000 — Fornecedores exibem 0% de cobertura na tela de seleção

**GitHub:** [#89](https://github.com/leonardosetti/COBECO/issues/89)  
**Status:** ABERTO (fix commitado em `d464fb8`, aguarda teste manual — seção Plano de Teste Manual no issue)  
**Severidade:** 3.75/4 — **Alta**  
**Impacto:** 3.25/4 — **Alto**  
**Prioridade:** Alta  
**RCA:** `coberturaDe(fid)` retorna 0 pois `state.resultado` só populado após clicar "Calcular". Fix: endpoint lote `/disponibilidade-lote` + `state.coberturaPorFornecedor` no frontend.  
**Rastreabilidade:** RF12-RF16, UC03-UC05  
**Evidências:** `backend/src/adapters/api/catalogo.py` (+60 linhas), `frontend/src/app.js` (+8 linhas), commit `d464fb8`

---

## BUG-001 — Criação de usuário não registra na base

**GitHub:** [#87](https://github.com/leonardosetti/COBECO/issues/87)  
**Severidade:** **Crítica** — Bloqueia salvar listas e perfil  
**Prioridade:** **P0**  
**RCA:**
- Backend: `POST /v1/auth/cadastrar` retorna sucesso mas não faz login automático (`auth.py:474-499`)
- Frontend: `vCadastro()` sem handler `data-action="cadastrar"` no dispatch (`app.js:806-818`, `888-934`)
- Falta `showToast` no fluxo de cadastro
**Rastreabilidade:** UC09/RF01, UC10/RF02  
**Evidências:** `backend/src/adapters/api/auth.py:474-499`, `frontend/src/app.js:806-818`, `frontend/src/app.js:888-934`

---

## BUG-002 — Listas não salvas — botão sem efeito

**GitHub:** [#88](https://github.com/leonardosetti/COBECO/issues/88)  
**Severidade:** **Alta** — Core functionality quebrada  
**Prioridade:** **P0**  
**RCA:**
- Frontend: botão `data-action="salvar-lista"` sem handler no dispatch (`app.js:653`, `888-934`)
- Backend: `POST /v1/listas` requer autenticação (`listas.py:389-433`)
- Fluxo completo ausente: modal aviso → cadastro → login → `PromoverListaEfemeraUseCase` (`usecases.py:427-441`)
**Rastreabilidade:** UC14/RF08, UC17/RF08, RF17  
**Evidências:** `frontend/src/app.js:653`, `frontend/src/app.js:888-934`, `backend/src/adapters/api/listas.py:389-433`

---

## BUG-003 — Campo de busca de categorias perde foco ao digitar

**GitHub:** [#81](https://github.com/leonardosetti/COBECO/issues/81)  
**Severidade:** **Média** — Usabilidade  
**Prioridade:** **P1**  
**RCA:** `buscarCategoriasUI()` → `recalcularVisiveis()` → `render()` → `innerHTML` completo destrói input `#busca-cat` (`app.js:941`, `967-982`, `602`, `484`)  
**Rastreabilidade:** RF20, RF26  
**Solução:** Atualizar apenas `#cat-grid` via DOM manipulation ou preservar foco pós-render  
**Evidências:** `frontend/src/app.js:575`, `941`, `602`, `484`

---

## BUG-004 — Fulltext search precário — termos insuficientes

**GitHub:** [#82](https://github.com/leonardosetti/COBECO/issues/82)  
**Severidade:** **Média** — Baixa recall/precisão  
**Prioridade:** **P1**  
**RCA:**
1. `CATEGORIA_GATILHOS` hardcoded: 11/25 categorias cobertas (`catalogo.py:70-82`)
2. Tabela `produto_classes` vazia — seed não popula (`script-seed-0004-realistic-seed-data.py`)
3. `autocomplete()` expande via `produto_classes` mas tabela vazia (`catalogo.py:311-381`)
**Rastreabilidade:** RF20, UC02/RF07, UC03/RF12  
**Evidências:** `backend/src/adapters/api/catalogo.py:70-82`, `311-381`, `backend/scripts/script-seed-0004-realistic-seed-data.py`, `backend/src/adapters/db/models.py:319-336`

---

## BUG-005 — Apresentação categorias — poluição visual

**GitHub:** [#83](https://github.com/leonardosetti/COBECO/issues/83)  
**Severidade:** **Baixa** — UX/UI  
**Prioridade:** **P2**  
**RCA:** `vCategorias()` usa grid simples sem tabs/accordions por área grande; CSS Grid ausente (`app.js:555-591`, `557-561`, `styles/input.css`)  
**Rastreabilidade:** RF12, RF27, RF26  
**Evidências:** `frontend/src/app.js:577-580`, `557-561`, `frontend/src/styles/input.css`

---

## BUG-006 — Grandes áreas incompletas / fake data

**GitHub:** [#84](https://github.com/leonardosetti/COBECO/issues/84)  
**Severidade:** **Média** — Descoberta de fornecedores afetada  
**Prioridade:** **P1**  
**RCA:**
1. `AREAS_GRANDES` nomes não batem com seed (25 categorias reais) (`catalogo.py:86-94`)
2. Seed expandido gera "Categoria Extra 26-50" fake (`script-seed-0004-realistic-seed-data.py:643-651`)
3. `listar_areas_grandes()` busca por nome exato (`catalogo.py:507-514`)
**Rastreabilidade:** RF27, RF28, RF12  
**Evidências:** `backend/src/adapters/api/catalogo.py:86-94`, `507-514`, `backend/scripts/script-seed-0004-realistic-seed-data.py:118-150`, `643-651`

---

## BUG-007 — Produtos irrelevantes (0% relevância) não omitidos

**GitHub:** [#85](https://github.com/leonardosetti/COBECO/issues/85)  
**Severidade:** **Alta** — Listas irrelevantes, nenhum fornecedor  
**Prioridade:** **P0**  
**RCA:** `listar_por_categorias()` faz JOIN via fornecedores (UNIÃO) — traz TODOS os produtos do fornecedor, não só da categoria (`catalogo.py:399-421`, `174-194`). BigSellers (Carrefour, Extra) têm 8 categorias cada (`seed-data.py:155-159`). `autocomplete_produtos` não filtra por categoria (`catalogo.py:636-642`)  
**Rastreabilidade:** RF19, RF13, UC02/RF07, UC03/RF12  
**Evidências:** `backend/src/adapters/api/catalogo.py:399-421`, `174-194`, `636-642`, `backend/scripts/script-seed-0004-realistic-seed-data.py:155-159`

---

## BUG-008 — Quantidade não multiplica unitário no somatório

**GitHub:** [#86](https://github.com/leonardosetti/COBECO/issues/86)  
**Severidade:** **Alta** — Cálculo financeiro incorreto  
**Prioridade:** **P0**  
**RCA:**
- Frontend `vVencedora()` multiplica corretamente: `itemWin.preco * i.qtd` (`app.js:782`)
- Backend `comparacao.py` e `exportacao.py` **pendentes de verificação** — podem não multiplicar
- `calcularOrcamentoEfemera` envia quantidade (`app.js:420-422`)
**Rastreabilidade:** RF15, RF16, RF17, UC06/UC07/UC08  
**Evidências:** `frontend/src/app.js:782`, `420-422`, `backend/src/adapters/api/comparacao.py`, `backend/src/adapters/api/exportacao.py`

---

## Métricas Agregadas

| Métrica | Contagem |
|---------|----------|
| Total bugs | 9 |
| P0 (Crítico/Alto) | 4 (BUG-001, 002, 007, 008) |
| P1 (Médio) | 4 (BUG-000, 003, 004, 006) |
| P2 (Baixo) | 1 (BUG-005) |
| Severidade Crítica | 1 |
| Severidade Alta | 5 (BUG-000, 001, 002, 007, 008) |
| Severidade Média | 3 |
| Severidade Baixa | 1 |

---

## Próximos Passos

1. **Validação humana** — Equipe analisa todos os 9 cards
2. **Priorização de sprint** — P0 primeiro (BUG-001, 002, 007, 008)
3. **BUG-000** — Executar teste manual (seção 7 do doc #89) para fechar
4. **BUG-008** — Verificar `comparacao.py` e `exportacao.py` backend
5. **Fixes** — Aplicar correções com atomic commits, testes, PR review

---

## Referências

- Repositório: `leonardosetti/COBECO`
- GitHub Issues: #81-89
- GitHub PRs: #90 (BUG-001), #91 (BUG-007), #92 (BUG-003), #93 (BUG-006)
- Doc BUG-000: `docs/bugs/bug-0001-cobertura-fornecedores-zero.md`
- Sessão checkpoint: `session/20261126_084932/`
- Protótipo: `doc-prototype-0003-prototype-high-v2-v1.0.html`
- Requisitos: `req-func-0001-requisitos-funcionais-canon.md`
- Casos de uso: `req-use-case-0001-casos-de-uso-canon.md`

---

*Gerado em 26/11/2026 — Sessão 20261126_084932*