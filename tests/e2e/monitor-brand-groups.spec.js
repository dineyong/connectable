const {test, expect} = require('@playwright/test');
const data = require('../../data/site/monitor-v3.json');
test('brand groups retain all products and count filtered results without empty groups', async ({page}) => {
  await page.goto('/monitor-v3.html');
  const brands = [...new Set(data.products.map(p=>p.manufacturer))];
  await expect(page.locator('.brand-group')).toHaveCount(brands.length);
  await expect(page.locator('#product-grid .product-card')).toHaveCount(30);
  for (const brand of brands) {
    const group = page.locator('.brand-group').filter({has:page.getByRole('heading',{name:new RegExp('^'+brand+' ')})});
    await expect(group.locator('.product-card')).toHaveCount(data.products.filter(p=>p.manufacturer===brand).length);
  }
  await page.locator('#monitor-search').fill('PA279CRV');
  await expect(page.locator('.brand-group')).toHaveCount(1);
  await expect(page.locator('.brand-group-title')).toHaveText('ASUS 1종');
  await page.locator('#monitor-search').fill('missing-monitor-xyz');
  await expect(page.locator('.brand-group')).toHaveCount(0);
  await expect(page.locator('#empty-state')).toBeVisible();
});
test('group toggle preserves comparison selection and global sorting remains available', async ({page}) => {
  await page.goto('/monitor-v3.html');
  const first=page.locator('.product-card [data-action="select"]').first();
  await first.click();
  await page.locator('#group-by-brand').uncheck();
  await expect(page.locator('.brand-group')).toHaveCount(0);
  await expect(page.locator('#selection-count')).toContainText('1 / 3');
  await page.locator('#sort-order').selectOption('size');
  await page.locator('#group-by-brand').check();
  await expect(page.locator('#selection-count')).toContainText('1 / 3');
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
});
