const { test, expect } = require("@playwright/test");
test("structured facts are readable in detail and comparison without losing conditions", async ({
  page,
}) => {
  await page.goto("/monitor-v3.html");
  await page.locator("#monitor-search").fill("PA279CRV");
  await page.locator('.product-card [data-action="detail"]').click();
  const hdmi = page
    .locator("#detail-dialog tbody tr")
    .filter({
      has: page.getByRole("rowheader", { name: "HDMI", exact: true }),
    });
  await expect(hdmi).toContainText("버전: 2.0");
  await expect(hdmi).toContainText("개수: 2");
  await expect(hdmi).not.toContainText('{"');
  await expect(page.locator("#detail-dialog")).toContainText(
    "제조사 추정 (MANUFACTURER_ESTIMATE)",
  );
  await expect(page.locator("#detail-dialog")).toContainText(
    "Daisy chain; directional split unspecified",
  );
  await page.keyboard.press("Escape");
  await page.locator('.product-card [data-action="select"]').click();
  await page.locator("#monitor-search").fill("M28U");
  await page.locator('.product-card [data-action="select"]').click();
  await page.locator("#compare-open").click();
  await expect(page.locator("#compare-table")).toContainText("버전: 2.0");
  await expect(page.locator("#compare-table")).toContainText("한국 SKU 미확인");
});
test("unknown structured keys are escaped and retained rather than executed", async ({
  page,
}) => {
  await page.addInitScript(() => {
    window.__formatterAttack = false;
  });
  await page.route("**/monitor-v3-data.js", async (route) => {
    const response = await route.fetch();
    const body = await response.text();
    await route.fulfill({
      response,
      body:
        body +
        '\nwindow.CONNECTABLE_MONITORS.products[0].facts[0].value={future_key:"<img src=x onerror=window.__formatterAttack=true>", count:0};',
    });
  });
  await page.goto("/monitor-v3.html");
  // Select by the fixture product identity, not the visual list order.
  const id = await page.evaluate(
    () => window.CONNECTABLE_MONITORS.products[0].id,
  );
  await page
    .locator(`.product-card[data-product-id="${id}"] [data-action="detail"]`)
    .click();
  await expect(page.locator("#detail-dialog")).toContainText(
    "future_key: <img src=x onerror=window.__formatterAttack=true>",
  );
  await expect(page.locator("#detail-dialog img")).toHaveCount(0);
  expect(await page.evaluate(() => window.__formatterAttack)).toBe(false);
});
