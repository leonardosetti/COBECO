# Plano de Implementação — COBECO MVP v2.0

**Status:** rascunho de execução (orientativo, verboso, ubíquo)  
**Versão:** 2.0  
**Data:** 13 de Novembro de 2026  
**Base normativa:** `constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md` v2.0 (lei suprema), `req-func-0001-requisitos-funcionais-canon.md` v3.2, `doc-arch-0001-camada-de-dados-canon.md` v3.2, `req-use-case-0001-casos-de-uso-canon.md` v3.2, `ADR-001` (stack ratificada), `board-roadmap-0001-roadmap-canon.md` (marcos S1–S5)  
**Repositório:** `git@github.com:leonardosetti/COBECO.git` (branch `main`, commit `e47a2de`)  
**Nota para sessões autônomas:** este roteiro deve ser seguido quase que de forma autônoma em rodadas direcionadas, sem ações destrutivas deliberadas.

---

# TÍTULO I — CONTEXTO E PRÉ-req-func-0001-requisitos-funcionais-canon

## 1. Estado atual do repositório

O scaffold do MVP já está publicado e versionado:

| Artefato | Estado | Local |
|---|---|---|
| Constitution v2.0 | ✅ Lei suprema | `constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md` |
| doc-agents-0001-agents-canon.md | ✅ Atualizado | `doc-agents-0001-agents-canon.md` |
| Requisitos SSOT v3.2 | ✅ | `req-func-0001-requisitos-funcionais-canon.md`, `req-use-case-0001-casos-de-uso-canon.md`, `doc-arch-0001-camada-de-dados-canon.md` |
| Stack ADR-001 | ✅ Ratificada | `docs/decisoes/doc-adr-0001-stack-decision-v1.0.md` |
| Backend FastAPI | ✅ Scaffold | `backend/src/` (domain/usecases/adapters) |
| Frontend Vanilla JS | ✅ Scaffold | `frontend/src/` (app.js, index.html) |
| Proxy nginx | ✅ | `proxy/config-nginx-0003-proxy-nginx-v1.0.conf` |
| Docker Compose | ✅ | `config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml`, `override` |
| Alembic + seed | ✅ | `backend/config-alembic-0001-alembic-v1.0/`, `backend/config-seed-0001-seed-v1.0.sql` |
| CI GitHub Actions | ✅ | `.github/workflows/config-ci-0001-github-actions-v1.0.yml` |
| Specs SDD | ✅ | `.ai/specs/spec-001…015` |
| Handoffs | ✅ | `.ai/handoffs/HF-*` |
| Templates de elite | ✅ | `docs/strategy/`, `docs/rfc/`, `docs/change/`, `docs/decisoes/`, `docs/operacao/`, `docs/auditorias/` |
| `config-env-0001-env-example-v1.0` | ⚠️ Não commitar | Já no `.gitignore` |

## 2. Skills a utilizar (ponto de partida)

### 2.1 Skills primárias

| Skill | Papel no plano | Quando acionar |
|---|---|---|
| `ponytail` | Solução mínima que funciona; evitar over-engineering; YAGNI | Toda implementação de código |
| `caveman` | Comunicação técnica direta; revisão de código sem cerimônia | Code review, diff review, documentação técnica |

### 2.2 Skills secundárias (UI/UX e frontend)

| Skill | Papel no plano | Quando acionar |
|---|---|---|
| `ui-ux-pro-max` | Direção de design, acessibilidade, tipografia, paleta, componentes | Telas do frontend, feedback visual (RNF05), impressão A4 (RF18) |
| `frontend-design` | Escolhas estéticas intencionais, não-templatizadas | Layout desktop-first ≥1024px, Tailwind config, componentes visuais |

### 2.3 Skills de suporte (conforme necessidade)

