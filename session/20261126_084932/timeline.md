# Timeline

## 2026-11-26 08:49:32
- User asked: Registrar 8 bugs no GitHub e fazer checkpoint da sessão
- Context gathered: Explorado codebase completo (backend FastAPI, frontend Vanilla JS, seed data, models)
- Decision: Usar GitHub CLI para criar issues com labels corretas do repo
- Result: 8 issues criados (#81-88) com RCA, severidade, prioridade, traceabilidade, logs, screenshots, evidências

## 2026-11-26 08:50:00
- Verified bugs 1-8 no código:
  - BUG-001: auth.py endpoint cadastrar sem login automático + frontend sem handler submit
  - BUG-002: frontend data-action="salvar-lista" sem handler no dispatch + backend requer auth
  - BUG-003: buscarCategoriasUI() chama render() full DOM rebuild perdendo foco do input
  - BUG-004: CATEGORIA_GATILHOS incompleto (11/25), produto_classes tabela vazia
  - BUG-005: vCategorias grid simples sem tabs/accordions, CSS Grid ausente
  - BUG-006: AREAS_GRANDES nomes não batem com seed (25 categorias reais vs hardcoded)
  - BUG-007: listar_por_categorias JOIN via fornecedores traz tudo do fornecedor (BigSellers)
  - BUG-008: Frontend multiplica corretamente mas backend comparacao.py/exportacao.py pendente verificação

## 2026-11-26 08:52:00
- Created github_issues_fixed.json com 8 issues estruturados
- Tentativa via jq pipeline falhou para BUG-001 e BUG-002 (escaping)
- Criados BUG-003 a BUG-008 via pipeline (#81-86)
- Criados BUG-001 e BUG-002 individualmente via heredoc (#87, #88)

## 2026-11-26 08:54:00
- Validado: gh issue list mostra 8 issues abertos com labels corretas
- Labels aplicadas: bug, tipo: bug, P0/P1/P2, camada: backend/frontend/database
- Checkpoint session iniciado

## 2026-11-26 09:00:00
- Review solicitado: descrições quebradas no GitHub (newlines literais `n`)
- Identificado BUG-0001 existente em `docs/bugs/bug-0001-cobertura-fornecedores-zero.md` (commit `d464fb8`, severidade 3.75/Alta, impacto 3.25/Alto, status ABERTO aguardando teste manual)
- Corrigidos todos os 8 issues GitHub via `gh issue edit --body-file` com markdown sanitizado
- Criado documento consolidado normalizado `docs/bugs/BUG_TRACKER.md` com sumário, métricas, rastreabilidade
- Checkpoint atualizado com 9 bugs totais (BUG-0001 + 8 novos)

## 2026-11-26 09:15:00
- Criado GitHub issue #89 para BUG-0001 normalizado como **BUG-000** (padrão BUG-00X)
- Issue inclui: severidade 3.75/Alta, impacto 3.25/Alto, prioridade Alta, RCA completo, logs E2E, screenshots, evidências código, plano de teste manual
- Labels aplicadas: bug, tipo: bug, P1, camada: frontend, camada: backend
- `docs/bugs/BUG_TRACKER.md` atualizado: ID normalizado, métricas ajustadas (P1=4, Severidade Alta=5)

## 2026-11-26 11:00:00
- User asked: implementar jornada efêmera (RF22-RF28) + verificar checkpoint + atualizar memória nemo
- Context gathered: SPECS v3.3 (SSOT), frontend/src/app.js, backend catalogo.py/comparacao.py, frontend index.html, prototypes 0003/0004
- Decision: adendo specs-jornada-efemera-v3.4.md (não tocar SSOT); mínima alteração no frontend; backend sem nova migração
- Result: RF22-RF28 implementados e commitados (3bf26c8, 65d5998, 0177128, b36a8e4, bdfca6d)

## 2026-11-26 11:30:00
- E2E Playwright contra stack real (localhost:8380): 5 novos testes em jornada-efemera.spec.ts — todos passam
- Suite completa: 17 passed, 1 skipped (pré-existente). Sem regressão.

## 2026-11-26 11:50:00
- Protótipos HTML 0003 e 0004 atualizados (bdfca6d); JS sintaxe OK em ambos
- Checkpoint verificado: HEAD=bdfca6d, sem arquivos rastreados pendentes de commit, branch=fix/bug-007-irrelevant-products
- Memória nemo sincronizada (este arquivo)