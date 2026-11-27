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
    this.nomeUsuarioInput = page.locator('#c-user');
    this.emailInput = page.locator('#c-email');
    this.nomeInput = page.locator('#c-nome');
    this.senhaInput = page.locator('#c-senha');
    this.confirmarSenhaInput = page.locator('#c-conf');
    this.perguntaSegurancaInput = page.locator('#c-perg');
    this.respostaSegurancaInput = page.locator('#c-resp');
    this.submitButton = page.locator('button[data-action="cadastrar"]');
    this.loginLink = page.locator('[data-action="page-login"]');
  }

  async goto(): Promise<void> {
    await super.goto('/#/cadastrar');
    await this.nomeUsuarioInput.waitFor({ state: 'visible', timeout: 10000 });
    // Wait for submit button to be ready
    await this.submitButton.waitFor({ state: 'visible', timeout: 10000 });
  }

  async cadastrar(data: CadastroData): Promise<string | null> {
    await this.nomeUsuarioInput.fill(data.nome_usuario);
    await this.emailInput.fill(data.email);
    await this.nomeInput.fill(data.nome);
    await this.senhaInput.fill(data.senha);
    await this.confirmarSenhaInput.fill(data.confirmar_senha);
    await this.perguntaSegurancaInput.selectOption(data.pergunta_seguranca);
    await this.respostaSegurancaInput.fill(data.resposta_seguranca);
    
    // Click the cadastrar button (triggers handleCadastro via click dispatcher)
    await this.submitButton.click();
    
    // Wait for toast to appear first (before navigation)
    await this.waitForToast();
    const toast = await this.getToastMessage();
    
    // Wait for navigation to categorias (success case after registration)
    await this.page.waitForURL('**/#/categorias', { timeout: 15000 }).catch(() => {});
    
    await this.page.waitForLoadState('networkidle');
    return toast;
  }

  async cadastrarMinimo(data: Partial<CadastroData>): Promise<void> {
    if (data.nome_usuario) await this.nomeUsuarioInput.fill(data.nome_usuario);
    if (data.email) await this.emailInput.fill(data.email);
    if (data.nome) await this.nomeInput.fill(data.nome);
    if (data.senha) await this.senhaInput.fill(data.senha);
    if (data.confirmar_senha) await this.confirmarSenhaInput.fill(data.confirmar_senha);
    if (data.pergunta_seguranca) await this.perguntaSegurancaInput.selectOption(data.pergunta_seguranca);
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