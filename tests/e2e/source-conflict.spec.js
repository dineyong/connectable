const { test, expect } = require('@playwright/test');
const AxeBuilder = require('@axe-core/playwright').default;

test('recorded source conflict stays visible in detail and comparison including differences-only', async ({page}) => {
  await page.goto('/monitor-v3.html');
  const card = model => page.locator('.product-card').filter({has:page.getByRole('heading',{name:model,exact:true})});
  await card('27UP850K-W').getByRole('button',{name:/출처·조건/}).click();
  await expect(page.locator('#detail-content .source-conflict')).toContainText('90W');
  await expect(page.locator('#detail-content .source-conflict')).toContainText('96W');
  await page.locator('[data-close="detail-dialog"]').click();
  for (const m of ['27UP850K-W','PA279CRV']) await card(m).getByRole('button',{name:/비교에 담기/}).click();
  await page.locator('#compare-open').click();
  await expect(page.locator('#compare-table thead .source-conflict')).toHaveCount(1);
  await page.locator('#differences-only').check();
  await expect(page.locator('#compare-table thead .source-conflict')).toBeVisible();
  const results=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa']).analyze();
  expect(results.violations).toEqual([]);
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
});

test('static product shows conflict without JavaScript; unflagged model gets no invented warning', async ({browser}) => {
  const context=await browser.newContext({javaScriptEnabled:false});
  const page=await context.newPage();
  await page.goto('/monitors/lg-27up850k-w/');
  await expect(page.locator('.source-conflict')).toBeVisible();
  await page.goto('/monitors/asus-pa279crv/');
  await expect(page.locator('.source-conflict')).toHaveCount(0);
  await context.close();
});
