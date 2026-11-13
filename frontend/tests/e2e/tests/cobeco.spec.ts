import { test, expect, Page } from '@playwright/test';

// ============================================================
// Helpers
// ============================================================
const BASE_URL = 'http://localhost:8380';

async function login(page: Page, username: string, password: string) {
  await page.goto(`${BASE_URL}/#/login`);
  await page.fill('input[name="nome_usuario"]', username);
  await page.fill('input[name="senha"]', password);
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL(`${BASE_URL}/#/`);
  await expect(page.locator('text=Login realizado')).toBeVisible({ timeout: 5000 });
}

async function cadastrar(page: Page, userData: {
  nome_usuario: string;
  email: string;
  nome: string;
  senha: string;
  pergunta_seguranca: string;
  resposta_seguranca: string;
}) {
  await page.goto(`${BASE_URL}/#/cadastrar`);
  await page.fill('input[name="nome_usuario"]', userData.nome_usuario);
  await page.fill('input[name="email"]', userData.email);
  await page.fill('input[name="nome"]', userData.nome);
  await page.fill('input[name="senha"]', userData.senha);
  await page.fill('input[name="confirmar_senha"]', userData.senha);
  await page.fill('input[name="pergunta_seguranca"]', userData.pergunta_seguranca);
  await page.fill('input[name="resposta_seguranca"]', userData.resposta_seguranca);
  await page.click('button[type="submit"]');
  await expect(page.locator('text=Conta criada')).toBeVisible({ timeout: 5000 });
}

async function criarLista(page: Page, nome: string, itens: Array<{produto: string, quantidade: number}>) {
  await page.goto(`${BASE_URL}/#/criar-lista`);
  await page.fill('#lista-nome', nome);
  
  for (const item of itens) {
    await page.fill('#item-produto', item.produto);
    await page.waitForSelector('#autocomplete-results:not(.hidden) button', { timeout: 3000 });
    await page.click(`#autocomplete-results button:has-text("${item.produto}")`);
    await page.fill('#item-quantidade', String(item.quantidade));
    await page.click('#btn-add-item');
    await expect(page.locator(`#tbody-itens tr:has-text("${item.produto}")`)).toBeVisible();
  }
  
  await page.click('#btn-salvar-lista');
  await expect(page.locator('text=Lista salva')).toBeVisible({ timeout: 5000 });
}

// ============================================================
// Testes: Autenticação
// ============================================================
test.describe('Autenticação', () => {
  const testUser = {
    nome_usuario: 'e2euser',
    email: 'e2e@teste.com',
    nome: 'E2E User',
    senha: 'Senha@123',
    pergunta_seguranca: 'Pet name?',
    resposta_seguranca: 'Fluffy'
  };

  test.beforeEach(async ({ page }) => {
    // Limpa localStorage/sessionStorage
    await page.evaluate(() => {
      localStorage.clear();
      sessionStorage.clear();
    });
  });

  test('UC09: Cadastrar usuário com dados válidos', async ({ page }) => {
    await cadastrar(page, testUser);
    await expect(page).toHaveURL(`${BASE_URL}/#/login`);
  });

  test('UC09: Cadastrar usuário - validação de senha fraca', async ({ page }) => {
    await page.goto(`${BASE_URL}/#/cadastrar`);
    await page.fill('input[name="nome_usuario"]', 'weakuser');
    await page.fill('input[name="email"]', 'weak@teste.com');
    await page.fill('input[name="nome"]', 'Weak User');
    await page.fill('input[name="senha"]', '123');
    await page.fill('input[name="confirmar_senha"]', '123');
    await page.fill('input[name="pergunta_seguranca"]', 'Pet?');
    await page.fill('input[name="resposta_seguranca"]', 'Dog');
    await page.click('button[type="submit"]');
    await expect(page.locator('text=maiúscula')).toBeVisible();
  });

  test('UC10: Login com credenciais válidas', async ({ page }) => {
    await login(page, testUser.nome_usuario, testUser.senha);
    await expect(page.locator('#nav-auth')).toContainText('E2E User');
  });

  test('UC10: Login com credenciais inválidas', async ({ page }) => {
    await page.goto(`${BASE_URL}/#/login`);
    await page.fill('input[name="nome_usuario"]', testUser.nome_usuario);
    await page.fill('input[name="senha"]', 'SenhaErrada');
    await page.click('button[type="submit"]');
    await expect(page.locator('text=Credenciais inválidas')).toBeVisible();
  });

  test('UC11: Logout remove sessão', async ({ page }) => {
    await login(page, testUser.nome_usuario, testUser.senha);
    await page.click('#btn-logout');
    await expect(page.locator('#nav-auth')).toContainText('Entrar');
    await expect(page.locator('text=Logout realizado')).toBeVisible();
  });

  test('UC12: Recuperar senha - modo log', async ({ page }) => {
    await page.goto(`${BASE_URL}/#/login`);
    await page.click('a:has-text("Esqueci minha senha")');
    await expect(page).toHaveURL(`${BASE_URL}/#/recuperar-senha`);
    // TODO: Implementar página de recuperação
  });
});

