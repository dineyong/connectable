const { test, expect } = require("@playwright/test");
const AxeBuilder = require("@axe-core/playwright").default;
const content = require("../../data/site/content-v2.json");
const readable = (r) =>
  r.observations?.[0]?.summary ||
  r.connection_summary?.[0] ||
  r.title.replace(/^(?:PUR|UQ)-\d+\s*[·:–-]\s*/, "");
const counts = (rows) =>
  `${new Set(rows.map((r) => r.source_refs[0]?.url || r.id)).size}개 원문 그룹 · 연구 기록 ${rows.length}개`;
test("source-derived content, CSP, local requests and responsive layout", async ({
  page,
}) => {
  const errors = [],
    requests = [];
  page.on("pageerror", (e) => errors.push(e.message));
  page.on("request", (r) => requests.push(r));
  const response = await page.goto("/");
  expect(response.headers()["content-security-policy"]).toContain(
    "connect-src 'none'",
  );
  await expect(page.locator("#monitor-list article")).toHaveCount(
    content.monitors.length,
  );
  await expect(page.locator("#review-count")).toHaveText(
    counts(content.reviews),
  );
  await expect(page.locator("#guide-list article")).toHaveCount(
    content.guides.length,
  );
  const m = await page.evaluate(() => ({
    w: innerWidth,
    s: document.documentElement.scrollWidth,
  }));
  expect(m.s).toBeLessThanOrEqual(m.w);
  expect(errors).toEqual([]);
  expect(
    requests.every(
      (r) => r.method() === "GET" && new URL(r.url()).hostname === "127.0.0.1",
    ),
  ).toBeTruthy();
  await expect(page.locator('a[href*="coupang"],iframe')).toHaveCount(0);
});
test("monitor details and guide relationships retain sources and unknown", async ({
  page,
}) => {
  await page.goto("/");
  const b = page.locator("#monitor-list button").first();
  await b.click();
  await expect(page.getByRole("dialog")).toContainText(
    content.monitors[0].title,
  );
  await expect(page.getByRole("dialog")).toContainText("UNKNOWN");
  await expect(page.getByRole("dialog")).toContainText(
    content.monitors[0].features[0].summary,
  );
  await expect(page.locator(".source-list a").first()).toHaveAttribute(
    "href",
    content.monitors[0].source_refs[0].url,
  );
  await page
    .getByRole("dialog")
    .getByRole("button", { name: content.guides[0].title + " →", exact: true })
    .click();
  await expect(page.locator("#detail-title")).toHaveText(
    content.guides[0].title,
  );
  await expect(page.getByRole("dialog")).toContainText(
    content.guides[0].body[0],
  );
  await page.keyboard.press("Escape");
  await expect(page.getByRole("dialog")).toBeHidden();
  await expect(b).toBeFocused();
});
test("model, interest, feature filters, search and pagination", async ({
  page,
}) => {
  await page.goto("/");
  await expect(page.locator("#review-list article")).toHaveCount(6);
  await page.getByRole("button", { name: "후기 더 보기", exact: true }).click();
  await expect(page.locator("#review-list article")).toHaveCount(12);
  await page
    .locator("#mac-filter")
    .selectOption(content.reviews[0].macbook_display_name);
  const n = content.reviews.filter(
    (r) => r.macbook_display_name === content.reviews[0].macbook_display_name,
  ).length;
  await expect(page.locator("#review-count")).toHaveText(
    counts(
      content.reviews.filter(
        (r) =>
          r.macbook_display_name === content.reviews[0].macbook_display_name,
      ),
    ),
  );
  await page.locator("#purpose-filter").selectOption("pd");
  const charged = content.reviews.filter(
    (r) =>
      r.macbook_display_name === content.reviews[0].macbook_display_name &&
      (r.functional_observations || []).some(
        (o) => o.pd?.recognized && o.pd.recognized !== "UNKNOWN",
      ),
  ).length;
  await expect(page.locator("#review-count")).toHaveText(
    `${charged}개 원문 그룹 · 연구 기록 ${charged}개`,
  );
  await page.getByRole("button", { name: "초기화", exact: true }).click();
  await expect(page.locator("#review-count")).toHaveText(
    counts(content.reviews),
  );
  await page.locator("#feature-filter").selectOption("POWER_TRANSFER");
  await expect(page.locator("#monitor-list article")).toHaveCount(
    content.monitors.filter((m) =>
      m.features.some((f) => f.property === "POWER_TRANSFER"),
    ).length,
  );
  await page.locator("#search").fill("없는후기000");
  await expect(page.locator("#review-count")).toHaveText(
    "0개 원문 그룹 · 연구 기록 0개",
  );
  await expect(page.locator("#review-list")).toContainText("검색 조건");
  await page.getByRole("button", { name: "초기화", exact: true }).click();
  await expect(page.locator("#monitor-list article")).toHaveCount(
    content.monitors.length,
  );
});
test("review deep link, observations and source safety", async ({ page }) => {
  await page.goto("/#reviews/PUR-001");
  await expect(page.getByRole("dialog")).toBeVisible();
  await expect(page.getByRole("dialog")).toContainText("사람 검토 대기");
  await expect(page.getByRole("dialog")).toContainText("3008×1692");
  if (!content.reviews.find((r) => r.id === "PUR-001").monitor_ids.length)
    await expect(page.getByRole("dialog")).toContainText(
      "공식 모델 연결 UNKNOWN",
    );
  for (const a of await page.locator(".source-list a").all()) {
    expect(await a.getAttribute("href")).toMatch(/^https:\/\//);
    await expect(a).toHaveAttribute("rel", "noopener noreferrer");
  }
  await page.keyboard.press("Escape");
  await expect(page.getByRole("dialog")).toBeHidden();
});
test("empty, corrupt and hostile data safely rendered", async ({ page }) => {
  await page.route("**/site-content-v2.js", (route) =>
    route.fulfill({
      contentType: "application/javascript",
      body: "window.CONNECTABLE_SITE_V2={monitors:[],reviews:[],guides:[]};",
    }),
  );
  await page.goto("/");
  await expect(page.locator("#monitor-list")).toContainText("준비");
  await expect(page.locator("#review-count")).toHaveText(
    "0개 원문 그룹 · 연구 기록 0개",
  );
  await page.unroute("**/site-content-v2.js");
  await page.route("**/site-content-v2.js", (route) =>
    route.fulfill({
      contentType: "application/javascript",
      body: "window.CONNECTABLE_SITE_V2={monitors:[null],reviews:[],guides:[]};",
    }),
  );
  await page.reload();
  await expect(page.locator("#monitor-list")).toContainText(
    "불러오지 못했습니다",
  );
  await page.unroute("**/site-content-v2.js");
  const x = structuredClone(content);
  x.monitors[0].title = "<img src=x onerror=alert(1)>";
  x.monitors[0].source_refs[0].url = "javascript:alert(1)";
  await page.route("**/site-content-v2.js", (route) =>
    route.fulfill({
      contentType: "application/javascript",
      body: "window.CONNECTABLE_SITE_V2=" + JSON.stringify(x) + ";",
    }),
  );
  await page.reload();
  await expect(page.locator("#monitor-list img")).toHaveCount(0);
  await page.locator("#monitor-list button").first().click();
  await expect(page.locator("#detail-title")).toHaveText(x.monitors[0].title);
  await expect(page.locator('.source-list a[href^="javascript:"]')).toHaveCount(
    0,
  );
});
test("keyboard skip and WCAG automated checks on page and detail", async ({
  page,
}) => {
  await page.goto("/");
  await page.keyboard.press("Tab");
  await expect(page.locator(".skip")).toBeFocused();
  const results = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa", "wcag21aa"])
    .analyze();
  expect(
    results.violations.map((v) => ({
      id: v.id,
      nodes: v.nodes.map((n) => n.target),
    })),
  ).toEqual([]);
  await page.locator("#review-list button").first().click();
  const detail = await new AxeBuilder({ page })
    .include("#detail")
    .withTags(["wcag2a", "wcag2aa", "wcag21aa"])
    .analyze();
  expect(
    detail.violations.map((v) => ({
      id: v.id,
      nodes: v.nodes.map((n) => n.target),
    })),
  ).toEqual([]);
});
test("preserved user mockup and internal review remain distinct", async ({
  page,
}) => {
  await page.goto("/legacy.html");
  await expect(
    page.getByRole("button", { name: "확인할 연결 조건 보기" }),
  ).toBeVisible();
  await page.goto("/review.html");
  await expect(page.locator("body")).toContainText("검토");
});

test("question corpus records retain configuration conclusions", async ({
  page,
}) => {
  const r = content.reviews.find(
    (r) => (r.configuration_conclusions || []).length,
  );
  await page.goto("/#reviews/" + r.id);
  await expect(page.getByRole("dialog")).toContainText(
    r.configuration_conclusions[0].summary,
  );
  await expect(page.getByRole("dialog")).toContainText(
    "해당 구성의 사용자 기록",
  );
});

test("browser back closes a detail and keeps filters", async ({ page }) => {
  await page.goto("/");
  await page.locator("#feature-filter").selectOption("POWER_TRANSFER");
  const b = page.locator("#monitor-list button").first();
  await b.click();
  await page.goBack();
  await expect(page.getByRole("dialog")).toBeHidden();
  await expect(page.locator("#feature-filter")).toHaveValue("POWER_TRANSFER");
  await expect(b).toBeFocused();
});

test("same original is one group with both research records accessible", async ({
  page,
}) => {
  await page.goto("/");
  await expect(page.locator("#review-count")).toHaveText(
    "37개 원문 그룹 · 연구 기록 38개",
  );
  while (await page.locator("#more-reviews").count())
    await page.locator("#more-reviews").click();
  await expect(page.locator("#review-list article")).toHaveCount(37);
  await expect(
    page.locator('#review-list button[data-id="UQ-0009"]'),
  ).toHaveCount(0);
  const card = page
    .locator("#review-list article")
    .filter({ has: page.locator('button[data-id="PUR-009"]') });
  await expect(card).toContainText("동일 원문 연구 기록 2개");
  await expect(card.locator("h3")).not.toContainText("PUR-009");
  await card.getByRole("button").click();
  await expect(page.getByRole("dialog")).toContainText(
    "별도 사용자 후기 2건이 아닙니다",
  );
  const uq = content.reviews.find((r) => r.id === "UQ-0009");
  await page.getByRole("dialog").locator('button[data-id="UQ-0009"]').click();
  await expect(page.locator("#detail-title")).toHaveText(readable(uq));
  await expect(page.getByRole("dialog")).toContainText(
    uq.observations[0].summary,
  );
  await page.getByRole("dialog").locator('button[data-id="PUR-009"]').click();
  await expect(page.locator("#detail-title")).toHaveText(
    readable(content.reviews.find((r) => r.id === "PUR-009")),
  );
  await page.keyboard.press("Escape");
  await page.locator("#search").fill("UQ-0009");
  await expect(page.locator("#review-list article")).toHaveCount(1);
  await page.locator('#review-list button[data-id="UQ-0009"]').click();
  await expect(
    page.getByRole("dialog").locator('button[data-id="PUR-009"]'),
  ).toBeVisible();
});

test("tracking parameters, fragments and trailing slash do not split an original", async ({
  page,
}) => {
  const x = structuredClone(content),
    a = x.reviews.find((r) => r.id === "PUR-009"),
    b = x.reviews.find((r) => r.id === "UQ-0009");
  const url = new URL(a.source_refs[0].url);
  url.pathname = url.pathname.replace(/\/$/, "") + "/";
  url.searchParams.set("utm_source", "test");
  url.hash = "section";
  b.source_refs[0].url = url.href;
  await page.route("**/site-content-v2.js", (route) =>
    route.fulfill({
      contentType: "application/javascript",
      body: "window.CONNECTABLE_SITE_V2=" + JSON.stringify(x) + ";",
    }),
  );
  await page.goto("/");
  await expect(page.locator("#review-count")).toHaveText(
    "37개 원문 그룹 · 연구 기록 38개",
  );
  await page.locator("#search").fill("UQ-0009");
  await page.locator("#review-list button").click();
  await expect(
    page.getByRole("dialog").locator('button[data-id="PUR-009"]'),
  ).toBeVisible();
});

test("two product comparison retains independent panel, port, power and unknown values", async ({
  page,
}) => {
  await page.goto("/");
  const controls = page.locator("[data-compare]");
  await controls.nth(0).check();
  await expect(page.locator("#compare-open")).toBeDisabled();
  await controls.nth(1).check();
  await expect(controls.nth(2)).toBeDisabled();
  await page.locator("#compare-open").click();
  await expect(page.locator("#detail-title")).toHaveText("두 모니터 비교");
  await expect(page.locator(".comparison")).toContainText(
    content.monitors[0].title,
  );
  await expect(page.locator(".comparison")).toContainText(
    content.monitors[1].title,
  );
  await expect(page.locator(".comparison")).toContainText(
    "UNKNOWN · 아직 확인되지 않음 (미지원 아님)",
  );
  const power = page.locator(".comparison tr").filter({
    has: page.getByRole("rowheader", {
      name: "공식 PD 공급 전력 상한·표기",
      exact: true,
    }),
  });
  for (const m of content.monitors.slice(0, 2))
    for (const f of m.features.filter((f) => f.property === "POWER_TRANSFER"))
      await expect(power).toContainText(f.summary);
  await page.keyboard.press("Escape");
  await expect(page.locator("#compare-open")).toBeFocused();
  await controls.nth(1).uncheck();
  await controls.nth(2).check();
  await page.locator("#compare-open").click();
  await expect(page.locator(".comparison")).toContainText(
    "DisplayPort에서 2560×1440 165Hz",
  );
  const width = await page.evaluate(() => ({
    w: innerWidth,
    s: document.documentElement.scrollWidth,
  }));
  expect(width.s).toBeLessThanOrEqual(width.w);
  const a11y = await new AxeBuilder({ page })
    .include("#detail")
    .withTags(["wcag2a", "wcag2aa", "wcag21aa"])
    .analyze();
  expect(a11y.violations.map((v) => v.id)).toEqual([]);
  await page.keyboard.press("Escape");
  await page.locator("#compare-clear").click();
  await expect(page.locator("#compare-bar")).toBeHidden();
});
test("official addon filters, readable titles, evidence IDs and guide contents", async ({
  page,
}) => {
  await page.goto("/");
  await expect(page.locator("#review-list h3").first()).toHaveText(
    readable(content.reviews[0]),
  );
  await expect(page.locator("#review-list h3").first()).not.toContainText(
    "PUR-001",
  );
  await page.locator("#addon-filter").selectOption("pd");
  await expect(page.locator("#monitor-list article")).toHaveCount(
    content.monitors.filter((m) =>
      m.features.some(
        (f) =>
          f.property === "POWER_TRANSFER" &&
          f.payload?.mode === "OFFER" &&
          typeof f.payload.watts === "number" &&
          f.payload.interface !== "UNKNOWN",
      ),
    ).length,
  );
  await page.getByRole("button", { name: "초기화", exact: true }).click();
  await page.locator("#review-list button").first().click();
  await page.locator(".record-evidence summary").click();
  await expect(page.locator(".record-evidence")).toContainText("PUR-001");
  await page.keyboard.press("Escape");
  await page.locator("#guide-list button").first().click();
  await expect(page.getByRole("dialog")).toContainText("짧은 요약");
  await expect(page.locator(".guide-toc button")).toHaveCount(
    content.guides[0].body.length,
  );
  await page.locator(".guide-toc button").last().click();
  await expect(
    page.locator("#guide-part-" + (content.guides[0].body.length - 1)),
  ).toBeFocused();
});

test("new exact models connect official features to their source records", async ({
  page,
}) => {
  await page.goto("/");
  const model = content.monitors.find((m) => m.id === "product:jooyon-v32ue");
  expect(model).toBeTruthy();
  await page
    .locator('#monitor-list button[data-id="' + model.id + '"]')
    .click();
  await expect(
    page.getByRole("dialog").locator('button[data-id="PUR-001"]'),
  ).toBeVisible();
  await expect(page.getByRole("dialog")).toContainText("표시 모델 수준");
  const headingOrder = await page
    .getByRole("dialog")
    .locator("h3")
    .allTextContents();
  expect(headingOrder.indexOf("제품 요약")).toBeLessThan(
    headingOrder.indexOf("공식 기능과 부가기능"),
  );
  expect(headingOrder.indexOf("동일 모델의 연결 기록")).toBeLessThan(
    headingOrder.indexOf("주의할 점과 결측"),
  );
  expect(headingOrder.indexOf("케이블과 설정을 확인하세요")).toBeLessThan(
    headingOrder.indexOf("출처와 확인일"),
  );
  await page.getByRole("dialog").locator('button[data-id="PUR-001"]').click();
  await expect(
    page.getByRole("dialog").locator('button[data-id="' + model.id + '"]'),
  ).toBeVisible();
  await page.keyboard.press("Escape");
  for (const feature of ["kvm", "speaker", "height"]) {
    await page.locator("#addon-filter").selectOption(feature);
    await expect(page.locator("#monitor-list article")).toHaveCount(1);
    await expect(page.locator("#monitor-list")).toContainText("27ULD950");
  }
});

test("public data retains resolvable official and user evidence references", async ({
  page,
}) => {
  await page.goto("/");
  const errors = await page.evaluate(() => {
    const d = window.CONNECTABLE_SITE_V2,
      errors = [];
    for (const m of d.monitors) {
      const facts = new Set(m.features.map((f) => f.fact_id));
      const sources = new Set(m.source_refs.map((s) => s.record_id));
      for (const c of Object.values(m.capabilities || {}))
        for (const id of c.feature_refs)
          if (!facts.has(id)) errors.push("fact:" + id);
      for (const f of m.features)
        for (const id of f.source_refs)
          if (!sources.has(id)) errors.push("source:" + id);
    }
    for (const r of d.reviews) {
      const evidence = new Set(r.evidence.map((e) => e.id));
      const configs = new Set(r.configurations.map((c) => c.id));
      for (const o of r.observations) {
        if (!configs.has(o.configuration_id))
          errors.push("configuration:" + o.configuration_id);
        for (const id of o.evidence_refs)
          if (!evidence.has(id)) errors.push("evidence:" + id);
      }
    }
    return errors;
  });
  expect(errors).toEqual([]);
});

test("official summary text reaches details and critical comparison cells unchanged", async ({
  page,
}) => {
  await page.goto("/");
  for (const m of content.monitors) {
    await page.locator(`#monitor-list button[data-id="${m.id}"]`).click();
    for (const f of m.features)
      await expect(page.locator("#detail-body")).toContainText(f.summary);
    await page.keyboard.press("Escape");
  }
  const choices = page.locator("[data-compare]");
  await choices.nth(0).check();
  await choices.nth(2).check();
  await page.locator("#compare-open").click();
  const row = (name) =>
    page
      .locator(".comparison tr")
      .filter({ has: page.getByRole("rowheader", { name, exact: true }) });
  await expect(
    row("공식 PD 공급 전력 상한·표기").locator("td").nth(0),
  ).toContainText("최대 90W 공급");
  await expect(
    row("공식 PD 공급 전력 상한·표기").locator("td").nth(0),
  ).toContainText("downstream은 최대 15W 충전");
  await expect(row("입력 포트별 해상도·Hz").locator("td").nth(1)).toContainText(
    "DisplayPort에서 2560×1440 165Hz",
  );
  await expect(row("입력 포트별 해상도·Hz").locator("td").nth(1)).toContainText(
    "HDMI에서 2560×1440 144Hz",
  );
  await expect(
    row("공식 PD 공급 전력 상한·표기").locator("td").nth(1),
  ).toContainText("UNKNOWN");
});
