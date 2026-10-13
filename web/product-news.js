(() => {
  'use strict';
  const data=window.CONNECTABLE_PRODUCT_NEWS;
  const output=document.getElementById('product-news-items');
  const status=document.getElementById('product-news-status');
  const filter=document.getElementById('product-news-filter');
  const registry={'benq-kr':['www.benq.com','/ko-kr/news/products/'],'apple-kr':['images.apple.com','/kr/newsroom/']};
  const labels={MONITOR_LAUNCH:'모니터 신제품',PHONE_PREORDER:'휴대폰 사전예약'};
  function render(){
    output.replaceChildren();
    if(!data || data.public_status!=='UNKNOWN' || !Array.isArray(data.items)) {status.textContent='신제품 소식을 불러오지 못했습니다.';filter.disabled=true;return;}
    for(const item of data.items){
      if(!item || typeof item!=='object' || typeof item.url!=='string')continue;
      let url;try {url=new URL(item.url);}catch {continue;}
      const source=registry[item.source_id];
      if(!source || url.protocol!=='https:' || url.hostname!==source[0] || !url.pathname.startsWith(source[1]) || url.username || url.password || url.port || url.search || url.hash || /[\s\\%\x00-\x1f\x7f]/.test(item.url) || item.url.split('/').some(part=>part==='.' || part==='..') || item.review_status!=='PENDING_PUBLICATION_REVIEW' || !labels[item.category])continue;
      if(filter.value!=='ALL' && item.category!==filter.value)continue;
      const card=document.createElement('article');card.className='announcement-card';
      const append=(tag,text,cls)=>{const el=document.createElement(tag);el.textContent=text;if(cls)el.className=cls;card.append(el);return el;};
      append('span',labels[item.category],'tag');append('h3',item.title);append('p',item.summary);
      if(item.preorder_on)append('p',`발표된 사전주문일 ${item.preorder_on} · 구매 가능일 ${item.available_on || '미확인'}`,'schedule');
      append('p',`${item.source_name} · ${item.region==='KR'?'국내 발표':'지역 미확인'} · 발표 ${item.published_on} · 본문 확인 ${item.checked_on}`,'meta');
      append('p','발표 기록 · 판매 상태 미확인','note');
      const a=append('a','공식 발표 읽기 ↗');a.href=url.href;a.target='_blank';a.rel='noopener noreferrer';output.append(card);
    }
    status.textContent=output.childElementCount?`${output.childElementCount}건 · 직접 확인한 발표 기록`:'이 분류에 확인된 발표가 없습니다.';
  }
  filter.addEventListener('change',render);render();
})();
