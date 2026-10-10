const { test, expect } = require("@playwright/test");
test("headline news shows publication dates, manufacturer scope and safe original links", async ({page}) => {
  await page.goto("/tech-news.html");
  await expect(page.getByRole("heading",{name:"새로운 테크 소식"})).toBeVisible();
  await expect(page.locator("#news-status")).toContainText("한국 시간");
  await expect(page.locator(".news-card").first()).toContainText("제조사 소식");
  const anchors = await page.locator(".news-card a").evaluateAll((links)=>links.map(a=>({url:a.href,rel:a.rel})));
  expect(anchors.length).toBeGreaterThan(0);
  for(const a of anchors){expect(a.url).toMatch(/^https:\/\/(news\.samsung\.com|blogs\.windows\.com)\//);expect(a.rel).toContain("noopener");}
  await page.selectOption("#news-filter","MONITOR_DISPLAY");
  for(const card of await page.locator(".news-card").all())await expect(card).toContainText("모니터·디스플레이 · 제목 기반");
});
test("hostile news title is text and unsafe article link is skipped", async({page})=>{
  await page.addInitScript(()=>window.alert=()=>{throw new Error("unexpected alert");});
  await page.route("**/tech-news-data.js",route=>route.fulfill({contentType:"application/javascript",body:`window.CONNECTABLE_TECH_NEWS={updated_at:"2026-10-10T12:00:00Z",sources:[{id:"samsung-kr",name:"출처",url:"https://news.samsung.com/kr/feed",status:"STALE",last_success_at:"2026-10-10T10:00:00Z"}],items:[{source_id:"samsung-kr",title:"<img src=x onerror=alert(1)>",url:"https://news.samsung.com/test",published_at:"2026-10-10T10:00:00Z",category:"TECH"},{source_id:"samsung-kr",title:"Bad link",url:"javascript:alert(1)",published_at:"2026-10-10T10:00:00Z",category:"TECH"}]};`}));
  await page.goto("/tech-news.html");
  await expect(page.locator(".news-card")).toHaveCount(1);
  await expect(page.locator(".news-card h2")).toHaveText("<img src=x onerror=alert(1)>");
  await expect(page.locator(".news-card img")).toHaveCount(0);
  await expect(page.locator("#news-sources")).toContainText("갱신 실패 · 이전 목록");
  await page.selectOption("#news-filter","MONITOR_DISPLAY");
  await expect(page.locator("#news-empty")).toBeVisible();
});

test("news has no accessibility violations or horizontal overflow", async ({page}) => {
  const AxeBuilder = require("@axe-core/playwright").default;
  await page.goto("/tech-news.html");
  await expect(page.locator(".news-card").first()).toBeVisible();
  const results = await new AxeBuilder({page}).analyze();
  expect(results.violations).toEqual([]);
  expect(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth)).toBe(false);
});
