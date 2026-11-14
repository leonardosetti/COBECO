# Project Charter — COBECO MVP

**Versão:** 1.0  
**Status:** Aprovado  
**Data de Criação:** 13/11/2026  
**Data de Aprovação:** 13/11/2026  
**Autor:** Leonardo Setti (Proddoc-arch-0006-uc-v1t Owner)  
**Aprovadores:** CCB (Change Control Board) — FATEC Taquaritinga ADS

---

## 1. Identificação do Projeto

| Campo | Valor |
|-------|-------|
| **Nome do Projeto** | COBECO — Comparador de Preços de Compras |
| **Código / ID** | COBECO-MVP-2026-01 |
| **Patrocinador** | FATEC Taquaritinga — Curso ADS (Laboratório de Engenharia de Software) |
| **Proddoc-arch-0006-uc-v1t Owner** | Leonardo Setti |
| **Tech Lead** | Leonardo Setti |
| **Data de Início Prevista** | 15/09/2026 |
| **Data de Término Prevista** | 30/10/2026 |
| **Metodologia** | Híbrido (PMBOK 7 + SDD + Scrum) |
| **Constituição Vigente** | `constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md` v2.0 (ratificada 13/11/2026) |

---

## 2. Justificativa e Objetivos (Business Case Resumido)

### 2.1 Problema / Oportunidade
Consumidores gastam tempo excessivo comparando preços de itens de compra em múltiplos fornecedores (mercados, farmácias, atacados). Não existe ferramenta simples, desktop-first, que permita criar uma lista, selecionar fornecedores de confiança e obter comparação consolidada com destaque da melhor oferta — tudo funcionando offline-first com exportação PDF para impressão.

### 2.2 Objetivos do Projeto (SMART)
| # | Objetivo | Métrica de Sdoc-arch-0006-uc-v1esso |
|---|----------|-------------------|
| 1 | Entregar MVP funcional com 18 RFs | 100% RFs "Done" no GitHub Projects + Demo funcional |
| 2 | Qualidade técnica ≥ mercado | Cobertura testes ≥ 80% (`pytest --cov-fail-under=80`) + Clean Architecture (code review R-01..R-07) |
| 3 | Documentação acadêmica aprovada | Nota orientador ≥ 8,0 + Banca ≥ 8,0 (ABNT) |
| 4 | Deploy reproduzível zero-config | `docker compose up` → saúde total + smoke test passa |
| 5 | Governança SDD + Constitution | 16 Specs ratificadas + Handoffs processados + ADR-001 + Gates CCB |

### 2.3 Benefícios Esperados
- **Tangíveis:** Software funcional open-source (portfolio), redução tempo comparação manual (30min → 5min em testes), artefatos de governança reutilizáveis.
- **Intangíveis:** Aprendizado Clean Architecture, SDD, PMBOK híbrido, Docker, CI/CD, testes, LGPD, trabalho em equipe 5 pessoas.

---

## 3. Escopo

### 3.1 Dentro do Escopo (In Scope)
- Autenticação completa (Cadastro, Login JWT, Logout, Recuperação Senha) — RF01-RF04
- CRUD Listas de Compras + Autocomplete produtos — RF07-RF11
- Pré-filtro (Categorias, Fornecedores, Disponibilidade) + Motor Comparação — RF12-RF16
- Exportação PDF A4 (ReportLab) + Otimização Impressão — RF17, RF18
- Perfil Usuário (Visualizar + Gerenciar) — RF05, RF06
- Infra: Docker Compose (nginx + FastAPI + MySQL 8 InnoDB), CI/CD GitHub Actions, Seed determinístico
- Documentação: ABNT, Specs SDD (16), ADR-001, C4, RAID, Test Plan, Runbooks, Release Notes
- Testes: Unit ≥80%, E2E Playwright (fluxos críticos)

### 3.2 Fora do Escopo (Out of Scope)
- Mobile / PWA / App nativo (RD01)
- Multi-idioma i18n (RD02)
- Notificações push/email (RD03)
- Histórico preços / gráficos (RD04)
- Listas compartilhadas / colaborativas (RD05)
- Integração APIs mercado reais (RD06)
- Admin panel / métricas uso (RD07)
- **Quality Board Público** (RD08) → **CR-001 aberto**, prioridade P2 pós-MVP
- LGPD com dados reais (RD09) — apenas sintéticos no MVP

### 3.3 Requisitos de Alto Nível (RFs Principais)
| ID | Requisito Funcional | Prioridade |
|----|---------------------|------------|
| RF01 | Cadastrar Usuário | P0 |
| RF02 | Login com JWT | P0 |
| RF03 | Logout | P1 |
| RF04 | Recuperar Senha | P1 |
| RF05 | Visualizar Perfil | P1 |
| RF06 | Gerenciar Perfil | P1 |
| RF07 | Criar Lista + Autocomplete | P0 |
| RF08 | Salvar / Promover Lista | P0 |
| RF09 | Listar Minhas Listas | P0 |
| RF10 | Editar Lista | P1 |
| RF11 | Excluir Lista | P1 |
| RF12 | Selecionar Categorias | P0 |
| RF13 | Selecionar Fornecedores | P0 |
| RF14 | Filtrar Disponibilidade | P1 |
| RF15 | Calcular Orçamento | P0 |
| RF16 | Visualizar Resultados | P0 |
| RF17 | Exportar PDF | P0 |
| RF18 | Otimização Impressão | P1 |

