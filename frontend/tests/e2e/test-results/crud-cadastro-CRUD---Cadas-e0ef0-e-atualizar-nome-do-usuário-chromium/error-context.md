# Instrdoc-arch-0006-uc-v1tions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: crud/cadastro.spec.ts >> CRUD - Cadastro de Usuário (UC01/RF01) >> UPDATE - Atualizar cadastro (via perfil) >> deve atualizar nome do usuário
- Location: tests/crud/cadastro.spec.ts:127:5

# Error details

```
TimeoutError: locator.waitFor: Timeout 10000ms exceeded.
Call log:
  - waiting for locator('#perfil-nome') to be visible

```

# Page snapshot

```yaml
- generic [active] [ref=f1e1]:
  - banner [ref=f1e2]:
    - generic [ref=f1e3]:
      - generic [ref=f1e4]:
        - heading "COBECO" [level=1] [ref=f1e7]
        - generic [ref=f1e8]: MVP
      - navigation [ref=f1e9]:
        - link "Entrar" [ref=f1e10] [cursor=pointer]:
          - /url: "#/login"
        - link "Cadastrar" [ref=f1e11] [cursor=pointer]:
          - /url: "#/cadastrar"
  - main [ref=f1e12]:
    - generic [ref=f1e13]:
      - heading "Compare preços e economize" [level=2] [ref=f1e14]
      - paragraph [ref=f1e15]: Crie sua lista de compras, compare preços entre fornecedores e encontre o melhor orçamento. Dados mockados para fins acadêmicos.
      - generic [ref=f1e16]:
        - link "Criar Lista" [ref=f1e17] [cursor=pointer]:
          - /url: "#/criar-lista"
        - link "Comparar Preços" [ref=f1e18] [cursor=pointer]:
          - /url: "#/comparar"
    - generic [ref=f1e19]:
      - generic [ref=f1e21]:
        - heading "Crie sua Lista" [level=3] [ref=f1e25]
        - paragraph [ref=f1e26]: Adicione produtos com autocomplete e defina quantidades.
      - generic [ref=f1e28]:
        - heading "Compare Fornecedores" [level=3] [ref=f1e32]
        - paragraph [ref=f1e33]: Filtre por categorias, selecione fornecedores e veja a tabela comparativa.
      - generic [ref=f1e35]:
        - heading "Exporte e Imprima" [level=3] [ref=f1e39]
        - paragraph [ref=f1e40]: Gere PDF profissional ou imprima direto do navegador.
  - contentinfo [ref=f1e41]:
    - generic [ref=f1e42]:
      - paragraph [ref=f1e43]: COBECO MVP — FATEC Taquaritinga — Análise e Desenvolvimento de Sistemas
      - paragraph [ref=f1e44]: Dados mockados para fins acadêmicos — Não representa preços reais de mercado
```

# Test source

```ts
  1  | import { Page, Locator, expect } from '@playwright/test';
  2  | import { BasePage } from './BasePage';
  3  | 
  4  | export interface PerfilData {
  5  |   nome?: string;
  6  |   email?: string;
  7  |   senha_atual?: string;
  8  |   nova_senha?: string;
  9  |   confirmar_nova_senha?: string;
  10 | }
  11 | 
  12 | export class PerfilPage extends BasePage {
  13 |   readonly nomeInput: Locator;
  14 |   readonly emailInput: Locator;
  15 |   readonly senhaAtualInput: Locator;
  16 |   readonly novaSenhaInput: Locator;
  17 |   readonly confirmarNovaSenhaInput: Locator;
  18 |   readonly submitButton: Locator;
  19 |   readonly logoutButton: Locator;
  20 |   readonly nomeDisplay: Locator;
  21 |   readonly usuarioDisplay: Locator;
  22 |   readonly emailDisplay: Locator;
  23 |   readonly criadoEmDisplay: Locator;
  24 | 
  25 |   constrdoc-arch-0006-uc-v1tor(page: Page) {
  26 |     super(page);
  27 |     this.nomeInput = page.locator('#perfil-nome');
  28 |     this.emailInput = page.locator('#perfil-email');
  29 |     this.senhaAtualInput = page.locator('#perfil-senha-atual');
  30 |     this.novaSenhaInput = page.locator('#perfil-nova-senha');
  31 |     this.confirmarNovaSenhaInput = page.locator('#perfil-confirmar-nova-senha');
  32 |     this.submitButton = page.locator('#form-perfil button[type="submit"]');
  33 |     this.logoutButton = page.locator('#btn-logout');
  34 |     this.nomeDisplay = page.locator('#perfil-nome-display, text=/Nome:/');
  35 |     this.usuarioDisplay = page.locator('#perfil-usuario-display, text=/Usuário:/');
  36 |     this.emailDisplay = page.locator('#perfil-email-display, text=/E-mail:/');
  37 |     this.criadoEmDisplay = page.locator('#perfil-criado-em-display, text=/Criado em:/');
  38 |   }
  39 | 
  40 |   async goto(): Promise<void> {
  41 |     await super.goto('/#/perfil');
> 42 |     await this.nomeInput.waitFor({ state: 'visible', timeout: 10000 });
     |                          ^ TimeoutError: locator.waitFor: Timeout 10000ms exceeded.
  43 |   }
  44 | 
  45 |   async atualizarPerfil(data: PerfilData): Promise<void> {
  46 |     if (data.nome !== undefined) await this.nomeInput.fill(data.nome);
  47 |     if (data.email !== undefined) await this.emailInput.fill(data.email);
  48 |     if (data.senha_atual !== undefined) await this.senhaAtualInput.fill(data.senha_atual);
  49 |     if (data.nova_senha !== undefined) await this.novaSenhaInput.fill(data.nova_senha);
  50 |     if (data.confirmar_nova_senha !== undefined) await this.confirmarNovaSenhaInput.fill(data.confirmar_nova_senha);
  51 |     await this.submitButton.click();
  52 |     await this.waitForToast();
  53 |     await this.page.waitForLoadState('networkidle');
  54 |   }
  55 | 
  56 |   async logout(): Promise<void> {
  57 |     await this.logoutButton.click();
  58 |     await this.page.waitForLoadState('networkidle');
  59 |   }
  60 | 
  61 |   async expectPerfilVisible(usuario: string, email: string, nome: string): Promise<void> {
  62 |     // The perfil page shows email and nome in the form fields, not as display text
  63 |     await this.expectVisible(this.nomeInput);
  64 |     await this.expectVisible(this.emailInput);
  65 |     await this.expectValue(this.emailInput, email);
  66 |     await this.expectValue(this.nomeInput, nome);
  67 |   }
  68 | 
  69 |   async expectFormValues(data: PerfilData): Promise<void> {
  70 |     if (data.nome !== undefined) await this.expectValue(this.nomeInput, data.nome);
  71 |     if (data.email !== undefined) await this.expectValue(this.emailInput, data.email);
  72 |   }
  73 | }
```