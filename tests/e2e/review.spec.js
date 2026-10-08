const { test, expect } = require("@playwright/test");
const AxeBuilder = require("@axe-core/playwright").default;

test.beforeEach(async ({ page }) => {
  await page.goto("/review.html");
});

async function open(page, id) {
  await page.locator(`[data-review-id="${id}"]`).click();
  await expect(page.locator("#review-dialog")).toBeVisible();
  await expect(page.locator("#review-detail-id")).toContainText(id);
}

test("all 18, repeat filters, search, empty and reset", async ({ page }) => {
  await expect(page.locator(".review-card")).toHaveCount(18);
  await expect(page.locator("#review-count")).toContainText("18건 표시");
  await page.locator("#review-feature").selectOption("pd");
  await expect(page.locator(".review-card")).toHaveCount(6);
  await page.locator("#review-feature").selectOption("ui_scale");
  await expect(page.locator(".review-card")).toHaveCount(2);
  await page.locator("#review-search").fill("V32UE");
  await expect(page.locator(".review-card")).toHaveCount(1);
  await page.locator("#review-search").fill("없음-XYZ-888");
  await expect(page.locator("#review-empty")).toBeVisible();
  await page.getByRole("button", { name: "필터 초기화" }).click();
  await expect(page.locator(".review-card")).toHaveCount(18);
  await expect(page.locator("#review-search")).toBeFocused();
  await expect(page.locator("#review-feature")).toHaveValue("ALL");
  await page.getByRole("link", { name: "사례 탐색으로 바로가기" }).focus();
  await page.keyboard.press("Enter");
  await expect(page).toHaveURL(/#review-filters$/);
  await expect(page.locator("#review-count")).toContainText("18건 표시");
  console.log(
    `QA browser ${test.info().project.name}: ${page.context().browser().browserType().name()} ${page.context().browser().version()}`,
  );
  await page.screenshot({
    path: `docs/screenshots/public-usage-review-${test.info().project.name}.png`,
    fullPage: false,
  });
});

test("source link, dates, signal vs UI, own function statuses", async ({
  page,
}) => {
  await open(page, "PUR-001");
  const dialog = page.locator("#review-dialog");
  await expect(dialog).toHaveAccessibleName(
    await page.locator("#review-detail-title").innerText(),
  );
  await expect(dialog).toContainText("2021-12-22");
  await expect(dialog).toContainText("2026-10-08");
  await expect(
    dialog.locator('[data-function="ui_scale"]').first(),
  ).toContainText("3008×1692");
  await expect(
    dialog.locator('[data-function="signal_mode"]').first(),
  ).toContainText("실제 신호 픽셀: 정보 없음");
  await expect(dialog.locator('[data-function="pd"]').first()).toContainText(
    "충전 사용 보고",
  );
  await expect(
    dialog.locator('[data-function="sleep_wake"]').first(),
  ).toContainText("UNKNOWN");
  await expect(dialog).toContainText("공식 사양 대조");
  const link = dialog.getByRole("link", { name: "공개 원문 열기" });
  await expect(link).toHaveAttribute("href", "https://makeany.tistory.com/97");
  await expect(link).toHaveAttribute("rel", "noopener noreferrer");
  await expect(link).toHaveAttribute("referrerpolicy", "no-referrer");
  await dialog.locator(".review-functions").first().scrollIntoViewIfNeeded();
  await page.screenshot({
    path: `docs/screenshots/public-usage-detail-${test.info().project.name}.png`,
    fullPage: false,
  });
});

test("purchase and advice stay separate from performed success", async ({
  page,
}) => {
  await open(page, "PUR-004");
  const d = page.locator("#review-dialog");
  await expect(d.locator(".review-observation")).toHaveCount(1);
  await expect(d).toContainText("목표 구성 · 수행 아님");
  await expect(d).toContainText("제안 구성 · 수행 아님");
  await expect(d).toContainText("타인의 HDMI 설정");
  await expect(d.locator('[data-function="signal_mode"]')).toContainText(
    "선택 가능 상한 · 출력 확인 아님",
  );
  await expect(d.locator('[data-function="video_output"]')).toContainText(
    "문제 보고",
  );
  await expect(
    d.locator(".review-function").filter({ hasText: "정상 보고" }),
  ).toHaveCount(0);
});

test("temporary recurrence, physical count and DisplayLink", async ({
  page,
}) => {
  await open(page, "PUR-009");
  await expect(page.locator("#review-dialog")).toContainText(
    "일시 효과 · 영구 해결 아님",
  );
  await expect(page.locator("#review-dialog")).toContainText(
    "재발 · 이전 정상 관측",
  );
  await page.getByRole("button", { name: "목록으로 돌아가기" }).click();
  await expect(page.locator("#review-dialog")).toBeHidden();
  await open(page, "PUR-013");
  const first = page.locator(".review-observation").first();
  await expect(first).toContainText("일부 복제");
  await expect(
    first.locator("dt", { hasText: "독립 확장 화면" }).locator("+ dd"),
  ).toContainText("UNKNOWN");
  await page.getByRole("button", { name: "목록으로 돌아가기" }).click();
  await expect(page.locator("#review-dialog")).toBeHidden();
  await open(page, "PUR-015");
  await expect(page.locator("#review-dialog")).toContainText(
    "DisplayLink 사용 보고 · 네이티브 출력 아님",
  );
});

test("keyboard, browser back, focus return and filter preservation", async ({
  page,
}) => {
  await page.locator("#review-search").fill("PUR-011");
  const card = page.locator(".review-card");
  await card.focus();
  await page.keyboard.press("Enter");
  await expect(page.locator("#review-dialog")).toBeVisible();
  await expect(page.locator("#review-close")).toBeFocused();
  await page.keyboard.press("Escape");
  await expect(page.locator("#review-dialog")).toBeHidden();
  await expect(card).toBeFocused();
  await expect(page.locator("#review-search")).toHaveValue("PUR-011");
  await card.click();
  await page.goBack();
  await expect(page.locator("#review-dialog")).toBeHidden();
  await expect(card).toBeFocused();
});

test("deep link returns to list and absent case is readable", async ({
  page,
}) => {
  await page.goto("/review.html#PUR-014");
  await expect(page.locator("#review-dialog")).toBeVisible();
  await expect(page.locator("#review-dialog")).toContainText(
    "관측 당시 호스트·기간 UNKNOWN",
  );
  await page.getByRole("button", { name: "목록으로 돌아가기" }).click();
  await expect(page).toHaveURL(/review\.html$/);
  await expect(page.locator(".review-card")).toHaveCount(18);
  await page.goto("/review.html#PUR-019");
  await expect(page.locator("#review-count")).toContainText(
    "요청한 사례 ID가 없습니다",
  );
  await expect(page.locator("#review-dialog")).toBeHidden();
});

test("data missing or invalid is error, never fallback cases", async ({
  page,
}) => {
  await page.route("**/review-data.js", (route) =>
    route.fulfill({
      contentType: "application/javascript",
      body: "window.CONNECTABLE_REVIEW_DATA = {};",
    }),
  );
  await page.reload();
  await expect(page.locator("#review-data-error")).toBeVisible();
  await expect(page.locator(".review-card")).toHaveCount(0);
  await expect(page.locator("#review-count")).toContainText("사례 수 미확인");
  await expect(page.locator("#review-search")).toBeDisabled();
  await page.unroute("**/review-data.js");
  await page.route("**/review-data.js", async (route) => {
    const response = await route.fetch();
    await route.fulfill({
      response,
      body:
        (await response.text()) +
        "\nwindow.CONNECTABLE_REVIEW_DATA.records[0].functionalObservations[0] = null;",
    });
  });
  await page.reload();
  await expect(page.locator("#review-data-error")).toBeVisible();
  await expect(page.locator(".review-card")).toHaveCount(0);
  await page.unroute("**/review-data.js");
  await page.route("**/review-data.js", (route) => route.abort());
  await page.reload();
  await expect(page.locator("#review-data-error")).toBeVisible();
  await expect(page.locator(".review-card")).toHaveCount(0);
});

test("hostile summary is text and private source blocks dataset", async ({
  page,
}) => {
  await page.route("**/review-data.js", async (route) => {
    const response = await route.fetch();
    const js = await response.text();
    await route.fulfill({
      response,
      body:
        js +
        "\nwindow.CONNECTABLE_REVIEW_DATA.records[0].title = '<img src=x onerror=\"alert(1)\">';",
    });
  });
  await page.reload();
  await open(page, "PUR-001");
  await expect(page.locator("#review-detail-title")).toContainText(
    "<img src=x",
  );
  await expect(page.locator("#review-dialog img")).toHaveCount(0);
  await page.unroute("**/review-data.js");
  await page.route("**/review-data.js", async (route) => {
    const response = await route.fetch();
    await route.fulfill({
      response,
      body:
        (await response.text()) +
        '\nwindow.CONNECTABLE_REVIEW_DATA.records[0].source.source_url = "file:///Users/private/data";',
    });
  });
  await page.reload();
  await expect(page.locator("#review-data-error")).toBeVisible();
});

test("no overflow, requests remain local GET, headers and no root exposure", async ({
  page,
}) => {
  const errors = [],
    requests = [];
  page.on("pageerror", (e) => errors.push(e.message));
  page.on("request", (r) =>
    requests.push({ url: r.url(), method: r.method() }),
  );
  const response = await page.reload();
  expect(response.headers()["content-security-policy"]).toContain(
    "connect-src 'none'",
  );
  await open(page, "PUR-013");
  const width = await page.evaluate(() => ({
    viewport: innerWidth,
    page: document.documentElement.scrollWidth,
    detail: document.querySelector("#review-dialog").scrollWidth,
    dialog: document.querySelector("#review-dialog").clientWidth,
  }));
  expect(width.page).toBeLessThanOrEqual(width.viewport);
  expect(width.detail).toBeLessThanOrEqual(width.dialog);
  expect(errors).toEqual([]);
  expect(
    requests.every(
      (r) => r.url.startsWith("http://127.0.0.1:8874/") && r.method === "GET",
    ),
  ).toBe(true);
  expect(
    (
      await page.request.get(
        "/data/research/review/public_usage_mapped_2026-10-08.jsonl",
      )
    ).status(),
  ).toBe(404);
});

test("WCAG page and populated detail contrast/keyboard semantics", async ({
  page,
}) => {
  const scan = async () =>
    new AxeBuilder({ page })
      .withTags(["wcag2a", "wcag2aa", "wcag21aa"])
      .analyze();
  expect(
    (await scan()).violations.map((v) => ({
      id: v.id,
      nodes: v.nodes.map((n) => n.target),
    })),
  ).toEqual([]);
  await open(page, "PUR-001");
  expect(
    (await scan()).violations.map((v) => ({
      id: v.id,
      nodes: v.nodes.map((n) => n.target),
    })),
  ).toEqual([]);
});

test("AI semantic corrections preserve follow-up scope and UNKNOWN gates", async ({
  page,
}) => {
  await open(page, "PUR-003");
  const dialog = page.locator("#review-dialog");
  await expect(dialog.locator("[data-semantic-review]")).toContainText(
    "AI 의미 검수",
  );
  await expect(dialog).toContainText("후속 댓글 2022-08-29 09:49");
  await expect(dialog).toContainText("최종 UHD 점등·Hz 확인은 없음");
  await expect(dialog).toContainText("공개 UNKNOWN");
  await expect(dialog).toContainText("0/30");
  await page.locator("#review-close").click();
  await page.locator('[data-review-id="PUR-008"]').click();
  const obs = dialog
    .locator(".review-observation")
    .filter({ hasText: "재구매한 UGREEN 7-in-1" });
  await expect(obs).toContainText("정상 보고");
  await expect(obs.locator('[data-function="sleep_wake"]')).toContainText(
    "UNKNOWN",
  );
  await expect(obs.locator('[data-function="signal_mode"]')).toContainText(
    "UNKNOWN",
  );
  await page.locator("#review-close").click();
  await page.locator('[data-review-id="PUR-015"]').click();
  await expect(dialog).toContainText("추가 작성일 UNKNOWN");
});