| Skill | Papel | Quando acionar |
|---|---|---|
| `caveman-review` | Revisão comprimida de diff/PR | Antes de todo merge |
| `caveman-commit` | Mensagens de commit Conventional Commits | Todo commit |
| `investigate-first` | Diagnóstico de falhas ambíguas | Quando houver regressão ou comportamento intermitente |
| `safe-refactor` | Restruturação preservando comportamento | Refatoração de backend/frontend |
| `surgical-patch` | Correção de bugs em camada estreita | Bugs pontuais em produção/homolog |
| `verify-and-stop` | Validação-only de aceitação | Última milha antes de release |

---

# TÍTULO II — PRINCÍPIOS DE IMPLEMENTAÇÃO (PONYTAIL + CAVEMAN)

## 3. Regras obrigatórias de implementação

3.1. **Ponytail (lazy senior):** escrever o mínimo código que resolva o problema completo. Nada de abstração, wrapper, tipo conversão, opção, config, boilerplate ou "para depois" que não seja exigido pelos 18 RF.

3.2. **Caveman (terse):** toda comunicação técnica direta, sem cerimônia, sem hedging, sem "Sure, I'd be happy to help". Um ideia por frase, máximo 20 palavras.

3.3. **Não ações destrutivas:** nunca executar `docker compose down -v`, `git reset --hard`, `rm -rf` em diretórios com dados, ou qualquer comando que apague dados sem confirmação humana explícita.

3.4. **SDD obrigatório (Constitution Art. 6):** todo código entra apenas via par spec + handoff aprovado. Nenhum código solto.

3.5. **DoD por PR (Constitution Art. 8.4):** Clean Architecture, queries parameterizadas, PT-BR, testes ≥80%, OpenAPI atualizado, `docker compose up` sem config manual.

---

# TÍTULO III — ARTEFATOS DE GOVERNANÇA (CRIAÇÃO OBRIGATÓRIA)

## 4. Artefatos de estratégia e planejamento

Criar, preencher e versionar os seguintes artefatos usando os templates de elite já existentes:

### 4.1 PRD (Proddoc-arch-0006-uc-v1t Requirements Document)
- **Arquivo:** `docs/strategy/PRD-001-cobeco-mvp.md`
- **Conteúdo:** requisitos de negócio, objetivos do produto, público-alvo, métricas de sdoc-arch-0006-uc-v1esso, RFs RF01–RF18, RNFs RNF01–RNF12.
- **Template:** `docs/strategy/TEMPLATE-PRD.md`

### 4.2 BRD (Business Requirements Document)
- **Arquivo:** `docs/strategy/BRD-001-cobeco-mvp.md`
- **Conteúdo:** necessidades de negócio de alto nível, retorno esperado, justificativa acadêmica.
- **Template:** copiar de `TEMPLATE-PRD.md` e adaptar (foco negócio/orçamento).

### 4.3 RFC (Request for Comments)
- **Arquivo:** `docs/rfc/RFC-001-<mudanca-proposta>.md`
- **Conteúdo:** proposta de mudança ampla para coleta de feedback antes de decisão final.
- **Template:** `docs/rfc/template-rfc-0001-rfc-v1.0.md`

### 4.4 CR (Change Request)
- **Arquivo:** `docs/change/CR-<NNN>-<descricao>.md`
- **Conteúdo:** alteração de escopo, prazo, custo ou requisitos aprovados. Análise de impacto obrigatória.
- **Template:** `docs/change/template-cr-0001-cr-v1.0.md`

### 4.5 Roadmap
- **Arquivo:** `board-roadmap-0001-roadmap-canon.md` (já existe, atualizar se necessário)
- **Conteúdo:** marcos S1–S5, datas, RFs atendidos.

## 5. Artefatos de arquitetura e especificação técnica

### 5.1 ADR (Architecture Decision Record)
- **Diretório:** `docs/decisoes/`
- **Arquivo:** `ADR-<NNN>-<slug>.md`
- **Quando:** toda decisão arquitetural importante (stack, banco, auth, deploy).
- **Template:** `docs/decisoes/template-adr-0001-adr-v1.0.md`

