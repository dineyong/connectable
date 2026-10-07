# 사용자 질문 수집 지침 v2

2026-10-07 채택. [ADR-006](DECISIONS.md), [정식 스키마](QUESTION_CORPUS_SCHEMA_V2.md),
[JSON Schema](../schemas/user-question-v2.schema.json)를 따른다.
기존 v1 지침과 제안서는 과거 기록이며 신규 입력은 이 지침을 기준으로 한다.

## 원본과 현재 범위

[정식 JSONL](../data/research/user_questions_v2.jsonl)이 질문 코퍼스의 유일한 기준 원본이다.
UTF-8, LF, 한 줄 한 사례, schema_version="2"로 저장한다. CSV는 필요할 때 생성하는 파생 요약이며
직접 수정하거나 JSONL로 역수입하지 않는다. v1 CSV는 과거 자료로 동결 보존한다.
채택 시 정식화한 5건에 [1차 배치](QUESTION_CORPUS_V2_MIGRATION_BATCH_1_REPORT.md) 5건과 [2차 배치](QUESTION_CORPUS_V2_MIGRATION_BATCH_2_REPORT.md) 6건과 [3차 배치](QUESTION_CORPUS_V2_MIGRATION_BATCH_3_REPORT.md) 4건을 추가하여 현재 20건이다.
21~100번 수집·공식 사양 대조·호환성 판정은 이번 배치에서 수행하지 않는다. 조사 구조 채택을 제품/UI 개발 착수로 해석하지 않는다.

## 포함과 제외

기기·모니터·연결 장치 일부와 사용자의 목표·증상·실제 시도 또는 구매 의도가 식별되는 공개 한국어 사례를 포함한다.
기존 MVP의 Apple Silicon MacBook Air/Pro 범위는 유지한다. 파일럿의 Windows·데스크톱 기록은 조사 표본이다.
영어 v1 예시 5건은 한국어 목표 건수에 포함하지 않는다.

실제 본문을 열어 확인해야 한다. 검색 제목·요약만으로 입력하지 않는다.
모델과 문제가 모두 불명확한 글, 복제본, 개인 정보를 제거할 수 없는 자료, 비공개·로그인 제한 자료는 제외한다.
로그인·CAPTCHA·차단 우회, 비공개 API, 대량 크롤링을 하지 않는다.
robots.txt나 사이트 정책에서 자동 수집이 부적절하면 개별 수동 확인 수준으로 제한하거나 제외한다.
접근 실패는 원문 삭제라고 단정하지 말고 제외 사유를 작업 보고서에 남긴다.

판매·제휴 링크가 있어도 구체적인 **본인의 사용 과정과 결과**가 확인되면 수집할 수 있다.
review.commercial_context에 판매·제휴·광고성 여부, 포함 사유와 근거를 반드시 기록한다.
상품 소개·판매 유도가 중심이고 실사용 근거가 불충분하면 제외한다. 판매 링크나 제휴 URL은 코퍼스에 저장하지 않는다.
광고성 의도·협찬을 확인하지 못하면 UNKNOWN을 유지하고 추가 검수 필요를 메모한다.

## 입력 순서

1. 원문 URL·사이트·게시일·확인일·접근 상태를 기록한다. 원문이 수정됐거나 후속댓글이 있으면 근거 위치를 나눈다.
2. 개인정보를 제거하고 사실을 짧게 요약한다. 원문·댓글·이미지를 통째로 복제하지 않는다.
3. case_classification에 실제 질문, 문제 해결 후기, 구매 전 질문, 장기 사용 후기를 구분한다.
4. 작성자 자신이 말한 모델·단자·조건만 nodes/ports/environment에 옮긴다. 모든 객체의 evidence_refs를 기록한다.
5. 목표 TARGET, 실제 시도 OBSERVED, 타인 조언 ADVICE를 구분하고 구성별 연결 순서·분기를 기록한다.
6. 실제로 한 조치만 attempts에 넣고 관측은 observations에 둔다. 제안만 받은 조치를 실행했다고 기록하지 않는다.
7. 목표와 관측 화면 수를 별도로 적고 전체 outcome을 분류한다. 일시 효과·재발은 durability와 recurrence_of에 둔다.
8. 명시적인 구성 종결 진술이 있으면 configuration_conclusions에 기록하고 범위가 맞는 작성자 종결 근거를 연결한다.
9. 등급 C 기본값, 결측, 상업성 검토, 검토 메모를 기록한다. 공식 대조 전 NO/NOT_CHECKED를 유지한다.
10. 자동 검증 후 사람이 모델·역할·중복·종결 진술·광고 경계·개인정보를 검수한다. 검증 PASS가 공개 승인은 아니다.

