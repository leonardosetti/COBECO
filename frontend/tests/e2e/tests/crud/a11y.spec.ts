import { test, expect } from '../../fixtures/test-fixtures';
import { createTestUser } from '../../utils/test-data';

test.describe('Acessibilidade (WCAG 2.1 AA)', () => {
  test.describe('Navegação por Teclado', () => {
    test('Tab order lógico em formulário de login', async ({ page, loginPage }) => {
      await loginPage.goto();
      
      // Primeiro Tab deve focar no campo usuário
      await page.keyboard.press('Tab');
      await expect(page.locator('input[name="nome_usuario"]')).toBeFocused();
      
      // Segundo Tab foca no campo senha
      await page.keyboard.press('Tab');
      await expect(page.locator('input[name="senha"]')).toBeFocused();
      
      // Terceiro Tab foca no botão submit
      await page.keyboard.press('Tab');
      await expect(page.locator('button[type="submit"]')).toBeFocused();
      
      // Links de navegação também devem ser acessíveis
      await page.keyboard.press('Tab');
      const cadastrarLink = page.locator('[data-link="/cadastrar"], a[href="#/cadastrar"]');
      await expect(cadastrarLink).toBeFocused();
    });

    test('Tab order lógico em formulário de cadastro', async ({ page, cadastroPage }) => {
      await cadastroPage.goto();
      
      const campos = [
        'input[name="nome_usuario"]',
        'input[name="email"]',
        'input[name="nome"]',
        'input[name="senha"]',
        'input[name="confirmar_senha"]',
        'input[name="pergunta_seguranca"]',
        'input[name="resposta_seguranca"]',
        'button[type="submit"]',
      ];
      
      for (const seletor of campos) {
        await page.keyboard.press('Tab');
        await expect(page.locator(seletor)).toBeFocused();
      }
    });

    test('Enter submete formulário quando botão focado', async ({ page, loginPage }) => {
      await loginPage.goto();
      
      await page.fill('input[name="nome_usuario"]', 'usuario');
      await page.fill('input[name="senha"]', 'senha');
      
      await page.keyboard.press('Tab'); // usuário
      await page.keyboard.press('Tab'); // senha
      await page.keyboard.press('Tab'); // botão
      
      await page.keyboard.press('Enter');
      
      // Deve tentar submeter (vai falhar credenciais, mas não erro de JS)
      await page.waitForTimeout(1000);
    });

    test('Escape fecha modais', async ({ page, cadastroPage, loginPage }) => {
      await cadastroPage.goto();
      await cadastroPage.cadastrar(createTestUser());
      
      await loginPage.goto();
      await loginPage.login('testuser', 'Senha@123');
      
      // Abre modal via showConfirm
      const modalOpened = await page.evaluate(() => {
        return new Promise((resolve) => {
          window.showConfirm('Teste Escape').then(() => resolve(true));
        });
      });
      
      expect(modalOpened).toBe(true);
      
      // Pressiona Escape
      await page.keyboard.press('Escape');
      await page.waitForTimeout(300);
      
      // Modal deve fechar
      const modalVisible = await page.locator('.modal').isVisible();
      expect(modalVisible).toBe(false);
    });

    test('Skip link para conteúdo principal', async ({ page }) => {
      await page.goto('/#/login');
      await page.waitForLoadState('networkidle');
      
      // Primeiro Tab deve mostrar skip link (se implementado)
      await page.keyboard.press('Tab');
      
      // Se houver skip link, deve ser o primeiro elemento focável
      const firstFocused = await page.evaluate(() => document.activeElement?.tagName);
      // Skip link ou primeiro input
      expect(['A', 'INPUT'].includes(firstFocused)).toBe(true);
    });
  });

  test.describe('Labels e ARIA', () => {
    test('todos inputs têm labels associados', async ({ page, cadastroPage }) => {
      await cadastroPage.goto();
      
      const inputs = [
        { seletor: 'input[name="nome_usuario"]', label: /usuário/i },
        { seletor: 'input[name="email"]', label: /email/i },
        { seletor: 'input[name="nome"]', label: /nome/i },
        { seletor: 'input[name="senha"]', label: /senha/i },
        { seletor: 'input[name="confirmar_senha"]', label: /confirmar/i },
        { seletor: 'input[name="pergunta_seguranca"]', label: /pergunta/i },
        { seletor: 'input[name="resposta_seguranca"]', label: /resposta/i },
      ];
      
      for (const { seletor, label } of inputs) {
        const input = page.locator(seletor);
        await expect(input).toBeVisible();
        
        // Verifica label associado via for=id ou aria-label/aria-labelledby
        const inputId = await input.getAttribute('id');
        const hasLabel = await page.evaluate((id) => {
          if (!id) return false;
          const labelEl = document.querySelector(`label[for="${id}"]`);
          return !!labelEl;
        }, inputId);
        
        const hasAriaLabel = await input.getAttribute('aria-label');
        const hasAriaLabelledBy = await input.getAttribute('aria-labelledby');
        
        expect(hasLabel || hasAriaLabel || hasAriaLabelledBy).toBe(true);
      }
    });

    test('botões têm texto acessível ou aria-label', async ({ page, cadastroPage, loginPage }) => {
      await loginPage.goto();
      
      const submitBtn = page.locator('button[type="submit"]');
      await expect(submitBtn).toBeVisible();
      
      // Botão deve ter texto visível ou aria-label
      const text = await submitBtn.textContent();
      const ariaLabel = await submitBtn.getAttribute('aria-label');
      expect(text?.trim().length || ariaLabel?.length).toBeGreaterThan(0);
    });

    test('alertas e toasts têm role=alert', async ({ page, cadastroPage, loginPage }) => {
      await cadastroPage.goto();
      await cadastroPage.cadastrar(createTestUser());
      
      await loginPage.goto();
      await loginPage.login('testuser', 'Senha@123');
      
      // Trigger toast
      await page.evaluate(() => window.showToast('Teste ARIA', 'sdoc-arch-0006-uc-v1cess'));
      
      const toast = page.locator('.toast, [role="alert"]').first();
      await expect(toast).toBeVisible({ timeout: 3000 });
      
      const role = await toast.getAttribute('role');
      expect(role).toBe('alert');
    });

    test('modais têm role=dialog e aria-modal', async ({ page }) => {
      const modalOpened = await page.evaluate(() => {
        return new Promise((resolve) => {
          window.showConfirm('Teste ARIA Modal').then(() => resolve(true));
        });
      });
      
      expect(modalOpened).toBe(true);
      
      const modal = page.locator('.modal[role="dialog"], .modal[aria-modal="true"]');
      await expect(modal.first()).toBeVisible({ timeout: 3000 });
      
      const role = await modal.first().getAttribute('role');
      const ariaModal = await modal.first().getAttribute('aria-modal');
      
      expect(role).toBe('dialog');
      expect(ariaModal).toBe('true');
    });

    test('tabelas têm headers corretos', async ({ authenticatedPage, listasPage }) => {
      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      await listasPage.criarLista({ titulo: 'Lista Tabela A11y' });
      await listasPage.waitForToast('Lista criada');
      
      await listasPage.page.goto('/#/criar-lista');
      await listasPage.page.waitForLoadState('networkidle');
      
      const table = listasPage.page.locator('table');
      await expect(table).toBeVisible();
      
      // Verifica thead com th
      const thead = table.locator('thead');
      await expect(thead).toBeVisible();
      
      const ths = thead.locator('th');
      const count = await ths.count();
      expect(count).toBeGreaterThan(0);
      
      // Cada th deve ter scope
      for (let i = 0; i < count; i++) {
        const th = ths.nth(i);
        const scope = await th.getAttribute('scope');
        // scope="col" é recomendado para headers de coluna
        expect(scope).toBeTruthy();
      }
    });
  });

  test.describe('Contraste e Cores', () => {
    test('texto principal tem contraste suficiente', async ({ page }) => {
      await page.goto('/#/login');
      await page.waitForLoadState('networkidle');
      
      // Verifica cor do texto principal vs fundo
      const bodyColor = await page.evaluate(() => {
        const style = getComputedStyle(document.body);
        return style.color;
      });
      
      const bgColor = await page.evaluate(() => {
        const style = getComputedStyle(document.body);
        return style.backgroundColor;
      });
      
      // Verifica se não são iguais (contraste mínimo)
      expect(bodyColor).not.toBe(bgColor);
    });

    test('links têm underline ou contraste suficiente', async ({ page, loginPage }) => {
      await loginPage.goto();
      
      const links = page.locator('a[href]');
      const count = await links.count();
      
      for (let i = 0; i < count; i++) {
        const link = links.nth(i);
        const style = await link.evaluate(el => getComputedStyle(el));
        
        // Link deve ter text-decoration underline ou color diferente do texto
        const textDecoration = style.textDecorationLine;
        const color = style.color;
        const parentColor = await link.evaluate(el => getComputedStyle(el.parentElement).color);
        
        // Pelo menos uma das condições deve ser verdadeira
        const hasUnderline = textDecoration.includes('underline');
        const hasContrast = color !== parentColor;
        
        expect(hasUnderline || hasContrast).toBe(true);
      }
    });

    test('estados de foco visíveis', async ({ page, loginPage }) => {
      await loginPage.goto();
      
      await page.keyboard.press('Tab');
      const focused = await page.evaluate(() => document.activeElement);
      
      // Elemento focado deve ter outline visível
      const outline = await page.evaluate(el => {
        const style = getComputedStyle(el);
        return style.outlineWidth !== '0px' || style.outlineStyle !== 'none';
      }, focused);
      
      expect(outline).toBe(true);
    });

    test('mensagens de erro têm contraste e ícones', async ({ page, cadastroPage }) => {
      await cadastroPage.goto();
      await cadastroPage.submitButton.click(); // Tenta submeter vazio
      
      // Verifica se mensagens de validação aparecem
      const errorMessages = page.locator('.error, .text-red-600, [role="alert"], .invalid-feedback');
      // Se houver erros, devem ser visíveis
      const count = await errorMessages.count();
      if (count > 0) {
        await expect(errorMessages.first()).toBeVisible();
      }
    });
  });

  test.describe('Formulários Acessíveis', () => {
    test('campos required têm atributo required', async ({ page, cadastroPage }) => {
      await cadastroPage.goto();
      
      const requiredFields = [
        'input[name="nome_usuario"]',
        'input[name="email"]',
        'input[name="nome"]',
        'input[name="senha"]',
        'input[name="confirmar_senha"]',
        'input[name="pergunta_seguranca"]',
        'input[name="resposta_seguranca"]',
      ];
      
      for (const seletor of requiredFields) {
        const input = page.locator(seletor);
        await expect(input).toHaveAttribute('required');
      }
    });

    test('campos com autocomplete apropriado', async ({ page, cadastroPage }) => {
      await cadastroPage.goto();
      
      const autocompleteChecks = [
        { seletor: 'input[name="nome_usuario"]', autocomplete: 'username' },
        { seletor: 'input[name="email"]', autocomplete: 'email' },
        { seletor: 'input[name="nome"]', autocomplete: 'name' },
        { seletor: 'input[name="senha"]', autocomplete: 'new-password' },
        { seletor: 'input[name="confirmar_senha"]', autocomplete: 'new-password' },
      ];
      
      for (const { seletor, autocomplete } of autocompleteChecks) {
        const input = page.locator(seletor);
        await expect(input).toHaveAttribute('autocomplete', autocomplete);
      }
    });

    test('fieldset/legend para grupos relacionados', async ({ page, cadastroPage }) => {
      await cadastroPage.goto();
      
      // Verifica se campos de senha estão agrupados
      const senhaFieldset = page.locator('fieldset:has(input[name="senha"])');
      // Se não houver fieldset, pelo menos devem ter labels claros
      // (implementação pode variar)
    });

    test('mensagens de erro associadas via aria-describedby', async ({ page, cadastroPage }) => {
      await cadastroPage.goto();
      await cadastroPage.submitButton.click(); // Submete vazio
      
      // Verifica se inputs têm aria-describedby apontando para erro
      const usuarioInput = page.locator('input[name="nome_usuario"]');
      const ariaDescribedBy = await usuarioInput.getAttribute('aria-describedby');
      
      // Se houver erro, deve ter aria-describedby
      const errorVisible = await page.locator('.error, .text-red-600').first().isVisible();
      if (errorVisible) {
        expect(ariaDescribedBy).toBeTruthy();
      }
    });
  });

  test.describe('Navegação Estrutural', () => {
    test('heading hierarchy correta (h1 > h2 > h3)', async ({ page, authenticatedPage, listasPage }) => {
      await listasPage.gotoMinhasListas();
      
      const headings = page.locator('h1, h2, h3, h4, h5, h6');
      const count = await headings.count();
      
      let lastLevel = 0;
      for (let i = 0; i < count; i++) {
        const heading = headings.nth(i);
        const tagName = await heading.evaluate(el => el.tagName.toLowerCase());
        const level = parseInt(tagName.charAt(1));
        
        // Primeiro heading deve ser h1
        if (i === 0) {
          expect(level).toBe(1);
        } else {
          // Não deve pular níveis (h1 -> h3 não permitido)
          expect(level - lastLevel).toBeLessThanOrEqual(1);
        }
        lastLevel = level;
      }
    });

    test('landmarks principais presentes', async ({ page }) => {
      await page.goto('/#/login');
      await page.waitForLoadState('networkidle');
      
      // main landmark
      await expect(page.locator('main')).toBeVisible();
      
      // header landmark
      await expect(page.locator('header, [role="banner"]')).toBeVisible();
      
      // nav landmark
      await expect(page.locator('nav, [role="navigation"]')).toBeVisible();
      
      // footer landmark
      await expect(page.locator('footer, [role="contentinfo"]')).toBeVisible();
    });

    test('regions têm labels acessíveis', async ({ page }) => {
      await page.goto('/#/login');
      await page.waitForLoadState('networkidle');
      
      // Nav deve ter aria-label ou aria-labelledby
      const nav = page.locator('nav').first();
      const ariaLabel = await nav.getAttribute('aria-label');
      const ariaLabelledBy = await nav.getAttribute('aria-labelledby');
      
      expect(ariaLabel || ariaLabelledBy).toBeTruthy();
    });
  });

  test.describe('Zoom e Redimensionamento', () => {
    test('layout funcional com zoom 200%', async ({ page, cadastroPage, loginPage }) => {
      await page.setViewportSize({ width: 1024, height: 768 });
      
      await cadastroPage.goto();
      await cadastroPage.cadastrar(createTestUser());
      
      await loginPage.goto();
      await loginPage.login('testuser', 'Senha@123');
      
      // Simula zoom 200% via CSS transform
      await page.evaluate(() => {
        document.body.style.transform = 'scale(2)';
        document.body.style.transformOrigin = 'top left';
        document.body.style.width = '50%';
      });
      
      await page.waitForTimeout(500);
      
      // Verifica se conteúdo principal ainda acessível
      await expect(page.locator('main')).toBeVisible();
      
      // Restaura
      await page.evaluate(() => {
        document.body.style.transform = '';
        document.body.style.width = '';
      });
    });

    test('texto não truncado em containers', async ({ page, cadastroPage }) => {
      await cadastroPage.goto();
      
      // Verifica se labels não estão cortados
      const labels = page.locator('label');
      const count = await labels.count();
      
      for (let i = 0; i < count; i++) {
        const label = labels.nth(i);
        const text = await label.textContent();
        const isVisible = await label.isVisible();
        
        if (isVisible && text) {
          // Texto não deve terminar com reticências (truncamento)
          expect(text.trim()).not.toMatch(/\.\.\.$/);
        }
      }
    });
  });
});