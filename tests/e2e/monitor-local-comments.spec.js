const { test, expect } = require('@playwright/test');
const KEY = 'connectable-v3-comment-drafts';
async function open(page, model = 'PA279CRV') {
  await page.locator('#monitor-search').fill(model);
  await page.locator('.product-card [data-action="detail"]').first().click();
}
const box = page => page.locator('#local-comments');
const input = page => box(page).getByLabel('댓글 초안 (최대 300자)');
const save = page => box(page).getByRole('button', { name: '이 브라우저에 초안 저장' });
test('local draft persists per product, renders as text, and deletion preserves other products', async ({page}) => {
  await page.goto('/monitor-v3.html');
  await open(page);
  await expect(box(page)).toContainText('공개되지 않으며');
  await expect(box(page).locator('.local-comment-saved')).toHaveText('저장된 초안이 없습니다.');
  await input(page).fill('<img src=x onerror=alert(1)> 읽기 쉬운 정보');
  await save(page).click();
  await expect(box(page).getByRole('status')).toContainText('저장했습니다');
  await expect(box(page).locator('.local-comment-saved img')).toHaveCount(0);
  await page.keyboard.press('Escape');
  await open(page, 'M28U');
  await expect(input(page)).toHaveValue('');
  await input(page).fill('두 번째 제품 초안');
  await save(page).click();
  await page.reload();
  await open(page);
  await expect(input(page)).toHaveValue('<img src=x onerror=alert(1)> 읽기 쉬운 정보');
  await box(page).getByRole('button', {name: '이 제품 초안 삭제'}).click();
  await expect(input(page)).toHaveValue('');
  await page.keyboard.press('Escape');
  await open(page, 'M28U');
  await expect(input(page)).toHaveValue('두 번째 제품 초안');
});
test('empty and oversized drafts are rejected and unicode limit is explicit', async ({page}) => {
  await page.goto('/monitor-v3.html');
  await open(page);
  await input(page).fill('  ');
  await save(page).click();
  await expect(box(page).getByRole('status')).toContainText('저장되지 않았습니다');
  await input(page).fill('😀'.repeat(301));
  await save(page).click();
  expect(await page.evaluate(key => localStorage.getItem(key), KEY)).toBeNull();
  await expect(input(page)).toHaveAttribute('aria-invalid', 'true');
  await input(page).fill('😀'.repeat(300));
  await save(page).click();
  await expect(box(page).getByRole('status')).toContainText('저장했습니다');
});
test('malformed storage is preserved and writes are disabled', async ({page}) => {
  await page.goto('/monitor-v3.html');
  for (const raw of ['broken json', JSON.stringify({version:1,drafts:[{productId:'monitor:a',text:'ok'},{productId:'monitor:a',text:'duplicate'}]}), JSON.stringify({version:1,drafts:[{productId:'monitor:a',text:123}]})]) {
    await page.evaluate(([key,raw]) => localStorage.setItem(key,raw), [KEY,raw]);
    await open(page);
    await expect(save(page)).toBeDisabled();
    await expect(box(page).getByRole('status')).toContainText('덮어쓰지 않습니다');
    expect(await page.evaluate(key => localStorage.getItem(key), KEY)).toBe(raw);
    await page.keyboard.press('Escape');
  }
});
test('blocked storage never claims save or deletion success', async ({page}) => {
  await page.goto('/monitor-v3.html');
  await open(page);
  await input(page).fill('저장할 초안');
  await save(page).click();
  await page.evaluate(() => {
    Storage.prototype.setItem = () => { throw new Error('Quota exceeded'); };
    Storage.prototype.removeItem = () => { throw new Error('Storage blocked'); };
  });
  await input(page).fill('저장 실패할 변경');
  await save(page).click();
  await expect(box(page).getByRole('status')).toContainText('저장하지 못했습니다');
  await expect(box(page).locator('.local-comment-saved')).toContainText('저장할 초안');
  await expect(input(page)).toHaveValue('저장 실패할 변경');
  await box(page).getByRole('button', {name:'이 제품 초안 삭제'}).click();
  await expect(box(page).getByRole('status')).toContainText('삭제하지 못했습니다');
  await expect(box(page).locator('.local-comment-saved')).toContainText('저장할 초안');
});
test('draft capacity rejects a new product without discarding existing drafts', async ({page}) => {
  await page.goto('/monitor-v3.html');
  await page.evaluate(key => localStorage.setItem(key, JSON.stringify({version:1,drafts:Array.from({length:30},(_,i)=>({productId:`monitor:example-${i}`,text:'local'}))})),KEY);
  await open(page);
  await input(page).fill('초과 저장');
  await save(page).click();
  await expect(box(page).getByRole('status')).toContainText('최대 30개');
  expect(await page.evaluate(key => JSON.parse(localStorage.getItem(key)).drafts.length,KEY)).toBe(30);
});
test('unavailable storage at mount disables saving without publishing or network calls', async ({page}) => {
  await page.goto('/monitor-v3.html');
  await page.evaluate(() => { Storage.prototype.getItem = () => { throw new Error('Storage denied'); }; });
  const requests = [];
  page.on('request', request => requests.push(request.url()));
  await open(page);
  await expect(save(page)).toBeDisabled();
  await expect(box(page).getByRole('status')).toContainText('저장소를 읽을 수 없거나');
  expect(requests).toEqual([]);
});
