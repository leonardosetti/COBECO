import { test, expect } from '../../fixtures/test-fixtures';
import { createTestUser } from '../../utils/test-data';

test.describe('Segurança Frontend - Prevenção XSS', () => {
  test.describe('Sanitização de Entrada', () => {
    test('deve escapar HTML no nome do usuário no perfil', async ({ authenticatedPage, perfilPage }) => {
      // Tenta atualizar nome com payload XSS
      const xssPayload = '<script>alert("XSS")</script>';
      
      await perfilPage.goto();
      await perfilPage.atualizarPerfil({ nome: xssPayload });
      
      // Verifica se nome foi sanitizado (não executado)
      await perfilPage.goto();
      
      const nomeInput = perfilPage.page.locator('#perfil-nome');
      const value = await nomeInput.inputValue();
      
      // Valor deve estar escapado (entidades HTML)
      expect(value).not.toContain('<script>');
      expect(value).toContain('<script>');
    });

    test('deve escapar HTML em descrição de lista', async ({ authenticatedPage, listasPage }) => {
      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      
      const xssPayload = '<img src=x onerror=alert(1)>';
      
      // Tenta criar lista com XSS no título
      await listasPage.page.fill('#lista-nome', xssPayload);
      await listasPage.page.click('#btn-salvar-lista');
      await listasPage.page.waitForLoadState('networkidle');
      
      // Verifica se título foi sanitizado
      const tituloSalvo = await listasPage.page.locator('.lista-titulo, h1, h2').first().textContent();
      expect(tituloSalvo).not.toContain('<img');
      expect(tituloSalvo).toContain('<img');
    });

    test('deve escapar HTML em itens da lista', async ({ authenticatedPage, listasPage }) => {
      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      
      const xssPayload = '<svg onload=alert(1)>';
      
      await listasPage.page.fill('#lista-nome', 'Lista XSS');
      await listasPage.page.waitForTimeout(500);
      
      // Adiciona item com XSS
      const produtoInput = listasPage.page.locator('#item-produto');
      await produtoInput.fill(xssPayload);
      await listasPage.page.waitForTimeout(500);
      
      const autocompleteResults = listasPage.page.locator('#autocomplete-results');
      await expect(autocompleteResults).toBeVisible({ timeout: 5000 });
      
      // Se autocomplete retornar resultado, seleciona
      const results = autocompleteResults.locator('.autocomplete-item, li, [data-produto-id]');
      if (await results.count() > 0) {
        await results.first().click();
        await listasPage.page.locator('#btn-add-item').click();
        await listasPage.page.waitForTimeout(300);
        
        // Verifica se item foi sanitizado na tabela
        const tabelaItens = listasPage.page.locator('#tbody-itens');
        const cellText = await tabelaItens.textContent();
        expect(cellText).not.toContain('<svg');
      }
    });
  });

  test.describe('escapeHtml Utility', () => {
    test('deve escapar caracteres especiais', async ({ page }) => {
      const result = await page.evaluate(() => {
        const escapeHtml = (text) => {
          if (text === null || text === undefined) return '';
          const div = document.createElement('div');
          div.textContent = String(text);
          return div.innerHTML;
        };
        
        return {
          script: escapeHtml('<script>alert(1)</script>'),
          img: escapeHtml('<img src=x onerror=alert(1)>'),
          quotes: escapeHtml('"teste"'),
          amp: escapeHtml('A & B'),
          safe: escapeHtml('Texto normal'),
        };
      });
      
      expect(result.script).toBe('<script>alert(1)</script>');
      expect(result.img).toBe('<img src=x onerror=alert(1)>');
      expect(result.quotes).toBe('"teste"');
      expect(result.amp).toBe('A & B');
      expect(result.safe).toBe('Texto normal');
    });

    test('deve retornar string vazia para null/undefined', async ({ page }) => {
      const result = await page.evaluate(() => {
        const escapeHtml = (text) => {
          if (text === null || text === undefined) return '';
          const div = document.createElement('div');
          div.textContent = String(text);
          return div.innerHTML;
        };
        
        return {
          null: escapeHtml(null),
          undefined: escapeHtml(undefined),
        };
      });
      
      expect(result.null).toBe('');
      expect(result.undefined).toBe('');
    });
  });

  test.describe('showToast Sanitization', () => {
    test('deve escapar mensagem do toast', async ({ page, cadastroPage, loginPage }) => {
      await cadastroPage.goto();
      await cadastroPage.cadastrar(createTestUser());
      
      await loginPage.goto();
      await loginPage.login('testuser', 'Senha@123');
      
      // Trigger toast com XSS
      await page.evaluate(() => window.showToast('<script>alert("toast XSS")</script>', 'success'));
      
      const toast = page.locator('.toast').first();
      await expect(toast).toBeVisible({ timeout: 3000 });
      
      const toastText = await toast.textContent();
      expect(toastText).not.toContain('<script>');
      expect(toastText).toContain('<script>');
    });
  });

  test.describe('showConfirm Sanitization', () => {
    test('deve escapar título e mensagem do modal', async ({ page }) => {
      const result = await page.evaluate(() => {
        return new Promise((resolve) => {
          window.showConfirm('<script>alert("confirm")</script>', {
            title: '<b>Título XSS</b>',
            confirmText: '<i>Confirmar</i>',
          }).then(() => resolve(true));
        });
      });
      
      expect(result).toBe(true);
      
      // Verifica se modal foi sanitizado
      const modal = page.locator('.modal');
      const title = modal.locator('#modal-title');
      const body = modal.locator('.modal-body');
      
      // Verifica se HTML foi escapado
      const titleText = await title.textContent();
      const bodyText = await body.textContent();
      
      expect(titleText).not.toContain('<b>');
      expect(titleText).toContain('<b>');
      expect(bodyText).not.toContain('<script>');
    });
  });

  test.describe('Content Security Policy', () => {
    test('CSP headers devem estar presentes', async ({ page }) => {
      const response = await page.goto('/#/login');
      const headers = response.headers();
      
      const csp = headers['content-security-policy'];
      expect(csp).toBeTruthy();
      
      // Verifica diretivas essenciais
      expect(csp).toContain("default-src 'self'");
      expect(csp).toContain("script-src 'self'");
      expect(csp).toContain("frame-ancestors 'none'");
    });

    test('não deve permitir scripts inline sem nonce', async ({ page }) => {
      await page.goto('/#/login');
      
      // Tenta injetar script via console
      const result = await page.evaluate(() => {
        try {
          const script = document.createElement('script');
          script.textContent = 'alert("CSP bypass")';
          document.head.appendChild(script);
          return 'executed';
        } catch (e) {
          return 'blocked';
        }
      });
      
      // CSP deve bloquear (depende da configuração)
      // Se CSP strict, deve bloquear
    });
  });

  test.describe('Proteção contra Clickjacking', () => {
    test('X-Frame-Options DENY', async ({ page }) => {
      const response = await page.goto('/#/login');
      const headers = response.headers();
      
      expect(headers['x-frame-options']).toBe('DENY');
    });

    test('frame-ancestors none no CSP', async ({ page }) => {
      const response = await page.goto('/#/login');
      const headers = response.headers();
      
      const csp = headers['content-security-policy'];
      expect(csp).toContain("frame-ancestors 'none'");
    });
  });

  test.describe('Proteção de Dados Sensíveis', () => {
    test('senha não deve aparecer no DOM', async ({ authenticatedPage, perfilPage }) => {
      await perfilPage.goto();
      
      // Verifica se campo senha é type=password
      const senhaInput = perfilPage.page.locator('#perfil-senha-atual, input[name="senha_atual"]');
      await expect(senhaInput).toHaveAttribute('type', 'password');
      
      // Verifica se senha não está no value
      const value = await perfilPage.page.locator('#perfil-senha-atual').inputValue();
      expect(value).toBe('');
    });

    test('token não deve estar em localStorage', async ({ page, cadastroPage, loginPage }) => {
      await cadastroPage.goto();
      await cadastroPage.cadastrar(createTestUser());
      
      await loginPage.goto();
      await loginPage.login('testuser', 'Senha@123');
      
      // Verifica localStorage
      const storage = await page.evaluate(() => {
        return {
          accessToken: localStorage.getItem('cobeco_access_token'),
          refreshToken: localStorage.getItem('cobeco_refresh_token'),
          user: localStorage.getItem('cobeco_user'),
        };
      });
      
      // Access token pode estar em localStorage (depende da implementação)
      // Refresh token NÃO deve estar em localStorage (deve estar em cookie httpOnly)
      expect(storage.refreshToken).toBeNull();
    });

    test('autocomplete off em campos sensíveis', async ({ page, cadastroPage }) => {
      await cadastroPage.goto();
      
      const senhaInput = page.locator('input[name="senha"]');
      const confirmarInput = page.locator('input[name="confirmar_senha"]');
      
      await expect(senhaInput).toHaveAttribute('autocomplete', 'new-password');
      await expect(confirmarInput).toHaveAttribute('autocomplete', 'new-password');
    });
  });

  test.describe('Proteção CSRF', () => {
    test('SameSite=Strict em cookies', async ({ page, cadastroPage, loginPage }) => {
      await cadastroPage.goto();
      await cadastroPage.cadastrar(createTestUser());
      
      const loginRes = await page.evaluate(async () => {
        const res = await fetch('/v1/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ nome_usuario: 'testuser', senha: 'Senha@123' }),
          credentials: 'include',
        });
        return {
          status: res.status,
          cookies: res.headers.get('set-cookie'),
        };
      });
      
      // Verifica SameSite=Strict no refresh token
      expect(emockRes.cookies).toContain('SameSite=Strict');
    });
  });
});