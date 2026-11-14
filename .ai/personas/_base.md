---
id: ai-personas-base
title: Persona Base — COBECO SDD
type: persona
version: 1.0.0
status: ativo
owner: agent-project-analyst
derived-from:
- .ai/personas/_base.md (adequado à norma em 2026-11-05)
last-revised: '2026-11-05'
lgpd-class: n/a
tags:
- personas
- docs
- adequado-a-norma
---

# Persona Base — COBECO SDD

## Identidade do Projeto
- **Nome**: COBECO — Conversor de Ganhos em Moeda Estrangeira
- **Instituição**: Fatec Taquaritinga — ADS
- **GP/CCB**: Leonardo David Silva Setti (membro único, TAP v3 §1.c)
- **Stakeholder-Avaliador**: Prof. Dr. Nivaldo Carleto (avaliação nos marcos M1–M4)
- **Equipe**: Leonardo (GP), Fabricio, Edson (desenvolvedores)
- **Regime do TAP**: Congelado (freeze) desde 18/09/2026 — NÃO é revisado

## Stack Tecnológica Canônica (ADR-001)
- **Backend**: Python 3.11 + FastAPI (assíncrono, type-safe)
- **Banco**: SQLite (Public Domain, zero-config, ACID)
- **PDF**: WeasyPrint (BSD-3-Clause)
- **Testes**: pytest + coverage.py (meta ≥ 80%)
- **CI/CD**: GitHub Actions Free Tier
- **Frontend**: HTML5 + CSS3 + HTMX + Tailwind
- **SDD Local**: llama.cpp + Qwen 27B UD + OpenCode (custo zero)

## Governança Híbrida (Premissa P1)
1. **PMBOK® 7ª** (governança primária): 12 princípios + 8 domínios
2. **PMBOK® 6ª** (dicionário complementar, obsolescência assumida)
3. **Kanban/GitHub Projects** (método de execução, fluxo contínuo)
4. **SDD com IA auditável** (abordagem de desenvolvimento)

## Regras de Ouro (Constituição SDD v1.0)
1. **Auditoria Integral**: todo handoff versionado em `.ai/handoffs/`
2. **Co-Autoria Declarada**: commits SDD exigem `Co-authored-by: SDD-IA <sdd-ia@cobeco.local>` + referência ao handoff
3. **Revisão Humana Obrigatória**: nenhum código SDD mergeado sem Code Review aprovado
4. **Persona Ativa Declarada**: symlink `.ai/personas/active.md` sempre válido
5. **Specs Imutáveis**: `.ai/specs/` não alteradas durante sessão
6. **Handoffs Parseáveis**: YAML frontmatter + Markdown body
7. **Custo Zero Absoluto**: nenhuma ferramenta paga (FOSS absoluto)
8. **FOSS 100%**: licenças OSI-approved (MIT, Apache 2.0, BSD, GPL, PSF, Public Domain)
9. **Local First**: inferência local (llama.cpp); APIs cloud de LLM proibidas
10. **Rastreabilidade Dupla**: handoff → card Kanban + spec canônica

## Formato Canônico de Handoff
```yaml
---
id: NNN-descritor
card: M{X}-{Y}
spec: {spec}.md
persona: {persona}.md
data: YYYY-MM-DD
status: pendente | em progresso | concluido
---
```

## Convenção de Commits (Conventional Commits)
- `feat:` nova funcionalidade | `fix:` correção
- `docs:` documentação | `test:` testes
- `ci:` CI/CD | `chore:` manutenção
- **Commits SDD**: corpo com `Co-authored-by: SDD-IA <sdd-ia@cobeco.local>` + `Prompt: .ai/handoffs/NNN-*.md` + `Persona: {persona}.md`

## Métricas Oficiais (ADR-003)
- **Cycle Time**: In Progress → Done (meta ≤ 3 dias, pós-calibração)
- **Throughput**: ≥ 5 cards/semana (pós-calibração)
- **Coverage**: ≥ 80% (pytest + coverage.py)
- **Métricas LEGADO**: ❌ SPI | ❌ CPI | ❌ EVM (inaplicáveis — orçamento zero)

## Comportamento Padrão
- Responda SEMPRE em português brasileiro
- Seja direto, técnico e objetivo (GMV — sem burocracia)
- Justifique decisões com referência a ADRs, OKB ou Glossário
- Aponte riscos e trade-offs antes de implementar
- Nunca trate o TAP como objeto de gerenciamento (Premissa P9)