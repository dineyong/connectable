import test from 'node:test';
import assert from 'node:assert/strict';
import {createHmac} from 'node:crypto';
import {signSearch,SEARCH_PATH,queryProduct,validateProduct} from '../../functions/_lib/coupang-products.mjs';
import {handleProduct} from '../../functions/api/coupang/product.js';
const env={COUPANG_PARTNERS_ACCESS_KEY:'test-access',COUPANG_PARTNERS_SECRET_KEY:'test-secret',COUPANG_PRODUCTS_ENABLED:'true',COUPANG_MEDIA_CONFIRMED:'true',COUPANG_IMAGE_USE_CONFIRMED:'true'};
const match={review_status:'HUMAN_REVIEWED',model_scope:'EXACT_ITEM_VARIANT',productId:'123',itemId:'456',vendorItemId:'789',requiredModel:'MD271UL',excludedTerms:['케이블','거치대','중고','리퍼']};
const product={productId:123,productName:'MSI MD271UL 모니터',productImage:'https://ads-partners.coupang.com/image1/test',productUrl:'https://link.coupang.com/re/AFFSDP?pageKey=123&itemId=456&vendorItemId=789',productPrice:9999,rank:1};
const fetchOK=async()=>Response.json({rCode:'0',data:{productData:[product]}});
const model={keyword:'MSI MD271UL'};
test('GET HMAC includes exact encoded query and UTC timestamp',async()=>{
 const query=new URLSearchParams({keyword:'MSI 모니터',limit:'10'}).toString();const sig=createHmac('sha256','test-secret').update('261024T010203ZGET'+SEARCH_PATH+query).digest('hex');
 assert.equal(await signSearch('test-access','test-secret',query,new Date('2026-10-24T01:02:03Z')),`CEA algorithm=HmacSHA256, access-key=test-access, signed-date=261024T010203Z, signature=${sig}`);
});
test('manual item/variant matching never picks the first search result',async()=>{
 const result=await queryProduct({model,match,env,fetcher:async(url,init)=>{assert.equal(new URL(url).origin,'https://api-gateway.coupang.com');assert.equal(init.redirect,'error');assert.equal(init.cache,undefined);assert.equal(init.headers['Cache-Control'],'no-store');return Response.json({rCode:'0',data:{productData:[{...product,productId:999},product]}});}});
 assert.equal(result.status,200);assert.deepEqual(Object.keys(result.product),['productId','productName','productImage','productUrl']);assert.equal(result.product.productImage,product.productImage);
});
test('missing review, missing key, option change and accessory are refused',async()=>{
 let calls=0;const fetcher=async()=>{calls++;return fetchOK();};
 assert.equal((await queryProduct({model,match:null,env,fetcher})).code,'MATCH_REVIEW_REQUIRED');
 assert.equal((await queryProduct({model,match,env:{},fetcher})).code,'KEYS_NOT_CONFIGURED');assert.equal(calls,0);
 for(const p of [{...product,productName:'MSI MD271UL 케이블'},{...product,productUrl:product.productUrl.replace('456','999')},{...product,productUrl:product.productUrl+'&itemId=456'},{...product,productName:'다른 모니터'}]) assert.equal(validateProduct(p,match),null);
});
test('unsafe image and link URLs are refused',()=>{
 for(const u of ['http://ads-partners.coupang.com/x','https://ads-partners.coupang.com.evil.test/x','https://user@ads-partners.coupang.com/x','https://ads-partners.coupang.com:88/x','data:image/png,test'])assert.equal(validateProduct({...product,productImage:u},match),null);
 for(const u of ['javascript:alert(1)','https://www.coupang.com/vp/products/123','https://link.coupang.com.evil.test/x','https://user@link.coupang.com/x'])assert.equal(validateProduct({...product,productUrl:u},match),null);
});
test('upstream failures return sanitized errors without credentials or response bodies',async()=>{
 for(const fetcher of [async()=>{throw Error('test-secret');},async()=>new Response('test-secret',{status:403}),async()=>new Response('bad json test-secret'),async()=>Response.json({rCode:'0',data:{productData:[product,product]}}),async()=>new Response('x'.repeat(270000))]){
  const result=await queryProduct({model,match,env,fetcher});assert.notEqual(result.status,200);assert.ok(!JSON.stringify(result).includes('test-secret'));
 }
 assert.equal((await queryProduct({model,match,env,fetcher:async()=>new Response('',{status:429})})).status,429);
});
test('public route is disabled by default and rejects arbitrary searches',async()=>{
 const req=new Request('https://monipick.com/api/coupang/product?model=monitor%3Amsi-modern-md271ul');
 assert.equal((await handleProduct(req,{})).status,503);
 assert.equal((await handleProduct(new Request(req.url+'&keyword=unrestricted'),env)).status,400);
 assert.equal((await handleProduct(new Request(req.url.replace('monitor%3Amsi-modern-md271ul','__proto__')),env)).status,404);
 assert.equal((await handleProduct(new Request(req.url,{method:'POST'}),env)).status,405);
 assert.equal((await handleProduct(req,env)).status,404);
});
test('enabled route requires exact reviewed binding, returns no-store and bounds requests',async()=>{
 const id='monitor:msi-modern-md271ul';const req=new Request('https://monipick.com/api/coupang/product?model='+encodeURIComponent(id));
 const options={fetcher:fetchOK,now:Date.parse('2026-10-24T05:00:00Z'),matches:{[id]:match}};
 const response=await handleProduct(req,env,options);assert.equal(response.status,200);assert.match(response.headers.get('Cache-Control'),/no-store/);const body=await response.json();assert.equal(body.model,id);assert.ok(!JSON.stringify(body).includes('test-secret'));
 for(let i=0;i<29;i++)assert.equal((await handleProduct(req,env,options)).status,200);
 assert.equal((await handleProduct(req,env,options)).status,429);
});

test('connection test is off without a short deadline, rejects foreign origin and never returns product data',async()=>{
 const {handleConnection}=await import('../../functions/api/coupang/connection.js');
 const now=Date.parse('2026-10-24T12:00:00Z');
 const req=new Request('https://monipick.com/api/coupang/connection',{method:'POST',headers:{Origin:'https://monipick.com'}});
 assert.equal((await handleConnection(req,env,{now})).status,404);
 const active={...env,COUPANG_CONNECTION_TEST_UNTIL:new Date(now+300000).toISOString()};
 const foreign=new Request(req.url,{method:'POST',headers:{Origin:'https://evil.test'}});
 assert.equal((await handleConnection(foreign,active,{now})).status,403);
 assert.equal((await handleConnection(req,{...active,COUPANG_CONNECTION_TEST_UNTIL:new Date(now+3600000).toISOString()},{now})).status,404);
 const response=await handleConnection(req,active,{now,fetcher:fetchOK});
 assert.equal(response.status,200);assert.deepEqual(await response.json(),{code:'API_AUTHENTICATED'});
 assert.equal((await handleConnection(req,active,{now,fetcher:fetchOK})).status,429);
 assert.equal((await handleConnection(req,active,{now:now+360000,fetcher:fetchOK})).status,404);
});
