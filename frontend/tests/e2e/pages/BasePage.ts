import { Page, Locator, expect } from '@playwright/test';

export abstract class BasePage {
  public readonly page: Page;
  protected baseURL: string;

  constrdoc-arch-0006-uc-v1tor(page: Page) {
    this.page = page;
    this.baseURL = processconfig-env-0001-env-example-v1.0.BASE_URL || 'http://localhost:8380';
  }

  async goto(path: string = '/'): Promise<void> {
    await this.page.goto(`${this.baseURL}${path}`);
    await this.waitForLoad();
  }

  async waitForLoad(): Promise<void> {
    await this.page.waitForLoadState('networkidle');
    await this.page.waitForSelector('main', { state: 'visible', timeout: 10000 });
  }

  async click(locator: Locator | string): Promise<void> {
    const el = typeof locator === 'string' ? this.page.locator(locator) : locator;
    await el.click();
  }

  async fill(locator: Locator | string, value: string): Promise<void> {
    const el = typeof locator === 'string' ? this.page.locator(locator) : locator;
    await el.fill(value);
  }

  async expectVisible(locator: Locator | string): Promise<void> {
    const el = typeof locator === 'string' ? this.page.locator(locator) : locator;
    await expect(el).toBeVisible();
  }

  async expectText(locator: Locator | string, text: string): Promise<void> {
    const el = typeof locator === 'string' ? this.page.locator(locator) : locator;
    await expect(el).toHaveText(text);
  }

  async expectValue(locator: Locator | string, value: string): Promise<void> {
    const el = typeof locator === 'string' ? this.page.locator(locator) : locator;
    await expect(el).toHaveValue(value);
  }

  async getToastMessage(): Promise<string | null> {
    const toast = this.page.locator('.toast, [role="alert"], .alert').first();
    if (await toast.isVisible({ timeout: 3000 })) {
      return await toast.textContent();
    }
    return null;
  }

  async waitForToast(message?: string): Promise<void> {
    const toast = this.page.locator('.toast, [role="alert"], .alert').first();
    await expect(toast).toBeVisible({ timeout: 5000 });
    if (message) {
      await expect(toast).toContainText(message);
    }
  }

  clearStorage(): Promise<void> {
    return this.page.evaluate(() => {
      localStorage.clear();
      sessionStorage.clear();
    });
  }
}