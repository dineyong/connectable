const {test, expect} = require('@playwright/test');

test('operating guide preserves missing contact, local storage scope and no analytics', async ({page}) => {
  await page.goto('/information.html');
  await expect(page.getByRole('heading', {name: '통계·광고 없이 시작합니다'})).toBeVisible();
  await expect(page.locator('#storage').locator('..')).toContainText('sessionStorage');
  await expect(page.locator('#storage').locator('..')).toContainText('localStorage');
  await expect(page.getByText('외부 수신 확인 대기', {exact: true})).toBeVisible();
  await expect(page.locator('#corrections').locator('..')).toContainText('contact@monipick.com');
  await expect(page.locator('a[href^="mailto:"],form')).toHaveCount(0);
  await expect(page.locator('#corrections').locator('..')).toContainText('자동 반영을 보장하지 않습니다');
  await expect(page.locator('script[src^="https:"],iframe')).toHaveCount(0);
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
});
