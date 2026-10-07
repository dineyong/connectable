# 질문 코퍼스 v2 마이그레이션 1차 배치

- 확인·변환일: 2026-10-07 (Asia/Seoul)
- 브랜치: `research/question-corpus-foundation`
- 시작 커밋: `1f7c73b289d3b22ce9417f789df064471c0fff08`
- 기준: [정식 스키마](../schemas/user-question-v2.schema.json), [수집 지침 v2](QUESTION_COLLECTION_GUIDE_V2.md)
- 원본: [v2 JSONL](../data/research/user_questions_v2.jsonl)

## 범위와 결과

기존 한국어 20건 중 지정한 UQ-0014·0024·0025·0006·0008만 이전했다.
기존 v2 5개 줄은 바이트 그대로 두고 뒤에 5개 줄을 추가하여 총 10건이다.
v1 한국어 CSV 20행과 영어 예시 5행은 변경하지 않았다. 신규 질문 수집과 나머지 10건 이전은 하지 않았다.
공식 사양 대조·호환 판정·웹사이트/UI·main 변경도 하지 않았다.

작업 전 README·docs 전체, 정식 Schema, 기존 5건, 검증기·테스트를 확인했다.
현재 브랜치와 깨끗한 작업 트리를 확인했고 기존 104개 테스트가 통과했다.
이번 배치의 실제 원문·작성자 후속댓글을 개별 열람했다. 검색 제목·요약으로 값을 채우지 않았다.
모든 사례는 C, NEEDS_REVIEW, usable_for_compatibility=NO, official_comparison=NOT_CHECKED다.

## 원문 재확인과 근거

