# Session State

- Session: 20261124_233501
- Repo: /lab/FATEC/202602/lab_eng_software/COBECO
- Branch: main
- Started: 2026-11-24 23:35
- Updated: 2026-11-26 01:45

## Goal
Adequar UI ao protótipo doc-prototype-0003 v3.2, subir containers, validar camada de dados, corrigir falha de cobertura de fornecedores, criar seed realista massivo com preços variáveis por fornecedor, validar performance (RNF09 p95 <500ms), ativar busca Full-Text Search com tokenização e relevância, e EXPANDIR FULL-TEXT SEARCH para buscas de listas e comparações, removendo todas as buscas por LIKE.

## Current Subtask
TODAS AS TAREFAS CONCLUÍDAS.

## Loaded Skills
- nemo-rl-session-memory - checkpoint de sessão durável.

## Current Status
- UI adequada ao protótipo v3.2: 6 views reescritas em frontend/src/app.js. COMMITADO em db610a0.
- Containers UP/healthy na porta 8380 (proxy).
- Banco dev com seed expandido aplicado (50 cat, 100 forn, 681 produtos, 3.276 preços, 330 relações N:N).
- Correção I1 (Livros órfã) COMMITADA em db610a0.
- Perfil "semantica" de seed COMMITADO em db610a0.
- Falha crítica de cobertura CORRIGIDA e COMMITADA em d464fb8.
- BUG-0001 registrado e COMMITADO em b4b29a1 (docs/bugs/).
- Seed realista massivo CRIADO e COMMITADO em e66b847.
- Performance RNF09 CUMPRIDA: p95 máximo 7ms em 3 rodadas.
- REQUISITO DE BUSCA FULL-TEXT SEARCH ATIVADO e COMMITADO em 46e0552:
  * ADR-0002: docs/decisoes/doc-adr-0002-busca-fulltext-v1.0.md (RF07, RF20, UC02; RNF06, RNF09)
  * Backend: endpoint /v1/catalogo/produtos/autocomplete retorna score de relevância (MATCH/AGAINST BOOLEAN MODE), ordenado por relevância decrescente
  * Frontend: autocomplete de produtos consome API de busca full-text (ApiClient.buscarProdutos) em vez de filtro local; exibe % de relevância por resultado
- FULL-TEXT SEARCH EXPANDIDO para listas e comparações, TODOS os LIKE removidos, COMMITADO em 8f4878e:
  * Migration 0007: índices FULLTEXT em produtos.marca, listas.nome, produto_classes.termos_busca_texto, produto_classes.marcas_referencia_texto
  * backend/src/adapters/api/produtos.py: autocomplete usa FULLTEXT para nome, marca e expansão semântica (produto_classes), sem LIKE
  * backend/src/adapters/api/catalogo.py: autocomplete de produtos usa FULLTEXT com score de relevância
  * backend/src/adapters/api/listas.py: busca de listas (listar_por_usuario) usa MATCH/AGAINST BOOLEAN MODE em vez de ilike
  * backend/alembic/versions/0007_add_fulltext_indices.py: migration reescrita com colunas normais (não virtuais) + UPDATE para popular + índices FULLTEXT
  * Índices aplicados no banco dev via SQL direto (alembic não roda por falta de variáveis de ambiente)
  * Colunas termos_busca_texto e marcas_referencia_texto populadas via UPDATE a partir do JSON existente
- NORMALIZAÇÃO DE DADOS CONCLUÍDA:
  * Tabela auxiliar marcas criada com 190 marcas reais
  * Todos os 166 produtos ativos têm marca real (zero genéricos)
  * Produtos com nomes reais e quantificações: "Arroz Tipo 1 5kg", "Sabão em Pó OMO 1kg", "Lâmpada LED Ericsson 50w", "Vaso Plástico Cinza 50cm", etc.
  * Unidades de medida: un, kg, L, m, g, ml

## Commits (6 total)
- db610a0: feat(UI) adequa frontend ao protótipo v3.2 + fix(seed) Livros órfã + perfil semantica
- d464fb8: fix(seed) corrigir cobertura de fornecedores na tela de seleção (RF12-RF16)
- b4b29a1: docs(bug) registra BUG-0001 cobertura de fornecedores zero
- e66b847: feat(seed) seed realista e massivo com preços variáveis por fornecedor
- 46e0552: feat(requisito) ativa busca Full-Text Search com tokenização e relevância
- 8f4878e: feat(busca) remove LIKE, expande Full-Text Search para listas e comparações

## Plan
- Nenhum. Todas as tarefas concluídas.

## Assumptions
- Banco dev roda com seed expandido aplicado (166 produtos ativos após normalização)
- Testes unitários exigem PYTHONPATH=backend
- Alembic não roda no container (falta variáveis de ambiente), migrações aplicadas via SQL direto

## Blockers
- Nenhum.
