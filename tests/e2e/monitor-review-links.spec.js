const { test, expect } = require('@playwright/test');
const reviews = require('../../data/site/monitor-review-links.json');

async function openDetail(page, id) {
  const button = page.locator(`[data-action="detail"][data-id="${id}"]`);
  await button.click();
  const section = page.locator('#detail-dialog .external-reviews');
  await section.scrollIntoViewIfNeeded();
  return section;
}

test('external review cards keep source, advertising and official facts separate; open new tabs', async ({page, context}) => {
  await page.goto('/monitor-v3.html');
  const section = await openDetail(page, 'monitor:gigabyte-m32u');
  await expect(section).toContainText('공식 사양·제품 평가 점수·호환성 승인이 아니며');
  await expect(section).toContainText('전문 리뷰');
  await expect(section).toContainText('개인 사용기');
  await expect(section).toContainText('광고·제휴 여부 미확인');
  const expected = reviews.items.filter(item => item.product_id === 'monitor:gigabyte-m32u');
  await expect(section.locator('a')).toHaveCount(expected.length);
  for (const item of expected) {
    const link = section.locator(`a[href="${item.url}"]`);
    await expect(link).toHaveAttribute('target', '_blank');
    await expect(link).toHaveAttribute('rel', 'noopener noreferrer');
    await expect(link).toHaveAccessibleName(/새 창 또는 새 탭/);
  }
  await context.route('https://www.rtings.com/**', route => route.fulfill({contentType:'text/html', body:'<!doctype html><title>Mock review destination</title><p>Review destination</p>'}));
  const newPage = context.waitForEvent('page');
  await section.locator('a').first().click();
  const destination = await newPage;
  await destination.waitForLoadState();
  await expect(destination).toHaveTitle('Mock review destination');
  expect(await destination.evaluate(() => window.opener)).toBeNull();
  await destination.close();
  await expect(page).toHaveURL(/monitor-v3\.html/);
  await expect(section.locator('img')).toHaveCount(0);
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
});

test('models without connected reviews show a clear empty state without borrowing other model links', async ({page}) => {
  await page.goto('/monitor-v3.html');
  const section = await openDetail(page, 'monitor:dell-u2724d');
  await expect(section).toContainText('아직 이 모델에 연결해 확인한 외부 후기 링크가 없습니다.');
  await expect(section.locator('a')).toHaveCount(0);
});

test('missing review payload preserves product detail and states review load failure', async ({page}) => {
  await page.route('**/monitor-review-links-data.js', route => route.fulfill({contentType:'application/javascript',body:''}));
  await page.goto('/monitor-v3.html');
  const section = await openDetail(page, 'monitor:gigabyte-m32u');
  await expect(section).toContainText('후기 링크 데이터를 불러오지 못했습니다.');
  await expect(page.locator('#detail-content .fact-value').first()).toBeVisible();
});

test('tampered review URLs and uncertain model scope fail closed while text is escaped and wraps', async ({page}) => {
  const good = {...reviews.items[0], title:'<img src=x onerror=alert(1)>' + '긴 제목 '.repeat(25), summary:'<script>window.injected=true</script>'};
  const badUrls = ['javascript:alert(1)','https://www.rtings.com.evil.test/monitor/reviews/gigabyte/m32u','https://www.rtings.com@evil.test/monitor/reviews/gigabyte/m32u','https://www.rtings.com/monitor/reviews/gigabyte/m32u?redirect=evil','https://www.rtings.com/%256aavascript'];
  const items = [good, ...badUrls.map((url,i) => ({...good,id:`bad-${i}`,url})), {...good,id:'uncertain',model_scope:'UNKNOWN'}, {...good,id:'bad-kind',review_type:'UNKNOWN'}];
  await page.route('**/monitor-review-links-data.js', route => route.fulfill({contentType:'application/javascript',body:`window.CONNECTABLE_REVIEW_LINKS=${JSON.stringify({schema_version:1,items})};`}));
  await page.goto('/monitor-v3.html');
  const section = await openDetail(page, good.product_id);
  await expect(section.locator('a')).toHaveCount(1);
  await expect(section.locator('img,script')).toHaveCount(0);
  await expect(section).toContainText('<script>window.injected=true</script>');
  expect(await page.evaluate(() => window.injected)).toBeUndefined();
  const fits = await section.evaluate(el => el.scrollWidth <= el.clientWidth);
  expect(fits).toBe(true);
});

test('static product documents retain review links without JavaScript and distinct empty state', async ({page}) => {
  await page.goto('/monitors/gigabyte-m32u/');
  const section = page.locator('.external-reviews');
  await expect(section.locator('a')).toHaveCount(2);
  for (const link of await section.locator('a').all()) {
    await expect(link).toHaveAttribute('target','_blank');
    await expect(link).toHaveAttribute('rel','noopener noreferrer');
  }
  await page.goto('/monitors/dell-u2724d/');
  await expect(page.locator('.review-links-empty')).toContainText('아직 이 모델');
});
