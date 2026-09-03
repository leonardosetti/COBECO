---
name: rodar-cobeco
description: Sobe o COBECO localmente (PostgreSQL, API e web) e dirige o fluxo de cotação por paridade. Use quando pedirem para rodar, iniciar, testar ou tirar screenshot da aplicação COBECO.
---

# Rodar o COBECO

`npm run dev` sozinho **não** sobe o projeto. A API inicia e `/health` responde, mas todo
endpoint devolve HTTP 500 com `Can't reach database server at localhost:5432`, porque desde a
migration `005_catalog_parity` a aplicação usa Prisma/PostgreSQL de verdade — repositórios em
memória só são usados quando `NODE_ENV=test` ou `VITEST` está definido.

Todos os caminhos abaixo são relativos a `COBECO/` (o monorepo fica nessa subpasta).

## Sequência de subida

```bash
# 1. Docker Desktop precisa estar rodando. Se "docker info" falhar:
#    Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
#    e aguarde ate "docker info" responder.

# 2. Banco
docker compose up -d postgres
docker exec cobeco-postgres pg_isready -U cobeco_user -d cobeco   # aguarde ficar pronto

# 3. Schema e dados (DATABASE_URL ja esta em apps/api/.env)
npx prisma migrate deploy --schema apps/api/prisma/schema.prisma
npm run db:seed        # imprime "Seed concluido: catalogo A-J (10 fornecedores, 50 produtos)..."

# 4. Aplicacao
npm run dev            # sobe API e web juntas
```

| Serviço | Endereço |
|---|---|
| Web (Vite) | http://localhost:5173 |
| API (Express) | http://localhost:3333 |
| PostgreSQL | container `cobeco-postgres` :5432 |

## Armadilhas conhecidas

- **`prisma generate` falha com `EPERM`** se a API estiver rodando — o processo trava
  `query_engine-windows.dll.node`. Pare a API antes de gerar o client.
- **`/docs` abre em branco.** O helmet aplica `script-src 'self'` e a página carrega o Swagger
  UI do unpkg.com, que é bloqueado pela CSP. O `/openapi.yaml` funciona normalmente.
- **Cadastro exige `consent: true`** no corpo — sem ele, HTTP 400 (LGPD).
- **Login tem rate limit de 5 tentativas por 15 minutos por IP** (RNF13). Ao depurar auth
  em sequência, o 6º pedido volta HTTP 429; reaproveite o token em vez de relogar.
- **O sign-up não devolve token**, só o usuário. O `accessToken` vem do `POST /auth/login`;
  o refresh token vem em cookie httpOnly.

## Dirigir o fluxo pela API

```bash
# cadastro -> login -> catalogo -> lista -> cotacao
# a senha exige maiuscula, minuscula, numero E caractere especial (RF01)
curl -s -X POST localhost:3333/api/auth/sign-up -H "Content-Type: application/json" \
  -d '{"name":"Teste","username":"teste1","email":"t1@cobeco.local","password":"SenhaForte123!","consent":true}'

# identifier aceita e-mail ou username (RF02); "email" ainda funciona
curl -s -X POST localhost:3333/api/auth/login -H "Content-Type: application/json" \
  -d '{"identifier":"teste1","password":"SenhaForte123!"}'      # copie o accessToken

curl -s localhost:3333/api/platform/categories -H "Authorization: Bearer $TOKEN"
curl -s "localhost:3333/api/platform/categories/$CAT/products" -H "Authorization: Bearer $TOKEN"

# disponibilidade de cada fornecedor para a lista (RF12), usada na tela de selecao
curl -s "localhost:3333/api/platform/lists/$LIST/suppliers" -H "Authorization: Bearer $TOKEN"

# cotar: supplierIds[] e obrigatorio, de 2 a 10 fornecedores (RF11)
curl -s -X POST "localhost:3333/api/platform/lists/$LIST/quote" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"supplierIds":["supplier-a","supplier-b"]}'
```

A resposta da cotação traz `groups`, `bestGroupId` e `meta`. O seed tem 10 fornecedores
(A–J) e 50 produtos (RNF09), mas o canário de regressão continua sendo o cenário da seção
7.3 do documento de concepção: **selecionando apenas A–H sobre os produtos 1 a 9**, o
agrupamento correto é **A,B / C,E,F,H / D / G**. Se divergir disso, o motor de paridade
regrediu.

## Dirigir a interface

Rode o E2E que já existe, que cobre cadastro, login, lista e cotação:

```bash
npx playwright test --config apps/web/playwright.config.ts --reporter=list
```

Para screenshots, use o Playwright do próprio projeto. Em um `.mjs` fora do repo, importe pelo
caminho absoluto (é CommonJS, então use o default import):

```js
import pw from 'file:///C:/.../COBECO/node_modules/@playwright/test/index.js';
const { chromium } = pw;
```

Seletores que funcionam (evite `getByLabel`, que colide com o checkbox de consentimento):

| Elemento | Seletor |
|---|---|
| Nome no cadastro | `#field-nome` |
| Nome de usuário | `#field-nome-de-usuário` |
| E-mail/username no login | `#field-e-mail-ou-nome-de-usuário` |
| Consentimento | `#consent` |
| Nova lista | `#new-list` + botão `Criar lista` (aria-label) |
| Itens em lote | `#bulk` + botão `Adicionar linhas` |
| Cotar | botão `Cotar lista completa` |

Rotas do front: `/`, `/sign-up`, `/login`, `/platform`, `/platform/history`.
Não existe `/cadastro` — a rota inexistente cai na landing pelo `path="*"`.

## Testes

```bash
npm test --workspaces --if-present   # 49 testes (47 API + 2 web)
npm run test:bdd --workspace apps/api
npm run test:e2e --workspace apps/web
```