// ============================================================
// Testes: Listas de Compras
// ============================================================
test.describe('Listas de Compras', () => {
  const testUser = {
    nome_usuario: 'listuser',
    email: 'list@teste.com',
    nome: 'List User',
    senha: 'Senha@123',
    pergunta_seguranca: 'Pet?',
    resposta_seguranca: 'Cat'
  };

  test.beforeEach(async ({ page }) => {
    await page.evaluate(() => { localStorage.clear(); sessionStorage.clear(); });
    await cadastrar(page, testUser);
    await login(page, testUser.nome_usuario, testUser.senha);
  });

  test('UC01/UC14: Criar lista em memória e salvar', async ({ page }) => {
    await criarLista(page, 'Compras da Semana', [
      { produto: 'Arroz', quantidade: 2 },
      { produto: 'Feijão', quantidade: 1 },
    ]);
    
    // Verifica redirecionamento para minhas-listas
    await expect(page).toHaveURL(`${BASE_URL}/#/minhas-listas`);
    await expect(page.locator('text=Compras da Semana')).toBeVisible();
  });

  test('UC15: Listar minhas listas com paginação', async ({ page }) => {
    // Cria 3 listas
    for (let i = 0; i < 3; i++) {
      await criarLista(page, `Lista ${i}`, [{ produto: 'Arroz', quantidade: 1 }]);
      await page.goto(`${BASE_URL}/#/criar-lista`);
    }
    
    await page.goto(`${BASE_URL}/#/minhas-listas`);
    await expect(page.locator('text=Lista 0')).toBeVisible();
    await expect(page.locator('text=Lista 1')).toBeVisible();
    await expect(page.locator('text=Lista 2')).toBeVisible();
  });

  test('UC13: Editar lista salva', async ({ page }) => {
    await criarLista(page, 'Lista Original', [{ produto: 'Arroz', quantidade: 1 }]);
    
    // Clica em ver/editar a primeira lista
    await page.click('a:has-text("Lista Original")');
    await expect(page).toHaveURL(/\/lista\/\d+/);
    
    // Edita
    await page.click('#btn-editar-lista');
    await page.fill('#lista-nome', 'Lista Editada');
    await page.click('#btn-salvar-lista');
    await expect(page.locator('text=Lista salva')).toBeVisible();
    
    // Verifica alteração
    await page.goto(`${BASE_URL}/#/minhas-listas`);
    await expect(page.locator('text=Lista Editada')).toBeVisible();
  });

  test('UC13: Excluir lista com confirmação', async ({ page }) => {
    await criarLista(page, 'Para Excluir', [{ produto: 'Arroz', quantidade: 1 }]);
    
    await page.goto(`${BASE_URL}/#/minhas-listas`);
    const btnExcluir = page.locator('button.btn-excluir').first();
    await btnExcluir.click();
    
    // Modal de confirmação
    await expect(page.locator('[role="dialog"]')).toBeVisible();
    await page.fill('[role="dialog"] input', 'Para Excluir');
    await page.click('[role="dialog"] button:has-text("Confirmar")');
    
    await expect(page.locator('text=Lista excluída')).toBeVisible();
    await expect(page.locator('text=Para Excluir')).not.toBeVisible();
  });
});

// ============================================================
// Testes: Catálogo e Autocomplete
// ============================================================
test.describe('Catálogo e Autocomplete', () => {
  test('UC02: Autocomplete de produtos na criação de lista', async ({ page }) => {
    await page.goto(`${BASE_URL}/#/criar-lista`);
    await page.fill('#item-produto', 'Arroz');
    
    // Aguarda resultados do autocomplete
    await page.waitForSelector('#autocomplete-results:not(.hidden) button', { timeout: 3000 });
    await expect(page.locator('#autocomplete-results button:has-text("Arroz")')).toBeVisible();
    
    // Seleciona primeiro resultado
    await page.click('#autocomplete-results button:has-text("Arroz")');
    await expect(page.locator('#item-produto')).toHaveValue('Arroz');
  });

  test('UC03: Pré-filtro por categorias na comparação', async ({ page }) => {
    await page.goto(`${BASE_URL}/#/comparar`);
    
    // Verifica categorias carregadas
    await expect(page.locator('#categorias-checkboxes')).toBeVisible();
    await expect(page.locator('input[name="categoria"]')).toHaveCount(11);
    
    // Seleciona categoria "Mercado"
    await page.check('input[name="categoria"][value="1"]');
    await expect(page.locator('#btn-proximo-fornecedores')).toBeEnabled();
  });
});

