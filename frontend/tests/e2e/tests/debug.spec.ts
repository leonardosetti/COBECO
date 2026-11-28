import { test, expect } from '@playwright/test';

test('debug window', async ({ page }) => {
  await page.goto('http://localhost:8480/#/login');
  await page.waitForLoadState('networkidle');
  
  const windowObj = await page.evaluate(() => ({
    appReady: typeof window.appReady,
    state: typeof window.state,
    readyPromise: typeof window.state?.readyPromise,
  }));
  
  console.log('Window object:', JSON.stringify(windowObj, null, 2));
  
  // Wait a bit more
  await page.waitForTimeout(5000);
  
  const windowObj2 = await page.evaluate(() => ({
    appReady: typeof window.appReady,
    state: typeof window.state,
    readyPromise: typeof window.state?.readyPromise,
  }));
  
  console.log('Window object after 5s:', JSON.stringify(windowObj2, null, 2));
});