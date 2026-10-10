"use strict";
(() => {
  const $ = (id) => document.getElementById(id);
  const data = window.CONNECTABLE_MONITORS;
  if (
    !data ||
    data.public_status !== "UNKNOWN" ||
    !Array.isArray(data.products)
  ) {
    $("interaction-status").textContent =
      "조사 데이터를 불러올 수 없습니다. 새로고침하거나 정적 제품 정보 링크를 이용해주세요.";
    $("result-count").textContent = "불러오기 실패";
    document
      .querySelectorAll(
        ".filter-body input, .filter-body select, #monitor-search, #sort-order, #nav-compare",
      )
      .forEach((el) => {
        el.disabled = true;
      });
    return;
  }
  const products = data.products;
  const selected = new Set();
  const esc = (value) =>
    String(value ?? "").replace(
      /[&<>"']/g,
      (c) =>
        ({
          "&": "&amp;",
          "<": "&lt;",
          ">": "&gt;",
          '"': "&quot;",
          "'": "&#39;",
        })[c],
    );
  const name = (p) => `${p.manufacturer} ${p.display_model}`;
  const unknown = (value) => value === null || value === undefined;
  const fmt = (value) =>
    unknown(value)
      ? "미확인"
      : typeof value === "object"
        ? JSON.stringify(value)
        : String(value);
  const labels = {
    size: "화면 크기",
    width: "가로 해상도",
    height: "세로 해상도",
    panel: "패널",
    refresh: "최대 주사율",
    brightness_typical: "일반 밝기",
    brightness_hdr_peak: "HDR 최고 밝기",
    brightness_unspecified: "밝기 (종류 미명시)",
    contrast_native: "기본 명암비",
    contrast_dynamic: "동적 명암비",
    response: "응답 시간",
    color_gamut: "색 영역",
    hdr: "HDR",
    hdmi: "HDMI",
    displayport: "DisplayPort",
    displayport_out: "DisplayPort 출력",
    usb_c: "USB-C",
    thunderbolt: "Thunderbolt",
    usb_hub: "USB 허브",
    pd_supply: "PD 공급",
    pd_supply_upstream: "업스트림 PD 공급",
    pd_supply_downstream: "다운스트림 PD 공급",
    kvm: "KVM",
    stand: "스탠드 조절",
    vesa: "VESA",
    vrr: "가변 주사율",
    dimensions: "치수",
    weight: "무게",
    warranty: "보증",
    power_consumption: "소비 전력",
    power_consumption_max: "최대 소비 전력",
    power_consumption_typical: "일반 소비 전력",
    power_consumption_normal: "일반 소비 전력",
    power_consumption_operating: "동작 소비 전력",
    power_consumption_standby: "대기 소비 전력",
    power_consumption_ac_input_max: "AC 입력 최대 전력",
    input_profile: "입력별 조건",
    console_input_profile: "콘솔 입력 조건",
    input_vertical_frequency: "입력 수직 주파수",
    dual_mode: "듀얼 모드",
    curvature: "곡률",
    active_area: "활성 화면 영역",
    local_dimming_zones: "로컬 디밍 영역",
    pbp: "PBP",
    pip: "PIP",
    daisy_chain: "데이지 체인",
  };
  const qualifiers = {
    UP_TO: "최대",
    RATED: "정격",
    MANUFACTURER_STATED: "제조사 표기",
    MANUFACTURER_ESTIMATE: "제조사 추정",
    TYPICAL: "일반",
    MAXIMUM: "최대",
    CONDITIONAL: "조건부",
  };
  const resolution = (f) =>
    unknown(f.width) || unknown(f.height)
      ? "해상도 미확인"
      : `${f.width} × ${f.height}`;
  function safeSource(url) {
    try {
      const u = new URL(url);
      return u.protocol === "https:" && !u.username && !u.password
        ? esc(u.href)
        : null;
    } catch {
      return null;
    }
  }
  function links(p, refs) {
    return (refs || [])
      .map((ref) => {
        const s = p.source_refs.find((x) => x.id === ref);
        const url = s && safeSource(s.url);
        return url
          ? `<a href="${url}" target="_blank" rel="noopener noreferrer">공식 출처</a>`
          : "출처 미확인";
      })
      .join(" · ");
  }
  function factValue(f) {
    return `${esc(fmt(f.value))}${f.unit ? ` ${esc(f.unit)}` : ""}`;
  }
  function factContext(f) {
    return `${esc(qualifiers[f.qualifier] || f.qualifier)} · ${esc(f.scope)}<br>${esc(f.location)}`;
  }
  function card(p) {
    const f = p.filters;
    return `<article class="product-card${selected.has(p.id) ? " selected" : ""}" data-product-id="${esc(p.id)}"><div class="monitor-art" aria-hidden="true"><div class="monitor-screen"></div><div class="monitor-neck"></div><div class="monitor-foot"></div></div><p class="product-brand">${esc(p.manufacturer)}</p><h3>${esc(p.display_model)}</h3><p class="spec-line">${unknown(f.size) ? "크기 미확인" : `${esc(f.size)}인치`} · ${esc(resolution(f))}<br>${unknown(f.refresh) ? "주사율 미확인" : `최대 ${esc(f.refresh)}Hz`} · ${esc(fmt(f.panel))}</p><div class="card-meta"><span>공식 문서 · ${esc(p.region)}</span><button type="button" data-action="detail" data-id="${esc(p.id)}" aria-label="${esc(name(p))} 출처·조건 보기">출처·조건 보기 ›</button></div><button type="button" class="select-button" data-action="select" data-id="${esc(p.id)}" aria-pressed="${selected.has(p.id)}" aria-label="${esc(name(p))} ${selected.has(p.id) ? "비교에서 빼기" : "비교에 담기"}">${selected.has(p.id) ? "✓ 비교에 담았어요" : "＋ 비교에 담기"}</button></article>`;
  }
  const filterIds = ["size", "resolution", "refresh", "panel", "usbc"];
  function matches(p) {
    const f = p.filters;
    const include = $("include-unknown").checked;
    return filterIds.every((key) => {
      const v = $(`filter-${key}`).value;
      if (v === "all") return true;
      let value = f[key === "usbc" ? "usb_c_video" : key];
      if (key === "resolution")
        value =
          unknown(f.width) || unknown(f.height)
            ? null
            : `${f.width}x${f.height}`;
      if (unknown(value)) return include;
      if (key === "size")
        return v === "small"
          ? value <= 24
          : v === "medium"
            ? value > 24 && value <= 27
            : v === "large"
              ? value > 27 && value <= 32
              : value > 32;
      if (key === "resolution") {
        const vals = { fhd: "1920x1080", qhd: "2560x1440", uhd: "3840x2160" };
        return v === "other"
          ? !Object.values(vals).includes(value)
          : value === vals[v];
      }
      if (key === "refresh")
        return v === "60"
          ? value <= 60
          : v === "120"
            ? value > 60 && value <= 120
            : value >= Number(v);
      if (key === "panel") return String(value).toUpperCase().includes(v);
      if (key === "usbc") return value === true;
      return false;
    });
  }
  function render() {
    const query = $("monitor-search").value.trim().toLocaleLowerCase();
    let list = products.filter(
      (p) => name(p).toLocaleLowerCase().includes(query) && matches(p),
    );
    const order = $("sort-order").value;
    list.sort((a, b) => {
      if (order === "name") return name(a).localeCompare(name(b), "en");
      const field = order === "size" ? "size" : "refresh";
      const av = a.filters[field],
        bv = b.filters[field];
      if (unknown(av)) return unknown(bv) ? 0 : 1;
      if (unknown(bv)) return -1;
      return order === "size" ? av - bv : bv - av;
    });
    $("product-grid").innerHTML = list.map(card).join("");
    $("result-count").textContent = `${list.length}종`;
    $("empty-state").hidden = list.length > 0;
  }
  function reset() {
    $("monitor-search").value = "";
    filterIds.forEach((key) => ($(`filter-${key}`).value = "all"));
    $("include-unknown").checked = false;
    render();
  }
  function renderTray() {
    $("compare-tray").hidden = selected.size === 0;
    $("selection-count").textContent = `${selected.size} / 3개 선택`;
    $("compare-open").disabled = selected.size < 2;
    $("compare-open").textContent = `${selected.size}개 비교하기 →`;
    $("selected-products").innerHTML = [...selected]
      .map((id) => {
        const p = products.find((x) => x.id === id);
        return `<div class="selected-item"><span>${esc(name(p))}</span><button type="button" data-action="select" data-id="${esc(id)}" aria-label="${esc(name(p))} 비교에서 빼기">×</button></div>`;
      })
      .join("");
  }
  function toggle(id) {
    if (selected.has(id)) selected.delete(id);
    else if (selected.size < 3) selected.add(id);
    else {
      $("interaction-status").textContent =
        "최대 3개까지 비교할 수 있어요. 먼저 비교함에서 한 제품을 빼주세요.";
      return;
    }
    $("interaction-status").textContent = "";
    const focus = document.activeElement;
    const wasCard = focus?.closest(".product-card");
    const wasTray = focus?.closest("#compare-tray");
    render();
    renderTray();
    if (wasCard || wasTray) {
      const target =
        [...document.querySelectorAll('[data-action="select"]')].find(
          (el) => el.dataset.id === id,
        ) ||
        document.querySelector("#selected-products button") ||
        $("monitor-search");
      target.focus();
    }
  }
  function detail(p) {
    $("detail-content").innerHTML =
      `<h2 id="detail-title">${esc(name(p))}</h2><p class="detail-meta">문서 지역 ${esc(p.region)} · 문서 모델 식별 ${esc(p.variant_status)}</p><p class="dialog-notice">한국 판매 SKU 동일성 미확인 · 사람 검토 미완료 · 호환성 판정 사용 불가. 아래는 공식 문서 조사값이며 실제 연결 성능이나 한국 SKU 사양의 보장이 아닙니다.</p><a class="detail-link" href="monitors/${encodeURIComponent(p.id.replace("monitor:", ""))}/">제품 정보 링크 열기 →</a><h3 class="detail-section">공식 문서의 사양과 조건</h3><div class="table-scroll" tabindex="0" aria-label="공식 사양표 가로 스크롤"><table><thead><tr><th scope="col">항목</th><th scope="col">표기값</th><th scope="col">조건·문서 위치</th><th scope="col">근거</th></tr></thead><tbody>${p.facts.map((f) => `<tr><th scope="row">${esc(labels[f.property] || f.property)}</th><td>${factValue(f)}</td><td>${factContext(f)}</td><td>${links(p, f.source_refs)}</td></tr>`).join("")}</tbody></table></div><h3 class="detail-section">아직 확인하지 못한 항목</h3><p class="detail-meta">${p.missing_fields.map((x) => esc(labels[x] || x)).join(" · ") || "별도 기록 없음"}</p><h3 class="detail-section">공식 출처</h3><ul class="source-list">${p.source_refs
        .map((s) => {
          const url = safeSource(s.url);
          return `<li>${url ? `<a href="${url}" target="_blank" rel="noopener noreferrer">${esc(s.title)}</a>` : esc(s.title)}<br>확인일 ${esc(s.checked_on)} · ${esc(s.access_status)}<br>${esc(s.location)}</li>`;
        })
        .join(
          "",
        )}</ul><h3 class="detail-section">조사 메모</h3><ul class="source-list">${p.notes.map((n) => `<li>${esc(n)}</li>`).join("")}</ul><section class="local-feedback"><h3 class="detail-section">이 정보가 도움이 됐나요?</h3><p>이 기기의 브라우저에만 저장하는 반응입니다. 제품 평가나 전체 사용자 집계가 아닙니다.</p><button type="button" id="helpful-toggle" aria-pressed="false">♡ 도움이 됐어요</button><p id="reaction-status" role="status"></p></section>`;
    const btn = $("helpful-toggle");
    const key = `connectable-v3-helpful:${p.id}`;
    let liked = false;
    try {
      liked = localStorage.getItem(key) === "yes";
    } catch {}
    const update = () => {
      btn.setAttribute("aria-pressed", String(liked));
      btn.textContent = liked ? "♥ 도움이 됐어요 · 취소" : "♡ 도움이 됐어요";
    };
    update();
    btn.addEventListener("click", () => {
      try {
        if (liked) localStorage.removeItem(key);
        else localStorage.setItem(key, "yes");
        liked = !liked;
        update();
        $("reaction-status").textContent = liked
          ? "이 브라우저에 저장했어요."
          : "저장된 반응을 지웠어요.";
      } catch {
        $("reaction-status").textContent =
          "브라우저 저장을 사용할 수 없습니다. 반응은 저장되지 않았어요.";
      }
    });
    $("detail-dialog").showModal();
  }
  function compare() {
    const list = [...selected].map((id) => products.find((p) => p.id === id));
    const keys = [
      ...new Set(list.flatMap((p) => p.facts.map((f) => f.property))),
    ];
    const only = $("differences-only").checked;
    const rows = keys
      .map((key) => {
        const facts = list.map((p) =>
          p.facts.filter((f) => f.property === key),
        );
        const signatures = facts.map((fs, index) =>
          JSON.stringify(
            fs.map((f) => ({
              value: f.value,
              unit: f.unit,
              scope: f.scope,
              qualifier: f.qualifier,
              location: f.location,
              region: list[index].region,
            })),
          ),
        );
        const different = new Set(signatures).size > 1;
        if (only && !different) return "";
        return `<tr class="${different ? "different" : ""}"><th scope="row">${esc(labels[key] || key)}</th>${facts.map((fs, i) => `<td>${fs.length ? fs.map((f) => `${factValue(f)}<span class="fact-context">${factContext(f)}<br>${links(list[i], f.source_refs)}</span>`).join("<hr>") : '<span class="unknown">미확인</span>'}</td>`).join("")}</tr>`;
      })
      .join("");
    $("compare-table").innerHTML =
      `<caption>공식 문서 조사값 비교 · 지역별 SKU와 실제 호환성은 미확인</caption><thead><tr><th scope="col">항목</th>${list.map((p) => `<th scope="col">${esc(name(p))}<span class="fact-context">문서 지역 ${esc(p.region)} · 한국 SKU 미확인</span></th>`).join("")}</tr></thead><tbody>${rows || `<tr><td colspan="${list.length + 1}">표기값·단위·범위·표현 종류가 다른 항목이 없습니다. 제품 동일성이나 호환성을 뜻하지 않습니다.</td></tr>`}</tbody>`;
  }
  document.addEventListener("click", (event) => {
    const b = event.target.closest("button");
    if (!b) return;
    if (b.dataset.close) {
      $(b.dataset.close).close();
      return;
    }
    if (b.dataset.action) {
      const p = products.find((p) => p.id === b.dataset.id);
      if (!p) return;
      if (b.dataset.action === "select") toggle(p.id);
      if (b.dataset.action === "detail") detail(p);
    }
  });
  $("monitor-search").addEventListener("input", render);
  filterIds.forEach((key) =>
    $(`filter-${key}`).addEventListener("change", render),
  );
  $("include-unknown").addEventListener("change", render);
  $("sort-order").addEventListener("change", render);
  $("reset-filters").addEventListener("click", reset);
  $("empty-reset").addEventListener("click", reset);
  $("differences-only").addEventListener("change", compare);
  function openCompare() {
    if (selected.size < 2) {
      $("interaction-status").textContent = "비교할 모니터를 2~3개 담아주세요.";
      $("products").scrollIntoView();
      return;
    }
    compare();
    $("compare-dialog").showModal();
  }
  $("compare-open").addEventListener("click", openCompare);
  $("nav-compare").addEventListener("click", openCompare);
  if (matchMedia("(max-width:760px)").matches) $("filters").open = false;
  render();
  renderTray();
})();