## 사례 유형과 장기 사용

QUESTION은 사용 중인 문제·방법 질문, TROUBLESHOOTING_REPORT는 실제 시도와 결과를 보고하는 후기,
PRE_PURCHASE_QUESTION은 구매·추가 연결 전 목표 질문이다. 성격이 불확실하면 UNKNOWN 단독으로 둔다.
명확한 복수 성격은 복수 유형으로 표시할 수 있다.

LONG_TERM_REPORT는 작성자가 사용 기간 또는 지속 사용을 명시한 경우에만 부여한다.
long_term_basis에는 USE_DURATION_REPORTED/CONTINUED_USE_REPORTED, 진술 요약, 작성자 evidence_refs를 기록한다.
오래된 게시물, 해결됐다는 답, 특정 제품을 보유했다는 언급만으로 장기 사용을 추정하지 않는다.
임의의 최소 일수 기준을 만들지 않는다.

## 부분 경로·순서와 시점

알려진 노드와 연결 관계만 기록한다. 미기재 구간은 UNKNOWN_GAP, 미완성 구성은 PARTIAL/UNKNOWN으로 둔다.
UNKNOWN_GAP 간선은 직접 케이블 연결 또는 특정 중간 장치가 있다는 뜻이 아니다.
USB-C 단자만으로 Thunderbolt·DisplayLink·영상 출력·PD 지원을 추정하지 않는다.
집과 회사 또는 여러 시도에서 동일 실물인지 모르면 노드를 임의 병합하지 않는다.

sequence는 표현 순서다. 작성자가 순서를 명시했으면 REPORTED_SEQUENCE,
일부 앞뒤만 복원했으면 RECONSTRUCTED_PARTIAL, 전후 미상이면 UNORDERED를 사용한다.
posted 날짜와 실제 관측 날짜를 구분한다. observed_on/author_confirmed_on은 명시된 경우만 채우고
“재연결 후” 같은 조건만 있으면 relative_time에 둔다.

객체별 evidence_refs를 현재 기준으로 사용한다. 필드별 claim registry는 후순위다.
원글·작성자 후속댓글·수정 본문·타인 댓글을 역할과 위치로 구분한다. 사용자명은 쓰지 않는다.
타인 댓글은 실제 결과 근거로 사용하지 않는다.
기존 자료만 재구조화하면 origin=MIGRATED_V1이고 확인일을 갱신하지 않는다. 새로 본문을 확인했을 때만 DIRECT_CHECK다.

## 화면 수

goal.counts와 observation.counts를 따로 기록한다. scope(EXTERNAL_ONLY/INCLUDING_INTERNAL/UNKNOWN)를 명시한다.
connected는 물리 참여 수, lit은 영상이 표시된 수, independent_extended는 복제되지 않은 확장 화면 수,
mirrored는 복제 그룹에 포함된 **전체 물리 화면 대수**다. 기준 화면도 mirrored에 포함한다.
확장과 복제 화면은 서로 중복 계산하지 않는다. 외장 두 대가 복제라면 lit=2, mirrored=2, independent_extended=0이다.
이는 논리 감지 출력 수 1과 별개다.

모르는 수치는 생략한다. 0으로 채우지 않는다. lit=2만으로 독립 확장 2를 생성하지 않는다.
일부 화면별 미러링이 알려져 있으면 대수 필드를 생략해 모순을 숨기지 않는다.
4K/FHD를 픽셀 수로 변환하거나 낮은 해상도 성공을 목표 해상도 성공으로 바꾸지 않는다.
내장 포함 여부·클램쉘·점등은 각각 확인한다.

