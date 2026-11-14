import { test, expect } from '../../fixtures/test-fixtures';
import { createTestUser } from '../../utils/test-data';

test.describe('Navegação e Roteamento (Hash-based)', () => {
  test.describe('Hash Navigation', () => {
    test('deve navegar para rotas principais via hash', async ({ page }) => {
      const rotas = [
        { hash: '#/login', seletor: 'input[name="nome_usuario"]' },
        { hash: '#/cadastrar', seletor: 'input[name="nome_usuario"]' },
        { hash: '#/recuperar-senha', seletor: 'input[name="nome_usuario"]' },
      ];

      for (const rota of rotas) {
        await page.goto(rota.hash);
        await page.waitForLoadState('networkidle');
        await expect(page.locator(rota.seletor)).toBeVisible({ timeout: 5000 });
      }
    });

    test('deve normalizar /home para /', async ({ page }) => {
      await page.goto('/#/home');
      await page.waitForLoadState('networkidle');
      expect(page.url()).toContain('#/');
    });

    test('deve redirecionar rota inexistente para home', async ({ page }) => {
      await page.goto('/#/rota-inexistente-xyz');
      await page.waitForLoadState('networkidle');
      expect(page.url()).toMatch(/#\/$/);
    });

    test('deve manter histórico do browser (voltar/avançar)', async ({ page, cadastroPage, loginPage }) => {
      await cadastroPage.goto();
      await cadastroPage.cadastrar(createTestUser());
      
      await loginPage.goto();
      await loginPage.login('testuser', 'Senha@123');
      
      // Navega para várias páginas
      await page.goto('/#/minhas-listas');
      await page.waitForLoadState('networkidle');
      
      await page.goto('/#/criar-lista');
      await page.waitForLoadState('networkidle');
      
      // Volta
      await page.goBack();
      await page.waitForLoadState('networkidle');
      expect(page.url()).toContain('#/minhas-listas');
      
      // Avança
      await page.goForward();
      await page.waitForLoadState('networkidle');
      expect(page.url()).toContain('#/criar-lista');
    });
  });

  test.describe('Deep Links', () => {
    test('deve acessar lista específica via deep link', async ({ authenticatedPage, listasPage }) => {
      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      await listasPage.criarLista({ titulo: 'Lista Deep Link' });
      await listasPage.waitForToast('Lista criada');

      const listaId = await listasPage.getListaIdByTitulo('Lista Deep Link');
      expect(listaId).not.toBeNull();

      // Acessa diretamente via URL
      await listasPage.page.goto(`/#/lista/${listaId}`);
      await listasPage.page.waitForLoadState('networkidle');

      await expect(listasPage.page.locator('h1, h2, .lista-titulo')).toContainText('Lista Deep Link');
    });

    test('deve acessar edição de lista via deep link', async ({ authenticatedPage, listasPage }) => {
      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      await listasPage.criarLista({ titulo: 'Lista Editar Deep Link' });
      await listasPage.waitForToast('Lista criada');

      const listaId = await listasPage.getListaIdByTitulo('Lista Editar Deep Link');
      expect(listaId).not.toBeNull();

      await listasPage.page.goto(`/#/editar-lista/${listaId}`);
      await listasPage.page.waitForLoadState('networkidle');

      await expect(listasPage.page.locator('#lista-nome')).toHaveValue('Lista Editar Deep Link');
    });

    test('deve acessar comparação via deep link', async ({ authenticatedPage, listasPage }) => {
      await listasPage.page.goto('/#/comparar');
      await listasPage.page.waitForLoadState('networkidle');
      
      await expect(listasPage.page.locator('h1, h2')).toContainText(/comparação|comparar/i);
    });

    test('deve acessar exportação via deep link', async ({ authenticatedPage, listasPage }) => {
      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      await listasPage.criarLista({ titulo: 'Lista Export Deep' });
      await listasPage.waitForToast('Lista criada');

      const listaId = await listasPage.getListaIdByTitulo('Lista Export Deep');
      expect(listaId).not.toBeNull();

      // Acessa URL de exportação diretamente
      const downloadPromise = listasPage.page.waitForEvent('download');
      await listasPage.page.goto(`/#/export/lista/${listaId}/pdf`);
      const download = await downloadPromise;
      
      expect(download).toBeTruthy();
    });
  });

  test.describe('Guards de Autenticação', () => {
    test('deve redirecionar para login se acessar rota protegida sem auth', async ({ page }) => {
      await page.goto('/#/minhas-listas');
      await page.waitForLoadState('networkidle');
      
      // Deve redirecionar para login
      await expect(page.locator('input[name="nome_usuario"]')).toBeVisible({ timeout: 5000 });
      expect(page.url()).toContain('#/login');
    });

    test('deve redirecionar para login se acessar criar lista sem auth', async ({ page }) => {
      await page.goto('/#/criar-lista');
      await page.waitForLoadState('networkidle');
      
      await expect(page.locator('input[name="nome_usuario"]')).toBeVisible({ timeout: 5000 });
    });

    test('deve redirecionar para login se acessar perfil sem auth', async ({ page }) => {
      await page.goto('/#/perfil');
      await page.waitForLoadState('networkidle');
      
      await expect(page.locator('input[name="nome_usuario"]')).toBeVisible({ timeout: 5000 });
    });

    test('deve permitir acesso a rotas públicas sem auth', async ({ page }) => {
      const publicRoutes = ['/#/login', '/#/cadastrar', '/#/recuperar-senha'];
      
      for (const route of publicRoutes) {
        await page.goto(route);
        await page.waitForLoadState('networkidle');
        
        // Não deve redirecionar para login
        await expect(page.locator('input[name="nome_usuario"]')).toBeVisible({ timeout: 5000 });
        expect(page.url()).toContain(route.replace('/#', '#'));
      }
    });

    test('deve permitir acesso a exportação PDF sem auth', async ({ page, listasPage, cadastroPage, loginPage }) => {
      // Cria lista autenticado
      const userData = createTestUser();
      await cadastroPage.goto();
      await cadastroPage.cadastrar(userData);
      await loginPage.goto();
      await loginPage.login(userData.nome_usuario, userData.senha);

      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      await listasPage.criarLista({ titulo: 'Lista Pública PDF' });
      await listasPage.waitForToast('Lista criada');

      const listaId = await listasPage.getListaIdByTitulo('Lista Pública PDF');
      expect(listaId).not.toBeNull();

      // Logout
      await page.goto('/#/perfil');
      await page.waitForLoadState('networkidle');
      await page.locator('#btn-logout').click();
      await page.waitForLoadState('networkidle');

      // Acessa exportação sem auth
      const downloadPromise = page.waitForEvent('download');
      await page.goto(`/#/export/lista/${listaId}/pdf`);
      const download = await downloadPromise;
      
      expect(download).toBeTruthy();
    });
  });

  test.describe('Navegação via Header/Menu', () => {
    test('deve navegar via links do header', async ({ authenticatedPage, listasPage }) => {
      // Testa navegação via menu do header
      const headerLinks = [
        { seletor: '[data-link="/minhas-listas"], a[href="#/minhas-listas"]', url: '/minhas-listas' },
        { seletor: '[data-link="/criar-lista"], a[href="#/criar-lista"]', url: '/criar-lista' },
        { seletor: '[data-link="/comparar"], a[href="#/comparar"]', url: '/comparar' },
        { seletor: '[data-link="/perfil"], a[href="#/perfil"]', url: '/perfil' },
      ];

      for (const link of headerLinks) {
        await listasPage.page.locator(link.seletor).click();
        await listasPage.page.waitForLoadState('networkidle');
        expect(listasPage.page.url()).toContain(`#${link.url}`);
      }
    });

    test('deve mostrar menu de usuário logado no header', async ({ authenticatedPage }) => {
      await expect(authenticatedPage.locator('#nav-auth .usuario-nome, #nav-auth .dropdown, .usuario-menu')).toBeVisible({ timeout: 5000 });
    });
  });
});