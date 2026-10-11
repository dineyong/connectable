const {test,expect}=require('@playwright/test');
const data=require('../../data/site/monitor-v3.json');
const key='connectable-v3-comparison';
test('comparison survives same-tab navigation and can be cleared',async({page})=>{
 await page.goto('/monitor-v3.html');
 await page.locator('#compare-start').click();
 await page.locator('#compare-pick-1').selectOption(data.products[0].id);
 await page.locator('#compare-pick-2').selectOption(data.products[1].id);
 await page.locator('#compare-picker-submit').click();
 await page.locator('[data-close="compare-dialog"]').click();
 await page.goto('/tech-news.html');await page.goto('/monitor-v3.html');
 await expect(page.locator('#selection-count')).toContainText('2 / 3');
 if(page.viewportSize().width<=760){const box=await page.locator('#compare-tray').boundingBox();expect(box.height).toBeLessThan(180);expect(box.width).toBeLessThanOrEqual(page.viewportSize().width);}
 await page.locator('#compare-open').click();
 await expect(page.locator('#compare-table')).toContainText(data.products[0].display_model);
 await page.locator('[data-close="compare-dialog"]').click();
 await page.locator('#compare-clear').click();await page.reload();
 await expect(page.locator('#compare-tray')).toBeHidden();
});
test('corrupt comparison data is preserved and does not crash search',async({page})=>{
 await page.goto('/monitor-v3.html');await page.evaluate(k=>sessionStorage.setItem(k,'broken-json'),key);await page.reload();
 await page.locator('#product-grid [data-action="select"]').first().click();
 await expect(page.locator('#comparison-storage-status')).toContainText('기존');
 expect(await page.evaluate(k=>sessionStorage.getItem(k),key)).toBe('broken-json');
 await page.locator('#monitor-search').fill('4K');await page.locator('#monitor-search').press('Enter');await expect(page.locator('#products-title')).toBeInViewport();
});
test('blocked session storage keeps comparison usable without false persistence',async({page})=>{
 await page.addInitScript(()=>Object.defineProperty(window,'sessionStorage',{get(){throw new Error('blocked')}}));
 await page.goto('/monitor-v3.html');await page.locator('#product-grid [data-action="select"]').first().click();
 await expect(page.locator('#comparison-storage-status')).toContainText('현재 화면에서만');
});
test('news search intersects source and category without changing curated announcements',async({page})=>{
 await page.goto('/tech-news.html');await page.locator('#news-source-filter').selectOption('windows-blog');
 await expect(page.locator('.news-card').first()).toContainText('Windows Blog');
 await page.locator('#news-search').fill('no-such-news-zzz');await expect(page.locator('#news-empty')).toBeVisible();
 await expect(page.locator('.announcement-card')).toHaveCount(2);
 await page.locator('#news-search').fill('');await expect(page.locator('.news-card').first()).toBeVisible();
});
