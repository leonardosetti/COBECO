# Post-Mortem (Blameless) — COBECO MVP

**Documento:** Análise Pós-Mortem Sem Culpa  
**Versão:** 1.0  
**Data:** 27/10/2026  
**Autor:** Leonardo Setti (Tech Lead)  
**Participantes:** Leonardo Setti (PO/TL), Fabrício Cabral (Back1), Nicholas Anthony (Back2/Arq), Eduardo Passarelli (Front), Nicolas Mallouk (QA)  
**Facilitador:** Leonardo Setti  
**Classificação:** Interno — Blameless (foco em processo, não pessoas)  
**Evento Analisado:** Projeto completo (15/09/2026 a 30/10/2026) — Entrega MVP v0.1.0

---

## 1. Resumo do Evento

**Projeto:** COBECO MVP — Comparador de Preços de Compras  
**Período:** 38 dias úteis (15/09 a 30/10/2026)  
**Equipe:** 5 integrantes (1 PO/TL, 2 Backend, 1 Frontend, 1 QA/Back)  
**Resultado:** ✅ **SUCESSO** — MVP entregue no prazo, qualidade ≥80%, docs ABNT aprovadas, demo funcional

> **Objetivo do Post-Mortem:** Identificar causas raiz dos desvios (riscos que se materializaram, issues), extrair lições de processo e propor melhorias sistêmicas — **sem atribuição de culpa a indivíduos**.

---

## 2. Linha do Tempo dos Eventos Principais

| Data | Evento | Impacto | Ação Tomada |
|------|--------|---------|-------------|
| 13/11/2025 | Constitution v2.0 ratificada | Base governança | CCB assina |
| 15/09/2026 | Kick-off + Sprint 0 inicia | Início oficial | Charter, RACI, ADR-001, Docker |
| 15/09 | Stack conflitante descoberta (I-001) | Risco crítico | ADR-001 ratificada dia 13/11 (antecipado) |
| 16/09 | Porta 8380 ocupada (I-003) | Bloqueio dev | Documentado `make ports-free` |
| 18/09 | MySQL utf8mb4 bug (I-004) | Schema não cria | Upgrade 8.0.36 |
| 22/09 | Sprint 1 inicia | Auth + Docs | Pair programming Auth |
| 23/09 | Autocomplete acentos (I-005) | Busca falha | `normalizar()` idêntica client/server |
| 25/09 | Rate limit por user (I-006) | Segurança | Corrigido para IP |
| 28/09 | Seed 18s (I-007) | CI lento | Bulk insert → 4.2s |
| 29/09 | **Gate 2** — PRD + US + C4 + RAID + Test Plan aprovados | Marco | CCB aprova Sprint 2 |
| 15/10 | PDF 7s (I-008) | RNF11 falha | ReportLab Table → 3.8s |
| 18/10 | E2E flaky (I-009) | CI instável | `data-testid` + retry |
| 20/10 | ABNT ajustes (I-010) | Docs rejeitadas | Template atualizado + pair writing |
| 27/10 | **Gate 3** — Cobertura 83% + Runbooks + Release + Demo | Marco | CCB + Orientador aprovam Go-Live |
| 30/10 | **Gate 4** — Apresentação + Encerramento | Final | Banca nota 9.0 |

---

## 3. Análise de Causa Raiz (5 Porquês) — Principais Desvios

### 3.1 Desvio: Stack Conflitante (I-001) — Resolvido Antes do Início
| Porquê | Resposta |
|--------|----------|
| 1. Por que havia duas stacks? | README (React/NestJS/PostgreSQL) vs board_roadmap (FastAPI/MySQL/Vanilla JS) |
| 2. Por que não foi decidido antes? | Duas propostas paralelas sem validação CCB |
| 3. Por que não houve validação? | Processo ADR não existia ainda (Constitution v2.0 ratificada 13/11) |
| 4. Por que Constitution não existia antes? | Projeto iniciado sem governança formal |
| 5. **Causa Raiz** | **Ausência de governança (Charter + ADR) no Sprint 0** |

**Ação Sistêmica:** Sprint 0 obrigatório com Charter, RACI, ADR-001 **antes** de qualquer código.

---

