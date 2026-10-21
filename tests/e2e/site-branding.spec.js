const { test, expect } = require('@playwright/test');

test('모니픽 brand and page metadata agree while private-review gates remain', async ({page}) => {
  for (const path of [
    '/monitor-v3.html', '/monitors/', '/monitors/asus-pa279crv/',
    '/guides/monitor-buying.html', '/tech-news.html', '/information.html', '/404.html',
    '/monitor10-review.html',
  ]) {
    await page.goto(path);
    const title = await page.title();
    expect(title).toContain('모니픽');
    await expect(page.locator('header .brand')).toContainText('모니픽');
    await expect(page.locator('meta[property="og:site_name"]')).toHaveAttribute('content', '모니픽');
    await expect(page.locator('meta[property="og:title"]')).toHaveAttribute('content', title);
    await expect(page.locator('meta[property="og:description"]')).toHaveAttribute(
      'content', await page.locator('meta[name="description"]').getAttribute('content'),
    );
    await expect(page.locator('meta[name="robots"]')).toHaveAttribute('content', /noindex/);
    await expect(page.locator('link[rel="canonical"],meta[property="og:url"]')).toHaveCount(0);
    await expect(page.locator('body')).not.toContainText('로컬 미리보기');
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
  }
});
