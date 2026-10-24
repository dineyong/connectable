const { defineConfig, devices } = require('@playwright/test');
module.exports = defineConfig({
  testDir: './tests/summary-e2e',
  fullyParallel: true,
  reporter: [['list']],
  use: { baseURL: 'http://127.0.0.1:8899', trace: 'retain-on-failure' },
  projects: [
    { name: 'desktop', use: { ...devices['Desktop Chrome'] } },
    { name: 'mobile', use: { ...devices['iPhone 13'], defaultBrowserType: 'chromium' } },
  ],
  webServer: {
    command: 'python3 -m scripts.serve_monipick_summary_expansion --port 8899',
    url: 'http://127.0.0.1:8899', reuseExistingServer: false,
  },
});
