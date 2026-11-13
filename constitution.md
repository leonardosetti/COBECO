# Constituição — COBECO MVP

**Projeto:** Cotação de Bens de Consumo (COBECO)  
**Local:** FATEC Taquaritinga — Análise e Desenvolvimento de Sistemas  
**Versão:** 1.0  
**Status:** Lei suprema do repositório

---

## Art. 1 — Identidade e escopo

1.1. O projeto denomina-se **COBECO** — Cotação de Bens de Consumo, MVP de comparação de preços entre fornecedores a partir de listas de compras.
1.2. Stack: FOSS 100%, LGPD primária, CPU-local (8700G / 60GB / llama.cpp), zero cloud, zero CUDA.
1.3. Escopo congelado: 18 RFs (REQUISITOS.md v3.2), 29 UCs (CASOSDEUSO.md v3.2), 8 tabelas PT-BR (CAMADADEDADOS.md v3.2).
1.4. Qualquer alteração de escopo requer CCB com ratificação humana (Art. 5.1).

## Art. 2 — Hierarquia normativa

Em conflito, vence o documento de nível superior:

1. `constitution.md` (lei suprema)
2. `AGENTS.md` (estado do repo e convenções)
3. `REQUISITOS.md` + `CASOSDEUSO.md` + `CAMADADEDADOS.md` (SSOT v3.2)
4. `board_roadmap.md` + `README.md` (planejamento)
5. ADRs (`docs/decisoes/`)
6. Especificações SDD (`.ai/specs/`)
7. Código-fonte
8. Arquivos de agente (`.opencode/agents/`)

## Art. 3 — Princípios de desenvolvimento

3.1. KISS: escopo enxuto, dados mockados via seed, UI desktop-first.
3.2. Clean Architecture: separação entre Domínio, Casos de Uso, Adaptadores, Frameworks.
3.3. ACID: transações explícitas, engine InnoDB ou equivalente, sem dados órfãos.
3.4. SDD (Spec-Driven): todo código entra apenas via spec + handoff par.
3.5. LGPD: dados sintéticos apenas; sem PII reais em seeds, fixtures, logs ou backups.
3.6. FOSS-first: nenhuma dependência paga ou proprietária sem Bypass de 3 pilares.
3.7. YAGNI: nenhuma abstração, wrapper ou opção "para depois" que não seja exigida pelo escopo atual.

## Art. 4 — Governança de agentes

4.1. O roster SSOT é `.ai/agents/registry.yaml` (projeto: COBECO).
4.2. O orquestrador L0 é `agent-nexus-prime-ultimate`; despacha via `scripts/nexus_dispatcher.py`.
4.3. Todo agente responde com parcel half-duplex contendo campo `dod` e `kill_switch`.
4.4. Kill Switch é não-negociável (vetores LGPD, vigilância, bypass de CI, meta-bypass).
4.5. Bypass requer: force majeure + saída FOSS nomeada + ratificação CCB humana.
4.6. Nenhum agente escreve código, specs ou arquivos de outro agente sem dispatch do L0.

## Art. 5 — Autoridade humana

5.1. O Humano é decisor único (CCB chair); aprovação humana é separada e obrigatória para merge e release.
5.2. Nenhum agente decide datas, orçamento ou escopo.
5.3. Recusa de conflito de interesse: agente não revisa nem aprova próprio trabalho.

## Art. 6 — Método SDD

6.1. Todo fluxo entra como spec (`.ai/specs/*.md`) e sai como handoff (`.ai/handoffs/HF-*.md`).
6.2. Handoff deve passar pelo `handoff_parser.py` antes do dispatch.
6.3. Cadeia de merge: reviewer (rubrica) → qa-sdet (evidência) → CI verde → gatekeeper → aprovação humana.

## Art. 7 — Segurança

7.1. Nenhum segredo, chave ou credencial em repositório, logs ou artefatos.
7.2. Rate limiting e validação de entrada em todas as fronteiras HTTP.
7.3. Erros nunca expõem tracebacks, payloads de usuário ou dados financeiros.

## Art. 8 — Qualidade

8.1. Cobertura de testes ≥ 80% nos módulos tocados (gate CI, não negociável).
8.2. Testes determinísticos: sem relógio de parede, sem rede, sem dados reais.
8.3. Todo PR passa por review rubric-citado (R-01..R-07) antes do merge.

---

**Última revisão:** 08 de Novembro de 2026  
**Próxima revisão:** após decisão de stack (README vs board_roadmap)