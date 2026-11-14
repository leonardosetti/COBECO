# PRD — <Nome do Produto / Funcionalidade>

**Documento:** Proddoc-arch-0006-uc-v1t Requirements Document  
**Versão:** 1.0  
**Status:** Draft | Aprovado | Arquivado  
**Data:** DD/MM/AAAA  
**Autor:** <Nome> (Proddoc-arch-0006-uc-v1t Owner)  
**Revisores:** <Nomes>  
**Base:** req-func-0001-requisitos-funcionais-canon.md v3.2, req-use-case-0001-casos-de-uso-canon.md v3.2, board-roadmap-0001-roadmap-canon.md, Constitution v2.0

---

## 1. Visão Geral

### 1.1 Por que (Problem Statement)
<Descreva o problema de negócio real que este produto resolve. Use dados se disponível.>

### 1.2 O que (Solution Summary)
<Descrição de alto nível da solução: o que será entregue, para quem, qual o valor.>

### 1.3 Público-alvo e Personas
| Persona | Descrição | Necessidade Principal | Prioridade |
|---------|-----------|----------------------|------------|
| <Ex.: Comprador doméstico> | Pessoa que faz compras semanais | Comparar preços rápido | P0 |
| <Ex.: Pequeno comerciante> | Dono de mercearia | Encontrar melhores fornecedores | P1 |

---

## 2. Objetivos do Produto (OKRs)

| Objetivo (O) | Key Result (KR) | Métrica | Alvo | Como Medir |
|--------------|-----------------|---------|------|------------|
| O1: Entregar MVP funcional | KR1: 18 RFs implementados | % RFs Done | 100% | GitHub Projects |
| | KR2: Cobertura de testes | % cobertura | ≥ 80% | `pytest --cov` |
| | KR3: Deploy reproduzível | `docker compose up` | Sdoc-arch-0006-uc-v1esso | Smoke test |
| O2: Qualidade técnica | KR4: Clean Architecture | Code review | Aprovado | Rubrica R-01..R-07 |
| | KR5: Documentação ABNT | Nota orientador | ≥ 8,0 | Avaliação formal |
| O3: Aprendizado da equipe | KR6: ADRs + Specs + Handoffs | Artefatos SDD | 100% | Repo `.ai/` |

---

## 3. Requisitos Funcionais (RF) — Consolidado do SSOT v3.2

| ID | Requisito | Descrição Resumida | Prioridade | UC Relacionada | Sprint |
|----|-----------|-------------------|------------|----------------|--------|
| RF01 | Cadastrar Usuário | Nome, email, senha, pergunta segurança | P0 | UC09 | S1 |
| RF02 | Login com JWT | Access 15min + Refresh 7d (cookie httpOnly) | P0 | UC10 | S1 |
| RF03 | Logout | Invalidar refresh token | P1 | UC11 | S1 |
| RF04 | Recuperar Senha | Pergunta segurança ou token stdout | P1 | UC12 | S1 |
| RF05 | Visualizar Perfil | Dados read-only + editáveis | P1 | UC18 | S4 |
| RF06 | Gerenciar Perfil | Email, nome, senha (exige atual), ACID | P1 | UC16 | S4 |
| RF07 | Criar Lista + Autocomplete | Memória (sessionStorage) + busca produtos | P0 | UC01, UC02 | S2 |
| RF08 | Salvar / Promover Lista | Persistir no BD + migrar efêmera | P0 | UC14, UC17 | S2 |
| RF09 | Listar Minhas Listas | Paginação, ordenação, soft delete | P0 | UC15 | S2 |
| RF10 | Editar Lista | Update nome/itens | P1 | UC13 | S2 |
| RF11 | Excluir Lista | Soft delete + confirmação digitação | P1 | UC13 | S2 |
| RF12 | Selecionar Categorias | 11 checkboxes, filtra fornecedores | P0 | UC03 | S3 |
| RF13 | Selecionar Fornecedores | Checkboxes + % disponibilidade, min 2 | P0 | UC04 | S3 |
| RF14 | Filtrar Disponibilidade | Slider 0-100%, tempo real | P1 | UC05 | S3 |
| RF15 | Calcular Orçamento | Tabela flat, cache 5min, timeout 10s | P0 | UC06 | S3 |
| RF16 | Visualizar Resultados | Ordenado preço ASC, highlight verde | P0 | UC07 | S3 |
| RF17 | Exportar PDF | ReportLab, A4 server-side, visitantes+auth | P0 | UC08/UC29 | S4 |
| RF18 | Otimização Impressão | CSS @media print, headers repetidos | P1 | UC09 | S4 |

