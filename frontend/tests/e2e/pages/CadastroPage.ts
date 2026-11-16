import { Page, Locator, expect } from '@playwright/test';
import { BasePage } from './BasePage';

export interface CadastroData {
  nome_usuario: string;
  email: string;
  nome: string;
  senha: string;
  confirmar_senha: string;
  pergunta_seguranca: string;
  resposta_seguranca: string;
}

export class CadastroPage extends BasePage {
  readonly nomeUsuarioInput: Locator;
  readonly emailInput: Locator;
  readonly nomeInput: Locator;
  readonly senhaInput: Locator;
  readonly confirmarSenhaInput: Locator;
  readonly perguntaSegurancaInput: Locator;
  readonly respostaSegurancaInput: Locator;
  readonly submitButton: Locator;
  readonly loginLink: Locator;

  constructor(page: Page) {
    super(page);
    this.nomeUsuarioInput = page.locator('#cad-nome-usuario, input[name="nome_usuario"]');
    this.emailInput = page.locator('#cad-email, input[name="email"]');
    this.nomeInput = page.locator('#cad-nome, input[name="nome"]');
    this.senhaInput = page.locator('#cad-senha, input[name="senha"]');
    this.confirmarSenhaInput = page.locator('#cad-confirmar-senha, input[name="confirmar_senha"]');
    this.perguntaSegurancaInput = page.locator('#cad-pergunta, input[name="pergunta_seguranca"]');
    this.respostaSegurancaInput = page.locator('#cad-resposta, input[name="resposta_seguranca"]');
    this.submitButton = page.locator('button[type="submit"]');
    this.loginLink = page.locator('[data-link="/login"], a[href="#/login"]');
  }

  async goto(): Promise<void> {
    await super.goto('/#/cadastrar');
    await this.nomeUsuarioInput.waitFor({ state: 'visible', timeout: 10000 });
    // Wait for form submit handler to be attached (router bindEvents)
    await this.page.waitForFunction(
      () => {
        const form = document.querySelector('#form-cadastro');
        return form && form.onsubmit != null;
      },
      { timeout: 15000 }
    );
  }

  async cadastrar(data: CadastroData): Promise<string | null> {
    await this.nomeUsuarioInput.fill(data.nome_usuario);
    await this.emailInput.fill(data.email);
    await this.nomeInput.fill(data.nome);
    await this.senhaInput.fill(data.senha);
    await this.confirmarSenhaInput.fill(data.confirmar_senha);
    await this.perguntaSegurancaInput.fill(data.pergunta_seguranca);
    await this.respostaSegurancaInput.fill(data.resposta_seguranca);
    
    // Submit form via dispatchEvent to trigger onsubmit handler
    await this.page.evaluate(() => {
      const form = document.querySelector('#form-cadastro');
      if (form) {
        const event = new Event('submit', { cancelable: true, bubbles: true });
        form.dispatchEvent(event);
      }
    });
    
    // Wait for navigation to login (success case)
    await this.page.waitForURL('**/#/login', { timeout: 10000 }).catch(() => {});
    
    // Try to get toast message before navigation
    const toast = await this.getToastMessage();
    await this.page.waitForLoadState('networkidle');
    return toast;
  }

  async cadastrarMinimo(data: Partial<CadastroData>): Promise<void> {
    if (data.nome_usuario) await this.nomeUsuarioInput.fill(data.nome_usuario);
    if (data.email) await this.emailInput.fill(data.email);
    if (data.nome) await this.nomeInput.fill(data.nome);
    if (data.senha) await this.senhaInput.fill(data.senha);
    if (data.confirmar_senha) await this.confirmarSenhaInput.fill(data.confirmar_senha);
    if (data.pergunta_seguranca) await this.perguntaSegurancaInput.fill(data.pergunta_seguranca);
    if (data.resposta_seguranca) await this.respostaSegurancaInput.fill(data.resposta_seguranca);
    await this.submitButton.click();
    // Don't wait for toast here - validation may prevent submit
    await this.page.waitForLoadState('networkidle');
  }

  async gotoLogin(): Promise<void> {
    await this.loginLink.click();
    await this.page.waitForLoadState('networkidle');
  }

  async expectCadastroFormVisible(): Promise<void> {
    await this.expectVisible(this.nomeUsuarioInput);
    await this.expectVisible(this.emailInput);
    await this.expectVisible(this.nomeInput);
    await this.expectVisible(this.senhaInput);
    await this.expectVisible(this.confirmarSenhaInput);
    await this.expectVisible(this.perguntaSegurancaInput);
    await this.expectVisible(this.respostaSegurancaInput);
    await this.expectVisible(this.submitButton);
  }

  async expectValidationError(field: string, message: string): Promise<void> {
    const error = this.page.locator(`[data-error-for="${field}"], .error-${field}, #${field}-error`);
    await expect(error).toBeVisible();
    await expect(error).toContainText(message);
  }
}