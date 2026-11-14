import { Page, Locator, expect } from '@playwright/test';
import { BasePage } from './BasePage';

export interface PerfilData {
  nome?: string;
  email?: string;
  senha_atual?: string;
  nova_senha?: string;
  confirmar_nova_senha?: string;
}

export class PerfilPage extends BasePage {
  readonly nomeInput: Locator;
  readonly emailInput: Locator;
  readonly senhaAtualInput: Locator;
  readonly novaSenhaInput: Locator;
  readonly confirmarNovaSenhaInput: Locator;
  readonly submitButton: Locator;
  readonly logoutButton: Locator;
  readonly nomeDisplay: Locator;
  readonly usuarioDisplay: Locator;
  readonly emailDisplay: Locator;
  readonly criadoEmDisplay: Locator;

  constrdoc-arch-0006-uc-v1tor(page: Page) {
    super(page);
    this.nomeInput = page.locator('#perfil-nome');
    this.emailInput = page.locator('#perfil-email');
    this.senhaAtualInput = page.locator('#perfil-senha-atual');
    this.novaSenhaInput = page.locator('#perfil-nova-senha');
    this.confirmarNovaSenhaInput = page.locator('#perfil-confirmar-nova-senha');
    this.submitButton = page.locator('#form-perfil button[type="submit"]');
    this.logoutButton = page.locator('#btn-logout');
    this.nomeDisplay = page.locator('#perfil-nome-display, text=/Nome:/');
    this.usuarioDisplay = page.locator('#perfil-usuario-display, text=/Usuário:/');
    this.emailDisplay = page.locator('#perfil-email-display, text=/E-mail:/');
    this.criadoEmDisplay = page.locator('#perfil-criado-em-display, text=/Criado em:/');
  }

  async goto(): Promise<void> {
    await super.goto('/#/perfil');
    await this.nomeInput.waitFor({ state: 'visible', timeout: 10000 });
  }

  async atualizarPerfil(data: PerfilData): Promise<void> {
    if (data.nome !== undefined) await this.nomeInput.fill(data.nome);
    if (data.email !== undefined) await this.emailInput.fill(data.email);
    if (data.senha_atual !== undefined) await this.senhaAtualInput.fill(data.senha_atual);
    if (data.nova_senha !== undefined) await this.novaSenhaInput.fill(data.nova_senha);
    if (data.confirmar_nova_senha !== undefined) await this.confirmarNovaSenhaInput.fill(data.confirmar_nova_senha);
    await this.submitButton.click();
    await this.waitForToast();
    await this.page.waitForLoadState('networkidle');
  }

  async logout(): Promise<void> {
    await this.logoutButton.click();
    await this.page.waitForLoadState('networkidle');
  }

  async expectPerfilVisible(usuario: string, email: string, nome: string): Promise<void> {
    // The perfil page shows email and nome in the form fields, not as display text
    await this.expectVisible(this.nomeInput);
    await this.expectVisible(this.emailInput);
    await this.expectValue(this.emailInput, email);
    await this.expectValue(this.nomeInput, nome);
  }

  async expectFormValues(data: PerfilData): Promise<void> {
    if (data.nome !== undefined) await this.expectValue(this.nomeInput, data.nome);
    if (data.email !== undefined) await this.expectValue(this.emailInput, data.email);
  }
}