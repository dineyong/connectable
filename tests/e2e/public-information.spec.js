const { test, expect } = require('@playwright/test');
const AxeBuilder = require('@axe-core/playwright').default;

test('source guidance is reachable and preserves evidence and local participation limits', async ({ page }) => {
  await page.goto('/monitor-v3.html');
  await page.getByRole('link', { name: '자료·비교 기준', exact: true }).click();
  await expect(page.getByRole('heading', { level: 1 })).toHaveText('자료와 비교 기준');
  await expect(page.locator('main')).toContainText('한국 판매 SKU 미확인');
  await expect(page.locator('main')).toContainText('전체 이용자 수나 제품 평가 점수로 집계하지 않습니다');
  await expect(page.locator('meta[name=robots]')).toHaveAttribute('content', /noindex/);
  expect((await new AxeBuilder({ page }).analyze()).violations).toEqual([]);
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
});

test('404 template offers root-relative recovery links for nested missing routes', async ({ page }) => {
  await page.goto('/404.html');
  await expect(page.getByRole('heading', { level: 1 })).toHaveText('페이지를 찾을 수 없어요.');
  await expect(page.getByRole('link', { name: '모니터 검색', exact: true })).toHaveAttribute('href', '/monitor-v3.html');
  await expect(page.getByRole('link', { name: '전체 제품 목록', exact: true })).toHaveAttribute('href', '/monitors/');
  await expect(page.locator('meta[name=robots]')).toHaveAttribute('content', /noindex/);
  expect((await new AxeBuilder({ page }).analyze()).violations).toEqual([]);
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
});
