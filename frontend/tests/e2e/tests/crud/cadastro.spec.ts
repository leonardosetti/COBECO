import { test, expect } from '../../fixtures/test-fixtures';
import { CadastroData } from '../../pages/CadastroPage';
import { createTestUser } from '../../utils/test-data';

test.describe('CRUD - Cadastro de Usuário (UC01/RF01)', () => {
  test.describe('CREATE - Cadastrar novo usuário', () => {
    test('deve cadastrar usuário com dados válidos', async ({ cadastroPage, loginPage }) => {
      const userData = createTestUser();
      
      await cadastroPage.goto();
      await cadastroPage.expectCadastroFormVisible();
      const toast = await cadastroPage.cadastrar(userData);
      
      // Verifica se chegou na página de login
      await loginPage.expectLoginFormVisible();
      
      // Toast pode ter aparecido antes do redirect
      if (toast) {
        expect(toast.toLowerCase()).toMatch(/conta criada|sdoc-arch-0006-uc-v1esso|redirecion/);
      }
    });

    test('deve cadastrar usuário com email único', async ({ cadastroPage, loginPage }) => {
      const userData = createTestUser({ email: `unique${Date.now()}@test.com` });
      
      await cadastroPage.goto();
      await cadastroPage.cadastrar(userData);
      
      await loginPage.expectLoginFormVisible();
    });

    test('deve exigir todos os campos obrigatórios', async ({ cadastroPage }) => {
      await cadastroPage.goto();
      // HTML5 validation prevents submit, just check required attributes
      await expect(cadastroPage.nomeUsuarioInput).toHaveAttribute('required');
      await expect(cadastroPage.emailInput).toHaveAttribute('required');
      await expect(cadastroPage.nomeInput).toHaveAttribute('required');
      await expect(cadastroPage.senhaInput).toHaveAttribute('required');
      await expect(cadastroPage.confirmarSenhaInput).toHaveAttribute('required');
      await expect(cadastroPage.perguntaSegurancaInput).toHaveAttribute('required');
      await expect(cadastroPage.respostaSegurancaInput).toHaveAttribute('required');
    });

    test('deve validar formato de email', async ({ cadastroPage }) => {
      const invalidEmails = ['invalido', 'invalido@', '@test.com', 'test@'];
      
      for (const email of invalidEmails) {
        await cadastroPage.goto();
        await cadastroPage.cadastrarMinimo({
          ...createTestUser(),
          email,
        });
        
        await expect(cadastroPage.emailInput).toHaveAttribute('type', 'email');
      }
    });

    test('deve validar força da senha (minlength 8)', async ({ cadastroPage }) => {
      const shortPasswords = ['123', 'senha', 'Senha'];
      
      for (const senha of shortPasswords) {
        await cadastroPage.goto();
        await cadastroPage.cadastrarMinimo({
          ...createTestUser(),
          senha,
          confirmar_senha: senha,
        });
        
        // HTML5 validation should prevent submit
        await expect(cadastroPage.senhaInput).toHaveAttribute('minlength', '8');
      }
    });

    test('deve confirmar senha igual', async ({ cadastroPage }) => {
      const userData = createTestUser({ confirmar_senha: 'OutraSenha@123' });
      
      await cadastroPage.goto();
      await cadastroPage.cadastrar(userData);
      
      // Verifica se permaneceu na página de cadastro (erro de validação)
      await expect(cadastroPage.page).toHaveURL(/.*#\/cadastrar/);
    });

    test('deve exigir pergunta de segurança', async ({ cadastroPage }) => {
      await cadastroPage.goto();
      await cadastroPage.cadastrarMinimo({
        ...createTestUser(),
        pergunta_seguranca: '',
        resposta_seguranca: 'Resposta',
      });
      
      await expect(cadastroPage.perguntaSegurancaInput).toHaveAttribute('required');
    });

    test('deve exigir resposta de segurança', async ({ cadastroPage }) => {
      await cadastroPage.goto();
      await cadastroPage.cadastrarMinimo({
        ...createTestUser(),
        pergunta_seguranca: 'nome_mae',
        resposta_seguranca: '',
      });
      
      await expect(cadastroPage.respostaSegurancaInput).toHaveAttribute('required');
    });
  });

  test.describe('READ - Verificar usuário cadastrado', () => {
    test('deve permitir login após cadastro', async ({ cadastroPage, loginPage }) => {
      const userData = createTestUser();
      
      await cadastroPage.goto();
      await cadastroPage.cadastrar(userData);
      
      await loginPage.goto();
      await loginPage.login(userData.nome_usuario, userData.senha);
      
      await expect(loginPage.page.locator('main')).toBeVisible();
    });

    test('deve mostrar dados do perfil após login', async ({ authenticatedPage, perfilPage, testUser }) => {
      await perfilPage.goto();
      await perfilPage.expectPerfilVisible(testUser.nome_usuario, testUser.email, testUser.nome);
    });
  });

  test.describe('UPDATE - Atualizar cadastro (via perfil)', () => {
    test('deve atualizar nome do usuário', async ({ authenticatedPage, perfilPage, testUser }) => {
      const novoNome = `Nome Atualizado ${Date.now()}`;
      
      await perfilPage.goto();
      await perfilPage.atualizarPerfil({ nome: novoNome });
      await perfilPage.waitForToast('Perfil atualizado');
      
      await perfilPage.goto();
      await perfilPage.expectFormValues({ nome: novoNome });
    });

    test('deve atualizar email do usuário', async ({ authenticatedPage, perfilPage }) => {
      const novoEmail = `novo_${Date.now()}@test.com`;
      
      await perfilPage.goto();
      await perfilPage.atualizarPerfil({ email: novoEmail });
      await perfilPage.waitForToast('Perfil atualizado');
      
      await perfilPage.goto();
      await perfilPage.expectFormValues({ email: novoEmail });
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
  });

  test.describe('DELETE - Exclusão de conta (se implementado)', () => {
    test.skip('deve permitir exclusão da conta', async ({ authenticatedPage, perfilPage, testUser, loginPage }) => {
      // Este teste será implementado quando houver endpoint de exclusão
    });
  });

  test.describe('Validações de Unicidade', () => {
    test('não deve permitir nome de usuário duplicado', async ({ cadastroPage, testUser }) => {
      await cadastroPage.goto();
      await cadastroPage.cadastrar(testUser);
      
      await cadastroPage.goto();
      await cadastroPage.cadastrar(testUser);
      
      const toast = await cadastroPage.getToastMessage();
      expect(toast?.toLowerCase()).toMatch(/usuário|já existe|duplicado|único/);
    });

    test('não deve permitir email duplicado', async ({ cadastroPage, testUser }) => {
      await cadastroPage.goto();
      await cadastroPage.cadastrar(testUser);
      
      const outroUsuario = createTestUser({ 
        nome_usuario: `outro${Date.now()}`,
        email: testUser.email,
      });
      
      await cadastroPage.goto();
      await cadastroPage.cadastrar(outroUsuario);
      
      const toast = await cadastroPage.getToastMessage();
      expect(toast?.toLowerCase()).toMatch(/email|já existe|duplicado|único/);
    });
  });

  test.describe('Navegação', () => {
    test('deve navegar para login a partir do cadastro', async ({ cadastroPage, loginPage }) => {
      await cadastroPage.goto();
      await cadastroPage.gotoLogin();
      await loginPage.expectLoginFormVisible();
    });

    test('deve navegar para recuperar senha a partir do login', async ({ loginPage }) => {
      await loginPage.goto();
      await loginPage.gotoRecuperarSenha();
      await expect(loginPage.page.locator('input[name="nome_usuario"]')).toBeVisible();
    });
  });
});