# Cronograma Detalhado (Gantt Simplificado) — COBECO MVP

**Versão:** 1.0  
**Data:** 29/09/2026 (Gate 2)  
**Responsável:** Leonardo Setti (Tech Lead)  
**Ferramenta:** Mermaid.js (versionado no repo)  
**Base:** WBS (`docs/strategy/WBS.md`)

---

## Diagrama de Gantt (Mermaid)

```mermaid
gantt
    title Cronograma COBECO MVP — 38 Dias Úteis
    dateFormat  YYYY-MM-DD
    axisFormat  %d/%m
    excludes    weekends

    section Fase 1: Iniciação (Sprint 0)
    Project Charter           :a1, 2026-09-15, 1d
    Business Case             :a2, after a1, 0.5d
    Stakeholder Register      :a3, after a1, 0.5d
    Matriz RACI               :a4, after a1, 0.5d
    WBS                       :a5, after a1, 0.5d
    Cronograma (Gantt)        :a6, after a5, 0.5d
    ADR-001 Stack             :a7, 2026-09-15, 1d
    Constitution v2.0         :a8, 2026-09-15, 0.5d
    GitHub Projects Setup     :a9, after a4, 1d
    Ambiente Dev (Docker)     :a10, after a7, 1d

    section Sprint 1: Setup, Docs, Auth (6 dias)
    PRD                       :b1, 2026-09-22, 1d
    User Stories RF01-RF04    :b2, after b1, 1d
    Diagramas C4              :b3, after a7, 1d
    RAID Log Inicial          :b4, after a3, 0.5d
    Test Plan                 :b5, after b2, 0.5d
    Docker Compose Prod       :b6, after a10, 1d
    Schema MySQL (8 tabelas)  :b7, after a7, 1d
    Seed Script               :b8, after b7, 1d
    UC09: Cadastrar Usuario   :b9, after b7, 1.5d
    UC10: Login JWT           :b10, after b9, 1.5d
    UC11: Logout              :b11, after b10, 0.5d
    UC12: Recuperar Senha     :b12, after b9, 1d
    Frontend Auth Pages       :b13, after b9, 2d
    Docs ABNT                 :b14, after b1, 3d

    section Sprint 2: Listas e Catálogo (6 dias)
    User Stories RF07-RF11    :c1, after b2, 0.5d
    UC02: Autocomplete        :c2, after b13, 1d
    UC01: Lista em Memória    :c3, after c2, 1d
    UC14: Salvar Lista        :c4, after b7, 1d
    UC17: Promover Lista      :c5, after c3 c4, 1d
    UC15: Listar Minhas Listas:c6, after c4, 1d
    UC13: Editar/Excluir Lista:c7, after c6, 1d
    Frontend Listas CRUD      :c8, after c4 c6, 2d

    section Sprint 3: Pré-filtro e Comparação (6 dias)
    User Stories RF12-RF16    :d1, after c1, 0.5d
    UC03: Selecionar Categorias:d2, after c8, 1d
    UC04: Selecionar Forneced.:d3, after d2, 1d
    UC05: Filtrar Disponibil. :d4, after d3, 1d
    UC06: Calcular Orçamento  :d5, after c4, 1.5d
    UC07: Visualizar Resultados:d6, after d5, 1.5d

    section Sprint 4: Export, Perfil, Polish (6 dias)
    User Stories RF05,06,17,18:e1, after d1, 0.5d
    UC08/UC29: Export PDF     :e2, after c4, 1.5d
    UC09: Otimização Impressão:e3, after e2, 1d
    UC18: Visualizar Perfil   :e4, after b9, 1d
    UC16: Gerenciar Perfil    :e5, after e4, 1d
    Frontend Perfil           :e6, after e4, 1d
    Feedback Visual Global    :e7, after c8, 1d

    section Sprint 5: Buffer, QA, Demo (6 dias)
    Cobertura Testes ≥80%     :f1, after e2, 2d
    Testes E2E Playwright     :f2, after e2, 1.5d
    CI/CD Pipeline            :f3, after a10, 1d
    Runbooks                  :f4, after f3, 1d
    Release Notes v0.1.0      :f5, after f1, 0.5d
    Refinar doc-readme-0001-readme-canon + OpenAPI  :f6, after f3, 0.5d
    Preparação Apresentação   :f7, after f1, 1.5d
    Post-Mortem / Lições      :f8, after f7, 0.5d
    Termo de Encerramento     :f9, after f8, 0.5d

    section Fase 3: Encerramento
    Apresentação Final        :g1, after f7, 1d
    Avaliação Banca           :g2, after g1, 1d
    Arquivamento Repo         :g3, after g2, 1d
    Retrospectiva Final       :g4, after g1, 0.5d
```

