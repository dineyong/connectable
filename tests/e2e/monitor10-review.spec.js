const { test, expect } = require('@playwright/test');
const AxeBuilder = require('@axe-core/playwright').default;

test('supplement is reachable without replacing original comparison data', async ({page}) => {
  await page.goto('/monitor-v3.html');
  await expect(page.locator('#product-grid .product-card')).toHaveCount(30);
  await page.getByRole('link', {name:'추가 확인 자료 10종 보기 →'}).click();
  await expect(page).toHaveURL(/monitor10-review\.html$/);
  for (let i=1; i<=10; i++) await expect(page.locator('#m10-'+String(i).padStart(2,'0'))).toBeVisible();
  await expect(page.locator('meta[name="robots"]')).toHaveAttribute('content', /noindex/);
  await expect(page.locator('iframe, script[type="application/ld+json"], a[href*="coupang"]')).toHaveCount(0);
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
});

test('supplement retains evidence and uncertainty with accessible mobile and desktop layout', async ({page}) => {
  await page.goto('/monitor10-review.html');
  const msi=page.locator('#m10-08');
  await expect(msi).toContainText(/충돌|CONFLICT/);
  await expect(page.locator('#m10-04')).toContainText(/리비전|Rev/);
  await expect(page.locator('#m10-10')).toContainText(/미확인|UNKNOWN/);
  expect(await page.locator('a[href^="https://"]').count()).toBeGreaterThanOrEqual(80);
  const audit=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa']).analyze();
  expect(audit.violations.map(v=>({id:v.id,nodes:v.nodes.map(n=>n.target)}))).toEqual([]);
});

test('context links keep revision and similarly named Dell models separate', async ({page}) => {
  await page.goto('/monitor-v3.html');
  const open = async (model) => page.locator('.product-card').filter({has: page.getByRole('heading', {name:model, exact:true})}).locator('[data-action="detail"]').click();
  await page.locator('#monitor-search').fill('M27Q');
  await page.locator('.product-card [data-action="detail"]').click();
  await expect(page.locator('#detail-dialog a[href="monitor10-review.html#m10-04"]')).toContainText('다른 리비전');
  await page.keyboard.press('Escape');
  await page.locator('#monitor-search').fill('U2724DE');
  await page.locator('.product-card [data-action="detail"]').click();
  await expect(page.locator('#detail-dialog a[href*="monitor10-review"]')).toHaveCount(0);
});
