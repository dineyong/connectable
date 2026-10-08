# Connectable — 제품 사양 의미 일치 검증

확인일: 2026-10-09. 기준 브랜치 `codex/data-validation-hardening`, 기준 커밋 `fb1382b4f06eff3396b8d54cf47d7d2690bb81d0`를 확인한 뒤 별도 `codex/product-semantic-validation`에서 작업했다.

## 실제 발견 사항

6모니터의 공식 fact 29개를 읽어 요약·typed payload와 화면의 선택·표시 구조를 대조했다. **현재 저장 데이터에서 기계적으로 확정 가능한 불일치는 0건**이다. 제품 값이 틀렸다고 만들어내거나 정상 데이터를 수정하지 않았다.

실제 결함은 기존 검증기의 의미 검사 부재였다. 실제 저장 fact의 메모리 복사에서 G2724D DP 165Hz를 typed 144Hz로, Dell upstream 90W 요약을15W로, DP1.4 typed 버전을1.2로 바꾸는 세 검사를 먼저 작성했다. 수정 전 세 검사 모두 FAIL(예상한 ValueError가 발생하지 않음), 수정 후 PASS. 이는 실데이터에서 발견한 잘못된 제품 사양이 아니라 **실제 저장 문장 형식을 기반으로 재현한 검증 결함**이다. 가짜 사례를 원본에 추가하지 않았다. 로그 `/tmp/connectable-semantic-red.log`.

## 자동 검사 범위

[product_semantics.py](../scripts/product_semantics.py)는 property별 **완전 일치하는 제한된 문장 형식**에서 명시된 필드만 비교한다. 임의 문장 전체에서 숫자를 뽑거나 AI로 자연어 의미를 확정하지 않는다.

- 해상도 숫자 쌍·Hz, 명시된 PANEL/PORT 및 입력 포트·최대 표기.
- 단위가 W인 전력, 명시된 upstream/downstream·USB-C 단자, ‘공급’ 방향, ‘최대’ 상한 표기.
- 명시된 DP 프로토콜·버전·Alt Mode 및 지원 표기.
- 지정된 포트 목록의 기능 식별자. 순서는 무관하며 포트 개수·동시 스트림 수를 추정하지 않는다.
- 제한된 VESA mm·틸트 각도·일부 명시적 기능 지원 문장.

known typed 값과 명시된 문장 값이 다른 경우에만 CONFLICT로 거부한다. typed UNKNOWN이나 누락은 값을 채우지 않고 MANUAL_REVIEW로 둔다. ‘USB-C PD 표기96W’만으로 공급 방향이나 RATED/UP_TO를 확정하지 않는다. 4K/FHD/QHD 이름에서 픽셀 수를 계산하지 않는다. PRODUCT_LABEL_ONLY 등 기존 무결성 검사는 그대로 유지한다.

`CONSISTENT_EXPLICIT_FIELDS`는 검사된 필드만 일치했다는 뜻이다. 전체 문장·미검사 필드·공식 출처의 진실성·실제 호환성이 승인됐다는 뜻이 아니다. 결과에 checked_fields, unresolved_fields, unexamined_fields를 제공한다. 검사하지 않은 필드의 의미는 수동 검토 대상이다.

## 수동 검토 결과

현재29개 중27개는 제한된 형식의 명시 필드 일치, 2개는 문장 전체가 수동 검토 대상이다.

| fact | 이유와 보존 기준 |
| --- | --- |
| jooyon-v32ue:site-1 | 32형 IPS·4K UHD 라벨만 존재. 픽셀·Hz를 추정하지 않음 |
| crossover-27uld950:site-2 | USB PD 지원·PD65 상품명과 상세 전력 UNKNOWN. 65W로 변환하지 않음 |

또한 다른27개의 unexamined_fields, 지역 SKU·OS/케이블 조건·실측 수전·지원 여부의 조건문, 새 문장 형식·부정문·인용문·복수 수치·원문이 수정된 경우는 사람 검토가 필요하다. Dell/LG 공식 출처 재확인은 이번에 수행하지 않았다. 기존 값과 미확인 상태를 그대로 유지했다.

## 변경 및 회귀 검사

