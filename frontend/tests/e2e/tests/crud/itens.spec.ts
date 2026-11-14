import { test, expect } from '../../fixtures/test-fixtures';
import { createTestUser, createListaData } from '../../utils/test-data';

test.describe('CRUD - Itens da Lista (UC07-RF07, UC08-RF08, UC09-RF09, UC10-RF10)', () => {
  let listaId: string;

  test.beforeEach(async ({ authenticatedPage, listasPage }) => {
    await listasPage.gotoMinhasListas();
    await listasPage.gotoCriarLista();
    await listasPage.criarLista(createListaData({ titulo: 'Lista para Itens' }));
    listaId = (await listasPage.getListaIdByTitulo('Lista para Itens')) || '';
  });

  test.describe('CREATE - Adicionar item à lista', () => {
    test('deve adicionar item com dados mínimos (apenas nome)', async ({ listasPage }) => {
      await listasPage.verLista(listaId);
      
      const adicionarButton = listasPage.page.locator('#btn-adicionar-item, button:has-text("Adicionar item"), [data-link*="item"]');
      await adicionarButton.click();
      
      const nomeInput = listasPage.page.locator('input[name="nome"], #item-nome');
      await nomeInput.fill('Arroz 5kg');
      
      const submitButton = listasPage.page.locator('button[type="submit"]');
      await submitButton.click();
      
      await listasPage.waitForToast('Item adicionado');
      await expect(listasPage.page.locator('text=Arroz 5kg')).toBeVisible();
    });

    test('deve adicionar item com preço', async ({ listasPage }) => {
      await listasPage.verLista(listaId);
      
      const adicionarButton = listasPage.page.locator('#btn-adicionar-item, button:has-text("Adicionar item")');
      await adicionarButton.click();
      
      await listasPage.page.fill('input[name="nome"], #item-nome', 'Feijão 1kg');
      await listasPage.page.fill('input[name="preco"], #item-preco', '8.50');
      
      await listasPage.page.click('button[type="submit"]');
      
      await listasPage.waitForToast('Item adicionado');
      await expect(listasPage.page.locator('text=Feijão 1kg')).toBeVisible();
      await expect(listasPage.page.locator('text=8,50')).toBeVisible();
    });

    test('deve adicionar item com loja', async ({ listasPage }) => {
      await listasPage.verLista(listaId);
      
      const adicionarButton = listasPage.page.locator('#btn-adicionar-item, button:has-text("Adicionar item")');
      await adicionarButton.click();
      
      await listasPage.page.fill('input[name="nome"], #item-nome', 'Leite 1L');
      await listasPage.page.fill('input[name="loja"], #item-loja', 'Supermercado ABC');
      
      await listasPage.page.click('button[type="submit"]');
      
      await listasPage.waitForToast('Item adicionado');
      await expect(listasPage.page.locator('text=Leite 1L')).toBeVisible();
      await expect(listasPage.page.locator('text=Supermercado ABC')).toBeVisible();
    });

    test('deve adicionar item com URL', async ({ listasPage }) => {
      await listasPage.verLista(listaId);
      
      const adicionarButton = listasPage.page.locator('#btn-adicionar-item, button:has-text("Adicionar item")');
      await adicionarButton.click();
      
      await listasPage.page.fill('input[name="nome"], #item-nome', 'Produto Online');
      await listasPage.page.fill('input[name="url"], #item-url', 'https://exemplo.com/produto');
      
      await listasPage.page.click('button[type="submit"]');
      
      await listasPage.waitForToast('Item adicionado');
      await expect(listasPage.page.locator('text=Produto Online')).toBeVisible();
    });

    test('deve exigir nome do item', async ({ listasPage }) => {
      await listasPage.verLista(listaId);
      
      const adicionarButton = listasPage.page.locator('#btn-adicionar-item, button:has-text("Adicionar item")');
      await adicionarButton.click();
      
      await listasPage.page.click('button[type="submit"]');
      
      await expect(listasPage.page.locator('input[name="nome"], #item-nome')).toHaveAttribute('required');
    });

    test('deve validar preço numérico', async ({ listasPage }) => {
      await listasPage.verLista(listaId);
      
      const adicionarButton = listasPage.page.locator('#btn-adicionar-item, button:has-text("Adicionar item")');
      await adicionarButton.click();
      
      await listasPage.page.fill('input[name="nome"], #item-nome', 'Produto Teste');
      await listasPage.page.fill('input[name="preco"], #item-preco', 'abc');
      
      await listasPage.page.click('button[type="submit"]');
      
      const toast = await listasPage.getToastMessage();
      expect(toast?.toLowerCase()).toMatch(/preço|número|valor|inválido/);
    });
  });

  test.describe('READ - Visualizar itens da lista', () => {
    test('deve listar todos os itens da lista', async ({ listasPage }) => {
      await listasPage.verLista(listaId);
      
      const adicionarButton = listasPage.page.locator('#btn-adicionar-item, button:has-text("Adicionar item")');
      
      await adicionarButton.click();
      await listasPage.page.fill('input[name="nome"], #item-nome', 'Item 1');
      await listasPage.page.click('button[type="submit"]');
      await listasPage.waitForToast('Item adicionado');
      
      await adicionarButton.click();
      await listasPage.page.fill('input[name="nome"], #item-nome', 'Item 2');
      await listasPage.page.click('button[type="submit"]');
      await listasPage.waitForToast('Item adicionado');
      
      await expect(listasPage.page.locator('text=Item 1')).toBeVisible();
      await expect(listasPage.page.locator('text=Item 2')).toBeVisible();
    });

    test('deve mostrar lista vazia quando não há itens', async ({ listasPage }) => {
      await listasPage.verLista(listaId);
      
      await expect(listasPage.page.locator('text=/nenhum item|vazio|adicionar.*primeiro/i')).toBeVisible();
    });
  });

  test.describe('UPDATE - Editar item', () => {
    test('deve editar nome do item', async ({ listasPage }) => {
      await listasPage.verLista(listaId);
      
      const adicionarButton = listasPage.page.locator('#btn-adicionar-item, button:has-text("Adicionar item")');
      await adicionarButton.click();
      await listasPage.page.fill('input[name="nome"], #item-nome', 'Item Original');
      await listasPage.page.click('button[type="submit"]');
      await listasPage.waitForToast('Item adicionado');
      
      const editarButton = listasPage.page.locator('button:has-text("Editar"), [data-action="editar"]').first();
      await editarButton.click();
      
      await listasPage.page.fill('input[name="nome"], #item-nome', 'Item Editado');
      await listasPage.page.click('button[type="submit"]');
      
      await listasPage.waitForToast('Item atualizado');
      await expect(listasPage.page.locator('text=Item Editado')).toBeVisible();
      await expect(listasPage.page.locator('text=Item Original')).not.toBeVisible();
    });

    test('deve editar preço do item', async ({ listasPage }) => {
      await listasPage.verLista(listaId);
      
      const adicionarButton = listasPage.page.locator('#btn-adicionar-item, button:has-text("Adicionar item")');
      await adicionarButton.click();
      await listasPage.page.fill('input[name="nome"], #item-nome', 'Item Com Preço');
      await listasPage.page.fill('input[name="preco"], #item-preco', '10.00');
      await listasPage.page.click('button[type="submit"]');
      await listasPage.waitForToast('Item adicionado');
      
      const editarButton = listasPage.page.locator('button:has-text("Editar"), [data-action="editar"]').first();
      await editarButton.click();
      
      await listasPage.page.fill('input[name="preco"], #item-preco', '15.50');
      await listasPage.page.click('button[type="submit"]');
      
      await listasPage.waitForToast('Item atualizado');
      await expect(listasPage.page.locator('text=15,50')).toBeVisible();
    });
  });

  test.describe('DELETE - Remover item', () => {
    test('deve remover item da lista', async ({ listasPage }) => {
      await listasPage.verLista(listaId);
      
      const adicionarButton = listasPage.page.locator('#btn-adicionar-item, button:has-text("Adicionar item")');
      await adicionarButton.click();
      await listasPage.page.fill('input[name="nome"], #item-nome', 'Item Para Remover');
      await listasPage.page.click('button[type="submit"]');
      await listasPage.waitForToast('Item adicionado');
      
      const removerButton = listasPage.page.locator('button:has-text("Remover"), [data-action="remover"]').first();
      await removerButton.click();
      
      const confirmButton = listasPage.page.locator('button:has-text("Confirmar"), button:has-text("Sim")');
      await confirmButton.click();
      
      await listasPage.waitForToast('Item removido');
      await expect(listasPage.page.locator('text=Item Para Remover')).not.toBeVisible();
    });

    test('deve pedir confirmação antes de remover', async ({ listasPage }) => {
      await listasPage.verLista(listaId);
      
      const adicionarButton = listasPage.page.locator('#btn-adicionar-item, button:has-text("Adicionar item")');
      await adicionarButton.click();
      await listasPage.page.fill('input[name="nome"], #item-nome', 'Item Para Confirmar');
      await listasPage.page.click('button[type="submit"]');
      await listasPage.waitForToast('Item adicionado');
      
      const removerButton = listasPage.page.locator('button:has-text("Remover"), [data-action="remover"]').first();
      await removerButton.click();
      
      await expect(listasPage.page.locator('text=/confirmar|tem certeza|remover/i')).toBeVisible();
    });
  });

  test.describe('Marcar/Desmarcar item (checkbox)', () => {
    test('deve marcar item como comprado', async ({ listasPage }) => {
      await listasPage.verLista(listaId);
      
      const adicionarButton = listasPage.page.locator('#btn-adicionar-item, button:has-text("Adicionar item")');
      await adicionarButton.click();
      await listasPage.page.fill('input[name="nome"], #item-nome', 'Item Para Marcar');
      await listasPage.page.click('button[type="submit"]');
      await listasPage.waitForToast('Item adicionado');
      
      const checkbox = listasPage.page.locator('input[type="checkbox"]').first();
      await checkbox.check();
      
      await expect(checkbox).toBeChecked();
      await expect(listasPage.page.locator('text=Item Para Marcar').locator('..')).toHaveClass(/line-through|comprado|done/);
    });

    test('deve desmarcar item', async ({ listasPage }) => {
      await listasPage.verLista(listaId);
      
      const adicionarButton = listasPage.page.locator('#btn-adicionar-item, button:has-text("Adicionar item")');
      await adicionarButton.click();
      await listasPage.page.fill('input[name="nome"], #item-nome', 'Item Para Desmarcar');
      await listasPage.page.click('button[type="submit"]');
      await listasPage.waitForToast('Item adicionado');
      
      const checkbox = listasPage.page.locator('input[type="checkbox"]').first();
      await checkbox.check();
      await checkbox.uncheck();
      
      await expect(checkbox).not.toBeChecked();
    });
  });
});