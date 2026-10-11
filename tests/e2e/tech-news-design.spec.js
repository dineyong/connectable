const { test, expect } = require("@playwright/test");

async function snapshot(page, data) {
  await page.route("**/tech-news-data.js", (route) =>
    route.fulfill({
      contentType: "application/javascript",
      body: `window.CONNECTABLE_TECH_NEWS=${JSON.stringify(data)};`,
    }),
  );
}
const source = {
  id: "fixture",
  name: "출처 예시",
  url: "https://news.samsung.com/kr/feed",
  status: "OK",
  kind: "MANUFACTURER_NEWSROOM",
  language: "ko",
};
const article = {
  source_id: "fixture",
  title: "테스트 소식",
  url: "https://news.samsung.com/kr/test",
  category: "TECH",
  published_at: "2026-10-10T10:00:00Z",
};

test("news navigation and saved snapshot are explicit on desktop and mobile", async ({
  page,
}) => {
  await page.goto("/tech-news.html");
  await expect(
    page
      .getByRole("navigation", { name: "주요 메뉴" })
      .getByRole("link", { name: "모니터 찾기" }),
  ).toHaveAttribute("href", "monitor-v3.html");
  await expect(page.getByRole("link", { name: "구매 가이드" })).toHaveAttribute(
    "href",
    "guides/monitor-buying.html",
  );
  await expect(page.locator('[aria-current="page"]')).toHaveText("테크 소식");
  await expect(page.locator(".snapshot")).toContainText("저장된 목록");
  await expect(page.locator(".snapshot")).toContainText(
    "새 기사를 직접 수집하지 않습니다",
  );
  await expect(page.locator("#news-count")).toHaveText(
    `표시 중 ${await page.locator(".news-card").count()}건`,
  );
  await page.getByText("출처별 수집 상태 보기", { exact: true }).click();
  await expect(page.locator("#news-sources")).toBeVisible();
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
  ).toBe(true);
});

test("malformed source and unknown dates do not break valid headlines or invent timestamps", async ({
  page,
}) => {
  const errors = [];
  page.on("pageerror", (error) => errors.push(error.message));
  await snapshot(page, {
    updated_at: "invalid",
    sources: [null, source, { ...source, id: "broken", url: "not-a-url" }],
    items: [
      null,
      { ...article, source_id: "broken" },
      { ...article, published_at: "invalid" },
    ],
  });
  await page.goto("/tech-news.html");
  await expect(page.locator(".news-card")).toHaveCount(1);
  await expect(page.locator("#news-status")).toContainText("시각 미확인");
  await expect(page.locator(".news-card .meta")).toContainText(
    "발행 시각 미확인",
  );
  await expect(page.locator("#news-count")).toHaveText("표시 중 1건");
  await page.selectOption("#news-filter", "MONITOR_DISPLAY");
  await expect(page.locator("#news-count")).toHaveText("표시 중 0건");
  await expect(page.locator("#news-empty")).toBeVisible();
  expect(errors).toEqual([]);
});

test("missing snapshot shows recoverable error and disables unusable filtering", async ({
  page,
}) => {
  const errors = [];
  page.on("pageerror", (error) => errors.push(error.message));
  await snapshot(page, { items: [] });
  await page.goto("/tech-news.html");
  await expect(page.locator("#news-status")).toContainText(
    "불러오지 못했습니다",
  );
  await expect(page.locator("#news-filter")).toBeDisabled();
  await expect(
    page.getByRole("button", { name: "목록 다시 보기" }),
  ).toBeEnabled();
  await expect(page.locator(".news-card")).toHaveCount(0);
  expect(errors).toEqual([]);
});
