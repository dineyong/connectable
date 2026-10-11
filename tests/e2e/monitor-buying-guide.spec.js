const {test,expect}=require('@playwright/test');
const AxeBuilder=require('@axe-core/playwright').default;
test('buying guide links, evidence and responsive layout remain usable',async({page})=>{
 await page.goto('/monitor-v3.html');
 await page.getByRole('link',{name:'주사율까지, 구매 가이드 모두 보기 →'}).click();
 await expect(page).toHaveTitle(/모니터 구매 가이드/);
 for(const anchor of ['resolution','refresh','usb-c']) {
  await page.locator(`.guide-nav a[href="#${anchor}"]`).click();
  await expect(page.locator(`#${anchor}`)).toBeVisible();
 }
 await expect(page.locator('article .source a')).toHaveCount(3);
 await expect(page.locator('meta[name="robots"]')).toHaveAttribute('content','noindex,nofollow');
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
 expect((await new AxeBuilder({page}).analyze()).violations).toEqual([]);
 await page.locator('.guide-cta').click();
 await expect(page.locator('#result-count')).toContainText('30');
});
