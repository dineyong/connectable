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
  await page.route('**/monitor-review-links-data.js', route => route.fulfill({contentType:'application/javascript',body:'window.CONNECTABLE_REVIEW_LINKS={schema_version:1,items:[]};'}));
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
  await expect(section.locator('a')).toHaveCount(reviews.items.filter(item => item.product_id === 'monitor:gigabyte-m32u').length);
  for (const link of await section.locator('a').all()) {
    await expect(link).toHaveAttribute('target','_blank');
    await expect(link).toHaveAttribute('rel','noopener noreferrer');
  }
  const other = require('../../data/site/monitor-v3.json').products?.find(p => !reviews.items.some(item => item.product_id === p.id));
  if (other) {
    await page.goto(`/monitors/${other.id.replace('monitor:', '')}/`);
    await expect(page.locator('.review-links-empty')).toContainText('아직 이 모델');
  }
});

test('video and blog links use reviewed model bindings and open separately without embeds', async ({page,context}) => {
  const base = {...reviews.items[0],product_id:'monitor:gigabyte-m32u'};
  const good = [
    {...base,id:'fixture-video',site:'YouTube',url:'https://www.youtube.com/watch?v=AbCdEf_1234'},
    {...base,id:'fixture-blog',site:'NaverBlog',url:'https://blog.naver.com/testhandle/123456789'},
    {...base,id:'fixture-custom-blog',site:'Blog',url:'https://review.example.test/2024/model.html'},
    {...base,id:'fixture-forum',site:'Forum',url:'https://forum.example.test/threads/model.123/'}
  ];
  const bad = [
    {...good[0],id:'fixture-query',url:good[0].url+'&redirect=evil'},
    {...good[0],id:'fixture-port',url:'https://www.youtube.com:443/watch?v=AbCdEf_1234'},
    {...good[0],id:'fixture-unregistered',url:'https://www.youtube.com/watch?v=XbCdEf_1234'},
    {...good[1],id:'fixture-host',url:'https://blog.naver.com.evil.test/testhandle/123456789'},
    {...good[2],id:'fixture-unregistered-blog',url:'https://evil.example.test/2024/model.html'},
    {...good[3],id:'fixture-unregistered-forum',url:'https://forum.example.test/threads/other.456/'},
    {...good[3],id:'fixture-spoof-forum',url:'https://forum.example.test.evil.test/threads/model.123/'},
    {...good[1],id:'fixture-traversal',url:'https://blog.naver.com/testhandle/../testhandle/123456789'}
  ];
  const reviewed_bindings = good.map(({product_id,site,url}) => ({product_id,site,url}));
  await page.route('**/monitor-review-links-data.js', route => route.fulfill({contentType:'application/javascript',body:`window.CONNECTABLE_REVIEW_LINKS=${JSON.stringify({schema_version:1,items:[...good,...bad],reviewed_bindings})};`}));
  await page.goto('/monitor-v3.html');
  const section = await openDetail(page, base.product_id);
  await expect(section.locator('a')).toHaveCount(4);
  await expect(section).toContainText('영상 리뷰');
  await expect(section).toContainText('네이버 블로그');
  await expect(section).toContainText('커뮤니티');
  await expect(section.locator('iframe,img')).toHaveCount(0);
  for (const item of good) {
    const link = section.locator(`a[href="${item.url}"]`);
    await expect(link).toHaveAttribute('target','_blank');
    await expect(link).toHaveAttribute('rel','noopener noreferrer');
  }
  await context.route('https://www.youtube.com/**', route => route.fulfill({contentType:'text/html',body:'<!doctype html><title>Fixture video</title>'}));
  const popup = context.waitForEvent('page');
  await section.locator('a[href*="youtube.com"]').click();
  const destination = await popup;
  await destination.waitForLoadState();
  await expect(destination).toHaveTitle('Fixture video');
  expect(await destination.evaluate(() => window.opener)).toBeNull();
  await destination.close();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
});
