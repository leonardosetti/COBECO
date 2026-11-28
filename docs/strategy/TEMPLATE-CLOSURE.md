# Termo de Encerramento do Projeto — <NOME DO PROJETO>

**Versão:** 1.0  
**Data:** DD/MM/AAAA  
**Projeto:** COBECO MVP  
**Período:** DD/MM/AAAA a DD/MM/AAAA  
**Autor:** Product Owner  
**Aprovação:** CCB + Banca Avaliadora (Gate 4)

---

## 1. Declaração de Encerramento

Por meio deste termo, declara-se oficialmente **ENCERRADO** o projeto **COBECO MVP**, tendo sido atingidos os objetivos propostos no Project Charter, entregues os artefatos contratados e validados pela banca avaliadora da FATEC Taquaritinga.

---

## 2. Objetivos vs. Resultados Alcançados

| Objetivo (Project Charter) | Métrica de Sucesso | Resultado Alcançado | Status |
|----------------------------|-------------------|---------------------|--------|
| Entregar MVP funcional (18 RFs) | 100% RFs Done no GitHub Projects | <XX%> | ☐ Atingido ☐ Parcial ☐ Não atingido |
| Cobertura de testes ≥ 80% | `pytest --cov-fail-under=80` | <XX%> | ☐ Atingido ☐ Parcial ☐ Não atingido |
| Documentação ABNT aprovada | Nota orientador ≥ 8,0 | <Nota> | ☐ Atingido ☐ Parcial ☐ Não atingido |
| Deploy reproduzível | `docker compose up` smoke test | ✅/❌ | ☐ Atingido ☐ Parcial ☐ Não atingido |
| Apresentação final (35 min) | Nota banca ≥ 8,0 | <Nota> | ☐ Atingido ☐ Parcial ☐ Não atingido |
| Clean Architecture + SDD | Code review R-01..R-07 + Specs ratificadas | ✅/❌ | ☐ Atingido ☐ Parcial ☐ Não atingido |

---

## 3. Entregas Físicas (Artefatos Finais)

| Artefato | Localização | Versão Final | Validado por |
|----------|-------------|--------------|--------------|
| **Código Fonte** | `git@github.com:leonardosetti/COBECO.git` (branch `main`, tag `v0.1.0`) | v0.1.0 | Tech Lead |
| **Documentação ABNT (PDF)** | Sharepoint FATEC / `docs/strategy/DOCUMENTACAO-ABNT.pdf` | Final | Orientador |
| **Project Charter** | `docs/strategy/PROJECT-CHARTER.md` | 1.0 | CCB |
| **Business Case** | `docs/strategy/BUSINESS-CASE.md` | 1.0 | PO |
| **PRD** | `docs/strategy/PRD.md` | 1.0 | CCB (Gate 2) |
| **User Stories (18 RFs)** | `docs/strategy/user-stories/US-*.md` + GitHub Issues | 1.0 | PO |
| **Matriz Rastreabilidade** | `docs/strategy/TRACEABILITY.md` | 1.0 | QA Lead |
| **Diagramas C4** | `docs/arquitetura/C4-*.md` | 1.0 | Arquiteto |
| **ADR-001 Stack** | `docs/decisoes/doc-adr-0001-stack-decision-v1.0.md` | Ratificada | CCB |
| **Constitution v2.0** | `constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md` | 2.0 | CCB |
| **Specs SDD (16)** | `.ai/specs/spec-*.spec.md` | Ratificadas | SDD Process |
| **Handoffs** | `.ai/handoffs/HF-*.md` | Processadas | L0 Dispatch |
| **RAID Log** | `docs/operacao/doc-raid-log-0001-raid-log-v1.0.md` | Final | Tech Lead |
| **Test Plan** | `docs/operacao/doc-test-plan-0001-test-plan-v1.0.md` | Final | QA Lead |
| **Runbooks** | `docs/operacao/RUNBOOK-*.md` | 1.0 | DevOps |
| **Release Notes v0.1.0** | `docs/operacao/doc-release-notes-0001-v0-1-0-v1.0.md` | 1.0 | PO |
| **Post-Mortem** | `docs/auditorias/audit-postmortem-0001-postmortem-v1.0.md` | 1.0 | Tech Lead |
| **Lições Aprendidas** | `docs/auditorias/audit-lessons-0001-lessons-learned-v1.0.md` | 1.0 | Equipe |
| **Apresentação Final (Slides)** | `docs/strategy/APRESENTACAO-FINAL.pdf` | Final | Equipe |