### 5.2 SPEC / Design Doc
- **Diretório:** `.ai/specs/`
- **Arquivo:** `spec-<NNN>-<slug>-v<ver>.spec.md`
- **Quando:** toda funcionalidade antes da implementação.
- **Template:** `.ai/specs/template-spec-0001-spec-v1.0.md`
- **Frontmatter canônico:** `id`, `title`, `type`, `version`, `status`, `owner`, `derived-from`, `last-revised`, `lgpd-class`, `tags`.

### 5.3 API Contract (OpenAPI/Swagger)
- **Local:** `/docs` no backend (quando `DEBUG=true`)
- **Conteúdo:** endpoints, parâmetros, formatos de resposta, códigos de erro.
- **Permite:** frontend e backend trabalharem em paralelo sem quebras de integração.

### 5.4 C4 / Diagramas de Arquitetura
- **Diretório:** `docs/arquitetura/`
- **Níveis:** Contexto, Contêineres, Componentes, Código.
- **Ferramenta:** Draw.io/Excalidraw existentes em `brain/diagrams/`.

## 6. Artefatos de execução e controle operacional

### 6.1 Epic / User Story / Task
- **Ferramenta:** GitHub Projects (milestones S1–S5)
- **Branch:** `feat/UC-XX-descricao`
- **Template:** `docs/strategy/TEMPLATE-USER-STORY.md`

### 6.2 TODO / FIXME / Tech Debt Log
- **Arquivo:** `docs/operacao/TECH-DEBT.md` (criar a partir do template)
- **Regra:** todo TODO/FIXME no código deve ter data, autor e issue vinculada.
- **Template:** `docs/operacao/template-tech-debt-0001-tech-debt-v1.0.md`

### 6.3 Test Plan / QA Sign-off
- **Arquivo:** `docs/operacao/doc-test-plan-0001-test-plan-v1.0-<release>.md`
- **Conteúdo:** estratégia de testes, cenários críticos, critérios de aceite.
- **Template:** `docs/operacao/template-test-plan-0001-test-plan-v1.0.md`

### 6.4 Changelog / Release Notes
- **Arquivo:** `CHANGELOG.md` (raiz)
- **Conteúdo:** novidades, correções, breaking changes por versão.
- **Template:** `docs/operacao/template-changelog-0001-changelog-v1.0.md`

## 7. Artefatos de operação, riscos e conformidade

### 7.1 Runbook / Playbook
- **Arquivo:** `docs/operacao/RUNBOOK.md`
- **Conteúdo:** instruções passo a passo para operação, manutenção, resposta a incidentes.
- **Template:** `docs/operacao/template-runbook-0001-runbook-v1.0.md`

### 7.2 Post-Mortem / RCA
- **Diretório:** `docs/auditorias/`
- **Arquivo:** `postmortem-<id>.md`
- **Quando:** após incidente em produção.
- **Template:** `docs/auditorias/template-postmortem-0001-postmortem-v1.0.md`

### 7.3 SLA / SLO / SLI
- **Arquivo:** `docs/auditorias/SLA-SLO-SLI.md`
- **Conteúdo:** acordos de nível de serviço, objetivos de confiabilidade, indicadores.
- **Template:** `docs/auditorias/template-sla-0001-sla-slo-sli-v1.0.md`

### 7.4 DPIA / Threat Model
- **Arquivo:** `docs/auditorias/DPIA-THREAT-MODEL.md`
- **Conteúdo:** avaliação de riscos de segurança e privacidade (LGPD).
- **Template:** `docs/auditorias/template-dpia-0001-dpia-threat-v1.0.md`

---

# TÍTULO IV — IMPLEMENTAÇÃO OTIMIZADA DE CONTAINERS (DOCKER / PODMAN)

## 8. Estrutura de containers (arquitetura ortogonal)

