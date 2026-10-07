# 질문 코퍼스 v2 채택·정식화 검증 기록

- 날짜: 2026-10-07
- 브랜치: `research/question-corpus-foundation`
- 시작 커밋: `4c22d2593c0ed104616c7fbcf6e3f11ab240ce20`
- 결정: 사용자 명시적 채택, [ADR-006](DECISIONS.md)

## 기준과 변경

정식 기준 스키마는 [schemas/user-question-v2.schema.json](../schemas/user-question-v2.schema.json),
유일한 원본은 [data/research/user_questions_v2.jsonl](../data/research/user_questions_v2.jsonl)이다.
[정식 필드 설명](QUESTION_CORPUS_SCHEMA_V2.md)과 [수집 지침 v2](QUESTION_COLLECTION_GUIDE_V2.md)를 작성했다.
README는 활성 기준, 파생 CSV 정책, 현재 5건과 전체 수집 이력 20건의 차이를 명시한다.

다음 사용자 결정을 ADR-006과 운영 지침에 반영했다.

- JSONL이 유일한 기준 원본, CSV는 직접 수정하지 않는 파생 요약
- 부분 경로·순서 허용 및 sequence_basis/topology_completeness/evidence_refs로 불확실성 보존
- mirrored는 복제 그룹 전체 물리 대수, independent_extended와 중복 계산 금지
- 객체별 근거 채택, 필드별 claim registry 후순위
- LONG_TERM_REPORT는 명시된 기간·지속 사용 근거가 있을 때만 부여
- 구체적 본인 실사용이 있는 판매·제휴 글은 포함 가능하며 상업성·포함 근거를 검토 정보에 기록
- 최종 FAILURE 비율 목표 없음, 명시적 최종 실패·포기만 허용
- 사용자 관측과 공식 사양 데이터셋 분리

## 구성별 결론

선택 배열 configuration_conclusions는 configuration_id, status, termination_type,
evidence_refs, 1~300자 summary를 필수로 하며 observation_ids는 선택이다.
미해결·미상 구성의 종결을 억지로 만들지 않는다. 한 구성에는 하나의 마지막으로 확인된 결론을 둔다.

구성 FAILURE는 결론이 참조하는 CASE_AUTHOR 근거의 author_configuration_terminations 안에
같은 구성·종결 유형을 명시한 진술 요약이 있어야 한다. 상세 관측 없이도 명시적 진술로 종결할 수 있으므로
observation_ids를 필수로 만들지 않았다. 잘못된 역할, 타 구성의 선언, 다른 종결 유형, 참조하지 않은 선언,
무신호·답변 부재만을 근거로 한 결론을 거부한다.

전체 outcome FAILURE는 별도 author_case_termination을 요구한다. 구성별 FAILURE 하나가 전체 목표의
포기를 뜻하지 않으며 최종 다른 구성이 성공해도 앞선 구성의 FAILURE는 함께 기록할 수 있다.
검증기는 구성 결론으로 전체 outcome을 덮어쓰거나 자동 집계하지 않는다.

추가된 선언 구조는 필드별 claim registry가 아니라 해당 원문 근거 안의 **작성자 종결 진술**을
구성 범위에 맞게 식별하는 최소 구조다. 실제 문장이 최종 실패·포기를 뜻하는지는 사람이 확인해야 한다.

## 기존 5건 정식화 결과

schema_version을 2로 바꾸고 새 review.commercial_context를 채웠다.
기존 관측·대수·경로·부분 순서·원문 확인일·v1 행 해시와 전체 outcome은 보존했다.
기록된 원문을 이번에 새로 열거나 공식 사양과 대조하지 않았고 origin=MIGRATED_V1, C등급, NEEDS_REVIEW, NO다.

| ID | 전체 outcome | 구성별 결론 | 상업성 검토 |
| --- | --- | --- | --- |
| UQ-0007 | UNRESOLVED | 없음 | 기존 자료에 없는 상업성 항목 UNKNOWN |
| UQ-0009 | LIMITED_SUCCESS | 없음. 일시 해결·재발은 관측으로 유지 | 기존 자료에 없는 상업성 항목 UNKNOWN |
| UQ-0010 | SUCCESS | cfg_final SUCCESS / GOAL_MET_REPORTED | 기존 자료에 없는 상업성 항목 UNKNOWN |
| UQ-0012 | SUCCESS | cfg_final SUCCESS / GOAL_MET_REPORTED | 판매·제휴 링크 YES, 광고성 의도 UNKNOWN, 본인 여러 경로 시험을 포함 사유로 기록 |
| UQ-0022 | LIMITED_SUCCESS | 없음. FHD 두 화면 제한 관측 유지 | 기존 자료에 없는 상업성 항목 UNKNOWN |