---

## 4. Métricas Finais do Projeto

### 4.1 Cronograma
| Métrica | Planejado | Realizado | Variação |
|---------|-----------|-----------|----------|
| Início | DD/MM/AAAA | DD/MM/AAAA | <dias> |
| Término | DD/MM/AAAA | DD/MM/AAAA | <dias> |
| Duração Total | 38 dias úteis | <X> dias úteis | <+/- dias> |
| Sprints Concluídas | 5 | <X> | — |

### 4.2 Qualidade
| Métrica | Meta | Alcançado | Status |
|---------|------|-----------|--------|
| Cobertura Testes Unitários | ≥ 80% | XX% | 🟢/🟡/🔴 |
| Testes E2E Passando | 100% críticos | YY/ZZ | 🟢/🟡/🔴 |
| Bugs Críticos em Produção | 0 | <N> | 🟢/🟡/🔴 |
| Lead Time médio (PR → Deploy) | < 2 dias | <X> dias | — |
| Deploy Frequency | 1/sprint | <X> | — |
| MTTR (Mean Time to Recovery) | < 1h | <X> min | — |
| Change Failure Rate | < 10% | <X>% | — |

### 4.3 Escopo
| Métrica | Valor |
|---------|-------|
| RFs Entregues | 18/18 (100%) |
| RFs Parciais | 0 |
| RFs Não Entregues | 0 |
| CRs Aprovados | <N> |
| CRs Rejeitados | <N> |
| Gold Plating Detectado | 0 (auditoria) |

### 4.4 Equipe
| Métrica | Valor |
|---------|-------|
| Tamanho da Equipe | 5 integrantes |
| Disponibilidade Média | XX% |
| Bus Factor Final | 2 (Backend) / 1 (Frontend) |
| Horas Totais Investidas | ~1.800h (estimado) |

---

## 5. Riscos e Issues Finais (RAID Log Final)

| ID | Item | Status Final | Resolução / Lição |
|----|------|--------------|-------------------|
| R-001 | Atraso Sprint 1 | ☐ Fechado / ☐ Aceito | <Como resolveu> |
| R-002 | Cobertura < 80% | ☐ Fechado / ☐ Aceito | <Como resolveu> |
| I-<NNN> | <Issue> | ☐ Resolvido / ☐ Contornado | <Ação> |

---

## 6. Lições Aprendidas (Consolidado)

### 6.1 O que Funcionou Bem (Keep)
1. **Spec-first (SDD) + Handoff** — Clareza total antes de codar; reduziu retrabalho.
2. **ADR-001 cedo** — Stack definida no Sprint 0 evitou thrashing técnico.
3. **Pair programming Auth** — Dois devs no crítico path (Auth) acelerou e melhorou qualidade.
4. **GitHub Projects + Milestones S1-S5** — Visibilidade total, rastreabilidade visual.
5. **Constitution v2.0 como lei suprema** — Decisões rápidas, sem bikeshedding.
6. **TDD desde Sprint 1** — Cobertura ≥80% natural, não "corrida" no final.
7. **Seed determinístico < 10s** — CI rápido, dev environment confiável.
8. **Runbooks testados** — Deploy/rollback sem sustos na demo.

