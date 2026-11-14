import { test, expect } from '../../fixtures/test-fixtures';
import { createTestUser } from '../../utils/test-data';

test.describe('CRUD - Perfil do Usuário (UC16-RF06, UC18-RF05)', () => {
  test.describe('READ - Visualizar perfil', () => {
    test('deve exibir dados do perfil corretamente', async ({ authenticatedPage, perfilPage, testUser }) => {
      await perfilPage.goto();
      
      await perfilPage.expectPerfilVisible(testUser.nome_usuario, testUser.email, testUser.nome);
      
      await expect(perfilPage.nomeInput).toHaveValue(testUser.nome);
      await expect(perfilPage.emailInput).toHaveValue(testUser.email);
      await expect(perfilPage.usuarioDisplay).toContainText(testUser.nome_usuario);
    });

    test('deve mostrar data de criação do usuário', async ({ authenticatedPage, perfilPage }) => {
      await perfilPage.goto();
      
      await expect(perfilPage.criadoEmDisplay).toBeVisible();
      const dataTexto = await perfilPage.criadoEmDisplay.textContent();
      expect(dataTexto).toMatch(/\d{4}-\d{2}-\d{2}|\d{2}\/\d{2}\/\d{4}/);
    });

    test('não deve mostrar senha no perfil', async ({ authenticatedPage, perfilPage }) => {
      await perfilPage.goto();
      
      await expect(perfilPage.page.locator('input[type="password"]')).not.toBeVisible();
      const pageText = await perfilPage.page.locator('body').textContent();
      expect(pageText?.toLowerCase()).not.toContain('senha@123');
    });
  });

  test.describe('UPDATE - Atualizar perfil', () => {
    test('deve atualizar nome completo', async ({ authenticatedPage, perfilPage }) => {
      const novoNome = `Nome Completo Atualizado ${Date.now()}`;
      
      await perfilPage.goto();
      await perfilPage.atualizarPerfil({ nome: novoNome });
      await perfilPage.waitForToast('Perfil atualizado');
      
      await perfilPage.goto();
      await expect(perfilPage.nomeInput).toHaveValue(novoNome);
    });

    test('deve atualizar email', async ({ authenticatedPage, perfilPage }) => {
      const novoEmail = `novo_email_${Date.now()}@test.com`;
      
      await perfilPage.goto();
      await perfilPage.atualizarPerfil({ email: novoEmail });
      await perfilPage.waitForToast('Perfil atualizado');
      
      await perfilPage.goto();
      await expect(perfilPage.emailInput).toHaveValue(novoEmail);
    });

    test('não deve permitir email inválido', async ({ authenticatedPage, perfilPage }) => {
      const emailsInvalidos = ['invalido', 'invalido@', '@test.com', 'test@'];
      
      for (const email of emailsInvalidos) {
        await perfilPage.goto();
        await perfilPage.atualizarPerfil({ email });
        
        const toast = await perfilPage.getToastMessage();
        expect(toast?.toLowerCase()).toMatch(/email|inválido|formato/);
      }
    });

    test('não deve permitir email já cadastrado', async ({ authenticatedPage, perfilPage, cadastroPage, loginPage }) => {
      const user2 = createTestUser();
      
      await cadastroPage.goto();
      await cadastroPage.cadastrar(user2);
      
      await perfilPage.goto();
      await perfilPage.atualizarPerfil({ email: user2.email });
      
      const toast = await perfilPage.getToastMessage();
      expect(toast?.toLowerCase()).toMatch(/email|já existe|duplicado|único/);
    });

    test('deve alterar senha com senha atual correta', async ({ authenticatedPage, perfilPage, testUser, loginPage }) => {
      const novaSenha = 'NovaSenha@456';
      
      await perfilPage.goto();
      await perfilPage.atualizarPerfil({
        senha_atual: testUser.senha,
        nova_senha: novaSenha,
        confirmar_nova_senha: novaSenha,
      });
      await perfilPage.waitForToast('Perfil atualizado');
      
      await perfilPage.logout();
      await loginPage.goto();
      await loginPage.login(testUser.nome_usuario, novaSenha);
      
      await expect(loginPage.page.locator('main')).toBeVisible();
    });

    test('não deve alterar senha com senha atual incorreta', async ({ authenticatedPage, perfilPage, testUser }) => {
      await perfilPage.goto();
      await perfilPage.atualizarPerfil({
        senha_atual: 'SenhaErrada@123',
        nova_senha: 'NovaSenha@456',
        confirmar_nova_senha: 'NovaSenha@456',
      });
      
      const toast = await perfilPage.getToastMessage();
      expect(toast?.toLowerCase()).toMatch(/senha|incorreta|atual/);
    });

    test('deve exigir confirmação de nova senha', async ({ authenticatedPage, perfilPage, testUser }) => {
      await perfilPage.goto();
      await perfilPage.atualizarPerfil({
        senha_atual: testUser.senha,
        nova_senha: 'NovaSenha@456',
        confirmar_nova_senha: 'OutraSenha@456',
      });
      
      const toast = await perfilPage.getToastMessage();
      expect(toast?.toLowerCase()).toMatch(/senha|coincid|confirmar/);
    });

    test('deve validar força da nova senha', async ({ authenticatedPage, perfilPage, testUser }) => {
      const senhasFracas = ['123', 'senha', 'Senha', 'SENHA@123', 'senha@123'];
      
      for (const novaSenha of senhasFracas) {
        await perfilPage.goto();
        await perfilPage.atualizarPerfil({
          senha_atual: testUser.senha,
          nova_senha: novaSenha,
          confirmar_nova_senha: novaSenha,
        });
        
        const toast = await perfilPage.getToastMessage();
        expect(toast?.toLowerCase()).toMatch(/senha|forte|caractere|mínimo/);
      }
    });

    test('não deve exigir senha atual se não estiver alterando senha', async ({ authenticatedPage, perfilPage }) => {
      const novoNome = `Nome Sem Senha ${Date.now()}`;
      
      await perfilPage.goto();
      await perfilPage.atualizarPerfil({ nome: novoNome });
      await perfilPage.waitForToast('Perfil atualizado');
      
      await perfilPage.goto();
      await expect(perfilPage.nomeInput).toHaveValue(novoNome);
    });

    test('deve atualizar apenas email sem alterar senha', async ({ authenticatedPage, perfilPage }) => {
      const novoEmail = `email_only_${Date.now()}@test.com`;
      
      await perfilPage.goto();
      await perfilPage.atualizarPerfil({ email: novoEmail });
      await perfilPage.waitForToast('Perfil atualizado');
      
      await perfilPage.goto();
      await expect(perfilPage.emailInput).toHaveValue(novoEmail);
    });
  });

  test.describe('Validações de formulário', () => {
    test('deve mostrar erro para campos obrigatórios vazios', async ({ authenticatedPage, perfilPage }) => {
      await perfilPage.goto();
      await perfilPage.nomeInput.clear();
      await perfilPage.submitButton.click();
      
      await expect(perfilPage.nomeInput).toHaveAttribute('required');
    });

    test('deve manter valores atuais se cancelar edição', async ({ authenticatedPage, perfilPage, testUser }) => {
      await perfilPage.goto();
      await perfilPage.nomeInput.fill('Nome Temporário');
      await perfilPage.page.keyboard.press('Escape');
      
      await perfilPage.goto();
      await expect(perfilPage.nomeInput).toHaveValue(testUser.nome);
    });
  });

  test.describe('Logout', () => {
    test('deve fazer logout e redirecionar para login', async ({ authenticatedPage, perfilPage, loginPage }) => {
      await perfilPage.goto();
      await perfilPage.logout();
      
      await loginPage.expectLoginFormVisible();
    });

    test('deve invalidar sessão após logout', async ({ authenticatedPage, perfilPage, loginPage, testUser }) => {
      await perfilPage.goto();
      await perfilPage.logout();
      
      await loginPage.goto();
      await loginPage.login(testUser.nome_usuario, testUser.senha);
      
      await expect(loginPage.page.locator('main')).toBeVisible();
    });
  });
});