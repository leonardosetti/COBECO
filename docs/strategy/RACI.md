# Matriz RACI — COBECO MVP

**Versão:** 1.0  
**Data:** 13/11/2026  
**Responsável:** Leonardo Setti (Tech Lead)  
**Aprovação:** CCB (Gate 1 — 13/11/2026)  
**Frequência de Revisão:** A cada mudança de escopo ou equipe

---

## Legenda RACI

| Código | Significado | Descrição |
|--------|-------------|-----------|
| **R** | **Responsible** | Quem executa o trabalho ("mão na massa") |
| **A** | **Accountable** | Quem aprova e responde pelo resultado (apenas **UM** por linha) |
| **C** | **Consulted** | Quem dá input antes da decisão/ação (duas vias) |
| **I** | **Informed** | Quem é avisado depois da decisão/ação (uma via) |

---

## Matriz RACI por Entregável/Atividade

| Entregável / Atividade | PO (Leo) | Tech Lead (Leo) | Arquiteto (Nicholas) | Dev Back 1 (Fabrício) | Dev Back 2 (Nicholas) | Dev Front (Eduardo) | QA (Nicolas) | Orientador |
|------------------------|:--------:|:---------------:|:--------------------:|:---------------------:|:---------------------:|:-------------------:|:------------:|:----------:|
| **Estratégia & Início** |
| Project Charter | A | R | C | I | I | I | I | C |
| Business Case | A | R | C | I | I | I | I | C |
| Stakeholder Register | A | R | I | I | I | I | I | C |
| Matriz RACI (esta) | A | R | C | I | I | I | I | I |
| Roadmap / Milestones | A | R | C | C | C | C | C | I |
| **Planejamento** |
| WBS / EAP | A | R | C | C | C | C | C | I |
| Cronograma (Gantt) | A | R | C | I | I | I | I | I |
| Sprint Planning (cada sprint) | A | R | C | R | R | R | C | I |
| **Produto & Requisitos** |
| PRD | A | C | C | C | C | C | C | I |
| User Stories + Critérios Aceite | A | C | C | C | C | C | R | I |
| Specs (SDD) | I | A | R | R | R | R | C | I |
| Protótipos / Wireframes | A | I | C | I | I | R | C | I |
| Backlog Priorização | A | C | I | C | C | C | I | I |
| **Arquitetura & Engenharia** |
| ADRs | I | A | R | C | C | C | I | I |
| RFCs | I | A | R | C | C | C | I | I |
| Diagramas C4 | I | A | R | C | C | C | I | I |
| Contratos API (OpenAPI) | I | A | R | R | R | C | C | I |
| DER / Dicionário Dados | I | A | R | R | R | I | C | I |
| NFRs | I | A | R | C | C | C | C | I |
| **Controle & Mudanças** |
| CR (Change Request) | A | R | C | C | C | C | C | I |
| RAID Log | A | R | C | C | C | C | R | I |
| Plano de Testes / QA | I | C | C | C | C | C | A/R | I |
| Status Report | A | R | I | I | I | I | I | C |
| **Entrega & Operação** |
| Runbooks | I | A | C | R | R | C | C | I |
| Release Notes | A | R | I | C | C | C | C | I |
| Deploy / Go-Live | I | A | C | R | R | R | C | I |
| Post-Mortem | A | R | R | R | R | R | R | I |
| Termo de Encerramento | A | R | C | I | I | I | I | C |

---

## Detalhamento por Sprint (Responsabilidades Principais)

### Sprint 0 (Iniciação — 15 a 19/09)
| Atividade | R | A | C | I |
|-----------|---|---|---|---|
| Charter + Business Case + Stakeholders + RACI | PO | PO | Tech Lead, Arquiteto | Equipe, Orientador |
| ADR-001 Stack | Arquiteto | Tech Lead | PO, Devs | Orientador |
| GitHub Projects (Milestones, Labels, Board, Issues S1) | Tech Lead | Tech Lead | PO | Equipe |
| Docker Compose + Makefile + CI skeleton | Dev Back 1 | Tech Lead | Dev Back 2 | Equipe |

### Sprint 1 (Setup, Docs, Auth — 22 a 29/09)
| Atividade | R | A | C | I |
|-----------|---|---|---|---|
| PRD + User Stories (RF01-RF04) | PO | PO | Tech Lead, Arquiteto, QA | Orientador |
| Diagramas C4 (Contexto, Containers, Components) | Arquiteto | Tech Lead | PO, Devs | Orientador |
| RAID Log Inicial + Test Plan | Tech Lead | Tech Lead | PO, QA | Orientador |
| Schema MySQL (8 tabelas) + Migrations | Dev Back 1 | Tech Lead | Arquiteto, Dev Back 2 | QA |
| Seed Script (300 preços <10s) | Dev Back 2 | Tech Lead | Dev Back 1 | QA |
| UC09: Cadastrar Usuário | Dev Back 1 | Tech Lead | Arquiteto | QA, Dev Front |
| UC10: Login JWT | Dev Back 1 | Tech Lead | Arquiteto | QA, Dev Front |
| UC11: Logout | Dev Back 1 | Tech Lead | — | QA, Dev Front |
| UC12: Recuperar Senha | Dev Back 1 | Tech Lead | — | QA, Dev Front |
| Frontend Auth Pages (Login, Cadastro, Recuperar) | Dev Front | Tech Lead | Dev Back 1 | QA |
| Docs ABNT (iniciar) | PO + Equipe | PO | Orientador | — |

