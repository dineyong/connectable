(() => {
  "use strict";
  const data = window.CONNECTABLE_TECH_NEWS;
  const status = document.getElementById("news-status");
  if (!data || !Array.isArray(data.items)) {
    status.textContent = "뉴스 목록을 불러오지 못했습니다. 이전 화면으로 돌아가 주세요.";
    return;
  }
  const time = (stamp) => stamp ? new Date(stamp).toLocaleString("ko-KR", {timeZone:"Asia/Seoul"}) : "성공 기록 없음";
  status.textContent = `목록 확인: ${time(data.updated_at)} (한국 시간)`;
  const sources = new Map(data.sources.map((s) => [s.id, s]));
  for (const source of data.sources) {
    const el = document.createElement("div");
    el.className = "source";
    el.textContent = `${source.name} · ${source.status === "OK" ? "RSS 확인" : source.status === "STALE" ? "갱신 실패 · 이전 목록" : "접근 실패"} · 마지막 성공 ${time(source.last_success_at)}`;
    document.getElementById("news-sources").append(el);
  }
  function render() {
    const selected = document.getElementById("news-filter").value;
    const articles = data.items.filter((i) => selected === "ALL" || i.category === selected);
    const container = document.getElementById("news-items");
    container.replaceChildren();
    for (const item of articles) {
      const source = sources.get(item.source_id);
      let url;
      try { url = new URL(item.url); } catch { continue; }
      if (url.protocol !== "https:" || !source || url.hostname !== new URL(source.url).hostname || url.username || url.password || (url.port && url.port !== "443")) continue;
      const card = document.createElement("article");
      card.className = "news-card";
      const tag = document.createElement("span"); tag.className = "tag";
      tag.textContent = item.category === "MONITOR_DISPLAY" ? "모니터·디스플레이 · 제목 기반" : "테크 · 제목 기반";
      const title = document.createElement("h2"); title.textContent = item.title;
      const meta = document.createElement("p"); meta.className = "meta";
      meta.textContent = `${source.name} · 제조사 소식 · ${source.language === "en" ? "영어 원문" : source.language === "ko" ? "한국어 원문" : "언어 미확인"} · 발행 ${time(item.published_at)}`;
      const link = document.createElement("a"); link.href = url.href; link.target = "_blank"; link.rel = "noopener noreferrer"; link.textContent = "원문 읽기 ↗";
      card.append(tag, title, meta, link); container.append(card);
    }
    document.getElementById("news-empty").hidden = container.childElementCount !== 0;
  }
  document.getElementById("news-filter").addEventListener("change", render);
  document.getElementById("news-reload").addEventListener("click", () => window.location.reload());
  render();
})();
