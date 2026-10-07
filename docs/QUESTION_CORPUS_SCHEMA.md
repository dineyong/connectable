# 사용자 질문 코퍼스 스키마 v1

확정일: 2026-10-07. 100건 수집 기반이며 현재 example은 검증용 5건이다. 기존 MVP·판정 상태는 변경하지 않는다.

## 파일과 직렬화

- [JSON Schema](../schemas/user-question.schema.json)가 자료형·enum·필수 필드의 단일 기준이다.
- [빈 템플릿](../data/research/user_questions.csv)과 [실제 예시](../data/research/user_questions.example.csv)는 동일한 전체 컬럼과 순서를 사용한다.
- UTF-8(BOM 읽기 허용), 쉼표 구분, LF, CSV 표준 따옴표 이스케이프. 배열 셀은 JSON이며 객체로 복수 디스플레이·연결 경로를 표현한다.
- 모든 컬럼 헤더 필수. 값 필수는 아래 표 기준. 선택 값 미상은 빈 셀, JSON에서는 키 생략; null 금지. 미상 상태값은 UNKNOWN. 알려진 빈 목록은 []이며 미상 목록은 결측 경로로 함께 기록한다.
- 수치 셀은 0 이상의 정수 또는 양수 실수. 날짜는 YYYY-MM-DD 실재 날짜, URL은 공개 HTTP(S) 절대주소. 자유 텍스트는 =, +, -, @로 시작하지 않는다(스프레드시트 수식 방지).
- source_normalized_model과 디스플레이 정규화는 명시된 표기 정리이며 공식 사양 확인을 의미하지 않는다. 해상도·주사율은 관측 조건이며 최대 성능으로 일반화하지 않는다.

## 데이터 사전

