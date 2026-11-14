# COBECO - Playwright E2E Test Framework

Framework de testes end-to-end estruturado usando Playwright com Page Object Model (POM).

## Estrutura do Projeto

```
frontend/tests/e2e/
├── pages/              # Page Objects (POM)
│   ├── BasePage.ts     # Classe base com métodos comuns
│   ├── LoginPage.ts    # Página de login
│   ├── CadastroPage.ts # Página de cadastro
│   ├── PerfilPage.ts   # Página de perfil
│   └── ListasPage.ts   # Página de listas/itens
├── fixtures/           # Test fixtures
│   └── test-fixtures.ts # Fixtures compartilhadas (loginPage, cadastroPage, etc.)
├── utils/              # Utilitários e helpers
│   ├── api-helpers.ts  # Helpers para chamadas API diretas
│   └── test-data.ts    # Dados de teste e factories
├── tests/
│   └── crud/           # Suítes de testes CRUD
│       ├── cadastro.spec.ts   # Testes de cadastro (UC01/RF01)
│       ├── auth.spec.ts       # Testes de autenticação (UC01, UC02, UC11, UC12)
│       ├── perfil.spec.ts     # Testes de perfil (UC16, UC18)
│       ├── listas.spec.ts     # Testes de listas (UC03-UC06)
│       ├── itens.spec.ts      # Testes de itens (UC07-UC10)
│       └── index.spec.ts      # Suite agrupadora
├── playwright.config.ts # Configuração do Playwright
├── global-setup.ts      # Setup global (health check)
├── global-teardown.ts   # Teardown global
├── tsconfig.json        # Configuração TypeScript
└── config-npm-0001-config-npm-0001-config-npm-0001-config-npm-0001-package-v1-v1.0-v1.0-v1.0.json         # Dependências e scripts
```

## Page Object Model (POM)

Cada página da aplicação tem uma classe correspondente que encapsula:
- **Seletores** (locators) dos elementos
- **Ações** do usuário (click, fill, navigate)
- **Asserções** específicas da página

### Exemplo de uso:

```typescript
import { test } from '../fixtures/test-fixtures';

test('exemplo de uso do POM', async ({ cadastroPage, loginPage }) => {
  await cadastroPage.goto();
  await cadastroPage.cadastrar(userData);
  
  await loginPage.goto();
  await loginPage.login(userData.nome_usuario, userData.senha);
});
```

## Fixtures

As fixtures fornecem instâncias prontas das Page Objects e dados de teste:

- `loginPage` - Instância de LoginPage
- `cadastroPage` - Instância de CadastroPage
- `perfilPage` - Instância de PerfilPage
- `listasPage` - Instância de ListasPage
- `testUser` - Dados de um usuário de teste único (gerado por timestamp)
- `authenticatedPage` - Página já autenticada (cadastra + loga automaticamente)

## Comandos Disponíveis

```bash
# Instalar dependências e browsers
npm install

# Executar todos os testes
npm test

# Executar testes em modo headed (ver browser)
npm run test:headed

# Abrir UI do Playwright
npm run test:ui

# Debug interativo
npm run test:debug

# Executar apenas testes CRUD
npm run test:crud

# Executar suítes específicas
npm run test:cadastro
npm run test:auth
npm run test:perfil
npm run test:listas
npm run test:itens

# Executar em browser específico
npm run test:chromium
npm run test:firefox
npm run test:webkit

# Ver relatório HTML
npm run report

# Gerar código de teste (codegen)
npm run codegen
```

## Variáveis de Ambiente

```bash
# URL base da aplicação (padrão: http://localhost:8380)
BASE_URL=http://localhost:8380

# Executar em CI
CI=true
```

## Boas Práticas

1. **Use Page Objects** - Nunca acesse seletores diretamente nos testes
2. **Dados únicos** - Use `createTestUser()` e `createListaData()` para gerar dados únicos
3. **Fixtures** - Use `authenticatedPage` para testes que precisam de usuário logado
4. **Asserções explícitas** - Use `waitForToast()` para verificar feedbacks de UI
5. **Limpeza** - As fixtures limpam localStorage/sessionStorage automaticamente

## Estrutura de Testes CRUD

Cada suíte segue o padrão CRUD:

```
CREATE - Testes de criação/registro
READ   - Testes de leitura/visualização
UPDATE - Testes de atualização/edição
DELETE - Testes de exclusão/remoção
```

## Integração com CI/CD

O pipeline GitHub Actions executa:
1. `npm run install` - Instala browsers
2. `npm run test:ci` - Executa testes com reporter de linha
3. Publica relatório HTML como artifact

## Adicionando Novos Testes

1. Crie/atualize Page Object em `pages/`
2. Adicione helpers em `utils/` se necessário
3. Crie arquivo de teste em `tests/crud/`
4. Use fixtures de `test-fixtures.ts`
5. Siga o padrão CRUD nas descrições

## Troubleshooting

### Testes flaky
- Aumente timeouts em `playwright.config.ts`
- Use `waitForLoadState('networkidle')` após navegações
- Verifique se elementos estão visíveis antes de interagir

### Falha de autenticação
- Verifique se `authenticatedPage` está sendo usado
- Confirme que o backend está rodando (`docker compose up -d`)
- Verifique logs do container `cobeco-backend`

### Porta ocupada
```bash
# Matar processos na porta 8380
lsof -ti:8380 | xargs kill -9
```