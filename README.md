# Device Compatibility Platform

노트북과 모니터, 케이블, 허브, 도킹 스테이션 조합의 연결 가능성을
공식 사양과 실제 사용자 사례를 바탕으로 판정하는 한국어 웹 서비스입니다.

현재 저장소는 **개발 전 조사·설계 단계**입니다. 제품 코드보다 시장 검증,
출처 정책, 데이터 모델, 판정 규칙을 먼저 확정합니다.

## 현재 단계

- 한국 내 직접 경쟁 서비스 조사: 완료
- 서비스 범위 확정: 완료
- 조사 및 데이터 수집 절차 정의: 완료
- 한국어 질문 파일럿: 20건 수집, 정식 v2 전환 20건
- 질문 코퍼스 v2: 채택 완료 (JSONL 원본, CSV 파생)
- 기존 20건 v2 이전: 완료 · 21~100번 수집: 미진행
- 공식 출처 목록 및 초기 데이터 구축: 1차 기반 완료 (Air 2모델, 사람 검수 대기)
- MVP 개발: 대기

## 핵심 원칙

1. AI의 추측으로 호환성을 판정하지 않습니다.
2. 모든 핵심 사양은 출처와 확인일을 기록합니다.
3. 공식 지원, 규격상 가능, 실사용 성공을 구분합니다.
4. 일반 댓글과 구조화된 연결 성공·실패 사례를 분리합니다.
5. 검색 페이지는 검증된 근거와 고유한 정보가 있을 때만 공개합니다.
6. 제휴수익보다 판정 정확성과 사용자 신뢰를 우선합니다.

## 문서

- [프로젝트 범위](docs/PROJECT_SCOPE.md)
- [조사 작업 절차](docs/RESEARCH_WORKFLOW.md)
- [의사결정 기록](docs/DECISIONS.md)


## 질문 코퍼스의 기준 파일

- **Authoritative schema:** [schemas/user-question-v2.schema.json](schemas/user-question-v2.schema.json)
- **유일한 기준 원본:** [data/research/user_questions_v2.jsonl](data/research/user_questions_v2.jsonl)
- [정식 스키마 설명](docs/QUESTION_CORPUS_SCHEMA_V2.md) · [수집 지침 v2](docs/QUESTION_COLLECTION_GUIDE_V2.md)
- [채택 및 검증 기록](docs/QUESTION_CORPUS_V2_ADOPTION_REPORT.md)

현재 v2 원본은 기존 20건 전체를 담는다(채택 시 5건 + 1차 5건 + 2차 6건 + 3차 4건).
[1차 배치](docs/QUESTION_CORPUS_V2_MIGRATION_BATCH_1_REPORT.md)와 [2차 배치 검수 보고서](docs/QUESTION_CORPUS_V2_MIGRATION_BATCH_2_REPORT.md)를 참고한다.
[3차 배치 보고서](docs/QUESTION_CORPUS_V2_MIGRATION_BATCH_3_REPORT.md)에서 마지막 4건 검수를 확인한다. 전체 수집 이력 20건과 혼동하지 않는다. v1 한국어 CSV와 영어 예시 5건은 과거 자료로 보존하며 직접 수정하지 않는다.
향후 CSV 요약은 v2 JSONL에서 파생하며 역으로 원본에 쓰지 않는다. 이번에는 CSV 생성기를 구현하지 않았다.

[제안 스키마 아카이브](schemas/archive/user-question-v2.proposed.schema.json)와
[제안 예시 아카이브](data/research/archive/user_questions_v2.example.jsonl)는 채택 전 기록으로,
활성 검증·수집·집계의 기준이 아니다. v2 검증기는 정식 스키마와 정식 JSONL만 기본 검사한다.

```sh
python3 -m unittest discover -s tests -v
python3 scripts/validate_question_corpus.py
python3 scripts/validate_question_corpus_v2.py
```

## 사이트 목업

사용자 요청에 따라 조사 기반 한국어 목업을 제작했다. 연결 조건 입력·미확인 조건 요약·실제 사례 검색과
상세 원문 확인을 제공한다. [목업 검증·실행 안내](docs/SITE_MOCKUP_REPORT.md)를 참고한다.
공식 호환 판정과 운영 서비스는 아직 구현하지 않았다.

```sh
python3 scripts/build_mockup_cases.py
python3 scripts/serve_mockup.py
```

로컬 미리보기: http://127.0.0.1:8873

브라우저 회귀 검사: `npm ci`, `npx playwright install chromium`, `npm run test:e2e`.
[추가 보강 보고서](docs/SITE_HARDENING_REPORT.md)를 참고한다.

## 공식 사양 및 판정 데이터

[1차 기반 문서](docs/OFFICIAL_DATA_FOUNDATION.md)에 공식 제품 원본·스키마·검수용 규칙을 정리했다.
사용자 코퍼스와 분리하며 사이트 공개 판정에는 아직 연결하지 않는다.
검증: `python3 -m scripts.validate_official_products`.