| 필드 | 설명 | 자료형 | 값 필수 | 허용값/제약 | 예시 |
|---|---|---|---|---|---|
| `id` | 내부 불변 ID | string | 필수 | `^UQ-[0-9]{4,}$` | `"UQ-0001"` |
| `source_url` | 개인 식별값·추적값을 제거한 공개 원문 URL | string | 필수 | `uri` | `"https://discussions.apple.com/thread/254292556"` |
| `site_name` | 사이트명 | string | 필수 | `자유 값` | `"Apple Support Community"` |
| `published_at` | 원문 게시일; 댓글 사례는 해당 댓글 날짜 | string | 선택 | `date` | `"2022-10-16"` |
| `checked_at` | 공개 본문을 확인한 한국 날짜 | string | 필수 | `date` | `"2026-10-07"` |
| `public_access` | 로그인 없이 본문 접근 가능 여부 | string | 필수 | `YES, NO, UNKNOWN` | `"YES"` |
| `reliability_grade` | 출처 등급; 단일 사례는 C | string | 필수 | `A, B, C, D, X` | `"A"` |
| `original_language` | 원문 언어 | string | 필수 | `ko, en, ja, zh, OTHER, UNKNOWN` | `"ko"` |
| `source_status` | 현재 접근 상태 | string | 필수 | `AVAILABLE, DELETED, INACCESSIBLE, UNKNOWN` | `"AVAILABLE"` |
| `source_location` | 원글 또는 댓글 날짜 등 익명 원문 위치 | string | 필수 | `자유 값` | `"원글"` |
| `source_manufacturer` | 소스 기기 제조사 | string | 선택 | `자유 값` | `"Apple"` |
| `source_family` | 제품군 | string | 선택 | `자유 값` | `"MacBook Air"` |
| `source_display_model` | 원문 모델명 | string | 필수 | `자유 값` | `"MacBook Air 13-inch 2020 M1"` |
| `source_normalized_model` | 명시된 항목만 정규화 | string | 선택 | `자유 값` | `"MacBook Air (M1, 2020)"` |
| `source_release_year` | 출시 연도; 구매 연도와 구분 | integer | 선택 | `Schema 참조` | `2020` |
| `source_chip` | 원문에서 식별한 칩 | string | 선택 | `자유 값` | `"M1"` |
| `source_variant` | 화면 크기 또는 하위 모델 | string | 선택 | `자유 값` | `"13-inch"` |
| `os_name` | 운영체제 | string | 선택 | `자유 값` | `"macOS"` |
| `os_version` | 보고된 버전 | string | 선택 | `자유 값` | `"15.1.1"` |
| `source_identity_certainty` | 소스 기기 모델 식별 확실성 | string | 필수 | `EXACT, PARTIAL, UNKNOWN` | `"EXACT"` |
| `displays` | 디스플레이별 조건 | array | 필수 | `Schema 참조` | `[]` |
| `connection_devices` | 케이블·어댑터·허브·독 배열 | array | 필수 | `Schema 참조` | `[]` |
| `desired_configuration` | 사용자가 원하는 구성의 사실 요약 | string | 필수 | `자유 값` | `"외장 화면 두 대 연결"` |
| `symptoms` | 보고된 증상 요약 | string | 필수 | `자유 값` | `"두 화면을 함께 사용하지 못함"` |
| `problem_type` | 주요 문제 분류 | string | 필수 | `NO_SIGNAL, RESOLUTION, REFRESH_RATE, MULTI_DISPLAY, FLICKER, PD_CHARGING, HDR, OTHER, UNKNOWN` | `"NO_SIGNAL"` |
| `attempted_solutions` | 실제로 시도한 해결 방법; 제안만 받은 방법 제외 | array | 선택 | `Schema 참조` | `[]` |
| `outcome` | 관측 결과이며 제품 호환 판정 아님 | string | 필수 | `SUCCESS, LIMITED_SUCCESS, FAILURE, UNRESOLVED, UNKNOWN` | `"SUCCESS"` |
| `outcome_evidence` | 원문 내 결과 판단 근거; 제3자와 분리 | string | 필수 | `자유 값` | `"원글에서 연결 실패를 보고하며 후속 확인 없음"` |
| `solution_devices_or_settings` | 결과에 기여한 장치나 설정 | array | 선택 | `Schema 참조` | `[]` |
| `output_mode` | 관측 출력 방식 | string | 필수 | `NATIVE, DISPLAYLINK, MIXED, UNKNOWN` | `"NATIVE"` |
| `display_mode` | 화면 모드 | string | 필수 | `MIRROR, EXTEND, MIXED, UNKNOWN` | `"MIRROR"` |
| `clamshell` | 클램쉘 사용 여부 | string | 필수 | `YES, NO, UNKNOWN` | `"YES"` |
| `target_external_display_count` | 원한 외장 화면 수 | integer | 선택 | `Schema 참조` | `1` |
| `actual_external_display_count` | 실제로 동작했다고 확인한 외장 화면 수 | integer | 선택 | `Schema 참조` | `1` |
| `pd_charging` | 소스 기기 충전 관측 | string | 필수 | `YES, NO, UNKNOWN` | `"YES"` |
| `pd_watts` | 관측 또는 명시된 PD 공급 W | number | 선택 | `Schema 참조` | `65` |
| `pd_conditions` | 충전기·포트·케이블 등 조건 | string | 선택 | `자유 값` | `"원문 미기재"` |
| `official_alignment` | 별도 공식 자료와 대조한 결과 | string | 필수 | `MATCH, CONFLICT, UNKNOWN, NOT_CHECKED` | `"MATCH"` |
| `official_source_urls` | 실제로 읽고 대조한 공식 문서 | array | 필수 | `Schema 참조` | `[]` |
| `independent_case_count` | 동일 조건의 독립 사례 수; 본 사례 포함, 좋아요 수 제외 | integer | 필수 | `Schema 참조` | `1` |
| `independent_case_urls` | 추가로 확인한 독립 사례 URL | array | 필수 | `Schema 참조` | `[]` |
| `missing_fields` | 결측 필드 경로; 와일드카드 허용 | array | 필수 | `Schema 참조` | `[]` |
| `conflict_status` | 검증 충돌 여부 | string | 필수 | `NONE, CONFLICT, UNKNOWN` | `"NONE"` |
| `review_status` | 검토 상태 | string | 필수 | `PENDING, NEEDS_REVIEW, REVIEWED, REJECTED` | `"PENDING"` |
| `review_notes` | 검토 근거 및 제한 | string | 필수 | `자유 값` | `"단일 자기보고 사례; 공식 대조 전"` |
| `usable_for_compatibility` | 향후 판정 근거 사용 승인 여부 | string | 필수 | `YES, NO, UNKNOWN` | `"YES"` |

### displays 배열 항목

