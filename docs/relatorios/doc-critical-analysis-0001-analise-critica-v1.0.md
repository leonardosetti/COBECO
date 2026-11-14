# Relatório Analítico Crítico — COBECO MVP

**Artefato:** Análise e controle técnico, negocial e de ambiente  
**Versão:** 1.1  
**Rodada:** 3 (incorpora Rodadas 1 e 2; a Rodada 1 existiu apenas na saída de prompt e não foi formalizada via arquivo)  
**Data:** 09 de Novembro de 2026  
**Status:** Decisão tomada — stack B oficializada  
**Destino:** `docs/relatorios/doc-critical-analysis-0001-analise-critica-v1.0.md` (SSOT de análise crítica; atualizado a cada rodada)

---

## Histórico de versões

| Versão | Data | Rodada | Conteúdo | Autor |
|--------|------|--------|----------|-------|
| 0.1 | — | 1 | Saída de prompt apenas (não formalizada via arquivo) | NEXUS-PRIME |
| 1.0 | 09/11/2026 | 2 | Peça 1 (objetivo, artefatos, conflito de stack, viabilidade técnica e negocial) + Peça 2 (tabela de falhas + proposições de ajuste) | NEXUS-PRIME |
| 1.1 | 09/11/2026 | 3 | Decisão de stack B oficializada (FastAPI + MySQL 8 + ReportLab); plano A arquivado como ADR; início da Peça 3 (plano de execução SDD/AI-Driven) | NEXUS-PRIME |

---

## 1. Objetivo e propósito do projeto

**Objetivo geral (doc-readme-0001-readme-canon):** Desenvolver um MVP funcional e minimalista que automatize a comparação de preços entre fornecedores a partir de listas de compras criadas pelo usuário, fornecendo orçamentos claros e evidenciando produtos ausentes.

**Propósito real detectado:** Projeto acadêmico da disciplina de Laboratório de Engenharia de Software (FATEC Taquaritinga — ADS). A entrega imediata avaliada é a documentação do projeto em PDF (ABNT) com apresentação em sala (30–35 min, 5 integrantes), prazo fixo de 18/09/2026 19h (wrk_grp.md). O desenvolvimento do software é a segunda fase.

**Avaliação crítica:** O propósito está bifurcado. O doc-readme-0001-readme-canon trata o software como produto (MVP com prazo 13/11/2026, 30 dias, 5 fases). O wrk_grp.md trata a documentação como o entregável avaliado agora. Não há clareza sobre qual prazo rege o trabalho da equipe, gerando risco de desalinhamento de esforço.

---

## 2. Artefatos produzidos — inventário e maturidade

