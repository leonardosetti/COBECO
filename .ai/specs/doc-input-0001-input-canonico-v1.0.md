---
id: doc-input-0001-input-canonico-v1.0
type: doc-input
title: DOC INPUT — Input Canonico
version: v1.0
status: ratificado
canonical: false
canonical_slug: input-canonico
created: '2026-11-14'
updated: '2026-11-14'
author: Leonardo Setti (@leonardosetti)
owner: CCB
ratified_by: null
ratified_at: null
supersedes: null
superseded_by: null
trace:
  constitution: []
  req_func: []
  req_nfunc: []
  use_cases: []
  specs: []
  handoffs: []
  adrs: []
  code: []
  tests: []
domain: specs
layer: spec
tags: []
lgpd_class: n/a
workflow:
  stage: rascunho
  reviewer: null
  reviewed_at: null
  approval_hash: null
  board_url: null
---
# INPUT CANÔNICO SUBORDINADO — COBECO v4.1.1

Este artefato é derivativo e subordinado. Ele não cria norma autônoma.
Hierarquia aplicável: constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md > TAP v3 > ADRs > OKB > Planos > Glossário > Este input > Especificações SDD > Código-fonte e testes.
Em conflito com camada superior, prevalece a hierarquia do Art. 2 da constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md v1.2.0.

## Hardware
- CPU: AMD Ryzen 7 8700G, Zen 4, 8C/16T, AVX-512.
- GPU: AMD Radeon 780M, RDNA 3, APU com VRAM compartilhada.
- RAM: 58GB reais; não usar 60GB nem 64GB como valor operativo.
- Limite de inferência: 32GB via systemd.
- SO: Arch Linux.
- Mesa: 26.2.2.
- Vulkan API: 1.4.354.
- Vulkan driver/loader: 1.4.357.

## Motor e modelo SDD
- Motor: llama.cpp com Vulkan, LTO e AVX-512.
- Service: systemd llama-server.
- Porta: 127.0.0.1:8080.
- Modelo primário: Qwen3-30B-A3B Q4_K_M.
- Modelo fallback: Qwen 14B Q4_K_M.
- Modelo batch: Qwen 72B Q4_K_M, deferred.
- Modelo deprecated: Qwen3.8-27B Q4_K_M, não usar.
- Contexto configurado: 32.768 tokens.
- Orçamento efetivo: 24.000 tokens.
- Output máximo: 4.096 tokens.
- Performance alvo: ≥ 12 t/s geração; ≥ 25 t/s prompt processing.

## Stack do produto
- Python 3.11.
- FastAPI.
- Uvicorn.
- PostgreSQL 15+.
- SQLAlchemy async com asyncpg.
- Alembic.
- Docker e Docker Compose.
- Nginx latente.
- WeasyPrint.
- Jinja2.
- HTMX e Tailwind no frontend.
- pytest, pytest-asyncio, pytest-cov.
- mypy e flake8.
- GitHub Actions Free Tier como Bypass registrado.

## APIs de câmbio
- Primária: Frankfurter.
- Fallbacks candidatos: fawazahmed0 currency-api, CurrencyConverter, AllRatesToday, datasets de bancos centrais, ECB Data Portal.
- Fallback mandatório: PTAX/BCB.
- Padrão: Circuit Breaker + adapter pattern + cache TTL no PostgreSQL.

## Governança operacional
- PMBOK 7ª como governança primária.
- PMBOK 6ª apenas como dicionário, com obsolescência procedural declarada.
- Kanban em GitHub Projects como SSOT de execução.
- Colunas: Backlog, Ready, In Progress, Code Review, Done.
- WIP: 3 por pessoa.
- Métricas vigentes: Cycle Time, Throughput, CFD, WIP, Coverage.
- Métricas obsoletas: EVM, SPI, CPI.
- Tasklists Markdown para cards ≥ 6h.
- Subissues rejeitadas.
- Labels mínimos por card: tipo, macro-fase, área, prioridade e MoSCoW quando aplicável.

## Protocolo de agentes
- Fluxo half-duplex.
- Auto-delegação proibida.
- Agentes são conselho, nunca veto ao humano.
- Revisão humana obrigatória antes de merge.
- Parcel JSON obrigatório ao final de tarefa complexa.
- Kill switch constitucional e operacional.