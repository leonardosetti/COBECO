import { test, expect } from '@playwright/test';

test.use({ baseURL: 'http://localhost:8380' });

test.describe('Fluxo completo visitante (E2E contra API real)', () => {

  test('categorias → lista → fornecedores → comparação → exportação PDF', async ({ page }) => {
    await page.goto('/');
    await page.waitForTimeout(1000);

    // ---------- Passo 1: Categorias ----------
    await page.click('[data-action="nav-nova"]');
    await page.waitForSelector('text=Selecione as categorias', { state: 'visible' });
    await page.click('[data-catcard="1"] input');
    await page.click('#btn-to-lista');

    // ---------- Passo 2: Lista ----------
    await page.waitForSelector('#nome-lista');
    await page.fill('#nome-lista', 'Lista E2E');
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
    await page.click('text=Ver vencedora');
    await page.waitForSelector('.win-hero h2', { state: 'visible' });

    // ---------- Exportar PDF (RF17 — visitante) ----------
    const downloadPromise = page.waitForEvent('download');
    await page.click('text=Exportar PDF');
    const download = await downloadPromise;
    expect(download.suggestedFilename()).toMatch(/^lista_\d{8}\.pdf$/);
  });

});
