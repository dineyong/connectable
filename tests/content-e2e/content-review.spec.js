// Apply the same existing functional/CSP checks to the proposed content variant.
require('../release-e2e/public-candidate.spec');
const {test,expect}=require('@playwright/test');
const AxeBuilder=require('@axe-core/playwright').default;

test('three fact summaries retain caveats, sources and mobile access',async({page})=>{
  for (const [id,power] of [['asus-pa279crv','96W'],['msi-modern-md271ul','65W'],['dell-u2724de','Thunderbolt']]){
    await page.goto(`/monitors/${id}/`);
    const section=page.locator('section[aria-labelledby=model-highlights]');
    await expect(section).toContainText(power);
    await expect(section).toContainText('미확인');
    await expect(section).toContainText('호환성 승인이 아닙니다');
    expect(await section.locator('a[target=_blank]').count()).toBeGreaterThan(0);
    expect((await new AxeBuilder({page}).analyze()).violations).toEqual([]);
    expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
  }
});

test('product navigation goes directly to final route and guide anchor',async({page})=>{
  await page.goto('/monitors/asus-pa279crv/');
  const links=await page.locator('a[href]').evaluateAll(xs=>xs.map(a=>a.getAttribute('href')));
  expect(links.filter(h=>!/^https?:/.test(h)&&/\.html(?:[?#]|$)/.test(h))).toEqual([]);
  await page.getByRole('link',{name:'USB-C·포트 선택 가이드',exact:true}).click();
  await expect(page).toHaveURL(/\/guides\/monitor-buying#usb-c$/);
  await expect(page.locator('#usb-c')).toBeVisible();
});
