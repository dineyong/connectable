const {test,expect}=require('@playwright/test');
const AxeBuilder=require('@axe-core/playwright').default;
test('buying guide links, evidence and responsive layout remain usable',async({page})=>{
 await page.goto('/monitor-v3.html');
 await page.getByRole('link',{name:'주사율까지, 구매 가이드 모두 보기 →'}).click();
 await expect(page).toHaveTitle(/모니터 구매 가이드/);
 for(const anchor of ['resolution','refresh','usb-c','comparison']) {
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

test('buying guide preserves uncertainty and opens official evidence in a new tab',async({page})=>{
 await page.goto('/guides/monitor-buying.html');
 const comparison=page.locator('#comparison');
 await page.locator('.guide-nav a[href="#comparison"]').click();
 await expect(comparison).toBeVisible();
 for(const heading of ['미확인은 미지원이 아닙니다','모델명 뒤의 지역·SKU도 확인하세요','정격과 최대, 공급과 소비는 구분합니다','단위와 연결 조건이 같아야 비교할 수 있어요','공식 사양과 후기는 서로 다른 정보입니다']) {
  await expect(comparison.getByRole('heading',{name:heading})).toBeVisible();
 }
 await expect(comparison).toContainText('한국 판매 제품에 그대로 적용하지 않습니다');
 await expect(comparison).toContainText('실제 충전 성공을 확인한 결과가 아닙니다');
 const evidence=page.locator('article .source a');
 for(let i=0;i<await evidence.count();i++) {
  await expect(evidence.nth(i)).toHaveAttribute('target','_blank');
  await expect(evidence.nth(i)).toHaveAttribute('rel','noopener noreferrer');
  await expect(evidence.nth(i)).toContainText('(새 창)');
 }
 // Avoid depending on the availability of an external support service.
 await page.context().route('https://support.microsoft.com/**',route=>route.fulfill({status:200,contentType:'text/html',body:'<!doctype html><html lang="ko"><title>공식 근거 링크 확인</title></html>'}));
 const popupPromise=page.waitForEvent('popup');
 await evidence.first().click();
 const popup=await popupPromise;
 await popup.waitForLoadState();
 expect(popup.url()).toContain('support.microsoft.com');
 await expect(page).toHaveURL(/guides\/monitor-buying\.html#comparison$/);
 await popup.close();
});
