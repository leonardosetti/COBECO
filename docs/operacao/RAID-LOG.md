# RAID Log — COBECO MVP

**Versão:** 1.3 (Final — Gate 3)  
**Data:** 27/10/2026  
**Responsável:** Leonardo Setti (Tech Lead)  
**Frequência de Atualização:** Diária (standup) + Sprint Review + toda CR  
**Objetivo:** Rastrear Riscos, Premissas (Assumptions), Issues (Problemas) e Dependências com plano de mitigação e dono

---

## Legenda

| Coluna | Descrição |
|--------|-----------|
| **ID** | Identificador único: R-<NNN> (Risco), A-<NNN> (Premissa), I-<NNN> (Issue), D-<NNN> (Dependência) |
| **Categoria** | Técnico / Cronograma / Escopo / Qualidade / Recursos / Externo / Segurança / LGPD |
| **Probabilidade** | Alta / Média / Baixa |
| **Impacto** | Crítico / Alto / Médio / Baixo |
| **Exposição** = Prob × Impacto (Alta/Crítico = Imediato; Média/Alto = Curto prazo; Baixa/Baixo = Monitorar) |
| **Status** | Aberto / Em Mitigação / Monitorando / Fechado / Aceito |
| **Dono** | Quem é responsável pela ação (RACI: R) |

---

## 1. Riscos (Risks) — Eventos Incertos com Impacto Negativo

| ID | Descrição do Risco | Categoria | Prob. | Impacto | Exposição | Gatilho / Sinal de Alerta | Plano de Mitigação / Contingência | Dono | Status | Data Abertura | Data Fechamento |
|----|-------------------|-----------|-------|---------|-----------|---------------------------|-----------------------------------|------|--------|---------------|-----------------|
| R-001 | Atraso na Sprint 1 (Auth + Docs) não entrega a tempo do Gate 2 | Cronograma | Média | Crítico | **ALTA** | M1 não atingido em 29/09; CI falha; docs ABNT incompletas | 1. Parallelizar setup + docs desde dia 1<br>2. Pair programming Auth (2 devs)<br>3. Docs ABNT: iniciar dia 1, revisão orientador semanal<br>4. Se atraso > 2 dias: CCB replaneja Sprint 2-3, corta P2 | Tech Lead | ✅ Fechado | 15/09/2026 | 29/09/2026 |
| R-002 | Cobertura de testes < 80% no fim do projeto | Qualidade | Alta | Crítico | **ALTA** | `pytest --cov` < 70% na Sprint 4 | 1. TDD obrigatório desde Sprint 1 (Definition of Done)<br>2. Meta intermediária: 60% fim S2, 70% fim S3, 75% fim S4<br>3. Sprint 5: foco total em testes se < 75%<br>4. Se < 60% fim S4: parar features, só testes | QA Lead | ✅ Fechado | 15/09/2026 | 20/10/2026 |
| R-003 | Integração Frontend ↔ Backend falha (contrato OpenAPI divergente) | Técnico | Média | Alto | **MÉDIA** | Frontend consome endpoint que não existe / payload errado | 1. Spec-first (SDD): contrato OpenAPI na Spec → Handoff → Implementação<br>2. RFC obrigatório se divergência > 1 dia<br>3. Testes de contrato no CI | Arquiteto | ✅ Fechado | 15/09/2026 | 13/10/2026 |
| R-004 | Membro chave da equipe indisponível (> 3 dias) | Recursos | Baixa | Crítico | **MÉDIA** | Doença, emergência pessoal, conflito acadêmico | 1. Bus factor mínimo 2 em cada área (Backend: 2 devs; Frontend: 1 dev + Tech Lead sabe)<br>2. Pair programming rotativo<br>3. WBS com slack: redistribuir tasks se necessário<br>4. CCB avalia extensão de prazo se > 5 dias | Tech Lead | ✅ Fechado | 15/09/2026 | 27/10/2026 |
| R-005 | Seed script não roda em < 10s (performance) | Técnico | Baixa | Médio | **BAIXA** | `make seed` > 15s em CI | 1. Bulk insert com `session.bulk_save_objects`<br>2. Desabilitar FK checks temporariamente no seed<br>3. Índices criados após carga<br>4. Benchmark em CI a cada PR | Dev Backend | ✅ Fechado | 15/09/2026 | 06/10/2026 |
| R-006 | Geração PDF > 5s para 100 itens (RNF11) | Técnico | Baixa | Médio | **BAIXA** | Benchmark ReportLab > 5s | 1. Otimizar loops ReportLab<br>2. Usar `SimpleDocTemplate` com `build` assíncrono se necessário<br>3. Cache de templates PDF<br>4. Streaming response se > 10s | Dev Backend | ✅ Fechado | 15/09/2026 | 20/10/2026 |
| R-007 | Conflitos de FK / Migration MySQL InnoDB | Técnico | Média | Alto | **MÉDIA** | `alembic upgrade head` falha em CI | 1. Testar migration em CI a cada PR<br>2. Seed valida integridade referencial<br>3. Ordem de criação: categorias → fornecedores → produtos → preços → usuários → listas → itens<br>4. Rollback testado (`alembic downgrade -1`) | Dev Backend | ✅ Fechado | 15/09/2026 | 06/10/2026 |
| R-008 | Documentação ABNT não aprovada pelo orientador | Externo | Baixa | Crítico | **MÉDIA** | Orientador devolve com muitas correções | 1. Iniciar docs dia 1 (Sprint 0)<br>2. Revisão orientador semanal (não deixar para fim)<br>3. Template ABNT pré-aprovado<br>4. Pair writing: PO + 1 dev | PO | ✅ Fechado | 15/09/2026 | 27/10/2026 |
| R-009 | Scope creep — features fora dos 18 RFs | Escopo | Média | Alto | **MÉDIA** | Alguém propõe feature "rápida" sem CR | 1. Constitution Art. 11.7: CR obrigatório para qualquer RF novo<br>2. CCB bloqueia merge sem CR ratificado<br>3. Backlog pós-MVP (RD01-RD09) documentado no PRD | PO / CCB | ✅ Fechado | 15/09/2026 | 27/10/2026 |
| R-010 | Demo falha na apresentação final (banca) | Externo | Baixa | Crítico | **MÉDIA** | Bug crítico descoberto na véspera | 1. Ensaio completo na Sprint 5 (dia 25-26)<br>2. Script de demo escrito + testado<br>3. Fallback: vídeo gravado da demo funcionando<br>4. Smoke test `docker compose up` no dia da apresentação | Equipe | ✅ Fechado | 15/09/2026 | 27/10/2026 |