---

## Marcos (Milestones) — Datas Chave

| Marco | Descrição | Data Prevista | Critério de Sdoc-arch-0006-uc-v1esso |
|-------|-----------|---------------|---------------------|
| **M0** | Kick-off + Charter Aprovado | 15/09/2026 | Gate 1: CCB assina Charter + RACI + ADR-001 |
| **M1** | Fim Sprint 1 (Auth + Docs) | 29/09/2026 | Gate 2: PRD + US + C4 + NFRs + Test Plan + RAID aprovados |
| **M2** | Fim Sprint 2 (Listas + Catálogo) | 06/10/2026 | CRUD listas funcional + Autocomplete |
| **M3** | Fim Sprint 3 (Comparação) | 13/10/2026 | Cálculo orçamento + Visualização resultados |
| **M4** | Fim Sprint 4 (Export + Perfil) | 20/10/2026 | PDF A4 + Perfil + UI Polish |
| **M5** | Fim Sprint 5 (QA + Demo) | 27/10/2026 | Gate 3: Cobertura ≥80% + Runbooks + Release + Demo |
| **M6** | Apresentação Final | 30/10/2026 | Gate 4: Banca avalia, Termo de Encerramento assinado |

---

## Dependências Críticas (Caminho Crítico)

```mermaid
graph TD
    A[ADR-001 Stack] --> B[Schema MySQL]
    B --> C[Seed Script]
    C --> D[UC09: Cadastrar Usuario]
    D --> E[UC10: Login JWT]
    E --> F[Frontend Auth Pages]
    F --> G[UC14: Salvar Lista]
    G --> H[UC15: Listar Listas]
    H --> I[UC13: Editar/Excluir]
    I --> J[Frontend Listas CRUD]
    J --> K[UC03: Selecionar Categorias]
    K --> L[UC04: Selecionar Fornecedores]
    L --> M[UC05: Filtrar Disponibilidade]
    C --> N[UC06: Calcular Orçamento]
    M --> O[UC07: Visualizar Resultados]
    N --> O
    O --> P[UC08: Export PDF]
    P --> Q[Testes E2E + Cobertura ≥80%]
    Q --> R[Demo + Apresentação]
```

**Caminho Crítico Estimado:** ~28 dias (ADR-001 → Demo)  
**Buffer Disponível:** 10 dias (Sprint 5 + Encerramento) = **35% de buffer**

---

## Recursos Alocados por Período

| Período | PO | Tech Lead | Arquiteto | Dev Back 1 | Dev Back 2 | Dev Front | QA | Orientador |
|---------|----|-----------|-----------|------------|------------|-----------|----|------------|
| Sprint 0 (5d) | 50% | 80% | 60% | 40% | 40% | 20% | 10% | 10% |
| Sprint 1 (6d) | 60% | 80% | 40% | 100% | 100% | 80% | 30% | 20% |
| Sprint 2 (6d) | 40% | 60% | 20% | 100% | 80% | 100% | 40% | 10% |
| Sprint 3 (6d) | 30% | 50% | 30% | 100% | 60% | 100% | 50% | 10% |
| Sprint 4 (6d) | 40% | 60% | 20% | 100% | 80% | 100% | 40% | 10% |
| Sprint 5 (6d) | 50% | 80% | 20% | 80% | 80% | 60% | 100% | 30% |
| Encerramento (3d) | 60% | 50% | 10% | 30% | 30% | 30% | 30% | 50% |

---

## Alertas de Cronograma

| Alerta | Gatilho | Ação |
|--------|---------|------|
| **Atraso Sprint 1 > 2 dias** | M1 não atingido em 01/10 | Replanejar Sprint 2-3, cortar escopo P2, CCB decide |
| **Cobertura < 70% no fim Sprint 4** | `pytest --cov` < 70% | Parar features, foco total em testes na Sprint 5 |
| **Integração Front↔Back falha** | Contrato OpenAPI não bate | Parar, alinhar contrato (SDD), RFC se necessário |
| **Membro indisponível > 3 dias** | Bus factor quebrado | Pair programming, redistribuir WBS, CCB avalia prazo |

---

## Controle de Versões

| Versão | Data | Autor | Mudança | Aprovado por |
|--------|------|-------|---------|--------------|
| 1.0 | 29/09/2026 | Leonardo Setti | Criação inicial baseada no WBS | CCB (Gate 2) |

---

**Fim do Cronograma**  
*Renderize o Mermaid no GitHub/GitLab/VS Code para visualização gráfica. Atualizar a cada Sprint Planning.*