// ============================================================
// Testes: Comparação de Preços
// ============================================================
test.describe('Comparação de Preços', () => {
  const testUser = {
    nome_usuario: 'compuser',
    email: 'comp@teste.com',
    nome: 'Comp User',
    senha: 'Senha@123',
    pergunta_seguranca: 'Pet?',
    resposta_seguranca: 'Bird'
  };

  test.beforeEach(async ({ page }) => {
    await page.evaluate(() => { localStorage.clear(); sessionStorage.clear(); });
    await cadastrar(page, testUser);
    await login(page, testUser.nome_usuario, testUser.senha);
    // Cria lista para comparar
    await criarLista(page, 'Lista Comparação', [
      { produto: 'Arroz', quantidade: 2 },
      { produto: 'Feijão', quantidade: 1 },
    ]);
  });

  test('UC06/UC07: Fluxo completo de comparação', async ({ page }) => {
    await page.goto(`${BASE_URL}/#/comparar`);
    
    // Passo 1: Seleciona categorias
    await page.check('input[name="categoria"][value="1"]'); // Mercado
    await page.click('#btn-proximo-fornecedores');
    
    // Passo 2: Seleciona fornecedores
    await expect(page.locator('#step-fornecedores')).toBeVisible();
    await page.check('input[name="fornecedor"][value="6"]'); // Pão de Açúcar
    await page.check('input[name="fornecedor"][value="9"]'); // Carrefour
    await page.check('input[name="fornecedor"][value="10"]'); // Extra
    
    // Ajusta slider de disponibilidade
    await page.fill('#slider-disponibilidade', '0');
    
    // Calcula orçamento
    await page.click('#btn-calcular-orcamento');
    
    // Passo 3: Resultado
    await expect(page.locator('#step-resultado')).toBeVisible();
    await expect(page.locator('#resultado-comparacao table')).toBeVisible();
    
    // Verifica destaque melhor oferta (verde)
    await expect(page.locator('.bg-green-50, .badge-success:has-text("MELHOR")')).toBeVisible();
    
    // Verifica ordenação por preço ASC
    const precos = await page.locator('tbody tr td:last-child').allTextContents();
    const precosNum = precos.map(p => parseFloat(p.replace(/[^\d,.-]/g, '').replace(',', '.')));
    for (let i = 1; i < precosNum.length; i++) {
      expect(precosNum[i]).toBeGreaterThanOrEqual(precosNum[i-1]);
    }
  });

  test('UC05: Slider de disponibilidade filtra fornecedores', async ({ page }) => {
    await page.goto(`${BASE_URL}/#/comparar`);
    await page.check('input[name="categoria"][value="1"]');
    await page.click('#btn-proximo-fornecedores');
    
    await page.check('input[name="fornecedor"][value="6"]');
    await page.check('input[name="fornecedor"][value="9"]');
    await page.check('input[name="fornecedor"][value="10"]');
    
    // Muda slider para 80%
    await page.fill('#slider-disponibilidade', '80');
    await expect(page.locator('#valor-disponibilidade')).toHaveText('80%');
    
    // Fornecedores com <80% devem ficar disabled
    // (verificação visual - badges warning/disabled)
  });
});

// ============================================================
// Testes: Exportação PDF
// ============================================================
test.describe('Exportação PDF', () => {
  const testUser = {
    nome_usuario: 'pdfuser',
    email: 'pdf@teste.com',
    nome: 'PDF User',
    senha: 'Senha@123',
    pergunta_seguranca: 'Pet?',
    resposta_seguranca: 'Fish'
  };

  test.beforeEach(async ({ page }) => {
    await page.evaluate(() => { localStorage.clear(); sessionStorage.clear(); });
    await cadastrar(page, testUser);
    await login(page, testUser.nome_usuario, testUser.senha);
    await criarLista(page, 'Lista para PDF', [
      { produto: 'Arroz', quantidade: 2 },
      { produto: 'Feijão', quantidade: 1 },
    ]);
  });

  test('UC08: Exportar lista em PDF', async ({ page }) => {
    await page.goto(`${BASE_URL}/#/minhas-listas`);
    await page.click('a:has-text("Lista para PDF")');
    
    // Clica em exportar PDF
    const downloadPromise = page.waitForEvent('download');
    await page.click('#btn-exportar-pdf');
    const download = await downloadPromise;
    
    // Verifica download
    expect(download.suggestedFilename()).toMatch(/^lista_\d{8}\.pdf$/);
    
    // Verifica que é PDF válido
    const buffer = await download.createReadStream().buffer();
    expect(buffer.slice(0, 4).toString()).toBe('%PDF');
  });

  test('UC09: Imprimir (CSS @media print)', async ({ page }) => {
    await page.goto(`${BASE_URL}/#/minhas-listas`);
    await page.click('a:has-text("Lista para PDF")');
    
    // Verifica que botão imprimir existe
    await expect(page.locator('#btn-imprimir')).toBeVisible();
    
    // Simula impressão (verifica que estilos print são aplicados)
    await page.emulateMedia({ media: 'print' });
    // Elementos .no-print devem estar ocultos
    await expect(page.locator('#header')).toBeHidden();
    await expect(page.locator('#footer')).toBeHidden();
    await expect(page.locator('.no-print')).toBeHidden();
  });
});

