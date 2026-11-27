import { Page, Locator } from '@playwright/test';
import { BasePage } from './BasePage';

export class LoginPage extends BasePage {
  readonly usuarioInput: Locator;
  readonly senhaInput: Locator;
  readonly submitButton: Locator;
  readonly cadastrarLink: Locator;
  readonly recuperarSenhaLink: Locator;
  readonly logoutButton: Locator;

  constructor(page: Page) {
    super(page);
    this.usuarioInput = page.locator('#l-user');
    this.senhaInput = page.locator('#l-pass');
    this.submitButton = page.locator('button[data-action="login"]');
    this.cadastrarLink = page.locator('[data-action="page-cadastro"]');
    this.recuperarSenhaLink = page.locator('[data-action="page-recuperar-senha"]');
    this.logoutButton = page.locator('[data-action="sair"]');
  }

  async goto(): Promise<void> {
    await super.goto('/#/login');
    await this.usuarioInput.waitFor({ state: 'visible', timeout: 10000 });
  }

  async login(usuario: string, senha: string): Promise<void> {
    await this.usuarioInput.fill(usuario);
    await this.senhaInput.fill(senha);
    await this.submitButton.click();
    await this.page.waitForLoadState('networkidle');
  }

  async gotoCadastro(): Promise<void> {
    await this.cadastrarLink.click();
    await this.page.waitForLoadState('networkidle');
  }

  async gotoRecuperarSenha(): Promise<void> {
    await this.recuperarSenhaLink.click();
    // Wait for hash change to recovery page (uses cadastro view)
    await this.page.waitForFunction(() => window.location.hash === '#/recuperar-senha');
    await this.page.waitForLoadState('networkidle');
    // Wait for cadastro form to be visible (recovery uses cadastro view)
    await this.page.waitForSelector('#c-user', { state: 'visible', timeout: 10000 });
  }

  async expectLoginFormVisible(): Promise<void> {
    await this.expectVisible(this.usuarioInput);
    await this.expectVisible(this.senhaInput);
    await this.expectVisible(this.submitButton);
  }

  async logout(): Promise<void> {
    await this.logoutButton.waitFor({ state: 'visible', timeout: 10000 });
    await this.logoutButton.click();
    await this.page.waitForLoadState('networkidle');
  }
}