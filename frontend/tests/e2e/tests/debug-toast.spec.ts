import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';

test('debug toast', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  
  // Try login with invalid credentials
  await loginPage.login('inexistente', 'Senha@123');
  
  // Wait a bit for toast
  await page.waitForTimeout(2000);
  
  // Check for toast elements
  const toasts = await page.locator('.toast, [role="alert"], .alert').all();
  console.log('Number of toast elements:', toasts.length);
  
  for (const toast of toasts) {
    const text = await toast.textContent();
    console.log('Toast text:', text);
    const classes = await toast.getAttribute('class');
    console.log('Toast classes:', classes);
    const role = await toast.getAttribute('role');
    console.log('Toast role:', role);
  }
  
  // Check if any toast is visible
  const visibleToast = await page.locator('.toast, [role="alert"], .alert').first().isVisible();
  console.log('Any toast visible:', visibleToast);
});