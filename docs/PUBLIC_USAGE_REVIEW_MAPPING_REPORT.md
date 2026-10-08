# 공개 사례 18건 검토용 구조 매핑

2026-10-08 · `research/question-corpus-foundation` · 로컬 검토 자료.

## 결과와 기준 파일

기존 공개 본문 조사 **18건 전체(PUR-001~018)**를 별도 검토용 객체로 매핑했다.
새 자료는 C등급 / REVIEW_ONLY / 공개 UNKNOWN / 사람 골든 승인 0을 유지한다.
정식 코퍼스·official catalog·pilot·골든·판정 엔진·목업에 합치지 않았다.
이번에 원문을 새로 열거나 추가 사례를 수집하지 않았다. 기존 조사 요약에 없는 값을 채우지 않았다.

- [변경하지 않은 조사 원본 18건](../data/research/review/public_usage_batch_2026-10-08.jsonl)
- [새 검토용 매핑 18건](../data/research/review/public_usage_mapped_2026-10-08.jsonl)
- [검토 매핑 검사 코드](../scripts/validate_public_usage_review.py)
- [회귀 테스트](../tests/test_validate_public_usage_review.py)
- [앞선 공개 조사 보고서](PUBLIC_USAGE_RESEARCH_BATCH_2026-10-08.md)

정식 기준은 계속 [질문 코퍼스 v2 스키마](../schemas/user-question-v2.schema.json)와
[기존 정식 20건](../data/research/user_questions_v2.jsonl)이다. 새 매핑을 정식 v2 코퍼스라고 부르지 않는다.
`mapping`에는 기존 v2의 사례 객체를 재사용하지만 코퍼스 `id/schema_version/migration`을 부여하지 않는다.
외곽 `id/source_id`는 PUR 연구 ID이며 UQ ID와 혼합하지 않는다. 정식 검증기에 자동 수입되지 않는다.

## 기존 구조 재사용

검사기는 정식 v2 스키마의 `$defs`와 객체 속성을 **실행 시 직접 읽어 재사용**한다.
노드·포트·구성·목표·시도·관측·출처·검토 객체와 참조/대수/종결 규칙을 복사한 별도 기준 스키마를 만들지 않았다.
기존 `check_value`, `check_semantics`, 날짜·URL·민감정보 검사도 재사용한다.
검토 외곽 구조만 새 검사기 안에 작게 정의했으며 일반 JSON Schema 구현체라고 주장하지 않는다.

| 내용 | 재사용 필드 / 처리 |
|---|---|
| 호스트·칩·모니터·케이블·허브·독 | `nodes`; 표시 모델은 작성자 진술, 정규화 모델/공식 ID는 UNKNOWN |
| 포트·연결 순서·분기 | `ports/configurations/edges`; 실제 위치 미확인, 미상 구간 UNKNOWN_GAP |
| 소스별 비교와 목표/조언 | 구성별 소스 1개; OBSERVED/TARGET/ADVICE를 분리 |
| OS·전원·덮개·HDR 조건 | `environment`와 구성 `settings`; 미기재는 UNKNOWN. 혼합 호스트의 OS를 공유하지 않음 |
| 실제 수행·관측·시간 | `attempts/observations/sequence_basis`; 일부 순서만 알면 RECONSTRUCTED_PARTIAL, 전후 미상이면 UNORDERED |
| 충전·클램쉘 | 기존 `observation.pd_charging/clamshell`; 기능별 근거와 함께 검사 |
| 임시 정상·재발 | `durability/recurrence_of`; 임시 우회를 영구 성공으로 바꾸지 않음 |
| 화면 수·복제·DisplayLink | 기존 counts/display_state; 독립 확장과 복제 대수 미상은 생략, 출력 모드와 분리 |
| 상업성·결측·검토 | `review.commercial_context/missing_fields`; 공식 대조 NOT_CHECKED, 재사용 NO |
| 게시물 전체 결과 | `outcome=UNKNOWN`; 기능 진술 매핑이 전체 목표 달성 승인에 해당하지 않음 |

