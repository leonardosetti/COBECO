import { Page, Locator } from '@playwright/test';
import { BasePage } from './BasePage';

export class LoginPage extends BasePage {
  readonly usuarioInput: Locator;
  readonly senhaInput: Locator;
  readonly submitButton: Locator;
  readonly cadastrarLink: Locator;
  readonly recuperarSenhaLink: Locator;

  constrdoc-arch-0006-uc-v1tor(page: Page) {
    super(page);
    this.usuarioInput = page.locator('input[name="nome_usuario"]');
    this.senhaInput = page.locator('input[name="senha"]');
    this.submitButton = page.locator('button[type="submit"]');
    this.cadastrarLink = page.locator('[data-link="/cadastrar"], a[href="#/cadastrar"]');
    this.recuperarSenhaLink = page.locator('[data-link="/recuperar-senha"], a[href="#/recuperar-senha"]');
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
    await this.page.waitForLoadState('networkidle');
  }

  async expectLoginFormVisible(): Promise<void> {
    await this.expectVisible(this.usuarioInput);
    await this.expectVisible(this.senhaInput);
    await this.expectVisible(this.submitButton);
  }
}