| ID·원문 | 재확인 범위 | evidence origin | v1 → v2 outcome | 구성 / 시도 / 관측 / 결론 |
| --- | --- | --- | --- | --- |
| [UQ-0014](https://discussionskorea.apple.com/thread/254154256) | 원글과 2022-09-01 타인 답변. 작성자 해결 확인 없음 | DIRECT_CHECK 2개(원글·타인 조언) | UNRESOLVED → UNRESOLVED | 3 / 1 / 1 / 0 |
| [UQ-0024](https://m.ppomppu.co.kr/new/bbs_view.php?id=computer&no=697599) | 브라우저에서 본문·첨부 포트 사진·댓글. 2025-05-19 작성자 Windows 언급 확인 | DIRECT_CHECK 2개(원글·작성자 댓글) | LIMITED_SUCCESS → LIMITED_SUCCESS | 3 / 2 / 2 / 0 |
| [UQ-0025](https://m.ppomppu.co.kr/new/bbs_view.php?id=computer&no=695639) | 브라우저에서 본문·2025-03-01 작성자 감사 댓글. 모델 이미지 표기는 재확인하지 않음 | DIRECT_CHECK 2개 + MIGRATED_V1 1개(LEGION 이미지 식별) | UNKNOWN → UNKNOWN | 3 / 0 / 1 / 0 |
| [UQ-0006](https://meeco.kr/mini/37328357) | 원글·2023-07-05 19:32 작성자 결과 댓글 | DIRECT_CHECK 2개 | LIMITED_SUCCESS → LIMITED_SUCCESS | 5 / 4 / 4 / 1 |
| [UQ-0008](https://m.ppomppu.co.kr/new/bbs_view.php?id=computer&no=654438) | 본문 제품 표기·브라우저에서 2022-08-08 17:22 작성자 결과 댓글 | DIRECT_CHECK 2개 | LIMITED_SUCCESS → LIMITED_SUCCESS | 4 / 3 / 4 / 1 |

구성 수에는 TARGET·ADVICE가 포함된다. 시도는 OBSERVED에만 연결한다.
전체 근거 11개 중 DIRECT_CHECK 10개, MIGRATED_V1 1개다. 공개 페이지에 로그인 버튼이 있어도
본문·댓글을 로그인 없이 열람했으며 로그인·CAPTCHA·접근 제한 우회나 비공개 API를 사용하지 않았다.

웹 열람 도구에서 UQ-0024·0025는 접근 오류가 발생했고 UQ-0008은 댓글 본문이 표시되지 않았다.
동일한 공개 URL을 일반 브라우저로 열어 정상 표시된 본문·댓글을 확인했다. 사이트의 차단·로그인 요구는
발생하지 않았다. 도구 오류를 원문 삭제·비공개 상태로 단정하지 않았다. 대량 수집·판매 링크 방문은 하지 않았다.
원문 전체·이미지·작성자명·닉네임·계정 링크·판매 URL은 저장하지 않았다.

source.checked_at과 각 evidence.checked_at은 실제 확인 범위에 대응한다.
MIGRATED_V1 근거는 기존 확인일을 이어받았으며 이번 확인일과 우연히 같은 날짜다.
게시일·댓글 게시일을 실제 관측일로 옮기지 않았고 observed_on/author_confirmed_on은 채우지 않았다.

## 사례별 구조와 해석

### UQ-0014 — 업데이트와 미해결

12.5.1 업데이트 이후 HDMI 연결의 간헐 증상은 cfg_after_update에 둔다.
업데이트 이전의 성공 관측이나 업데이트가 원인이라는 인과 판정은 생성하지 않았다.
일반 점검 답변은 OTHER_COMMENT와 ADVICE 구성으로 분리하고 실제 실행 시도에 넣지 않았다.
커뮤니티 시스템의 글타래 닫힘은 작성자의 최종 실패·포기 선언으로 해석하지 않았다.
케이블·중간 장치·모니터 입력 단자는 UNKNOWN_GAP/PARTIAL로 남긴다.

### UQ-0024 — 두 모니터 입력 포트

원글 첨부 사진에서 번개·화면 아이콘이 **휴대용 모니터 측**에 있음을 확인했다.
SER8 후면 C 포트는 공통으로 두고 모니터 측 두 입력 포트를 cfg_lightning/cfg_icon으로 구분했다.
영상 정상과 NO_SIGNAL은 별도 관측이며, 어느 비교를 먼저 했는지 미상이므로 UNORDERED다.
별도 모니터 전원 케이블 없이 시험했다는 사실만 설정에 기록한다. 이를 PC의 PD 충전 관측으로 바꾸지 않았다.
타인 댓글의 DP Alt Mode·PD 설명이나 다른 사용자의 드라이버 해결은 작성자의 결과·공식 사양에 넣지 않았다.

### UQ-0025 — 현재·계획·구매 후보

현재 외장 한 대와 내장 화면을 사용하는 cfg_current만 OBSERVED다. 단순 현재 상태 보고이므로
추가 연결 시도는 0개다. 작성자 계획의 HDMI + USB-C to DP와 허브 대안은 각각 TARGET으로 둔다.
구매 예정 케이블과 MOKiN 허브는 TARGET에만 속한다. 판매 제목의 성능·PD 수치는 가져오지 않았다.
타인의 독자적인 다중 화면 사례와 감사 댓글을 작성자의 실행·성공으로 사용하지 않는다.
원글 모델 이미지의 LEGION 표기는 기존 v1 근거를 유지하고 정확한 SKU·OS는 미상이다.
현재 내장 영상 사용은 확인됐지만 목표 내장 포함 총 대수와 복제·독립 확장 대수는 채우지 않았다.

본문 판매 링크는 YES, 제휴·광고성 여부는 UNKNOWN이다. 기존 본인 사용 과정과 추가 연결·충전 질문이
구체적이고 판매 유도 중심이 아니므로 구매 전 질문으로 포함했다. 상품 사양과 추천은 기록하지 않았다.

### UQ-0006 — 직접 성공과 허브 제한

직접 HDMI 정상 관측과 허브 색상 문제·DDU 후 지속·30Hz 정상 색상 관측을 구분했다.
직접 경로와 허브 경로의 HDMI 케이블이 동일 실물인지 확인되지 않아 로컬 노드를 나눴다.
허브 호스트 연결 세부는 UNKNOWN_GAP이다. 일부 앞뒤만 확인돼 RECONSTRUCTED_PARTIAL을 사용했다.
최종 댓글은 30Hz의 색상 정상만 확인하므로 해상도를 목표 4K에서 자동 복사하지 않았다.
최종 허브 구성 결론은 LIMITED_SUCCESS다. 직접 HDMI 정상은 별도 관측으로 유지한다.
환불 분쟁 접수 계획을 허브 경로의 명시적 포기 선언으로 바꾸지 않았다.

### UQ-0008 — 영상과 오디오

초기 해상도 선택 문제, 교체 케이블의 55Hz 깜빡임, 최종 CRU 50Hz 영상 정상, 같은 최종 구성의
모니터 스피커 미인식을 각각 관측으로 둔다. 최종 시도는 영상·오디오 두 관측을 함께 참조한다.
55Hz→최종 50Hz는 작성자의 중간/최종 표현을 따르지만 오디오 관측의 순서는 UNORDERED다.
HDMI 2.0은 작성자의 케이블 표기만 notes에 보존하고 규격 인증으로 취급하지 않는다.
영상 signal_state는 정상이며 오디오 미인식은 별도 관측 summary에 명시한다.
최종 만족 보고와 기능 제한을 함께 보존해 구성 결론·전체 outcome 모두 LIMITED_SUCCESS다.

## 스키마 문제와 다음 배치

**변환 보류 0건. 다음 배치 전에 필수 Schema 수정은 없다.** 현재 부분 경로·순서와 선택 결론 구조로
이번 5건을 왜곡 없이 표현할 수 있다. 정식 JSON Schema와 검증기를 변경하지 않았다.

오디오 인식처럼 영상 이외의 기능은 전용 관측 축이 없어 summary에 의존한다. 최소 개선 후보는 선택
observation aspect(예: VIDEO/AUDIO/POWER/UNKNOWN)와 기능별 관측 상태다. 아직 채택·추가하지 않는다.
현재 소비자는 signal_state만으로 모든 기능 성공을 집계하면 안 된다.
구매 후보 여러 개 중 대표 허브만 노드화했으며 나머지 후보의 존재는 TARGET notes에 보존했다.
후보별 상세 제품 목록을 만들 필요가 있으면 별도 검수 작업으로 남긴다.

남은 결측은 정확한 모델·입력 단자·케이블 동일성·허브 입력 세부·OS 버전·실제 관측일·확장/복제 모드·PD다.
확인된 성공도 장기 안정·최대 성능·다른 제품의 호환성을 증명하지 않는다.
상업성 의도·협찬·의미상 중복·작성자 역할의 진위와 원문의 이후 변경은 사람 검수가 계속 필요하다.

## 검증과 보존

| 명령·검사 | 결과 |
| --- | --- |
| 작업 전 `python3 -m unittest discover -s tests -q` | 기존 104개 PASS |
| 작업 후 `python3 -m unittest discover -s tests -q` | 기존 104개 + 배치 회귀 9개 = 113개 PASS |
| `python3 scripts/validate_question_corpus.py` | 한국어 20행·영어 예시 5행 PASS |
| `python3 scripts/validate_question_corpus_v2.py` | 정식 JSONL 10건 PASS |
| `python3 -m json.tool schemas/user-question-v2.schema.json > /dev/null` | PASS, Schema 변경 없음 |
| migration 행 해시·ID·URL·전체 outcome 대조 | 10건 모두 원본 대응·일치 |
| ID·정규화 URL 중복 | 각각 0건 |
| JSONL 형식 | UTF-8/LF/한 줄 한 객체/총 10줄, 빈 줄·중복 키·비유한 수 없음 |
| v1 CSV 두 파일·기존 v2 5개 줄 | 시작 커밋과 바이트 동일 |
| 개인정보·비밀값 패턴 및 수동 문구 검토 | 발견 없음, 닉네임·계정·판매 URL 미저장 |
| README/docs Markdown 내부 경로 검사 | PASS |
| `git diff --check`, 추가 5건의 펼친 객체 및 실제 diff 검토 | PASS |

기존 v2 테스트는 5건 집합을 첫 5줄에서 검사하고 허브 분기 사례를 ID로 선택하도록 수정했다.
기존 104개 테스트를 삭제하거나 검사 범위를 약화하지 않았다. 신규 회귀는 총 10건·해시·바이트 보존,
각 사례의 역할/포트/결과/주사율/오디오·호환 승인 금지를 검사한다.
최초 신규 테스트의 OS 기대 문자열이 기존 표현 Monterey 12.5.1과 달라 실패했으며 기대값을 고쳐 재실행했다.

기존 5줄의 SHA-256: `a3dcf04b2f6d576723ca4f16c471ce5bf32ebb36ccac84e7370de404432a9d9d`.
v1 두 파일의 바이트 해시도 [기존 이전 보고서](QUESTION_CORPUS_V2_MIGRATION_REPORT.md)의 보존 증거와 같다.
README·정식 설명·수집 지침의 현재 건수와 보고서 링크만 갱신하고 DECISIONS·v1·아카이브는 보존했다.

데이터·문서/검증을 논리적 단위로 현재 research 브랜치에만 커밋·push한다.
최종 SHA와 push 여부는 완료 응답에서 보고한다. main merge·push·강제 push·기존 이력 수정은 하지 않는다.