A Constitution (Art. 12.1) exige redes ortogonais:
- **rede `data`** (interna, DB only): `db`, `migrate`, `seed`, `backend` (acesso ao DB)
- **rede `edge`** (externa): `frontend`, `backend`, `proxy`
- **Proxy nginx** na porta 8380: `/` → frontend, `/v1/` → backend, `/openapi.json` → backend

## 9. Implementação otimizada (Docker Compose — padrão do projeto)

O `config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml` já existe com serviços: `db`, `migrate`, `seed`, `backend`, `frontend`, `proxy`.

### 9.1 Boas práticas obrigatórias para containers

| Prática | Aplicação |
|---|---|
| Imagens oficiais e fixadas | `mysql:8.0`, `nginx:alpine`, builds a partir de `Dockerfile` fixo |
| Variáveis de ambiente via `config-env-0001-env-example-v1.0` | Nunca commitar `config-env-0001-env-example-v1.0`; usar `config-env-0001-env-example-v1.0.example` |
| Healthchecks | `db` tem healthcheck; `backend` e `frontend` devem ter |
| Limites de memória | Já definidos no `config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml` (ex: db 1G, backend 512M) |
| Redes isoladas | `data` interna, `edge` externa (já configurado) |
| Volumes nomeados | `db_data` para persistência do MySQL |
| Ordem de inicialização | `db` → `migrate` → `seed` → `backend` → `frontend` → `proxy` |

### 9.2 Opção Podman (alternativa, se requerido)

Se o ambiente de destino usar Podman em vez de Docker:
- Substituir `docker compose` por `podman-compose` ou `config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0` compatível com Podman
- Ajustar `--default-authentication-plugin=mysql_native_password` se necessário
- Manter a mesma estrutura de redes e serviços
- Não modificar o `config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml` existente sem CR ratificado (Constitution Art. 5.4)

### 9.3 Não ações destrutivas

- Nunca rodar `docker compose down -v` sem confirmação humana (apaga volume `db_data`)
- Nunca rodar `docker system prune -f` sem revisar o que será removido
- Sempre fazer backup do volume antes de recriar o banco: `docker cp cobeco-db:/var/lib/mysql ./backup/`

---

# TÍTULO V — WORKFLOWS DE IMPLEMENTAÇÃO OTIMIZADOS E SEGUROS

## 10. Fluxo de trabalho geral (branch → PR → merge)

```
1. Criar branch: feat/UC-XX-descricao (a partir de main)
2. Implementar (ponytail: mínimo código que funcione)
3. Criar/atualizar spec + handoff (SDD, se ainda não existir)
4. Criar/atualizar artefatos de governança (User Story, Tech Debt, etc.)
5. Commit: tipo(escopo): resumo imperativo (caveman-commit)
6. Push para o branch remoto
7. Abrir PR para main
8. CI roda: ruff + pytest --cov≥80 + mypy + build Docker (<5 min)
9. Code review: rubrica R-01..R-07 (caveman-review)
10. Gatekeeper: verifica DoD (Art. 8.4)
11. Aprovação humana (CCB chair)
12. Merge em main
13. Mover card no kanban para "Done"
```

## 11. Workflow por Sprint (S1–S5)

### Sprint 1 — Setup, Docs e Auth (RF01–RF04)
1. Validar `config-env-0001-env-example-v1.0.example` → copiar para `config-env-0001-env-example-v1.0` local (não commitar)
2. Verificar `docker compose up -d --build` sobe todos os serviços
3. Executar `make migrate` e `make seed`
4. Implementar router de perfil completo (`backend/src/adapters/api/perfil.py`) — RF05/RF06
5. Verificar auth: cadastro (RF01), login JWT (RF02), logout (RF03), recuperação senha (RF04)
6. Testes: `make test` (integration `test_auth_flow.py`)
7. Critério de saída: RF01–RF06 funcionando via `docker compose up`

