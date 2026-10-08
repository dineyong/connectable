"use strict";
(() => {
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
  const unknown = "정보 없음 · 범위 미상 (UNKNOWN)";
  const value = (x) =>
    x == null || x === "" || x === "UNKNOWN" ? unknown : String(x);
  const labels = {
    NORMAL: "정상 보고 · 검토 대기",
    PROBLEM: "문제 보고 · 검토 대기",
    TEMPORARY_WORKAROUND: "임시 우회 · 검토 대기",
    UNKNOWN: unknown,
  };
  const domains = {
    video_output: "화면 출력",
    signal_mode: "해상도·주사율",
    ui_scale: "UI 배율",
    pd: "충전",
    clamshell: "클램쉘",
    sleep_wake: "잠자기 복귀",
    reconnect: "재연결",
  };
  const evidenceDomains = {
    VIDEO_OUTPUT: "화면 출력",
    SIGNAL_MODE: "모드 표기",
    UI_SCALE: "UI 배율",
    PD_CHARGING: "충전",
    CLAMSHELL: "클램쉘",
    SLEEP_WAKE: "잠자기 복귀",
    RECONNECT: "재연결",
    OTHER: "기타 진술",
  };
  const roles = {
    AUTHOR_OBSERVATION: "작성자 실제 관측",
    PERFORMED_CHANGE: "작성자 수행 조치",
    CONFIGURATION_REPORT: "작성자 연결 구성 설명",
    ADVICE: "조언 · 수행 아님",
    PURCHASE_PLAN: "구매 계획 · 수행 아님",
    PRODUCT_DESCRIPTION: "상품 소개 · 실측 아님",
    CONTEXT: "맥락·기기 정보",
  };
  const kinds = {
    SOURCE: "소스 기기",
    DISPLAY: "디스플레이",
    CABLE: "케이블",
    HUB: "허브",
    DOCK: "독",
    ADAPTER: "어댑터",
    POWER_SOURCE: "전원 장치",
    UNKNOWN_DEVICE: "장치 미상",
  };
  const connectors = {
    USB_C: "USB-C",
    USB_A: "USB-A",
    HDMI: "HDMI",
    DISPLAYPORT: "DisplayPort",
    MINI_DISPLAYPORT: "Mini DisplayPort",
    THUNDERBOLT_REPORTED: "Thunderbolt라고 표기",
    VGA: "VGA",
    INTERNAL: "내장",
    UNKNOWN: "포트 미상",
  };
  const configRoles = {
    OBSERVED: "실제 사용 구성",
    TARGET: "목표 구성 · 수행 아님",
    ADVICE: "제안 구성 · 수행 아님",
  };
  const settingLabels = {
    external_power: "외부 전원 연결",
    lid: "덮개",
    hdr: "HDR",
    os_name: "운영체제",
    os_version: "OS 버전",
    laptop_case: "노트북 케이스",
  };
  const settingValues = {
    YES: "있음",
    NO: "없음",
    CLOSED: "닫힘",
    OPEN: "열림",
    ON: "사용",
    OFF: "미사용",
  };
  const modeBasis = {
    REPORTED_OUTPUT: "작성자 출력 진술 · 미검수",
    SELECTABLE_LIMIT: "선택 가능 상한 · 출력 확인 아님",
    SELECTABLE_LABEL: "선택 가능 표기 · 출력 확인 아님",
    SELECTED_SETTING: "선택 설정 · 전송 확인 아님",
    UNKNOWN: "기준 미상",
  };
  const sequences = {
    UNORDERED: "표현 순서이며 실제 전후는 미상",
    RECONSTRUCTED_PARTIAL: "일부 앞뒤만 재구성",
    REPORTED_SEQUENCE: "작성자가 보고한 순서",
  };
  const grid = document.querySelector("#review-grid");
  const search = document.querySelector("#review-search");
  const feature = document.querySelector("#review-feature");
  const dialog = document.querySelector("#review-dialog");
  const body = document.querySelector("#review-detail-body");
  const count = document.querySelector("#review-count");
  let records = [],
    activeId = null,
    returnId = null,
    openedFromList = false;

  function safeUrl(raw) {
    try {
      const u = new URL(raw);
      return u.protocol === "https:" &&
        !u.username &&
        !u.password &&
        u.hostname.includes(".") &&
        /[a-z]/i.test(u.hostname) &&
        !/\.(local|internal)$/i.test(u.hostname)
        ? u.href
        : null;
    } catch {
      return null;
    }
  }
  function badge(text, type = "") {
    return `<span class="review-chip ${type}">${esc(text)}</span>`;
  }
  function status(result) {
    return badge(
      labels[result.status] || unknown,
      result.status === "UNKNOWN"
        ? "unknown"
        : result.status === "NORMAL"
          ? ""
          : "problem",
    );
  }
  function dl(items) {
    return `<dl class="review-dl">${items.map(([a, b]) => `<dt>${esc(a)}</dt><dd>${esc(b)}</dd>`).join("")}</dl>`;
  }
  function refs(items) {
    return `<small>근거: ${esc(items.join(", ") || "정보 없음")}</small>`;
  }
  function known(r, key) {
    return r.functionalObservations.some((d) =>
      key === "signal_mode"
        ? [
            d.signal_mode.resolution_pixels,
            d.signal_mode.resolution_label,
            d.signal_mode.hz,
          ].some((x) => x !== "UNKNOWN")
        : key === "ui_scale"
          ? d.ui_scale.value !== "UNKNOWN"
          : key === "pd"
            ? d.pd.recognized !== "UNKNOWN"
            : d[key].status !== "UNKNOWN",
    );
  }
  function dataValid(data) {
    try {
      return dataShapeValid(data);
    } catch {
      return false;
    }
  }
  function dataShapeValid(data) {
    if (
      !data ||
      data.version !== "review-ui-1" ||
      data.recordStatus !== "REVIEW_ONLY" ||
      data.publicStatus !== "UNKNOWN" ||
      data.approvedGold !== 0 ||
      !Array.isArray(data.records) ||
      data.records.length !== 18
    )
      return false;
    const ids = new Set();
    for (const r of data.records) {
      if (
        !r ||
        !/^PUR-\d{3}$/.test(r.id) ||
        ids.has(r.id) ||
        r.grade !== "C" ||
        r.publicStatus !== "UNKNOWN" ||
        r.basis !== "USER_REPORT" ||
        r.reviewStatus !== "NEEDS_REVIEW" ||
        !r.source ||
        !safeUrl(r.source.source_url)
      )
        return false;
      ids.add(r.id);
      for (const key of [
        "nodes",
        "ports",
        "configurations",
        "observations",
        "functionalObservations",
        "evidence",
        "evidenceRoles",
        "attempts",
        "unscopedStatements",
        "missing",
      ])
        if (!Array.isArray(r[key])) return false;
      for (const key of [
        "nodes",
        "ports",
        "configurations",
        "observations",
        "evidence",
        "evidenceRoles",
        "attempts",
        "unscopedStatements",
      ]) {
        if (!r[key].every((item) => item && typeof item === "object"))
          return false;
      }
      if (
        !r.nodes.every(
          (n) =>
            typeof n.id === "string" &&
            typeof n.display_model === "string" &&
            Object.hasOwn(kinds, n.kind),
        )
      )
        return false;
      if (
        !r.goal ||
        !r.environment ||
        !r.commercial ||
        r.functionalObservations.length !== r.observations.length
      )
        return false;
      for (const d of r.functionalObservations) {
        if (!r.observations.some((o) => o.id === d.observation_id))
          return false;
        for (const key of Object.keys(domains))
          if (!d[key] || !Array.isArray(d[key].evidence_refs)) return false;
        for (const key of [
          "video_output",
          "clamshell",
          "sleep_wake",
          "reconnect",
        ])
          if (!Object.hasOwn(labels, d[key].status)) return false;
        if (
          typeof d.signal_mode.hz !== "string" ||
          typeof d.signal_mode.resolution_pixels !== "string" ||
          typeof d.ui_scale.value !== "string" ||
          !["YES", "NO", "UNKNOWN"].includes(d.pd.recognized)
        )
          return false;
      }
    }
    return Array.from(
      { length: 18 },
      (_, i) => `PUR-${String(i + 1).padStart(3, "0")}`,
    ).every((id) => ids.has(id));
  }
  function renderList() {
    const q = search.value.trim().toLowerCase();
    const selected = feature.value;
    const matches = records.filter(
      (r) =>
        [
          r.id,
          r.title,
          ...r.nodes.map((n) => n.display_model),
          ...r.observations.map((o) => o.summary),
          ...r.configurations.map((c) => c.notes),
        ]
          .join(" ")
          .toLowerCase()
          .includes(q) &&
        (selected === "ALL" || known(r, selected)),
    );
    grid.innerHTML = matches
      .map((r) => {
        const host = r.nodes.find((n) => n.id === "src");
        const tags = Object.keys(domains)
          .filter((key) => known(r, key))
          .map((key) => badge(`${domains[key]} 진술`))
          .join("");
        return `<a class="story-card review-card" data-review-id="${esc(r.id)}" href="#${esc(r.id)}" aria-label="${esc(r.id)} ${esc(r.title)} 상세 보기"><div class="story-meta"><span class="review-card-id">${esc(r.id)}</span>${badge("C · 검토 전용", "unknown")}</div><h3>${esc(r.title)}</h3><p>${esc(value(host?.display_model))} · OS ${esc(value(r.environment.os_name))}</p><div class="review-card-tags">${tags || badge("기능별 결과 미확인", "unknown")}</div><p>작성자 진술 · 사람 검토 대기<br>누락·범위 미상 정보는 UNKNOWN 유지</p><div class="story-footer"><span>${esc(r.source.site_name)} · 확인 ${esc(r.source.checked_at)}</span><span aria-hidden="true">↗</span></div></a>`;
      })
      .join("");
    document.querySelector("#review-empty").hidden = matches.length !== 0;
    count.textContent = `전체 18건 중 ${matches.length}건 표시 · 호환성 판정 집계 아님`;
  }
  function renderFunction(d) {
    const sm = d.signal_mode;
    const actualHz =
      sm.hz_basis === "REPORTED_OUTPUT"
        ? `${sm.hz}Hz · 작성자 보고, 실측 미검수`
        : unknown;
    const signal = `<article class="review-function" data-function="signal_mode"><h5>신호 해상도·주사율</h5><p>실제 신호 픽셀: ${esc(value(sm.resolution_pixels))}</p><p>출력 Hz 진술: ${esc(actualHz)}</p><p>해상도 표기: ${esc(value(sm.resolution_label))}${sm.resolution_label !== "UNKNOWN" ? `<br><small>${esc(modeBasis[sm.label_basis])}</small>` : ""}</p>${sm.hz !== "UNKNOWN" ? `<p>Hz 표기: ${esc(sm.hz)}Hz<br><small>${esc(modeBasis[sm.hz_basis])}</small></p>` : ""}<small>4K/FHD 표기를 픽셀로 변환하지 않습니다.</small>${refs(sm.evidence_refs)}</article>`;
    const ui = `<article class="review-function" data-function="ui_scale"><h5>UI 배율·작업 공간</h5><p>${esc(value(d.ui_scale.value))}</p><small>전송 신호의 해상도와 구분합니다.</small>${refs(d.ui_scale.evidence_refs)}</article>`;
    const pd = `<article class="review-function" data-function="pd"><h5>충전 인식·전력</h5>${badge(d.pd.recognized === "YES" ? "충전 사용 보고 · 검토 대기" : d.pd.recognized === "NO" ? "충전 문제 보고 · 검토 대기" : unknown, d.pd.recognized === "UNKNOWN" ? "unknown" : "")}<p>실제 수전 와트: ${esc(value(d.pd.watts))}</p><small>충전 진술이 PD 프로파일·협상 확인을 뜻하지 않습니다.</small>${refs(d.pd.evidence_refs)}</article>`;
    const result = (key) =>
      `<article class="review-function" data-function="${esc(key)}"><h5>${esc(domains[key])}</h5>${status(d[key])}${refs(d[key].evidence_refs)}</article>`;
    return `<div class="review-functions">${result("video_output")}${signal}${ui}${pd}${result("clamshell")}${result("sleep_wake")}${result("reconnect")}</div>`;
  }
  function renderDetail(r) {
    const nodes = Object.fromEntries(r.nodes.map((n) => [n.id, n]));
    const ports = Object.fromEntries(r.ports.map((p) => [p.id, p]));
    const eRoles = Object.fromEntries(
      r.evidenceRoles.map((e) => [e.evidence_id, e]),
    );
    const evidence = Object.fromEntries(r.evidence.map((e) => [e.id, e]));
    const sourceLink = safeUrl(r.source.source_url);
    const source = `<section class="review-detail-section"><h3>출처와 검토 상태</h3><div class="review-evidence-line">${badge("사용자 진술 · C등급")}${badge("검토 대기", "unknown")}${badge("공개 UNKNOWN", "unknown")}</div>${dl(
      [
        ["출처", r.source.site_name],
        ["게시일", r.source.published_at],
        ["원문 확인일", r.source.checked_at + " · 기존 조사 이력"],
        ["공식 사양 대조", "미실행"],
        ["독립 실물 검증", "미실행"],
        ["사람 승인 골든", "0/30 · 이 사례가 승인됐다는 뜻이 아님"],
      ],
    )}${sourceLink ? `<a class="review-source-link" href="${esc(sourceLink)}" target="_blank" rel="noopener noreferrer" referrerpolicy="no-referrer">공개 원문 열기 ↗</a>` : "<p>출처 링크 정보 없음</p>"}${r.semanticReview ? `<p class="review-section-note" data-semantic-review>AI 의미 검수 · ${esc(r.semanticReview.checked_at)} · ${r.semanticReview.status === "AI_CORRECTED" ? "교정" : r.semanticReview.status === "AI_MATCHED" ? "일치" : "재확인 불가"}<br>${esc(r.semanticReview.notes)}<br>사람 승인·공식 사양 대조·실물 검증은 아닙니다.</p>` : `<p class="review-section-note">기존 공개 조사 요약을 재구조화했습니다. 새 원문 확인이나 공식 호환 승인은 아닙니다.</p>`}</section>`;
    const devices = `<section class="review-detail-section"><h3>게시물에 등장한 기기</h3><p class="review-section-note">아래 기기가 모든 관측에서 사용됐다는 뜻은 아닙니다. 각 구성의 소스와 경로를 따로 확인하세요.</p><div class="review-node-grid">${r.nodes.map((n) => `<article class="review-node"><h4>${esc(kinds[n.kind])} · ${esc(n.id)}</h4><p>${esc(value(n.display_model))}</p>${n.kind === "SOURCE" ? `<p>칩: ${esc(value(n.chip))}</p>` : ""}<p>정규화 모델: ${esc(value(n.normalized_model))}</p><p>식별: ${n.identity_certainty === "UNKNOWN" ? "정보 없음" : "표시명 일부만 확인 · 최종 식별 대기"}</p>${n.kind === "CABLE" ? `<p>실물 SKU·길이: ${esc(unknown)}</p>` : ""}<p class="review-section-note">${esc(n.notes || "추가 기기 정보 없음")}</p></article>`).join("")}</div></section>`;
    const configs = `<section class="review-detail-section"><h3>구성과 연결 구간</h3><p class="review-section-note">단자 이름은 규격 지원 보장이 아닙니다. 경로 내 포트 역할만 표시하며 실물 위치·미상 구간은 추정하지 않습니다.</p>${r.configurations
      .map(
        (c) =>
          `<article class="review-config"><h4>${badge(configRoles[c.role], c.role === "OBSERVED" ? "" : "advice")} ${esc(c.id)}</h4><p>이 구성의 소스: ${esc(value(c.node_ids.map((id) => nodes[id]).find((n) => n.kind === "SOURCE")?.display_model))}</p>${
            c.edges.length
              ? c.edges
                  .map((edge) => {
                    const a = ports[edge.from_port],
                      b = ports[edge.to_port];
                    return `<div class="review-edge"><span>${esc(value(nodes[a.node_id].display_model))} / ${esc(connectors[a.connector])}</span><span aria-hidden="true">→</span><span>${esc(value(nodes[b.node_id].display_model))} / ${esc(connectors[b.connector])}</span>${badge(edge.purpose === "POWER" ? "전원 경로" : "영상 경로", "unknown")}${edge.path_status === "UNKNOWN_GAP" ? badge("연결 구간 미상", "problem") : ""}</div>`;
                  })
                  .join("")
              : `<p>${esc(unknown)} · 실제 연결을 확인한 경로가 아닙니다.</p>`
          }${dl(c.settings.map((s) => [settingLabels[s.key] || s.key, settingValues[s.value] || value(s.value)]))}<p class="review-section-note">${esc(c.notes || "추가 구성 정보 없음")}</p>${refs(c.evidence_refs)}</article>`,
      )
      .join("")}</section>`;
    const observations = `<section class="review-detail-section"><h3>작성자의 관측 · 기능별 분리</h3><p class="review-section-note">한 기능의 정상 보고를 다른 기능이나 전체 목표 달성으로 확대하지 않습니다.</p>${r.observations
      .map((o) => {
        const d = r.functionalObservations.find(
          (d) => d.observation_id === o.id,
        );
        return `<article class="review-observation" data-observation="${esc(o.id)}"><h4>관측 ${o.sequence} · ${esc(o.id)} / ${esc(o.configuration_id)}</h4><p class="review-section-note">${esc(sequences[o.sequence_basis])}</p><p>${esc(o.summary)}</p>${o.durability !== "UNKNOWN" ? `<p class="review-durability">${esc({ TEMPORARY: "일시 효과 · 영구 해결 아님", RECURRENT: "재발 · 이전 정상 관측 " + o.recurrence_of, NO_RECURRENCE_REPORTED: "재발 없이 사용했다는 진술 · 기간·조건 추가 검수 필요" }[o.durability])}</p>` : ""}${renderFunction(d)}${d.other_notes !== "UNKNOWN" ? `<p>기타 진술: ${esc(d.other_notes)}</p>` : ""}${dl(
          [
            ["연결된 물리 화면", value(o.counts.connected)],
            ["실제 점등 화면", value(o.counts.lit)],
            ["독립 확장 화면", value(o.counts.independent_extended)],
            ["복제 그룹 전체 화면", value(o.counts.mirrored)],
            [
              "내장 화면 포함 범위",
              {
                EXTERNAL_ONLY: "외장만",
                INCLUDING_INTERNAL: "내장 포함",
                UNKNOWN: unknown,
              }[o.counts.scope],
            ],
            [
              "내장 화면 점등",
              { YES: "보고됨", NO: "꺼짐 보고", UNKNOWN: unknown }[
                o.counts.internal_screen_lit
              ],
            ],
          ],
        )}${o.display_states.some((s) => s.output_mode === "DISPLAYLINK") ? `<p>${badge("DisplayLink 사용 보고 · 네이티브 출력 아님", "advice")}</p>` : ""}</article>`;
      })
      .join("")}</section>`;
    const changes = `<section class="review-detail-section"><h3>목표·실제 수행·조언</h3><h4>목표</h4><p>${esc(r.goal.summary)}</p><h4>관측과 연결된 실제 수행</h4>${r.attempts.length ? `<ul>${r.attempts.map((a) => `<li>${esc(a.action)}<br><span class="review-section-note">${esc(a.configuration_id)} · ${esc(a.observation_ids.join(", "))} · ${esc(sequences[a.sequence_basis])}</span></li>`).join("")}</ul>` : "<p>관측과 연결할 수 있는 수행 시도 정보 없음. 수행하지 않았다는 뜻은 아닙니다.</p>"}<h4>관측으로 합치지 않은 진술</h4>${
      r.unscopedStatements.length
        ? r.unscopedStatements
            .map((s) => {
              const e = evidence[s.evidence_id],
                a = eRoles[s.evidence_id];
              return `<div class="review-node">${badge(roles[a.statement_role], "advice")}<p>${esc(e.summary)}</p><p class="review-section-note">${esc(s.notes)}</p></div>`;
            })
            .join("")
        : "<p>별도로 남긴 진술 없음.</p>"
    }</section>`;
    const commercial = `<section class="review-detail-section"><h3>상업성·남은 결측</h3>${dl(
      [
        ["판매 링크", value(r.commercial.sales_links)],
        ["제휴 링크", value(r.commercial.affiliate_links)],
        ["광고성", value(r.commercial.advertising)],
        ["포함 사유", r.commercial.inclusion_basis],
      ],
    )}<p>${esc(r.commercial.notes || "상업성 추가 정보 없음")}</p><p class="review-section-note">UNKNOWN은 광고가 없다는 뜻이 아닙니다. 판매·제휴 링크 자체는 이 화면에 넣지 않습니다.</p><ul>${r.missing.map((x) => `<li>${esc(x)}</li>`).join("")}</ul></section>`;
    const evidenceSection = `<section class="review-detail-section"><h3>근거 위치와 진술 역할</h3><p class="review-section-note">원문·작성자 후속 댓글·타인의 조언을 구분합니다. DIRECT_CHECK는 원문 확인입니다. 기존 조사 근거와 AI 재확인 근거는 각 위치·검수 메모로 구분하며 실물 재현이 아닙니다.</p>${r.evidence
      .map((e) => {
        const a = eRoles[e.id];
        return `<details class="review-evidence"><summary>${esc(e.id)} · ${esc(roles[a.statement_role])}</summary><p>${esc(e.summary)}</p>${dl(
          [
            [
              "작성 주체",
              e.actor === "CASE_AUTHOR" ? "사례 작성자" : "다른 사람",
            ],
            [
              "원문 종류",
              {
                ORIGINAL_POST: "원글",
                AUTHOR_COMMENT: "작성자 후속 댓글",
                OTHER_COMMENT: "타인 댓글",
                EDITED_POST: "수정 본문",
              }[e.kind],
            ],
            ["근거 위치", e.location],
            ["확인일", e.checked_at],
            ["근거 성격", "사용자 진술 · 공식 사양/독립 실물 검증 아님"],
            [
              "기능 범위",
              a.domains.map((x) => evidenceDomains[x]).join(", ") ||
                "실제 결과 근거로 사용하지 않음",
            ],
          ],
        )}</details>`;
      })
      .join("")}</section>`;
    body.innerHTML = `<h2 id="review-detail-title">${esc(r.title)}</h2><div class="review-banner"><strong>사용자 진술 · 검토 전용</strong><p>전체 호환성은 UNKNOWN입니다. 정보가 존재하는 것과 검수가 완료된 것은 다릅니다.</p></div>${source}${devices}${configs}${observations}${changes}${commercial}${evidenceSection}`;
    document.querySelector("#review-detail-id").textContent =
      r.id + " / REVIEW NOTE";
  }
  function route() {
    const id = location.hash.slice(1);
    if (!id || id === "review-filters") {
      activeId = null;
      if (dialog.open) dialog.close();
      return;
    }
    const r = records.find((r) => r.id === id);
    if (!r) {
      history.replaceState(null, "", location.pathname + location.search);
      count.textContent =
        "요청한 사례 ID가 없습니다. 전체 목록에서 다시 선택해 주세요.";
      if (dialog.open) dialog.close();
      return;
    }
    if (activeId === id && dialog.open) return;
    activeId = id;
    try {
      renderDetail(r);
    } catch {
      body.innerHTML =
        '<h2 id="review-detail-title">상세 자료를 표시하지 못했습니다.</h2><p>목록으로 돌아가 다시 열어 주세요. 다른 자료로 대체하지 않습니다.</p>';
    }
    if (!dialog.open) dialog.showModal();
    dialog.scrollTop = 0;
  }
  function closeDetail() {
    if (openedFromList && activeId) history.back();
    else {
      history.replaceState(null, "", location.pathname + location.search);
      route();
    }
  }
  document
    .querySelector("#review-retry")
    .addEventListener("click", () => location.reload());
  if (!dataValid(window.CONNECTABLE_REVIEW_DATA)) {
    document.querySelector("#review-data-error").hidden = false;
    count.textContent = "검토 자료 오류 · 사례 수 미확인";
    search.disabled = true;
    feature.disabled = true;
    document.querySelector("#review-reset").disabled = true;
    return;
  }
  records = window.CONNECTABLE_REVIEW_DATA.records;
  document
    .querySelector("#review-filters")
    .addEventListener("submit", (event) => event.preventDefault());
  search.addEventListener("input", renderList);
  feature.addEventListener("change", renderList);
  document.querySelector("#review-reset").addEventListener("click", (event) => {
    event.preventDefault();
    search.value = "";
    feature.value = "ALL";
    renderList();
    search.focus();
  });
  grid.addEventListener("click", (event) => {
    const card = event.target.closest("[data-review-id]");
    if (
      !card ||
      event.metaKey ||
      event.ctrlKey ||
      event.shiftKey ||
      event.altKey
    )
      return;
    event.preventDefault();
    returnId = card.dataset.reviewId;
    openedFromList = true;
    history.pushState(null, "", `#${returnId}`);
    route();
  });
  document
    .querySelector("#review-close")
    .addEventListener("click", closeDetail);
  dialog.addEventListener("cancel", (event) => {
    event.preventDefault();
    closeDetail();
  });
  dialog.addEventListener("close", () => {
    const card = Array.from(grid.querySelectorAll("[data-review-id]")).find(
      (c) => c.dataset.reviewId === returnId,
    );
    (card || search).focus();
    activeId = null;
    openedFromList = false;
  });
  window.addEventListener("popstate", route);
  window.addEventListener("hashchange", route);
  renderList();
  route();
})();
