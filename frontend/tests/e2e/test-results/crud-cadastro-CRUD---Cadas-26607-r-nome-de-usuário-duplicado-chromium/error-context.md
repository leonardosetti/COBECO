# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: crud/cadastro.spec.ts >> CRUD - Cadastro de Usuário (UC01/RF01) >> Validações de Unicidade >> não deve permitir nome de usuário duplicado
- Location: tests/crud/cadastro.spec.ts:199:5

# Error details

```
TypeError: expect(received).toMatch(expected)

Matcher error: received value must be a string

Received has value: undefined
```

# Page snapshot

```yaml
- generic [ref=e1]:
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
            - textbox "Nome de usuário *" [ref=e21]: testuser_1794843477487
            - paragraph [ref=e22]: 3-30 caracteres, apenas letras e números
          - generic [ref=e23]:
            - generic [ref=e24]: Email *
            - textbox "Email *" [ref=e25]: test_1794843477487@example.com
          - generic [ref=e26]:
            - generic [ref=e27]: Nome completo *
            - textbox "Nome completo *" [ref=e28]: Test User 1794843477487
          - generic [ref=e29]:
            - generic [ref=e30]: Senha *
            - textbox "Senha *" [ref=e31]: Senha@123
            - paragraph [ref=e32]: "Mín. 8 chars: 1 maiúscula, 1 minúscula, 1 número, 1 especial"
          - generic [ref=e33]:
            - generic [ref=e34]: Confirmar senha *
            - textbox "Confirmar senha *" [ref=e35]: Senha@123
          - generic [ref=e36]:
            - generic [ref=e37]: Pergunta de segurança *
            - textbox "Pergunta de segurança *" [ref=e38]:
              - /placeholder: "Ex: Nome do seu primeiro animal de estimação?"
              - text: nome_mae
          - generic [ref=e39]:
            - generic [ref=e40]: Resposta *
            - textbox "Resposta *" [active] [ref=e41]: Maria Silva
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
  107 |   test.describe('READ - Verificar usuário cadastrado', () => {
  108 |     test('deve permitir login após cadastro', async ({ cadastroPage, loginPage }) => {
  109 |       const userData = createTestUser();
  110 |       
  111 |       await cadastroPage.goto();
  112 |       await cadastroPage.cadastrar(userData);
  113 |       
  114 |       await loginPage.goto();
  115 |       await loginPage.login(userData.nome_usuario, userData.senha);
  116 |       
  117 |       await expect(loginPage.page.locator('main')).toBeVisible();
  118 |     });
  119 | 
  120 |     test('deve mostrar dados do perfil após login', async ({ authenticatedPage, perfilPage, testUser }) => {
  121 |       await perfilPage.goto();
  122 |       await perfilPage.expectPerfilVisible(testUser.nome_usuario, testUser.email, testUser.nome);
  123 |     });
  124 |   });
  125 | 
  126 |   test.describe('UPDATE - Atualizar cadastro (via perfil)', () => {
  127 |     test('deve atualizar nome do usuário', async ({ authenticatedPage, perfilPage, testUser }) => {
  128 |       const novoNome = `Nome Atualizado ${Date.now()}`;
  129 |       
  130 |       await perfilPage.goto();
  131 |       await perfilPage.atualizarPerfil({ nome: novoNome });
  132 |       await perfilPage.waitForToast('Perfil atualizado');
  133 |       
  134 |       await perfilPage.goto();
  135 |       await perfilPage.expectFormValues({ nome: novoNome });
  136 |     });
  137 | 
  138 |     test('deve atualizar email do usuário', async ({ authenticatedPage, perfilPage }) => {
  139 |       const novoEmail = `novo_${Date.now()}@test.com`;
  140 |       
  141 |       await perfilPage.goto();
  142 |       await perfilPage.atualizarPerfil({ email: novoEmail });
  143 |       await perfilPage.waitForToast('Perfil atualizado');
  144 |       
  145 |       await perfilPage.goto();
  146 |       await perfilPage.expectFormValues({ email: novoEmail });
  147 |     });
  148 | 
  149 |     test('deve alterar senha com senha atual correta', async ({ authenticatedPage, perfilPage, testUser, loginPage }) => {
  150 |       const novaSenha = 'NovaSenha@456';
  151 |       
  152 |       await perfilPage.goto();
  153 |       await perfilPage.atualizarPerfil({
  154 |         senha_atual: testUser.senha,
  155 |         nova_senha: novaSenha,
  156 |         confirmar_nova_senha: novaSenha,
  157 |       });
  158 |       await perfilPage.waitForToast('Perfil atualizado');
  159 |       
  160 |       await perfilPage.logout();
  161 |       await loginPage.goto();
  162 |       await loginPage.login(testUser.nome_usuario, novaSenha);
  163 |       
  164 |       await expect(loginPage.page.locator('main')).toBeVisible();
  165 |     });
  166 | 
  167 |     test('não deve alterar senha com senha atual incorreta', async ({ authenticatedPage, perfilPage, testUser }) => {
  168 |       await perfilPage.goto();
  169 |       await perfilPage.atualizarPerfil({
  170 |         senha_atual: 'SenhaErrada@123',
  171 |         nova_senha: 'NovaSenha@456',
  172 |         confirmar_nova_senha: 'NovaSenha@456',
  173 |       });
  174 |       
  175 |       const toast = await perfilPage.getToastMessage();
  176 |       expect(toast?.toLowerCase()).toMatch(/senha|incorreta|atual/);
  177 |     });
  178 | 
  179 |     test('deve exigir confirmação de nova senha', async ({ authenticatedPage, perfilPage, testUser }) => {
  180 |       await perfilPage.goto();
  181 |       await perfilPage.atualizarPerfil({
  182 |         senha_atual: testUser.senha,
  183 |         nova_senha: 'NovaSenha@456',
  184 |         confirmar_nova_senha: 'OutraSenha@456',
  185 |       });
  186 |       
  187 |       const toast = await perfilPage.getToastMessage();
  188 |       expect(toast?.toLowerCase()).toMatch(/senha|coincid|confirmar/);
  189 |     });
  190 |   });
  191 | 
  192 |   test.describe('DELETE - Exclusão de conta (se implementado)', () => {
  193 |     test.skip('deve permitir exclusão da conta', async ({ authenticatedPage, perfilPage, testUser, loginPage }) => {
  194 |       // Este teste será implementado quando houver endpoint de exclusão
  195 |     });
  196 |   });
  197 | 
  198 |   test.describe('Validações de Unicidade', () => {
  199 |     test('não deve permitir nome de usuário duplicado', async ({ cadastroPage, testUser }) => {
  200 |       await cadastroPage.goto();
  201 |       await cadastroPage.cadastrar(testUser);
  202 |       
  203 |       await cadastroPage.goto();
  204 |       await cadastroPage.cadastrar(testUser);
  205 |       
  206 |       const toast = await cadastroPage.getToastMessage();
> 207 |       expect(toast?.toLowerCase()).toMatch(/usuário|já existe|duplicado|único/);
      |                                    ^ TypeError: expect(received).toMatch(expected)
  208 |     });
  209 | 
  210 |     test('não deve permitir email duplicado', async ({ cadastroPage, testUser }) => {
  211 |       await cadastroPage.goto();
  212 |       await cadastroPage.cadastrar(testUser);
  213 |       
  214 |       const outroUsuario = createTestUser({ 
  215 |         nome_usuario: `outro${Date.now()}`,
  216 |         email: testUser.email,
  217 |       });
  218 |       
  219 |       await cadastroPage.goto();
  220 |       await cadastroPage.cadastrar(outroUsuario);
  221 |       
  222 |       const toast = await cadastroPage.getToastMessage();
  223 |       expect(toast?.toLowerCase()).toMatch(/email|já existe|duplicado|único/);
  224 |     });
  225 |   });
  226 | 
  227 |   test.describe('Navegação', () => {
  228 |     test('deve navegar para login a partir do cadastro', async ({ cadastroPage, loginPage }) => {
  229 |       await cadastroPage.goto();
  230 |       await cadastroPage.gotoLogin();
  231 |       await loginPage.expectLoginFormVisible();
  232 |     });
  233 | 
  234 |     test('deve navegar para recuperar senha a partir do login', async ({ loginPage }) => {
  235 |       await loginPage.goto();
  236 |       await loginPage.gotoRecuperarSenha();
  237 |       await expect(loginPage.page.locator('input[name="nome_usuario"]')).toBeVisible();
  238 |     });
  239 |   });
  240 | });
```