import {models} from '../../_lib/coupang-models.mjs';
import {reviewedMatches} from '../../_lib/coupang-matches.mjs';
import {queryProduct} from '../../_lib/coupang-products.mjs';

// No API data cache, persistence or logging. Limiter stores counters only.
let windowStart=0, requests=0;
export async function handleProduct(request,env,{fetcher=fetch,now=Date.now(),matches=reviewedMatches}={}){
  const headers={'Content-Type':'application/json; charset=utf-8','Cache-Control':'private, no-store, max-age=0','X-Content-Type-Options':'nosniff','Referrer-Policy':'no-referrer'};
  const reply=(status,body)=>new Response(JSON.stringify(body),{status,headers});
  if(request.method!=='GET')return reply(405,{code:'METHOD_NOT_ALLOWED'});
  const url=new URL(request.url);
  if(url.searchParams.getAll('model').length!==1 || [...url.searchParams.keys()].some(k=>k!=='model'))return reply(400,{code:'INVALID_QUERY'});
  const id=url.searchParams.get('model'),model=Object.hasOwn(models,id)?models[id]:null;
  if(!model)return reply(404,{code:'UNKNOWN_MODEL'});
  if(env.COUPANG_PRODUCTS_ENABLED!=='true'||env.COUPANG_MEDIA_CONFIRMED!=='true'||env.COUPANG_IMAGE_USE_CONFIRMED!=='true')return reply(503,{code:'INTEGRATION_NOT_ENABLED'});
  if(!Object.hasOwn(matches,id))return reply(404,{code:'MATCH_REVIEW_REQUIRED'});
  if(now-windowStart>=60000 || now<windowStart){windowStart=now;requests=0;}
  if(++requests>30)return reply(429,{code:'LOCAL_RATE_LIMITED'});
  const result=await queryProduct({model,match:matches[id],env,fetcher,now:new Date(now)});
  return result.product?reply(200,{model:id,product:result.product}):reply(result.status,{code:result.code});
}
export const onRequest = ({request,env})=>handleProduct(request,env);
