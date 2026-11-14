---
id: doc-arch-0010-c4-context-v1.0
type: doc-arch
title: DOC ARCH — C4 Context
version: v1.0
status: ratificado
canonical: false
canonical_slug: c4-context
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
domain: architecture
layer: architecture
tags: []
lgpd_class: n/a
workflow:
  stage: rascunho
  reviewer: null
  reviewed_at: null
  approval_hash: null
  board_url: null
---
# Diagrama de Contexto (C4 Level 1) — COBECO MVP

**Versão:** 1.0  
**Data:** 15/09/2026  
**Autor:** Nicholas Anthony (Arquiteto)  
**Ferramenta:** Mermaid.js (Docs-as-Code)  
**Base:** ADR-001, Constitution v2.0  
**Status:** Ratificado (Gate 2 — 29/09/2026)

---

## Diagrama Mermaid

```mermaid
C4Context
    title Diagrama de Contexto — COBECO MVP

    Person(user, "Usuário Autenticado", "Pessoa física com conta no sistema — cria listas persistidas, compara preços, exporta PDF, gerencia perfil")
    Person(visitor, "Visitante", "Usuário não autenticado — cria lista efêmera em memória, exporta PDF, pode se cadastrar/login")
    
    System(cobeco, "COBECO MVP", "Sistema web de comparação de preços de compras entre fornecedores. SPA Vanilla JS + Tailwind (nginx) + API FastAPI (Python) + MySQL 8.0 InnoDB. Deploy via Docker Compose.")
    
    System_Ext(github, "GitHub", "Repositório de código (git@github.com:leonardosetti/COBECO.git), GitHub Actions (CI/CD), GitHub Projects (gestão ágil), GitHub Container Registry (ghcr.io)")
    System_Ext(dockerhub, "Docker Hub / ghcr.io", "Registry de imagens Docker (backend, frontend, proxy, mysql)")
    System_Ext(fatec, "FATEC Taquaritinga", "Instituição acadêmica — orientador, banca avaliadora, coordenação curso ADS")
    System_Ext(orientador, "Orientador Acadêmico", "Revisa documentação ABNT, aprova marcos, avalia entrega final")
    System_Ext(banca, "Banca Avaliadora (3 professores)", "Avalia apresentação final (35min), demo, documentação — nota final")

    Rel(user, cobeco, "Usa", "HTTPS/8380 via nginx proxy")
    Rel(visitor, cobeco, "Usa (lista efêmera + PDF)", "HTTPS/8380 via nginx proxy")
    Rel(cobeco, github, "Código + CI/CD + Artefatos", "HTTPS/443 (git push, Actions, Packages)")
    Rel(cobeco, dockerhub, "Pull/Push imagens Docker", "HTTPS/443")
    Rel(fatec, cobeco, "Avalia entrega final", "Apresentação + Demo + Documentação")
    Rel(orientador, cobeco, "Acompanha + Aprova", "Revisões quinzenais docs ABNT, Sprint Reviews")
    Rel(banca, cobeco, "Avalia final", "Apresentação 35min + Demo + Docs")

    UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")
```

---

## Descrição Narrativa

O **COBECO MVP** é um sistema web acessado via browser na porta **8380** (roteada por **nginx** reverso proxy). Dois tipos de atores humanos interagem:

1. **Usuário Autenticado** — Tem conta no sistema (cadastro via RF01). Acesso completo: CRUD de listas persistidas no MySQL, comparação de preços com pré-filtro, exportação PDF, gestão de perfil.
2. **Visitante** — Não tem conta. Pode criar **lista efêmera** em `sessionStorage` (memória do browser), usar autocomplete, exportar PDF. Ao fazer login, pode **promover** a lista efêmera para persistência (RF08/UC17).

O código-fonte vive no **GitHub** (repositório público `leonardosetti/COBECO`). **GitHub Actions** executa CI/CD: `ruff` (lint) + `pytest --cov≥80%` + `mypy` + build Docker. Imagens Docker publicadas no **ghcr.io** (GitHub Container Registry).

A **FATEC Taquaritinga** é a instituição patrocinadora. O **Orientador** acompanha quinzenalmente (Sprint Reviews, docs ABNT). A **Banca** (3 professores) avalia a entrega final: apresentação 35min + demo funcional + documentação ABNT.

---

## Decisões Arquiteturais Relacionadas (ADRs)

| ADR | Título | Impacto no Contexto |
|-----|--------|---------------------|
| ADR-001 | Stack Tecnológica (FastAPI, MySQL, Vanilla JS, nginx, ReportLab) | Define containers L2 e tecnologias de cada ator/sistema |
| ADR-002 | Clean Architecture 4 Camadas (manual) | Define organização interna do Container Backend (L3) |
| ADR-003 | Autenticação JWT + Refresh Cookie httpOnly | Define fluxo de auth entre User/Visitor e Sistema |
| ADR-004 | PDF Server-side ReportLab | Define responsabilidade de exportação no Backend |
| ADR-005 | Seed Determinístico + MySQL InnoDB | Define dados iniciais e constraints de integridade |

---

## Rastreabilidade

| Artefato | Localização |
|----------|-------------|
| Constitution v2.0 | `constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md` Art. 1.3, 3.1, 3.7 |
| ADR-001 Stack | `docs/decisoes/doc-adr-0001-stack-decision-v1.0.md` |
| Specs SDD | `.ai/specs/spec-004` a `spec-016` |
| PRD | `docs/strategy/PRD.md` |
| User Stories | `docs/strategy/user-stories/US-*.md` |

---

## Controle de Versões

| Versão | Data | Autor | Mudança | Aprovado por |
|--------|------|-------|---------|--------------|
| 1.0 | 15/09/2026 | Nicholas Anthony | Criação inicial baseada em ADR-001 | CCB (Gate 2) |

---

**Fim do Diagrama de Contexto (C4 Level 1)**  
*Renderize no GitHub/VS Code/Mermaid Live Editor para visualização gráfica. Atualizar a cada ADR/CR arquitetural.*