# 모니터 비교 v3 파생 데이터 계약

기준일: 2026-10-10. 로컬 화면용 계약이며 공식 승인 카탈로그가 아니다.

## 원본과 생성

[원본 조사](../data/research/monitor-expansion/official_specs.json) 30종을
[기존 검증기](../scripts/validate_monitor_expansion.py)의 `official()`로 먼저 검증한다.
[생성기](../scripts/build_monitor_v3.py)는 원본의 모든 제품 필드, fact 값·단위·scope·qualifier·출처·미확인 필드를 그대로 복제한다.
원본을 수정하지 않는다. JSON은 [monitor-v3.json](../data/site/monitor-v3.json),
브라우저 번들은 [monitor-v3-data.js](../web/monitor-v3-data.js)의 `window.CONNECTABLE_MONITORS`다.
생성 파일은 직접 수정하지 않는다.

```sh
python3 scripts/build_monitor_v3.py
python3 scripts/build_monitor_v3.py --check
python3 -m unittest tests.test_monitor_v3 -v
```

`--check`는 파일 부재 또는 바이트 불일치를 실패 처리한다. 실행 시각을 넣지 않아 같은 원본에서 같은 파일이 나온다.
자바스크립트의 `<`와 줄 구분 문자는 escape하며 화면에서 문자열은 HTML로 해석하지 않아야 한다.

## 표시·필터 구조

루트는 원본 `schema_version`, `checked_on`, `public_status=UNKNOWN`, `products`에 `source_path`만 추가한다.
제품에는 `review_status=PENDING_HUMAN_REVIEW`, `usable_for_compatibility=NO`, `filters`, `filter_fact_refs`를 추가한다.
`filter_fact_refs`는 각 필터 값에 사용한 해당 제품의 fact ID 배열이다. 미확인은 null과 빈 배열이다.

| 필터 | 허용 원본 | 의미 |
|---|---|---|
| size | size / inch / PANEL | 원문 화면 대각선 수치 |
| width, height | width 또는 height / px / NATIVE_RESOLUTION | 양의 정수 픽셀 |
| refresh | refresh / Hz / PANEL | 원문 패널 주사율; 입력별 주파수와 다름 |
| panel | panel / null / PANEL | 원문 문자열 그대로; IPS 세부 명칭을 자동 합치지 않음 |
| usb_c_video | usb_c / null / PORT | 명시된 영상 모드만 true, 명시적인 USB-C 없음만 false |

숫자는 양의 유한 int/float만 허용하며 bool·숫자 문자열·다른 단위·다른 scope를 변환하지 않는다.
qualifier UNKNOWN은 필터로 사용하지 않는다. 같은 허용 조건의 값이 충돌하면 null로 남긴다.
필터는 사양을 찾는 보조값이며 원문 조건을 삭제하거나 호환성을 확정하지 않는다.

USB-C 모드는 실제 수집 문자열 `DP Alt Mode`, `DP Alt Mode + data`, `DP Alt Mode + Data`,
`DP Alternate`, `DP alt`만 허용한다. 커넥터 개수·데이터 기능·충전 전력·Thunderbolt 존재로
DP Alt Mode를 추정하지 않는다. 새 표현은 자동 인정하지 않고 후속 검토한다.
따라서 usb_c_video는 Thunderbolt를 포함한 모든 USB-C 연결의 지원 여부가 아니라 **확인된 DP Alt Mode 필터**다.
화면은 이 범위를 명확히 설명하고 null을 미지원으로 표시하지 않아야 한다.

## 실제 남은 결측과 표시 제약

- XG27AQDMG: 크기와 패널 refresh 미확인. DP 240Hz/HDMI 144Hz 입력 주파수는 상세 fact로 보존하며 패널 refresh로 승격하지 않는다.
- PG32UCDM: 패널 종류와 패널 refresh 미확인. 제품명·이미지·다른 필드에서 추론하지 않는다.
- M28U: USB-C 커넥터는 있으나 영상 모드 미확인. Dell U2724DE의 별도 Thunderbolt 정보도 USB-C DP Alt Mode로 합치지 않는다.
- 지역·SKU·리비전은 원본대로 표시한다. 한국 판매 제품과의 동일성은 별도 검토다.
- 전력은 원본 fact의 RATED/UP_TO와 scope를 함께 표시한다. 이 생성기는 PD와 소비전력을 한 숫자로 합치지 않는다.
- 후기·검색량·판매량·가격·추천 순위·승인 상태는 이 파생 구조에 새로 만들지 않는다.

## 검증

[15개 회귀 테스트](../tests/test_monitor_v3.py)는 원본 불변, 출처 없는 원본 거부, 정확 단위·scope,
불리언/잘못된 수치, 충돌, 픽셀 정수, USB-C 추정 차단, 명시 지원/없음, 실제 입력 주파수 사례,
제품 내부 fact 참조, 결정적 생성, script escape, stale 파일 탐지와 실제 산출물을 검사한다.
검증 통과는 공식 사양의 사람 승인이나 실제 연결 성공을 뜻하지 않는다.
