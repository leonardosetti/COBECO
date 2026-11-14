import { chromium, FullConfig } from '@playwright/test';
import { createTestUser } from './utils/test-data';

async function globalSetup(config: FullConfig) {
  const baseURL = process.env.BASE_URL || 'http://localhost:8380';
  
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  try {
    await page.goto(`${baseURL}/health`, { timeout: 30000 });
    await page.waitForLoadState('networkidle');
    console.log('✓ Health check passed');
  } catch (error) {
    console.error('✗ Health check failed:', error);
    throw error;
  } finally {
    await browser.close();
  }
  
  const timestamp = Date.now();
  const testUser = createTestUser({ nome_usuario: `e2e_test_${timestamp}` });
  
  process.env.TEST_USER = JSON.stringify(testUser);
  
  console.log('✓ Global setup completed');
}

export default globalSetup;