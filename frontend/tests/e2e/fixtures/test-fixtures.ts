import { test as base, Page } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';
import { CadastroPage, CadastroData } from '../pages/CadastroPage';
import { PerfilPage } from '../pages/PerfilPage';
import { ListasPage } from '../pages/ListasPage';

interface TestFixtures {
  loginPage: LoginPage;
  cadastroPage: CadastroPage;
  perfilPage: PerfilPage;
  listasPage: ListasPage;
  authenticatedPage: Page;
  testUser: CadastroData;
}

export const test = base.extend<TestFixtures>({
  loginPage: async ({ page }, use) => {
    const loginPage = new LoginPage(page);
    await use(loginPage);
  },

  cadastroPage: async ({ page }, use) => {
    const cadastroPage = new CadastroPage(page);
    await use(cadastroPage);
  },

  perfilPage: async ({ page }, use) => {
    const perfilPage = new PerfilPage(page);
    await use(perfilPage);
  },

  listasPage: async ({ page }, use) => {
    const listasPage = new ListasPage(page);
    await use(listasPage);
  },

  testUser: async ({}, use) => {
    const timestamp = Date.now();
    const user: CadastroData = {
      nome_usuario: `testuser_${timestamp}`,
      email: `test_${timestamp}@example.com`,
      nome: `Test User ${timestamp}`,
      senha: 'Senha@123',
      confirmar_senha: 'Senha@123',
      pergunta_seguranca: 'nome_mae',
      resposta_seguranca: 'Maria Silva',
    };
    await use(user);
  },

  authenticatedPage: async ({ page, loginPage, testUser, cadastroPage }, use) => {
    await page.goto('/');
    await page.waitForLoadState('domcontentloaded');
    
    await page.evaluate(() => {
      try {
        localStorage.clear();
        sessionStorage.clear();
      } catch (e) {
        // Ignore security errors
      }
    });

    await cadastroPage.goto();
    await cadastroPage.cadastrar(testUser);

    await loginPage.goto();
    await loginPage.login(testUser.nome_usuario, testUser.senha);

    await use(page);

    await page.evaluate(() => {
      try {
        localStorage.clear();
        sessionStorage.clear();
      } catch (e) {
        // Ignore security errors
      }
    });
  },
});

export { expect } from '@playwright/test';