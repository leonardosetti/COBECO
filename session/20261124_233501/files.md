# Files

## Inspected
- doc-prototype-0003-prototype-high-v2-v1.0.html - protótipo alta fidelidade v3.2
- frontend/src/app.js - views do frontend (reatas escritas + correção de cobertura + busca full-text)
- frontend/src/styles/prototype.css - CSS extraído do protótipo (não alterado)
- frontend/src/index.html - shell HTML (não alterado)
- backend/src/adapters/api/catalogo.py - router de catálogo (endpoint disponibilidade-lote + busca semântica categorias + autocomplete full-text)
- backend/src/adapters/api/produtos.py - router de produtos (autocomplete full-text com score de relevância)
- backend/src/adapters/api/listas.py - router de listas (busca de listas via FULLTEXT em vez de ilike)
- backend/src/adapters/db/models.py - modelos do banco (Índice FULLTEXT ft_produto_nome)
- backend/src/domain/entities.py - entidades (UnidadeMedida expande com G e ML)
- backend/src/domain/repositories.py - interfaces de repositório
- backend/src/domain/usecases.py - casos de uso (RF/UC mapeados)
- backend/config-seed-0001-seed-v1.0.sql - seed SQL (regenerado com Livros→Extra)
- backend/scripts/script-seed-0001-generate-seed-v1.0.py - gerador SQL baseline
- backend/scripts/script-seed-0002-seed-data-v1.0.py - fonte canônica (_UNIT_PATTERN aceita g/ml)
- backend/scripts/script-seed-0003-prototype-seed-v1.0.py - seed protótipo DOC-03
- backend/scripts/script-seed-0004-realistic-seed-data.py - gerador de dados realistas (perfis realistico/expandido)
- backend/scripts/script-seed-0005-generate-realistic-seed.py - gerador SQL idempotente realista
- backend/tests/unit/test_seed_data.py - testes de seed (7 passed)
- backend/alembic/versions/0007_add_fulltext_indices.py - NOVO: migração índices FULLTEXT
- backend/decisoes/doc-adr-0001-stack-decision-v1.0.md - ADR stack
- backend/decisoes/doc-adr-0002-busca-fulltext-v1.0.md - NOVO: ADR busca full-text
- docs/bugs/bug-0001-cobertura-fornecedores-zero.md - NOVO: registro do bug
- req-func-0001, doc-arch-0001, constitution-0001, doc-analysis-0001 - documentos canônicos

## Changed
- frontend/src/app.js - 6 views reescritas + carregarCoberturaFornecedores() + state.coberturaPorFornecedor +
  ApiClient.buscarProdutos() + updateSugestoes consome API full-text com exibição de % relevância
- backend/src/adapters/api/catalogo.py - novo endpoint GET /fornecedores/disponibilidade-lote + autocomplete full-text
- backend/src/adapters/api/listas.py - busca de listas usa MATCH/AGAINST BOOLEAN MODE em vez de ilike; autocomplete full-text
- backend/src/adapters/api/produtos.py - campo relevancia em respostas; autocomplete ordenado por relevância sem LIKE
- backend/scripts/script-seed-0002-seed-data-v1.0.py - _UNIT_PATTERN aceita g/ml
- backend/scripts/script-seed-0003-prototype-seed-v1.0.py - Extra cats [1,2,11] → [1,2,9,11]
- backend/config-seed-0001-seed-v1.0.sql - regenerado com Livros→Extra (26 relações)
- backend/src/domain/entities.py - UnidadeMedida expande com G (g) e ML (ml)
- backend/alembic/versions/0007_add_fulltext_indices.py - NOVO: índices FULLTEXT em produtos.marca, listas.nome, produto_classes.termos_busca_texto, produto_classes.marcas_referencia_texto

## Added (novos arquivos)
- backend/scripts/script-seed-0004-realistic-seed-data.py - gerador de dados realistas (perfis realistico/expandido)
- backend/scripts/script-seed-0005-generate-realistic-seed.py - gerador SQL idempotente realista
- docs/decisoes/doc-adr-0002-busca-fulltext-v1.0.md - ADR-0002 busca full-text search
- docs/bugs/bug-0001-cobertura-fornecedores-zero.md - registro formal do BUG-0001

## Generated (não commitados)
- /tmp/0007_add_fulltext_indices.py - cópia da migration
- /tmp/apply_ft.sql - SQL para colunas de texto em produto_classes (aplicado no banco)
- /tmp/apply_ft2.sql - SQL para colunas normais em produto_classes (aplicado no banco)
- /tmp/apply_triggers.sql - SQL para triggers (não aplicado, falta privilégio SUPER)
- /tmp/seed-realistico.sql - SQL perfil realistico (aplicado no banco dev, depois sobrescrito por expandido)
- /tmp/seed-expandido.sql - SQL perfil expandido (aplicado no banco dev)
- session/20261124_233501/ - checkpoint desta sessão (nemo-rl-session-memory)

## Commits
- db610a0: feat(UI) adequa frontend ao protótipo v3.2 + fix(seed) Livros órfã + perfil semantica
- d464fb8: fix(seed) corrigir cobertura de fornecedores na tela de seleção (RF12-RF16)
- b4b29a1: docs(bug) registra BUG-0001 cobertura de fornecedores zero
- e66b847: feat(seed) seed realista e massivo com preços variáveis por fornecedor
- 46e0552: feat(requisito) ativa busca Full-Text Search com tokenização e relevância
- 8f4878e: feat(busca) remove LIKE, expande Full-Text Search para listas e comparações

## Banco dev (estado final)
- 50 categorias, 100 fornecedores, 681 produtos, 3.276 preços, 330 relações N:N (seed expandido aplicado)
- Preços variáveis por fornecedor confirmados via API
- Índices FULLTEXT aplicados: produtos.marca, listas.nome, produto_classes.termos_busca_texto, produto_classes.marcas_referencia_texto

## Performance (RNF09 — p95 <500ms) — CUMPRIDA
- 3 rodadas: p95 máximo 7ms (limite 500ms)
