---
id: doc-user-story-0017-us-017-v1.0
type: doc-user-story
title: DOC USER STORY — Us 017
version: v1.0
status: ratificado
canonical: false
canonical_slug: us-017
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
# User Story — doc-user-story-0017-us-017

**Título:** Exportar Lista em PDF (ReportLab)  
**ID Único:** doc-user-story-0017-us-017  
**Status:** Done  
**Sprint:** S4 | **Milestone:** S4: Export, Perfil e Polish  
**Prioridade:** P0  
**Story Points:** 5  
**Autor:** Leonardo Setti (PO)  
**Data Criação:** 15/09/2026  
**Data Atualização:** 20/10/2026  
**Rastreabilidade:** RF17, UC08/UC29, spec-004

---

## 1. História

Como **usuário (autenticado ou visitante)**,  
eu quero **exportar minha lista de compras (ou resultado de comparação) em PDF A4 server-side**,  
para **imprimir e levar ao mercado / compartilhar**.

---

## 2. Critérios de Aceite — Gherkin

### Cenário 1: Exportar PDF lista autenticado
```gherkin
Dado que sou usuário autenticado com lista ID 123 salva
Quando faço POST /v1/export/pdf com {"lista_id": 123, "tipo": "lista"}
Então o sistema gera PDF server-side com ReportLab
E retorna 200 com Content-Type: application/pdf
E header Content-Disposition: attachment; filename="lista_20261015.pdf"
E PDF contém: cabeçalho "COBECO - Lista de Compras", nome da lista, data, tabela itens (Produto, Qtd, Un, Preço Estimado, Subtotal), total, rodapé com data/hora geração
E tempo geração < 5s para 100 itens
```

### Cenário 2: Exportar PDF resultado comparação (visitante ou autenticado)
```gherkin
Dado que calculei orçamento (tenho dados do resultado em sessionStorage)
Quando faço POST /v1/export/pdf com {"orcamento_data": {...}, "tipo": "comparacao"}
Então gera PDF com: cabeçalho "COBECO - Comparação de Preços", data, tabela por fornecedor (Itens Disponíveis, Ausentes, Total), highlight melhor fornecedor, rodapé
E funciona para visitante (sem auth) e autenticado
```

### Cenário 3: PDF A4, margens, fonte PT-BR
```gherkin
Dado que PDF é gerado
Quando abro o arquivo
Então página A4 (210x297mm), margens 20mm
E fonte DejaVuSans (suporta acentos PT-BR)
E tabelas não quebram no meio de linha (keepTogether)
E header repete em páginas longas
```

### Cenário 4: Nome arquivo com data
```gherkin
Dado que exporto hoje (15/10/2026)
Quando download inicia
Então arquivo: `lista_20261015.pdf` (lista) ou `comparacao_20261015.pdf` (comparação)
```

### Cenário 5: Erro geração → 500 + log
```gherkin
Dado que ReportLab falha (ex: fonte não encontrada)
Quando exporta
Então retorna 500 "Erro ao gerar PDF. Tente novamente."
E loga erro completo no backend
```

---

## 3. Critérios — Tabela

| # | Critério | Tipo | Auto? | Teste | Status |
|---|----------|------|-------|-------|--------|
| AC-01 | POST /v1/export/pdf → PDF A4 ReportLab, download, filename data | Funcional | Sim | `test_export_pdf_lista.py` | ✅ |
| AC-02 | Funciona visitante + autenticado (tipo lista ou comparacao) | Funcional | Sim | `test_export_pdf_visitante.py` | ✅ |
| AC-03 | A4, margens 20mm, DejaVuSans, keepTogether, header repeat | Não-funcional | Sim (visual) | `test_export_pdf_formato.py` | ✅ |
| AC-04 | Performance < 5s para 100 itens | Não-funcional | Sim (benchmark) | `test_export_pdf_perf.py` | ✅ |
| AC-05 | Erro → 500 + log | Não-funcional | Sim | `test_export_pdf_erro.py` | ✅ |
| AC-06 | Frontend: Botão "Exportar PDF" → loading, download automático, toast | Frontend | Sim (E2E) | `test_export_pdf_frontend.py` | ✅ |

---

## 4. Tarefas Técnicas

| Task ID | Descrição | Camada | Est. | Resp. | Status | Branch |
|---------|-----------|--------|------|-------|--------|--------|
| TA-160 | Backend: POST /v1/export/pdf — ReportLab SimpleDocTemplate, DejaVuSans registrado, A4, tabelas | Backend | 5 | Fabrício | ✅ | `feat/UC-08-export-pdf` |
| TA-161 | Backend: Duas templates — Lista (itens simples) e Comparação (por fornecedor + highlight melhor) | Backend | 3 | Fabrício | ✅ | `feat/UC-08-export-pdf` |
| TA-162 | Backend: Performance — otimizar loops, registrar fonte uma vez, streaming response se > 10s | Backend | 2 | Fabrício | ✅ | `feat/UC-08-export-pdf` |
| TA-163 | Testes: lista, comparação, visitante, auth, performance, formato, erros | Backend | 2 | Nicolas | ✅ | `feat/UC-08-export-pdf` |
| TA-164 | Frontend: Botão Exportar → POST, blob download, filename, toast sdoc-arch-0006-uc-v1esso/erro | Frontend | 3 | Eduardo | ✅ | `feat/UC-08-export-pdf` |

---

## 5. DoD

- [x] ReportLab server-side (zero dependência client)
- [x] A4, 20mm margens, DejaVuSans (acentos PT-BR)
- [x] `keepTogether` nas linhas tabela, header repeat páginas longas
- [x] Dois modos: Lista (itens) + Comparação (por fornecedor + highlight melhor)
- [x] Visitante + Autenticado
- [x] `< 5s` para 100 itens
- [x] Filename `lista_YYYYMMDD.pdf` / `comparacao_YYYYMMDD.pdf`
- [x] Testes ≥80%, Code review, CI, CCB

---

## 6. Rastreabilidade

| Artefato | ID |
|----------|-----|
| req-func-0001-requisitos-funcionais-canon.md | RF17 |
| req-use-case-0001-casos-de-uso-canon.md | UC08, UC29 |
| spec-004 | Spec ID |
| Branch | `feat/UC-08-export-pdf` |

---

## 7. Notas

- **Fonte DejaVuSans:** Registrar no container backend: `pdfmetrics.registerFont(TTFont('DejaVuSans', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))`. Dockerfile instala `fonts-dejavu-core`.
- **Templates:** Função `gerar_pdf_lista(dados)` e `gerar_pdf_comparacao(dados)`.
- **Streaming:** Se lista > 200 itens, usar `Response(stream_generator, media_type='application/pdf')` para não segurar memória.
- **Concorrência:** ReportLab thread-safe para uso básico.

---

**Fim doc-user-story-0017-us-017**