---

## 4. Premissas e Restrições

### 4.1 Premissas (Assumptions)
| # | Premissa | Impacto se Falsa |
|---|----------|------------------|
| A1 | Equipe de 5 integrantes permanece estável por 38 dias | Replanejar WBS, redistribuir carga, CCB avalia prazo |
| A2 | GitHub Free Tier + ghcr.io + Actions (2000 min/mês) suficientes | Migrar CI para self-hosted ou pagar upgrade |
| A3 | MySQL 8.0 InnoDB atende todos RFs (ACID, FK, utf8mb4) | Avaliar PostgreSQL (migração custosa, ADR necessário) |
| A4 | Vanilla JS + Tailwind atende RF07-RF18 (desktop-first) | Migrar para React (custo alto, curva aprendizado) |
| A5 | ReportLab gera PDF A4 server-side < 5s (100 itens) | Otimizar ou usar WeasyPrint (Python) |
| A6 | Orientador disponível para revisões semanais | Atraso docs ABNT → risco crítico |
| A7 | Banca aceita demo técnica + docs ABNT | Ajustar entregáveis |
| A8 | Dados sintéticos atendem LGPD (Constitution Art. 3.5) | Revisar seed + testes |
| A9 | Docker Compose roda em máquinas dos 5 integrantes | Padronizar via GitHub Codespaces |
| A10 | Constitution v2.0 permanece vigente sem mudanças maiores | Revisar todos artefatos |

### 4.2 Restrições (Constraints)
| # | Restrição | Tipo |
|---|-----------|------|
| C1 | Prazo fixo: 30 dias úteis (5 sprints de 6 dias + buffers) | Tempo |
| C2 | Equipe de 5 integrantes (1 PO/TL, 2 Backend, 1 Frontend, 1 QA compartilhado) | Recurso |
| C3 | Orçamento zero (recursos próprios, ferramentas FOSS) | Custo |
| C4 | Stack definida em ADR-001 (FastAPI, MySQL, Vanilla JS, nginx, ReportLab) | Tecnologia |
| C5 | Constitution v2.0 como lei suprema (Art. 5.1 CCB, Art. 6 SDD, Art. 3 KISS/YAGNI) | Governança |
| C6 | Entrega acadêmica: 18/09/2026 às 19h (docs ABNT) + Apresentação 30/10/2026 | Prazo duro |

---

## 5. Riscos Principais (Top 5)

| ID | Risco | Prob. | Impacto | Exposição | Mitigação |
|----|-------|-------|---------|-----------|-----------|
| R-001 | Atraso Sprint 1 (Auth + Docs) não entrega a tempo do Gate 2 | Média | Crítico | **ALTA** | Parallelizar setup+docs dia 1; Pair programming Auth; Docs ABNT iniciam dia 1; CCB replaneja se >2 dias atraso |
| R-002 | Cobertura testes < 80% no fim do projeto | Alta | Crítico | **ALTA** | TDD obrigatório Sprint 1; Metas intermediárias (60% S2, 70% S3, 75% S4); Sprint 5 foco total testes se <75% |
| R-003 | Integração Front↔Back falha (contrato OpenAPI divergente) | Média | Alto | **MÉDIA** | Spec-first (SDD): contrato na Spec → Handoff → Impl; RFC obrigatório se divergência >1 dia; Testes contrato no CI |
| R-004 | Membro chave indisponível (>3 dias) | Baixa | Crítico | **MÉDIA** | Bus factor 2 (Backend: 2 devs); Pair programming rotativo; WBS com slack; CCB avalia extensão se >5 dias |
| R-008 | Docs ABNT não aprovadas pelo orientador | Baixa | Crítico | **MÉDIA** | Iniciar docs dia 1; Revisão orientador semanal; Template ABNT pré-aprovado; Pair writing PO+dev |

---

## 6. Stakeholders Principais

| Nome | Papel | Interesse | Poder | Engajamento Necessário |
|------|-------|-----------|-------|------------------------|
| Leonardo Setti | Proddoc-arch-0006-uc-v1t Owner / Tech Lead | Alto | Alto | Liderar + Decidir técnico |
| Fabrício Cabral | Dev Backend 1 | Médio | Baixo | Executar |
| Nicholas Anthony | Dev Backend 2 | Médio | Baixo | Executar |
| Eduardo Passarelli | Dev Frontend | Médio | Baixo | Executar |
| Nicolas Mallouk | QA / Dev Backend (compartilhado) | Médio | Baixo | Validar + Executar |
| Orientador Acadêmico | Governança Externa | Alto | Alto | Aprovar marcos |
| Banca Avaliadora (3 profs) | Avaliação Final | Alto | Alto | Avaliar entrega final |
| Coordenação Curso ADS | Patrocinador | Médio | Alto | Informado (Status Report mensal) |
| FATEC Taquaritinga | Instituição | Baixo | Alto | Informado (Relatório final) |

