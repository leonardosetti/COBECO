import { test, expect } from '@playwright/test';
import { BasePage } from '../pages/BasePage';

test.describe('Smoke — COBECO MVP (headless)', () => {
  let page: BasePage;

  test.beforeEach(async ({ page: p }) => {
    page = new BasePage(p);
    await page.goto('/');
    await page.clearStorage();
  });

  test('home renderiza título, hero e CTA de nova lista', async () => {
    await expect(page.page.locator('h1')).toContainText('Compras mais inteligentes');
    await expect(page.page.locator('text=Criar minha lista')).toBeVisible();
    await expect(page.page.locator('#main')).toBeVisible();
  });

  test('navega para categorias e renderiza pré-filtro (RF12/UC03)', async () => {
    await page.page.click('text=Criar minha lista');
    await page.expectVisible('h1:has-text("Selecione as categorias")');
    await expect(page.page.locator('text=Passo 1 de 5')).toBeVisible();
    // Pelo menos uma categoria renderizada
    await expect(page.page.locator('.cat-card, [data-catcard]')).toHaveCount(11);
  });

  test('botão continuar desabilitado sem categoria (RF12)', async () => {
    await page.page.click('text=Criar minha lista');
    const btn = page.page.locator('#btn-to-lista');
    await expect(btn).toBeDisabled();
  });
});
