(() => {
  "use strict";
  const $ = (s) => document.querySelector(s);
  const array = (v) => (Array.isArray(v) ? v : []);
  const str = (v) => (typeof v === "string" ? v : "UNKNOWN");
  const esc = (v) =>
    str(v).replace(
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
  const data = window.CONNECTABLE_SITE_V2;
  const valid =
    data &&
    ["monitors", "reviews", "guides"].every(
      (k) =>
        Array.isArray(data[k]) &&
        data[k].every(
          (r) =>
            r &&
            typeof r.id === "string" &&
            typeof r.title === "string" &&
            Array.isArray(r.source_refs),
        ),
    );
  if (!valid) {
    for (const kind of ["monitor", "review", "guide"])
      $(`#${kind}-list`).innerHTML =
        '<div class="empty error"><strong>콘텐츠를 불러오지 못했습니다.</strong><p>정적 데이터 파일과 생성 상태를 확인하세요.</p></div>';
    return;
  }
  const monitors = data.monitors,
    reviews = data.reviews,
    guides = data.guides;
  function originalKey(r) {
    for (const ref of array(r.source_refs)) {
      try {
        const u = new URL(ref.url);
        if (u.protocol !== "https:" || u.username || u.password) continue;
        u.hash = "";
        for (const key of [...u.searchParams.keys()])
          if (/^utm_/i.test(key) || ["fbclid", "gclid"].includes(key))
            u.searchParams.delete(key);
        u.searchParams.sort();
        u.pathname = u.pathname.replace(/\/$/, "") || "/";
        return u.href;
      } catch {}
    }
    return "record:" + r.id;
  }
  const reviewGroups = new Map();
  for (const r of reviews) {
    const key = originalKey(r);
    if (!reviewGroups.has(key)) reviewGroups.set(key, []);
    reviewGroups.get(key).push(r);
  }
  const selected = new Set();
  const addonLabels = {
    usb_c_video: "USB-C로 영상 연결",
    pd: "충전 공급 (공식 표기)",
    kvm: "키보드·마우스 공유 (KVM)",
    speaker: "스피커 내장",
    height: "높이 조절",
  };
  function addonFacts(m, key) {
    const capability =
      m.capabilities?.[
        {
          usb_c_video: "usb_c_video",
          pd: "pd_supply",
          kvm: "kvm",
          speaker: "speakers",
          height: "height_adjustment",
        }[key]
      ];
    if (capability && capability.status !== "CONFIRMED_MANUFACTURER_STATEMENT")
      return [];
    return array(m.features).filter((f) => {
      if (f.basis !== "MANUFACTURER_SPEC") return false;
      const p = f.payload || {},
        prop = f.property;
      if (key === "usb_c_video")
        return (
          prop === "PROTOCOL" &&
          String(p.interface).startsWith("USB_C") &&
          p.support === "SUPPORTED"
        );
      if (key === "pd") return prop === "POWER_TRANSFER" && p.mode === "OFFER";
      if (key === "kvm") return prop === "KVM" && p.support === "SUPPORTED";
      if (key === "speaker")
        return (
          ["SPEAKER", "SPEAKERS", "AUDIO"].includes(prop) &&
          (p.support === "SUPPORTED" || p.built_in === true)
        );
      if (key === "height")
        return (
          ["ERGONOMICS", "HEIGHT_ADJUSTMENT", "STAND"].includes(prop) &&
          (p.height_adjustment === true ||
            p.height_adjustable === true ||
            (p.support === "SUPPORTED" && prop === "HEIGHT_ADJUSTMENT"))
        );
      return false;
    });
  }
  const readableTitle = (r) =>
    summary(r)[0] ||
    array(r.connection_summary)[0] ||
    r.title.replace(/^(?:PUR|UQ)-\d+\s*[·:–-]\s*/, "");
  function reviewType(r) {
    const observed = new Set(
      array(r.configurations)
        .filter((c) => c.role === "OBSERVED")
        .map((c) => c.id),
    );
    const observations = array(r.observations).filter((o) =>
      observed.has(o.configuration_id),
    );
    if (
      observations.some((o) =>
        ["NO_SIGNAL", "DEGRADED", "INTERMITTENT"].includes(o.signal_state),
      )
    )
      return "문제 관측 포함";
    if (observations.some((o) => o.signal_state === "NORMAL"))
      return "사용 관측 포함";
    return "연결 기록";
  }
  const reviewLinksFor = (m) =>
    reviews.filter((r) => array(r.monitor_ids).includes(m.id));
  const labels = {
    VIDEO_PROFILE: "해상도·주사율",
    PROTOCOL: "영상 연결",
    POWER_TRANSFER: "충전 공급",
    KVM: "키보드·마우스 공유",
    SPEAKERS: "스피커",
    HEIGHT_ADJUSTMENT: "높이 조절",
    PORTS: "연결 포트",
    REMOTE_CONTROL: "리모컨",
    VESA: "모니터 암 장착",
    PIP_PBP: "화면 분할",
    TILT: "기울기 조절",
  };
  const status = '<span class="status">검토 중 · UNKNOWN</span>';
  const sourceHTML = (r) =>
    '<h3>출처와 확인일</h3><ul class="source-list">' +
    array(r.source_refs)
      .map((s) => {
        let u;
        try {
          u = new URL(s.url);
        } catch {
          return "";
        }
        if (u.protocol !== "https:" || u.username || u.password) return "";
        return `<li><a href="${esc(u.href)}" target="_blank" rel="noopener noreferrer">${esc(s.title || u.hostname)} ↗</a> · 확인 ${esc(s.checked_on)} · 게시 ${esc(s.published_on)}</li>`;
      })
      .join("") +
    "</ul>";
  const listHTML = (values) =>
    "<ul>" +
    array(values)
      .map((v) => `<li>${esc(typeof v === "string" ? v : v.summary)}</li>`)
      .join("") +
    "</ul>";
  const summary = (r) =>
    array(r.observations)
      .map((o) => o.summary)
      .filter((v) => typeof v === "string");
  const contains = (r, q) =>
    JSON.stringify(r).toLowerCase().includes(q.toLowerCase());
  const known = (v) => v !== undefined && v !== null && v !== "UNKNOWN";
  const topics = {
    video: "영상 출력",
    pd: "충전",
    sleep_wake: "잠자기 복귀",
    reconnect: "재연결",
  };
  const hasTopic = (r, topic) =>
    array(r.functional_observations).some((o) => {
      const f = o[topic === "video" ? "video_output" : topic];
      return f && known(f.status ?? f.recognized);
    });
  function options(selector, values) {
    const el = $(selector);
    for (const v of [...new Set(values)]
      .filter((v) => v && v !== "UNKNOWN")
      .sort()) {
      const opt = document.createElement("option");
      opt.value = v;
      opt.textContent = v;
      el.append(opt);
    }
  }
  options(
    "#mac-filter",
    reviews.map((r) => r.macbook_display_name),
  );
  for (const [key, label] of Object.entries(topics)) {
    const o = document.createElement("option");
    o.value = key;
    o.textContent = label;
    $("#purpose-filter").append(o);
  }
  // This is a reading interest, not a claim about the author's work or product suitability.
  $("#purpose-filter").parentElement.firstChild.textContent = "살펴볼 항목";
  for (const [key, label] of Object.entries(labels).filter(([key]) =>
    ["VIDEO_PROFILE", "PROTOCOL", "POWER_TRANSFER"].includes(key),
  )) {
    const o = document.createElement("option");
    o.value = key;
    o.textContent = label;
    $("#feature-filter").append(o);
  }
  for (const [key, label] of Object.entries(addonLabels)) {
    const o = document.createElement("option");
    o.value = key;
    o.textContent = label;
    $("#addon-filter").append(o);
  }
  let shownReviews = 6;
  function empty(title, text) {
    return `<div class="empty"><strong>${title}</strong><p>${text}</p></div>`;
  }
  function render() {
    const mac = $("#mac-filter").value,
      topic = $("#purpose-filter").value,
      feature = $("#feature-filter").value,
      query = $("#search").value.trim(),
      addon = $("#addon-filter").value;
    const rr = reviews.filter(
      (r) =>
        (!mac || r.macbook_display_name === mac) &&
        (!topic || hasTopic(r, topic)) &&
        (!query || contains(r, query)),
    );
    const groups = [...reviewGroups.values()].filter((group) =>
      group.some((r) => rr.includes(r)),
    );
    const mm = monitors.filter(
      (m) =>
        (!addon || addonFacts(m, addon).length > 0) &&
        (!feature || array(m.features).some((f) => f.property === feature)) &&
        (!query || contains(m, query)) &&
        ((!mac && !topic) ||
          rr.some((r) => array(r.monitor_ids).includes(m.id))),
    );
    $("#monitor-count").textContent = `${mm.length}개 모델`;
    $("#review-count").textContent =
      `${groups.length}개 원문 그룹 · 연구 기록 ${rr.length}개`;
    $("#monitor-list").innerHTML =
      mm
        .map(
          (m) =>
            `<article class="card"><div class="product-art" role="img" aria-label="일반 모니터 개념도. ${esc(m.title)} 실제 제품 사진 아님"><span>제품 사진 미확보 · 개념도</span></div><div class="card-body">${status}<h3>${esc(m.title)}</h3><div class="tags">${[
              ...new Set(
                array(m.features).map(
                  (f) => labels[f.property] || "기타 공식 기능",
                ),
              ),
            ]
              .slice(0, 3)
              .map((t) => `<span class="tag">${esc(t)}</span>`)
              .join(
                "",
              )}</div><p>${esc(array(m.features)[0]?.summary || "공식 기능 확인 중")}</p><p>동일 모델 연구 기록 ${reviewLinksFor(m).length}개 · ${reviewLinksFor(m).length ? "개별 구성의 관측 확인" : "연결된 후기 없음"}</p><label class="compare-choice"><input type="checkbox" data-compare="${esc(m.id)}" ${selected.has(m.id) ? "checked" : ""} ${selected.size === 2 && !selected.has(m.id) ? "disabled" : ""}> ${esc(m.title)} 비교 담기</label><button class="card-link" data-kind="monitors" data-id="${esc(m.id)}">${esc(m.title)} 기능·후기 보기 →</button></div></article>`,
        )
        .join("") ||
      empty(
        monitors.length
          ? "조건에 맞는 확인 자료가 없습니다."
          : "모니터 자료를 준비하고 있습니다.",
        "후기의 공식 모델 연결이 미상인 경우 후보를 추정하지 않습니다. 필터를 초기화해 전체 자료를 살펴보세요.",
      );
    $("#review-list").innerHTML =
      groups
        .slice(0, shownReviews)
        .map((group) => {
          const r = group.find((r) => rr.includes(r));
          return `<article class="card"><div class="card-body"><div class="tags"><span class="tag">${reviewType(r)} · 사용자 보고 C등급</span>${status}</div><h3>${esc(readableTitle(r))}</h3>${group.length > 1 ? `<p class="group-note">동일 원문 연구 기록 ${group.length}개<br>상세에서 각 기록의 관측을 확인하세요.</p>` : ""}<p>${esc(r.macbook_display_name)} · ${esc(array(r.reported_monitor_models).join(" / ") || "모니터 모델 UNKNOWN")}</p><p>${esc(array(r.connection_summary)[0] || "연결 경로 UNKNOWN")}</p><button class="card-link" data-kind="reviews" data-id="${esc(r.id)}">연결 기록 자세히 보기 →</button></div></article>`;
        })
        .join("") ||
      empty(
        reviews.length
          ? "검색 조건에 맞는 후기가 없습니다."
          : "출처 있는 후기를 준비하고 있습니다.",
        "새 조건으로 검색하거나 필터를 초기화하세요.",
      );
    if (groups.length > shownReviews) {
      const b = document.createElement("button");
      b.className = "button secondary";
      b.id = "more-reviews";
      b.textContent = "후기 더 보기";
      b.addEventListener("click", () => {
        shownReviews += 6;
        render();
        $("#more-reviews")?.focus();
      });
      $("#review-list").append(b);
    }
    renderCompareBar();
    $("#guide-list").innerHTML =
      guides
        .map(
          (g) =>
            `<article class="card"><div class="card-body">${status}<h3>${esc(g.title)}</h3><p>${esc(array(g.body)[0])}</p><button class="card-link" data-kind="guides" data-id="${esc(g.id)}">${esc(g.title)} 읽기 →</button></div></article>`,
        )
        .join("") ||
      empty(
        "연결 가이드를 준비하고 있습니다.",
        "확인 가능한 근거가 도착하면 표시합니다.",
      );
  }
  function renderCompareBar() {
    $("#compare-bar").hidden = selected.size === 0;
    $("#compare-selection").textContent =
      [...selected]
        .map((id) => monitors.find((m) => m.id === id)?.title)
        .join(" / ") + ` · ${selected.size}/2개 선택`;
    $("#compare-open").disabled = selected.size !== 2;
  }
  const unknown = "UNKNOWN · 아직 확인되지 않음 (미지원 아님)";
  function comparisonRows() {
    return [
      [
        "패널 해상도·Hz",
        (m) =>
          array(m.features).filter(
            (f) =>
              f.property === "VIDEO_PROFILE" && f.payload?.scope === "PANEL",
          ),
      ],
      [
        "입력 포트별 해상도·Hz",
        (m) =>
          array(m.features).filter(
            (f) =>
              f.property === "VIDEO_PROFILE" && f.payload?.scope === "PORT",
          ),
      ],
      ["USB-C 영상 지원", (m) => addonFacts(m, "usb_c_video")],
      [
        "공식 PD 공급 전력 상한·표기",
        (m) =>
          array(m.features).filter(
            (f) =>
              f.property === "POWER_TRANSFER" && f.payload?.mode === "OFFER",
          ),
      ],
      ["KVM", (m) => addonFacts(m, "kvm")],
      ["스피커", (m) => addonFacts(m, "speaker")],
      ["높이 조절", (m) => addonFacts(m, "height")],
    ];
  }
  function openComparison() {
    if (selected.size !== 2) return;
    const pair = [...selected].map((id) => monitors.find((m) => m.id === id));
    if (!dialog.open) opener = document.activeElement;
    $("#detail-body").innerHTML =
      `${status}<h2 id="detail-title">두 모니터 비교</h2><p>같은 항목을 공식 자료로 비교합니다. UNKNOWN은 미지원이 아니며, 공식 공급 전력은 맥북의 실제 수전 전력이 아닙니다.</p><p class="comparison-hint">화면이 좁으면 표 안에서 좌우로 이동해 두 제품을 비교하세요.</p><div class="comparison-scroll" tabindex="0" role="region" aria-label="모니터 비교표 · 가로 이동 가능"><table class="comparison"><caption>공식 기능 및 동일 모델 연결 기록 비교</caption><thead><tr><th scope="col">비교 항목</th>${pair.map((m) => `<th scope="col">${esc(m.title)}</th>`).join("")}</tr></thead><tbody>${comparisonRows()
        .map(
          ([label, extract]) =>
            `<tr><th scope="row">${label}</th>${pair
              .map(
                (m) =>
                  `<td>${
                    extract(m)
                      .map((f) => esc(f.summary))
                      .join("<br>") || unknown
                  }</td>`,
              )
              .join("")}</tr>`,
        )
        .join("")}<tr><th scope="row">동일 모델 연결 기록</th>${pair
        .map(
          (m) =>
            `<td><div class="detail-links">${
              related(
                "reviews",
                reviewLinksFor(m).map((r) => r.id),
              ) || "정확히 연결된 후기 없음"
            }</div></td>`,
        )
        .join(
          "",
        )}</tr><tr><th scope="row">출처 지역·검토 상태</th>${pair.map((m) => `<td>${esc(m.region)} · 검토 중 · UNKNOWN</td>`).join("")}</tr></tbody></table></div><h3>제품 상세</h3><div class="detail-links">${related(
        "monitors",
        pair.map((m) => m.id),
      )}</div>${pair.map((m) => `<h3>${esc(m.title)}</h3>${sourceHTML(m)}`).join("")}`;
    if (!dialog.open) dialog.showModal();
    dialog.scrollTop = 0;
    $(".dialog-close").focus();
  }
  $("#compare-open").addEventListener("click", openComparison);
  $("#compare-clear").addEventListener("click", () => {
    selected.clear();
    render();
  });
  document.addEventListener("change", (e) => {
    const id = e.target.dataset.compare;
    if (!id) return;
    if (e.target.checked && selected.size < 2) selected.add(id);
    else selected.delete(id);
    render();
    document.querySelector(`[data-compare="${CSS.escape(id)}"]`)?.focus();
  });
  document.addEventListener("click", (e) => {
    const b = e.target.closest("[data-jump]");
    if (!b) return;
    const target = document.getElementById(b.dataset.jump);
    target?.scrollIntoView({ block: "start" });
    target?.focus();
  });
  const dialog = $("#detail");
  let opener = null,
    pushed = false;
  function related(kind, ids) {
    return array(ids)
      .map((id) => {
        const r = data[kind].find((x) => x.id === id);
        return r
          ? `<button data-kind="${kind}" data-id="${esc(id)}">${esc(kind === "reviews" ? readableTitle(r) : r.title)} →</button>`
          : "";
      })
      .join("");
  }
  function open(kind, id, fromRoute = false) {
    const r = array(data[kind]).find((r) => r.id === id);
    if (!r) return;
    const wasOpen = dialog.open;
    if (!wasOpen) opener = document.activeElement;
    let body = "";
    if (kind === "monitors") {
      const linked = reviewLinksFor(r);
      body = `<section><h3>제품 요약</h3><p>${esc(array(r.features)[0]?.summary || "공식 요약 확인 필요")} · 출처 지역 ${esc(r.region)}</p>${r.variant ? `<p>모델 범위: ${esc(r.variant)}</p>` : ""}<p>사람 검토 대기. 한국 판매 변형과 맥북의 실제 출력·충전 결과는 별도 확인이 필요합니다.</p></section><section><h3>공식 기능과 부가기능</h3>${array(
        r.features,
      )
        .map(
          (f) =>
            `<p><strong>${esc(f.summary)}</strong></p>${array(f.conditions).length ? listHTML(f.conditions) : ""}`,
        )
        .join("")}<ul>${Object.entries(addonLabels)
        .map(
          ([key, label]) =>
            `<li>${label}: ${
              addonFacts(r, key).length
                ? addonFacts(r, key)
                    .map((f) => esc(f.summary))
                    .join(" / ")
                : "UNKNOWN · 아직 확인되지 않음 (미지원 아님)"
            }</li>`,
        )
        .join(
          "",
        )}</ul></section><section><h3>동일 모델의 연결 기록</h3><p>표시 모델 수준의 연결입니다. 실물 SKU·리비전 일치와 호환성 승인을 뜻하지 않습니다.</p><div class="detail-links">${
        related(
          "reviews",
          linked.map((x) => x.id),
        ) ||
        "<p>정확한 공식 모델에 연결된 후기가 없습니다. 비슷한 모델명을 대신 연결하지 않습니다.</p>"
      }</div></section><section><h3>주의할 점과 결측</h3>${
        r.capabilities
          ? listHTML(
              Object.values(r.capabilities)
                .map((c) => c.notes)
                .filter((n) => typeof n === "string"),
            )
          : ""
      }${listHTML(r.missing_fields)}</section><section><h3>케이블과 설정을 확인하세요</h3>${linked.length ? listHTML(linked.flatMap((x) => array(x.connection_summary))) : "<p>이 모델의 사용자 케이블·설정 자료는 아직 확인되지 않았습니다.</p>"}<p>영상 입력·케이블 모델·길이·OS·덮개·충전 조건을 따로 확인하세요.</p></section><h3>함께 읽을 가이드</h3><div class="detail-links">${related(
        "guides",
        guides
          .filter((x) => array(x.related_monitor_ids).includes(id))
          .map((x) => x.id),
      )}</div>`;
    } else if (kind === "reviews") {
      const siblings = reviewGroups.get(originalKey(r)) || [r];
      body = `<h3>연결 경험 요약</h3><p>${esc(summary(r)[0] || "관측 UNKNOWN")}</p><p>사용자 보고 · C등급 · 호환성 판정에 사용 불가 · 사람 검토 대기</p><p>${esc(r.macbook_display_name)} / ${esc(array(r.reported_monitor_models).join(" / "))}</p><h3>보고된 연결 경로</h3>${listHTML(r.connection_summary)}<h3>구성 범위</h3>${listHTML(array(r.configurations).map((c) => `${c.id} · ${{ OBSERVED: "작성자 관측", TARGET: "목표·계획", ADVICE: "조언" }[c.role] || c.role} · ${c.topology_completeness} · ${c.notes || "UNKNOWN"}`))}<h3>관측과 불편</h3>${listHTML(summary(r))}${array(
        r.observations,
      )
        .map(
          (o) =>
            `<p>구성 ${esc(o.configuration_id)} · 신호 상태 ${esc(o.signal_state)} · 지속성 ${esc(o.durability)} · 충전 ${esc(o.pd_charging)} · 덮개 ${esc(o.clamshell)}</p>`,
        )
        .join(
          "",
        )}<h3>작성자의 구성별 결론</h3>${array(r.configuration_conclusions).length ? listHTML(array(r.configuration_conclusions).map((c) => `${c.configuration_id} · ${c.status} · ${c.termination_type} · ${c.summary}`)) : "<p>구성별 종결 결론 UNKNOWN</p>"}<p>종결 진술은 해당 구성의 사용자 기록이며 공식 판정이 아닙니다.</p><h3>기능별 관측 (측정·설정 구분)</h3>`;
      if (siblings.length > 1)
        body =
          `<h3>동일 원문의 다른 연구 기록</h3><p>이 원문은 연구 기록 ${siblings.length}개로 정리되었습니다. 별도 사용자 후기 ${siblings.length}건이 아닙니다. 각 기록의 구성과 관측을 따로 확인하세요.</p><div class="detail-links">${related(
            "reviews",
            siblings.filter((x) => x.id !== r.id).map((x) => x.id),
          )}</div>` + body;
      if (!array(r.functional_observations).length)
        body +=
          "<p>기능별 정리 자료 UNKNOWN. 위 관측 요약과 결측을 확인하세요.</p>";
      body += array(r.functional_observations)
        .map(
          (o) =>
            `<p>${esc(o.observation_id)} · 영상 ${esc(o.video_output?.status)} · 신호 해상도 ${esc(String(o.signal_mode?.resolution_pixels ?? "UNKNOWN"))} · 해상도 표기 ${esc(o.signal_mode?.resolution_label)} · Hz ${esc(String(o.signal_mode?.hz ?? "UNKNOWN"))} (${esc(o.signal_mode?.hz_basis)}) · UI 배율 ${esc(String(o.ui_scale?.value ?? "UNKNOWN"))} · 충전 인식 ${esc(o.pd?.recognized)} / W ${esc(String(o.pd?.watts ?? "UNKNOWN"))} · 덮개 ${esc(o.clamshell?.status)} · 잠자기 복귀 ${esc(o.sleep_wake?.status)} · 재연결 ${esc(o.reconnect?.status)}</p>`,
        )
        .join("");
      body += `<h3>결측과 확인할 점</h3>${listHTML(r.missing_fields)}<h3>상업성 맥락</h3><p>판매 링크 ${esc(r.commercial_context?.sales_links)} · 제휴 링크 ${esc(r.commercial_context?.affiliate_links)} · 광고 ${esc(r.commercial_context?.advertising)}</p><p>${esc(r.commercial_context?.inclusion_basis)} · ${esc(r.commercial_context?.notes)}</p><h3>관련 공식 모델</h3>${array(r.monitor_links).length ? "<p>MODEL_ONLY · 표시 모델 수준 연결. 실물 SKU·변형·리비전 일치 UNKNOWN.</p>" : ""}<div class="detail-links">${related("monitors", r.monitor_ids) || "<p>공식 모델 연결 UNKNOWN. 보고된 모델명으로 자동 연결하지 않습니다.</p>"}</div><h3>함께 읽을 가이드</h3><div class="detail-links">${
        related(
          "guides",
          guides
            .filter((g) => array(g.related_review_ids).includes(id))
            .map((g) => g.id),
        ) ||
        related(
          "guides",
          guides.map((g) => g.id),
        )
      }</div>`;
    } else {
      body = `<p>편집 체크리스트 · 사람 검토 대기</p><h3>짧은 요약</h3><p>${esc(array(r.body)[0])}</p><nav class="guide-toc" aria-label="가이드 목차"><h3>확인할 순서</h3>${array(
        r.body,
      )
        .map(
          (p, i) =>
            `<button data-jump="guide-part-${i}">${i + 1}. ${esc(p)}</button>`,
        )
        .join("")}</nav>${array(r.body)
        .map(
          (p, i) =>
            `<section id="guide-part-${i}" tabindex="-1"><h3>확인 항목 ${i + 1}</h3><p>${esc(p)}</p></section>`,
        )
        .join(
          "",
        )}<h3>관련 모니터</h3><div class="detail-links">${related("monitors", r.related_monitor_ids)}</div><h3>관련 연결 후기</h3><div class="detail-links">${related("reviews", r.related_review_ids)}</div>`;
    }
    $("#detail-body").innerHTML =
      `${status}<h2 id="detail-title">${esc(kind === "reviews" ? readableTitle(r) : r.title)}</h2><p>공개 호환 판정 UNKNOWN · 개별 보고는 다른 구성의 성공 보장이 아닙니다.</p>${body}<details class="record-evidence"><summary>근거 기록 ID와 검토 상태</summary><p>기록 ID: ${esc(r.id)} · 검토 상태: ${esc(r.review_status)} · 원본 제목: ${esc(r.title)}</p></details>${sourceHTML(r)}`;
    if (!dialog.open) dialog.showModal();
    dialog.scrollTop = 0;
    $(".dialog-close").focus();
    if (!fromRoute) {
      if (!wasOpen) {
        history.pushState(null, "", `#${kind}/${encodeURIComponent(id)}`);
        pushed = true;
      } else
        history.replaceState(null, "", `#${kind}/${encodeURIComponent(id)}`);
    }
  }
  document.addEventListener("click", (e) => {
    const b = e.target.closest("[data-kind][data-id]");
    if (b) open(b.dataset.kind, b.dataset.id);
  });
  $(".dialog-close").addEventListener("click", () => dialog.close());
  dialog.addEventListener("close", () => {
    const section = location.hash.split("/")[0];
    if (pushed) {
      pushed = false;
      history.back();
    } else if (["#monitors", "#reviews", "#guides"].includes(section))
      history.replaceState(null, "", section);
    if (opener?.isConnected) opener.focus();
  });
  function route() {
    const match = location.hash.match(/^#(monitors|reviews|guides)\/(.+)$/);
    if (match) {
      try {
        open(match[1], decodeURIComponent(match[2]), true);
      } catch {}
    } else if (dialog.open) {
      pushed = false;
      dialog.close();
    }
  }
  window.addEventListener("hashchange", route);
  window.addEventListener("popstate", route);
  for (const s of [
    "#mac-filter",
    "#purpose-filter",
    "#feature-filter",
    "#addon-filter",
    "#search",
  ])
    $(s).addEventListener(s === "#search" ? "input" : "change", () => {
      shownReviews = 6;
      render();
    });
  $("#reset").addEventListener("click", () => {
    for (const s of [
      "#mac-filter",
      "#purpose-filter",
      "#feature-filter",
      "#addon-filter",
      "#search",
    ])
      $(s).value = "";
    shownReviews = 6;
    render();
  });
  const disclosure = data.disclosures;
  if (disclosure && !Array.isArray(disclosure))
    $("#disclosure-text").innerHTML = Object.values(disclosure)
      .filter((v) => typeof v === "string")
      .map((v) => `<p>${esc(v)}</p>`)
      .join("");
  render();
  route();
})();
