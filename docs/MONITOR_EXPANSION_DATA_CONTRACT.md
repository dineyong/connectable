# 모니터 확대 조사 데이터 계약

기준일: 2026-10-10. 이 계약은 격리된 조사 배치용이다. 기존 official catalog·typed capability·호환성 판정 계약을 대체하지 않는다. 기준 원본은 `data/research/monitor-expansion/`의 세 JSON이다. 검증기는 [validate_monitor_expansion.py](../scripts/validate_monitor_expansion.py), 회귀 테스트는 [test_monitor_expansion.py](../tests/test_monitor_expansion.py)다.

## 공통

`schema_version=1`, `checked_on=YYYY-MM-DD`, `public_status=UNKNOWN`을 유지한다. URL은 공개 HTTPS이며 자격증명·비정상 포트·제어문자·위험 인코딩을 거부한다. JSON 중복 키·NaN·Infinity를 거부한다. 날짜·ID 중복·참조·enum·개인정보 패턴을 검사한다. 검사 통과는 사실의 사람 승인이나 공개 권리 검토 완료가 아니다.

## 공식 사양

[official_specs.json](../data/research/monitor-expansion/official_specs.json)의 `products` 각 객체는 id, manufacturer, display_model, region, variant_status, source_refs, facts, missing_fields, notes를 갖는다. 제품 ID는 `monitor:`와 영문 소문자 slug다. `variant_status`는 UNKNOWN 또는 EXACT_DOCUMENT_MODEL이며 공식 문서 모델 식별과 한국 판매 SKU 동일성은 별개다.

source_refs에는 id, url, title, checked_on, access_status=DIRECT_CHECK, location을 저장한다. 제조사별 정확한 공개 호스트 목록만 허용한다. 새 호스트는 수동 범위 검토 후 추가한다. 도메인 검사는 문서의 특정 모델 내용이나 실시간 리다이렉트까지 보증하지 않는다.

facts는 id, property, value, unit, scope, source_refs, location, qualifier다. value는 공식 문서의 숫자·문자열·배열·객체를 보존하며 공통 계산용 typed payload가 아니다. qualifier는 MANUFACTURER_STATED, UP_TO, RATED, UNKNOWN이다. typical/native를 RATED로 치환하지 않는다. 제조사 estimated 표기는 객체·scope·notes에 남긴다. unit은 모르면 null이다. 포트/입력·조건/동시성·지역을 scope와 location에 기록하고 다른 지역의 값으로 결측을 덮지 않는다. missing_fields는 확인하지 못한 항목, notes는 제한과 충돌이다.

## 커뮤니티

[community_reviews.json](../data/research/monitor-expansion/community_reviews.json)의 reviews는 id, manufacturer, display_model, url, site, checked_on, origin, record_type, sentiment, summary, positives, limitations, usage_conditions, commercial_context, review_status, usable_for_compatibility를 저장한다.

origin: DIRECT_CHECK/EXISTING_RESEARCH. record_type: FIRST_HAND_REVIEW/PROBLEM_REPORT/QUESTION/RECOMMENDATION. sentiment: POSITIVE/MIXED/NEGATIVE/UNKNOWN. commercial_context: PRESENT/NOT_OBSERVED/UNKNOWN. NOT_OBSERVED는 비협찬 인증이 아니다. 검토 PENDING_HUMAN_REVIEW, 호환성 사용 NO를 유지한다.

classifications는 display_model, label, review_refs, rationale다. label은 POSITIVE_REVIEW_CANDIDATE/MIXED_REPORTS/INSUFFICIENT_EVIDENCE다. 긍정 후보는 같은 표시 모델의 긍정 본인 사용 원문 2개 이상을 요구한다. 이는 독립 사용자 2명·추천 순위·품질 인증을 뜻하지 않는다. 지역 접미사와 하드웨어 리비전을 자동 동일시하지 않는다. excluded_sources에는 url/reason을 기록한다. 본문 전문·작성자명·사진·개인정보는 복제하지 않는다.

## 검색·구매 신호

[market_signals.json](../data/research/monitor-expansion/market_signals.json)의 signals는 id, display_model, platform, url, checked_on, metric, value, unit, period, scope, source_kind=DIRECT_CHECK, is_proxy, limitations다. metric은 SEARCH_VOLUME/SALES_COUNT/PLATFORM_RANK/REVIEW_COUNT/SEARCH_INTEREST_INDEX다. 실제로 확보한 유한 비음수 수치만 signal로 넣는다. 미확보 항목은 0으로 만들지 않는다.

검색지수·리뷰수·플랫폼 순위는 is_proxy=true다. 검색 자료로 PURCHASE_INTEREST_CANDIDATE를 만들 수 없다. classifications는 모델/label/signal_refs/rationale, label은 SEARCH_INTEREST_CANDIDATE/PURCHASE_INTEREST_CANDIDATE/INSUFFICIENT_PUBLIC_DATA다. 후보는 검토 큐이며 인기 확정이 아니다. access_attempts에는 url/status/reason을 기록한다.

네이버 데이터랩은 배치별 정규화된 상대값이다. scope·period·limitations에 정확 검색어, 조회 기간, 기기/성별/연령, 정규화 배치를 보존한다. 서로 다른 조회 배치의 수치를 순위로 합치지 않는다. 광고 정렬·옵션 통합 리뷰·검색 결과 순번을 실제 판매량으로 변환하지 않는다.

## 화면 연결 전 남은 계약

공통 단위 변환, 속성 enum, 입력별 최대/동시 조건, 필드별 검토 상태, 정확 SKU 연결을 별도 설계해야 한다. 이 배치의 generic facts를 기존 필터에 바로 넣지 않는다. 원본 근거·후기·시장 지표는 독립 계층으로 유지한다.
