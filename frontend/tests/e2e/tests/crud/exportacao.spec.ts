import { test, expect } from '../../fixtures/test-fixtures';
import { createTestUser, createListaData } from '../../utils/test-data';

test.describe('CRUD - Exportação PDF (UC08-RF17)', () => {
  test.describe('Exportar Lista em PDF', () => {
    test('deve baixar PDF da lista autenticado', async ({ authenticatedPage, listasPage }) => {
      // Cria lista com itens
      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      await listasPage.criarLista(createListaData({ titulo: 'Lista para PDF' }));
      await listasPage.waitForToast('Lista criada');

      // Adiciona itens
      await listasPage.page.goto('/#/criar-lista');
      await listasPage.page.waitForLoadState('networkidle');
      
      const produtoInput = listasPage.page.locator('#item-produto');
      await produtoInput.waitFor({ state: 'visible', timeout: 10000 });
      
      for (const produto of ['Arroz 5kg', 'Feijão 1kg', 'Óleo 900ml']) {
        await produtoInput.fill(produto);
        await listasPage.page.waitForTimeout(500);
        const autocompleteResults = listasPage.page.locator('#autocomplete-results');
        await expect(autocompleteResults).toBeVisible({ timeout: 5000 });
        await autocompleteResults.locator('.autocomplete-item, li, [data-produto-id]').first().click();
        await listasPage.page.locator('#item-quantidade').fill('1');
        await listasPage.page.locator('#btn-add-item').click();
        await listasPage.page.waitForTimeout(300);
      }

      // Salva lista
      await listasPage.page.locator('#btn-salvar-lista').click();
      await listasPage.waitForToast('Lista salva');

      // Obtém ID da lista
      const listaId = await listasPage.getListaIdByTitulo('Lista para PDF');
      expect(listaId).not.toBeNull();

      // 2. Clica em exportar PDF
      const btnExportar = listasPage.page.locator('#btn-exportar-pdf, button:has-text("Exportar PDF"), a:has-text("PDF")');
      await expect(btnExportar).toBeVisible({ timeout: 10000 });
      
      // Configura download
      const downloadPromise = listasPage.page.waitForEvent('download');
      await btnExportar.click();
      const download = await downloadPromise;

      // Verifica download
      expect(download).toBeTruthy();
      expect(download.suggestedFilename()).toMatch(/lista_\d{8}\.pdf/);
      
      // Verifica que é PDF
      const buffer = await download.createReadStream().then(stream => {
        const chunks = [];
        return new Promise((resolve) => {
          stream.on('data', chunk => chunks.push(chunk));
          stream.on('end', () => resolve(Buffer.concat(chunks)));
        });
      });
      expect(buffer.slice(0, 5).toString()).toBe('%PDF-');
    });

    test('deve baixar PDF como visitante (sem auth)', async ({ page, listasPage, cadastroPage, loginPage }) => {
      // Cria usuário e lista
      const userData = createTestUser();
      await cadastroPage.goto();
      await cadastroPage.cadastrar(userData);
      await loginPage.goto();
      await loginPage.login(userData.nome_usuario, userData.senha);

      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      await listasPage.criarLista(createListaData({ titulo: 'Lista Visitante PDF' }));
      await listasPage.waitForToast('Lista criada');

      // Adiciona item
      await page.goto('/#/criar-lista');
      await page.waitForLoadState('networkidle');
      
      const produtoInput = page.locator('#item-produto');
      await produtoInput.waitFor({ state: 'visible' });
      await produtoInput.fill('Arroz');
      await page.waitForTimeout(500);
      const autocompleteResults = page.locator('#autocomplete-results');
      await expect(autocompleteResults).toBeVisible({ timeout: 5000 });
      await autocompleteResults.locator('.autocomplete-item, li, [data-produto-id]').first().click();
      await page.locator('#btn-add-item').click();
      await page.waitForTimeout(300);

      await page.locator('#btn-salvar-lista').click();
      await page.waitForTimeout(1000);

      const listaId = await listasPage.getListaIdByTitulo('Lista Visitante PDF');
      expect(listaId).not.toBeNull();

      // Logout
      await page.goto('/#/perfil');
      await page.waitForLoadState('networkidle');
      await page.locator('#btn-logout').click();
      await page.waitForLoadState('networkidle');

      // Acessa PDF sem auth
      const downloadPromise = page.waitForEvent('download');
      await page.goto(`/#/export/lista/${listaId}/pdf`);
      const download = await downloadPromise;

      expect(download).toBeTruthy();
      expect(download.suggestedFilename()).toMatch(/lista_\d{8}\.pdf/);
      
      const buffer = await download.createReadStream().then(stream => {
        const chunks = [];
        return new Promise((resolve) => {
          stream.on('data', chunk => chunks.push(chunk));
          stream.on('end', () => resolve(Buffer.concat(chunks)));
        });
      });
      expect(buffer.slice(0, 5).toString()).toBe('%PDF-');
    });

    test('PDF deve ter nome no formato lista_YYYYMMDD.pdf', async ({ authenticatedPage, listasPage }) => {
      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      await listasPage.criarLista(createListaData({ titulo: 'Lista Nome PDF' }));
      await listasPage.waitForToast('Lista criada');

      await listasPage.page.goto('/#/criar-lista');
      await listasPage.page.waitForLoadState('networkidle');
      
      const produtoInput = listasPage.page.locator('#item-produto');
      await produtoInput.waitFor({ state: 'visible' });
      await produtoInput.fill('Arroz');
      await listasPage.page.waitForTimeout(500);
      const autocompleteResults = listasPage.page.locator('#autocomplete-results');
      await expect(autocompleteResults).toBeVisible({ timeout: 5000 });
      await autocompleteResults.locator('.autocomplete-item, li, [data-produto-id]').first().click();
      await listasPage.page.locator('#btn-add-item').click();
      await listasPage.page.waitForTimeout(300);

      await listasPage.page.locator('#btn-salvar-lista').click();
      await listasPage.waitForToast('Lista salva');

      const listaId = await listasPage.getListaIdByTitulo('Lista Nome PDF');
      expect(listaId).not.toBeNull();

      const downloadPromise = listasPage.page.waitForEvent('download');
      await listasPage.page.locator('#btn-exportar-pdf, button:has-text("Exportar PDF")').click();
      const download = await downloadPromise;

      const filename = download.suggestedFilename();
      expect(filename).toMatch(/lista_\d{8}\.pdf$/);
      
      // Verifica se data é hoje
      const today = new Date();
      const expectedDate = today.toISOString().split('T')[0].replace(/-/g, '');
      expect(filename).toContain(expectedDate);
    });
  });

  test.describe('Impressão (CSS @media print)', () => {
    test('deve imprimir lista via botão imprimir', async ({ authenticatedPage, listasPage }) => {
      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      await listasPage.criarLista(createListaData({ titulo: 'Lista Imprimir' }));
      await listasPage.waitForToast('Lista criada');

      await listasPage.page.goto('/#/criar-lista');
      await listasPage.page.waitForLoadState('networkidle');
      
      const produtoInput = listasPage.page.locator('#item-produto');
      await produtoInput.waitFor({ state: 'visible' });
      await produtoInput.fill('Arroz');
      await listasPage.page.waitForTimeout(500);
      const autocompleteResults = listasPage.page.locator('#autocomplete-results');
      await expect(autocompleteResults).toBeVisible({ timeout: 5000 });
      await autocompleteResults.locator('.autocomplete-item, li, [data-produto-id]').first().click();
      await listasPage.page.locator('#btn-add-item').click();
      await listasPage.page.waitForTimeout(300);

      await listasPage.page.locator('#btn-salvar-lista').click();
      await listasPage.waitForToast('Lista salva');

      // Clica em imprimir
      const btnImprimir = listasPage.page.locator('#btn-imprimir, button:has-text("Imprimir")');
      await expect(btnImprimir).toBeVisible({ timeout: 5000 });
      
      // Verifica se abre dialog de impressão (não podemos testar fully, mas verificamos se função é chamada)
      const printSpy = await listasPage.page.evaluate(() => {
        const originalPrint = window.print;
        window.print = () => { window.printCalled = true; };
        return () => window.printCalled;
      });
      
      await btnImprimir.click();
      await listasPage.page.waitForTimeout(500);
      
      const printCalled = await listasPage.page.evaluate(() => window.printCalled);
      expect(printCalled).toBe(true);
    });

    test('CSS @media print deve ocultar elementos de navegação', async ({ authenticatedPage, listasPage }) => {
      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      await listasPage.criarLista(createListaData({ titulo: 'Lista Print CSS' }));
      await listasPage.waitForToast('Lista criada');

      await listasPage.page.goto('/#/criar-lista');
      await listasPage.page.waitForLoadState('networkidle');
      
      const produtoInput = listasPage.page.locator('#item-produto');
      await produtoInput.waitFor({ state: 'visible' });
      await produtoInput.fill('Arroz');
      await listasPage.page.waitForTimeout(500);
      const autocompleteResults = listasPage.page.locator('#autocomplete-results');
      await expect(autocompleteResults).toBeVisible({ timeout: 5000 });
      await autocompleteResults.locator('.autocomplete-item, li, [data-produto-id]').first().click();
      await listasPage.page.locator('#btn-add-item').click();
      await listasPage.page.waitForTimeout(300);

      await listasPage.page.locator('#btn-salvar-lista').click();
      await listasPage.waitForToast('Lista salva');

      // Emula media print
      await listasPage.page.emulateMedia({ media: 'print' });
      
      // Verifica se header/nav estão ocultos
      const header = listasPage.page.locator('#header, header, nav');
      await expect(header).toBeHidden();
      
      // Verifica se botões de ação estão ocultos
      const actionButtons = listasPage.page.locator('#btn-salvar-lista, #btn-add-item, #btn-exportar-pdf, #btn-imprimir, .btn-primary');
      await expect(actionButtons.first()).toBeHidden();
      
      // Restaura media screen
      await listasPage.page.emulateMedia({ media: 'screen' });
    });
  });

  test.describe('Performance PDF (RNF11)', () => {
    test('geração de PDF < 5s para lista até 100 itens', async ({ authenticatedPage, listasPage }) => {
      // Cria lista com muitos itens (simulado)
      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      await listasPage.criarLista(createListaData({ titulo: 'Lista Performance' }));
      await listasPage.waitForToast('Lista criada');

      await listasPage.page.goto('/#/criar-lista');
      await listasPage.page.waitForLoadState('networkidle');
      
      const produtoInput = listasPage.page.locator('#item-produto');
      await produtoInput.waitFor({ state: 'visible' });
      
      // Adiciona 20 itens únicos (reutiliza produtos do seed)
      const produtos = ['Arroz', 'Feijão', 'Óleo', 'Açúcar', 'Sal', 'Macarrão', 'Leite', 'Café', 'Farinha', 'Molho'];
      for (let i = 0; i < 20; i++) {
        const produto = produtos[i % produtos.length] + ` ${i + 1}`;
        await produtoInput.fill(produto);
        await listasPage.page.waitForTimeout(300);
        const autocompleteResults = listasPage.page.locator('#autocomplete-results');
        await expect(autocompleteResults).toBeVisible({ timeout: 5000 });
        await autocompleteResults.locator('.autocomplete-item, li, [data-produto-id]').first().click();
        await listasPage.page.locator('#btn-add-item').click();
        await listasPage.page.waitForTimeout(200);
      }

      await listasPage.page.locator('#btn-salvar-lista').click();
      await listasPage.waitForToast('Lista salva');

      // Mede tempo de download/geração PDF
      const startTime = Date.now();
      
      const downloadPromise = listasPage.page.waitForEvent('download');
      await listasPage.page.locator('#btn-exportar-pdf, button:has-text("Exportar PDF")').click();
      const download = await downloadPromise;
      
      const elapsed = Date.now() - startTime;
      
      expect(download).toBeTruthy();
      expect(elapsed).toBeLessThan(5000); // RNF11: < 5 segundos
    });
  });
});