### Sprint 2 (Listas e Catálogo — 30/09 a 06/10)
| Atividade | R | A | C | I |
|-----------|---|---|---|---|
| User Stories (RF07-RF11) | PO | PO | Tech Lead, QA | — |
| UC02: Autocomplete Produtos | Dev Front | Tech Lead | Dev Back 2 | QA |
| UC01: Lista em Memória | Dev Front | Tech Lead | — | QA |
| UC14: Salvar Lista (Persistir) | Dev Back 2 | Tech Lead | Arquiteto | QA, Dev Front |
| UC17: Promover Lista Efêmera | Dev Front | Tech Lead | Dev Back 2 | QA |
| UC15: Listar Minhas Listas | Dev Back 2 | Tech Lead | — | QA, Dev Front |
| UC13: Editar/Excluir Lista | Dev Back 2 | Tech Lead | — | QA, Dev Front |
| Frontend Listas CRUD | Dev Front | Tech Lead | Dev Back 2 | QA |

### Sprint 3 (Pré-filtro e Comparação — 07 a 13/10)
| Atividade | R | A | C | I |
|-----------|---|---|---|---|
| User Stories (RF12-RF16) | PO | PO | Tech Lead, QA | — |
| UC03: Selecionar Categorias | Dev Front | Tech Lead | Dev Back 1 | QA |
| UC04: Selecionar Fornecedores | Dev Front | Tech Lead | Dev Back 1 | QA |
| UC05: Filtrar Disponibilidade | Dev Front | Tech Lead | Dev Back 1 | QA |
| UC06: Calcular Orçamento | Dev Back 1 | Tech Lead | Arquiteto | QA, Dev Front |
| UC07: Visualizar Resultados | Dev Front | Tech Lead | Dev Back 1 | QA |

### Sprint 4 (Export, Perfil, Polish — 14 a 20/10)
| Atividade | R | A | C | I |
|-----------|---|---|---|---|
| User Stories (RF05,06,17,18) | PO | PO | Tech Lead, QA | — |
| UC08/UC29: Export PDF (ReportLab) | Dev Back 1 | Tech Lead | Arquiteto | QA, Dev Front |
| UC09: Otimização Impressão (CSS @media print) | Dev Front | Tech Lead | Dev Back 1 | QA |
| UC18: Visualizar Perfil | Dev Back 1 | Tech Lead | — | QA, Dev Front |
| UC16: Gerenciar Perfil | Dev Back 1 | Tech Lead | — | QA, Dev Front |
| Frontend Perfil | Dev Front | Tech Lead | Dev Back 1 | QA |
| Feedback Visual Global (Toast, Skeletons, Modais) | Dev Front | Tech Lead | — | QA |

### Sprint 5 (Buffer, QA, Demo — 21 a 27/10)
| Atividade | R | A | C | I |
|-----------|---|---|---|---|
| Cobertura Testes ≥80% | QA + Devs | QA | Tech Lead | PO |
| Testes E2E Playwright | QA | QA | Tech Lead | PO |
| CI/CD Pipeline (ruff + pytest + build <5min) | DevOps (Nicholas) | Tech Lead | QA | PO |
| Runbooks (Deploy, Rollback, Seed, Backup, Incidentes) | DevOps | Tech Lead | QA | PO |
| Release Notes v0.1.0 + CHANGELOG | PO | PO | Tech Lead | Orientador |
| Refinar README + OpenAPI | PO | PO | Tech Lead | Orientador |
| Preparação Apresentação (Roteiro 35min, Ensaio) | Equipe | PO | Tech Lead | Orientador |
| Post-Mortem / Lições | Tech Lead | Tech Lead | Equipe | PO |

---

## Regras de Ouro da Matriz

1. **Apenas UM "A" (Accountable)** por linha — quem tem a palavra final
2. **Pelo menos UM "R" (Responsible)** por linha — alguém precisa fazer
3. **Evitar muitos "C"** — consultar demais paralisa; limitar a 2-3 por linha
4. **"I" é ilimitado** — informar não custa caro
5. **Revisar a cada Sprint Planning** — papéis podem mudar

---

## Validação da Matriz (Gate 1)

| Verificação | Status | Observação |
|-------------|--------|------------|
| Todas as linhas têm exatamente 1 "A" | ✅ Sim | Validado |
| Todas as linhas têm pelo menos 1 "R" | ✅ Sim | Validado |
| Nenhuma coluna sobrecarregada (>60% R+A) | ✅ Sim | Tech Lead + PO têm mais A; Devs têm R distribuídos |
| Stakeholders externos (Orientador) só têm C/I | ✅ Sim | Apenas C no Charter/Business Case; I nos demais |

---

## Controle de Versões

| Versão | Data | Autor | Mudança | Aprovado por |
|--------|------|-------|---------|--------------|
| 1.0 | 13/11/2026 | Leonardo Setti | Criação inicial — Gate 1 CCB | CCB |

---

**Fim da Matriz RACI — COBECO MVP**  
*Esta matriz vive no repositório (Docs-as-Code) e é versão controlada via Git.*