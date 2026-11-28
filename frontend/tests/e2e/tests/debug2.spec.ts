import { test, expect } from '@playwright/test';

test('debug console', async ({ page }) => {
  const logs: string[] = [];
  page.on('console', msg => logs.push(`${msg.type()}: ${msg.text()}`));
  page.on('pageerror', err => logs.push(`ERROR: ${err.message}`));
  
  await page.goto('http://localhost:8480/#/login');
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(5000);
  
  console.log('Console logs:');
  logs.forEach(log => console.log(log));
});