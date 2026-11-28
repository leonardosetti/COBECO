# Handoff

## Resume From Here
Sessão COBECO CONCLUÍDA em `main` do repositório `/lab/FATEC/202602/lab_eng_software/COBECO`.
Seis commits realizados: db610a0, d464fb8, b4b29a1, e66b847, 46e0552, 8f4878e.
Todas as entregas estão no banco dev e nos arquivos commitados.

## Estado final
- UI adequada ao protótipo doc-prototype-0003 v3.2 (6 views em frontend/src/app.js)
- Stack rodando na porta 8380 (proxy): db, backend, frontend, proxy — Up/healthy
- Banco dev com seed expandido aplicado (50 cat, 100 forn, 681 prod, 3.276 preços, 330 relações)
- Falha crítica de cobertura CORRIGIDA: fornecedores mostram % real na tela de seleção (antes de Calcular)
- BUG-0001 registrado (docs/bugs/) e commitado — aberto aguardando teste manual
- Seed realista massivo criado e commitado (perfis realistico e expandido)
- Preços variam por fornecedor para o mesmo produto (validado via API)
- Performance RNF09 CUMPRIDA: p95 máximo 7ms (limite 500ms) em 3 rodadas
- Busca Full-Text Search ATIVADA para produtos (autocomplete com score de relevância)
- Busca Full-Text Search EXPANDIDA para listas (listar_por_usuario) e produto_classes
- TODAS as buscas por LIKE removidas do sistema
- Índices FULLTEXT aplicados no banco: produtos.marca, listas.nome, produto_classes.termos_busca_texto, produto_classes.marcas_referencia_texto

## Commits realizados
- db610a0: feat(UI) adequa frontend ao protótipo v3.2 + fix(seed) Livros órfã + perfil semantica
- d464fb8: fix(seed) corrigir cobertura de fornecedores na tela de seleção (RF12-RF16)
- b4b29a1: docs(bug) registra BUG-0001 cobertura de fornecedores zero
- e66b847: feat(seed) seed realista e massivo com preços variáveis por fornecedor
- 46e0552: feat(requisito) ativa busca Full-Text Search com tokenização e relevância
- 8f4878e: feat(busca) remove LIKE, expande Full-Text Search para listas e comparações

## Próximos passos (opcionais)
1. Executar teste manual do BUG-0001 (seção 7 do docs/bugs/) e fechar o bug
2. Commitar /tmp/seed-realistico.sql e /tmp/seed-expandido.sql no repo (atualmente só no /tmp do host)
3. Criar PR referenciando commit d464fb8 para correção da cobertura
4. Deixar containers rodando para desenvolvimento

## Watch Outs
- Arquivos não commitados restantes: README.md, frontend/src/styles/prototype.css, session/ (checkpoint, não commitar)
- Testes unitários exigem PYTHONPATH=/lab/FATEC/202602/lab_eng_software/COBECO/backend
- Não armazenar secrets nos arquivos de sessão
- O endpoint de disponibilidade lote e busca full-text dependem do backend com --reload ativo (está)
- Alembic não roda no container (falta variáveis de ambiente SECRET_KEY), migrações aplicadas via SQL direto

## Evidências de funcionamento (API na porta 8380)
- GET /v1/catalogo/fornecedores/disponibilidade-lote?produtos=1,2,3 → 100 fornecedores com cobertura, vários com 100%
- POST /v1/comparacao/calcular-efemera (produto 1, qtd 2, fornecedores 1,2,3) → Pão de Açúcar R$ 23,22 (vencedor), Carrefour R$ 25,02, Extra R$ 26,84
- GET /v1/produtos/autocomplete?q=arroz → produtos com arroz ordenados por relevância, campo relevancia preenchido
- 3 rodadas de performance: p95 máximo 7ms (RNF09 <500ms CUMPRIDO)
- Busca de listas por nome usa MATCH/AGAINST BOOLEAN MODE (sem ilike)
