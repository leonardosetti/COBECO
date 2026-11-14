# Business Case — COBECO MVP (Versão Acadêmica)

**Versão:** 1.0  
**Status:** Aprovado  
**Data:** 13/11/2026  
**Autor:** Leonardo Setti (Product Owner)  
**Relacionado:** `docs/strategy/PROJECT-CHARTER.md`

---

## 1. Sumário Executivo

O **COBECO MVP** é um sistema web desktop-first para comparação de preços de compras entre fornecedores. O projeto visa entregar um software funcional open-source em 30 dias úteis (5 sprints), desenvolvido por uma equipe de 5 alunos do curso de Análise e Desenvolvimento de Sistemas da FATEC Taquaritinga, como requisito da disciplina Laboratório de Engenharia de Software.

O problema abordado é real: consumidores gastam 30+ minutos comparando preços manualmente em múltiplos estabelecimentos. O COBECO reduz esse tempo para <5 minutos via lista de compras + seleção de fornecedores + motor de comparação consolidado + exportação PDF para impressão.

O investimento é **zero financeiro** (R$ 0,00) — apenas horas da equipe (estimadas em ~1.800h totais) e uso de ferramentas FOSS (GitHub, Docker, MySQL, Python, Vanilla JS). O retorno é **educacional e de portfólio**: software funcional público, artefatos de governança PMBOK+SDD reutilizáveis, e aprendizado prático de Clean Architecture, CI/CD, testes, LGPD.

---

## 2. Contexto e Problema

### 2.1 Situação Atual
- Comparação de preços de compras é feita manualmente: ida a múltiplos mercados, anotação de preços, planilhas caseiras.
- Não existe ferramenta simples, offline-first, desktop-only, que permita criar lista → selecionar fornecedores confiáveis → comparar → imprimir PDF.
- Soluções existentes são mobile-first, requerem cadastro em marketplaces, ou são complexas (ERP).

### 2.2 Oportunidade de Melhoria
- Entregar MVP em 30 dias com stack moderna (FastAPI, MySQL, Vanilla JS) e governança profissional (PMBOK 7 + SDD + Constitution).
- Código open-source no GitHub serve como portfólio técnico para os 5 integrantes.
- Artefatos de governança (Charter, RACI, PRD, Specs, C4, RAID, Runbooks) são templates reutilizáveis.

### 2.3 Consequências de Não Fazer
- Perda da oportunidade acadêmica (nota da disciplina).
- Equipe não pratica engenharia de software profissional (SDD, CI/CD, testes, docs).
- Portfolio técnico fraco para mercado de trabalho.

---

## 3. Análise de Alternativas

| Alternativa | Descrição | Prós | Contras | Custo Estimado | Tempo | Recomendação |
|-------------|-----------|------|---------|----------------|-------|--------------|
| **A — COBECO MVP (Escolhida)** | FastAPI + MySQL + Vanilla JS + Docker + SDD + PMBOK híbrido | Stack definida (ADR-001), Constitution v2.0, governança clara, FOSS, prazo viável | Requer disciplina SDD, pair programming, TDD | R$ 0 | 30 dias | ☑ **Escolhida** |
| B — Stack React/NestJS/PostgreSQL (README original) | Full TypeScript, NestJS, Prisma, PostgreSQL | Ecossistema maduro, type-safe fullstack | Curva aprendizado alta, 2 linguagens, build complexo, prazo risco | R$ 0 | 45+ dias | ☐ |
| C — Status Quo (não fazer) | Entregar apenas docs ABNT sem código | Zero esforço técnico | Nota zero na implementação, sem portfolio, sem aprendizado | R$ 0 | 0 dias | ☐ |

**Alternativa Escolhida:** **A** — Alinhada com ADR-001 ratificada, Constitution v2.0, prazo acadêmico, equipe capabilities.

---

## 4. Benefícios Esperados

### 4.1 Benefícios Quantificáveis (Tangíveis)
| Benefício | Métrica | Valor Atual | Valor Alvo | Ganho | Como Medir |
|-----------|---------|-------------|------------|-------|------------|
| Tempo comparação preços | Minutos | 30 min (manual) | 5 min (COBECO) | -83% | Cronômetro em teste usabilidade |
| Cobertura testes | % | 0% (início) | ≥ 80% | +80 pp | `pytest --cov` |
| Deploy reproduzível | Boolean | Falho (sem Docker) | `docker compose up` OK | 100% | Smoke test CI |
| Artefatos governança | Count | 0 | 15+ (Charter, RACI, PRD, Specs, C4, RAID, Runbooks) | 15+ | Repo `docs/` + `.ai/` |

### 4.2 Benefícios Qualitativos (Intangíveis)
| Benefício | Descrição | Stakeholder Impactado |
|-----------|-----------|----------------------|
| Aprendizado Clean Architecture + SDD | Equipe aplica padrões profissionais, spec-first, handoff, code review | 5 alunos |
| Portfolio GitHub público | Repo com 18 RFs, CI verde, docs, releases | 5 alunos (LinkedIn/GitHub) |
| Templates reutilizáveis | Charter, RACI, PRD, Specs, C4, RAID, Runbooks para projetos futuros | FATEC / Comunidade |
| Experiência PMBOK híbrido | Governança leve + agilidade técnica, gates CCB, stage gates | 5 alunos |
| Conformidade LGPD (sintéticos) | Seed + testes sem PII real, Constitution Art. 3.5 | Projeto / Instituição |

