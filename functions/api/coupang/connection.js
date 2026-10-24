import {signSearch,SEARCH_PATH} from '../../_lib/coupang-products.mjs';

// Short-lived diagnostics only; no products, API errors, keys or account details in output.
let lastAttempt=0;
export async function handleConnection(request,env,{fetcher=fetch,now=Date.now()}={}){
 const headers={'Content-Type':'application/json; charset=utf-8','Cache-Control':'private, no-store, max-age=0','X-Content-Type-Options':'nosniff'};
 const reply=(status,code,details={})=>new Response(JSON.stringify({code,...details}),{status,headers});
 if(request.method!=='POST')return reply(405,'METHOD_NOT_ALLOWED');
 const url=new URL(request.url);
 if(url.search || request.headers.get('Origin')!==url.origin || request.headers.get('Content-Length') && request.headers.get('Content-Length')!=='0')return reply(403,'INVALID_TEST_REQUEST');
 const until=Date.parse(env.COUPANG_CONNECTION_TEST_UNTIL || '');
 if(!Number.isFinite(until)||until<=now||until-now>600000)return reply(404,'CONNECTION_TEST_DISABLED');
 if(!env.COUPANG_PARTNERS_ACCESS_KEY || !env.COUPANG_PARTNERS_SECRET_KEY)return reply(503,'KEYS_NOT_CONFIGURED');
 if(lastAttempt && now-lastAttempt<60000 && now>=lastAttempt)return reply(429,'TEST_COOLDOWN');
 lastAttempt=now;
 let stage='SIGNING';
 try{
  const query=new URLSearchParams({keyword:'MSI MD271UL',limit:'1'}).toString();
  const auth=await signSearch(env.COUPANG_PARTNERS_ACCESS_KEY,env.COUPANG_PARTNERS_SECRET_KEY,query,new Date(now));
  stage='REQUEST';
  const response=await fetcher('https://api-gateway.coupang.com'+SEARCH_PATH+'?'+query,{method:'GET',headers:{Authorization:auth,Accept:'application/json','Cache-Control':'no-store'},redirect:'error',signal:AbortSignal.timeout(10000)});
  if(!response.ok){await response.body?.cancel();return reply(424,'API_AUTH_NOT_VERIFIED',{upstreamStatus:response.status});}
  stage='RESPONSE';
  const reader=response.body.getReader();const bytes=[];let size=0;
  while(true){const {done,value}=await reader.read();if(done)break;size+=value.length;if(size>262144){await reader.cancel();return reply(502,'INVALID_API_RESPONSE');}bytes.push(value);}
  const raw=new Uint8Array(size);let i=0;for(const b of bytes){raw.set(b,i);i+=b.length;}
  const data=JSON.parse(new TextDecoder().decode(raw));
  return data.rCode==='0'?reply(200,'API_AUTHENTICATED'):reply(424,'API_AUTH_NOT_VERIFIED',{stage:'API_RESULT'});
 }catch(error){
  const message=String(error?.message||'').toLowerCase();
  const reason=message.includes('timeout')?'TIMEOUT':message.includes('cache')?'CACHE_OPTION':message.includes('redirect')?'REDIRECT':message.includes('abortsignal')?'ABORT_SIGNAL':message.includes('fetch')?'FETCH':message.includes('header')?'HEADER':'OTHER';
  return reply(424,'API_AUTH_NOT_VERIFIED',{stage,reason});
 }
}
export const onRequest=({request,env})=>handleConnection(request,env);
