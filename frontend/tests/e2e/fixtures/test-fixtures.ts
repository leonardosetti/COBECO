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
    const random = Math.random().toString(36).substring(2, 8);
    const user: CadastroData = {
      nome_usuario: `testuser${timestamp}${random}`,
      email: `test${timestamp}${random}@example.com`,
      nome: `Test User ${timestamp}`,
      senha: 'Senha@123',
      confirmar_senha: 'Senha@123',
      pergunta_seguranca: 'cidade',
      resposta_seguranca: 'Fluffy',
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

    // Register user (auto-logs in after registration)
    await cadastroPage.goto();
    const toast = await cadastroPage.cadastrar(testUser);
    console.log('Registration toast:', toast);
    
    // Wait for registration to complete and navigation to categorias
    await page.waitForURL('**/#/categorias', { timeout: 20000 });
    await page.waitForLoadState('networkidle');
    // Give header time to render after hash change
    await page.waitForTimeout(2000);
    
    // Wait for logout button to appear in header (user is logged in after registration)
    await page.waitForSelector('[data-action="sair"]', { state: 'visible', timeout: 20000 });

    await use(page);
  },
});

export { expect } from '@playwright/test';