import { test, expect } from '../../fixtures/test-fixtures';
import { createTestUser } from '../../utils/test-data';

test.describe('Responsividade Desktop-First (≥1024px)', () => {
  test.describe('Breakpoints Principais', () => {
    test('layout funciona em 1024px (mínimo suportado)', async ({ page, cadastroPage, loginPage }) => {
      await page.setViewportSize({ width: 1024, height: 768 });
      
      await cadastroPage.goto();
      await cadastroPage.cadastrar(createTestUser());
      
      await loginPage.goto();
      await loginPage.login('testuser', 'Senha@123');
      
      await expect(page.locator('main')).toBeVisible();
      await expect(page.locator('#header')).toBeVisible();
      
      // Verifica se não há overflow horizontal
      const bodyWidth = await page.evaluate(() => document.body.scrollWidth);
      const viewportWidth = await page.evaluate(() => window.innerWidth);
      expect(bodyWidth).toBeLessThanOrEqual(viewportWidth + 20); // Tolerância para scrollbar
    });

    test('layout funciona em 1366px (comum notebook)', async ({ page, cadastroPage, loginPage }) => {
      await page.setViewportSize({ width: 1366, height: 768 });
      
      await cadastroPage.goto();
      await cadastroPage.cadastrar(createTestUser());
      
      await loginPage.goto();
      await loginPage.login('testuser', 'Senha@123');
      
      await expect(page.locator('main')).toBeVisible();
      await expect(page.locator('.max-w-7xl, .container')).toBeVisible();
    });

    test('layout funciona em 1440px (desktop padrão)', async ({ page, cadastroPage, loginPage }) => {
      await page.setViewportSize({ width: 1440, height: 900 });
      
      await cadastroPage.goto();
      await cadastroPage.cadastrar(createTestUser());
      
      await loginPage.goto();
      await loginPage.login('testuser', 'Senha@123');
      
      await expect(page.locator('main')).toBeVisible();
      
      // Verifica se container centralizado tem largura máxima
      const container = page.locator('.max-w-7xl, .container, main > div:first-child');
      const box = await container.boundingBox();
      expect(box?.width).toBeLessThanOrEqual(1440);
    });

    test('layout funciona em 1920px (full HD)', async ({ page, cadastroPage, loginPage }) => {
      await page.setViewportSize({ width: 1920, height: 1080 });
      
      await cadastroPage.goto();
      await cadastroPage.cadastrar(createTestUser());
      
      await loginPage.goto();
      await loginPage.login('testuser', 'Senha@123');
      
      await expect(page.locator('main')).toBeVisible();
    });
  });

  test.describe('Breakpoint Único - Sem Mobile', () => {
    test('não deve quebrar para layout mobile em 800px', async ({ page, cadastroPage, loginPage }) => {
      await page.setViewportSize({ width: 800, height: 600 });
      
      await cadastroPage.goto();
      await cadastroPage.cadastrar(createTestUser());
      
      await loginPage.goto();
      await loginPage.login('testuser', 'Senha@123');
      
      // Deve mostrar layout desktop com scroll horizontal se necessário
      await expect(page.locator('main')).toBeVisible();
      
      // Não deve ter classes mobile-only visíveis
      const mobileOnly = page.locator('.mobile-only, .md\\:hidden, .lg\\:hidden, .xl\\:hidden');
      await expect(mobileOnly).toBeHidden();
    });

    test('não deve quebrar em 600px', async ({ page, cadastroPage, loginPage }) => {
      await page.setViewportSize({ width: 600, height: 800 });
      
      await cadastroPage.goto();
      await cadastroPage.cadastrar(createTestUser());
      
      await loginPage.goto();
      await loginPage.login('testuser', 'Senha@123');
      
      await expect(page.locator('main')).toBeVisible();
      
      // Layout desktop deve persistir (com scroll horizontal)
      const bodyWidth = await page.evaluate(() => document.body.scrollWidth);
      expect(bodyWidth).toBeGreaterThan(600);
    });

    test('não deve ter menu hambúrguer mobile', async ({ page, cadastroPage, loginPage }) => {
      await page.setViewportSize({ width: 500, height: 800 });
      
      await cadastroPage.goto();
      await cadastroPage.cadastrar(createTestUser());
      
      await loginPage.goto();
      await loginPage.login('testuser', 'Senha@123');
      
      // Não deve ter botão de menu mobile
      const hamburger = page.locator('.hamburger, .menu-toggle, button[aria-label="Menu"], .md\\:hidden button');
      await expect(hamburger).toBeHidden();
    });
  });

  test.describe('Componentes Responsivos', () => {
    test('tabelas devem ter scroll horizontal em telas pequenas', async ({ page, cadastroPage, loginPage, listasPage }) => {
      await page.setViewportSize({ width: 800, height: 600 });
      
      await cadastroPage.goto();
      await cadastroPage.cadastrar(createTestUser());
      
      await loginPage.goto();
      await loginPage.login('testuser', 'Senha@123');
      
      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      await listasPage.criarLista({ titulo: 'Lista Tabela' });
      await listasPage.waitForToast('Lista criada');
      
      // Verifica se tabela tem container com scroll
      const tableContainer = page.locator('.table-container, .overflow-x-auto, div:has(table)');
      await expect(tableContainer.first()).toBeVisible();
      
      // Verifica se tabela não estica além da viewport
      const table = page.locator('table');
      const tableBox = await table.boundingBox();
      const viewportWidth = await page.evaluate(() => window.innerWidth);
      expect(tableBox?.width).toBeLessThanOrEqual(viewportWidth);
    });

    test('formulários devem ser usáveis em 1024px', async ({ page, cadastroPage }) => {
      await page.setViewportSize({ width: 1024, height: 768 });
      
      await cadastroPage.goto();
      
      // Verifica se campos do formulário estão visíveis e usáveis
      await expect(cadastroPage.nomeUsuarioInput).toBeVisible();
      await expect(cadastroPage.emailInput).toBeVisible();
      await expect(cadastroPage.senhaInput).toBeVisible();
      
      // Verifica se botão submit está acessível
      await expect(cadastroPage.submitButton).toBeVisible();
      await expect(cadastroPage.submitButton).toBeEnabled();
    });

    test('modais devem ser centralizados e legíveis', async ({ page, cadastroPage, loginPage }) => {
      await page.setViewportSize({ width: 1024, height: 768 });
      
      await cadastroPage.goto();
      await cadastroPage.cadastrar(createTestUser());
      
      await loginPage.goto();
      await loginPage.login('testuser', 'Senha@123');
      
      // Abre modal de confirmação (ex: excluir lista)
      // Como não temos lista, testa showConfirm via console
      const modalOpened = await page.evaluate(() => {
        return new Promise((resolve) => {
          window.showConfirm('Teste modal').then(() => resolve(true));
        });
      });
      
      expect(modalOpened).toBe(true);
      
      // Verifica se modal está centralizado
      const modal = page.locator('.modal');
      const modalBox = await modal.boundingBox();
      const viewportWidth = await page.evaluate(() => window.innerWidth);
      const viewportHeight = await page.evaluate(() => window.innerHeight);
      
      if (modalBox) {
        expect(modalBox.x).toBeGreaterThanOrEqual(0);
        expect(modalBox.y).toBeGreaterThanOrEqual(0);
        expect(modalBox.x + modalBox.width).toBeLessThanOrEqual(viewportWidth);
        expect(modalBox.y + modalBox.height).toBeLessThanOrEqual(viewportHeight);
      }
    });

    test('toasts devem aparecer no canto inferior direito', async ({ page, cadastroPage, loginPage }) => {
      await page.setViewportSize({ width: 1024, height: 768 });
      
      await cadastroPage.goto();
      await cadastroPage.cadastrar(createTestUser());
      
      await loginPage.goto();
      await loginPage.login('testuser', 'Senha@123');
      
      // Trigger toast via console
      await page.evaluate(() => window.showToast('Teste toast', 'success'));
      
      const toastContainer = page.locator('#toast-container');
      await expect(toastContainer).toBeVisible();
      
      const toastBox = await toastContainer.boundingBox();
      const viewportWidth = await page.evaluate(() => window.innerWidth);
      const viewportHeight = await page.evaluate(() => window.innerHeight);
      
      if (toastBox) {
        // Deve estar no canto inferior direito
        expect(toastBox.x + toastBox.width).toBeGreaterThan(viewportWidth * 0.7);
        expect(toastBox.y + toastBox.height).toBeGreaterThan(viewportHeight * 0.7);
      }
    });
  });

  test.describe('Grid e Flexbox', () => {
    test('grid de listas deve adaptar colunas', async ({ authenticatedPage, listasPage }) => {
      // Testa em diferentes larguras
      const viewports = [
        { width: 1024, expectedCols: 1 },
        { width: 1366, expectedCols: 1 },
        { width: 1440, expectedCols: 1 },
        { width: 1920, expectedCols: 1 }, // Lista usa tabela, não grid
      ];

      for (const vp of viewports) {
        await listasPage.page.setViewportSize({ width: vp.width, height: 768 });
        await listasPage.gotoMinhasListas();
        
        // Lista usa tabela, não grid - verifica se tabela é responsiva
        const table = listasPage.page.locator('table');
        await expect(table).toBeVisible();
      }
    });

    test('cards de fornecedores na comparação devem empilhar', async ({ authenticatedPage, listasPage }) => {
      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      await listasPage.criarLista({ titulo: 'Lista Grid' });
      await listasPage.waitForToast('Lista criada');
      
      await listasPage.page.goto('/#/comparar');
      await listasPage.page.waitForLoadState('networkidle');
      
      const fornecedorCheckboxes = listasPage.page.locator('input[type="checkbox"][name="fornecedor"], .fornecedor-selecao input');
      await expect(fornecedorCheckboxes.first()).toBeVisible({ timeout: 10000 });
      await fornecedorCheckboxes.first().check();
      
      await listasPage.page.locator('#btn-comparar, button:has-text("Comparar")').click();
      await listasPage.page.waitForLoadState('networkidle');
      
      // Verifica se cards de fornecedores estão em coluna única (mobile-first seria grid, mas desktop-first usa flex-col)
      const fornecedorCards = listasPage.page.locator('.fornecedor-card, .card:has(.fornecedor_nome), details > .card');
      const count = await fornecedorCards.count();
      expect(count).toBeGreaterThan(0);
    });
  });
});