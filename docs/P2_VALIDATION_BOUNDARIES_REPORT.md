# 통합 전 P2 검증 경계 보강

확인일: 2026-10-09. 기준: `199c146`(P1 수정 `4f51e0f` 포함).
작업 브랜치: `codex/p2-validation-boundaries`.
고정 코드 후보: `28cc669`. 최종 보고서 커밋 SHA는 완료 응답과 Git 이력에 기록한다.

## 목표와 세 작업 단위

기존 P1 수정 검수를 반복하지 않고 [독립 검토의 IR-01~04](P1_FIX_INDEPENDENT_REVIEW.md) 및 미확인 승인·CI 경계를 보강했다. 원본 사양·코퍼스·화면을 바꾸지 않고 검증기·생성·CI만 수정했다.

| 단위 | 내용 | 커밋 |
|---|---|---|
| 1 | URL 인코딩·입력값 | 1bc30f9, ea7503f |
| 2 | 생성 전 원본 검증, 모델별 fact 근거, 미확인 승인 차단 | 9385df0, c39f8a8 |
| 3 | CI 범위 및 읽기 전용 JS 최신성 gate | 28cc669 |

URL 단위 초기 테스트에서는 query가 없는 정상 URL을 strict parser가 거부하는 회귀가 발견됐다. 테스트 실패 뒤 커밋이 이어지게 실행한 것은 작업 실수다. 이력을 수정하지 않고 `ea7503f`에서 query가 없으면 빈 배열로 처리하도록 수정했고 정상 회귀를 재실행했다. 이 두 커밋은 함께 검토해야 하며 최종 후보는 모두 포함한다.

## 수정 전 재현과 수정 결과

먼저 새로운 테스트를 작성했다. 초기 **9개 테스트 실행에서 정상 1개 통과, 나머지 결함 검사 실패(subTest 포함 17개 실패)**를 확인했다. 실패 로그 `/tmp/connectable-p2-red.log`. 이후 protocol.mode 음성 테스트도 별도로 실패(`ValueError not raised`)를 확인한 뒤 수정했다. 모든 변형은 메모리 복사/mock이며 원본에 가짜 값을 저장하지 않았다.

| 재현 입력 | 수정 후 |
|---|---|
| %00·%0A·%0D 경로, raw DEL | UNKNOWN |
| 5회 인코딩된 외부 URL을 language로 전달 | UNKNOWN |
| malformed escape, 빈/중복 query 조각, 임의 language 값 | UNKNOWN |
| 정상 Unicode 제품 경로 및 language=en-us | 기존 허용 유지 |
| 원본 pilot에 미허용 final_url 삽입 후 단독 생성 | 생성 전 원본 Schema 검사에서 거부 |
| 다른 모델의 공식 record를 fact 근거로 추가 | 제품·fact별 원본 근거 범위 검사에서 거부 |
| 파생 링크의 EXACT_SKU/SKU 승격 | 거부, MODEL_ONLY/UNKNOWN 유지 |
| public COMPATIBLE, human APPROVED, 사용자 근거 사용 YES | 거부 |
| Cross 부분 확인 mode를 verified_fields로 이동 | 거부 |
| verified_fields를 줄이고 비확인 width 변경 | 거부 |
| 미등록 PROTOCOL.mode | 거부 |
| 오래된 JS 자산에 --check | 실패 종료, 파일 자동 수정 없음 |

## 1. URL 입력 계약

[data_trust.py](../scripts/data_trust.py)는 디코딩된 path의 제어문자/공백 및 raw DEL을 거부하고 UTF-8 디코딩 오류를 UNKNOWN으로 처리한다. query의 malformed percent escape·빈 조각·구문 오류를 거부한다.

Dell language는 소문자 2자리 언어 또는 2자리-2자리 코드로만 인정한다. 주연테크 게시물·page와 크로스오버 상품 ID는 ASCII 숫자로 제한한다. 이 좁은 자료형 검사 때문에 깊게 인코딩된 URL이 디코딩 횟수 제한 뒤에 숨더라도 허용되지 않는다. 미등록 경로·언어 형식은 수동 검토 대상으로 유지한다. 모든 제조사 URL 형식을 지원한다고 주장하지 않는다.

외부 URL 자동 접속·DNS 조회·HTTP redirect 탐색은 추가하지 않았다. 공통 helper는 기록된 redirect_chain/final_url을 검사하지만 원본 Schema가 허용하지 않는 자료는 생성 전에 거부한다. 향후 리다이렉트 수집을 추가하려면 별도 자료형·수집 정책·네트워크 안전 설계가 필요하다. live redirect/SSRF 방어까지 완료했다는 뜻은 아니다.

