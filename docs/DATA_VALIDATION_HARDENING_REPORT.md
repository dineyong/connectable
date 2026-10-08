# Connectable — 데이터 검증 무결성 보강

작업일: 2026-10-09. [감사 보고서](SITE_MONITOR_BATCH_1_AUDIT.md)의 검증기·참조 결함을 보강했다. 원문 재조사, 제품 수집, 판정 엔진 확장, UI 기능 추가, 배포·광고·제휴 활성화는 수행하지 않았다.

## 브랜치와 커밋

- 시작 HEAD: `52a8bc33de666c224322cd186521147e3a88fb7e`.
- 작업 브랜치: `codex/data-validation-hardening`.
- `ce9d6df`: 기존 미커밋 사이트·연구 입력·archive·검증 의존 자료를 보존한 기준 자료 커밋. 72파일이며 새 제품을 수집한 변경이 아니다. 이 커밋 단독은 완성된 실행 기준이 아니라 다음 코드 커밋과 함께 사용하는 보존 단계다.
- `c6c3730`: 검증기와 파생 데이터 참조 보강. 기존 미추적 생성기·테스트도 처음 Git에 기록했다.
- `0f5e197`: 기능과 fact 속성·지원 상태가 맞지 않는 참조 거부 및 회귀 검사.
- 이 보고서의 문서 커밋은 위 코드 커밋의 자식으로 기록한다. 해당 최종 SHA와 원격 push 결과는 완료 응답에서 제공한다. main과 기존 연구 브랜치 ref는 변경하지 않는다.

기존 작업 트리에는 미커밋 구현이 있었으므로 GitHub 재현에 필요한 자료를 함께 기록했다. 기존 README·DECISIONS 및 별도 GP 검토 문서의 미커밋 변경은 이번 커밋 범위에서 제외하고 그대로 남겼다. 기준 자료에 CONNECTION_GOLD_SET_PLAN의 기존 검토 문구와 legacy 테스트 경로 이관이 포함됐으며 이번에 새로 변경한 것은 아니다.

## 수정 전후

| 결함 | 수정 전 재현 | 수정 후 |
| --- | --- | --- |
| 빈 fact/product/후기 연결 근거 | 빈 source_refs가 PASS | nonempty·중복·존재 여부 검사로 거부 |
| 잘못된 typed payload | VIDEO_PROFILE에 `{watts:-1}`만 넣어도 PASS | property별 필수·허용 필드, enum, 유한 양수·정수 차원, 범위 검사 |
| 다른 모델 공식 출처 | V32UE fact에 MSI 공식 출처 연결이 PASS | 소속 제품의 출처 목록·모델 범위 검사로 거부 |
| 파생 fact 참조 대상 누락 | capability.feature_refs는 남지만 features.fact_id 누락 | fact_id와 source_refs·출처 record_id 보존, 생성 전후 검사 |
| 기능 의미가 다른 참조 | USB-C 영상 capability가 PD fact를 가리켜도 PASS | capability별 property·지원 상태·영상 단자/공급 역할 검사 |
| 알려진 지원 상태와 모순 | UNSUPPORTED fact로 CONFIRMED capability 표시 가능 | 같은 참조의 SUPPORTED/OFFER 조건 검사로 거부 |

추가로 credential-free HTTPS, 실제 ISO 날짜, 제조사 fact의 확인 상태·위치·요약, 전역/로컬 ID 중복과 관계 참조를 검증한다. PRODUCT_LABEL_ONLY 전력은 UNKNOWN만 허용하며 PD65 상품명에서 65W를 생성하지 않는다. 원본 content의 source_file·record_id·URL은 실제 저장 원본과 대조한다. 사용자 자료의 source_file은 코퍼스 또는 mapping record로 연결되고, 제조사 자료는 해당 source record로 연결된다.

기존 proposed typed schema를 억지로 완화하지 않았다. 사이트 pilot에서 이미 사용하던 UNKNOWN 및 기능 property를 위한 별도 엄격한 계약을 `site_content_validation.py`에 정의했다. 이는 호환 판정 엔진에 적용하는 계산 규칙이나 공식 스키마 정식 채택이 아니다.

## 실제 변경 파일