---

## 7. Estrutura de Governança

### 7.1 Change Control Board (CCB)
| Papel | Nome | Autoridade |
|-------|------|------------|
| Chair / PO | Leonardo Setti | Decisão final de escopo, prazo, orçamento |
| Tech Lead | Leonardo Setti | Viabilidade técnica, arquitetura |
| Arquiteto | Nicholas Anthony | Qualidade, NFRs, ADRs |
| QA Lead | Nicolas Mallouk | Testes, cobertura, release gate |

### 7.2 Gates de Aprovação (Stage Gates)
| Gate | Momento | Critério | Aprovadores |
|------|---------|----------|-------------|
| **Gate 1** | Início (Kick-off 15/09) | Charter + RACI + ADR-001 ratificados | CCB |
| **Gate 2** | Fim Sprint 1 (29/09) | PRD + User Stories + C4 + NFRs + Test Plan + RAID Log aprovados | CCB |
| **Gate 3** | Fim Sprint 5 (27/10) | Cobertura ≥80% + Runbooks + Release Notes + Demo funcional | CCB + Orientador |
| **Gate 4** | Encerramento (30/10) | Termo Encerramento + Lições + Post-Mortem | CCB + Banca |

---

## 8. Orçamento e Recursos

| Recurso | Quantidade | Custo Unitário | Total | Observação |
|---------|------------|----------------|-------|------------|
| Desenvolvedores (alunos) | 5 | R$ 0,00 | R$ 0,00 | Equipe acadêmica |
| GitHub (repo + Actions + Projects) | — | Gratuito | R$ 0,00 | Free tier |
| Docker Hub / ghcr.io | — | Gratuito | R$ 0,00 | Free tier |
| MySQL (container) | — | Gratuito | R$ 0,00 | FOSS |
| Domínio/SSL | — | Gratuito | R$ 0,00 | Não necessário (localhost) |

**Orçamento Total: R$ 0,00** (Projeto acadêmico sem custo financeiro)

---

## 9. Cronograma Macro (Milestones)

| Milestone | Descrição | Data Prevista | Gate |
|-----------|-----------|---------------|------|
| M0 | Kick-off + Charter + RACI + ADR-001 + GitHub Projects + Docker | 15/09/2026 | Gate 1 |
| M1 | Sprint 1: Setup, Docs, Auth (Schema, Seed, RF01-RF04, Docs ABNT) | 29/09/2026 | Gate 2 |
| M2 | Sprint 2: Listas e Catálogo (RF07-RF11) | 06/10/2026 | — |
| M3 | Sprint 3: Pré-filtro e Comparação (RF12-RF16) | 13/10/2026 | — |
| M4 | Sprint 4: Export, Perfil, Polish (RF05,06,17,18) | 20/10/2026 | — |
| M5 | Sprint 5: Buffer, QA, Demo (Testes ≥80%, CI, Runbooks, Release, Demo) | 27/10/2026 | Gate 3 |
| M6 | Apresentação Final + Encerramento | 30/10/2026 | Gate 4 |

---

## 10. Critérios de Sdoc-arch-0006-uc-v1esso do Projeto

| Critério | Meta | Como Medir |
|----------|------|------------|
| Entrega de todos RFs (18) | 100% | GitHub Projects "Done" + Demo |
| Cobertura de testes | ≥ 80% | `pytest --cov-fail-under=80` |
| Documentação ABNT | Aprovada | Orientador + Banca (nota ≥ 8,0) |
| Deploy funcional | `docker compose up` | Smoke test em staging |
| Apresentação final | Nota ≥ 8,0 | Banca avaliadora |
| Governança SDD | 16 Specs + Handoffs + ADR | Repo `.ai/` versionado |

---

## 11. Aprovação Formal (CCB) — Gate 1 (13/11/2026)

| Papel | Nome | Assinatura | Data | Voto |
|-------|------|------------|------|------|
| **CCB Chair / PO** | Leonardo Setti | _______________ | 13/11/2026 | ☑ Aprovar |
| **Tech Lead** | Leonardo Setti | _______________ | 13/11/2026 | ☑ Aprovar |
| **Arquiteto** | Nicholas Anthony | _______________ | 13/11/2026 | ☑ Aprovar |
| **QA Lead** | Nicolas Mallouk | _______________ | 13/11/2026 | ☑ Aprovar |

---

## 12. Controle de Versões

| Versão | Data | Autor | Descrição da Mudança |
|--------|------|-------|----------------------|
| 1.0 | 13/11/2026 | Leonardo Setti | Criação inicial — Gate 1 CCB |

---

**Fim do Project Charter — COBECO MVP**  
*Este documento vive no repositório (Docs-as-Code) e é versão controlada via Git.*