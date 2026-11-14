# RAID Log — <NOME DO PROJETO>

**Versão:** 1.0  
**Data:** DD/MM/AAAA  
**Responsável:** Tech Lead  
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
| R-001 | Atraso na Sprint 1 (Auth + Docs) não entrega a tempo do Gate 2 | Cronograma | Média | Crítico | **ALTA** | M1 não atingido em 29/09; CI falha; docs ABNT incompletas | 1. Parallelizar setup + docs desde dia 1<br>2. Pair programming Auth (2 devs)<br>3. Docs ABNT: iniciar dia 1, revisão orientador semanal<br>4. Se atraso > 2 dias: CCB replaneja Sprint 2-3, corta P2 | Tech Lead | ☐ Aberto | DD/MM/AAAA | |
| R-002 | Cobertura de testes < 80% no fim do projeto | Qualidade | Alta | Crítico | **ALTA** | `pytest --cov` < 70% na Sprint 4 | 1. TDD obrigatório desde Sprint 1 (Definition of Done)<br>2. Meta intermediária: 60% fim S2, 70% fim S3, 75% fim S4<br>3. Sprint 5: foco total em testes se < 75%<br>4. Se < 60% fim S4: parar features, só testes | QA Lead | ☐ Aberto | DD/MM/AAAA | |
| R-003 | Integração Frontend ↔ Backend falha (contrato OpenAPI divergente) | Técnico | Média | Alto | **MÉDIA** | Frontend consome endpoint que não existe / payload errado | 1. Spec-first (SDD): contrato OpenAPI na Spec → Handoff → Implementação<br>2. RFC obrigatório se divergência > 1 dia<br>3. Testes de contrato (Pact ou similar) no CI | Arquiteto | ☐ Aberto | DD/MM/AAAA | |
| R-004 | Membro chave da equipe indisponível (> 3 dias) | Recursos | Baixa | Crítico | **MÉDIA** | Doença, emergência pessoal, conflito acadêmico | 1. Bus factor mínimo 2 em cada área (Backend: 2 devs; Frontend: 1 dev + Tech Lead sabe)<br>2. Pair programming rotativo<br>3. WBS com slack: redistribuir tasks se necessário<br>4. CCB avalia extensão de prazo se > 5 dias | Tech Lead | ☐ Aberto | DD/MM/AAAA | |
| R-005 | Seed script não roda em < 10s (performance) | Técnico | Baixa | Médio | **BAIXA** | `make seed` > 15s em CI | 1. Bulk insert com `session.bulk_save_objects`<br>2. Desabilitar FK checks temporariamente no seed<br>3. Índices criados após carga<br>4. Benchmark em CI a cada PR | Dev Backend | ☐ Aberto | DD/MM/AAAA | |
| R-006 | Geração PDF > 5s para 100 itens (RNF11) | Técnico | Baixa | Médio | **BAIXA** | Benchmark ReportLab > 5s | 1. Otimizar loops ReportLab<br>2. Usar `SimpleDocTemplate` com `build` assíncrono se necessário<br>3. Cache de templates PDF<br>4. Streaming response se > 10s | Dev Backend | ☐ Aberto | DD/MM/AAAA | |
| R-007 | Conflitos de FK / Migration MySQL InnoDB | Técnico | Média | Alto | **MÉDIA** | `alembic upgrade head` falha em CI | 1. Testar migration em CI a cada PR<br>2. Seed valida integridade referencial<br>3. Ordem de criação: categorias → fornecedores → produtos → preços → usuários → listas → itens<br>4. Rollback testado (`alembic downgrade -1`) | Dev Backend | ☐ Aberto | DD/MM/AAAA | |
| R-008 | Documentação ABNT não aprovada pelo orientador | Externo | Baixa | Crítico | **MÉDIA** | Orientador devolve com muitas correções | 1. Iniciar docs dia 1 (Sprint 0)<br>2. Revisão orientador semanal (não deixar para fim)<br>3. Template ABNT pré-aprovado<br>4. Pair writing: PO + 1 dev | PO | ☐ Aberto | DD/MM/AAAA | |
| R-009 | Scope creep — features fora dos 18 RFs | Escopo | Média | Alto | **MÉDIA** | Alguém propõe feature "rápida" sem CR | 1. Constitution Art. 11.7: CR obrigatório para qualquer RF novo<br>2. CCB bloqueia merge sem CR ratificado<br>3. Backlog pós-MVP (RD01-RD09) documentado no PRD | PO / CCB | ☐ Aberto | DD/MM/AAAA | |
| R-010 | Demo falha na apresentação final (banca) | Externo | Baixa | Crítico | **MÉDIA** | Bug crítico descoberto na véspera | 1. Ensaio completo na Sprint 5 (dia 25-26)<br>2. Script de demo escrito + testado<br>3. Fallback: vídeo gravado da demo funcionando<br>4. Smoke test `docker compose up` no dia da apresentação | Equipe | ☐ Aberto | DD/MM/AAAA | |

