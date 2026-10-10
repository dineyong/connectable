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
