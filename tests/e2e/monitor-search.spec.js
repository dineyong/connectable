const {test,expect}=require('@playwright/test');
const data=require('../../data/site/monitor-v3.json');
test('model and spec search intersect exact known fields',async({page})=>{
 await page.goto('/monitor-v3.html');
 const cases=[['27인치 QHD',p=>p.filters.size===27&&p.filters.width===2560&&p.filters.height===1440],['4K IPS',p=>p.filters.width===3840&&p.filters.height===2160&&String(p.filters.panel).includes('IPS')],['144 Hz',p=>p.filters.refresh===144],['USB-C',p=>p.filters.usb_c_video===true],['PA279 CRV',p=>p.display_model==='PA279CRV']];
 for(const [query,fn] of cases){await page.locator('#monitor-search').fill(query);expect(await page.locator('#product-grid .product-card').evaluateAll(rows=>rows.map(r=>r.dataset.productId).sort())).toEqual(data.products.filter(fn).map(p=>p.id).sort());}
 await page.locator('#monitor-search').fill('999Hz');await expect(page.locator('#product-grid .product-card')).toHaveCount(0);
});
