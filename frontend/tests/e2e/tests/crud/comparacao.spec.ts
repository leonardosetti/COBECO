import { test, expect } from '../../fixtures/test-fixtures';
import { createTestUser, createListaData } from '../../utils/test-data';

test.describe('CRUD - Comparação de Preços (UC05-RF15, UC06-RF16)', () => {
  test.describe('Fluxo Completo de Comparação', () => {
    test('deve criar lista, ir para comparação, selecionar fornecedores e ver tabela flat', async ({ 
      authenticatedPage, 
      listasPage 
    }) => {
      // 1. Cria lista com itens
      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      await listasPage.criarLista(createListaData({ titulo: 'Lista Comparação Completa' }));
      await listasPage.waitForToast('Lista criada');

      // Adiciona alguns itens à lista (simula via UI)
      await listasPage.page.goto('/#/criar-lista');
      await listasPage.page.waitForLoadState('networkidle');
      
      // Adiciona itens via autocomplete (simplificado)
      const produtoInput = listasPage.page.locator('#item-produto');
      await produtoInput.waitFor({ state: 'visible', timeout: 10000 });
      
      // Adiciona 3 itens
      for (const produto of ['Arroz', 'Feijão', 'Óleo']) {
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

      // 2. Vai para comparação
      await listasPage.page.goto('/#/comparar');
      await listasPage.page.waitForLoadState('networkidle');

      // 3. Seleciona fornecedores (pelo menos 2)
      const fornecedorCheckboxes = listasPage.page.locator('input[type="checkbox"][name="fornecedor"], .fornecedor-selecao input');
      await expect(fornecedorCheckboxes.first()).toBeVisible({ timeout: 10000 });
      
      // Seleciona primeiros 3 fornecedores
      const count = await fornecedorCheckboxes.count();
      const selectCount = Math.min(3, count);
      for (let i = 0; i < selectCount; i++) {
        await fornecedorCheckboxes.nth(i).check();
      }

      // 4. Clica em comparar
      const btnComparar = listasPage.page.locator('#btn-comparar, button:has-text("Comparar"), button:has-text("Comparar Preços")');
      await btnComparar.click();
      await listasPage.page.waitForLoadState('networkidle');

      // 5. Verifica tabela flat de comparação
      await expect(listasPage.page.locator('.comparacao-table, table.comparacao, .tabela-comparacao')).toBeVisible({ timeout: 15000 });

      // Verifica estrutura da tabela
      const headers = listasPage.page.locator('table thead th');
      await expect(headers).toContainText(['Fornecedor', 'Disponíveis', 'Ausentes', '% Disp.', 'Total']);

      // 6. Verifica ordenação por preço ASC
      const rows = listasPage.page.locator('table tbody tr');
      const rowCount = await rows.count();
      expect(rowCount).toBeGreaterThan(0);

      // Verifica ordenação por preço ASC
      const precos = [];
      for (let i = 0; i < rowCount; i++) {
        const precoText = await rows.nth(i).locator('td:last-child, td.text-right').textContent();
        const preco = parseFloat(precoText?.replace(/[^\d,]/g, '').replace(',', '.') || '0');
        precos.push(preco);
      }
      
      // Verifica ordenação ASC (menor preço primeiro)
      for (let i = 1; i < precos.length; i++) {
        expect(precos[i]).toBeGreaterThanOrEqual(precos[i - 1]);
      }

      // 7. Verifica melhor fornecedor destacado
      const melhorBadge = listasPage.page.locator('.badge-sdoc-arch-0006-uc-v1cess:has-text("MELHOR"), .melhor-oferta, .melhor-fornecedor');
      await expect(melhorBadge.first()).toBeVisible({ timeout: 5000 });
    });
  });

  test.describe('Slider de Disponibilidade (RF16)', () => {
    test('deve filtrar fornecedores por disponibilidade mínima', async ({ authenticatedPage, listasPage }) => {
      // Cria lista e vai para comparação
      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      await listasPage.criarLista(createListaData({ titulo: 'Lista Slider' }));
      await listasPage.waitForToast('Lista criada');

      // Adiciona itens básicos
      await listasPage.page.goto('/#/criar-lista');
      await listasPage.page.waitForLoadState('networkidle');
      
      const produtoInput = listasPage.page.locator('#item-produto');
      await produtoInput.waitFor({ state: 'visible' });
      
      for (const produto of ['Arroz', 'Feijão']) {
        await produtoInput.fill(produto);
        await listasPage.page.waitForTimeout(500);
        const autocompleteResults = listasPage.page.locator('#autocomplete-results');
        await expect(autocompleteResults).toBeVisible({ timeout: 5000 });
        await autocompleteResults.locator('.autocomplete-item, li, [data-produto-id]').first().click();
        await listasPage.page.locator('#btn-add-item').click();
        await listasPage.page.waitForTimeout(300);
      }

      await listasPage.page.locator('#btn-salvar-lista').click();
      await listasPage.waitForToast('Lista salva');

      // Vai para comparação
      await listasPage.page.goto('/#/comparar');
      await listasPage.page.waitForLoadState('networkidle');

      // Seleciona fornecedores
      const fornecedorCheckboxes = listasPage.page.locator('input[type="checkbox"][name="fornecedor"], .fornecedor-selecao input');
      await expect(fornecedorCheckboxes.first()).toBeVisible({ timeout: 10000 });
      const count = await fornecedorCheckboxes.count();
      for (let i = 0; i < Math.min(3, count); i++) {
        await fornecedorCheckboxes.nth(i).check();
      }

      // Testa slider 0% (todos)
      const slider = listasPage.page.locator('input[type="range"][name="disponibilidade"], #slider-disponibilidade, .disponibilidade-slider');
      if (await slider.count() > 0) {
        await slider.fill('0');
        await listasPage.page.waitForTimeout(500);
        
        const btnComparar = listasPage.page.locator('#btn-comparar, button:has-text("Comparar")');
        await btnComparar.click();
        await listasPage.page.waitForLoadState('networkidle');
        
        const rows0 = await listasPage.page.locator('table tbody tr').count();
        
        // Testa slider 100% (apenas fornecedores com todos itens)
        await listasPage.page.goto('/#/comparar');
        await listasPage.page.waitForLoadState('networkidle');
        
        for (let i = 0; i < Math.min(3, await fornecedorCheckboxes.count()); i++) {
          await fornecedorCheckboxes.nth(i).check();
        }
        
        await slider.fill('100');
        await listasPage.page.waitForTimeout(500);
        await listasPage.page.locator('#btn-comparar, button:has-text("Comparar")').click();
        await listasPage.page.waitForLoadState('networkidle');
        
        const rows100 = await listasPage.page.locator('table tbody tr').count();
        
        // 100% deve retornar menos ou igual fornecedores
        expect(rows100).toBeLessThanOrEqual(rows0);
      }
    });

    test('deve exibir percentual de disponibilidade por fornecedor', async ({ authenticatedPage, listasPage }) => {
      // Setup rápido
      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      await listasPage.criarLista(createListaData({ titulo: 'Lista %' }));
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
      
      await listasPage.page.goto('/#/comparar');
      await listasPage.page.waitForLoadState('networkidle');
      
      const fornecedorCheckboxes = listasPage.page.locator('input[type="checkbox"][name="fornecedor"], .fornecedor-selecao input');
      await expect(fornecedorCheckboxes.first()).toBeVisible({ timeout: 10000 });
      await fornecedorCheckboxes.first().check();
      if (await fornecedorCheckboxes.count() > 1) {
        await fornecedorCheckboxes.nth(1).check();
      }
      
      await listasPage.page.locator('#btn-comparar, button:has-text("Comparar")').click();
      await listasPage.page.waitForLoadState('networkidle');
      
      // Verifica coluna % Disp.
      const percCells = listasPage.page.locator('table tbody td:nth-child(4), .percentual-disponibilidade');
      await expect(percCells.first()).toBeVisible({ timeout: 5000 });
      
      // Verifica se valores são percentuais válidos (0-100)
      const percTexts = await percCells.allTextContents();
      for (const text of percTexts) {
        const perc = parseFloat(text.replace('%', '').replace(',', '.'));
        expect(perc).toBeGreaterThanOrEqual(0);
        expect(perc).toBeLessThanOrEqual(100);
      }
    });
  });

  test.describe('Detalhes por Item', () => {
    test('deve expandir detalhes por item ao clicar', async ({ authenticatedPage, listasPage }) => {
      // Setup similar ao anterior
      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      await listasPage.criarLista(createListaData({ titulo: 'Lista Detalhes' }));
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
      
      await listasPage.page.goto('/#/comparar');
      await listasPage.page.waitForLoadState('networkidle');
      
      const fornecedorCheckboxes = listasPage.page.locator('input[type="checkbox"][name="fornecedor"], .fornecedor-selecao input');
      await expect(fornecedorCheckboxes.first()).toBeVisible({ timeout: 10000 });
      await fornecedorCheckboxes.first().check();
      
      await listasPage.page.locator('#btn-comparar, button:has-text("Comparar")').click();
      await listasPage.page.waitForLoadState('networkidle');
      
      // Procura botão/resumo "Ver detalhes por item"
      const detalhesSummary = listasPage.page.locator('details summary:has-text("detalhe"), details summary:has-text("item"), .ver-detalhes');
      if (await detalhesSummary.count() > 0) {
        await detalhesSummary.first().click();
        await listasPage.page.waitForTimeout(300);
        
        // Verifica se detalhes apareceram
        const detalhesContent = listasPage.page.locator('details[open] .card, .detalhes-itens, .item-detalhado');
        await expect(detalhesContent.first()).toBeVisible({ timeout: 3000 });
      }
    });
  });
});