## 2. 원본 검증 및 승인 경계

### 생성 전 실제 소비 객체 검증

[site_input_validation.py](../scripts/site_input_validation.py)를 도입하고 [build_site_content_v2.py](../scripts/build_site_content_v2.py)의 변환 시작 전에 호출한다.

- pilot: 기존 Schema/typed validator로 실제 읽은 객체 검사.
- Mac catalog: 기존 catalog validator로 실제 객체 검사.
- 공개 후기 원본/매핑: 기존 파일 envelope·해시 검사와 실제 소비 객체 검사를 함께 실행. 원본 읽기 snapshot 변경, ID 범위, observation 참조 및 source hash 위반 거부.
- 한국어 v2: 기존 record Schema·의미 검사와 ID/정규화 URL 중복·빈 코퍼스 검사.
- batch: 기존 모델/제조사 검사 유지. 데이터 파싱은 중복 JSON key·비유한 상수를 거부한다.

파일 검사만 수행하고 다른 메모리 객체를 생성에 쓰는 우회도 막는다. 이 기능은 생성 전에 호출되며 입력 자료를 수정하지 않는다. 원본을 추가로 네트워크 수집하거나 Schema를 완화하지 않았다.

### 제품별 fact 근거 바인딩

[site_content_validation.py](../scripts/site_content_validation.py)는 pilot와 monitor batch의 현재 원본 제품·fact 인덱스를 기준으로 검사한다. 각 monitor의 모델·제조사, source ID 범위, fact의 제품 ID와 원본 source_refs가 일치해야 한다. 같은 제조사라도 다른 모델 record는 거부한다. full과 public projection 모두 같은 계약으로 검사한다.

이는 원본에 기록된 연결 관계 검증이다. 공식 원문 내용이 진실인지, 지역 SKU가 동일한지까지 자동 증명하지 않는다. 새로운 제품/fact는 근거 있는 원본에 먼저 추가되어야 하며 파생 자산에만 만든 임의 ID는 승인하지 않는다.

### 미확인 승인 차단

- 모든 site 객체의 public_status는 UNKNOWN만 허용한다.
- monitor/fact는 PENDING_HUMAN_REVIEW, 후기/guide는 NEEDS_REVIEW를 요구한다.
- 후기 링크는 MODEL_ONLY/variant_match UNKNOWN/NEEDS_REVIEW만 허용한다.
- 제공된 usable_for_compatibility는 NO만 허용한다. public projection에서 원래 제외된 필드를 새로 노출하지 않는다.
- PROTOCOL.mode는 현재 필요한 ALT_MODE/UNKNOWN만 허용한다. 새로운 모드는 명시적 계약 검토가 필요하다.
- [공식 검토 검증기](../scripts/validate_official_spec_review.py)는 기존 fact 재확인의 전체 payload가 원본과 같아야 한다. 비확인 필드만 바꾸고 부분 검증으로 숨길 수 없다.
- 역사적인 수동 2건의 확인/미확인 필드 집합을 그 배치의 정책으로 고정했다. 새로운 공식 확인은 이 기록의 mode를 조용히 승격하는 대신 별도 근거·검토 배치로 다뤄야 한다. 일반적인 필드별 claim registry나 사람 승인 UI는 만들지 않았다.

부분 검토의 의미를 UI에서 새롭게 표시하는 작업과 LG RATED/UP_TO 문구 수정은 이번 검증 코드 배치에서 수행하지 않았다. 원본의 RATED와 별도 검토 UP_TO는 그대로이며, UNKNOWN 숫자를 채우지 않았다. Cross의 기존 공급 필터 표시와 수동 문장의 공개 콘텐츠 적용 gate는 다음 별도 콘텐츠 검토 항목이다. 현 화면은 로컬 검토 목업이고 사람/공개 승격은 차단된다.

## 3. CI 자동 검사