---

## 4. Requisitos Não Funcionais (RNF) — Consolidado

| ID | Requisito | Métrica / Critério | Validação |
|----|-----------|-------------------|-----------|
| RNF01 | Disponibilidade | 99,5% uptime (exclui manutenção) | Monitoramento |
| RNF02 | Documentação OpenAPI | Swagger `/docs` sempre atualizado | CI check |
| RNF03 | Banco de Dados | MySQL 8.0 InnoDB, utf8mb4, ACID | ADR-001 |
| RNF04 | UI Desktop-first | ≥1024px, Vanilla JS + Tailwind | Testes visuais |
| RNF05 | Feedback Visual | Toast, skeletons, modais | Manual + E2E |
| RNF06 | Cobertura Testes | ≥ 80% (unit + integração) | `pytest --cov-fail-under=80` |
| RNF07 | CI/CD Pipeline | ruff + pytest + build < 5 min | GitHub Actions |
| RNF08 | Seed Determinístico | 11 cat, 10 forn, 50 prod, 300 preços < 10s | Script validado |
| RNF09 | Segurança Auth | bcrypt salt=12, JWT HS256, rate limit 6/15min | Testes segurança |
| RNF10 | LGPD | Dados sintéticos only, sem PII real | Constitution Art. 3.5 |
| RNF11 | PDF Performance | < 5s para 100 itens | Benchmark |
| RNF12 | MySQL InnoDB Obrigatório | Engine InnoDB, FKs, CASCADE/RESTRICT | Migration check |

---

## 5. Escopo

### 5.1 Dentro do Escopo (MVP - Sprints 1-5)
- Todos os 18 RFs acima
- Infra Docker + CI/CD + Seed + Migrations
- Documentação ABNT + Specs SDD + Handoffs
- Testes unitários (≥80%) + E2E (Playwright)
- Demo funcional + Apresentação final

### 5.2 Fora do Escopo (Backlog Pós-MVP / RD01-RD09)
- RD01: App mobile (PWA/nativo)
- RD02: Multi-idioma (i18n)
- RD03: Notificações push/email
- RD04: Histórico de preços / gráficos
- RD05: Lista compartilhada / colaborativa
- RD06: Integração com APIs de mercado reais
- RD07: Admin panel / métricas de uso
- RD08: Quality Board Público (proposta iminente → CR-001)
- RD09: LGPD compliance com dados reais

---

## 6. Cronograma e Marcos (Roadmap)

| Sprint | Tema | Entregas Principais | Prazo | Gate |
|--------|------|---------------------|-------|------|
| S0 | Iniciação | Charter, RACI, ADR-001, GitHub Projects, Docker | 15-19/09 | Gate 1 |
| S1 | Setup, Docs, Auth | Schema, Seed, Auth (RF01-04), Docs ABNT | 22-29/09 | Gate 2 |
| S2 | Listas e Catálogo | CRUD Listas, Autocomplete (RF07-11) | 30/09-06/10 | — |
| S3 | Pré-filtro e Comparação | Categorias, Fornecedores, Cálculo (RF12-16) | 07-13/10 | — |
| S4 | Export, Perfil, Polish | PDF, Perfil, UI Feedback (RF05,06,17,18) | 14-20/10 | — |
| S5 | Buffer, QA, Demo | Testes ≥80%, CI, Runbooks, Release, Demo | 21-27/10 | Gate 3 |
| — | Encerramento | Apresentação, Post-Mortem, Termo Encerramento | 28-30/10 | Gate 4 |

---

## 7. Rastreabilidade Completa

