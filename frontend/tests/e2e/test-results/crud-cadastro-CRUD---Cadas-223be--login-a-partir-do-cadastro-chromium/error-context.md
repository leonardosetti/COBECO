# Instrdoc-arch-0006-uc-v1tions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: crud/cadastro.spec.ts >> CRUD - Cadastro de Usuário (UC01/RF01) >> Navegação >> deve navegar para login a partir do cadastro
- Location: tests/crud/cadastro.spec.ts:228:5

# Error details

```
Error: locator.click: Error: strict mode violation: locator('[data-link="/login"], a[href="#/login"]') resolved to 2 elements:
    1) <a href="#/login" class="btn btn-ghost text-sm">Entrar</a> aka getByRole('link', { name: 'Entrar' })
    2) <a data-link="" href="#/login" class="text-primary-600 hover:underline">Entre</a> aka getByRole('link', { name: 'Entre' })

Call log:
  - waiting for locator('[data-link="/login"], a[href="#/login"]')

```

# Page snapshot

```yaml
- generic [active] [ref=e1]:
  - banner [ref=e2]:
    - generic [ref=e3]:
      - generic [ref=e4]:
        - heading "COBECO" [level=1] [ref=e7]
        - generic [ref=e8]: MVP
      - navigation [ref=e9]:
        - link "Entrar" [ref=e10] [cursor=pointer]:
          - /url: "#/login"
        - link "Cadastrar" [ref=e11] [cursor=pointer]:
          - /url: "#/cadastrar"
  - main [ref=e12]:
    - generic [ref=e14]:
      - heading "Criar conta" [level=2] [ref=e16]
      - generic [ref=e17]:
        - generic [ref=e18]:
          - generic [ref=e19]:
            - generic [ref=e20]: Nome de usuário *
            - textbox "Nome de usuário *" [ref=e21]
            - paragraph [ref=e22]: 3-30 caracteres, apenas letras e números
          - generic [ref=e23]:
            - generic [ref=e24]: Email *
            - textbox "Email *" [ref=e25]
          - generic [ref=e26]:
            - generic [ref=e27]: Nome completo *
            - textbox "Nome completo *" [ref=e28]
          - generic [ref=e29]:
            - generic [ref=e30]: Senha *
            - textbox "Senha *" [ref=e31]
            - paragraph [ref=e32]: "Mín. 8 chars: 1 maiúscula, 1 minúscula, 1 número, 1 especial"
          - generic [ref=e33]:
            - generic [ref=e34]: Confirmar senha *
            - textbox "Confirmar senha *" [ref=e35]
          - generic [ref=e36]:
            - generic [ref=e37]: Pergunta de segurança *
            - textbox "Pergunta de segurança *" [ref=e38]:
              - /placeholder: "Ex: Nome do seu primeiro animal de estimação?"
          - generic [ref=e39]:
            - generic [ref=e40]: Resposta *
            - textbox "Resposta *" [ref=e41]
          - button "Criar conta" [ref=e42] [cursor=pointer]
        - paragraph [ref=e43]:
          - text: Já tem conta?
          - link "Entre" [ref=e44] [cursor=pointer]:
            - /url: "#/login"
  - contentinfo [ref=e45]:
    - generic [ref=e46]:
      - paragraph [ref=e47]: COBECO MVP — FATEC Taquaritinga — Análise e Desenvolvimento de Sistemas
      - paragraph [ref=e48]: Dados mockados para fins acadêmicos — Não representa preços reais de mercado
```

# Test source

