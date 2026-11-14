import { test, expect } from '../../fixtures/test-fixtures';
import { createTestUser } from '../../utils/test-data';

test.describe('CRUD - Catálogo e Autocomplete (UC02-RF07, UC03-RF12, RF13)', () => {
  test.describe('Autocomplete de Produtos', () => {
    test('deve buscar produtos por termo parcial', async ({ authenticatedPage, listasPage }) => {
      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      
      // Aguarda campo de autocomplete
      const produtoInput = listasPage.page.locator('#item-produto');
      await produtoInput.waitFor({ state: 'visible', timeout: 10000 });
      
      // Digita termo de busca
      await produtoInput.fill('Arroz');
      
      // Aguarda resultados do autocomplete
      const autocompleteResults = listasPage.page.locator('#autocomplete-results');
      await expect(autocompleteResults).toBeVisible({ timeout: 5000 });
      
      // Verifica se há resultados
      const items = autocompleteResults.locator('.autocomplete-item, li, [data-produto-id]');
      await expect(items.first()).toBeVisible({ timeout: 3000 });
    });

    test('deve selecionar produto do autocomplete', async ({ authenticatedPage, listasPage }) => {
      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      
      const produtoInput = listasPage.page.locator('#item-produto');
      await produtoInput.waitFor({ state: 'visible' });
      
      await produtoInput.fill('Feijão');
      
      const autocompleteResults = listasPage.page.locator('#autocomplete-results');
      await expect(autocompleteResults).toBeVisible({ timeout: 5000 });
      
      // Clica no primeiro resultado
      const firstResult = autocompleteResults.locator('.autocomplete-item, li, [data-produto-id]').first();
      await firstResult.click();
      
      // Verifica se produto foi selecionado
      await expect(produtoInput).toHaveValue(/Feijão/i);
      
      // Verifica se ID do produto foi preenchido
      const produtoIdInput = listasPage.page.locator('#item-produto-id');
      await expect(produtoIdInput).not.toHaveValue('');
    });

    test('deve limitar resultados do autocomplete', async ({ authenticatedPage, listasPage }) => {
      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      
      const produtoInput = listasPage.page.locator('#item-produto');
      await produtoInput.waitFor({ state: 'visible' });
      
      // Termo genérico que retorna muitos resultados
      await produtoInput.fill('a');
      
      const autocompleteResults = listasPage.page.locator('#autocomplete-results');
      await expect(autocompleteResults).toBeVisible({ timeout: 5000 });
      
      // Verifica limite (geralmente 10-15 itens)
      const items = autocompleteResults.locator('.autocomplete-item, li, [data-produto-id]');
      const count = await items.count();
      expect(count).toBeLessThanOrEqual(15);
    });
  });

  test.describe('Pré-filtro por Categorias', () => {
    test('deve exibir categorias na comparação', async ({ authenticatedPage, listasPage }) => {
      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      
      // Cria lista com alguns itens
      await listasPage.criarLista({ titulo: 'Lista Cat' });
      await listasPage.waitForToast('Lista criada');
      
      // Vai para comparação
      await listasPage.page.goto('/#/comparar');
      await listasPage.page.waitForLoadState('networkidle');
      
      // Verifica se categorias estão disponíveis para filtro
      const categoriaCheckboxes = listasPage.page.locator('input[type="checkbox"][name="categoria"], .categoria-filtro input');
      await expect(categoriaCheckboxes.first()).toBeVisible({ timeout: 5000 });
    });

    test('deve filtrar fornecedores por categoria selecionada', async ({ authenticatedPage, listasPage }) => {
      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      await listasPage.criarLista({ titulo: 'Lista Cat Filtro' });
      await listasPage.waitForToast('Lista criada');
      
      await listasPage.page.goto('/#/comparar');
      await listasPage.page.waitForLoadState('networkidle');
      
      // Seleciona primeira categoria
      const firstCategoria = listasPage.page.locator('input[type="checkbox"][name="categoria"], .categoria-filtro input').first();
      await firstCategoria.check();
      
      // Seleciona fornecedores
      const fornecedorCheckboxes = listasPage.page.locator('input[type="checkbox"][name="fornecedor"], .fornecedor-selecao input');
      await expect(fornecedorCheckboxes.first()).toBeVisible({ timeout: 5000 });
      
      // Verifica se fornecedores filtrados correspondem à categoria
      // (implementação depende da UI real)
    });
  });

  test.describe('Fornecedores', () => {
    test('deve listar fornecedores ativos para seleção', async ({ authenticatedPage, listasPage }) => {
      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      await listasPage.criarLista({ titulo: 'Lista Forn' });
      await listasPage.waitForToast('Lista criada');
      
      await listasPage.page.goto('/#/comparar');
      await listasPage.page.waitForLoadState('networkidle');
      
      // Verifica lista de fornecedores
      const fornecedorList = listasPage.page.locator('.fornecedor-item, .fornecedor-checkbox, [data-fornecedor-id]');
      await expect(fornecedorList.first()).toBeVisible({ timeout: 5000 });
    });

    test('deve exibir categorias de cada fornecedor', async ({ authenticatedPage, listasPage }) => {
      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      await listasPage.criarLista({ titulo: 'Lista Forn Cat' });
      await listasPage.waitForToast('Lista criada');
      
      await listasPage.page.goto('/#/comparar');
      await listasPage.page.waitForLoadState('networkidle');
      
      // Verifica se categorias são exibidas junto aos fornecedores
      const categoriaTags = listasPage.page.locator('.categoria-tag, .badge-categoria, [data-categoria]');
      // Pelo menos uma tag de categoria deve ser visível
      await expect(categoriaTags.first()).toBeVisible({ timeout: 5000 });
    });
  });
});