| Artefato | Localização | Status |
|----------|-------------|--------|
| Constitution v2.0 | `constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md` | ✅ Ratificada |
| Requisitos v3.2 | `req-func-0001-requisitos-funcionais-canon.md` | ✅ SSOT |
| Casos de Uso v3.2 | `req-use-case-0001-casos-de-uso-canon.md` | ✅ SSOT |
| Camada de Dados | `doc-arch-0001-camada-de-dados-canon.md` | ✅ SSOT |
| ADR-001 Stack | `docs/decisoes/doc-adr-0001-stack-decision-v1.0.md` | ✅ Ratificada |
| Specs SDD (16) | `.ai/specs/spec-*.spec.md` | ✅ Ratificadas |
| Handoffs | `.ai/handoffs/HF-*.md` | ✅ Processo ativo |
| Roadmap | `board-roadmap-0001-roadmap-canon.md` + `doc-github-projects-0001-github-projects-canon.md` | ✅ Definido |
| PRD (este) | `docs/strategy/PRD.md` | 📝 Em elaboração |
| User Stories | `docs/strategy/USER-STORIES.md` + GitHub Issues | 📝 Pendente |
| Diagramas C4 | `docs/arquitetura/C4-*.md` | 📝 Pendente |
| RAID Log | `docs/operacao/doc-raid-log-0001-raid-log-v1.0.md` | 📝 Pendente |
| Test Plan | `docs/operacao/doc-test-plan-0001-test-plan-v1.0.md` | ✅ Existe |

---

## 8. Riscos e Mitigações (Top 10)

| ID | Risco | Prob. | Impacto | Exposição | Mitigação | Responsável |
|----|-------|-------|---------|-----------|-----------|-------------|
| PRD-R1 | Atraso Sprint 1 (Auth) | Média | Alto | Alta | Parallelizar setup + docs; pair programming | Tech Lead |
| PRD-R2 | Baixa cobertura testes | Alta | Alto | Alta | TDD desde Sprint 1; meta 80% no Definition of Done | QA |
| PRD-R3 | Integração Front↔Back falha | Média | Alto | Média | Contrato OpenAPI primeiro (SDD); RFC se divergência | Arquiteto |
| PRD-R4 | Membro equipe indisponível | Baixa | Muito Alto | Média | Bus factor 2; pair programming; redistribuir WBS | Tech Lead |
| PRD-R5 | Seed não roda < 10s | Baixa | Médio | Baixa | Otimizar queries; bulk insert; testar em CI | Dev Backend |
| PRD-R6 | PDF > 5s (100 itens) | Baixa | Médio | Baixa | ReportLab otimizado; streaming se necessário | Dev Backend |
| PRD-R7 | MySQL InnoDB conflitos FK | Média | Alto | Média | Migration testada em CI; seed valida integridade | Dev Backend |
| PRD-R8 | Docs ABNT não aprovadas | Baixa | Muito Alto | Alta | Iniciar dia 1; revisão orientador semanal | PO |
| PRD-R9 | Scope creep (features extras) | Média | Alto | Média | CR obrigatório para qualquer RF novo; CCB bloqueia | PO/CCB |
| PRD-R10 | Demo falha na apresentação | Baixa | Muito Alto | Alta | Ensaio Sprint 5; script de demo; fallback gravado | Equipe |

---

## 9. Aprovação (Gate 2 — Fim Sprint 1)

| Papel | Nome | Assinatura | Data | Decisão |
|-------|------|------------|------|---------|
| **CCB Chair / PO** | | | | ☐ Aprovar ☐ Rejeitar |
| **Tech Lead** | | | | ☐ Aprovar ☐ Rejeitar |
| **Arquiteto** | | | | ☐ Aprovar ☐ Rejeitar |
| **QA Lead** | | | | ☐ Aprovar ☐ Rejeitar |
| **Orientador Acadêmico** | | | | ☐ Aprovar ☐ Rejeitar |

---

## 10. Controle de Versões

| Versão | Data | Autor | Mudança | Aprovado por |
|--------|------|-------|---------|--------------|
| 1.0 | DD/MM/AAAA | PO | Criação inicial consolidando SSOT v3.2 | CCB (Gate 2) |

---

**Fim do PRD**  
*Este documento é vivo — atualizado a cada mudança de escopo via CR ratificado.*