## 전체 결과와 구성별 종결

SUCCESS는 작성자 목표 달성, LIMITED_SUCCESS는 일부·조건부·일시 효과, UNRESOLVED는 해결 확인 없는 진행 상태,
UNKNOWN은 결과 정보 없음이다. FAILURE는 작성자의 명시적 최종 실패 또는 사용 포기만 허용한다.
FAILURE 목표 비율은 없다. 무신호 관측과 답변 부재를 최종 실패로 바꾸지 않는다.

configuration_conclusions는 선택 배열이다. configuration_id, status, termination_type, evidence_refs,
짧은 summary를 기록하며 관련 observation_ids는 선택이다. 상세 관측이 없으면 observation을 만들어 채우지 않는다.
실제 OBSERVED 구성만 참조하고 같은 구성의 결론을 중복으로 넣지 않는다.

구성 FAILURE는 참조한 evidence.author_configuration_terminations 안에 동일 configuration_id와
FINAL_FAILURE_REPORTED/ABANDONED_REPORTED 진술이 있어야 한다. summary는 실제 작성자의
명시적 종결 문장을 사실 중심으로 요약하고 evidence.location은 그 원문 위치를 가리켜야 한다.
무신호·답변 부재·타인의 포기 권유만 있으면 이 구조를 만들지 않는다.

전체 outcome FAILURE는 별도 evidence.author_case_termination을 요구한다.
앞선 구성의 포기와 최종 다른 구성의 성공은 함께 존재할 수 있다. 구성 결론을 전체 outcome으로 자동 집계하지 않는다.
채택 당시 5건과 1차 배치 5건에서 명시적 실패·포기 진술을 확보하지 않았으므로 구성 FAILURE는 추가하지 않았다.

## 개인정보·중복·공식 데이터 분리

사용자명·닉네임·실명·이메일·전화번호·주문번호·기기 일련번호·계정 URL을 저장하지 않는다.
원문 URL에서는 추적값을 제거하되 게시물 번호는 보존한다. 원문 전체와 스크린샷을 저장하지 않는다.
ID와 정규화 URL 중복은 오류다. 모바일/PC 뽐뿌 주소는 게시판 id·게시물 no로 비교한다.
같은 작성자의 후속댓글·다른 계정 비교·동일 글 재게시를 독립 사례로 세지 않는다.
다른 사이트 재게시의 의미상 중복과 동일인 여부는 사람이 검수한다. 개인 식별자를 저장해서 해결하지 않는다.

단일 사례는 C다. 공식 지원 커뮤니티의 일반 사용자 글도 공식 사양이 아니다.
공식 제조사 사양은 별도 데이터셋에서 관리한다. 코퍼스 product_links는 모델 연결 후보만 담고 사양을 복제하지 않는다.
공식 대조는 이번 작업에서 하지 않으며 NO/NOT_CHECKED를 유지한다. 추후 공식 비교의 충돌은 별도 대조 기록에서
CONFLICT로 관리하고 검토 상태를 NEEDS_REVIEW, 판정 재사용을 NO로 유지한다.

## 검증 명령

```sh
python3 -m unittest discover -s tests -v
python3 scripts/validate_question_corpus.py
python3 scripts/validate_question_corpus_v2.py
python3 -m json.tool schemas/user-question-v2.schema.json > /dev/null
```

v1 검증은 과거 기록의 보존 확인용이다. v2 기본 검증은 정식 스키마와 정식 JSONL만 읽는다.
archive의 proposed 자료를 활성 코퍼스로 합치지 않는다.
검증기는 자료형·enum·참조·대수·종결 근거 구조·개인정보/비밀값 패턴을 확인한다.
실제 문구가 명시적 종결인지, 작성자 역할이 맞는지, 실사용이 충분한지와 원문 진위는 사람 검수가 필요하다.

## 파일럿 이전 완료 현황

2026-10-07 [3차 배치](QUESTION_CORPUS_V2_MIGRATION_BATCH_3_REPORT.md)로 정식 JSONL은 20건이 됐다.
기존 20건 이전은 완료됐으며 추가 수집·공식 대조는 미진행이다.