### 3.2 Desvio: Seed > 10s (I-007) — Meta RNF08
| Porquê | Resposta |
|--------|----------|
| 1. Por que seed demorava 18s? | Insert individual em loop Python (`session.add()` + `commit()` por registro) |
| 2. Por que não usou bulk insert? | Desenvolvedor não conhecia `session.bulk_save_objects()` |
| 3. Por que não houve code review de performance? | PR focou em funcionalidade, não performance |
| 4. Por que não havia benchmark no CI? | Seed não testada em CI (apenas local) |
| 5. **Causa Raiz** | **Falta de benchmark automatizado + code review de performance no Definition of Done** |

**Ação Sistêmica:** `make seed` no CI com threshold < 10s + code review checklist inclui performance.

---

### 3.3 Desvio: PDF > 5s (I-008) — Meta RNF11
| Porquê | Resposta |
|--------|----------|
| 1. Por que PDF demorava 7s? | Loop Python criando células uma a uma (`canvas.drawString`) |
| 2. Por que não usou `Table` do ReportLab? | Desconhecimento da API `Table`/`SimpleDocTemplate` |
| 3. Por que não houve spike técnico? | Estimativa baseada em "PDF simples" sem validação |
| 4. Por que estimativa não foi validada? | Spike não feito para tarefas > 3 SP |
| 5. **Causa Raiz** | **Ausência de spike técnico obrigatório para tarefas desconhecidas/estimadas > 3 SP** |

**Ação Sistêmica:** Planning Poker + spike obrigatório para tarefas > 3 SP ou tecnologia nova.

---

### 3.4 Desvio: Testes E2E Flaky (I-009)
| Porquê | Resposta |
|--------|----------|
| 1. Por que testes falhavam intermitentemente? | Seletores CSS baseados em classes Tailwind (mudam com build) + race condition |
| 2. Por que não usou `data-testid`? | Padrão não definido no início do projeto |
| 3. Por que não havia retry nativo? | Configuração Playwright padrão sem `retries` |
| 4. Por que não foi pego em code review? | Testes E2E revisados apenas por QA, não por dev |
| 5. **Causa Raiz** | **Ausência de padrões de teste E2E (data-testid, retry, waitForLoadState) no Definition of Done** |

**Ação Sistêmica:** DoD inclui: `data-testid` obrigatório, `retries: 2`, `waitForLoadState('networkidle')`, code review duplo (dev + QA).

---

### 3.5 Desvio: Docs ABNT Ajustes (I-010)
| Porquê | Resposta |
|--------|----------|
| 1. Por que orientador pediu ajustes? | Template ABNT desatualizado vs norma FATEC 2026 (referências, numeração) |
| 2. Por que template estava desatualizado? | Copiado de ano anterior sem validação com orientador |
| 3. Por que não validou antes? | Docs ABNT iniciadas Sprint 1 (tarde), revisão só no fim |
| 4. Por que iniciaram tarde? | Foco em código Sprint 1, docs "depois" |
| 5. **Causa Raiz** | **Docs ABNT não priorizadas no Sprint 0 + pair writing não definido** |

**Ação Sistêmica:** Docs ABNT iniciam dia 1 (Sprint 0), pair writing PO+dev, revisão orientador semanal obrigatória.

---

## 4. O que Funcionou Bem (Keep Doing)

| Prática | Evidência de Sucesso | Por que Funcionou |
|---------|---------------------|-------------------|
| **Spec-first (SDD) + Handoff** | 0 retrabalho em integração Front↔Back; contrato OpenAPI estável | Clareza total antes de codar; Handoff parser → L0 dispatch |
| **ADR-001 no Sprint 0** | Stack definida dia 1; 0 thrashing técnico | Decisão arquitetural explícita + CCB ratifica |
| **Pair Programming Auth** | 2 devs no crítico path; 0 bugs críticos em Auth | Conhecimento compartilhado; revisão em tempo real |
| **GitHub Projects + Milestones** | Visibilidade total; standups em 10 min | Kanban visual + issues vinculadas a milestones |
| **Constitution v2.0 como Lei** | Decisões rápidas; CCB efetivo; 0 bikeshedding | Autoridade clara; "não negocieável" |
| **TDD desde Sprint 1** | Cobertura 83% final (meta 80%); 0 corrida final | Testes escritos antes do código; DoD exige |
| **Seed Determinístico 4.2s** | CI rápido; dev env confiável; testes determinísticos | Bulk insert + índices pós-carga; script versionado |
| **Runbooks Testados** | Deploy/rollback demo sem sustos | Game Day Sprint 5; procedimentos validados |
| **Mermaid C4 Diagrams** | Docs-as-Code; renderizam no GitHub; 0 ferramenta externa | Versionados; diff no PR; acessíveis |
| **RAID Log Ativo** | 10 riscos, 10 issues, todos fechados | Atualização diária standup; revisão Sprint Review |

