const { test, expect } = require("@playwright/test");

test("partial reviews distinguish checked labels from unknown numeric fields", async ({
  page,
}) => {
  await page.goto("/");
  await page
    .locator('#monitor-list button[data-id="product:jooyon-v32ue"]')
    .click();
  const facts = page.locator(".fact-review").filter({ hasText: "부분 검증" });
  await expect(facts).toContainText("확인된 필드: 해상도 표기");
  await expect(facts).toContainText("가로 픽셀 · 세로 픽셀 · 주사율");
  await expect(facts).toContainText("한국 SKU 동일성 및 호환성 승인 보류");
  await page.keyboard.press("Escape");
  await page
    .locator('#monitor-list button[data-id="product:crossover-27uld950"]')
    .click();
  await expect(
    page.locator(".fact-review").filter({ hasText: "부분 검증" }),
  ).toContainText("공급 W 미확인");
  await expect(page.locator("#detail-body")).not.toContainText("65W 공급");
  await page.keyboard.press("Escape");
  await page.locator("#addon-filter").selectOption("pd");
  await expect(page.locator("#monitor-list")).not.toContainText("27ULD950");
  await expect(page.locator("#monitor-count")).toHaveText("4개 모델");
});

test("LG rated and regional up-to evidence remain separate in details and comparison", async ({
  page,
}) => {
  await page.goto("/");
  await page
    .locator('#monitor-list button[data-id="product:lg-27up850-w"]')
    .click();
  await expect(page.locator("#detail-body")).toContainText("정격 (RATED)");
  await expect(page.locator("#detail-body")).toContainText("최대 상한 (UP_TO)");
  await expect(page.locator("#detail-body")).toContainText("지역 LV");
  await expect(page.locator("#detail-body")).toContainText(
    "한국 판매 SKU 적용 미확인",
  );
  await page.keyboard.press("Escape");
  await page.locator('[data-compare="product:lg-27up850-w"]').check();
  await page.locator('[data-compare="product:crossover-27uld950"]').check();
  await page.locator("#compare-open").click();
  const row = page
    .locator(".comparison tr")
    .filter({
      has: page.getByRole("rowheader", {
        name: "공식 PD 공급 전력 상한·표기",
        exact: true,
      }),
    });
  await expect(row).toContainText("정격 (RATED)");
  await expect(row).toContainText("최대 상한 (UP_TO)");
  await expect(row).toContainText("제품명 표기만 확인");
  await expect(row).toContainText("공급 W 미확인");
});

test("missing field review metadata never creates completed verification", async ({
  page,
}) => {
  await page.route("**/site-content-v2.js", async (route) => {
    const response = await route.fetch();
    await route.fulfill({
      response,
      body:
        (await response.text()) +
        "\nfor(const m of window.CONNECTABLE_SITE_V2.monitors) for(const f of m.features) delete f.field_review;",
    });
  });
  await page.goto("/");
  await page
    .locator('#monitor-list button[data-id="product:jooyon-v32ue"]')
    .click();
  await expect(page.locator("#detail-body")).toContainText("검토 정보 없음");
  await expect(page.locator("#detail-body")).not.toContainText(
    "모델 범위 공식 재확인",
  );
});