- [검증 계약](../scripts/site_content_validation.py): payload·출처·로컬/전역·capability 참조 검사.
- [콘텐츠 생성기](../scripts/build_site_content_v2.py): batch 검증 강화, 생성 결과 검증, 직접 CLI 실행 경로 유지.
- [브라우저 파생 생성기](../web/derive-site-content.py): 생성 전후 검증, fact/source ID와 익명화된 사용자 근거·구성·관측 대상 보존.
- [파생 JS](../web/site-content-v2.js): 참조를 해결할 수 있는 대상 객체 추가. 원본 JSON의 내용·해시를 바꾸지 않음.
- [Python 회귀 검사](../tests/test_site_validation_hardening.py): 신규 17개 테스트.
- [브라우저 회귀 검사](../tests/e2e/site-v2.spec.js): 공식 fact/source와 사용자 관측/configuration/evidence 실제 자산 참조 검사 1시나리오, desktop/mobile 2개.
- 이 보고서. 이전 미커밋 자료의 Git 등록 목록은 `git show --stat ce9d6df`로 확인할 수 있다.

## 테스트와 보존

1. 수정 전 첫 6개 회귀 검사 모두 FAIL. 로그 `/tmp/connectable-hardening-red.log`. 빈 근거 3종·잘못된 payload·모델 출처 불일치·파생 fact target 누락을 재현했다.
2. 검증기 수정 후 5개 PASS·projection 1개 FAIL. 대상 보존 후 6개 모두 PASS. 추가 capability 검사 2개도 수정 전 FAIL을 확인했다. 로그 `/tmp/connectable-hardening-capability-red.log`.
3. 최종 전체 `python3 -m unittest discover -s tests -q`: **336개 PASS**. 기존319개 유지+신규17개. v1 CSV·영어 예시·정식 v2 JSONL도 PASS. 작업 트리 실행 3.018초.
4. 전체 `npm run test:e2e -- --workers=2 --output=/tmp/connectable-hardening-e2e-results`: **64개 PASS, 29.0초**. 기존62개 유지+신규2개. 실패를 삭제하거나 기준을 완화하지 않았다.
5. 커밋을 `git archive`로 임시 폴더에 풀어 미커밋 변경에 의존하지 않는 재현을 검사했다. 첫 커밋 조합에서 Python334·브라우저64 PASS. 최종 코드 `0f5e197`에서도 **Python336개 PASS(2.965초)·브라우저64개 PASS(18.8초)**. 로그는 `/tmp/connectable-hardening-final-commit-python.log`, `/tmp/connectable-hardening-final-commit-e2e.log`에 기록했다. npm 의존성은 설치된 동일 lockfile 환경을 사용했다.
6. `python3 scripts/build_site_content_v2.py --check` PASS. 생성 JSON 바이트 일치. 공개 파생 데이터도 입력·출력 계약 검사 PASS.
7. 작업 전 data·schemas·archive·web 64파일 SHA-256과 비교: 바뀐 기존 파일은 파생 생성기·파생 JS 두 개뿐이다. catalog·코퍼스·규칙·스키마·모니터 batch 원본·content JSON·화면 HTML/CSS/앱·스크린샷·archive는 바이트 그대로다.
8. `git diff --check` 및 개인정보/비밀값 패턴 검사 PASS. 브라우저 projection에는 내부 source_file 경로를 넣지 않았다. 개인정보 패턴 검사는 모든 자유문장의 개인정보 부재를 수학적으로 증명하지는 않는다.

## 호환성 영향과 남은 위험

현재 정상 데이터 6모니터·38연구기록·3가이드가 거부되지 않으며 화면 출력 의미는 유지된다. 파생 JS에는 ID와 익명화 근거·구성·관측 대상이 추가돼 크기가 늘었다. 공급 전력·실제 충전 관측, 사용자/공식 근거, UNKNOWN과 미지원은 계속 분리한다. 향후 계약 밖 property는 자동 추정하거나 통과시키지 않고 명시적 설계 검토를 요구한다.

Dell/LG 공식 사양 재확인은 여전히 미완료이며 새 값을 채우지 않았다. 요약문과 typed 값의 모든 의미 일치, 가이드의 주제별 관련성, 완전한 기능 수집, 실물 연결·실제 Safari·스크린리더·사진 권리·공개 운영 심사는 남아 있다. 참조·형식 검증은 공식 페이지의 진실성이나 전체 호환 승인 근거가 아니다. 모든 공개 호환 상태 UNKNOWN과 사람 승인 골든0/30을 유지했다.

이번 범위의 검증기/파생 참조 결함은 해결했다. 다음 단계에서는 이 결과를 검토하고 요약 일치·가이드 관련성·접근 불가 공식 자료 재검수를 별도 범위로 진행할 것을 권고한다.
