const { test, expect } = require('@playwright/test');
const AxeBuilder = require('@axe-core/playwright').default;

test('public-format home works with its generated CSP and result CTA', async ({page}) => {
  const violations=[];
  page.on('console', msg => { if (/violates|refused to/i.test(msg.text())) violations.push(msg.text()); });
  const response=await page.goto('/');
  expect(response.status()).toBe(200);
  expect(response.headers()['content-security-policy']).toContain("script-src 'self'");
  await expect(page.locator('.product-card')).toHaveCount(30);
  await expect(page.locator('link[rel=canonical]')).toHaveAttribute('href','https://monipick.com/');
  await expect(page.locator('meta[name=robots]')).toHaveAttribute('content','index,follow');
  await expect(page.locator('.preview-strip')).not.toContainText('비공개 검수');
  await page.locator('[data-purpose="office"]').click();
  await expect(page.locator('#purpose-results-open')).toBeVisible();
  await expect(page.locator('[data-purpose="office"]')).toBeFocused();
  await page.locator('#purpose-results-open').click();
  await expect(page.locator('#products')).toBeFocused();
  expect(violations).toEqual([]);
});

test('search compare and source dialog preserve uncertainty under public CSP', async ({page}) => {
  await page.goto('/');
  for (const model of ['PA279CRV','M28U']) {
    await page.locator('#monitor-search').fill(model);
    await expect(page.locator('.product-card')).toHaveCount(1);
    await page.locator('.product-card [data-action=select]').click();
  }
  await page.locator('#compare-open').click();
  await expect(page.locator('#compare-table')).toContainText('한국 SKU 미확인');
  await page.keyboard.press('Escape');
  await page.locator('.product-card [data-action=detail]').click();
  await expect(page.locator('#detail-dialog')).toContainText('호환성 판정 사용 불가');
  const links=page.locator('#detail-dialog a[target="_blank"]');
  expect(await links.count()).toBeGreaterThan(0);
  for(const link of await links.all()) await expect(link).toHaveAttribute('rel',/noopener/);
});

test('operations and static product metadata use public copy without altering evidence', async ({page}) => {
  await page.goto('/information');
  await expect(page.locator('main')).toContainText('Cloudflare Email Routing');
  await expect(page.locator('a[href="mailto:contact@monipick.com"]')).toBeVisible();
  await expect(page.locator('main')).not.toContainText('공개 전 실제 운영');
  await expect(page.locator('main')).toContainText('전체 이용자 수나 제품 평가 점수로 집계하지 않습니다');
  await page.goto('/monitors/asus-pa279crv/');
  await expect(page.locator('link[rel=canonical]')).toHaveAttribute('href','https://monipick.com/monitors/asus-pa279crv/');
  await expect(page.locator('body')).toContainText('한국 판매 SKU 동일성은 미확인');
  expect((await new AxeBuilder({page}).analyze()).violations).toEqual([]);
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
});

test('missing routes return real 404, and sitemap and redirects resolve correctly', async ({page,request}) => {
  for(const route of ['/missing-release-page','/monitors/missing-release-page/']) {
    const r=await page.goto(route);
    expect(r.status()).toBe(404);
    await expect(page.getByRole('heading',{level:1})).toHaveText('페이지를 찾을 수 없어요.');
  }
  const sitemap=await request.get('/sitemap.xml');
  expect((await sitemap.text()).match(/<loc>/g)).toHaveLength(34);
  const redirect=await request.get('/monitor-v3.html?q=4k',{maxRedirects:0});
  expect(redirect.status()).toBe(301);
  expect(redirect.headers().location).toBe('/?q=4k');
  const forbidden=await request.get('/manifest.json');
  expect(forbidden.status()).toBe(404);
});

test('news renders as dated snapshot and remains excluded from indexing', async ({page}) => {
  const response=await page.goto('/tech-news');
  expect(response.headers()['x-robots-tag']).toBe('noindex, follow');
  await expect(page.locator('meta[name=robots]')).toHaveAttribute('content','noindex,follow');
  await expect(page.locator('.preview-strip')).toContainText('저장된 제조사 소식');
  await expect(page.locator('body')).not.toContainText('비공개 검수 중');
  expect(await page.locator('a[target="_blank"]').count()).toBeGreaterThan(0);
});
