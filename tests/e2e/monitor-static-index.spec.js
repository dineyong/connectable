const {test,expect}=require('@playwright/test');
test.use({javaScriptEnabled:false});
test('all product documents remain reachable without JavaScript', async ({page})=>{
 await page.goto('/monitor-v3.html');
 await page.getByRole('link',{name:'전체 모니터 정적 제품 정보 보기'}).click();
 await expect(page.locator('.static-product-groups li a')).toHaveCount(30);
 await page.getByRole('link',{name:'PA279CRV',exact:true}).click();
 await expect(page.getByRole('heading',{name:'ASUS PA279CRV',exact:true})).toBeVisible();
 await expect(page.locator('tbody tr')).not.toHaveCount(0);
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
});
