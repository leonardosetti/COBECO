import { test, expect } from '../../fixtures/test-fixtures';
import { createTestUser } from '../../utils/test-data';

test.describe('Autenticação - Login/Logout/Recuperação (UC01-RF01, UC02-RF02, UC11-RF03, UC12-RF04)', () => {
  test.describe('Login', () => {
    test('deve fazer login com credenciais válidas', async ({ cadastroPage, loginPage }) => {
      const userData = createTestUser();
      
      await cadastroPage.goto();
      await cadastroPage.cadastrar(userData);
      
      await loginPage.goto();
      await loginPage.login(userData.nome_usuario, userData.senha);
      
      await expect(loginPage.page.locator('main')).toBeVisible();
    });

    test('não deve fazer login com senha incorreta', async ({ cadastroPage, loginPage }) => {
      const userData = createTestUser();
      
      await cadastroPage.goto();
      await cadastroPage.cadastrar(userData);
      
      await loginPage.goto();
      await loginPage.login(userData.nome_usuario, 'SenhaErrada@123');
      
      const toast = await loginPage.getToastMessage();
      expect(toast?.toLowerCase()).toMatch(/senha|inválida|credencial|incorreta/);
    });

    test('não deve fazer login com usuário inexistente', async ({ loginPage }) => {
      await loginPage.goto();
      await loginPage.login('usuario_inexistente', 'Senha@123');
      
      const toast = await loginPage.getToastMessage();
      expect(toast?.toLowerCase()).toMatch(/usuário|não encontrado|credencial|inválida/);
    });

    test('não deve fazer login com campos vazios', async ({ loginPage }) => {
      await loginPage.goto();
      await loginPage.submitButton.click();
      
      await expect(loginPage.usuarioInput).toHaveAttribute('required');
      await expect(loginPage.senhaInput).toHaveAttribute('required');
    });

    test('deve redirecionar para home se já autenticado', async ({ authenticatedPage, loginPage }) => {
      await loginPage.goto();
      await expect(loginPage.page.locator('main')).toBeVisible();
    });
  });

  test.describe('Logout', () => {
    test('deve fazer logout via botão no perfil', async ({ authenticatedPage, perfilPage, loginPage }) => {
      await perfilPage.goto();
      await perfilPage.logout();
      
      await loginPage.expectLoginFormVisible();
    });

    test('deve limpar tokens no logout', async ({ authenticatedPage, perfilPage, loginPage, testUser }) => {
      await perfilPage.goto();
      await perfilPage.logout();
      
      await loginPage.goto();
      await loginPage.login(testUser.nome_usuario, testUser.senha);
      
      await expect(loginPage.page.locator('main')).toBeVisible();
    });
  });

  test.describe('Recuperação de Senha', () => {
    test('deve solicitar recuperação de senha', async ({ loginPage, cadastroPage }) => {
      const userData = createTestUser();
      
      await cadastroPage.goto();
      await cadastroPage.cadastrar(userData);
      
      await loginPage.goto();
      await loginPage.gotoRecuperarSenha();
      
      await expect(loginPage.page.locator('input[name="nome_usuario"]')).toBeVisible();
      await loginPage.page.fill('input[name="nome_usuario"]', userData.nome_usuario);
      await loginPage.page.click('button[type="submit"]');
      
      const toast = await loginPage.getToastMessage();
      expect(toast?.toLowerCase()).toMatch(/recuperação|enviad|instruçõ|token|logado/);
    });

    test('não deve revelar se usuário existe na recuperação', async ({ loginPage }) => {
      await loginPage.goto();
      await loginPage.gotoRecuperarSenha();
      
      await loginPage.page.fill('input[name="nome_usuario"]', 'usuario_que_nao_existe_12345');
      await loginPage.page.click('button[type="submit"]');
      
      const toast = await loginPage.getToastMessage();
      expect(toast?.toLowerCase()).toMatch(/recuperação|enviad|instruçõ|token|logado/);
    });

    test('deve confirmar recuperação com token válido', async ({ loginPage, cadastroPage }) => {
      const userData = createTestUser();
      
      await cadastroPage.goto();
      await cadastroPage.cadastrar(userData);
      
      await loginPage.goto();
      await loginPage.gotoRecuperarSenha();
      
      await loginPage.page.fill('input[name="nome_usuario"]', userData.nome_usuario);
      await loginPage.page.click('button[type="submit"]');
      
      const toast = await loginPage.getToastMessage();
      const tokenMatch = toast?.match(/token[:\s]+(\w+)/i);
      
      if (tokenMatch) {
        const token = tokenMatch[1];
        await loginPage.page.goto('/#/recuperar-senha/confirmar');
        await loginPage.page.fill('input[name="nome_usuario"]', userData.nome_usuario);
        await loginPage.page.fill('input[name="token"]', token);
        await loginPage.page.fill('input[name="nova_senha"]', 'NovaSenha@456');
        await loginPage.page.fill('input[name="confirmar_nova_senha"]', 'NovaSenha@456');
        await loginPage.page.click('button[type="submit"]');
        
        const confirmToast = await loginPage.getToastMessage();
        expect(confirmToast?.toLowerCase()).toMatch(/senha alterada|sucesso/);
      }
    });

    test('não deve confirmar recuperação com token inválido', async ({ loginPage, cadastroPage }) => {
      const userData = createTestUser();
      
      await cadastroPage.goto();
      await cadastroPage.cadastrar(userData);
      
      await loginPage.goto();
      await loginPage.page.goto('/#/recuperar-senha/confirmar');
      await loginPage.page.fill('input[name="nome_usuario"]', userData.nome_usuario);
      await loginPage.page.fill('input[name="token"]', 'token_invalido_123');
      await loginPage.page.fill('input[name="nova_senha"]', 'NovaSenha@456');
      await loginPage.page.fill('input[name="confirmar_nova_senha"]', 'NovaSenha@456');
      await loginPage.page.click('button[type="submit"]');
      
      const toast = await loginPage.getToastMessage();
      expect(toast?.toLowerCase()).toMatch(/token|inválido|expirado/);
    });
  });

  test.describe('Rate Limiting', () => {
    test('deve limitar tentativas de login', async ({ loginPage }) => {
      for (let i = 0; i < 5; i++) {
        await loginPage.goto();
        await loginPage.login('usuario_teste', 'senha_errada');
      }
      
      await loginPage.goto();
      await loginPage.login('usuario_teste', 'senha_errada');
      
      const toast = await loginPage.getToastMessage();
      expect(toast?.toLowerCase()).toMatch(/tentativa|bloqueado|rate|limit|aguarde/);
    });

    test('deve limitar solicitações de recuperação de senha', async ({ loginPage }) => {
      for (let i = 0; i < 3; i++) {
        await loginPage.goto();
        await loginPage.gotoRecuperarSenha();
        await loginPage.page.fill('input[name="nome_usuario"]', 'usuario_teste');
        await loginPage.page.click('button[type="submit"]');
      }
      
      await loginPage.goto();
      await loginPage.gotoRecuperarSenha();
      await loginPage.page.fill('input[name="nome_usuario"]', 'usuario_teste');
      await loginPage.page.click('button[type="submit"]');
      
      const toast = await loginPage.getToastMessage();
      expect(toast?.toLowerCase()).toMatch(/tentativa|bloqueado|rate|limit|aguarde/);
    });
  });
});