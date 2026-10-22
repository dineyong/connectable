const { defineConfig, devices } = require('@playwright/test');
module.exports = defineConfig({
  testDir: './tests/release-e2e',
  fullyParallel: true,
  reporter: [['list']],
  use: { baseURL: 'http://127.0.0.1:8876', trace: 'retain-on-failure' },
  projects: [
    { name: 'desktop', use: { ...devices['Desktop Chrome'] } },
    { name: 'mobile', use: { ...devices['iPhone 13'], defaultBrowserType: 'chromium' } },
  ],
  webServer: {
    command: 'python3 -m scripts.serve_monipick_candidate --port 8876',
    url: 'http://127.0.0.1:8876', reuseExistingServer: false,
  },
});