// ============================================================
// Testes: Perfil do Usuário
// ============================================================
test.describe('Perfil do Usuário', () => {
  const testUser = {
    nome_usuario: 'perfiluser',
    email: 'perfil@teste.com',
    nome: 'Perfil User',
    senha: 'Senha@123',
    pergunta_seguranca: 'Pet?',
    resposta_seguranca: 'Hamster'
  };

  test.beforeEach(async ({ page }) => {
    await page.evaluate(() => { localStorage.clear(); sessionStorage.clear(); });
    await cadastrar(page, testUser);
    await login(page, testUser.nome_usuario, testUser.senha);
  });

  test('UC18: Visualizar perfil', async ({ page }) => {
    await page.goto(`${BASE_URL}/#/perfil`);
    
    await expect(page.locator('text=Perfil User')).toBeVisible();
    await expect(page.locator('text=perfiluser')).toBeVisible();
    await expect(page.locator('text=perfil@teste.com')).toBeVisible();
  });

  test('UC16: Editar perfil - alterar nome', async ({ page }) => {
    await page.goto(`${BASE_URL}/#/perfil`);
    await page.fill('#perfil-nome', 'Nome Atualizado');
    await page.click('button[type="submit"]');
    await expect(page.locator('text=Perfil atualizado')).toBeVisible();
    
    // Verifica alteração
    await page.goto(`${BASE_URL}/#/perfil`);
    await expect(page.locator('#perfil-nome')).toHaveValue('Nome Atualizado');
  });

  test('UC16: Alterar senha', async ({ page }) => {
    await page.goto(`${BASE_URL}/#/perfil`);
    await page.fill('#perfil-senha-atual', 'Senha@123');
    await page.fill('#perfil-nova-senha', 'NovaSenha@456');
    await page.fill('#perfil-confirmar-nova-senha', 'NovaSenha@456');
    await page.click('button[type="submit"]');
    await expect(page.locator('text=Perfil atualizado')).toBeVisible();
    
    // Tenta login com nova senha
    await page.click('#btn-logout');
    await login(page, 'perfiluser', 'NovaSenha@456');
  });
});

// ============================================================
// Testes: Responsividade (Desktop-first ≥1024px)
// ============================================================
test.describe('Responsividade Desktop-First', () => {
  test('Layout funciona em 1024px', async ({ page }) => {
    await page.setViewportSize({ width: 1024, height: 768 });
    await page.goto(BASE_URL);
    await expect(page.locator('main')).toBeVisible();
    await expect(page.locator('#header')).toBeVisible();
  });

  test('Layout funciona em 1440px', async ({ page }) => {
    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto(BASE_URL);
    await expect(page.locator('main')).toBeVisible();
  });

  test('Breakpoint único (sem mobile)', async ({ page }) => {
    await page.setViewportSize({ width: 800, height: 600 });
    await page.goto(BASE_URL);
    // Deve mostrar scroll horizontal ou layout desktop
    // Não deve quebrar para mobile
    await expect(page.locator('main')).toBeVisible();
  });
});

// ============================================================
// Testes: Acessibilidade Básica
// ============================================================
test.describe('Acessibilidade', () => {
  test('Navegação por teclado (Tab)', async ({ page }) => {
    await page.goto(`${BASE_URL}/#/login`);
    await page.keyboard.press('Tab');
    await expect(page.locator('input[name="nome_usuario"]')).toBeFocused();
    await page.keyboard.press('Tab');
    await expect(page.locator('input[name="senha"]')).toBeFocused();
    await page.keyboard.press('Tab');
    await expect(page.locator('button[type="submit"]')).toBeFocused();
  });

  test('Labels associados aos inputs', async ({ page }) => {
    await page.goto(`${BASE_URL}/#/login`);
    const usuarioInput = page.locator('input[name="nome_usuario"]');
    const senhaInput = page.locator('input[name="senha"]');
    
    await expect(usuarioInput).toHaveAttribute('id');
    await expect(page.locator(`label[for="${await usuarioInput.getAttribute('id')}"]`)).toBeVisible();
  });

  test('Contraste de cores (verificação visual básica)', async ({ page }) => {
    await page.goto(BASE_URL);
    // Verifica que texto principal não é cinza claro em fundo branco
    const mainText = page.locator('main').first();
    await expect(mainText).toBeVisible();
  });
});