구성 46개 중 **OBSERVED 44 / TARGET 1 / ADVICE 1**, 수행 시도 13개, 관측 50개다.
이 수는 서로 다른 사건이나 독립 사용자 수가 아니다. 한 글의 비교·설정·시간을 분리한 로컬 객체 수다.
시도와 결과를 확실히 연결할 수 없는 수행 진술은 `unscoped_statements`에 남겼다.
무신호·사용 불편만으로 전체/구성 FAILURE를 만들지 않았고 구성 종결 객체를 새로 승인하지 않았다.

케이블 SKU·길이는 원본에 알려지지 않았으므로 노드 notes와 결측 목록에 UNKNOWN으로 남긴다.
길이를 추정해 별도 typed capability에 넣지 않는다. 이 최소 검토 매핑에는 케이블 길이 전용 계산 필드를 추가하지 않았다.
알려진 표시명과 실제 SKU·리비전 최종 식별은 별개다.

## 추가한 최소 검토 정보

새 정식 코퍼스 필드는 없다. 다음 정보는 검토 파일 외곽에만 추가했다.

1. `source_id/source_line_sha256/mapping_basis`: 원본 **LF 포함 한 행 바이트**와 연결한다.
   `EXISTING_REVIEW_SUMMARY`는 기존 직접 확인 조사 요약을 재구조화했다는 뜻이다.
   원본 URL·게시일·확인일·접근 상태를 보존하고, 근거의 DIRECT_CHECK와 확인일도 기존 확인 이력에서 상속한다.
   이번 매핑 작업의 새 원문 재확인으로 해석하지 않는다. v1 이전이 아니므로 MIGRATED_V1로 바꾸지도 않는다.
2. `evidence_annotations`: 기존 evidence 객체별로 진술 역할, 근거 성격, 기능 범위,
   관련 configuration ID, 원본 JSON Pointer, 해상도/주사율/전력 의미를 적는다.
   필드별 claim registry나 제조사 사양 데이터셋을 만들지 않았다.
3. `functional_observations`: 기존 observation ID에 영상·모드·배율·충전·클램쉘·복귀·재연결의 검토 슬롯을 연결한다.
   각 슬롯은 독립적이며 미확인은 UNKNOWN과 빈 evidence_refs로 명시한다.
4. `unscoped_statements`: 구매계획·조언·상품 소개·결과를 결합하기 어려운 수행 진술을 관측과 분리한다.

진술 역할은 AUTHOR_OBSERVATION / PERFORMED_CHANGE / CONFIGURATION_REPORT /
ADVICE / PURCHASE_PLAN / PRODUCT_DESCRIPTION / CONTEXT다.
**작성자의 조언도 실제 관측이나 수행으로 바꾸지 않는다.** 타인 댓글은 OTHER_COMMENT/OTHER로 보존한다.
이번 배치는 USER_REPORT 근거만 허용한다. 제조사 사양이나 독립 실물 재현으로 재분류하면 검사가 실패한다.
제품 소개의 상품 최대값은 PRODUCT_DESCRIPTION으로만 보존하며 공식 claim을 생성하지 않는다.

기능 상태 NORMAL/PROBLEM/TEMPORARY_WORKAROUND/UNKNOWN은 검토용 관측 표기다.
게시물 outcome의 SUCCESS/FAILURE나 엔진의 COMPATIBLE/INCOMPATIBLE을 뜻하지 않는다.
클램쉘 설정 여부와 그 상태에서의 사용 관측도 별개로 둔다.

### 신호·배율·전력 경계

- `signal_mode.resolution_pixels`: 실제 신호 픽셀. 18건 모두 UNKNOWN이다.
- `resolution_label/label_basis`: 작성자의 4K/FHD 등 출력 진술과 선택 가능 표기를 구분한다.
  SELECTABLE_LABEL을 기존 display_state의 실제 출력 해상도 표기로 복사하지 않는다.
