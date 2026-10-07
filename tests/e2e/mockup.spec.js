const { test, expect } = require("@playwright/test");
const AxeBuilder = require("@axe-core/playwright").default;

test.beforeEach(async ({ page }) => {
  await page.goto("/");
});

test("required fields, unknown result and stale summary", async ({ page }) => {
  await page.getByRole("button", { name: "확인할 연결 조건 보기" }).click();
  await expect(page.locator("#form-error")).toContainText("선택해 주세요");
  await expect(page.locator("#source")).toBeFocused();
  await page.locator("#source").selectOption("MacBook Pro");
  await page.locator("#chip").selectOption("M1 Pro");
  await page.locator("#connection").selectOption("USB-C 허브");
  await page.locator("#charging").check();
  await page.getByRole("button", { name: "확인할 연결 조건 보기" }).click();
  await expect(page.locator("#result")).toContainText(
    "아직 확인되지 않은 구성",
  );
  await expect(page.locator("#result")).toContainText("충전 조건");
  await page.locator("#chip").selectOption("M2");
  await expect(page.locator("#result")).toContainText("구성이 변경됐어요");
  await expect(page.locator("#result")).not.toContainText("M1 Pro");
});

test("search, filter and pagination", async ({ page }) => {
  await expect(page.locator(".story-card")).toHaveCount(6);
  await page.getByRole("button", { name: "사례 더 보기" }).click();
  await expect(page.locator(".story-card")).toHaveCount(12);
  await page.getByRole("button", { name: "미해결", exact: true }).click();
  await expect(page.locator('[data-filter="UNRESOLVED"]')).toHaveAttribute(
    "aria-pressed",
    "true",
  );
  for (const text of await page.locator(".outcome-tag").allTextContents())
    expect(text).toBe("미해결");
  await page.locator("#case-search").fill("없는사례000");
  await expect(page.locator("#empty-search")).toBeVisible();
  await expect(page.locator("#search-count")).toContainText("0건");
  await page.locator("#case-search").fill("");
  await expect(page.locator("#empty-search")).toBeHidden();
});

test("dialog source, escape and focus return", async ({ page }) => {
  const card = page.locator(".story-card").first();
  await card.click();
  await expect(page.getByRole("dialog")).toBeVisible();
  await expect(page.getByRole("dialog")).toHaveAccessibleName(
    await page.locator("#dialog-title").innerText(),
  );
  await expect(page.locator(".dialog-warning")).toContainText("공식 사양 대조");
  const href = await page.locator(".source-link").getAttribute("href");
  expect(href).toMatch(/^https:\/\//);
  await page.keyboard.press("Escape");
  await expect(page.getByRole("dialog")).toBeHidden();
  await expect(card).toBeFocused();
});

test("hostile input remains text", async ({ page }) => {
  await page.locator("#source").selectOption("MacBook Air");
  await page.locator("#chip").selectOption("M1");
  await page.locator("#connection").selectOption("HDMI 직접 연결");
  await page.locator("#display").fill('<img src=x onerror="alert(1)">');
  await page.getByRole("button", { name: "확인할 연결 조건 보기" }).click();
  await expect(page.locator("#result")).toContainText("<img src=x");
  await expect(page.locator("#result img")).toHaveCount(0);
});

test("no overflow or client errors; preview headers", async ({ page }) => {
  const errors = [];
  page.on("pageerror", (e) => errors.push(e.message));
  const response = await page.goto("/");
  expect(response.headers()["content-security-policy"]).toContain(
    "connect-src 'none'",
  );
  expect(response.headers()["x-content-type-options"]).toBe("nosniff");
  const width = await page.evaluate(() => ({
    document: document.documentElement.scrollWidth,
    viewport: innerWidth,
  }));
  expect(width.document).toBeLessThanOrEqual(width.viewport);
  await page.getByRole("button", { name: "사례 더 보기" }).click();
  expect(errors).toEqual([]);
  const denied = await page.request.get("/../data/research/user_questions.csv");
  expect(denied.status()).toBe(404);
});

test("WCAG automated accessibility: page and detail", async ({ page }) => {
  const results = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa", "wcag21aa"])
    .analyze();
  expect(
    results.violations.map((v) => ({
      id: v.id,
      nodes: v.nodes.map((n) => n.target),
    })),
  ).toEqual([]);
  await page.locator(".story-card").first().click();
  const dialog = await new AxeBuilder({ page })
    .include("#case-dialog")
    .withTags(["wcag2a", "wcag2aa", "wcag21aa"])
    .analyze();
  expect(
    dialog.violations.map((v) => ({
      id: v.id,
      nodes: v.nodes.map((n) => n.target),
    })),
  ).toEqual([]);
});
