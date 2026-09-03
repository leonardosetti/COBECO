import { expect, test } from '@playwright/test';

test('cadastro, login, lista e cotação por paridade', async ({ page }) => {
  const suffix = Date.now();
  const email = `e2e-${suffix}@example.com`;
  const username = `e2e_${suffix}`;
  const password = 'Senha1234!';

  await page.goto('/sign-up');
  await page.locator('#field-nome').fill('Pessoa E2E');
  await page.locator('#field-nome-de-usuário').fill(username);
  await page.locator('#field-e-mail').fill(email);
  await page.locator('#field-senha').fill(password);
  await page.locator('#field-confirmar-senha').fill(password);
  await page.getByRole('checkbox').check();
  await page.getByRole('button', { name: /criar conta/i }).click();
  await page.waitForURL('**/platform');

  // RF02: o login também aceita o nome de usuário.
  await page.goto('/login');
  await page.locator('#field-e-mail-ou-nome-de-usuário').fill(username);
  await page.locator('#field-senha').fill(password);
  await page.getByRole('button', { name: /fazer login/i }).click();
  await expect(page.getByText(/minhas listas/i)).toBeVisible();

  await page.getByPlaceholder('Nova lista').fill('Compra E2E');
  await page.getByLabel('Criar lista').click();
  await page.getByLabel('Produto').fill('Produto 1');
  await page.getByRole('button', { name: 'Adicionar', exact: true }).click();
  await page.getByRole('button', { name: /cotar lista completa/i }).click();
  await expect(page.getByRole('heading', { name: /grupos por paridade/i })).toBeVisible();
  await expect(page.getByText(/melhor orçamento/i)).toBeVisible();
});
