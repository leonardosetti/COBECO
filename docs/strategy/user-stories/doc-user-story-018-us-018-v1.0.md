---
id: doc-user-story-018-us-018-v1.0
type: doc-user-story
title: DOC USER STORY — Us 018
version: v1.0
status: ratificado
canonical: false
canonical_slug: us-018
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
# User Story — doc-user-story-018-us-018

**Título:** Otimização para Impressão (CSS @media print)  
**ID Único:** doc-user-story-018-us-018  
**Status:** Done  
**Sprint:** S4 | **Milestone:** S4: Export, Perfil e Polish  
**Prioridade:** P1  
**Story Points:** 3  
**Autor:** Leonardo Setti (PO)  
**Data Criação:** 15/09/2026  
**Data Atualização:** 20/10/2026  
**Rastreabilidade:** RF18, UC09, spec-008

---

## 1. História

Como **usuário visualizando lista ou resultados**,  
eu quero **imprimir a página (Ctrl+P) com layout otimizado para papel A4**,  
para **ter versão impressa limpa sem menus, navegação, cores de fundo desnecessárias**.

---

## 2. Critérios de Aceite — Gherkin

### Cenário 1: @media print oculta navegação e elementos UI
```gherkin
Dado que estou na página "Minhas Listas" ou "Resultados"
Quando abro impressão (Ctrl+P) ou `window.print()`
Então o preview de impressão NÃO mostra: header/navbar, sidebar, botões (Exportar, Editar, Excluir), footer, toast, modais
E mostra APENAS: título da página, tabela de dados, totais, data/hora impressão
```

### Cenário 2: Tabelas — quebra de página limpa + header repetido
```gherkin
Dado que tabela tem 50 linhas (não cabe em uma página A4)
Quando imprimo
Então quebras de página ocorrem ENTRE linhas (não no meio de célula)
E header da tabela (`<thead>`) repete no topo de cada página impressa
E linhas não ficam cortadas horizontalmente
```

### Cenário 3: Cores — economizar tinta, legibilidade
```gherkin
Dado que impressão em preto e branco
Quando preview
Então backgrounds coloridos removidos (bg-green-50 → branco)
E bordas pretas finas nas tabelas
E texto preto sobre branco (contraste máximo)
E highlight verde da melhor oferta → borda verde espessa + negrito (não background)
```

### Cenário 4: PDF vs Impressão Navegador
```gherkin
Dado que usuário pode escolher "Exportar PDF" (doc-user-story-017-us-017) OU "Imprimir" (Ctrl+P)
Quando imprime via navegador
Então resultado visual similar ao PDF (tabela limpa, header repetido)
Mas PDF (ReportLab) tem controle total de paginação; impressão navegador depende do engine do browser
```

---

## 3. Critérios — Tabela

| # | Critério | Tipo | Auto? | Teste | Status |
|---|----------|------|-------|-------|--------|
| AC-01 | @media print oculta nav, botões, footer, toasts, modais | Funcional | Sim (visual) | `test_print_oculta_ui.py` | ✅ |
| AC-02 | Tabelas: quebra entre linhas, thead repete cada página | Funcional | Sim (visual) | `test_print_tabela_quebra.py` | ✅ |
| AC-03 | Cores: sem backgrounds, bordas pretas, texto preto, highlight → borda+negrito | Funcional | Sim (visual) | `test_print_cores.py` | ✅ |
| AC-04 | `window.print()` botão funcional nas páginas Lista/Resultados | Funcional | Sim (E2E) | `test_print_botao.py` | ✅ |
| AC-05 | Frontend: CSS @media print em arquivo dedicado `print.css` | Técnico | Sim | `test_print_css_arquivo.py` | ✅ |

---

## 4. Tarefas Técnicas

| Task ID | Descrição | Camada | Est. | Resp. | Status | Branch |
|---------|-----------|--------|------|-------|--------|--------|
| TA-170 | Frontend: Criar `print.css` — @media print rules para ocultar UI, tabelas, cores | Frontend | 3 | Eduardo | ✅ | `feat/UC-09-imprimir` |
| TA-171 | Frontend: Incluir `print.css` no `index.html` (link media="print") | Frontend | 0.5 | Eduardo | ✅ | `feat/UC-09-imprimir` |
| TA-172 | Frontend: Ajustar highlight verde melhor oferta → @media print: border-left 4px green + font-weight bold | Frontend | 1 | Eduardo | ✅ | `feat/UC-09-imprimir` |
| TA-173 | Testes visuais: imprimir Lista, Resultados, Comparação — validar quebra, header repeat, ocultação | Frontend | 2 | Nicolas | ✅ | `feat/UC-09-imprimir` |

---

## 5. DoD

- [x] `print.css` dedicado, carregado via `<link rel="stylesheet" href="print.css" media="print">`
- [x] Ocultação completa: `nav, .btn, .toast, .modal, footer, .sidebar { display: none !important }`
- [x] Tabelas: `thead { display: table-header-group }`, `tr { page-break-inside: avoid }`, `table { page-break-after: auto }`
- [x] Cores: `@media print { .bg-green-50 { background: white !important; border-left: 4px solid green; font-weight: bold } }`
- [x] Botão "Imprimir" chama `window.print()` nas páginas relevantes
- [x] Testes visuais manuais (E2E Playwright pode testar geração PDF via `page.pdf()` simulando print)
- [x] Code review, CI, CCB

---

## 6. Rastreabilidade

| Artefato | ID |
|----------|-----|
| req-func-0001-requisitos-funcionais-canon.md | RF18 |
| req-use-case-0001-casos-de-uso-canon.md | UC09 |
| spec-008 | Spec ID |
| Branch | `feat/UC-09-imprimir` |

---

## 7. Notas

- **CSS Print:** Arquivo separado evita poluir CSS principal. Carregado com `media="print"` — browser só baixa/aplica ao imprimir.
- **thead Repeat:** `thead { display: table-header-group }` funciona na maioria browsers modernos. Fallback: repetir header manualmente se necessário.
- **Quebra de Linha:** `tr { page-break-inside: avoid }` evita corte no meio da linha. `td { page-break-inside: avoid }` também ajuda.
- **Teste Automatizado:** Playwright `await page.pdf({ format: 'A4', printBackground: true })` simula impressão para screenshot comparison.

---

**Fim doc-user-story-018-us-018**