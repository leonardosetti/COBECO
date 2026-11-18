import { test, expect } from '@playwright/test';

test.use({ baseURL: 'http://localhost:8380' });

test.describe('Fluxo completo visitante (E2E contra API real)', () => {

  test('cadastro → lista → fornecedores → comparação → exportação PDF', async ({ page }) => {
    const un = 'e2e_' + Date.now();
    const email = un + '@teste.com';

    // ---------- Cadastro ----------
    await page.goto('/');
    await page.click('text=Criar conta');
    await page.waitForURL('**/cadastro');
    await page.fill('#c-user', un);
    await page.fill('#c-nome', 'Usuário E2E');
    await page.fill('#c-email', email);
    await page.fill('#c-senha', 'Senha@123');
    await page.fill('#c-conf', 'Senha@123');
    await page.selectOption('#c-perg', 'pet');
    await page.fill('#c-resp', 'Rex');
    await page.click('button[data-primary]:text("Criar conta")');
    await page.waitForResponse((r) => r.url().includes('/auth/cadastrar') && r.status() === 200);

    // ---------- Login ----------
    await page.click('text=Entrar');
    await page.waitForURL('**/login');
    await page.fill('#l-user', un);
    await page.fill('#l-pass', 'Senha@123');
    await page.click('button[data-primary]:text("Entrar")');

    // ---------- Passo 1: Categorias ----------
    await page.click('text=Criar minha lista');
    await page.waitForSelector('.cat-card', { state: 'visible' });
    await page.click('[data-catcard="1"] input'); // Mercado
    await page.click('#btn-to-lista');

    // ---------- Passo 2: Lista ----------
    await page.waitForSelector('#nome-lista');
    await page.fill('#nome-lista', 'Lista E2E');
    // Adiciona produto via autocomplete
    await page.fill('#busca', 'arroz');
    await page.waitForTimeout(350); // debounce
    await page.click('.sug-item', { timeout: 5000 });
    await page.waitForSelector('#itens-box tbody tr', { state: 'visible' });
    await page.click('#btn-to-forn');

    // ---------- Passo 3: Fornecedores ----------
    await page.waitForSelector('.forn-card', { state: 'visible' });
    // Seleciona os 2 primeiros fornecedores elegíveis
    const cards = page.locator('.forn-card input.forn-cb:not(:disabled)');
    await cards.first().check();
    await cards.nth(1).check();
    await page.click('#btn-calc');

    // ---------- Passo 4: Resultados ----------
    await page.waitForSelector('.kpi win', { state: 'visible', timeout: 15000 });
    const vencedorNome = page.locator('.card.kpi.win .v');
    await expect(vencedorNome).not.toBeEmpty();

    // ---------- Passo 5: Lista vencedora ----------
    await page.click('text=Ver lista vencedora');
    await page.waitForSelector('.win-hero h2', { state: 'visible' });

    // ---------- Exportar PDF ----------
    const downloadPromise = page.waitForEvent('download');
    await page.click('text=Exportar PDF');
    const download = await downloadPromise;
    expect(download.suggestedFilename()).toMatch(/^lista_\d{8}\.pdf$/);
  });

});
