const { test, expect } = require('@playwright/test');
const AxeBuilder = require('@axe-core/playwright').default;

test('monitor search has a visible persistent label instead of a placeholder-only name', async ({ page }) => {
  await page.goto('/monitor-v3.html');
  await expect(page.locator('label[for="monitor-search"]')).toBeVisible();
  const results = await new AxeBuilder({ page }).withRules(['label-title-only']).analyze();
  expect(results.violations).toEqual([]);
  await page.locator('#monitor-search').fill('PA279CRV');
  await expect(page.locator('label[for="monitor-search"]')).toBeVisible();
  await expect(page.locator('#product-grid .product-card')).toHaveCount(1);
});

test('local preview warning belongs to a named landmark without changing release status', async ({ page }) => {
  await page.goto('/monitor-v3.html');
  await expect(page.getByRole('region', { name: '비공개 검수 안내' })).toContainText('한국 SKU와 호환성 검토 전');
  const results = await new AxeBuilder({ page }).withRules(['region']).analyze();
  expect(results.violations).toEqual([]);
  await expect(page.locator('meta[name="robots"]')).toHaveAttribute('content', /noindex/);
});