```ts
  1   | import { Page, Locator, expect } from '@playwright/test';
  2   | import { BasePage } from './BasePage';
  3   | 
  4   | export interface CadastroData {
  5   |   nome_usuario: string;
  6   |   email: string;
  7   |   nome: string;
  8   |   senha: string;
  9   |   confirmar_senha: string;
  10  |   pergunta_seguranca: string;
  11  |   resposta_seguranca: string;
  12  | }
  13  | 
  14  | export class CadastroPage extends BasePage {
  15  |   readonly nomeUsuarioInput: Locator;
  16  |   readonly emailInput: Locator;
  17  |   readonly nomeInput: Locator;
  18  |   readonly senhaInput: Locator;
  19  |   readonly confirmarSenhaInput: Locator;
  20  |   readonly perguntaSegurancaInput: Locator;
  21  |   readonly respostaSegurancaInput: Locator;
  22  |   readonly submitButton: Locator;
  23  |   readonly loginLink: Locator;
  24  | 
  25  |   constrdoc-arch-0006-uc-v1tor(page: Page) {
  26  |     super(page);
  27  |     this.nomeUsuarioInput = page.locator('#cad-nome-usuario, input[name="nome_usuario"]');
  28  |     this.emailInput = page.locator('#cad-email, input[name="email"]');
  29  |     this.nomeInput = page.locator('#cad-nome, input[name="nome"]');
  30  |     this.senhaInput = page.locator('#cad-senha, input[name="senha"]');
  31  |     this.confirmarSenhaInput = page.locator('#cad-confirmar-senha, input[name="confirmar_senha"]');
  32  |     this.perguntaSegurancaInput = page.locator('#cad-pergunta, input[name="pergunta_seguranca"]');
  33  |     this.respostaSegurancaInput = page.locator('#cad-resposta, input[name="resposta_seguranca"]');
  34  |     this.submitButton = page.locator('button[type="submit"]');
  35  |     this.loginLink = page.locator('[data-link="/login"], a[href="#/login"]');
  36  |   }
  37  | 
  38  |   async goto(): Promise<void> {
  39  |     await super.goto('/#/cadastrar');
  40  |     await this.nomeUsuarioInput.waitFor({ state: 'visible', timeout: 10000 });
  41  |     // Wait for form submit handler to be attached (router bindEvents)
  42  |     await this.page.waitForFunction(
  43  |       () => {
  44  |         const form = document.querySelector('#form-cadastro');
  45  |         return form && form.onsubmit != null;
  46  |       },
  47  |       { timeout: 15000 }
  48  |     );
  49  |   }
  50  | 
  51  |   async cadastrar(data: CadastroData): Promise<string | null> {
  52  |     await this.nomeUsuarioInput.fill(data.nome_usuario);
  53  |     await this.emailInput.fill(data.email);
  54  |     await this.nomeInput.fill(data.nome);
  55  |     await this.senhaInput.fill(data.senha);
  56  |     await this.confirmarSenhaInput.fill(data.confirmar_senha);
  57  |     await this.perguntaSegurancaInput.fill(data.pergunta_seguranca);
  58  |     await this.respostaSegurancaInput.fill(data.resposta_seguranca);
  59  |     
  60  |     // Submit form via dispatchEvent to trigger onsubmit handler
  61  |     await this.page.evaluate(() => {
  62  |       const form = document.querySelector('#form-cadastro');
  63  |       if (form) {
  64  |         const event = new Event('submit', { cancelable: true, bubbles: true });
  65  |         form.dispatchEvent(event);
  66  |       }
  67  |     });
  68  |     
  69  |     // Wait for navigation to login (sdoc-arch-0006-uc-v1cess case)
  70  |     await this.page.waitForURL('**/#/login', { timeout: 10000 }).catch(() => {});
  71  |     
  72  |     // Try to get toast message before navigation
  73  |     const toast = await this.getToastMessage();
  74  |     await this.page.waitForLoadState('networkidle');
  75  |     return toast;
  76  |   }
  77  | 
  78  |   async cadastrarMinimo(data: Partial<CadastroData>): Promise<void> {
  79  |     if (data.nome_usuario) await this.nomeUsuarioInput.fill(data.nome_usuario);
  80  |     if (data.email) await this.emailInput.fill(data.email);
  81  |     if (data.nome) await this.nomeInput.fill(data.nome);
  82  |     if (data.senha) await this.senhaInput.fill(data.senha);
  83  |     if (data.confirmar_senha) await this.confirmarSenhaInput.fill(data.confirmar_senha);
  84  |     if (data.pergunta_seguranca) await this.perguntaSegurancaInput.fill(data.pergunta_seguranca);
  85  |     if (data.resposta_seguranca) await this.respostaSegurancaInput.fill(data.resposta_seguranca);
  86  |     await this.submitButton.click();
  87  |     // Don't wait for toast here - validation may prevent submit
  88  |     await this.page.waitForLoadState('networkidle');
  89  |   }
  90  | 
  91  |   async gotoLogin(): Promise<void> {
> 92  |     await this.loginLink.click();
      |                          ^ Error: locator.click: Error: strict mode violation: locator('[data-link="/login"], a[href="#/login"]') resolved to 2 elements:
  93  |     await this.page.waitForLoadState('networkidle');
  94  |   }
  95  | 
  96  |   async expectCadastroFormVisible(): Promise<void> {
  97  |     await this.expectVisible(this.nomeUsuarioInput);
  98  |     await this.expectVisible(this.emailInput);
  99  |     await this.expectVisible(this.nomeInput);
  100 |     await this.expectVisible(this.senhaInput);
  101 |     await this.expectVisible(this.confirmarSenhaInput);
  102 |     await this.expectVisible(this.perguntaSegurancaInput);
  103 |     await this.expectVisible(this.respostaSegurancaInput);
  104 |     await this.expectVisible(this.submitButton);
  105 |   }
  106 | 
  107 |   async expectValidationError(field: string, message: string): Promise<void> {
  108 |     const error = this.page.locator(`[data-error-for="${field}"], .error-${field}, #${field}-error`);
  109 |     await expect(error).toBeVisible();
  110 |     await expect(error).toContainText(message);
  111 |   }
  112 | }
```