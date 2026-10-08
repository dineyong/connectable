"use strict";
const records = window.CONNECTABLE_CASES || [];
let lastCard = null;
const safeUrl = (value) => {
  try {
    const u = new URL(value);
    return u.protocol === "https:" ? u.href : null;
  } catch {
    return null;
  }
};
const labels = {
  SUCCESS: "성공",
  LIMITED_SUCCESS: "제한적 성공",
  UNRESOLVED: "미해결",
  UNKNOWN: "결과 미확인",
  FAILURE: "최종 실패",
};
const esc = (value) =>
  String(value ?? "").replace(
    /[&<>"']/g,
    (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[
        c
      ],
  );
const grid = document.querySelector("#story-grid");
let filter = "ALL",
  query = "",
  limit = 6;
function renderCases() {
  const matches = records.filter(
    (r) =>
      (filter === "ALL" || r.outcome === filter) &&
      [r.title, r.goal, r.summary, r.sourceModel]
        .join(" ")
        .toLowerCase()
        .includes(query),
  );
  grid.innerHTML = matches
    .slice(0, limit)
    .map(
      (r) =>
        `<button class="story-card" data-id="${esc(r.id)}" aria-label="${esc(r.title)} 상세 보기"><div class="story-meta"><span class="outcome-tag ${r.outcome === "LIMITED_SUCCESS" ? "limited" : r.outcome === "SUCCESS" ? "" : "open"}">${labels[r.outcome]}</span><span>${esc(r.id)}</span></div><h3>${esc(r.title)}</h3><p>${esc(r.summary)}</p><div class="story-footer"><span>${esc(r.site)} · 사용자 관측</span><span>↗</span></div></button>`,
    )
    .join("");
  document.querySelector("#empty-search").hidden = matches.length > 0;
  document.querySelector("#search-count").textContent =
    `일치하는 사례 ${matches.length}건 · ${Math.min(limit, matches.length)}건 표시`;
  if (!window.CONNECTABLE_CASES)
    document.querySelector("#empty-search").textContent =
      "사례 자료를 불러오지 못했습니다. 페이지를 새로고침해 주세요.";
  document.querySelector("#show-more").hidden = matches.length <= limit;
}
document.querySelector("#total-count").textContent = records.length;
document.querySelectorAll("[data-filter]").forEach((button) =>
  button.addEventListener("click", () => {
    filter = button.dataset.filter;
    limit = 6;
    document.querySelectorAll("[data-filter]").forEach((b) => {
      b.classList.toggle("active", b === button);
      b.setAttribute("aria-pressed", String(b === button));
    });
    renderCases();
  }),
);
document.querySelector("#case-search").addEventListener("input", (e) => {
  query = e.target.value.trim().toLowerCase();
  limit = 6;
  renderCases();
});
document.querySelector("#show-more").addEventListener("click", () => {
  limit += 6;
  renderCases();
});
const dialog = document.querySelector("#case-dialog");
grid.addEventListener("click", (e) => {
  const card = e.target.closest("[data-id]");
  if (!card) return;
  const r = records.find((r) => r.id === card.dataset.id);
  lastCard = card;
  document.querySelector("#dialog-id").textContent = `${r.id} / FIELD NOTE`;
  document.querySelector("#dialog-body").innerHTML =
    `<h2 id="dialog-title">${esc(r.title)}</h2><span class="outcome-tag">${labels[r.outcome]} · 사용자 보고</span><h3>원했던 구성</h3><p>${esc(r.goal)}</p><h3>작성자가 보고한 결과</h3><p>${esc(r.summary)}</p><h3>관측 내용</h3><ul>${r.observations.map((o) => `<li>${esc(o)}</li>`).join("")}</ul><h3>남은 미확인 조건</h3><p>${esc(r.notes)}</p><p class="dialog-warning">단일 공개 사례(C등급)이며 공식 사양 대조와 검수 전입니다. 이 사례를 다른 구성의 호환성 보장으로 사용할 수 없습니다.</p><a class="source-link" href="${esc(safeUrl(r.url) || "#")}" target="_blank" rel="noopener noreferrer">공개 원문 확인 ↗</a><p class="source-date">출처: ${esc(r.site)} · 확인일: ${esc(r.checked)}</p>`;
  dialog.showModal();
});
dialog.addEventListener("close", () => lastCard?.focus());
document
  .querySelector("#close-dialog")
  .addEventListener("click", () => dialog.close());
dialog.addEventListener("click", (e) => {
  if (e.target === dialog) {
    const rect = dialog.getBoundingClientRect();
    if (
      e.clientX < rect.left ||
      e.clientX > rect.right ||
      e.clientY < rect.top ||
      e.clientY > rect.bottom
    )
      dialog.close();
  }
});
document.querySelector("#connection-form").addEventListener("submit", (e) => {
  e.preventDefault();
  const source = document.querySelector("#source"),
    chip = document.querySelector("#chip"),
    connection = document.querySelector("#connection");
  const missing = [source, chip, connection].filter((x) => !x.value);
  [source, chip, connection].forEach((x) => {
    x.setAttribute("aria-invalid", String(!x.value));
    x.setAttribute("aria-describedby", "form-error");
  });
  const error = document.querySelector("#form-error");
  if (missing.length) {
    error.textContent =
      "맥북 모델, 칩, 연결 방식을 선택해 주세요. 모르는 항목은 미상 옵션을 선택할 수 있습니다.";
    missing[0].focus();
    return;
  }
  error.textContent = "";
  const count = document.querySelector("#count").value,
    display =
      document.querySelector("#display").value.trim() || "모니터 모델 미상";
  const charge = document.querySelector("#charging").checked;
  const checks = [
    [
      "소스 기기 출력 조건",
      `${source.value} · ${chip.value}의 공식 모델별 외장 출력 수·동시 조건 확인 필요`,
    ],
    [
      "디스플레이와 연결 경로",
      `${display} · ${connection.value}의 입력 단자 및 케이블·중간 장치 규격 확인 필요`,
    ],
    [
      "목표 화면 성능",
      `${document.querySelector("#resolution").value} · ${document.querySelector("#refresh").value} · 외장 ${count === "3" ? "3대 이상" : count + "대"}의 동시 지원 여부 미확인`,
    ],
    ...(charge
      ? [
          [
            "충전 조건",
            "소스와 모니터·독의 PD 지원 및 전력, 영상 동시 사용 조건 확인 필요",
          ],
        ]
      : []),
  ];
  document.querySelector("#result").innerHTML =
    `<div class="result-header"><span>CONNECTION OVERVIEW</span><span class="status-dot"></span></div><div class="result-filled"><span class="result-badge">아직 확인되지 않은 구성</span><h3>연결 조건을<br>정리했어요.</h3><p>선택한 구성의 공식 사양 자료가 아직 연결되지 않아 최대 성능과 연결 가능 여부는 미확인입니다.</p>${checks.map(([t, d]) => `<div class="check-item"><span>○</span><div><strong>${esc(t)}</strong><small>${esc(d)}</small></div></div>`).join("")}</div><div class="result-note"><span>ⓘ</span><p>화면 목업의 확인 항목입니다. 실제 호환 판정·추천·제품 지원 사양을 의미하지 않습니다.</p></div>`;
  if (window.matchMedia("(max-width:640px)").matches)
    document
      .querySelector("#result")
      .scrollIntoView({
        behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches
          ? "auto"
          : "smooth",
        block: "start",
      });
});
renderCases();

// A changed input invalidates the previous summary; never present stale conditions.
document.querySelector("#connection-form").addEventListener("input", () => {
  document.querySelector("#form-error").textContent = "";
  document
    .querySelectorAll("[aria-invalid]")
    .forEach((x) => x.removeAttribute("aria-invalid"));
  if (document.querySelector(".result-filled"))
    document.querySelector("#result").innerHTML =
      '<div class="result-empty"><h3>구성이 변경됐어요.</h3><p>확인 버튼을 눌러 새 구성의 조건을 다시 정리해 주세요.</p></div>';
});

document.querySelector("#corpus-count").textContent = records.length;