- [새 의미 검사기](../scripts/product_semantics.py): 읽기 전용 CLI, fact별 결과와 CONFLICT 시 실패 종료.
- [기존 무결성 검사](../scripts/site_content_validation.py): typed payload 형식 검사를 유지한 뒤 의미 검사를 호출한다. 콘텐츠 생성과 공개 파생 생성 전후에 적용된다.
- [Python 검사](../tests/test_product_semantics.py):12개 추가. 실제 형식의 모순·역할·해상도·포트·전력·부정/인용/복수값·UNKNOWN·4K/PD 라벨·소수Hz·읽기 전용·방향/등급 비추정 검사.
- [브라우저 검사](../tests/e2e/site-v2.spec.js):1시나리오×desktop/mobile 2개 추가. 6제품29요약의 상세 표시를 대조하고 비교 셀에서 독립 기대값90/15W와 DP165/HDMI144Hz 및 UNKNOWN을 확인한다.

기존 UI는 summary를 이스케이프해 표시하며 비교 행은 typed property/scope에 따라 분류한다. 표시 문구를 새로 생성하거나 화면 기능을 바꾸지 않았다. 상세29요약 검사는 원본과 표시의 일치를 확인하며, 원문 사실이 맞는지를 검증하는 독립 oracle은 아니다. 비교의 주요 숫자는 별도 고정 기대값으로 검사했다.

## 전체 검증 및 보존

- 작업 트리 Python 전체 **348개 PASS, 3.424초**(기존336+신규12). v1 CSV·영어 예시·v2 JSONL도 PASS.
- 작업 트리 브라우저 전체 **66개 PASS, 20.1초**(기존64+신규2), desktop/mobile Chromium.
- `python3 scripts/build_site_content_v2.py --check`: PASS, 원본/파생 JSON 생성 일치.
- `python3 scripts/product_semantics.py`:29개 결과, CONFLICT0·명시 필드 일치27·수동 검토2, 정상 종료.
- 작업 전 data/schema/archive/web 64파일 모두 SHA-256 일치. 원본·catalog·코퍼스·규칙·파생JS·기존목업을 수정하지 않았다.
- E2E가 재생성한 기존 docs의 후기 캡처2개는 작업 시작 기준 커밋 바이트로 복구했다. 시작 시 이 파일들에는 사용자 변경이 없었다. 최종 커밋 재현 검사는 임시 폴더에서 수행해 원래 캡처를 다시 덮어쓰지 않는다.
- Git diff 및 문서 내부 링크 검사. 테스트 실패를 숨기거나 기존 테스트를 삭제하지 않았다.

코드 커밋 `00fedca`만 `git archive`로 임시 폴더에 풀어 전체 테스트를 추가 재실행했다. **Python348개 PASS(3.438초)·브라우저66개 PASS(19.8초)**. 로그는 `/tmp/connectable-semantic-commit-python.log`, `/tmp/connectable-semantic-commit-e2e.log`이다. 임시 폴더는 동일 lockfile의 설치된 npm 의존성과 Chromium을 사용했다.

## 남은 위험과 Git 정보

보수적인 형식 제한 때문에 문장 표현을 바꾸면 자동 검사 범위에서 벗어나 수동 검토가 늘어난다. 현재 MANUAL_REVIEW는 CLI 결과와 이 보고서로 제공하며 자동 검수가 승인된 것으로 취급하지 않는다. 새로운 자유문장이 생성 경로를 통과할 수 있다는 점은 의도된 정책이며, 사람 검토 절차를 대체하지 않는다. 모든 자연어 모순 탐지, 공식 자료 최신성, 모든 비교 조합/조건의 의미 승인, 실제 기기/스크린리더 검증은 아직 제공하지 않는다.

코드 커밋: `00fedca51410d50fcaae20a3c6766552d1193151`. 보고서 최종 커밋은 이 커밋의 자식으로 기록하며 최종 SHA·push 결과는 완료 응답에서 제공한다. 기존 README·DECISIONS 및 GP 검토 문서의 미커밋 변경은 이번 커밋에 포함하지 않는다. main 병합·공개 배포·호환성 엔진 변경은 하지 않았다.