---

## 5. Investimento Necessário

### 5.1 Recursos Humanos
| Papel | Qtd | Dedicação | Horas Estimadas | Observação |
|-------|-----|-----------|-----------------|------------|
| Product Owner / Tech Lead | 1 (Leonardo) | 50% | ~300h | Charter, RACI, PRD, PO duties, code review |
| Dev Backend | 2 (Fabrício, Nicholas) | 100% | ~600h cada | Auth, Listas, Comparação, PDF, Perfil, Seed, Migrations |
| Dev Frontend | 1 (Eduardo) | 100% | ~300h | Auth pages, Listas UI, Comparação UI, PDF print, Perfil UI, Feedback components |
| QA / Dev Backend | 1 (Nicolas) | 50% QA + 50% Backend | ~300h | Test Plan, Unit/E2E, CI, RAID, Runbooks, Seed |

**Total Horas Estimadas:** ~2.100h (equipe de 5, 38 dias úteis = ~11h/dia/pessoa média)

### 5.2 Infraestrutura e Ferramentas (Todas FOSS / Free Tier)
| Item | Custo | Modelo |
|------|-------|--------|
| GitHub (repo público + Actions 2000min/mês + Projects) | Gratuito | Free tier |
| ghcr.io (Docker images) | Gratuito | Free tier |
| MySQL 8.0 (container) | Gratuito | FOSS |
| Python 3.11 + FastAPI + SQLAlchemy + Alembic + pytest + ruff + mypy | Gratuito | FOSS |
| Vanilla JS + Tailwind CSS + nginx | Gratuito | FOSS |
| ReportLab (PDF) | Gratuito | FOSS |
| Playwright (E2E) | Gratuito | FOSS |
| VS Code / Git / Docker Desktop | Gratuito | FOSS / Já instalados |

**Investimento Financeiro Total: R$ 0,00**

---

## 6. Análise Financeira (Simplificada - Acadêmica)

| Métrica | Valor | Observação |
|---------|-------|------------|
| **ROI Financeiro** | N/A | Projeto sem receita direta |
| **Payback** | N/A | Não aplicável |
| **Valor Agregado (EVM)** | Acompanhar via Sprint Review | Velocity (SP/sprint), Burndown, % Done |
| **Custo por Sprint** | ~420h / sprint | 5 pessoas × 6 dias × ~14h/dia (inclui estudo) |
| **Custo Total (Horas)** | ~2.100h | Proxy de "investimento" |

> **Nota:** Por ser projeto acadêmico sem fins lucrativos, a análise foca em **valor educacional**, **entrega no prazo** e **qualidade técnica** como proxies de retorno. O "orçamento" é tempo da equipe.

---

## 7. Riscos Financeiros e de Cronograma

| Risco | Impacto no Cronograma | Impacto em Horas (Custo) | Mitigação |
|-------|----------------------|--------------------------|-----------|
| Atraso Sprint 1 (Setup/Auth) | +3 a 5 dias | +200h | Parallelizar setup + docs; Pair programming Auth |
| Baixa cobertura testes | Rework Sprint 5 | +150h | TDD desde Sprint 1; Metas intermediárias |
| Integração Front↔Back falha | +2 dias | +80h | Contrato OpenAPI primeiro (SDD); RFC se divergência |
| Membro indisponível >3 dias | +5 a 10 dias | +300h | Bus factor 2; Pair programming; Redistribuir WBS |
| Docs ABNT rejeitadas | +5 dias (rework) | +100h | Iniciar dia 1; Revisão semanal orientador |

---

## 8. Cronograma de Realização de Benefícios

| Benefício | Quando Começa a Ser Realizado | Como Validar |
|-----------|-------------------------------|--------------|
| Aprendizado técnico (SDD, Clean Arch, CI/CD) | Sprint 0 (Setup) | Code review, Retrospectiva, Specs ratificadas |
| Software funcionando (Auth + Listas) | Sprint 2 (Fim) | Demo interna + `make test` verde |
| Comparação completa + PDF | Sprint 4 (Fim) | Demo interna fluxo completo |
| Demo para banca + Portfolio | Sprint 5 (Fim) | Apresentação oficial + Repo público |
| Artefatos governança reutilizáveis | Pós-projeto | Templates em `docs/` + `.ai/` no GitHub |

---

## 9. Aprovação (Gate 1 — 13/11/2026)

| Papel | Nome | Assinatura | Data | Decisão |
|-------|------|------------|------|---------|
| **CCB Chair / PO** | Leonardo Setti | _______________ | 13/11/2026 | ☑ Aprovar |
| **Tech Lead** | Leonardo Setti | _______________ | 13/11/2026 | ☑ Aprovar |
| **Orientador Acadêmico** | [Nome Orientador] | _______________ | 13/11/2026 | ☑ Aprovar |

---

## 10. Controle de Versões

| Versão | Data | Autor | Mudança |
|--------|------|-------|---------|
| 1.0 | 13/11/2026 | Leonardo Setti | Criação inicial — Gate 1 CCB |

---

**Fim do Business Case — COBECO MVP**  
*Versão acadêmica simplificada — foco em valor educacional e entrega técnica.*