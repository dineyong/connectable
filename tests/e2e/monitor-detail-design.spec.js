const {test,expect}=require('@playwright/test');
test('detail cards retain every fact and evidence on a narrow screen',async({page})=>{
 await page.goto('/monitor-v3.html');
 await page.locator('#monitor-search').fill('PA279CRV');
 await page.locator('.product-card [data-action="detail"]').click();
 const rows=page.locator('#detail-dialog tbody tr');
 expect(await rows.count()).toBeGreaterThan(10);
 for(const row of await rows.all()){
  await expect(row.locator('td[data-label]')).toHaveCount(3);
  expect(await row.locator('a[href^="https:"]').count()).toBeGreaterThan(0);
 }
 expect(await page.locator('#detail-dialog').evaluate(e=>e.scrollWidth<=e.clientWidth)).toBe(true);
 await page.keyboard.press('Escape');
 await page.goto('/monitors/asus-pa279crv/');
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
 for(const row of await page.locator('tbody tr').all())await expect(row.locator('td[data-label]')).toHaveCount(2);
});
test('comparison keeps labels sticky and source links intact while horizontally scrolling',async({page})=>{
 await page.goto('/monitor-v3.html');
 for(const model of ['PA279CRV','M28U','U2724D']){
  await page.locator('#monitor-search').fill(model);
  await page.locator('.product-card [data-action="select"]').first().click();
 }
 await page.locator('#compare-open').click();
 const scroll=page.locator('#compare-dialog .table-scroll');
 const cell=page.locator('#compare-table tbody th').first();
 expect(await cell.evaluate(e=>getComputedStyle(e).position)).toBe('sticky');
 const left=(await cell.boundingBox()).x;
 await scroll.evaluate(e=>{e.scrollLeft=e.scrollWidth;});
 expect(Math.abs((await cell.boundingBox()).x-left)).toBeLessThan(2);
 expect(await page.locator('#compare-table a[href^="https:"]').count()).toBeGreaterThan(0);
 await expect(page.locator('#compare-dialog')).toContainText('미확인');
 await page.locator('#differences-only').check();
 await page.locator('#differences-only').uncheck();
});
