const { test, expect } = require("@playwright/test");
const data = require("../../data/site/monitor-v3.json");
const actual = (page) =>
  page
    .locator("#product-grid .product-card")
    .evaluateAll((cards) => cards.map((c) => c.dataset.productId).sort());
const expected = (fn) =>
  data.products
    .filter(fn)
    .map((p) => p.id)
    .sort();
test("purpose shortcuts apply exactly their visible numeric conditions without charging or compatibility inference", async ({
  page,
}) => {
  await page.goto("/monitor-v3.html");
  const cases = [
    [
      "office",
      (p) =>
        p.filters.width >= 2560 &&
        p.filters.height >= 1440 &&
        p.filters.refresh !== null &&
        p.filters.refresh <= 120,
    ],
    ["gaming", (p) => p.filters.refresh >= 144],
    ["creative", (p) => p.filters.width === 3840 && p.filters.height === 2160],
    ["laptop", (p) => p.filters.usb_c_video === true],
  ];
  for (const [id, fn] of cases) {
    await page.locator(`[data-purpose="${id}"]`).click();
    expect(await actual(page)).toEqual(expected(fn));
    await expect(
      page.locator('[data-purpose][aria-pressed="true"]'),
    ).toHaveCount(1);
  }
  await page.locator("#purpose-all").click();
  await expect(page.locator(".product-card")).toHaveCount(30);
  await expect(page.locator("#purpose-result")).toBeHidden();
  await expect(page.locator('[data-purpose][aria-pressed="true"]')).toHaveCount(
    0,
  );
});
test("purpose retains brand selection and manual condition changes clear shortcut highlight", async ({
  page,
}) => {
  await page.goto("/monitor-v3.html");
  if (!(await page.locator("#brand-options").isVisible()))
    await page.locator("#filters > summary").click();
  await page.locator('#brand-options input[value="LG"]').check();
  await page.locator('[data-purpose="gaming"]').click();
  expect(await actual(page)).toEqual(
    expected((p) => p.manufacturer === "LG" && p.filters.refresh >= 144),
  );
  await page.locator("#filter-refresh").selectOption("240");
  await expect(page.locator('[data-purpose][aria-pressed="true"]')).toHaveCount(
    0,
  );
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
  ).toBe(true);
});

test("purpose previews count and only navigates after explicit result click", async ({page}) => {
  await page.goto('/monitor-v3.html');
  await expect(page.locator('[data-purpose="laptop"]')).toContainText('맥북·맥미니');
  for (const purpose of ['office','gaming']) {
    await page.locator(`[data-purpose="${purpose}"]`).click();
    await expect(page.locator(`[data-purpose="${purpose}"]`)).toBeFocused();
    await expect(page.locator('#purpose-result')).toBeVisible();
    const count = await page.locator('.product-card').count();
    await expect(page.locator('#purpose-results-open')).toContainText(`${count}개 보기`);
    await page.locator('#purpose-results-open').click();
    await expect(page.locator('#products')).toBeFocused();
    await expect(page.locator('#products-title')).toBeInViewport();
  }
});

test("direct comparison picker rejects missing and duplicate choices and compares two or three", async ({page}) => {
  await page.goto('/monitor-v3.html');
  await page.locator('#compare-start').click();
  await page.locator('#compare-picker-submit').click();
  await expect(page.locator('#compare-picker-status')).toContainText('첫 번째와 두 번째');
  const ids = data.products.slice(0,3).map(p=>p.id);
  await page.locator('#compare-pick-1').selectOption(ids[0]);
  await page.locator('#compare-pick-2').selectOption(ids[0]);
  await page.locator('#compare-picker-submit').click();
  await expect(page.locator('#compare-picker-status')).toContainText('서로 다른');
  await page.locator('#compare-pick-2').selectOption(ids[1]);
  await page.locator('#compare-picker-submit').click();
  await expect(page.locator('#compare-dialog')).toBeVisible();
  await expect(page.locator('#compare-table')).toContainText(data.products[0].display_model);
  await expect(page.locator('#compare-table')).toContainText(data.products[1].display_model);
  await page.locator('[data-close="compare-dialog"]').click();
  await page.locator('#compare-start').click();
  await page.locator('#compare-pick-3').selectOption(ids[2]);
  await page.locator('#compare-picker-submit').click();
  await expect(page.locator('#compare-table')).toContainText(data.products[2].display_model);
  await page.locator('[data-close="compare-dialog"]').click();
  await page.locator('#compare-start').click();
  await page.locator('#compare-pick-1').selectOption('');
  await page.keyboard.press('Escape');
  await expect(page.locator('#selection-count')).toContainText('3 / 3');
});

test("purpose preview preserves zero results without inventing matches", async ({page}) => {
 await page.goto('/monitor-v3.html');
 await page.locator('#monitor-search').fill('nonexistent-model-zzz');
 await page.locator('[data-purpose="office"]').click();
 await expect(page.locator('#purpose-results-open')).toContainText('0개 보기');
 await expect(page.locator('#purpose-result-description')).toContainText('조건을 바꾸거나');
 await page.locator('#purpose-results-open').click();
 await expect(page.locator('#empty-state')).toBeVisible();
});
