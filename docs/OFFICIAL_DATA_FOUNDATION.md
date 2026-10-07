# 공식 사양 및 판정 데이터 1차 기반

2026-10-08. 사용자가 공식 사양·판정 데이터 구축을 다음 작업으로 선택했다.
질문 21~100번 추가 수집과 공식 데이터 기반 구축을 별도 단계로 진행한다.
이번 산출물은 초기 검수 자료이며 공개 호환 판정 승인이 아니다.

## 기준 파일과 데이터 사전

- [공식 제품 데이터](../data/official/products.json): 별도 기준 원본, version=1.
- [공식 데이터 스키마](../schemas/official-products.schema.json): 추가 필드 금지, 필수값·enum·날짜·URL 검사.
- [검증기](../scripts/validate_official_products.py): 현재 Apple 지원 사양 출처만 허용하는 초기 제한 구현.
- [화면 수 규칙 후보](../scripts/evaluate_display_count_candidate.py): 검수용이며 사이트에 연결하지 않는다.
- [회귀 테스트](../tests/test_official_products.py).

`product_id`는 불변 식별자다. 이름 변경 때 키를 다시 생성하지 않는다.
제조사·표시 모델·모델 번호·연도·칩·지역을 분리한다. KR은 확인한 한국어 사양 문서의 지역이다.
모든 저장 claim에는 source_refs, 원문 섹션 location, 조건이 필요하다.
외장 화면 프로파일은 external_count + resolution_label + refresh_hz를 함께 저장한다.
6K를 임의의 픽셀 수로 변환하지 않는다. 포트 기능 주장은 별도 객체다.
공식 문서 갱신일과 스냅샷은 확인되지 않아 선택 필드를 생략했다.
`missing_fields`는 추가 조사가 필요한 조건이며 미지원이라는 의미가 아니다.
A등급은 출처 등급이다. 최종 사람 검수는 PENDING_HUMAN_REVIEW이며 공개 판정과 구분한다.
현재 두 모델의 GPU 변형을 별도 식별자로 분리하지 않았다. 페이지에 공통으로 명시된 주장만 저장했다.

## 직접 확인한 출처

| 제품 ID | 모델 번호 | 공식 출처 | 확인일 | 저장 범위 |
| --- | --- | --- | --- | --- |
| product:air-m1-2020 | A2337 | [Apple M1 Air 기술 사양](https://support.apple.com/ko-kr/111883) | 2026-10-08 | 비디오 지원, 충전 및 확장, 모델 식별 |
| product:air-m2-2022 | A2681 | [Apple M2 Air 기술 사양](https://support.apple.com/ko-kr/111867) | 2026-10-08 | 디스플레이 지원, 충전 및 확장, 모델 식별 |

공개 원문을 직접 열고 필요한 섹션을 확인했다. 전체 원문과 연락처는 저장하지 않았다.
두 문서 모두 내장 화면과 동시에 외장 1대 최대 6K 60Hz, 충전·DisplayPort 지원 포트 2개를 명시한다.
어댑터 정격을 최소 PD 입력 전력으로 기록하지 않았다. 포트 수를 화면 수로 해석하지 않았다.

## NATIVE-COUNT-001 규칙 후보

입력: 정확한 product_id, output_method, builtin_active, external_independent_count.
출력: status, candidate_status, review_status, rule_id, claim_refs, reason.

- 지원 목록의 모델 + NATIVE + 내장 화면 활성 true에서만 해당 프로파일을 적용한다.
- 요청한 독립 외장 화면 수가 공식 프로파일 수를 초과하면 candidate_status=INCOMPATIBLE.
- public 용도의 status는 모든 경우 UNKNOWN이다. 최종 사람 검수가 필요하다.
- 제한 이내는 긍정 판정하지 않는다. 해상도·주사율·입력 포트·케이블·독·전원을 추가 검수해야 한다.
- DisplayLink, 복제, 내장 화면 비활성/미상, 미식별 모델은 UNKNOWN.
- 정수가 아닌 화면 수, 0 이하 화면 수, 잘못된 공식 데이터는 오류로 거부한다.

이는 화면 수의 필요조건 검사 하나다. 대역폭 계산·MST·DSC·HDR·PD·실사용 교차 검증과 전체 판정 엔진은 미구현이다.
CONFLICT 등 기존 판정 상태를 변경하지 않았다. VERIFIED_COMPATIBLE 생성은 허용하지 않는다.

## 검증 및 보존

```sh
python3 -m unittest discover -s tests -q
python3 -m scripts.validate_official_products
python3 scripts/validate_question_corpus.py
python3 scripts/validate_question_corpus_v2.py
npm run test:e2e
```

Python 기존 131개와 신규 13개 총 144개 PASS. 공식 제품 2건 검증 PASS.
Playwright 데스크톱·모바일 회귀 12개 PASS. 문서 경로·JSON 구문·git diff 공백 검사 PASS.
신규 검사는 출처 누락·중복 제품·프로파일 결측·잘못된 날짜·비공식 URL·출력 방식·클램쉘 불확실성·입력 오류·공개 판정 분리를 포함한다.
v1 한국어 20건·영어 5건과 v2 20건은 변경하지 않았다. 질문의 official_comparison과 usable_for_compatibility도 유지한다.
공식 제품과 질문의 자동 모델 매칭 및 comparison 데이터는 아직 만들지 않았다.

## 남은 단계

1. 두 모델의 사람 검수 및 변경 감지·스냅샷 보존 정책 확정.
2. MacBook Pro 및 다음 Air 세대의 동시 출력 프로파일과 OS·클램쉘 조건 수집.
3. 초기 모니터와 독의 포트별 출력·PD·OS 조건 수집 및 스키마 확장 검토.
4. 경로 전체 판정 데이터와 최소 30개 조합 테스트, 충돌 처리 검수.
5. 공식 데이터 승인 이후 사이트 연결. 질문 100건 목표와 MVP 명세는 계속 미완료다.

현재 catalog schema는 이 두 소스 기기용 초기 형태다. 모니터·독의 사실을 억지로 같은 property enum에 넣지 않는다.
공식 웹페이지는 변경될 수 있고 스냅샷이 없어 과거 문구 재현에 한계가 있다.
