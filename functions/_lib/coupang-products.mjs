const API_ORIGIN = 'https://api-gateway.coupang.com';
export const SEARCH_PATH = '/v2/providers/affiliate_open_api/apis/openapi/v1/products/search';

export async function signSearch(access, secret, query, date=new Date()) {
  if(typeof access!=='string'||!access||/[\s,\r\n]/.test(access)||typeof secret!=='string'||!secret) throw new Error('INVALID_CREDENTIALS');
  const stamp=date.toISOString().slice(2,19).replace(/[-:]/g,'')+'Z';
  const key=await crypto.subtle.importKey('raw',new TextEncoder().encode(secret),{name:'HMAC',hash:'SHA-256'},false,['sign']);
  const sig=await crypto.subtle.sign('HMAC',key,new TextEncoder().encode(stamp+'GET'+SEARCH_PATH+query));
  const hex=[...new Uint8Array(sig)].map(b=>b.toString(16).padStart(2,'0')).join('');
  return `CEA algorithm=HmacSHA256, access-key=${access}, signed-date=${stamp}, signature=${hex}`;
}
function safeURL(value,kind){
  if(typeof value!=='string'||/[\s\\\x00-\x1f\x7f]/.test(value))return false;
  try {const u=new URL(value);return u.protocol==='https:'&&!u.username&&!u.password&&!u.port&&
    (kind==='image'?u.hostname==='ads-partners.coupang.com':['link.coupang.com','coupa.ng'].includes(u.hostname));} catch{return false;}
}
export function validateProduct(p,match) {
  if(!p || String(p.productId)!==match.productId || typeof p.productName!=='string' || !p.productName || p.productName.length>500)return null;
  if(!safeURL(p.productImage,'image')||!safeURL(p.productUrl,'link'))return null;
  const target=new URL(p.productUrl);
  if(target.searchParams.getAll('itemId').length!==1 || target.searchParams.getAll('vendorItemId').length!==1 || target.searchParams.get('itemId')!==match.itemId || target.searchParams.get('vendorItemId')!==match.vendorItemId)return null;
  // Matching is a human-reviewed ID decision, never the first search result or fuzzy model text.
  const normalized=p.productName.toUpperCase().replace(/[\s-]/g,'');
  if(!normalized.includes(match.requiredModel.toUpperCase().replace(/[\s-]/g,'')))return null;
  if((match.excludedTerms||[]).some(t=>normalized.includes(t.toUpperCase().replace(/[\s-]/g,''))))return null;
  return {productId:p.productId,productName:p.productName,productImage:p.productImage,productUrl:p.productUrl};
}
export async function queryProduct({model,match,env,fetcher=fetch,now=new Date()}) {
  if(!match || match.review_status!=='HUMAN_REVIEWED' || match.model_scope!=='EXACT_ITEM_VARIANT' || !/^\d{1,20}$/.test(match.productId)||!/^\d{1,20}$/.test(match.itemId)||!/^\d{1,20}$/.test(match.vendorItemId)||typeof match.requiredModel!=='string'||!match.requiredModel || !Array.isArray(match.excludedTerms) || match.excludedTerms.some(t=>typeof t!=='string'||!t))return {status:404,code:'MATCH_REVIEW_REQUIRED'};
  if(!env.COUPANG_PARTNERS_ACCESS_KEY || !env.COUPANG_PARTNERS_SECRET_KEY)return {status:503,code:'KEYS_NOT_CONFIGURED'};
  const params=new URLSearchParams({keyword:model.keyword,limit:'10',imageSize:'512x512'});
  const query=params.toString();
  try{
    const authorization=await signSearch(env.COUPANG_PARTNERS_ACCESS_KEY,env.COUPANG_PARTNERS_SECRET_KEY,query,now);
    const response=await fetcher(API_ORIGIN+SEARCH_PATH+'?'+query,{method:'GET',headers:{Authorization:authorization,Accept:'application/json','Cache-Control':'no-store'},redirect:'error',signal:AbortSignal.timeout(10000)});
    if(!response.ok)return {status:response.status===429?429:502,code:response.status===429?'UPSTREAM_RATE_LIMITED':'UPSTREAM_UNAVAILABLE'};
    const max=256*1024;const chunks=[];let length=0;const reader=response.body.getReader();
    while(true){const {done,value}=await reader.read();if(done)break;length+=value.byteLength;if(length>max){await reader.cancel();return {status:502,code:'INVALID_UPSTREAM_RESPONSE'};}chunks.push(value);}
    const bytes=new Uint8Array(length);let offset=0;for(const chunk of chunks){bytes.set(chunk,offset);offset+=chunk.length;}
    const raw=JSON.parse(new TextDecoder().decode(bytes));
    if(raw.rCode!=='0'||!Array.isArray(raw.data?.productData))return {status:502,code:'INVALID_UPSTREAM_RESPONSE'};
    const rows=raw.data.productData.filter(p=>String(p?.productId)===match.productId);
    if(rows.length!==1)return {status:404,code:'APPROVED_ITEM_UNAVAILABLE'};
    const product=validateProduct(rows[0],match);
    return product?{status:200,product}:{status:404,code:'ITEM_RECHECK_REQUIRED'};
  }catch{return {status:502,code:'UPSTREAM_UNAVAILABLE'};}
}