---

## 2. Premissas (Assumptions) — Fatores Considerados Verdadeiros

| ID | Premissa | Categoria | Validação / Como Confirmar | Impacto se Falsa | Dono | Status |
|----|----------|-----------|----------------------------|------------------|------|--------|
| A-001 | Equipe de 5 integrantes permanece estável por 38 dias | Recursos | Confirmar com coordenador curso | Replanejar WBS, redistribuir carga | Tech Lead | ☐ Válida |
| A-002 | GitHub Free Tier + ghcr.io + Actions minutos suficientes | Infra | Monitorar quota Actions (2000 min/mês) | Migrar CI para self-hosted ou pagar | DevOps | ☐ Válida |
| A-003 | MySQL 8.0 InnoDB atende todos RFs (ACID, FK, utf8mb4) | Técnico | ADR-001 ratificado + testes migração | Avaliar PostgreSQL (migração custosa) | Arquiteto | ☐ Válida |
| A-004 | Vanilla JS + Tailwind atende RF07-RF18 (desktop-first) | Técnico | Protótipo validado + especificação | Migrar para React (custo alto) | Arquiteto | ☐ Válida |
| A-005 | ReportLab gera PDF A4 server-side < 5s (100 itens) | Técnico | Benchmark em Sprint 4 | Otimizar ou usar WeasyPrint (Python) | Dev Backend | ☐ Válida |
| A-006 | Orientador disponível para revisões semanais | Externo | Agendar reuniões recorrentes | Atraso docs ABNT → risco R-008 | PO | ☐ Válida |
| A-007 | Banca avaliadora aceita demo técnica + docs ABNT | Externo | Confirmar critérios avaliação | Ajustar entregáveis | PO | ☐ Válida |
| A-008 | Dados sintéticos atendem LGPD (Constitution Art. 3.5) | Legal | Auditoria DB: 0 PII real | Revisar seed + testes | QA Lead | ☐ Válida |
| A-009 | Docker Compose roda em máquinas dos 5 integrantes | Infra | Testar `docker compose up` em cada env | Padronizar via GitHub Codespaces | DevOps | ☐ Válida |
| A-010 | Constitution v2.0 permanece vigente sem mudanças maiores | Governança | CCB não propõe emenda | Revisar todos artefatos | CCB Chair | ☐ Válida |

---

## 3. Issues (Problemas) — Eventos que JÁ OCORRERAM e Precisam Resolução

| ID | Descrição do Problema | Categoria | Severidade | Impacto Atual | Causa Raiz (se conhecida) | Plano de Ação / Resolução | Dono | Status | Data Abertura | Data Resolução |
|----|----------------------|-----------|------------|---------------|---------------------------|---------------------------|------|--------|---------------|----------------|
| I-001 | *Exemplo:* Stack conflitante entre doc-readme-0001-readme-canon (React/NestJS) e board-roadmap-0001-roadmap-canon (FastAPI/Vanilla) | Técnico | Crítico | Projeto paralisado | Duas propostas não validadas | ADR-001 ratificada (FastAPI stack) | Arquiteto | ☐ Fechado | 13/11/2026 | 13/11/2026 |
| I-002 | *Exemplo:* GitHub Projects não configurado (milestones, labels, board) | Processo | Alto | Sem rastreabilidade visual | Setup não feito | Configurar milestones S1-S5, labels, board columns, issues | Tech Lead | ☐ Aberto | DD/MM/AAAA | |

---

## 4. Dependências (Dependencies) — Entregas Externas ou Internas Necessárias

