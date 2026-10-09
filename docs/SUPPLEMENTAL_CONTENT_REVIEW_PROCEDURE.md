# 보충 공식 근거의 수동 편집 검토 절차

이 절차는 원본 fact에 새 값을 자동 적용하지 않는 보충 근거 검토다. 기존 [원본 검토 절차](CONTENT_REVIEW_PROCEDURE.md)와 공개 UNKNOWN 정책은 유지한다.

## 기준 파일과 범위

- [보충 검토 스키마](../schemas/supplemental-content-review.schema.json).
- [보충 검토 ledger](../data/review/supplemental_content_reviews.json): 실제 records 0건.
- [검증기](../scripts/supplemental_content_review.py): `python3 scripts/supplemental_content_review.py`.
- 현재 허용 대상은 [27ULD950 배치](../data/official/crossover_pd_followup_2026-10-09.json) 하나다. 다른 제품·근거는 계약을 별도 검토해야 한다.

원본 fact만 검토하는 기존 ledger에 새 assertion을 넣지 않는다. 새 ledger는 대상 배치 전체와 assertion, 관련 원본 fact, 캡처의 해시를 함께 고정한다. 어느 하나가 바뀌면 기존 검토를 재사용할 수 없다. JSON hash는 정렬 키·UTF-8·공백 없는 JSON 기준 `scripts.validate_official_spec_review.digest`이며 파일 바이트 해시와 다르다. 캡처만 파일 바이트 해시다.

## 실제 검토 후 작성할 필드

| 필드 | 의미·요건 |
|---|---|
| id | `supp-review:<고유 식별자>`, 중복 금지 |
| target_batch_id / target_assertion_id | 체크리스트의 정확한 보충 대상 |
| evidence_batch_sha256 | 보충 batch 전체의 정렬 JSON SHA-256 |
| related_fact_sha256 / capture_sha256 | 원본 fact와 발췌 이미지 바인딩 |
| reviewer_id | 담당자가 사용하는 `reviewer:<가명>`; 실명·이메일·커뮤니티 닉네임 저장 금지 |
| reviewed_on | 담당자가 실제 검토한 ISO 날짜; 근거 확인 이전 날짜 금지 |
| result | NEEDS_REVIEW / PARTIALLY_VERIFIED / EVIDENCE_SUFFICIENT / REJECTED |
| evidence_refs | 정확한 `CROSS-PD-PAGE`와 `CROSS-PD-IMAGE`, 둘 다 필요 |
| reviewed_fields | 직접 확인한 mode / watts / rating_basis의 부분집합; 미확인 포트 포함 금지 |
| remaining_unknowns | interface / power_qualifier / pd_profiles / simultaneous_budget / sku_revision / actual_host_power 모두 유지 |
| notes | 원문 위치, 확인한 내용, 접근 실패, 남은 조건, 표시 제안에 대한 의견 |
| public_status / usable_for_compatibility | UNKNOWN / NO 고정 |

PARTIALLY_VERIFIED에는 최소 한 필드가 필요하다. EVIDENCE_SUFFICIENT에는 세 필드가 모두 필요하지만 남은 조건은 계속 미확인이다. NEEDS_REVIEW와 REJECTED에도 정확한 대상·근거·이유가 필요하다.

## 기록과 적용의 구분

1. [검토 자료](CROSSOVER_PD_HUMAN_REVIEW_PACKET.md)와 실제 원문을 대조한다. 접근 제한을 우회하지 않는다.
2. 실제 담당자가 결과를 작성한다. AI가 검토자·날짜·승인 결과를 대신 생성하지 않는다. 테스트의 reviewer는 가상 fixture이며 실제 ledger에 복사하지 않는다.
3. 검증기와 전체 테스트를 실행하고 diff를 사람이 확인한다. stale hash·다른 근거·미확인 필드 승인·개인정보·공개 승격을 거부한다.
4. 원본·역사 배치·공개 화면에는 적용하지 않는다. EVIDENCE_SUFFICIENT도 편집 근거 충족 기록일 뿐 화면 적용, 한국 SKU, 호환성 또는 공개 승인이 아니다.
5. 표시 적용은 별도 변경·회귀 검증으로 진행한다. 정책을 임의로 완화하거나 기존 검토 이력을 덮어쓰지 않는다.

## 한계

파일 형식 검증은 실제 사람이 검토했는지, 가명 소유자와 권한이 누구인지 증명하지 못한다. 저장소 리뷰·서명·권한 관리가 필요하다. 문장 진실성, 최신 원문과의 일치, 물리적 충전 결과도 별도 검토 대상이다. 이 단계는 인증·관리자 UI·자동 승인 시스템이 아니다.
