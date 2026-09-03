import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  use: { baseURL: 'http://localhost:5173', trace: 'on-first-retry' },
  projects: [{ name: 'chromium', use: { ...devices['Desktop Chrome'] } }],
  webServer: [
    {
      command: 'npm run dev --prefix ../api',
      port: 3333,
      reuseExistingServer: true,
      env: {
        NODE_ENV: 'test',
        JWT_ACCESS_SECRET: 'e2e-access-secret-01234567890123456789',
        JWT_REFRESH_SECRET: 'e2e-refresh-secret-0123456789012345678',
      },
    },
    { command: 'npm run dev', port: 5173, reuseExistingServer: true },
  ],
});