### 6.2 O que Melhorar (Improve)
1. **Frontend bus factor 1** — Apenas 1 dev sabia Vanilla JS + Tailwind; cross-train na próxima.
2. **Docs ABNT atrasadas** — Iniciaram tarde (Sprint 1); iniciar no Sprint 0 da próxima vez.
3. **RAID Log atualização manual** — Automatizar coleta de riscos do GitHub Issues/PRs.
4. **Testes E2E frágeis** — Alguns flaky no Playwright; investir em seletores estáveis + retry.
5. **Estimativa de tarefas** — Subestimamos complexidade do cálculo orçamento (UC06); usar Planning Poker.
6. **Comunicação com orientador** — Reuniões quinzenais foram poucas; semanais curtas (15min) seriam melhores.

### 6.3 Surpresas (Surprise)
1. **MySQL InnoDB FK cascade** — Comportamento `ON DELETE CASCADE` em `itens_lista` apaga itens ao deletar lista (soft delete não cascateia). Documentado no DER.
2. **ReportLab fontes** — Fonte padrão não tem acentos PT-BR; precisou registrar `DejaVuSans` no container.
3. **nginx proxy cache** — Cache de 5min no `/v1/orcamento` causou dado stale em teste; header `Cache-Control: no-store` em dev.

### 6.4 Recomendações para Próximos Projetos
1. **Iniciar com Sprint 0 dedicado** a Charter, RACI, ADR, GitHub Projects, Docker — não misturar com Sprint 1.
2. **Definir bus factor mínimo 2** por área crítica no RACI.
3. **Automatizar RAID Log** via GitHub Actions (labels `risk`, `issue`, `dependency` → markdown).
4. **Investir em Design System mínimo** (tokens cores, espaçamento, componentes base) mesmo em Vanilla JS.
5. **Game Day por Sprint** — Testar runbook de rollback, restore, incident response a cada 2 semanas.

---

## 7. Aprovação Formal (Gate 4 — Encerramento)

| Papel | Nome | Assinatura | Data | Decisão |
|-------|------|------------|------|---------|
| **CCB Chair / PO** | | | | ☐ Aceitar Encerramento ☐ Requer Ação |
| **Tech Lead** | | | | ☐ Aceitar Encerramento ☐ Requer Ação |
| **Arquiteto** | | | | ☐ Aceitar Encerramento ☐ Requer Ação |
| **QA Lead** | | | | ☐ Aceitar Encerramento ☐ Requer Ação |
| **Orientador Acadêmico** | | | | ☐ Aceitar Encerramento ☐ Requer Ação |
| **Banca Avaliadora (1)** | | | | ☐ Aprovar Entrega ☐ Reprovar |
| **Banca Avaliadora (2)** | | | | ☐ Aprovar Entrega ☐ Reprovar |
| **Banca Avaliadora (3)** | | | | ☐ Aprovar Entrega ☐ Reprovar |

---

## 8. Próximos Passos Pós-Projeto (Opcional)

| Ação | Responsável | Prazo | Observação |
|------|-------------|-------|------------|
| Tornar repo público (se privado) | Tech Lead | Imediato | Portfolio equipe |
| Publicar article/post-mortem blog | PO | 30 dias | Compartilhar aprendizado |
| Submeter a evento/concurso | Equipe | 60 dias | SBES, WTD, etc. |
| Manutenção corretiva (se bugs) | Voluntários | Conforme demanda | Issue tracker ativo |
| Evoluir para v1.0 (Roadmap RD01-RD09) | Novo PO/Equipe | Novo ciclo | Novo Charter + CR |

---

## Controle de Versões

| Versão | Data | Autor | Mudança | Aprovado por |
|--------|------|-------|---------|--------------|
| 1.0 | DD/MM/AAAA | PO | Criação final pós-apresentação | CCB + Banca (Gate 4) |

---

**Fim do Termo de Encerramento**  
*Este documento formaliza o aceite final. Arquivar no repo e no Sharepoint FATEC.*