### Sprint 2 — Listas e Catálogo (RF07–RF11)
1. Verificar routers `catalogo.py`, `listas.py`, `comparacao.py`
2. Verificar frontend `app.js` (autocomplete debounce 300ms, lista em memória `sessionStorage`)
3. Validar transação ACID em salvar lista (RF08)
4. Validar soft delete (`deletado_em`) em listas e usuarios
5. Rodar `make seed` (<10s — RNF08)
6. Critério de saída: fluxo cadastro → lista → salvar → listar funcionando

### Sprint 3 — Pré-filtro e Comparação (RF12–RF16)
1. Verificar seleção de categorias (RF12), fornecedores (RF13), slider disponibilidade (RF14)
2. Verificar cálculo de orçamento com cache 5min + timeout 10s (RF15)
3. Verificar tabela ordenada preço ASC, destaque verde melhor oferta (RF16)
4. Critério de saída: fluxo categorias → fornecedores → cálculo → resultados funcionando

### Sprint 4 — Exportação, Perfil e Polish (RF17–RF18)
1. Verificar `POST /export/pdf` com ReportLab, PDF A4, nome `lista_YYYYMMDD.pdf` (RF17)
2. Verificar `<5s` para até 100 itens (RNF11)
3. Verificar CSS `@media print` (ocultar menus, quebras de página, header repetido) (RF18)
4. Verificar feedback visual global: toasts, loading, modais (RNF05)
5. Critério de saída: PDF baixável e Ctrl+P gera view A4 limpa

### Sprint 5 — Buffer, QA e Demo (Todos)
1. Escrever testes unitários em `backend/tests/unit/` (cobertura ≥80% — RNF06)
2. Implementar testes E2E Playwright (fluxo demo: cadastro → comparação → exportação PDF)
3. Rodar `make ci` localmente (<5 min — RNF07)
4. Refinar doc-readme-0001-readme-canon.md e validar OpenAPI `/docs` (RNF02)
5. Ensaio da apresentação final (30–35 min, 5 integrantes)
6. Code review rubrica R-01..R-07 + aprovação humana + merge em `main`

## 12. Workflow de segurança (sem degradação implemental)

| Etapa | Ação | Ferramenta | Frequência |
|---|---|---|---|
| Pré-commit | Verificar que nenhum segredo está staged | `git diff --cached --name-only \| grep -iE '\config-env-0001-env-example-v1.0\$|secrets/|\.pem$|\.key$'` | Todo commit |
| Pré-push | Rodar `make ci` localmente | config-make-0001-makefile-v1 + GitHub Actions | Todo push |
| PR | Code review rubrica R-01..R-07 | `caveman-review` | Todo PR |
| Merge | Gatekeeper verifica DoD | Checklist Art. 8.4 | Todo merge |
| Sprint | Avaliação recorrente de arquitetura e conformidade | Revisão da Constitution | A cada sprint |
| Release | DPIA/Threat Model revisado (se tocar dados reais) | `docs/auditorias/` | Antes de release com dados reais |

## 13. Sem risco de degradação implemental ou distorção de objetivos

- **Não implementar funcionalidades fora dos 18 RF** sem CR ratificado (Constitution Art. 1.4, 5.4)
- **Não adicionar abstrações "para depois"** (YAGNI, Art. 3.7)
- **Não vazar dependência de framework para o Domain** (Clean Architecture, Art. 3.2)
- **Não usar queries não parameterizadas** (proteção contra SQLi, Art. 7.2)
- **Não usar PII real** em seeds, fixtures, logs (LGPD, Art. 3.5)
- **Não pular CI verde** antes de merge (Art. 8.5)
- **Não commitar `config-env-0001-env-example-v1.0`** ou credenciais (Art. 7.1)
- **Não rodar comandos destrutivos** sem confirmação humana (Art. 13.3 deste plano)

---

# TÍTULO VI — USO DE SKILLS DE PRODUÇÃO UI/UX

## 14. Skills UI/UX a utilizar

