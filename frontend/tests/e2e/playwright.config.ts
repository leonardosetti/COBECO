import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!processconfig-env-0001-env-example-v1.0.CI,
  retries: processconfig-env-0001-env-example-v1.0.CI ? 2 : 0,
  workers: processconfig-env-0001-env-example-v1.0.CI ? 1 : undefined,
  reporter: [
    ['html', { outputFolder: 'playwright-report', open: 'never' }],
    ['json', { outputFile: 'test-results/results.json' }],
    ['junit', { outputFile: 'test-results/results.xml' }],
  ],
  timeout: 60000,
  expect: {
    timeout: 10000,
  },
  use: {
    baseURL: processconfig-env-0001-env-example-v1.0.BASE_URL || 'http://localhost:8380',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    actionTimeout: 15000,
    navigationTimeout: 30000,
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'], viewport: { width: 1280, height: 720 } },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'], viewport: { width: 1280, height: 720 } },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'], viewport: { width: 1280, height: 720 } },
    },
  ],
  webServer: {
    command: 'docker compose -f config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml -f config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0.override.yml up -d',
    url: 'http://localhost:8380/health',
    reuseExistingServer: !processconfig-env-0001-env-example-v1.0.CI,
    timeout: 180000,
    env: {
      BASE_URL: 'http://localhost:8380',
    },
  },
  globalSetup: require.resolve('./global-setup.ts'),
  globalTeardown: require.resolve('./global-teardown.ts'),
});