- `hz/hz_basis`: REPORTED_OUTPUT / SELECTABLE_LIMIT / SELECTED_SETTING / UNKNOWN을 구분한다.
  설정 상한 30Hz, 선택 후 무신호 144Hz를 실제 출력 Hz로 저장하지 않는다.
  검토 슬롯의 숫자 Hz는 UNKNOWN과 함께 명시할 수 있도록 숫자 문자열로 저장한다.
  기존 v2 display_state의 숫자 Hz는 보고된 출력이고 개별 화면 범위가 명확할 때만 채운다.
- `ui_scale`: 배율·작업 공간 표기. PUR-001의 3008×1692와 PUR-014의 QHD를 신호 픽셀로 바꾸지 않는다.
- `pd.recognized`: 작성자가 충전을 보고했는지. USB-PD 프로파일·전압 협상 확인을 뜻하지 않는다.
  `watts/power_basis`는 실제 수전 측정과 별개다. 18건의 실제 와트는 모두 UNKNOWN이다.
  CHARGING_RECOGNITION/PRODUCT_MAXIMUM 근거를 MEASURED_INPUT으로 승격할 수 없다.

각 기능의 알려진 값에는 해당 기능·구성에 해당하는 작성자 관측 근거가 필요하다.
영상 근거를 복사하여 충전·클램쉘·복귀·재연결 정상으로 바꾸면 실패한다.
숫자·enum 검사만으로 원문 의미의 진위를 판정할 수는 없으므로 근거 역할의 수동 검수는 계속 필요하다.

## 18건 사람이 검토할 매핑 요약

아래의 정상·문제는 작성자 진술이며 공식 판정이 아니다. 모든 행의 공개 상태는 UNKNOWN이다.
공통 케이블 SKU·길이·공식 제품 ID와 측정 와트는 UNKNOWN이다.

