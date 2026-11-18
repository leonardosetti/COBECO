import { test, expect } from '@playwright/test';

test.use({ baseURL: 'http://localhost:8380' });

test.describe('Fluxo completo visitante (E2E contra API real)', () => {

  test('categorias → lista → fornecedores → comparação → exportação PDF', async ({ page }) => {
    // ---------- Passo 1: Categorias ----------
    await page.goto('/');
    await page.waitForSelector('h1', { state: 'visible' });
    await page.click('button.btn.btn-white.btn-lg'); // Criar minha lista
    await page.waitForSelector('text=Selecione as categorias', { state: 'visible' });
    await page.click('[data-catcard="1"] input'); // Mercado
    await page.click('#btn-to-lista');

    // ---------- Passo 2: Lista ----------
    await page.waitForSelector('#nome-lista');
    await page.fill('#nome-lista', 'Lista E2E');
    // Adiciona item diretamente ao estado (o autocomplete UI depende do JS em cache)
    await page.evaluate(() => {
      window.state.lista.itens.push({ pid: 1, qtd: 1 });
      window.refreshListaUI();
    });
    await page.waitForSelector('#itens-box tbody tr', { state: 'visible' });
    await page.click('#btn-to-forn');

    // ---------- Passo 3: Fornecedores ----------
    await page.waitForSelector('.forn-card', { state: 'visible' });
    await page.evaluate(() => {
      const ids = Array.from(document.querySelectorAll('[data-forncard]')).map(el => +el.dataset.forncard).slice(0, 2);
      window.state.fornecedores = ids;
      window.refreshFornecedores();
    });
    await page.click('#btn-calc');

    // ---------- Passo 4: Resultados ----------
    await page.waitForSelector('text=Passo 4 de 5', { state: 'visible', timeout: 15000 });
    const vencedorNome = page.locator('.card.kpi.win .v');
    await expect(vencedorNome).not.toBeEmpty();

    // ---------- Passo 5: Lista vencedora ----------
    await page.click('text=Ver lista vencedora');
    await page.waitForSelector('.win-hero h2', { state: 'visible' });

    // ---------- Exportar PDF (RF17 — visitante, preview da lista vencedora) ----------
    await page.click('text=Exportar PDF');
    await page.waitForSelector('.a4-sheet', { state: 'visible', timeout: 5000 });
    await expect(page.locator('.a4-sheet')).toContainText('LISTA VENCEDORA');
    await expect(page.locator('.a4-sheet')).toContainText('TOTAL CONSOLIDADO');
  });

});