| Artefato | Status | Observação |
|----------|--------|------------|
| doc-readme-0001-readme-canon.md | Docs | Visão, stack, cronograma, out of scope. Última atualização 31/08/2026. |
| req-func-0001-requisitos-funcionais-canon.md v3.2 | SSOT | 18 RFs, 12 RNFs, 9 desejáveis. Aprovado 14/09/2026. |
| req-use-case-0001-casos-de-uso-canon.md v3.2 | SSOT | 29 UCs (19 principais + 10 internos), matriz de rastreabilidade RF→UC. |
| doc-arch-0001-camada-de-dados-canon.md v3.2 | SSOT | DER com 8 tabelas, nomenclatura PT-BR, seed documentado. |
| board-roadmap-0001-roadmap-canon.md | Plano | 5 milestones, 5 sprints, Kanban, DoD, branch pattern feat/UC-XX. |
| constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md | Lei suprema | Governança de agentes, SDD, hierarquia normativa, Kill Switch. |
| doc-agents-0001-agents-canon.md | Estado do repo | Confirma: docs only, nenhum código, stack conflitante, comandos não verificados. |
| brain/md/* (5 arquivos) | Docs | Refinamento de requisitos, casos de uso, especificação MVP, análise fundamental, manual. |
| brain/diagrams/* | Diagramas | DER, casos de uso, estado, protótipos Excalidraw (.drawio, .xml, .png). |
| excalidraw_baixa/* | Protótipos | Baixa fidelidade (SVG/PNG). |
| doc-figma-0001-figma-export-v1.0.html, COBECO_prtp_high_v*.html | Protótipos | Alta fidelidade exportada (v1.0, v1.1, v2.0). |
| Projeto_COBECO.docx | Monografia | 19,9 MB — modelo ABNT. |
| prj_docs/COBECO_Monografia_new.docx | Monografia | 985 KB — cópia da monografia. |
| graphify-out/ | Grafo | Grafo de conhecimento já construído (GRAPH_REPORT.md existente). |
| node_modules/ | Dependências | Presentes no root — suspeito para um repo "docs only". |

**Avaliação:** Requisitos, casos de uso e dados estão coerentes entre si (v3.2) e possuem rastreabilidade. Documentação de apoio (monografia, protótipos, diagramas) existe. Ausente: qualquer código-fonte, `config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml`, `config-env-0001-env-example-v1.0.example`, testes, CI/CD, OpenAPI/swagger, scripts de seed, `.github/` workflows. Conforme doc-agents-0001-agents-canon.md e constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon, o repositório está em fase de design — nenhuma implementação iniciada.

---

## 3. Conflito de stack crítico (bloqueador de arranque)

Dois planos de stack mutuamente exclusivos, nenhum verificado por código:

- **doc-readme-0001-readme-canon.md (31/08/2026):** React 18 + TS + Vite + Tailwind + shadcn/ui (:8080) + Node.js 20 + NestJS 10 (:3000) + PostgreSQL 16 + Prisma 5 (:5432) + Docker Compose + GitHub Actions + Jest + Vitest. Email: Resend + Mailhog.
- **board-roadmap-0001-roadmap-canon.md (15/09/2026):** FastAPI + Pydantic backend + MySQL 8 InnoDB + pytest/ruff + ReportLab PDF export.

**Conflitos concretos:**
1. Banco: PostgreSQL (doc-readme-0001-readme-canon) vs MySQL (board-roadmap-0001-roadmap-canon + doc-arch-0001-camada-de-dados-canon.md especifica MySQL InnoDB).
2. Backend: NestJS/Node (doc-readme-0001-readme-canon) vs FastAPI/Python (board-roadmap-0001-roadmap-canon + req-func-0001-requisitos-funcionais-canon.md menciona Pydantic, pytest, ReportLab).
3. Testes: Jest+Vitest (doc-readme-0001-readme-canon) vs pytest/ruff (board-roadmap-0001-roadmap-canon).
4. ORM: Prisma (doc-readme-0001-readme-canon) vs "zero ORM pesado, Repository pattern" (doc-arch-0001-camada-de-dados-canon.md).
5. PDF: apenas CSV + print navegador (doc-readme-0001-readme-canon out of scope) vs ReportLab server-side (req-func-0001-requisitos-funcionais-canon.md RF17, board-roadmap-0001-roadmap-canon S4).
6. Nomenclatura: PT-BR (DoD, doc-arch-0001-camada-de-dados-canon) vs inglês típico do ecossistema Node/Nest.

**Decisão (Rodada 3, 09/11/2026):** Stack **B** oficializada — FastAPI + Pydantic + MySQL 8 InnoDB + pytest/ruff + ReportLab + Docker Compose + GitHub Actions. Plano A (doc-readme-0001-readme-canon/NestJS+PostgreSQL+Prisma) arquivado como ADR e não será implementado. Justificativa: alinhamento com req-func-0001-requisitos-funcionais-canon.md v3.2 (Pydantic, ReportLab, MySQL InnoDB), doc-arch-0001-camada-de-dados-canon.md (MySQL InnoDB, zero ORM pesado) e board-roadmap-0001-roadmap-canon.md (plano mais recente, 15/09/2026).

**Impacto:** Bloqueador P0 resolvido. A stack B é agora o SSOT de implementação. O doc-readme-0001-readme-canon.md e o board-roadmap-0001-roadmap-canon.md devem ser atualizados para refletir a stack B (remoção de referências ao plano A). Até que esses documentos sejam alinhados, toda estimativa de esforço baseada no plano A está inválida.

---

## 4. Viabilidade técnica

**Favorável:**
- Escopo enxuto (KISS), dados mockados via seed, sem APIs externas/scraping no MVP.
- Arquitetura limpa definida (4 camadas: Domain → UseCase → Adapter → Framework).
- ACID via transações explícitas, soft delete, FKs com CASCADE/RESTRICT.
- FOSS-first, zero cloud, zero CUDA (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon Art. 1.2) — compatível com hardware local 8700G/60GB.
- Rastreabilidade RF→UC→UC interno bem feita.

**Riscos técnicos:**
- Autenticação: JWT access em memória + refresh httpOnly cookie; recuperação de senha via pergunta de segurança (sem email) — padrão fraco.
- Rate limiting híbrido por IP + username sob NAT (empresa/escola) é frágil.
- Lista em memória (sessionStorage) sem persistência para visitantes — perda de dados em recarga é comportamento documentado, mas UX ruim.
- `RECOVERY_MODE=log` (token no stdout) expõe token de recuperação em logs de container — risco LGPD/segurança.
- Nenhuma tabela de sessão/refresh_tokens no DER (YAGNI), mas RF02 exige refresh token 7d — contradição entre DER e requisito.
- Ausência de testes, CI, Docker, OpenAPI hoje — tudo está no planejamento, nada executado.

---

## 5. Viabilidade negocial/acadêmica

**Favorável:**
- Problema real (comparação de preços) com valor compreensível para banca e usuários.
- Escopo MVP delimitado com out of scope claro.
- Cronograma de 30 dias dividido em 5 fases (doc-readme-0001-readme-canon) ou 5 sprints de ~6 dias (board-roadmap-0001-roadmap-canon).
- 5 integrantes definidos (wrk_grp.md), distribuição de falas igualitária exigida na apresentação.

**Riscos negociais:**
- Prazo de documentação (18/09/2026) expirado (hoje é 09/11/2026) — risco de entrega atrasada/reprovada na disciplina.
- Prazo de software (13/11/2026) a 4 dias — inviável começar do zero agora sem código.
- Proddoc-arch-0006-uc-v1t Owner, Tech Lead e Arquiteto não nomeados (doc-readme-0001-readme-canon placeholders "[Nome]").
- Nenhum nome de integrante na documentação → wrk_grp.md adverte: sem nome, não há nota.
- Stack não definida → impossível orçar infra, hospedagem, ou definir time-to-market.

---

## 6. Tabela de falhas — prioridade e criticidade

| # | Falha | Tipo | Prioridade | Criticidade | Contexto / Evidência |
|---|-------|------|------------|-------------|----------------------|
| F01 | Stack duplo não resolvido (doc-readme-0001-readme-canon vs board-roadmap-0001-roadmap-canon) | Técnica / Programática | P0 | Bloqueia arranque de código | doc-readme-0001-readme-canon (31/08) vs board-roadmap-0001-roadmap-canon (15/09); nenhum código existe |
| F02 | DER sem tabela de sessão/refresh_tokens, mas RF02 exige refresh 7d | Técnica / Lógica | P1 | Inconsistência requisito vs modelo de dados | doc-arch-0001-camada-de-dados-canon.md (8 tabelas, YAGNI sem sessão) vs req-func-0001-requisitos-funcionais-canon.md RF02 |
| F03 | RECOVERY_MODE=log expõe token de recuperação em stdout | Técnica / Negocial | P1 | Risco LGPD / exposição de segredo | req-use-case-0001-casos-de-uso-canon.md UC12 HP2; constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon Art. 7.1 |
| F04 | PO, Tech Lead, Arquiteto não nomeados | Negocial / Contextual | P1 | Sem responsabilização clara | doc-readme-0001-readme-canon placeholders "[Nome]" |
| F05 | Prazo de documentação (18/09/2026) expirado | Negocial / Contextual | P1 | Risco de reprovação na disciplina | wrk_grp.md Due September 18, 2026; hoje 09/11/2026 |
| F06 | Prazo de software (13/11/2026) a 4 dias, sem código | Negocial | P0 | Inviável entregar MVP do zero agora | doc-readme-0001-readme-canon Fase 1–5, total 30 dias, data limite 13/11/2026 |
| F07 | node_modules no root de repo "docs only" | Programática / Contextual | P2 | Polui repositório; indica scaffolding interrompido | doc-agents-0001-agents-canon.md: "No config-npm-0001-config-npm-0001-config-npm-0001-config-npm-0001-package-v1-v1.0-v1.0-v1.0.json..."; node_modules presente no root |
| F08 | Autenticação via pergunta de segurança sem email | Técnica / Negocial | P2 | Padrão fraco de recuperação | req-use-case-0001-casos-de-uso-canon.md UC12; req-func-0001-requisitos-funcionais-canon.md RF04 |
| F09 | Rate limiting híbrido IP+username sob NAT | Técnica | P2 | Frágil em ambientes corporativos/escolares | req-use-case-0001-casos-de-uso-canon.md UC10 EC4 |
| F10 | Lista em memória (sessionStorage) perdida em recarga | Técnica / UX | P2 | Perda de dados do visitante | req-use-case-0001-casos-de-uso-canon.md UC01 HP2 |
| F11 | Sem testes, CI, Docker, OpenAPI implementados | Técnica / Programática | P1 | DoD não atingível sem código | doc-agents-0001-agents-canon.md; board-roadmap-0001-roadmap-canon DoD |
| F12 | Nomes de integrantes ausentes na documentação | Negocial / Contextual | P1 | wrk_grp adverte: sem nome, sem nota | wrk_grp.md linhas 35, 39–47 |

---

## 7. Proposições de ajuste (rodada 2)

| ID | Proposição | Escopo | Responsável sugerido | Prazo sugerido |
|----|------------|--------|----------------------|----------------|
| A1 | **Decidir stack única** (NestJS+React+PostgreSQL+Prisma OU FastAPI+MySQL+ReportLab) e arquivar o plano não escolhido como ADR | Técnica / Programática | Tech Lead + Arquiteto | Imediato (bloqueia tudo) |
| A2 | Nomear Proddoc-arch-0006-uc-v1t Owner, Tech Lead e Arquiteto no doc-readme-0001-readme-canon e na monografia | Negocial / Contextual | Grupo | Imediato |
| A3 | Regularizar documentação: entregar PDF atrasado com justificativa ou redefinir prazo com o professor | Negocial / Contextual | Grupo + Professor | Imediato (prazo expirado) |
| A4 | Revisar DER: incluir tabela de sessão/refresh_tokens OU remover requisito de refresh de RF02 | Técnica / Lógica | Arquiteto | Antes de codificar auth |
| A5 | Remover `RECOVERY_MODE=log` ou proteger logs contra retenção de tokens | Técnica / Segurança | Backend | Antes de codificar recuperação |
| A6 | Redefinir escopo realista para os ~4 dias restantes (MVP enxuto: catálogo + comparação, sem auth complexa) OU adiar para próximo ciclo | Negocial / Técnica | PO + Tech Lead | Imediato |
| A7 | Limpar `node_modules` do root do repositório | Programática | Qualquer integrante | Imediato |
| A8 | Implementar testes, CI, Docker, OpenAPI conforme DoD antes de qualquer merge | Técnica / Programática | QA + Backend + Frontend | Durante desenvolvimento |
| A9 | Incluir nomes de todos os 5 integrantes na monografia/PDF e no doc-readme-0001-readme-canon | Negocial / Contextual | Grupo | Antes da entrega da documentação |

---

## 8. Decisão pendente — prompt de decisão

**Decisão requerida:** Qual stack o COBECO deve implementar?

**Opções:**
- **A)** Stack doc-readme-0001-readme-canon: React 18 + TS + Vite + Tailwind + shadcn/ui + Node.js 20 + NestJS 10 + PostgreSQL 16 + Prisma 5 + Docker Compose + GitHub Actions + Jest + Vitest.
- **B)** Stack board-roadmap-0001-roadmap-canon: FastAPI + Pydantic + MySQL 8 InnoDB + pytest/ruff + ReportLab + Docker Compose + GitHub Actions.
- **C)** Outra stack (especificar com justificativa).

**Critérios de decisão:** alinhamento com req-func-0001-requisitos-funcionais-canon.md v3.2 (Pydantic, ReportLab, MySQL InnoDB sugerem B), alinhamento com doc-arch-0001-camada-de-dados-canon.md (MySQL InnoDB, zero ORM pesado sugere B), familiaridade da equipe, prazo restante (~4 dias).

**Aguardando resposta do grupo/PO/Tech Lead para prosseguir com a Peça 3 (plano de execução SDD/AI-Driven e artefatos mandatórios para pré-produção).**

---

## 9. Próximas peças planejadas

- **Peça 4:** Matriz de conformidade de produção (DoD, CI, testes, LGPD, segurança) com checklist de aceitação.
- **Peça 5:** Relatório consolidado final para tomada de decisão e handoff para produção.

---

## 10. Peça 3 — Plano de execução SDD/AI-Driven Development (ondas, gates, artefatos mandatórios)

**Base normativa:** constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md Art. 6 (Método SDD), Art. 4 (Governança de agentes), doc-agents-0001-agents-canon.md (DoD), board-roadmap-0001-roadmap-canon.md (5 sprints, milestones).  
**Stack oficial:** B (FastAPI + Pydantic + MySQL 8 InnoDB + pytest/ruff + ReportLab + Docker Compose + GitHub Actions).  
**Orquestrador:** NEXUS-PRIME ULTIMATE (L0) — despacha via `scripts/script-dispatch-0001-nexus-dispatcher-v1.0.py`, roster em `.ai/agents/config-registry-0001-registry-v1.0.yaml`.

### 10.1 Princípios SDD (não negociáveis)

- Todo fluxo entra como spec (`.ai/specs/*.md`) e sai como handoff (`.ai/handoffs/HF-*.md`).
- Handoff passa pelo `handoff_parser.py` **antes** do dispatch.
- Cadeia de merge: reviewer (rubrica R-01..R-07) → qa-sdet (evidência) → CI verde → gatekeeper → aprovação humana (CCB).
- Nenhum agente escreve código, specs ou arquivos de outro agente sem dispatch do L0.
- Half-duplex: cada despacho retorna parcel com `dod` e `kill_switch`.

### 10.2 Ondas de execução (adaptado aos ~4 dias restantes)

Dado o prazo crítico (prazo de software 13/11/2026, hoje 09/11/2026), as ondas são enxutas e focadas no MVP viável:

| Wave | Foco | Artefatos de entrada (spec) | Artefatos de saída (handoff) | Gate de saída |
|------|------|----------------------------|------------------------------|---------------|
| W0 | Setup e infra | `.ai/specs/infra-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0.md` | `config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml`, `config-env-0001-env-example-v1.0.example`, `Dockerfile.backend`, `Dockerfile.frontend` | `docker compose up` sobe sem config manual |
| W1 | Schema e seed | `.ai/specs/db-schema-mysql.md` | 8 tabelas PT-BR (doc-arch-0001-camada-de-dados-canon.md v3.2), `seed.py` (11 cat + 10 forn + 50 prod + ~300 preços) | `make seed` <10s; schema valida FKs/CHECK |
| W2 | Autenticação core | `.ai/specs/auth-jwt.md` | Endpoints cadastro/login/logout, bcrypt salt=12, JWT access 15m + refresh 7d httpOnly, rate limit 6/15m | Testes unitários auth ≥80%; sem brute-force |
| W3 | Listas e catálogo | `.ai/specs/listas-catalogo.md` | CRUD listas, itens_lista, autocomplete produtos, categoria pré-filtro | Transação ACID lista+itens; FK validadas |
| W4 | Comparação e export | `.ai/specs/comparacao-export.md` | Motor de cálculo flat, cache 5min, timeout 10s, endpoint PDF (ReportLab), impressão `@media print` | Cálculo <2s (100 itens + 10 forn); PDF <5s (100 itens) |
| W5 | QA, CI e demo | `.ai/specs/qa-ci.md` | `pytest` + `ruff`, CI workflow GitHub Actions, cobertura ≥80%, doc-readme-0001-readme-canon atualizado | Pipeline <5min; CI verde; DoD completo |

**Restrição de prazo:** Com 4 dias restantes, W0–W2 são obrigatórios para MVP mínimo; W3–W5 são desejáveis. Se houver corte, priorizar: auth básico + catálogo + comparação flat (sem PDF complexo).

### 10.3 Gates de qualidade (FAIL-CLOSED)

| Gate | Condição | Ação em falha |
|------|----------|---------------|
| G0 | `scripts/sync_agent_registry.py --check` exit 0 | BLOCK `REGISTRY_UNREAD` |
| G1 | `nexus_dispatcher --check task.json` = ACCEPT | Sem dispatch; envelope rejeitado retorna ao remetente |
| G2 | `pytest tests/agents/` verde | BLOCK de dispatch em massa até ficar verde |
| G3 | Handoff válido via `handoff_parser.py` v2 | Sem handoff válido → não dispacha |
| G4 | Parcel retornado com `dod == true` | Tarefa não encerra; não entra em agregação "done" |
| G5 | Kill Switch invocado | Para todo roteamento; log; escala ao humano |
| G6 | Constitution Art. 4 (15 vetores) | Recusa imediata, sem negociação |

### 10.4 Artefatos mandatórios para pré-produção

| Artefato | Caminho | Obrigatoriedade | Fonte |
|----------|---------|-----------------|-------|
| Spec de infra | `.ai/specs/infra-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0.md` | Obrigatório (W0) | L0 → agent-infra |
| Spec de schema DB | `.ai/specs/db-schema-mysql.md` | Obrigatório (W1) | L0 → agent-db |
| Spec de auth | `.ai/specs/auth-jwt.md` | Obrigatório (W2) | L0 → agent-auth |
| Spec de listas | `.ai/specs/listas-catalogo.md` | Obrigatório (W3) | L0 → agent-backend |
| Spec de comparação | `.ai/specs/comparacao-export.md` | Obrigatório (W4) | L0 → agent-backend |
| Spec de QA/CI | `.ai/specs/qa-ci.md` | Obrigatório (W5) | L0 → agent-qa |
| Handoffs válidos | `.ai/handoffs/HF-*.md` | Obrigatório toda wave | `handoff_parser.py` v2 |
| Ledger de tarefas | `.ai/agents/config-ledger-0001-ledger-v1.0.yaml` | Obrigatório (append-only) | NEXUS-PRIME |
| Roster SSOT | `.ai/agents/config-registry-0001-registry-v1.0.yaml` | Obrigatório | `sync_agent_registry.py --check` |
| ADR de stack | `docs/decisoes/adr-stack-b.md` | Obrigatório (decisão B) | NEXUS-PRIME |
| DoD checklist | `docs/dod-checklist.md` | Obrigatório | board-roadmap-0001-roadmap-canon.md seção 4 |

### 10.5 Roteiro imediato (próximas 48–72h)

1. **Nomear PO, Tech Lead, Arquiteto** (proposição A2) — sem isso, não há quem assine specs nem aprove merges.
2. **Criar ADR de stack B** (`docs/decisoes/adr-stack-b.md`) arquivando o plano A.
3. **Atualizar doc-readme-0001-readme-canon.md e board-roadmap-0001-roadmap-canon.md** para stack B (remoção de referências ao plano A).
4. **Limpar `node_modules` do root** (proposição A7).
5. **Escrever spec W0** (`.ai/specs/infra-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0.md`) e dispatchar via L0.
6. **Aguardar parcel com `dod == true`** antes de iniciar W1.

---

## 11. Peça 4 — Matriz de conformidade de produção (DoD, CI, testes, LGPD, segurança)

**Base:** board-roadmap-0001-roadmap-canon.md seção 4 (Definition of Done), constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md Art. 7 (Segurança) e Art. 8 (Qualidade), req-func-0001-requisitos-funcionais-canon.md RNFs.

### 11.1 Checklist de conformidade por camada

| # | Item | Camada | Fonte | Obrigatório | Meio de verificação |
|---|------|--------|-------|-------------|---------------------|
| C01 | Código segue Clean Architecture (4 camadas); nenhuma vazão de framework para o Domain | Backend | board-roadmap-0001-roadmap-canon DoD | Sim | Code review (rubrica R-01..R-07) |
| C02 | Todas as queries usam parameterized queries (proteção contra SQLi) | Backend | board-roadmap-0001-roadmap-canon DoD | Sim | Review + teste de injeção |
| C03 | Nomenclatura de banco e variáveis em PT-BR (conforme DER v3.2) | Banco/Backend | board-roadmap-0001-roadmap-canon DoD | Sim | Grep de identificadores em inglês |
| C04 | Testes unitários escritos; cobertura não diminuiu (≥80% módulos tocados) | Backend/Frontend | board-roadmap-0001-roadmap-canon DoD + constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon Art. 8.1 | Sim | `pytest --cov` / `vitest --coverage` |
| C05 | Contrato OpenAPI (`/docs`) atualizado (SDD) | Backend | board-roadmap-0001-roadmap-canon DoD | Sim | Swagger acessível; spec condiz com endpoints |
| C06 | Funciona via `docker compose up` sem config manual extra | Infra | board-roadmap-0001-roadmap-canon DoD | Sim | Build limpo do zero; `docker compose up -d` |
| C07 | Schema MySQL 8 InnoDB com 8 tabelas PT-BR, FKs CASCADE/RESTRICT, soft delete | Banco | doc-arch-0001-camada-de-dados-canon.md v3.2 | Sim | `SHOW CREATE TABLE`; DER v3.2 |
| C08 | Seed: 11 categorias + 10 fornecedores + 50 produtos + ~300 preços em <10s | Banco | doc-arch-0001-camada-de-dados-canon.md v3.2 + RNF08 | Sim | `make seed` <10s |
| C09 | Autenticação: bcrypt salt=12; JWT access 15m (memória) + refresh 7d (httpOnly) | Backend | req-func-0001-requisitos-funcionais-canon.md RF01/RF02 | Sim | Inspeção de código; teste de token |
| C10 | Rate limiting 6 tentativas/15min por IP + username | Backend | req-func-0001-requisitos-funcionais-canon.md RF02 + RNF10 | Sim | Teste de brute-force simulado |
| C11 | Recuperação de senha sem `RECOVERY_MODE=log` (sem token em stdout) | Backend | constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon Art. 7.1 | Sim | Ausência de `console.log`/`print` de token |
| C12 | LGPD: dados sintéticos apenas; sem PII reais em seeds, fixtures, logs, backups | Todos | constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon Art. 3.5 | Sim | Revisão de seeds e fixtures |
| C13 | FOSS-first: nenhuma dependência paga/proprietária sem Bypass de 3 pilares | Todos | constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon Art. 3.6 | Revisão de `requirements.txt` / `config-npm-0001-config-npm-0001-config-npm-0001-config-npm-0001-package-v1-v1.0-v1.0-v1.0.json` |
| C14 | Erros não expõem tracebacks, payloads de usuário ou dados financeiros | Backend | constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon Art. 7.3 | Sim | Teste de erro forçado; inspeção de responses |
| C15 | Feedback visual <100ms (toasts, loading, modais) | Frontend | req-func-0001-requisitos-funcionais-canon.md RNF05 | Sim | Teste de interface |
| C16 | Layout desktop-only ≥1024px | Frontend | req-func-0001-requisitos-funcionais-canon.md RNF04 | Sim | Breakpoint único; teste de resolução |
| C17 | API <500ms p95 | Backend | req-func-0001-requisitos-funcionais-canon.md RNF09 | Sim | `curl + time`; carga simulada |
| C18 | PDF gerado <5s para listas até 100 itens (ReportLab) | Backend | req-func-0001-requisitos-funcionais-canon.md RNF11 | Sim | Teste de geração PDF |
| C19 | CI/CD pipeline <5min (ruff + pytest --cov + build) | Infra | req-func-0001-requisitos-funcionais-canon.md RNF07 | Sim | GitHub Actions workflow verde |
| C20 | DoD assinado por reviewer + qa-sdet + gatekeeper + aprovação humana | Processo | constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon Art. 6.3 | Sim | Checklist de PR preenchido |

### 11.2 Gates de bloqueio (FAIL-CLOSED)

| Gate | Condição | Consequência de falha |
|------|----------|----------------------|
| G-Prod-01 | Qualquer item C01–C20 não atendido | Merge bloqueado; não entra em "Done" |
| G-Prod-02 | CI pipeline vermelho ou >5min | Não há deploy; correção obrigatória antes de novo push |
| G-Prod-03 | Cobertura <80% nos módulos tocados | PR não aprovado por qa-sdet |
| G-Prod-04 | Kill Switch invocado (qualquer vetor Art. 4.6) | Todo roteamento para; escala ao humano |
| G-Prod-05 | Bypass sem 3 pilares (force majeure + FOSS exit + CCB) | Recusa imediata; log de tentativa |

### 11.3 Matriz de conformidade por sprint

| Sprint | Itens aplicáveis | Gate de entrada | Gate de saída |
|--------|-----------------|-----------------|---------------|
| S1 (Setup, Docs, Auth) | C01–C06, C07, C09, C10, C11, C12, C13, C14, C15, C16, C19 | G0 (registry check) | C01–C06, C07, C09, C10, C11, C12, C13, C14, C15, C16, C19 |
| S2 (Listas, Catálogo) | C01–C08, C12, C13, C14, C17 | G-Prod-01 (S1 verde) | C01–C08, C12, C13, C14, C17 |
| S3 (Pré-filtro, Comparação) | C01–C04, C07, C12, C13, C14, C17, C18 | G-Prod-01 (S2 verde) | C01–C04, C07, C12, C13, C14, C17, C18 |
| S4 (Export, Perfil, Polish) | C01–C06, C12, C13, C14, C15, C16, C18 | G-Prod-01 (S3 verde) | C01–C06, C12, C13, C14, C15, C16, C18 |
| S5 (Buffer, QA, Demo) | C01–C20 todos | G-Prod-01 (S4 verde) | C01–C20; CI verde; DoD completo |

### 11.4 Checklist de aceitação para pré-produção

- [ ] Stack B documentada como ADR e alinhada em doc-readme-0001-readme-canon + board-roadmap-0001-roadmap-canon
- [ ] `docker compose up` sobe frontend + backend + MySQL sem config manual
- [ ] 8 tabelas criadas com schema PT-BR, FKs, CHECK, soft delete
- [ ] Seed executa em <10s e popula 11 cat + 10 forn + 50 prod + ~300 preços
- [ ] Endpoints auth (cadastro/login/logout) funcionam com bcrypt + JWT
- [ ] Rate limiting 6/15min ativo; sem token de recuperação em stdout
- [ ] CRUD de listas com transação ACID; FK de produto validada
- [ ] Motor de comparação flat com cache 5min e timeout 10s
- [ ] Endpoint PDF (ReportLab) <5s para 100 itens
- [ ] Testes unitários ≥80% cobertura; `pytest --cov` verde
- [ ] CI GitHub Actions <5min; ruff + pytest --cov + build
- [ ] LGPD: sem PII em seeds/fixtures/logs; dados sintéticos apenas
- [ ] Segurança: erros não expõem tracebacks; parameterized queries
- [ ] DoD checklist assinado por reviewer, qa-sdet, gatekeeper e humano

## 12. Peça 5 — Relatório consolidado final (tomada de decisão e handoff para produção)

**Artefato:** Consolidado de todas as rodadas (1 a 4).  
**Versão:** 1.1 (Rodada 5).  
**Data:** 09 de Novembro de 2026.  
**Status:** Pronto para decisão de handoff.

### 12.1 Resumo executivo

O COBECO é um projeto acadêmico de Laboratório de Engenharia de Software (FATEC Taquaritinga — ADS) com propósito bifurcado: (i) entrega de documentação em PDF (ABNT) já devida (prazo expirado 18/09/2026) e (ii) desenvolvimento de um MVP de comparação de preços entre fornecedores (prazo planejado 13/11/2026). O repositório está em fase docs-only; nenhum código foi implementado. Há dois planos de stack conflitantes, agora resolvidos em favor da **Stack B** (FastAPI + Pydantic + MySQL 8 InnoDB + pytest/ruff + ReportLab + Docker Compose + GitHub Actions), alinhada ao SSOT v3.2 (req-func-0001-requisitos-funcionais-canon, req-use-case-0001-casos-de-uso-canon, doc-arch-0001-camada-de-dados-canon).

### 12.2 Veredito de viabilidade

| Dimensão | Veredito | Justificativa |
|----------|----------|---------------|
| Técnica | **Condicional** | Arquitetura e requisitos bem definidos; stack B agora escolhida; mas zero código, zero CI, zero Docker, zero testes hoje. Prazo de 4 dias é insuficiente para MVP completo. |
| Negocial | **Crítico** | Prazo de documentação expirado (risco de reprovação). Prazo de software inviável sem corte de escopo. Responsáveis (PO, Tech Lead, Arquiteto) não nomeados. Nomes de integrantes ausentes na documentação. |
| Ambiental | **Adequado** | Hardware local 8700G/60GB compatível com FOSS-first, zero cloud, zero CUDA (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon Art. 1.2). |

### 12.3 Falhas críticas não resolvidas (bloqueantes de produção)

| ID | Falha | Status | Ação requerida |
|----|-------|--------|----------------|
| F01 | Stack duplo | RESOLVIDO (Stack B) | Arquivar plano A como ADR; alinhar doc-readme-0001-readme-canon e board-roadmap-0001-roadmap-canon |
| F06 | Prazo de software a 4 dias, sem código | ABERTO | Cortar escopo para MVP mínimo (auth básico + catálogo + comparação) OU adiar para próximo ciclo |
| F04 | PO, Tech Lead, Arquiteto não nomeados | ABERTO | Nomear responsáveis antes de qualquer spec ser assinada |
| F05 | Prazo de documentação expirado | ABERTO | Entregar PDF atrasado com justificativa ou redefinir prazo com professor |
| F12 | Nomes de integrantes ausentes | ABERTO | Incluir todos os 5 nomes na monografia/PDF e doc-readme-0001-readme-canon |
| F02 | DER sem sessão/refresh_tokens vs RF02 exige refresh 7d | ABERTO | Incluir tabela de sessão OU remover refresh de RF02 |
| F03 | RECOVERY_MODE=log expõe token | ABERTO | Remover ou proteger logs contra retenção de tokens |

### 12.4 Proposições de ajuste consolidadas (A1–A9)

| ID | Proposição | Prioridade | Status |
|----|------------|------------|--------|
| A1 | Decidir stack única (B) e arquivar plano A como ADR | P0 | Feito (Rodada 3) |
| A2 | Nomear PO, Tech Lead, Arquiteto | P1 | Pendente |
| A3 | Regularizar documentação atrasada | P1 | Pendente |
| A4 | Revisar DER: sessão/refresh_tokens vs RF02 | P1 | Pendente |
| A5 | Remover `RECOVERY_MODE=log` | P1 | Pendente |
| A6 | Redefinir escopo realista para 4 dias OU adiar | P0 | Pendente |
| A7 | Limpar `node_modules` do root | P2 | Pendente |
| A8 | Implementar testes, CI, Docker, OpenAPI conforme DoD | P1 | Durante desenvolvimento |
| A9 | Incluir nomes dos 5 integrantes na documentação | P1 | Pendente |

### 12.5 Plano de execução SDD/AI-Driven (ondas W0–W5)

Resumo das ondas (detalhe na seção 10):

| Wave | Foco | Criticidade para MVP mínimo |
|------|------|------------------------------|
| W0 | Setup e infra (Docker Compose) | Obrigatório |
| W1 | Schema DB + seed (8 tabelas PT-BR) | Obrigatório |
| W2 | Autenticação core (JWT, bcrypt, rate limit) | Obrigatório |
| W3 | Listas e catálogo (CRUD, autocomplete, categoria) | Desejável |
| W4 | Comparação flat + export PDF (ReportLab) | Desejável |
| W5 | QA, CI, cobertura ≥80%, demo | Obrigatório para entrega acadêmica |

### 12.6 Matriz de conformidade de produção (resumo)

20 itens de conformidade (C01–C20) distribuídos por 5 sprints, com 5 gates de bloqueio (FAIL-CLOSED). Detalhe na seção 11.

### 12.7 Decisão de handoff

**Recomendação do NEXUS-PRIME:** Não autorizar handoff para produção enquanto não estiverem resolvidos: (i) nomeação de responsáveis (A2), (ii) regularização da documentação atrasada (A3), (iii) corte de escopo realista ou adiamento (A6), (iv) correção de F02/F03 (DER e RECOVERY_MODE). Com esses itens resolvidos, iniciar W0–W2 imediatamente; W3–W5 dependem do tempo remanescente.

### 12.8 Próximos passos imediatos (próximas 48–72h)

1. Nomear PO, Tech Lead e Arquiteto (A2).
2. Criar ADR de stack B (`docs/decisoes/adr-stack-b.md`).
3. Atualizar doc-readme-0001-readme-canon.md e board-roadmap-0001-roadmap-canon.md para stack B.
4. Limpar `node_modules` do root (A7).
5. Escrever spec W0 (`.ai/specs/infra-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0.md`) e dispatchar via L0.
6. Entregar documentação PDF atrasada com justificativa (A3).

---

**FIM DO RELATÓRIO — Versão 1.1 / Rodada 5 (consolidado final)**

**Artefato SSOT:** `docs/relatorios/doc-critical-analysis-0001-analise-critica-v1.0.md`  
**Orquestrador:** NEXUS-PRIME ULTIMATE (L0)  
**Stack oficial:** B (FastAPI + MySQL 8 + ReportLab)



