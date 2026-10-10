const { test, expect } = require("@playwright/test");
const AxeBuilder = require("@axe-core/playwright").default;
const dataset = require("../../data/site/monitor-v3.json");

const cards = (page) => page.locator("#product-grid .product-card");
const modelCard = (page, model) => cards(page).filter({ hasText: model });
const viewportFits = async (page) => {
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
  ).toBe(true);
};
const openFilters = async (page) => {
  if (!(await page.locator("#filter-resolution").isVisible()))
    await page.locator("#filters > summary").click();
};
const axeCheck = async (page) => {
  const results = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa", "wcag21aa"])
    .analyze();
  expect(
    results.violations.map(({ id, nodes }) => ({
      id,
      targets: nodes.map((n) => n.target),
    })),
  ).toEqual([]);
};

test("static product document exposes complete sourced facts without premature indexing or offers", async ({
  page,
}) => {
  await page.goto("/monitors/asus-pa279crv/index.html");
  const product = dataset.products.find(
    (p) => p.id === "monitor:asus-pa279crv",
  );
  await expect(page.getByRole("heading", { level: 1 })).toHaveText(
    "ASUS PA279CRV",
  );
  await expect(page.locator("table tbody tr")).toHaveCount(
    product.facts.length,
  );
  await expect(page.locator("aside")).toContainText(
    "한국 판매 SKU 동일성은 미확인",
  );
  await expect(page.locator('meta[name="robots"]')).toHaveAttribute(
    "content",
    /noindex/,
  );
  await expect(
    page.locator('link[rel="canonical"], script[type="application/ld+json"]'),
  ).toHaveCount(0);
  for (const link of await page.locator('table a[href^="https:"]').all())
    expect(product.source_refs.map((s) => s.url)).toContain(
      await link.getAttribute("href"),
    );
  await viewportFits(page);
  await axeCheck(page);
  await page.getByRole("link", { name: "← 모니터 목록", exact: true }).click();
  await expect(page).toHaveURL(/monitor-v3\.html$/);
  await expect(cards(page)).toHaveCount(30);
});

test("v3 shows the 30 research models locally without invented prices or public approval", async ({
  page,
}) => {
  const errors = [],
    requests = [];
  page.on("pageerror", (e) => errors.push(e.message));
  page.on("request", (r) => requests.push(r.url()));
  const response = await page.goto("/monitor-v3.html");
  expect(response.headers()["content-security-policy"]).toContain(
    "connect-src 'none'",
  );
  await expect(cards(page)).toHaveCount(30);
  await expect(page.locator('meta[name="robots"]')).toHaveAttribute(
    "content",
    /noindex/,
  );
  await expect(
    page.locator('iframe, a[href*="coupang"], a[href*="aliexpress"]'),
  ).toHaveCount(0);
  expect(requests.every((url) => new URL(url).hostname === "127.0.0.1")).toBe(
    true,
  );
  expect(errors).toEqual([]);
  await viewportFits(page);
});

test("model search is reversible and empty results never become substitute recommendations", async ({
  page,
}) => {
  await page.goto("/monitor-v3.html");
  await page.locator("#monitor-search").fill("PA279CRV");
  await expect(cards(page)).toHaveCount(1);
  await expect(cards(page)).toContainText("PA279CRV");
  await page.locator("#monitor-search").fill("없는모델-000000");
  await expect(cards(page)).toHaveCount(0);
  await expect(page.locator("#result-count")).toContainText("0");
  await page.locator("#monitor-search").fill("");
  await expect(cards(page)).toHaveCount(30);
});

test("USB-C video filter distinguishes explicit support, absence and unknown connectors", async ({
  page,
}) => {
  await page.goto("/monitor-v3.html");
  await openFilters(page);
  await page.locator("#include-unknown").uncheck();
  await page.locator("#filter-usbc").selectOption("yes");
  await expect(modelCard(page, "PA279CRV")).toHaveCount(1);
  await expect(modelCard(page, "M28U")).toHaveCount(0);
  await expect(modelCard(page, "S32CG554EU")).toHaveCount(0);
  await page.locator("#include-unknown").check();
  await expect(modelCard(page, "M28U")).toHaveCount(1);
  await expect(modelCard(page, "S32CG554EU")).toHaveCount(0);
});

