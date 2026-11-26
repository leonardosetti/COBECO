import { test, expect } from '@playwright/test';

test.use({ baseURL: 'http://localhost:8380' });

test.describe('Jornada efêmera (RF22-RF28)', () => {

  test('RF24 — Navbar fixa com link Início visível em todas as views', async ({ page }) => {
    await page.goto('/');
    await page.click('[data-action="nav-nova"]');
    await page.waitForSelector('text=Selecione as categorias', { state: 'visible' });
    // Navbar: link Início no header (qualificado para não pegar o botão "← Voltar" da view)
    await expect(page.locator('header [data-action="nav-home"]')).toBeVisible();
    await page.click('header [data-action="nav-home"]');
    // Voltou ao home: CTA "Criar minha lista" visível
    await expect(page.locator('text=Criar minha lista')).toBeVisible();
  });

  test('RF27/RF28 — Pré-filtro de grandes áreas multi-seleção filtra categorias', async ({ page }) => {
    await page.goto('/');
    await page.click('[data-action="nav-nova"]');
    await page.waitForSelector('text=Selecione as categorias', { state: 'visible' });

    // Inicialmente mostra categorias (>= 1, número real depende do seed)
    await page.waitForSelector('[data-catcard]', { state: 'visible', timeout: 10000 });
    const totalInicial = await page.locator('[data-catcard]').count();
    expect(totalInicial).toBeGreaterThan(0);

    // Seleciona a área "Supermercado" (primeiro checkbox de área) -> filtra categorias
    await page.locator('.area-cb-input').first().check();
    await page.waitForTimeout(600);
    const aposSupermercado = await page.locator('[data-catcard]').count();
    expect(aposSupermercado).toBeLessThan(totalInicial);
    expect(aposSupermercado).toBeGreaterThan(0);

    // Marca tambem a segunda área (multi-selecao) -> mostra mais categorias (uniao)
    await page.locator('.area-cb-input').nth(1).check();
    await page.waitForTimeout(600);
    const aposDuasAreas = await page.locator('[data-catcard]').count();
    expect(aposDuasAreas).toBeGreaterThanOrEqual(aposSupermercado);

    // Limpar áreas volta a mostrar todas (categorias reaparecem)
    await page.click('[data-action="area-limpar"]');
    await page.waitForTimeout(1000);
    const aposLimpar = await page.locator('[data-catcard]').count();
    expect(aposLimpar).toBeGreaterThan(0);
    expect(aposLimpar).toBeGreaterThanOrEqual(aposDuasAreas);
  });

  test('RF26 — Busca semântica nunca esconde categorias já selecionadas', async ({ page }) => {
    await page.goto('/');
    await page.click('[data-action="nav-nova"]');
    await page.waitForSelector('text=Selecione as categorias', { state: 'visible' });

    // Seleciona "Mercado" (id 1)
    await page.click('[data-catcard="1"] input');
    await expect(page.locator('[data-catcard="1"]')).toHaveClass(/sel/);

    // Busca por termo que nao bate em Mercado (ex.: "informatica") -> Mercado continua visível
    await page.fill('#busca-cat', 'informatica');
    await page.waitForTimeout(700);
    await expect(page.locator('[data-catcard="1"]')).toBeVisible();
    await expect(page.locator('[data-catcard="1"] input')).toBeChecked();
  });

  test('RF25 — Modal Sim/Não ao voltar ao início com rascunho em andamento', async ({ page }) => {
    await page.goto('/');
    await page.click('[data-action="nav-nova"]');
    await page.waitForSelector('text=Selecione as categorias', { state: 'visible' });

    // Cria rascunho: seleciona categoria e vai para lista, adiciona item
    await page.click('[data-catcard="1"] input');
    await page.click('#btn-to-lista');
    await page.waitForSelector('#nome-lista');
    await page.fill('#nome-lista', 'Rascunho E2E');
    await page.evaluate(() => {
      window.state.lista.itens.push({ pid: 1, qtd: 1 });
      window.refreshListaUI();
    });
    await page.waitForSelector('#itens-box tbody tr', { state: 'visible' });

    // Tenta voltar ao início -> deve abrir modal Sim/Não
    await page.click('[data-action="nav-home"]');
    await page.waitForTimeout(500);
    const modal = page.locator('.modal-overlay');
    await expect(modal).toBeVisible();
    await expect(page.locator('text=Esquecer lista em andamento')).toBeVisible();

    // Clicar "Não — manter" -> cancela navegação, permanece na lista com rascunho
    await page.click('[data-action="modal-cancel"]');
    await page.waitForTimeout(400);
    await expect(page.locator('#nome-lista')).toHaveValue('Rascunho E2E');
    await expect(page.locator('text=Passo 2 de 5')).toBeVisible();
  });

  test('RF22/RF23 — Concluir lista exportando PDF volta ao início e retém lista em sessionStorage', async ({ page }) => {
    await page.goto('/');
    await page.click('[data-action="nav-nova"]');
    await page.waitForSelector('text=Selecione as categorias', { state: 'visible' });

    // Passo 1: categorias
    await page.click('[data-catcard="1"] input');
    await page.click('#btn-to-lista');

    // Passo 2: lista
    await page.waitForSelector('#nome-lista');
    await page.fill('#nome-lista', 'Lista Concluída E2E');
    await page.evaluate(() => {
      window.state.lista.itens.push({ pid: 1, qtd: 1 });
      window.refreshListaUI();
    });
    await page.waitForSelector('#itens-box tbody tr', { state: 'visible' });
    await page.click('#btn-to-forn');

    // Passo 3: fornecedores (seleciona 2 elegiveis)
    await page.waitForSelector('.forn-card', { state: 'visible' });
    await page.evaluate(() => {
      const ids = Array.from(document.querySelectorAll('[data-forncard]')).map(el => +el.dataset.forncard).slice(0, 2);
      window.state.fornecedores = ids;
      window.refreshFornecedores();
    });
    await page.click('#btn-calc');

    // Passo 4: resultados
    await page.waitForSelector('text=Passo 4 de 5', { state: 'visible', timeout: 15000 });

    // Passo 5: vencedora
    await page.click('[data-action="ver-vencedora"]');
    await page.waitForSelector('.win-hero h2', { state: 'visible' });

    // Exportar PDF -> conclui jornada
    const downloadPromise = page.waitForEvent('download');
    await page.click('[data-action="export-pdf"]');
    const download = await downloadPromise;
    expect(download.suggestedFilename()).toMatch(/^lista_\d{8}\.pdf$/);

    // Deve voltar ao Início (RF22)
    await expect(page.locator('text=Criar minha lista')).toBeVisible({ timeout: 10000 });

    // sessionStorage deve reter lista gerada (RF23)
    const gerada = await page.evaluate(() => {
      const d = JSON.parse(sessionStorage.getItem('cobeco_jornada') || '{}');
      return d.gerada ? d.gerada.lista.nome : null;
    });
    expect(gerada).toBe('Lista Concluída E2E');

    // Rascunho deve estar limpo (RF22)
    const rascunho = await page.evaluate(() => {
      const d = JSON.parse(sessionStorage.getItem('cobeco_jornada') || '{}');
      return (d.rascunho?.lista?.itens || []).length;
    });
    expect(rascunho).toBe(0);
  });

});
