# Timeline

## 2026-11-24 23:35
- Checkpoint inicial criado

## 2026-11-24 23:50 (retomada)
- User pediu "Prossiga!"

## 2026-11-24 23:50-23:55
- Corrigido categoria 9 (Livros) órfã + criado perfil "semantica" de seed
- Commit db610a0

## 2026-11-25 00:08-00:10
- Stack reiniciado, seed semantica aplicado, validação RF12-RF16 ao vivo via API

## 2026-11-25 00:20-00:30
- Identificada falha crítica: todos os fornecedores apareciam com 0% de cobertura na tela de seleção
- Causa raiz: coberturaDe() dependia de state.resultado (só populado após calcular)
- Backend: endpoint GET /v1/catalogo/fornecedores/disponibilidade-lote
- Frontend: carregarCoberturaFornecedores(), state.coberturaPorFornecedor, uso do mapa
- E2E validado com sucesso via crawler (navegador real)
- Commit d464fb8

## 2026-11-25 00:30-00:45
- BUG-0001 registrado em docs/bugs/bug-0001-cobertura-fornecedores-zero.md
- Commit b4b29a1

## 2026-11-25 00:45-01:00
- User pediu seed realista massivo com preços variáveis por fornecedor
- Verificada estrutura: fornecedores_produtos já suporta preço por fornecedor-produto (PK composta)
- Criado script-seed-0004-realistic-seed-data.py (perfis realistico/expandido)
- Criado script-seed-0005-generate-realistic-seed.py (gerador SQL idempotente)
- Entidade UnidadeMedida expande com G (g) e ML (ml)
- _UNIT_PATTERN aceita g e ml
- CNPJs duplicados corrigidos (Americanas: 77666555)
- Commit e66b847

## 2026-11-25 01:00-01:05
- Seed expandido aplicado no banco dev: 50 cat, 100 forn, 681 prod, 3.276 preços, 330 relações
- 3 rodadas de testes de performance (RNF09 p95 <500ms): p95 máximo 7ms
- RNF09 CUMPRIDO

## 2026-11-25 01:15-01:30
- User pediu ativar requisito de busca Full-Text Search com tokenização e relevância
- Criado ADR-0002: docs/decisoes/doc-adr-0002-busca-fulltext-v1.0.md (RF07, RF20, UC02; RNF06, RNF09)
- Backend (produtos.py): endpoint /v1/produtos/autocomplete retorna score de relevância (MATCH/AGAINST BOOLEAN MODE), ordenado por relevância decrescente
- Frontend (app.js): autocomplete de produtos consome API de busca full-text (ApiClient.buscarProdutos) em vez de filtro local; exibe % de relevância por resultado com fallback para busca local se API falhar
- Commit 46e0552

## 2026-11-26 00:30 (fase atual)
- User pediu expandir técnica de full-text search para buscas de listas e comparações, remover todas as buscas por LIKE
- Migração 0007: índices FULLTEXT em produtos.marca, listas.nome, produto_classes.termos_busca_texto, produto_classes.marcas_referencia_texto
- backend/src/adapters/api/produtos.py: autocomplete usa FULLTEXT para nome, marca e expansão semântica (produto_classes), sem LIKE
- backend/src/adapters/api/catalogo.py: autocomplete de produtos usa FULLTEXT com score de relevância
- backend/src/adapters/api/listas.py: busca de listas (listar_por_usuario) usa MATCH/AGAINST BOOLEAN MODE em vez de ilike
- Migration 0007 reescrita com colunas normais (não virtuais, MySQL 8 não suporta FULLTEXT em virtuais) + UPDATE para popular + índices FULLTEXT
- Colunas termos_busca_texto e marcas_referencia_texto populadas via UPDATE a partir do JSON existente
- Commit 8f4878e
- Sintaxe JS e Python OK

## 2026-11-26 00:45 (final)
- session_state.md, timeline.md, files.md, handoff.md atualizados. Sessão concluída.
