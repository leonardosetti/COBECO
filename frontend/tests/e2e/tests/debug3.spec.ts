import { test, expect } from '@playwright/test';

test('debug hash routing', async ({ page }) => {
  const logs: string[] = [];
  page.on('console', msg => logs.push(`${msg.type()}: ${msg.text()}`));
  page.on('pageerror', err => logs.push(`ERROR: ${err.message}`));
  
  await page.goto('http://localhost:8480/#/login');
  await page.waitForLoadState('networkidle');
  
  // Wait for appReady
  await page.evaluate(() => window.appReady);
  await page.waitForTimeout(2000);
  
  const state = await page.evaluate(() => window.state);
  console.log('State view:', state?.view);
  console.log('State ready:', state?.ready);
  console.log('Location hash:', await page.evaluate(() => window.location.hash));
  
  console.log('Console logs:');
  logs.forEach(log => console.log(log));
  
  // Check main content
  const mainContent = await page.locator('main').innerHTML();
  console.log('Main content length:', mainContent.length);
  console.log('Main content preview:', mainContent.substring(0, 500));
});