지정 5건에 명시적인 구성 포기·최종 실패 선언을 새로 확보하지 않았으므로 구성 FAILURE는 추가하지 않았다.
2건의 성공 결론은 기존 작성자 최종 성공 보고를 그대로 참조한다. 테스트에서 사용하는 명시 포기/실패 진술은
검증용 메모리 변경이며 실제 데이터 파일에 저장한 가상 사례가 아니다.
기존 자료에 없는 상업성 항목을 NO로 추정하지 않았고 원문 추가 검수 필요를 메모했다.

## proposed 파일 보존 방식

제안 파일은 다음 경로로 **바이트 그대로 이동**했다.

- [스키마 아카이브](../schemas/archive/user-question-v2.proposed.schema.json)
- [예시 아카이브](../data/research/archive/user_questions_v2.example.jsonl)

제안서와 이전 마이그레이션 보고서에는 역사 기록 안내와 현재 기준 링크를 추가했다.
제안 당시의 검증 명령·권고·미채택 상태는 당시 기록으로 읽어야 한다.
archive는 활성 기준이 아니고 기본 검증·집계에 포함하지 않는다. 정식 검증기는 schema_version=2만 허용하며
2-proposed 아카이브 입력을 거부한다. 따라서 두 스키마가 동시에 authoritative인 상태는 아니다.

v1 한국어 CSV 20행·영어 예시 5행·Schema·검증기·테스트·기존 v1 스키마 설명/수집 지침은 같은 경로와 바이트로 보존했다.
DECISIONS의 기존 ADR-001~005는 고치지 않고 ADR-006을 덧붙였다. CSV를 새로운 v2 원본처럼 재해석하지 않는다.

## 검증

작업 전 기존 전체 75개 테스트와 v1 CSV 검증이 통과했다. 작업 후 다음을 실행했다.

| 명령·검사 | 결과 |
| --- | --- |
| `python3 -m unittest discover -s tests -p test_validate_question_corpus.py -v` | 기존 v1 26개 PASS |
| `python3 -m unittest discover -s tests -v` | 기존 v1 26개 + v2 78개 = 총 104개 PASS |
| `python3 scripts/validate_question_corpus.py` | v1 한국어 20행·영어 예시 5행 PASS |
| `python3 scripts/validate_question_corpus_v2.py` | 정식 v2 5건 PASS |
| `python3 -m json.tool schemas/user-question-v2.schema.json > /dev/null` | 정식 스키마 JSON 구문 PASS |
| 구성별 종결·전체 outcome 독립성 테스트 | 명시 선언 없거나 잘못된 구성·역할·종결·관측을 연결한 사례 거부, 유효한 구성 포기와 전체 성공 공존 |
| 화면 수 회귀 테스트 | 복제 그룹 전체 대수와 확장 대수 중복·기지 화면 모드와 모순·점등 미상으로 숨긴 물리 대수 초과 거부 |
| 장기 사용·상업성 검토 테스트 | 명시 기간/지속 사용 근거 없는 장기 유형 거부, 상업성 검토 정보 필수 |
| v2 ID·정규화 URL 검사, v1 대응 검사 | 활성 5건 중복 0, 기존 ID·URL·행 해시·outcome 보존 |
| archive 이동 전후 및 v1 파일 바이트 비교 | 변경 없음 |
| 문서 Markdown 내부 경로 검사 | PASS |
| 개인정보·비밀값 패턴 및 요약 필드 검토 | 저장 대상 개인정보·비밀값 발견 없음 |
| `git diff --check` 및 최종 diff 검토 | PASS |

JSON Schema는 자료형·enum·필수 필드·길이를 정의한다. 다른 객체의 ID와 작성자 근거를 대조하는 조건은
[표준 라이브러리 검증기](../scripts/validate_question_corpus_v2.py)로 확인한다.
범용 JSON Schema 엔진 또는 source truth 검증기는 아니다.

## 남은 위험과 이번에 하지 않은 일

- 작성자 역할·실제 명시 진술·실사용의 충분성·광고 중심 여부·의미상 중복은 사람이 원문을 검수해야 한다.
- 기존 v1 요약만 사용한 5건은 개별 시도 날짜·부분 경로·광고성 미확정 값이 남아 있다. 스키마 확정이 결측을 해결하지 않는다.
- 개인정보/비밀값 패턴은 모든 개인정보 부재를 증명하지 않는다. 원문 URL 자체는 작성자가 있는 공개 페이지로 이어진다.
- 부분 그래프·부분 순서와 C등급 관측을 공식 최대 성능이나 호환 판정으로 일반화하면 안 된다.
- 나머지 15건 이전, 21~100번 수집, 공식 제조사 사양 대조, 호환성 판정, CSV 파생 생성기, 웹사이트/UI는 미구현·미진행이다.
- 기존 MVP 범위는 유지한다. 이번 채택은 조사 구조의 승인이다.

현재 조사 브랜치에만 논리적 단위로 커밋·push한다. main merge/push와 강제 push, 기존 이력 수정은 하지 않는다.
최종 커밋 SHA와 push 여부는 완료 응답에서 보고한다.