| 필드 | 설명 | 자료형 | 값 필수 | 허용값/제약 | 예시 |
|---|---|---|---|---|---|
| `displays[].manufacturer` | 제조사 | string | 선택 | `자유 값` | `"BenQ"` |
| `displays[].display_model` | 원문 모델 표기 | string | 선택 | `자유 값` | `"EW3280U"` |
| `displays[].normalized_model` | 명시된 모델의 표기 정리; 공식 검증 아님 | string | 선택 | `자유 값` | `"EW3280U"` |
| `displays[].resolution` | 목표 픽셀 해상도; 4K만 언급되면 비움 | string | 선택 | `^[1-9][0-9]*x[1-9][0-9]*$` | `"3840x2160"` |
| `displays[].resolution_label` | 원문 해상도 표현 | string | 선택 | `자유 값` | `"4K"` |
| `displays[].target_hz` | 목표 Hz | number | 선택 | `Schema 참조` | `60` |
| `displays[].actual_hz` | 보고된 실제 Hz; 변동 범위는 메모 | number | 선택 | `Schema 참조` | `30` |
| `displays[].input_ports` | 명시된 입력 포트 | array | 선택 | `Schema 참조` | `[]` |
| `displays[].hdr` | HDR 사용 여부 | string | 선택 | `YES, NO, UNKNOWN` | `"YES"` |
| `displays[].identity_certainty` | 제품 식별 확실성 | string | 필수 | `EXACT, PARTIAL, UNKNOWN` | `"EXACT"` |
| `displays[].actual_resolution` | 실제 영상이 나온 픽셀 해상도 | string | 선택 | `^[1-9][0-9]*x[1-9][0-9]*$` | `2560x1080` |

### connection_devices 배열 항목

| 필드 | 설명 | 자료형 | 값 필수 | 허용값/제약 | 예시 |
|---|---|---|---|---|---|
| `connection_devices[].kind` | 연결 장치 유형 | string | 필수 | `CABLE, ADAPTER, USB_C_HUB, THUNDERBOLT_DOCK, DISPLAYLINK_DEVICE, UNKNOWN` | `"CABLE"` |
| `connection_devices[].manufacturer` | 제조사 | string | 선택 | `자유 값` | `"Dell"` |
| `connection_devices[].display_model` | 표시 모델 | string | 선택 | `자유 값` | `"D6000"` |
| `connection_devices[].normalized_model` | 정리 모델 | string | 선택 | `자유 값` | `"D6000"` |
| `connection_devices[].input_ports` | 호스트 측 입력 | array | 선택 | `Schema 참조` | `[]` |
| `connection_devices[].output_ports` | 디스플레이 측 출력 | array | 선택 | `Schema 참조` | `[]` |
| `connection_devices[].driver_used` | 드라이버 실제 사용; 필요 여부와 구분 | string | 필수 | `YES, NO, UNKNOWN` | `"YES"` |
| `connection_devices[].power_supplied` | 장치 전원 공급 여부 | string | 필수 | `YES, NO, UNKNOWN` | `"YES"` |
| `connection_devices[].notes` | 분기 경로·드라이버·전원 조건 | string | 선택 | `자유 값` | `"드라이버 설치 여부 미상"` |

## 개인정보·중복·신뢰 기준

사용자명·실명·이메일·전화번호·주문번호·기기 일련번호·계정 URL을 저장하지 않는다. 원문이나 댓글을 통째로 복제하지 않고 연결 조건과 결과를 한국어로 요약한다. 원문 위치는 날짜와 원글/댓글 역할로 기록한다. URL이 개인 식별자를 포함하면 안전한 게시물 주소로 바꾸거나 제외한다.

동일 URL+동일 원글/댓글 위치는 중복이다. 추적 파라미터·앵커를 제거한 게시물 주소로 비교한다. 다른 사이트 재게시·동일인이 반복 보고한 같은 구성은 독립 사례로 세지 않는다. 동일 스레드의 다른 구성은 위치·조건을 분리하고 독립성을 사람이 검토한다. ID 중복은 자동 오류, 의미상 중복은 사람 검수다.

A: 공식 사양·매뉴얼·표준기관. B: 확인된 공식 지원 답변 또는 복수 독립 일치 사례. C: 단일 커뮤니티·리뷰·블로그. D: 판매 설명·출처 불명 요약(후보만). X: 출처 없는 AI 생성값(입력 금지). 제조사 커뮤니티의 일반 사용자 글은 C다. 여러 사례만으로 공식 지원을 선언하지 않는다.

## 검토와 재사용

SUCCESS는 해당 보고자의 목표 달성, LIMITED_SUCCESS는 목표 일부 달성, FAILURE는 명시된 최종 실패, UNRESOLVED는 시도 후 해결 확인 없음, UNKNOWN은 결과 정보 없음이다. 사이트의 해결됨 배지보다 본인 보고를 우선한다. 타인의 성공을 원글의 성공으로 옮기지 않는다.

official_alignment=CONFLICT이면 conflict_status=CONFLICT 및 NEEDS_REVIEW. 단일 C 사례, 공식 대조 전, 모델/조건 미상, 충돌 사례는 usable_for_compatibility=NO. YES는 REVIEWED, 공식 MATCH, 충돌 NONE, A/B 근거, 복수 독립 사례와 사람 승인 메모가 필요하다. 자동 검증 통과는 사람 승인을 대체하지 않는다.

[수집 지침](QUESTION_COLLECTION_GUIDE.md) · [기존 절차](RESEARCH_WORKFLOW.md)