test("input-specific refresh is not promoted into an unconditional filter maximum", async ({
  page,
}) => {
  await page.goto("/monitor-v3.html");
  await openFilters(page);
  await page.locator("#include-unknown").uncheck();
  await page.locator("#filter-refresh").selectOption("240");
  await expect(modelCard(page, "XG27AQDMG")).toHaveCount(0);
  await expect(modelCard(page, "PA279CRV")).toHaveCount(0);
  await page.locator("#include-unknown").check();
  await expect(modelCard(page, "XG27AQDMG")).toHaveCount(1);
  await expect(modelCard(page, "PA279CRV")).toHaveCount(0);
});

test("detail retains region, incomplete review, fact conditions and official source links", async ({
  page,
}) => {
  await page.goto("/monitor-v3.html");
  const card = modelCard(page, "PA279CRV");
  const trigger = card.locator('[data-action="detail"]');
  await trigger.click();
  const dialog = page.locator("#detail-dialog");
  await expect(dialog).toBeVisible();
  await expect(dialog).toContainText("US");
  await expect(dialog).toContainText(/검토|미확인/);
  const links = dialog.locator('a[href^="https:"]');
  expect(await links.count()).toBeGreaterThan(0);
  for (const link of await links.all()) {
    await expect(link).toHaveAttribute("rel", /noopener/);
    expect(new URL(await link.getAttribute("href")).hostname).toMatch(
      /(^|\.)asus\.com$/,
    );
  }
  await axeCheck(page);
  await viewportFits(page);
  await page.keyboard.press("Escape");
  await expect(dialog).toBeHidden();
  await expect(trigger).toBeFocused();
});

test("comparison requires two, supports three, preserves unknown and differences are reversible", async ({
  page,
}) => {
  await page.goto("/monitor-v3.html");
  await modelCard(page, "PA279CRV").locator('[data-action="select"]').click();
  await expect(page.locator("#compare-open")).toBeDisabled();
  await modelCard(page, "M28U").locator('[data-action="select"]').click();
  await expect(page.locator("#compare-open")).toBeEnabled();
  await modelCard(page, "U2724D")
    .filter({ hasNotText: "U2724DE" })
    .locator('[data-action="select"]')
    .click();
  await modelCard(page, "VG27AQ").locator('[data-action="select"]').click();
  await expect(page.locator("#selection-count")).toContainText("3 / 3");
  await expect(page.locator("#interaction-status")).toContainText("최대 3개");
  await page.locator("#compare-open").click();
  const dialog = page.locator("#compare-dialog"),
    table = page.locator("#compare-table");
  await expect(dialog).toBeVisible();
  for (const name of ["PA279CRV", "M28U", "U2724D"])
    await expect(table).toContainText(name);
  await expect(table).toContainText(/미확인|UNKNOWN/);
  const fullRows = await table.locator("tbody tr:visible").count();
  await page.locator("#differences-only").check();
  expect(await table.locator("tbody tr:visible").count()).toBeLessThanOrEqual(
    fullRows,
  );
  await page.locator("#differences-only").uncheck();
  await expect(table.locator("tbody tr:visible")).toHaveCount(fullRows);
  await axeCheck(page);
  await viewportFits(page);
  await page.keyboard.press("Escape");
  await expect(page.locator("#compare-open")).toBeFocused();
});

test("helpful reaction is browser-local, reversible and not a fabricated global count", async ({
  page,
}) => {
  await page.goto("/monitor-v3.html");
  await modelCard(page, "PA279CRV").locator('[data-action="detail"]').click();
  await expect(page.locator(".local-feedback")).toContainText(
    "전체 사용자 집계가 아닙니다",
  );
  await page.locator("#helpful-toggle").click();
  await expect(page.locator("#helpful-toggle")).toHaveAttribute(
    "aria-pressed",
    "true",
  );
  await page.reload();
  await modelCard(page, "PA279CRV").locator('[data-action="detail"]').click();
  await expect(page.locator("#helpful-toggle")).toHaveAttribute(
    "aria-pressed",
    "true",
  );
  await page.keyboard.press("Escape");
  await modelCard(page, "M28U").locator('[data-action="detail"]').click();
  await expect(page.locator("#helpful-toggle")).toHaveAttribute(
    "aria-pressed",
    "false",
  );
  await page.keyboard.press("Escape");
  await modelCard(page, "PA279CRV").locator('[data-action="detail"]').click();
  await page.locator("#helpful-toggle").click();
  expect(
    await page.evaluate(() =>
      localStorage.getItem("connectable-v3-helpful:monitor:asus-pa279crv"),
    ),
  ).toBeNull();
});

