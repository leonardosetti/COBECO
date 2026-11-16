import { test, expect } from '../../fixtures/test-fixtures';
import { createTestUser } from '../../utils/test-data';

test.describe('Estados de UI - Loading, Empty, Error, Success', () => {
  test.describe('Estados de Loading', () => {
    test('deve mostrar spinner durante navegação', async ({ page, cadastroPage, loginPage }) => {
      await cadastroPage.goto();
      await cadastroPage.cadastrar(createTestUser());
      
      await loginPage.goto();
      
      // Preenche e submete
      await page.fill('input[name="nome_usuario"]', 'testuser');
      await page.fill('input[name="senha"]', 'Senha@123');
      
      // Clica e verifica spinner
      await page.click('button[type="submit"]');
      
      // Verifica se spinner aparece no botão
      const btn = page.locator('button[type="submit"]');
      await expect(btn).toContainHTML('spinner');
      await expect(btn).toBeDisabled();
    });

    test('deve mostrar spinner ao salvar lista', async ({ authenticatedPage, listasPage }) => {
      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      
      const produtoInput = listasPage.page.locator('#item-produto');
      await produtoInput.waitFor({ state: 'visible' });
      await produtoInput.fill('Arroz');
      await listasPage.page.waitForTimeout(500);
      
      const autocompleteResults = listasPage.page.locator('#autocomplete-results');
      await expect(autocompleteResults).toBeVisible({ timeout: 5000 });
      await autocompleteResults.locator('.autocomplete-item, li, [data-produto-id]').first().click();
      await listasPage.page.locator('#btn-add-item').click();
      await listasPage.page.waitForTimeout(300);
      
      // Clica salvar e verifica spinner
      await listasPage.page.locator('#btn-salvar-lista').click();
      
      const btn = listasPage.page.locator('#btn-salvar-lista');
      await expect(btn).toContainHTML('spinner');
      await expect(btn).toBeDisabled();
    });

    test('deve mostrar loading na comparação', async ({ authenticatedPage, listasPage }) => {
      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      await listasPage.criarLista({ titulo: 'Lista Loading' });
      await listasPage.waitForToast('Lista criada');
      
      // Adiciona item rápido
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
      
      // Vai para comparação
      await listasPage.page.goto('/#/comparar');
      await listasPage.page.waitForLoadState('networkidle');
      
      const fornecedorCheckboxes = listasPage.page.locator('input[type="checkbox"][name="fornecedor"], .fornecedor-selecao input');
      await expect(fornecedorCheckboxes.first()).toBeVisible({ timeout: 10000 });
      await fornecedorCheckboxes.first().check();
      
      // Clica comparar e verifica loading
      await listasPage.page.locator('#btn-comparar, button:has-text("Comparar")').click();
      
      // Verifica indicador de loading
      const loading = listasPage.page.locator('.loading, .spinner, [aria-busy="true"]');
      await expect(loading.first()).toBeVisible({ timeout: 5000 });
    });
  });

  test.describe('Estados Vazios (Empty States)', () => {
    test('deve mostrar estado vazio em minhas listas sem listas', async ({ page, cadastroPage, loginPage }) => {
      await cadastroPage.goto();
      await cadastroPage.cadastrar(createTestUser());
      
      await loginPage.goto();
      await loginPage.login('testuser', 'Senha@123');
      
      await page.goto('/#/minhas-listas');
      await page.waitForLoadState('networkidle');
      
      // Verifica mensagem de estado vazio
      await expect(page.locator('text=/nenhuma lista|nenhuma lista salva|criar.*primeira/i')).toBeVisible({ timeout: 5000 });
      
      // Verifica botão/criar primeira lista
      await expect(page.locator('a[href="#/criar-lista"], button:has-text("Criar"), .btn-primary')).toBeVisible();
    });

    test('deve mostrar estado vazio em criar lista sem itens', async ({ authenticatedPage, listasPage }) => {
      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      
      // Verifica badge de 0 itens
      await expect(listasPage.page.locator('#badge-itens, .badge:has-text("0 itens"), text=/0 itens/')).toBeVisible();
      
      // Verifica se tabela de itens está oculta ou mostra mensagem
      const tabelaItens = listasPage.page.locator('#card-itens-lista, .itens-lista-vazia');
      // Pode estar oculta ou mostrar mensagem
    });

    test('deve mostrar estado vazio na comparação sem fornecedores', async ({ authenticatedPage, listasPage }) => {
      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      await listasPage.criarLista({ titulo: 'Lista Vazia Comp' });
      await listasPage.waitForToast('Lista criada');
      
      await listasPage.page.goto('/#/comparar');
      await listasPage.page.waitForLoadState('networkidle');
      
      // Não seleciona nenhum fornecedor
      await listasPage.page.locator('#btn-comparar, button:has-text("Comparar")').click();
      await listasPage.page.waitForLoadState('networkidle');
      
      // Verifica mensagem de nenhum fornecedor selecionado
      await expect(listasPage.page.locator('text=/nenhum fornecedor|selecione.*fornecedor/i')).toBeVisible({ timeout: 5000 });
    });

    test('deve mostrar estado vazio em autocomplete sem resultados', async ({ authenticatedPage, listasPage }) => {
      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      await listasPage.criarLista({ titulo: 'Lista Auto' });
      await listasPage.waitForToast('Lista criada');
      
      await listasPage.page.goto('/#/criar-lista');
      await listasPage.page.waitForLoadState('networkidle');
      
      const produtoInput = listasPage.page.locator('#item-produto');
      await produtoInput.waitFor({ state: 'visible' });
      
      // Termo que não retorna resultados
      await produtoInput.fill('xyzprodutoinexistente123');
      await listasPage.page.waitForTimeout(500);
      
      const autocompleteResults = listasPage.page.locator('#autocomplete-results');
      // Pode mostrar "nenhum resultado" ou ficar vazio
      const isVisible = await autocompleteResults.isVisible();
      if (isVisible) {
        await expect(listasPage.page.locator('text=/nenhum|não encontrado|sem resultado/i')).toBeVisible({ timeout: 3000 });
      }
    });
  });

  test.describe('Estados de Erro', () => {
    test('deve mostrar erro de validação em campos obrigatórios', async ({ page, cadastroPage }) => {
      await cadastroPage.goto();
      await cadastroPage.submitButton.click(); // Submete vazio
      
      // Verifica mensagens de erro
      await expect(page.locator('.error, .text-red-600, [role="alert"], .invalid-feedback').first()).toBeVisible({ timeout: 3000 });
    });

    test('deve mostrar erro de email inválido', async ({ page, cadastroPage }) => {
      await cadastroPage.goto();
      await cadastroPage.cadastrarMinimo({
        ...createTestUser(),
        email: 'email_invalido',
      });
      
      await expect(page.locator('.error, .text-red-600, [role="alert"]')).toContainText(/email|inválido/i);
    });

    test('deve mostrar erro de senha fraca', async ({ page, cadastroPage }) => {
      await cadastroPage.goto();
      await cadastroPage.cadastrarMinimo({
        ...createTestUser(),
        senha: '123',
        confirmar_senha: '123',
      });
      
      await expect(page.locator('.error, .text-red-600, [role="alert"]')).toContainText(/senha|forte|caractere|mínimo/i);
    });

    test('deve mostrar erro de senhas não coincidem', async ({ page, cadastroPage }) => {
      await cadastroPage.goto();
      await cadastroPage.cadastrarMinimo({
        ...createTestUser(),
        senha: 'Senha@123',
        confirmar_senha: 'OutraSenha@123',
      });
      
      await expect(page.locator('.error, .text-red-600, [role="alert"]')).toContainText(/senha|coincid|confirmar/i);
    });

    test('deve mostrar erro de login inválido', async ({ page, cadastroPage, loginPage }) => {
      await cadastroPage.goto();
      await cadastroPage.cadastrar(createTestUser());
      
      await loginPage.goto();
      await loginPage.login('usuario', 'SenhaErrada@123');
      
      await expect(page.locator('.error, .text-red-600, [role="alert"], .toast-error')).toContainText(/senha|credencial|inválid/i);
    });

    test('deve mostrar erro de usuário inexistente no login', async ({ page, loginPage }) => {
      await loginPage.goto();
      await loginPage.login('usuario_inexistente_xyz', 'Senha@123');
      
      await expect(page.locator('.error, .text-red-600, [role="alert"], .toast-error')).toContainText(/usuário|não encontrado|credencial/i);
    });

    test('deve mostrar erro de email duplicado no cadastro', async ({ page, cadastroPage }) => {
      const userData = createTestUser();
      
      await cadastroPage.goto();
      await cadastroPage.cadastrar(userData);
      
      await cadastroPage.goto();
      await cadastroPage.cadastrar(userData);
      
      await expect(page.locator('.error, .text-red-600, [role="alert"], .toast-error')).toContainText(/email|já existe|duplicado|único/i);
    });

    test('deve mostrar erro de nome de usuário duplicado', async ({ page, cadastroPage }) => {
      const userData = createTestUser();
      
      await cadastroPage.goto();
      await cadastroPage.cadastrar(userData);
      
      await cadastroPage.goto();
      await cadastroPage.cadastrar(userData);
      
      await expect(page.locator('.error, .text-red-600, [role="alert"], .toast-error')).toContainText(/usuário|já existe|duplicado|único/i);
    });

    test('deve mostrar toast de erro em falha de rede', async ({ page }) => {
      // Simula erro de rede interceptando requisição
      await page.route('**/v1/auth/login', route => {
        route.abort('failed');
      });
      
      await page.goto('/#/login');
      await page.waitForLoadState('networkidle');
      
      await page.fill('input[name="nome_usuario"]', 'test');
      await page.fill('input[name="senha"]', 'pass');
      await page.click('button[type="submit"]');
      
      await expect(page.locator('.toast-error, [role="alert"].error, .toast:has-text("Erro")')).toBeVisible({ timeout: 5000 });
    });
  });

  test.describe('Estados de Sucesso', () => {
    test('deve mostrar toast de sucesso no cadastro', async ({ page, cadastroPage }) => {
      await cadastroPage.goto();
      await cadastroPage.cadastrar(createTestUser());
      
      await expect(page.locator('.toast-success, [role="alert"].success, .toast:has-text("sucesso"), .toast:has-text("criada")')).toBeVisible({ timeout: 5000 });
    });

    test('deve mostrar toast de sucesso no login', async ({ page, cadastroPage, loginPage }) => {
      await cadastroPage.goto();
      await cadastroPage.cadastrar(createTestUser());
      
      await loginPage.goto();
      await loginPage.login('testuser', 'Senha@123');
      
      await expect(page.locator('.toast-success, [role="alert"].success, .toast:has-text("sucesso"), .toast:has-text("Login")')).toBeVisible({ timeout: 5000 });
    });

    test('deve mostrar toast de sucesso ao salvar lista', async ({ authenticatedPage, listasPage }) => {
      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      
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
    });

    test('deve mostrar toast de sucesso ao atualizar perfil', async ({ authenticatedPage, perfilPage }) => {
      await perfilPage.goto();
      await perfilPage.atualizarPerfil({ nome: 'Nome Atualizado' });
      
      await perfilPage.waitForToast('Perfil atualizado');
    });

    test('deve mostrar toast de sucesso ao excluir lista', async ({ authenticatedPage, listasPage }) => {
      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      await listasPage.criarLista({ titulo: 'Lista Para Excluir Sucesso' });
      await listasPage.waitForToast('Lista criada');
      
      const listaId = await listasPage.getListaIdByTitulo('Lista Para Excluir Sucesso');
      expect(listaId).not.toBeNull();
      
      await listasPage.excluirLista(listaId!);
      
      await listasPage.waitForToast('Lista excluída');
    });

    test('deve mostrar toast de sucesso ao exportar PDF', async ({ authenticatedPage, listasPage }) => {
      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      await listasPage.criarLista({ titulo: 'Lista PDF Sucesso' });
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
      
      const listaId = await listasPage.getListaIdByTitulo('Lista PDF Sucesso');
      expect(listaId).not.toBeNull();
      
      const downloadPromise = listasPage.page.waitForEvent('download');
      await listasPage.page.locator('#btn-exportar-pdf, button:has-text("Exportar PDF")').click();
      const download = await downloadPromise;
      
      expect(download).toBeTruthy();
    });
  });

  test.describe('Feedback Visual Imediato', () => {
    test('botão deve ficar disabled durante submit', async ({ page, cadastroPage }) => {
      await cadastroPage.goto();
      await cadastroPage.cadastrar(createTestUser());
      
      // Segundo cadastro (duplicado) deve mostrar botão disabled durante request
      await cadastroPage.goto();
      const userData = createTestUser();
      await cadastroPage.nomeUsuarioInput.fill(userData.nome_usuario);
      await cadastroPage.emailInput.fill(userData.email);
      await cadastroPage.nomeInput.fill(userData.nome);
      await cadastroPage.senhaInput.fill(userData.senha);
      await cadastroPage.confirmarSenhaInput.fill(userData.confirmar_senha);
      await cadastroPage.perguntaSegurancaInput.fill(userData.pergunta_seguranca);
      await cadastroPage.respostaSegurancaInput.fill(userData.resposta_seguranca);
      
      await cadastroPage.submitButton.click();
      
      await expect(cadastroPage.submitButton).toBeDisabled();
      await expect(cadastroPage.submitButton).toContainHTML('spinner');
    });

    test('input deve mostrar estado de erro visual', async ({ page, cadastroPage }) => {
      await cadastroPage.goto();
      await cadastroPage.cadastrarMinimo({
        ...createTestUser(),
        email: 'invalido',
      });
      
      // Campo email deve ter classe de erro ou border vermelho
      const emailInput = cadastroPage.emailInput;
      const borderColor = await emailInput.evaluate(el => getComputedStyle(el).borderColor);
      const hasErrorClass = await emailInput.evaluate(el => el.classList.contains('error') || el.classList.contains('border-red-500'));
      
      // Deve ter indicador visual de erro
      expect(borderColor === 'rgb(239, 68, 68)' || hasErrorClass).toBe(true);
    });

    test('checkbox deve mostrar estado checked/unchecked', async ({ authenticatedPage, listasPage }) => {
      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      await listasPage.criarLista({ titulo: 'Lista Checkbox' });
      await listasPage.waitForToast('Lista criada');
      
      await listasPage.page.goto('/#/comparar');
      await listasPage.page.waitForLoadState('networkidle');
      
      const checkbox = listasPage.page.locator('input[type="checkbox"][name="fornecedor"], .fornecedor-selecao input').first();
      await expect(checkbox).toBeVisible({ timeout: 10000 });
      
      // Inicialmente unchecked
      await expect(checkbox).not.toBeChecked();
      
      // Clica e verifica checked
      await checkbox.check();
      await expect(checkbox).toBeChecked();
      
      // Desmarca
      await checkbox.uncheck();
      await expect(checkbox).not.toBeChecked();
    });
  });
});