---

## 5. O que Melhorar (Action Items)

| # | Melhoria | Ação Concreta | Responsável | Prazo | Métrica Sucesso |
|---|----------|---------------|-------------|-------|-----------------|
| 1 | **Bus Factor Frontend = 1** | Pair programming rotativo (Front+Back1, Front+Back2, Front+QA) a cada Sprint | TL | Próximo projeto | 2 devs sabem Frontend |
| 2 | **Docs ABNT no Sprint 0** | Iniciar dia 1; pair writing PO+dev; revisão orientador semanal 15min | PO | Próximo projeto | 0 ajustes finais |
| 3 | **Automatizar RAID Log** | Script `gh issue list --label risk,issue,dependency` → markdown diário | DevOps | Próximo projeto | 0 atualização manual |
| 4 | **Padrões E2E Obrigatórios** | DoD: `data-testid`, `retries: 2`, `waitForLoadState('networkidle')`, code review duplo | QA + TL | Próximo projeto | 0 flaky |
| 4 | **Spike Obrigatório > 3 SP** | Planning Poker + spike técnico para tarefas > 3 SP ou tech nova | TL + Equipe | Próximo projeto | 0 surpresas performance |
| 6 | **Benchmark Automatizado** | `make seed` + `make pdf-bench` no CI com thresholds (<10s, <5s) | DevOps | Próximo projeto | CI falha se > threshold |
| 7 | **Game Day por Sprint** | Testar runbook rollback, restore, incident response a cada 2 semanas | DevOps | Próximo projeto | 0 incidentes deploy |
| 8 | **Planning Poker Calibrado** | Referência histórica (SP vs horas reais) para calibrar estimativas | TL | Próximo projeto | Variância < 20% |

---

## 6. Métricas Finais do Projeto

| Métrica | Planejado | Realizado | Status |
|---------|-----------|-----------|--------|
| Duração | 38 dias | 38 dias | ✅ |
| RFs Entregues | 18 | 18 | ✅ |
| Cobertura Testes | ≥ 80% | 83% | ✅ |
| Bugs Críticos Produção | 0 | 0 | ✅ |
| Deploy Frequency | 1/sprint | 5 | ✅ |
| Lead Time (PR→Deploy) | < 2 dias | 1.2 dias | ✅ |
| MTTR | < 1h | 15 min | ✅ |
| Change Failure Rate | < 10% | 0% | ✅ |
| Docs ABNT Nota | ≥ 8.0 | 9.2 | ✅ |
| Banca Nota | ≥ 8.0 | 9.0 | ✅ |

---

## 7. Aprovação e Arquivamento

| Papel | Nome | Assinatura | Data |
|-------|------|------------|------|
| **Tech Lead / Facilitador** | Leonardo Setti | _______________ | 27/10/2026 |
| **Product Owner** | Leonardo Setti | _______________ | 27/10/2026 |
| **Arquiteto** | Nicholas Anthony | _______________ | 27/10/2026 |
| **Dev Backend 1** | Fabrício Cabral | _______________ | 27/10/2026 |
| **Dev Backend 2** | Nicholas Anthony | _______________ | 27/10/2026 |
| **Dev Frontend** | Eduardo Passarelli | _______________ | 27/10/2026 |
| **QA Lead** | Nicolas Mallouk | _______________ | 27/10/2026 |

---

## 8. Arquivamento

- **Localização:** `docs/auditorias/POST-MORTEM.md` (repo Git)
- **Backup:** Sharepoint FATEC / pasta do projeto
- **Retenção:** Permanente (lições aprendidas institucionais)

---

**Fim do Post-Mortem — COBECO MVP**  
*Blameless: foco em processo, não pessoas. Lições aplicadas no próximo ciclo.*