test("hostile product text and executable source URLs are not injected into markup", async ({
  page,
}) => {
  const modified = structuredClone(dataset);
  modified.products[0].display_model = '<img src=x onerror="alert(1)">';
  modified.products[0].source_refs[0].url = "javascript:alert(1)";
  await page.route("**/monitor-v3-data.js", (route) =>
    route.fulfill({
      contentType: "application/javascript",
      body: "window.CONNECTABLE_MONITORS=" + JSON.stringify(modified) + ";",
    }),
  );
  await page.goto("/monitor-v3.html");
  await page.locator("#monitor-search").fill("<img");
  await expect(cards(page)).toHaveCount(1);
  await expect(cards(page).locator("img")).toHaveCount(0);
  await cards(page).locator('[data-action="detail"]').click();
  await expect(page.locator("#detail-title")).toHaveText(
    "ASUS " + modified.products[0].display_model,
  );
  await expect(
    page.locator('#detail-dialog a[href^="javascript:"], #detail-dialog img'),
  ).toHaveCount(0);
});

test("difference-only comparison retains equal numbers with different documented conditions", async ({
  page,
}) => {
  const modified = structuredClone(dataset);
  const first = modified.products.find((p) => p.display_model === "PA279CRV");
  const second = modified.products.find((p) => p.display_model === "M28U");
  for (const product of [first, second]) {
    const fact = product.facts.find((f) => f.property === "size");
    fact.value = 27;
    fact.unit = "inch";
    fact.scope = "PANEL";
    fact.qualifier = "MANUFACTURER_STATED";
    fact.location =
      product === first ? "Document condition A" : "Document condition B";
  }
  await page.route("**/monitor-v3-data.js", (route) =>
    route.fulfill({
      contentType: "application/javascript",
      body: "window.CONNECTABLE_MONITORS=" + JSON.stringify(modified) + ";",
    }),
  );
  await page.goto("/monitor-v3.html");
  for (const model of ["PA279CRV", "M28U"])
    await modelCard(page, model).locator('[data-action="select"]').click();
  await page.locator("#compare-open").click();
  await page.locator("#differences-only").check();
  const row = page
    .locator("#compare-table tbody tr")
    .filter({
      has: page.getByRole("rowheader", { name: "화면 크기", exact: true }),
    });
  await expect(row).toBeVisible();
  await expect(row).toContainText("Document condition A");
  await expect(row).toContainText("Document condition B");
});

test("invalid data envelope and changed publication status fail closed", async ({
  page,
}) => {
  const errors = [];
  page.on("pageerror", (e) => errors.push(e.message));
  for (const invalid of [
    null,
    { public_status: "UNKNOWN", products: {} },
    { ...dataset, public_status: "APPROVED" },
  ]) {
    await page.route("**/monitor-v3-data.js", (route) =>
      route.fulfill({
        contentType: "application/javascript",
        body: "window.CONNECTABLE_MONITORS=" + JSON.stringify(invalid) + ";",
      }),
    );
    await page.goto("/monitor-v3.html");
    await expect(page.locator("#result-count")).toHaveText("불러오기 실패");
    await expect(page.locator("#monitor-search")).toBeDisabled();
    await expect(cards(page)).toHaveCount(0);
    await page.unroute("**/monitor-v3-data.js");
  }
  expect(errors).toEqual([]);
});

test("blocked browser storage never reports a saved helpful reaction", async ({
  page,
}) => {
  await page.addInitScript(() => {
    Storage.prototype.setItem = () => {
      throw new DOMException("blocked", "SecurityError");
    };
  });
  await page.goto("/monitor-v3.html");
  await modelCard(page, "PA279CRV").locator('[data-action="detail"]').click();
  await page.locator("#helpful-toggle").click();
  await expect(page.locator("#helpful-toggle")).toHaveAttribute(
    "aria-pressed",
    "false",
  );
  await expect(page.locator("#reaction-status")).toContainText(
    "저장되지 않았어요",
  );
});

test("keyboard entry and responsive page pass automated accessibility checks", async ({
  page,
}) => {
  await page.goto("/monitor-v3.html");
  await page.keyboard.press("Tab");
  await expect(page.locator(".skip")).toBeFocused();
  await page.keyboard.press("Enter");
  await viewportFits(page);
  await axeCheck(page);
});