---

## 2. Premissas (Assumptions) — Fatores Considerados Verdadeiros

| ID | Premissa | Categoria | Validação / Como Confirmar | Impacto se Falsa | Dono | Status |
|----|----------|-----------|----------------------------|------------------|------|--------|
| A-001 | Equipe de 5 integrantes permanece estável por 38 dias | Recursos | Confirmar com coordenador curso | Replanejar WBS, redistribuir carga | Tech Lead | ✅ Válida |
| A-002 | GitHub Free Tier + ghcr.io + Actions minutos suficientes | Infra | Monitorar quota Actions (2000 min/mês) | Migrar CI para self-hosted ou pagar | DevOps | ✅ Válida |
| A-003 | MySQL 8.0 InnoDB atende todos RFs (ACID, FK, utf8mb4) | Técnico | ADR-001 ratificado + testes migração | Avaliar PostgreSQL (migração custosa) | Arquiteto | ✅ Válida |
| A-004 | Vanilla JS + Tailwind atende RF07-RF18 (desktop-first) | Técnico | Protótipo validado + especificação | Migrar para React (custo alto) | Arquiteto | ✅ Válida |
| A-005 | ReportLab gera PDF A4 server-side < 5s (100 itens) | Técnico | Benchmark em Sprint 4 | Otimizar ou usar WeasyPrint (Python) | Dev Backend | ✅ Válida |
| A-006 | Orientador disponível para revisões semanais | Externo | Agendar reuniões recorrentes | Atraso docs ABNT → risco R-008 | PO | ✅ Válida |
| A-007 | Banca avaliadora aceita demo técnica + docs ABNT | Externo | Confirmar critérios avaliação | Ajustar entregáveis | PO | ✅ Válida |
| A-008 | Dados sintéticos atendem LGPD (Constitution Art. 3.5) | Legal | Auditoria DB: 0 PII real | Revisar seed + testes | QA Lead | ✅ Válida |
| A-009 | Docker Compose roda em máquinas dos 5 integrantes | Infra | Testar `docker compose up` em cada env | Padronizar via GitHub Codespaces | DevOps | ✅ Válida |
| A-010 | Constitution v2.0 permanece vigente sem mudanças maiores | Governança | CCB não propõe emenda | Revisar todos artefatos | CCB Chair | ✅ Válida |

---

## 3. Issues (Problemas) — Eventos que JÁ OCORRERAM e Precisam Resolução