| ID | 경로·조건·개별 결과 | 구성/시도/관측 | 남은 경계 |
|---|---|---|---|
| PUR-001 | M1 Air→C-C→V32UE 영상·충전 진술. 3008×1692는 UI. 내장 화면 보조 | 1/1/2 | 코드웨이·60Hz 없음. 반복 사용을 매번 재연결 성공으로 단정 안 함. 오디오 제어는 notes |
| PUR-002 | M1 C-C 불안정·무출력과 SOHO Dock HDMI 정상 분리 | 2/2/3 | 다른 기기의 비교 정상은 상세 경로 부족. 모델 전체 결함/성공률로 집계 안 함 |
| PUR-003 | M1 C-C/C-HDMI 정상·SSD 허브 M7 무출력·LG 비교 정상. PC HDMI/DP-C와 삼성 노트북 비교 분리 | 8/0/8 | 클램쉘 시점의 정확한 경로 UNKNOWN. PC 무출력은 최종 FAILURE 아님. 원격 사용은 유선 해결 아님 |
| PUR-004 | M2 Belkin HDMI 최대30Hz 선택. 구매계획 TARGET·타인 제안 ADVICE | 3/0/1 | 실제 점등/최종 Hz·구매/교체 성공 UNKNOWN |
| PUR-005 | M2 Pro HDMI/Windows HDMI/Mac C-C의 깜빡임 분리 | 3/0/3 | 60/30Hz·HDR·케이블·드라이버 변경의 개별 순서/결과 미상, 실제 수행 진술만 별도 보존 |
| PUR-006 | 칩 미상 Mac→번들C-C→27ULD950 클램쉘 영상·충전 | 1/0/2 | 4K 콘텐츠 재생≠신호 측정. 포인트·구매권유 상태 보존 |
| PUR-007 | MSI 직접 정상/Belkin INC013qc 경유 미인식/LG 비교 정상 | 3/0/3 | 혼합 M4 표기는 chip UNKNOWN. 클램쉘 듀얼은 목표만, 수행·독립2대 아님 |
| PUR-008 | Baseus 4K30·복귀 문제→UGREEN6 4K60·복귀 정상. UGREEN7은 결과 미확인 | 4/1/4 | 덮개 전환·EasyRes는 특정 허브에 결합하지 않고 별도 UNKNOWN_GAP. 재연결은 임시 우회 |
| PUR-009 | M1 Monterey12.1 깜빡임→미러링 ON/OFF 임시 정상→재연결/재부팅 재발 | 3/1/3 | 포트·모니터 UNKNOWN. TEMPORARY와 RECURRENT 연결 유지 |
| PUR-010 | M1 허브 HDMI→U28E590D 초기4K60 미출력 | 1/0/1 | HDMI2 설명은 실제 최종 모드 아님. 소개 Apple MUF82KH/A는 관측 구성에 없음 |
| PUR-011 | 초기HD/재연결4K 선택/60Hz 깜빡임/30Hz 안정 분리 | 4/2/4 | M1 16인치 원문 표기 유지, chip UNKNOWN. 선택 가능 해상도·선택 Hz와 실제 전송 구분 |
| PUR-012 | M1 HOST C-C→MH510→DP. 별도 PD IN 전원. 영상·동시 충전 | 1/0/1 | 최대3화면·8K/4K120·100W는 소개 수치. 실제 Hz·수전 UNKNOWN |
| PUR-013 | M1 Pro→USB4 표기→PD2307→DP2/HDMI1→3화면, 일부 복제·충전 | 1/1/2 | connected=3만 기록. lit/복제 전체 대수/독립 대수·90/96W 측정 UNKNOWN |
| PUR-014 | UNKNOWN 호스트의 초기C-C/Belkin 교체/충전 사용/UI 배율 분리 | 4/1/4 | M2 Air 서술과 Mac mini 사진을 해당 시도의 소스로 강제 결합 안 함. 제휴 고지 보존 |
| PUR-015 | M1→USB-C 허브→DisplayLink→HDMI2; 설치 후 2화면·충전, FHD60 추가 진술 | 1/1/3 | 네이티브 아님. 독립 확장 대수/어느 화면의60Hz인지 미확정, 전 화면 Hz로 복제 안 함 |
| PUR-016 | 기존 허브4K30→UGREEN4K60 | 2/1/2 | 모니터·허브SKU·실제 픽셀·OS UNKNOWN |
| PUR-017 | M1 UGREEN HDMI→IP2730 FHD120 정상 / 144Hz 선택 검은 화면 | 2/1/2 | 144는 선택 값. 대역폭 설명/DP 권고는 조언, 공식 원인·수행 아님 |
| PUR-018 | M1 일체형UGREEN 케이스 장착 간섭 / 제거 후 포괄적 사용 정상 | 2/1/2 | 영상·PD 개별 성공은 UNKNOWN. 이전 허브 불안정을 현재 구성으로 결합 안 함.4K60/30은 상품 수치 |

상업성은 기존 조사 상태를 보존했다. PUR-006 포인트/권유, PUR-008·018 제휴 링크,
PUR-012·013 판매/행사 링크, PUR-014 제휴 고지 등은 포함 사유와 함께 기존 commercial_context로 연결한다.
대가/제조사 제공 미확인을 “광고 없음”으로 바꾸지 않았다.
서로 다른 조건의 같은 모델 정상/문제 진술을 공식 CONFLICT로 묶거나 성공률로 계산하지 않는다.
사용자의 M1 Air/V32UE/코드웨이 실물 사례는 조건 미완성이며 새 19번째 사례로 넣지 않았다.
검색 리드와 접근 제한 자료는 앞선 보고서에만 남고 매핑 대상에 없다.

## 검증과 보존

```sh
python3 -m unittest tests.test_validate_public_usage_review -q
python3 -m unittest discover -s tests -q
python3 scripts/validate_public_usage_review.py
python3 scripts/validate_question_corpus.py
python3 scripts/validate_question_corpus_v2.py
python3 -m scripts.validate_official_products
python3 scripts/validate_connection_model_pilot.py
python3 scripts/path_instance_v1.py --check
```

