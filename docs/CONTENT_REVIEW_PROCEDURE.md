# 콘텐츠 수동 검토 절차

현재 단계는 검토 기록 준비이며 공개 승인 기능은 없다. 공개 UNKNOWN, 호환성 사용 NO, 원본의 사람 검토 대기 정책을 유지한다.

## 기준 파일

- [검토 기록 Schema](../schemas/content-review.schema.json)
- [검토 기록 원본](../data/review/content_reviews.json): 현재 빈 records. 실제 검토자나 승인 기록을 만들어 넣지 않는다.
- [검토 기록 검증기](../scripts/content_review.py): `python3 -m scripts.content_review`.
- [기존 공식 부분 확인 배치](../data/official/spec_manual_review_2026-10-09.json): 화면 표시 근거. 새 기록으로 과거 배치를 덮어쓰지 않는다.

## 기록 순서

1. 검토할 정확한 fact ID, 연결 제품 모델, 지역, 원본 payload 및 문장을 확인한다.
2. 해당 fact의 공식 source_refs와 공식 문서 위치를 직접 대조한다. 같은 제조사의 다른 모델 문서를 대신 사용하지 않는다. 원문에 접근할 수 없으면 NEEDS_REVIEW로 유지한다.
3. 대상 fact 전체의 SHA-256을 기록한다. 계산은 `scripts.validate_official_spec_review.digest`의 정렬 JSON 기준이다. 값이 바뀌면 이전 검토를 재사용할 수 없다.
4. 검토자가 직접 reviewer_id(예: 조직 내부의 `reviewer:<가명식별자>`), reviewed_on(실제 ISO 날짜), source_refs, notes(문서 위치·확인 범위·결측·지역 적용 범위)를 기록한다. 실명·메일·닉네임을 저장하지 않는다. 가명과 실제 담당자 연결은 공개 저장소 외부에서 관리한다.
5. result는 NEEDS_REVIEW / PARTIALLY_VERIFIED / EVIDENCE_SUFFICIENT / REJECTED 중 하나다. EVIDENCE_SUFFICIENT는 편집 검토의 근거 충족 기록일 뿐, 제품 호환·한국 SKU 승인·공개 승인 상태가 아니다. PARTIALLY_VERIFIED는 notes에 확인한 필드와 남은 필드를 명시하며 화면의 필드 확인 목록을 변경하지 않는다.
6. 검증기·전체 테스트·파생물 최신성 검사를 실행한 뒤 Git diff로 근거와 결과를 사람 검토한다. 빈 검토자·근거·메모, 다른 fact 근거, stale hash, 중복 ID 및 APPROVED/COMPATIBLE/YES 승격은 거부한다.

## 보류와 향후 승인

기록 생성과 실제 검토 완료를 동일시하지 않는다. 사람 검토 사실 자체는 코드로 증명할 수 없으며 담당자의 서명·저장소 리뷰와 권한 관리가 필요하다. 현재 파일 검토 체계는 인증된 관리자 기능이 아니다.

이번 단계에서는 원본/공개 데이터로 승인 기록을 적용하지 않는다. 공개 승인과 자동 배포는 지원하지 않는다. 향후 승인 정책 변경은 별도 결정·스키마·필드별 근거 검증·지역 SKU 검수·권한 관리가 필요하다.

## 표시 원칙

원본 사양 문장을 보존하고 필드별 재확인 정보를 함께 표시한다. 별도 기록이 없으면 재확인 완료라고 하지 않는다. UNKNOWN은 미지원이 아니다. MANUAL_REVIEW/PENDING_HUMAN_REVIEW는 검토 대기이며 호환 판정이 아니다.

정격 RATED와 최대 UP_TO는 동일 숫자여도 서로 대체하지 않는다. LG LV 자료의 UP_TO는 별도 지역 근거로 표시하고 한국 SKU 동일성은 UNKNOWN이다. 크로스오버 PD65 제품명만으로 65W 공급·단자·방향을 확정하거나 공급 기능 필터에 포함하지 않는다. 기능 필터는 자료 탐색이며 제품 적합성 승인이나 추천 순위가 아니다.