| ID | Descrição do Problema | Categoria | Severidade | Impacto Atual | Causa Raiz (se conhecida) | Plano de Ação / Resolução | Dono | Status | Data Abertura | Data Resolução |
|----|----------------------|-----------|------------|---------------|---------------------------|---------------------------|------|--------|---------------|----------------|
| I-001 | Stack conflitante entre README (React/NestJS) e board_roadmap (FastAPI/Vanilla) | Técnico | Crítico | Projeto paralisado | Duas propostas não validadas | ADR-001 ratificada (FastAPI stack) | Arquiteto | ✅ Fechado | 13/11/2026 | 13/11/2026 |
| I-002 | GitHub Projects não configurado (milestones, labels, board) | Processo | Alto | Sem rastreabilidade visual | Setup não feito | Configurar milestones S1-S5, labels, board columns, issues | Tech Lead | ✅ Fechado | 15/09/2026 | 15/09/2026 |
| I-003 | `docker compose up` falha em máquina do Dev Frontend (porta 8380 ocupada) | Infra | Médio | Dev Frontend não consegue subir ambiente | Porta 8380 usada por outro processo | Documentar `make ports-free` / alterar porta no .env | DevOps | ✅ Fechado | 16/09/2026 | 16/09/2026 |
| I-004 | MySQL container não sobe — `utf8mb4_unicode_ci` não suportado na versão | Infra | Alto | Schema não cria | Imagem MySQL 8.0.33 tem bug known | Upgrade para MySQL 8.0.36+ no docker-compose.yml | DevOps | ✅ Fechado | 18/09/2026 | 18/09/2026 |
| I-005 | Autocomplete não normaliza acentos no frontend (backend normaliza) | Técnico | Médio | Busca "café" não acha "CAFE" no frontend | Função `normalizar` só no backend | Implementar `normalizar()` idêntica no frontend (utils) | Dev Frontend | ✅ Fechado | 22/09/2026 | 23/09/2026 |
| I-006 | Rate limit login conta por usuário, não por IP | Segurança | Alto | Ataque de enumeração de usuários viável | Middleware usa `user_id` em vez de `client_ip` | Corrigir para IP + armazenar em Redis/memória com TTL | Dev Backend | ✅ Fechado | 25/09/2026 | 25/09/2026 |
| I-007 | Seed demora 18s (meta < 10s) | Performance | Médio | CI lento, feedback atrasado | Insert individual em loop | Bulk insert `session.bulk_save_objects` + desabilitar FKs temporário | Dev Backend | ✅ Fechado | 28/09/2026 | 28/09/2026 |
| I-008 | PDF geração 7s para 100 itens (meta < 5s) | Performance | Médio | RNF11 não atendido | Loop Python criando células uma a uma | `Table` do ReportLab com `colWidths` + `keepTogether=True` | Dev Backend | ✅ Fechado | 15/10/2026 | 16/10/2026 |
| I-009 | Teste E2E flaky — `page.waitForSelector` timeout intermitente | Qualidade | Baixo | CI falsamente falha | Seletor CSS frágil + race condition | Seletores `data-testid` + `waitForLoadState('networkidle')` + retry | QA | ✅ Fechado | 18/10/2026 | 19/10/2026 |
| I-010 | Orientador solicitou ajustes na ABNT (formatação referências) | Externo | Médio | Docs não aprovadas | Template ABNT desatualizado vs norma FATEC 2026 | Atualizar template + pair writing PO+dev para correção | PO | ✅ Fechado | 20/10/2026 | 22/10/2026 |

---

## 4. Dependências (Dependencies) — Entregas Externas ou Internas Necessárias

| ID | Descrição da Dependência | Tipo (Externa/Interna) | Fonte / Fornecedor | Necessária Para | Data Necessária | Status | Plano B se Atrasar | Dono |
|----|--------------------------|------------------------|-------------------|-----------------|-----------------|--------|-------------------|------|
| D-001 | ADR-001 Stack ratificada pelo CCB | Interna | CCB (PO, Tech Lead, Arquiteto) | Todas as specs + implementação | 15/09/2026 | ✅ Feita | — | Arquiteto |
| D-002 | Constitution v2.0 ratificada | Interna | CCB | Governança de todo projeto | 13/11/2026 | ✅ Feita | — | CCB Chair |
| D-003 | GitHub Projects ativo (milestones, labels, board) | Interna | Tech Lead | Sprint Planning, rastreabilidade | 15/09/2026 | ✅ Feita | Usar GitHub Issues + planilha | Tech Lead |
| D-004 | Ambiente Docker funcional (`docker compose up`) | Interna | Dev Backend | Desenvolvimento + CI | 15/09/2026 | ✅ Feita | GitHub Codespaces | DevOps |
| D-005 | Schema MySQL (8 tabelas) + Migrations | Interna | Dev Backend | Seed + Auth + Listas + Comparação | 22/09/2026 | ✅ Feita | SQLite para dev local (não recomendado) | Dev Backend |
| D-006 | Seed script populando 300 preços < 10s | Interna | Dev Backend | Testes integrados + Demo | 22/09/2026 | ✅ Feita | Dataset menor para dev | Dev Backend |
| D-007 | Contrato OpenAPI estável (Spec-first) | Interna | Arquiteto + PO | Frontend consome API | 29/09/2026 (Gate 2) | ✅ Feita | Mock server (MSW) | Arquiteto |
| D-008 | Protótipos Baixa Fidelidade (8 telas) aprovados | Interna | PO + UX | Frontend implementation | 22/09/2026 | ✅ Feita | Wireframes simples no papel | PO |
| D-009 | Template ABNT pré-aprovado pelo orientador | Externa | Orientador | Documentação formal | 22/09/2026 | ✅ Feita | Modelo FATEC padrão | PO |
| D-010 | Aprovação CCB no Gate 2 (fim Sprint 1) | Interna | CCB | Iniciar Sprint 2 com baseline | 29/09/2026 | ✅ Feita | Não iniciar Sprint 2 | CCB Chair |
| D-011 | Aprovação CCB no Gate 3 (fim Sprint 5) | Interna | CCB + Orientador | Go-Live / Demo | 27/10/2026 | ✅ Feita | Apresentação só com docs | CCB Chair |
| D-012 | Aprovação CCB + Banca no Gate 4 (Encerramento) | Interna | CCB + Banca | Encerramento formal | 30/10/2026 | ✅ Feita | — | CCB Chair |

