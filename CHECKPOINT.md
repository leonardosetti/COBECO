# CHECKPOINT — Sessão COBECO (2026-11-27)

## Contexto
Projeto COBECO (FATEC / lab_eng_software). Backend Python + SQLAlchemy Async + MySQL 8.

## O que foi feito
1. Mapeado o banco: 10 tabelas via ORM em `backend/src/adapters/db/models.py`.
2. Criado `backend/scripts/dump_and_reset.py` — dump JSON de todas as tabelas + reset (DELETE ordenado ou TRUNCATE). Ainda não executado.
3. Criado `backend/scripts/pre_seed.csv` — CSV único de pré-seed (desnormalizado, 52 linhas produto×fornecedor) com colunas:
   produto_id, produto_nome, marca, categoria, categoria_macro, unidade, ativo_produto, fornecedor_id, fornecedor_nome, fornecedor_cnpj, fornecedor_ativo, atende_categoria, preco, estoque, disponivel.
   Base para scraping posterior de produtos/marcas/fornecedores.
4. Criado `backend/scripts/gerar_seed_csv.py` — lê o CSV e gera `backend/seed_from_csv.sql` idempotente com:
   - equalização: `fornecedores_produtos` apenas quando `atende_categoria = S` (nem todo produto em todo fornecedor);
   - flag de estoque: `fornecedores_produtos.ativo = (disponivel == 'S')`, `estoque = 0` quando indisponível;
   - `fornecedores_categorias` derivado da igualdade categoria-fornecedor.
   Resultado gerado: 11 categorias, 10 fornecedores, 20 produtos, 18 relações fc, 52 fp.
5. `backend/seed_from_csv.sql` gerado e validado.

## Arquivos novos
- backend/scripts/dump_and_reset.py
- backend/scripts/pre_seed.csv
- backend/scripts/gerar_seed_csv.py
- backend/seed_from_csv.sql (gerado)

## Próximos passos possíveis
A. Executar dump contra MySQL: `cd backend && python scripts/dump_and_reset.py --mode dump`
B. Executar reset: `cd backend && python scripts/dump_and_reset.py --mode reset` (ou `--mode truncate`)
C. Aplicar seed: `seed_from_csv.sql` (ou `seed.sql`) no MySQL
D. Enriquecer o CSV com scraping e regenerar o seed

## Observações
- Ordem de DELETE/TRUNCATE respeita FKs (filhos primeiro).
- Precisa de MySQL rodando e acessível via `DATABASE_URL` no `.env`.
