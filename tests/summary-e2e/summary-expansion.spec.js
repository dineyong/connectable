require('../content-e2e/content-review.spec');
const {test,expect}=require('@playwright/test');
const AxeBuilder=require('@axe-core/playwright').default;
const expansion=require('../../data/editorial/monitor-summary-expansion.json');

test('all 27 remaining summaries show bound facts, dates and unresolved scope',async({page})=>{
  test.setTimeout(120000);
  for (const item of expansion.products){
    await page.goto('/monitors/'+item.product_id.replace('monitor:','')+'/');
    const section=page.locator('section[aria-labelledby=model-highlights]');
    await expect(section).toHaveCount(1);
    for (const claim of item.claims) await expect(section).toContainText(claim.summary);
    await expect(section).toContainText(item.caution);
    await expect(section).toContainText('문서 지역:');
    await expect(section).toContainText('호환성 승인이 아닙니다');
    expect(await page.locator('meta[name=description]').getAttribute('content')).toBe(item.description);
    for(const link of await section.locator('a[target=_blank]').all()){
      expect(await link.getAttribute('rel')).toBe('noopener noreferrer');
      await expect(link).toHaveText(/공식 근거 · \d{4}-\d{2}-\d{2}/);
    }
    expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
  }
});

test('conflicts, long regional SKU and alternate modes remain accessible',async({page})=>{
  for(const slug of ['lg-27up850k-w','msi-mag-274qrf-qd-e2','samsung-s65uc-ls34c650ueexxy','lg-32gs95ue-b','dell-u2724d']){
    await page.goto('/monitors/'+slug+'/');
    expect((await new AxeBuilder({page}).analyze()).violations).toEqual([]);
    await expect(page.locator('#specs')).toBeVisible();
    if(['lg-27up850k-w','msi-mag-274qrf-qd-e2'].includes(slug))
      await expect(page.locator('aside.source-conflict')).toContainText('충돌이 해소된 것으로 해석하지 마세요');
  }
});