| ID | Descrição da Dependência | Tipo (Externa/Interna) | Fonte / Fornecedor | Necessária Para | Data Necessária | Status | Plano B se Atrasar | Dono |
|----|--------------------------|------------------------|-------------------|-----------------|-----------------|--------|-------------------|------|
| D-001 | ADR-001 Stack ratificada pelo CCB | Interna | CCB (PO, Tech Lead, Arquiteto) | Todas as specs + implementação | 15/09/2026 | ✅ Feita | — | Arquiteto |
| D-002 | Constitution v2.0 ratificada | Interna | CCB | Governança de todo projeto | 13/11/2026 | ✅ Feita | — | CCB Chair |
| D-003 | GitHub Projects ativo (milestones, labels, board) | Interna | Tech Lead | Sprint Planning, rastreabilidade | 15/09/2026 | ☐ Pendente | Usar GitHub Issues + planilha | Tech Lead |
| D-004 | Ambiente Docker funcional (`docker compose up`) | Interna | Dev Backend | Desenvolvimento + CI | 15/09/2026 | ☐ Pendente | GitHub Codespaces | DevOps |
| D-005 | Schema MySQL (8 tabelas) + Migrations | Interna | Dev Backend | Seed + Auth + Listas + Comparação | 22/09/2026 | ☐ Pendente | SQLite para dev local (não recomendado) | Dev Backend |
| D-006 | Seed script populando 300 preços < 10s | Interna | Dev Backend | Testes integrados + Demo | 22/09/2026 | ☐ Pendente | Dataset menor para dev | Dev Backend |
| D-007 | Contrato OpenAPI estável (Spec-first) | Interna | Arquiteto + PO | Frontend consome API | 29/09/2026 (Gate 2) | ☐ Pendente | Mock server (MSW) | Arquiteto |
| D-008 | Protótipos Baixa Fidelidade (8 telas) aprovados | Interna | PO + UX (se houver) | Frontend implementation | 22/09/2026 | ☐ Pendente | Wireframes simples no papel | PO |
| D-009 | Template ABNT pré-aprovado pelo orientador | Externa | Orientador | Documentação formal | 22/09/2026 | ☐ Pendente | Modelo FATEC padrão | PO |
| D-010 | Aprovação CCB no Gate 2 (fim Sprint 1) | Interna | CCB | Iniciar Sprint 2 com baseline | 29/09/2026 | ☐ Pendente | Não iniciar Sprint 2 | CCB Chair |

---

## 5. Resumo de Exposição (Heat Map)

| Exposição | Riscos | Premissas Críticas | Issues Abertos | Dependências Críticas |
|-----------|--------|-------------------|----------------|----------------------|
| **ALTA** (Ação Imediata) | R-001, R-002 | A-001, A-003 | I-002 | D-003, D-004, D-005 |
| **MÉDIA** (Curto Prazo) | R-003, R-004, R-007 | A-004, A-006 | — | D-006, D-007, D-010 |
| **BAIXA** (Monitorar) | R-005, R-006, R-008, R-009, R-010 | A-002, A-005, A-007, A-008, A-009, A-010 | I-001 (fechado) | D-008, D-009 |

---

## 6. Ações de Mitigação Prioritárias (Próximos 7 Dias)

| Ação | Risco/Dependência Relacionada | Responsável | Prazo | Status |
|------|------------------------------|-------------|-------|--------|
| Configurar GitHub Projects (milestones, labels, board, issues S1) | D-003, R-001 | Tech Lead | Hoje | ☐ |
| Validar `docker compose up` em todas máquinas da equipe | D-004, A-009 | DevOps + Equipe | Hoje | ☐ |
| Executar `alembic upgrade head` + `make seed` em CI | D-005, D-006, R-007 | Dev Backend | 2 dias | ☐ |
| Agendar revisões semanais com orientador (docs ABNT) | D-009, R-008, A-006 | PO | 3 dias | ☐ |
| Escrever Spec-first para Auth (OpenAPI contrato) | D-007, R-003 | Arquiteto | 3 dias | ☐ |
| Definir Definition of Done com TDD obrigatório | R-002 | QA Lead + Tech Lead | 1 dia | ☐ |

---

## Controle de Versões

| Versão | Data | Autor | Mudança | Aprovado por |
|--------|------|-------|---------|--------------|
| 1.0 | DD/MM/AAAA | Tech Lead | Criação inicial baseada no WBS + PRD | CCB (Gate 1) |
| 1.1 | DD/MM/AAAA | Tech Lead | Atualização pós-Sprint 1 | Tech Lead |

---

**Fim do RAID Log**  
*Documento vivo — atualizado diariamente no standup, revisado no Sprint Review, versionado no Git.*