[workflow](../.github/workflows/validate.yml)의 push 범위를 main, research/question-corpus-foundation, codex/**로 변경했다. pull_request 검사도 유지한다. 권한은 contents:read이며 배포 job·광고/제휴 job·외부 URL fetch를 추가하지 않았다. 동일 ref의 오래된 실행은 concurrency로 취소한다.

기존 Python·코퍼스·catalog·pilot·path 및 브라우저 검사에 다음 명시적 gate를 추가했다.

- 공개 후기 매핑 validator.
- site JSON 생성 --check.
- public JS 생성 --check.
- 공식 수동 검토 validator.
- product_semantics CLI.

[derive-site-content.py](../web/derive-site-content.py)의 --check는 JS 결과 바이트를 비교하고 오래됐으면 실패 종료하며 파일에 쓰지 않는다. 기본 생성 동작은 유지한다. 원격 Actions 실제 결과는 아래 별도 기록한다. YAML 구문 검사와 로컬 실행은 원격 runner 성공의 대체 증거가 아니다. 저장소 branch protection의 required checks 설정은 변경하지 않았다.

## 전체 검증

최종 코드 후보 `28cc669`를 git archive로 임시 폴더에 풀어 실행했다. 기존 사용자 문서나 E2E 스크린샷을 덮어쓰지 않도록 저장소 밖에서 실행했다. 동일 package-lock의 설치된 npm 의존성과 Chromium을 사용했다.

- Python: **386 PASS**, 17.385초(기존370 + 신규16).
- 브라우저: **66 PASS**, 21.0초(desktop/mobile Chromium).
- 신규16: URL3, 생성/근거/승인11, JS stale/read-only2.
- v1 CSV·영어 예시·v2 JSONL: PASS.
- build_site_content_v2 --check: PASS.
- derive-site-content --check: PASS.
- 공식 검토10·부분검토2: PASS.
- 공개 후기 매핑18: PASS.
- 의미 검사: 기존 29개 fact, CONFLICT0, 수동2 유지.
- workflow YAML 파싱 및 추가 command 확인: PASS.

기존 정상 6모니터·38기록·3가이드가 통과했다. 원본·파생 JSON/JS·화면은 보존했다. 검증은 코드 계약과 회귀 검사이며 서비스의 실제 제품 정확도 또는 외부 최종 승인이 아니다.

## 보존 및 변경 파일

기존 변경은 검증 코드·생성 스크립트·workflow 여섯 파일에 한정된다. 신규 파일은 입력 validator, 테스트 세 파일, 본 보고서다. catalog·pilot·코퍼스·rules·schemas·site JSON·web 화면/JS 자산·archive 및 사용자 README/DECISIONS/GP 문서 변경은 보존했다. 기존 로컬 통합 감사 보고서는 이번 커밋에 넣지 않았다.

- 변경: data_trust.py, build_site_content_v2.py, site_content_validation.py, validate_official_spec_review.py, web/derive-site-content.py, .github/workflows/validate.yml.
- 신규: site_input_validation.py, test_url_validation_boundaries.py, test_p2_validation_boundaries.py, test_projection_check.py, 본 보고서.

작업 전 hash 및 내부 링크·diff·비밀값 검사 최종 결과는 아래 기록한다.

## 통합 판단 및 다음 검토

지금 후보는 재현된 경계 입력을 거부하고 정상 자료를 보존한다. 하지만 main 병합·배포·외부 최종 승인을 수행하지 않았다. 원격 CI 성공을 확인한 뒤 사용자가 실제 diff를 검토해 통합 후보를 승인해야 한다.

남은 사항은 부분 검토/수동 문장의 화면 표현과 편집 승인 절차, LG 정격/상한 표시의 의미 검토, 지역 SKU 확인, 미커밋 진행 문서 정리, 실물/다른 브라우저 검증이다. 이들을 숫자 추측·즉시 원본 변경으로 해결하지 않는다. 실시간 redirect 수집은 별도 위험 평가 후 진행한다.

## 원격 CI 및 최종 보존 기록

- 코드 후보 `28cc669d049e5b583054fa2f7d00f3484f6d372f`의 [GitHub Actions 실행](https://github.com/dineyong/connectable/actions/runs/37855983017): SUCCESS. Python 386개(24.780초), Chromium 브라우저 66개(35.7초)와 모든 데이터/파생물 검사 통과. 로컬 실행 결과와 원격 실행 결과를 각각 확인했다.
- 작업 전 SHA-256 manifest 165개 경로 비교: 기존 파일 변경은 위 여섯 코드/workflow 파일뿐이다. 원본 자료, 기존 화면, 사용자 미커밋 자료의 바이트는 보존됐다.
- 본 보고서 내부 상대 경로: 누락 없음. `git diff --check`: 통과.
- 추가된 파일과 diff를 개인정보·자격증명 패턴 및 직접 코드 검토로 검사했다. 실제 사용자 식별정보나 비밀값 추가 없음. 회귀 테스트의 공격 입력은 합성 URL이며 사용자 자료가 아니다.
- main은 `c58dee5f3d1222d49e598dddbac5c8c6a7b4b8f0` 그대로다. 별도 작업 브랜치만 push했다. 이 보고서의 최종 커밋 SHA는 Git 이력으로 확인하며, 보고서 자신에 순환 참조하는 SHA를 기록하지 않는다.
