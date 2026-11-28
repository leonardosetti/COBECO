# Files

## Inspected
- req-func-0001-requisitos-funcionais-canon.md - requisitos funcionais canon (RF01-RF18, RNF01-RNF12)
- SPECS.md - especificacao consolidada v3.3 (SSOT)
- backend/src/adapters/api/catalogo.py - router de catálogo (categorias, fornecedores, produtos, disponibilidade-lote)
- backend/src/adapters/api/comparacao.py - router de comparacao (calcular orçamenteo RF15/RF16)
- backend/src/adapters/api/listas.py - router de listas (RF07-RF11)
- backend/src/domain/repositories.py - interfaces de repositório (clean architecture)
- backend/src/domain/usecases.py - casos de uso (RF/UC mapeados)
- frontend/src/app.js - views do frontend (Passos 1-5, cobertura, slider, busca produtos)
- backend/tests/unit/ - suíte de teste unitária (146 testes preexistentes)

## Changed
- backend/src/adapters/api/catalogo.py:
  * CategoriaRepositoryImpl.buscar_por_termo() (busca por nome ILIKE + mapa CATEGORIA_GATILHOS)
  * ProdutoRepositoryImpl.listar_por_categorias() (RF19: produtos derivados de fornecedor<->categoria + fornecedor<->produto)
  * GET /catalogo/categorias/busca?q= (RF20) com schema CategoriaBuscaResponse (match_por: nome|sinonimo)
  * GET /catalogo/produtos?categorias= (RF19)
- backend/src/domain/repositories.py:
  * ProdutoRepository.listar_por_categorias (interface)
  * CategoriaRepository.buscar_por_termo (interface)
- frontend/src/app.js:
  * RF14: fornecedoresElegiveis (omite cobertura 0% e abaixo do piso), fornCardsHTML (sem cards 0%), refreshFornecedores (re-filtra selecao), ApiClient.buscarCategorias, carregarProdutos(categorias)
  * RF19/RF20: estado categoriasVisiveis, categoriaBusca, campo busca-cat, buscarCategoriasUI(), recarrega produtos ao ir para Lista

## Added (novos arquivos)
- backend/tests/unit/adapters/test_catalogo_busca.py - testes RF19/RF20 (7 testes)
- req-func-0002-requisitos-cobertura-categorias-semantica.md - requisitos RF14 (alterado), RF19, RF20, RF21 + rodadas de implementacao
- session/20261125_150000/ - checkpoint desta sessao (nao commitar)

## Generated (não commitados)
- session/20261125_150000/ - checkpoint desta sessao

## Banco dev (estado final - sessao anterior 20261124_233501)
- 50 categorias, 100 fornecedores, 681 produtos, 3.276 preços, 330 relações N:N (seed expandido aplicado)
- Preços variáveis por fornecedor confirmados via API

## Commits da sessao anterior (referencia)
- db610a0, d464fb8, b4b29a1, e66b847 (ja commitados em main)
