(() => {
  "use strict";
  const data = window.CONNECTABLE_TECH_NEWS;
  const status = document.getElementById("news-status");
  if (!data || !Array.isArray(data.items) || !Array.isArray(data.sources)) {
    status.textContent =
      "뉴스 목록을 불러오지 못했습니다. 이전 화면으로 돌아가 주세요.";
    ["news-filter","news-search","news-source-filter"].forEach(id => document.getElementById(id).disabled = true);
    document
      .getElementById("news-reload")
      .addEventListener("click", () => window.location.reload());
    return;
  }
  const time = (stamp, fallback = "시각 미확인") => {
    if (typeof stamp !== "string" || !stamp || Number.isNaN(Date.parse(stamp)))
      return fallback;
    return new Date(stamp).toLocaleString("ko-KR", { timeZone: "Asia/Seoul" });
  };
  status.textContent = `저장 목록 확인: ${time(data.updated_at)} (한국 시간)`;
  const sourceRows = data.sources.filter((s) => s && typeof s.id === "string");
  const sources = new Map(sourceRows.map((s) => [s.id, s]));
  for (const source of sourceRows) {
    const option = document.createElement("option"); option.value = source.id; option.textContent = source.name; document.getElementById("news-source-filter").append(option);
    const el = document.createElement("div");
    el.className = "source";
    el.textContent = `${source.name} · ${source.status === "OK" ? "RSS 확인" : source.status === "STALE" ? "갱신 실패 · 이전 목록" : source.status === "ACCESS_FAILED" ? "접근 실패" : "수집 상태 미확인"} · 마지막 성공 ${time(source.last_success_at, "성공 시각 미확인")}`;
    document.getElementById("news-sources").append(el);
  }
  function render() {
    const selected = document.getElementById("news-filter").value;
    const query = document.getElementById("news-search").value.trim().toLocaleLowerCase();
    const sourceFilter = document.getElementById("news-source-filter").value;
    const articles = data.items.filter(
      (i) => i && typeof i.title === "string" && i.title.toLocaleLowerCase().includes(query) && (sourceFilter === "ALL" || i.source_id === sourceFilter) && (selected === "ALL" || i.category === selected),
    );
    const container = document.getElementById("news-items");
    container.replaceChildren();
    for (const item of articles) {
      const source = sources.get(item.source_id);
      let url, sourceUrl;
      try {
        url = new URL(item.url);
        sourceUrl = new URL(source?.url);
      } catch {
        continue;
      }
      if (
        url.protocol !== "https:" ||
        sourceUrl.protocol !== "https:" ||
        url.hostname !== sourceUrl.hostname ||
        url.username ||
        url.password ||
        sourceUrl.username ||
        sourceUrl.password ||
        (url.port && url.port !== "443") ||
        (sourceUrl.port && sourceUrl.port !== "443")
      )
        continue;
      if (typeof item.title !== "string" || !item.title.trim()) continue;
      const card = document.createElement("article");
      card.className = "news-card";
      const tag = document.createElement("span");
      tag.className = "tag";
      tag.textContent =
        item.category === "MONITOR_DISPLAY"
          ? "모니터·디스플레이 · 제목 기반"
          : "테크 · 제목 기반";
      const title = document.createElement("h2");
      title.textContent = item.title;
      const meta = document.createElement("p");
      meta.className = "meta";
      meta.textContent = `${source.name} · ${source.kind === "MANUFACTURER_NEWSROOM" ? "제조사 소식" : "출처 유형 미확인"} · ${source.language === "en" ? "영어 원문" : source.language === "ko" ? "한국어 원문" : "언어 미확인"} · 발행 ${time(item.published_at)}`;
      const link = document.createElement("a");
      link.href = url.href;
      link.target = "_blank";
      link.rel = "noopener noreferrer";
      link.textContent = "원문 읽기 ↗";
      card.append(tag, title, meta, link);
      container.append(card);
    }
    document.getElementById("news-empty").hidden =
      container.childElementCount !== 0;
    document.getElementById("news-count").textContent =
      `표시 중 ${container.childElementCount}건`;
  }
  document.getElementById("news-search").addEventListener("input", render);
  document.getElementById("news-source-filter").addEventListener("change", render);
  document.getElementById("news-filter").addEventListener("change", render);
  document
    .getElementById("news-reload")
    .addEventListener("click", () => window.location.reload());
  render();
})();
