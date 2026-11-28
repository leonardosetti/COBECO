# Handoff

## Resume From Here
Sessão com dois blocos concluídos: (A) registro de 9 bugs no GitHub (#81-89) + `docs/bugs/BUG_TRACKER.md` (nenhum fix aplicado, apenas registro/documentação); (B) implementação da jornada efêmera COBECO (RF22-RF28) já commitada em HEAD `bdfca6d` (branch `fix/bug-007-irrelevant-products`): navbar fixa com link Início (RF24), pré-filtro de grandes áreas multi-seleção + backend `GET /catalogo/areas-grandes` e `?areas=` (RF27/RF28), busca semântica não oculta selecionadas (RF26), modal "Esquecer lista em andamento? Sim/Não" (RF25), retorno ao início após exportar PDF com rascunho → `gerada`/`historico` em `sessionStorage` (RF22/RF23). Protótipos HTML 0003/0004 atualizados. 5 testes E2E novos (jornada-efemera.spec.ts) e suite completa (17 passed, 1 skipped) validados contra stack real. Nenhum arquivo rastreado pendente de commit.

## Next Actions
- [ ] Revisar `specs-jornada-efemera-v3.4.md` com o time (adendo ao SPECS v3.3, implementação já feita)
- [ ] Opcional: incorporar arquivos untracked relevantes ao checkpoint de entrega
- [ ] Aguardar análise humana dos 9 bugs (bug tracker) — P0 primeiro (BUG-001, 002, 007, 008)
- [ ] BUG-000 (#89): executar teste manual para fechar (fix `d464fb8` já commitado)

## Watch Outs
- Issues #87 (BUG-001) e #88 (BUG-002) criados via heredoc (escaping no JSON pipeline)
- BUG-000 permanece ABERTO até teste manual validado
- Seed real tem 50 categorias (não 11 do SPECS v3.3); AREAS_GRANDES mapeado aos nomes reais
- CATEGORIA_GATILHOS e AREAS_GRANDES hardcoded em `catalogo.py` — migrar para DB quando >20 categorias
- Frontend usa full render (innerHTML) causando perda de foco (BUG-003) — refator para DOM parciais recomendada
- `produto_classes` tabela vazia (BUG-004)
- Arquivos untracked não commitados: `docs/bugs/BUG_TRACKER.md`, `docker-compose-minimal/simple.yml`, `frontend/src/assets/`, `github_issues*.json`, `req-func-0002-*.md`, `backend/tests/unit/adapters/`, `session/`