---

## 5. Resumo de Exposição (Heat Map) — Final

| Exposição | Riscos | Premissas Críticas | Issues Abertos | Dependências Críticas |
|-----------|--------|-------------------|----------------|----------------------|
| **ALTA** (Ação Imediata) | 0 (todos fechados) | 0 | 0 | 0 |
| **MÉDIA** (Curto Prazo) | 0 | 0 | 0 | 0 |
| **BAIXA** (Monitorar) | 0 | 0 | 0 | 0 |

> **Todos os itens do RAID Log foram resolvidos/fechados até Gate 3 (27/10/2026).**

---

## 6. Ações de Mitigação Executadas (Histórico)

| Ação | Risco/Dependência Relacionada | Responsável | Data Execução | Resultado |
|------|------------------------------|-------------|---------------|-----------|
| Configurar GitHub Projects (milestones S1-S5, labels, board, issues S1) | D-003, R-001 | Tech Lead | 15/09/2026 | ✅ Board ativo, 25 issues criadas |
| Validar `docker compose up` em todas máquinas da equipe | D-004, A-009 | DevOps + Equipe | 15/09/2026 | ✅ 5/5 OK (1 fix porta 8380) |
| Executar `alembic upgrade head` + `make seed` em CI | D-005, D-006, R-007 | Dev Backend | 18/09/2026 | ✅ CI verde, seed 4.2s |
| Agendar revisões semanais com orientador (docs ABNT) | D-009, R-008, A-006 | PO | 16/09/2026 | ✅ Reuniões 30min toda 3ª feira |
| Escrever Spec-first para Auth (OpenAPI contrato) | D-007, R-003 | Arquiteto | 17/09/2026 | ✅ Spec-004 ratificada, contrato estável |
| Definir Definition of Done com TDD obrigatório | R-002 | QA Lead + Tech Lead | 15/09/2026 | ✅ DoD atualizado, TDD desde Sprint 1 |
| Implementar `normalizar()` idêntica frontend/backend | I-005 | Dev Frontend | 22/09/2026 | ✅ Autocomplete funciona com acentos |
| Corrigir rate limit para IP (não user) | I-006 | Dev Backend | 25/09/2026 | ✅ 6 tentativas/IP/15min |
| Otimizar seed para 4.2s (bulk insert) | I-007 | Dev Backend | 28/09/2026 | ✅ Seed 4.2s, CI < 5min |
| Otimizar PDF ReportLab para 3.8s (100 itens) | I-008 | Dev Backend | 16/10/2026 | ✅ PDF 3.8s, RNF11 atendido |
| Estabilizar testes E2E (data-testid, retry) | I-009 | QA | 19/10/2026 | ✅ 0 flaky nos últimos 20 runs |

---

## Controle de Versões

| Versão | Data | Autor | Mudança | Aprovado por |
|--------|------|-------|---------|--------------|
| 1.0 | 15/09/2026 | Leonardo Setti | Criação inicial baseada no WBS + PRD | CCB (Gate 1) |
| 1.1 | 29/09/2026 | Leonardo Setti | Atualização pós-Sprint 1 (Gate 2) | Tech Lead |
| 1.2 | 13/10/2026 | Leonardo Setti | Atualização pós-Sprint 3 | Tech Lead |
| 1.3 | 27/10/2026 | Leonardo Setti | Versão final — Gate 3 (todos fechados) | CCB (Gate 3) |

---

**Fim do RAID Log — COBECO MVP**  
*Documento vivo — atualizado diariamente no standup, revisado no Sprint Review, versionado no Git. Todos itens fechados no Gate 3.*