신규 회귀 **54개 통과**, 전체 **290개(기존236+신규54) 통과**.
18건 매핑·원본 행 해시·ID·정규화 URL·객체/근거 참조·날짜·UTF-8/LF/한 행 한 객체·민감정보 검사를 통과했다.
형식 검사는 BOM/CRLF/빈 행/마지막 LF 누락/중복 JSON 키/NaN을 거부한다.
기존 v1/v2·catalog·pilot·Path Instance 검증도 통과했다.

회귀는 조언/구매계획/상품 소개의 관측 승격, 한 기능 근거의 다른 기능 재사용,
배율→신호·선택상한→출력·인식/상품상한→실측와트 오인, 누락UNKNOWN,
원본 확인일 갱신,18건 누락/중복/비공개 실물 혼입, DL/복제 과대 계수와 임시 우회의 재발 유실을 검사한다.

원본18건 SHA-256: `8131cea42edf5644c8fc5f276690c6f4767bf4e2a355dd000e037b6bc777eb43`.
원본 행 해시는 줄의 LF까지 포함하며 숫자 문자열만 바뀌어도 보존 오류가 난다.
작업 시작 스냅샷의 **기존71파일**(README·docs·data·schemas·scripts·tests·mockup, 캐시 제외)은
모두 바이트 그대로 보존했다. 기존 미커밋 파일도 덮어쓰지 않았다.
새 데이터·보고서의 개인정보/비밀 패턴과 내부 문서 링크를 점검했다.
테스트의 이메일/전화/토큰 모양 문자열은 거부 검사용 합성 입력이며 실제 개인정보·키가 아니다.
Git diff와 새 파일을 직접 검토했다. 원격 작업·commit·push·PR·merge·배포·삭제는 하지 않았다.

## 남은 한계와 화면 연결 전 최소 조건

1. 요약 자료는 원문 전체를 대체하지 않는다. 추가/최종 검수 전 원문의 정확한 근거 위치·작성자 역할·각 설정 시점을 다시 확인한다.
   검사기는 사람이 붙인 역할/범위를 검증하지만 역할 자체의 진실을 자연어로 자동 증명하지 못한다.
2. 케이블 길이·SKU, 상세 OS, 실제 출력 픽셀, 협상/실측 전력, 재현 기간이 많이 비어 있다.
   범용 호환성·최대 모드·충전 성공을 계산할 수 있는 입력은 아니다.
3. PUR-013·015처럼 다중 화면의 어느 화면·어느 그룹인지 미상인 경우 global 진술만 유지한다.
   개별 화면 값으로 자동 전파하지 않는다. audio/Apple Watch/물리 장착은 notes에 보존하고 이번에 별도 판정 모델을 만들지 않았다.
4. 정식 v2 관측의 `summary/display_state`만 읽는 소비자는 기능 범위를 모르므로
   이 검토 자료를 그대로 수입하면 배율·선택 모드·기능 성공이 섞일 위험이 있다.
   기존 소비자를 바꾸거나 정식 스키마 필드를 추가하지 않았고 현재 경로로 자동 수입도 없다.
5. 추후 검토 화면은 얇은 읽기 전용 어댑터부터 필요하다. PUR ID/원문 링크/확인일/작성자 진술 배지,
   UNKNOWN을 숨기지 않는 기능별 슬롯, TARGET/ADVICE/OBSERVED 분리, 상업성/결측 표시만 우선한다.
   공식 자료와 실물 검증은 별도 패널/근거 종류로 표시하고, 전체 호환 성공·실패 집계/승인 버튼/상품 추천과 연결하지 않는다.
6. 정식 코퍼스 확장 채택 전에 기능 범위와 모드 의미의 최소 선택 필드를 별도로 검토한다.
   이번 외곽은 해당 문제를 검토하기 위한 작은 구조이며 정식 v2 개정이나 typed capability 승인 결정이 아니다.

이번에는 UI·공식 대조·판정·추가 수집을 수행하지 않았다. 다음 단계는 원문 의미 수동 검수와 최소 표시 계약 확정이다.