### 14.1 `ui-ux-pro-max`
Acionar para:
- Direção de design das telas do frontend (desktop-first ≥1024px)
- Escolha de paleta de cores, tipografia, ícones, componentes visuais
- Acessibilidade e feedback visual (RNF05: toasts, loading skeletons, modais de confirmação)
- Otimização para impressão A4 (RF18: `@media print`, ocultar menus, quebras de página)

### 14.2 `frontend-design`
Acionar para:
- Escolhas estéticas intencionais, não-templatizadas
- Tailwind CSS configuração (`tailwind.config.js`, `postcss.config.js`)
- Layout responsivo apenas para desktop (sem mobile, RNF04)
- Componentes Vanilla JS sem framework pesado

### 14.3 Fluxo de produção UI/UX
1. Acionar `ui-ux-pro-max` para definir direção visual
2. Acionar `frontend-design` para implementar no Tailwind + Vanilla JS
3. Revisar com `caveman-review` (diff review)
4. Validar com `ponytail` (mínimo código, sem over-engineering)

---

# TÍTULO VII — ROTEIRO PARA SESSÕES AUTÔNOMAS (PRÓXIMA SESSÃO)

## 15. Instruções para execução quase autônoma

Em uma nova sessão com rodadas direcionadas, este agente deverá:

### 15.1 Passo 0 — Restaurar contexto
- Ler `constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md` v2.0 (lei suprema)
- Ler `doc-agents-0001-agents-canon.md` (estado do repo e convenções)
- Ler `doc-plan-0001-plano-implementacao-mvp-canon.md` v2.0 (este documento)
- Verificar `git status` e `git log --oneline -5` no repositório local
- Confirmar remote `origin git@github.com:leonardosetti/COBECO.git`

### 15.2 Passo 1 — Escolher a rodada atual
Com base nos marcos S1–S5, identificar qual Sprint está ativa. Prioridade: itens P0 primeiro, depois P1.

### 15.3 Passo 2 — Seguir o fluxo SDD
Para cada tarefa:
1. Verificar se existe spec em `.ai/specs/`; se não, criar a partir de `TEMPLATE-SPEC.md`
2. Verificar se existe handoff em `.ai/handoffs/`; se não, criar `HF-<NNNN>.md`
3. Implementar código seguindo ponytail (mínimo necessário)
4. Criar/atualizar User Story e Tech Debt Log se aplicável
5. Commit com caveman-commit
6. Push e abrir PR
7. Aguardar CI verde e code review

### 15.4 Passo 3 — Não fazer
- Não rodar `docker compose down -v` ou comandos destrutivos
- Não implementar funcionalidades fora dos 18 RF sem CR
- Não commitar `config-env-0001-env-example-v1.0` ou segredos
- Não pular code review ou CI verde
- Não adicionar abstrações desnecessárias

### 15.5 Critério de parada da sessão
- Todos os itens P0 da Sprint atual implementados e testados
- Cobertura ≥80% nos módulos tocados
- `make ci` verde localmente
- PRs revisados e mergados (ou prontos para merge com aprovação humana)

---

# TÍTULO VIII — RISCOS E MITIGAÇÕES

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| `config-env-0001-env-example-v1.0` commitado acidentalmente | Baixa | Crítica | `.gitignore` + verificação pré-commit |
| Regressão em auth (RF01–RF04) | Média | Alta | Testes integration `test_auth_flow.py` + CI |
| Cobertura <80% | Média | Alta | `pytest --cov-fail-under=80` no CI |
| SQLi por query não parameterizada | Baixa | Crítica | Revisão de código + DoD |
| Perda de dados por `down -v` | Baixa | Crítica | Nunca rodar sem confirmação; backup de volume |
| Desvio de escopo (RFs extras) | Média | Média | CR ratificado pelo CCB |
| Stack divergente (doc-readme-0001-readme-canon vs board-roadmap-0001-roadmap-canon) | Baixa | Média | ADR-001 ratificado como fonte única |

---

**Fim do Plano de Implementação — COBECO MVP v2.0**  
*Alinhado com Constitution v2.0 — FATEC Taquaritinga ADS — 13/11/2026*
