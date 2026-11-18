import { test, expect } from '@playwright/test';

test.use({ baseURL: 'http://localhost:8380' });

test.describe('Smoke — COBECO MVP (headless)', () => {
  test('home renderiza título, hero e CTA de nova lista', async ({ page }) => {
    await page.goto('/');
    await page.waitForSelector('h1', { state: 'visible' });
    await expect(page.locator('h1')).toContainText('Compras mais inteligentes');
    await expect(page.locator('[data-action="nav-nova"]').first()).toBeVisible();
    await expect(page.locator('#main')).toBeVisible();
  });

  test('navega para categorias e renderiza pré-filtro (RF12/UC03)', async ({ page }) => {
    await page.goto('/');
    await page.click('button.btn.btn-white.btn-lg');
    await page.waitForSelector('h1', { state: 'visible' });
    await expect(page.locator('h1')).toContainText('Selecione as categorias');
    await expect(page.locator('text=Passo 1 de 5')).toBeVisible();
    await expect(page.locator('[data-catcard]')).toHaveCount(11);
  });

  test('botão continuar desabilitado sem categoria (RF12)', async ({ page }) => {
    await page.goto('/');
    await page.click('button.btn.btn-white.btn-lg');
    await page.waitForSelector('#btn-to-lista', { state: 'visible' });
    const btn = page.locator('#btn-to-lista');
    await expect(btn).toBeDisabled();
  });
});
