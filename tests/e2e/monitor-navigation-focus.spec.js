const { test, expect } = require('@playwright/test');

test('empty-result reset restores keyboard focus to reusable search', async ({ page }) => {
  await page.goto('/monitor-v3.html');
  await page.locator('#monitor-search').fill('missing-navigation-model-zzz');
  await expect(page.locator('#empty-state')).toBeVisible();
  await page.locator('#empty-reset').focus();
  await page.keyboard.press('Enter');
  await expect(page.locator('#product-grid .product-card')).toHaveCount(30);
  await expect(page.locator('#monitor-search')).toHaveValue('');
  await expect(page.locator('#monitor-search')).toBeFocused();
  await page.keyboard.type('PA279CRV');
  await expect(page.locator('#product-grid .product-card')).toHaveCount(1);
});

test('comparison removal restores a visible focus target on desktop and mobile', async ({ page }) => {
  await page.goto('/monitor-v3.html');
  await page.locator('#product-grid [data-action="select"]').nth(0).click();
  await page.locator('#product-grid [data-action="select"]').nth(1).click();
  if (page.viewportSize().width <= 760) {
    await page.locator('#compare-clear').focus();
    await page.keyboard.press('Enter');
    await expect(page.locator('#compare-tray')).toBeHidden();
    await expect(page.locator('#compare-start')).toBeFocused();
    return;
  }
  const remainingId = await page.locator('#selected-products button').nth(1).getAttribute('data-id');
  await page.locator('#selected-products button').first().focus();
  await page.keyboard.press('Enter');
  await expect(page.locator(`#selected-products button[data-id="${remainingId}"]`)).toBeFocused();
  await expect(page.locator('#compare-open')).toBeDisabled();
  await page.keyboard.press('Enter');
  await expect(page.locator('#compare-tray')).toBeHidden();
  await expect(page.locator('#compare-start')).toBeFocused();
});
