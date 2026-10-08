# Connectable — 모니터 배치 1 통합 품질 감사

감사일: 2026-10-09. 대상: [통합 보고서](SITE_MONITOR_BATCH_1_INTEGRATION_REPORT.md)의 로컬 구현.

## 대상 식별과 결론

브랜치: `research/question-corpus-foundation`. HEAD: `52a8bc33de666c224322cd186521147e3a88fb7e`.
**배치 1 구현은 해당 커밋에 포함된 완성본이 아니라 수정·미추적 파일이 있는 작업 트리다.** 따라서 HEAD만 checkout해서 이번 감사 결과를 재현할 수 없다. README·web/index.html 등 기존 수정과 data/site·새 UI·테스트·보고서의 미추적 상태를 확인했다. 감사 과정에서는 이 문서만 추가하고 코드·데이터를 수정하지 않았다. 테스트가 만드는 임시 로그·결과물은 검증 산출물이다. 커밋·push·merge·배포는 실행하지 않았다.

판정: **로컬 콘텐츠 보강과 검토는 조건부 진행 가능. 공개 운영 준비 완료로 판정할 수 없다.** 현재 데이터에서 원본 훼손·공식/후기 근거 혼합·공개 호환 승인·치명적 화면 오류는 발견하지 않았다. 그러나 출처 검증·payload 검증·파생 참조·관련 링크의 보강과 공식 자료 재확인이 필요하다. 문제는 이 감사에서 수정하지 않았다.

## 항목별 결과

| 검증 항목 | 결과 | 근거·한계 |
| --- | --- | --- |
| 모니터 6종 구조 | 통과 | ID 중복 없음. 기존 pilot 3종과 별도 batch 3종을 읽기 전용으로 파생. 모든 공개 상태 UNKNOWN |
| 공식 사양 원문 대조 | 부분 통과 / 일부 확인 불가 | 신규 3종과 G2724D의 저장 사실 대조. U2723QE 페이지 도구 오류, LG 페이지 초기 열림 후 상세 조회 timeout으로 일부 주장 재확인 불가 |
| 실제 후기 4건 | 통과 | 원문 본문을 열어 모델·구성·관측 대조. MODEL_ONLY·변형 UNKNOWN 유지 |
| 두 제품 비교 | 통과 / 구조적 위험 | 두 개 제한, 패널/입력별 Hz/PD 분리, UNKNOWN 고지. 요약문 표시에 의존하며 전력 역할별 행은 없음 |
| 공식 기능 필터 | 통과 / 데이터 완전성 한계 | 현재 저장 fact와 일치. 미수집 기능을 미지원으로 바꾸지 않음. 6종 전체 사양 완전성은 보장하지 않음 |
| 목차·상세·관련 링크 | 경로 통과 / 의미 개선 필요 | 현재 ID 참조 유효, 목차 초점 이동 검사. 세 가이드에 동일한 모니터·후기 목록을 일괄 연결 |
| Python·브라우저 재실행 | 통과 | 319개·62개 PASS. 상세 실행 결과 아래 기록 |
| 기존 원본 보존 | 통과 | 보호 manifest 17파일, archive 8+16파일 해시 일치. 관련 추적 원본 15파일 HEAD 대비 변경 없음 |
| 테스트 중요 기능 포함 | 부분 통과 | 안전 렌더링·CSP·출처·원본 보존·비교·필터·탐색 포함. 빈 근거·payload 오류·모든 비교 셀·모든 필터 조합의 검증 공백 |

## 공식 원문 확인

| 모델 | 원문과 결과 |
| --- | --- |
| Dell U2723QE | [GB 공식 페이지](https://www.dell.com/en-gb/shop/dell-ultrasharp-27-4k-usb-c-hub-monitor-u2723qe/apd/210-bcxk/monitors-monitor-accessories). 이번 열람은 Internal Error. 기존 4K60·DP Alt Mode·90W upstream·15W downstream 사실은 보존했으며 이번 원문 재검증 통과로 집계하지 않음 |
| LG 27UP850-W | [MY 공식 페이지](https://www.lg.com/my/monitors/ultrafine-uhd-4k-5k/27up850-w/). 첫 열람에 페이지가 반환됐으나 상세 위치/문구 조회는 Internal Error·timeout. 저장된 4K60·96W·DP Alt Mode 전체는 이번 감사에서 확인 불가 |
| Dell G2724D | [US 공식 페이지](https://www.dell.com/en-us/shop/dell-27-gaming-monitor-g2724d/apd/210-bhxc/monitors-monitor-accessories). DP 2560×1440 165Hz와 HDMI 144Hz 일치. 추가 사양의 높이 조절은 화면 자료에 아직 수집되지 않음 |
| 주연테크 V32UE | [공식 출시 자료](https://www.jooyon.co.kr/bbs/board.php?bo_table=press&page=16&wr_id=227). USB-C 영상·65W, 포트, 리모컨, VESA 일치. 숫자 픽셀·Hz 미상을 유지 |
| 크로스오버 27ULD950 | [일반 제품 페이지](https://www.crosslcd.co.kr/shop/item.php?it_id=1716533757). 4K60·KVM·스피커·높이·PIP/PBP·VESA 일치. PD65 상품명으로 watts를 채우지 않음 |
| MSI MD271UL | [글로벌 공식 사양](https://www.msi.com/Business-Productivity-Monitor/Modern-MD271UL/Specification). 4K60·입력별 한도·DP Alternate·65W·틸트 일치. 글로벌 사양의 지역 차이 고지를 유지 |

공식 출처의 GB/MY/US/GLOBAL 지역은 한국 실물 SKU 승인과 다르다. 접근 오류에 대한 우회나 대체 검색 요약 사용은 하지 않았다.

## 후기 원문과 요약

| ID | 모델 연결·원문 대조 |
| --- | --- |
| PUR-001 | [원문](https://makeany.tistory.com/97). M1 Air→V32UE의 USB-C 영상·충전, 3008X1692 보기 설정 확인. 이를 실제 신호 해상도·Hz·충전 측정W로 승격하지 않음 |
| PUR-005 | [원문](https://quasarzone.com/bbs/qf_dp/views/515378). 27ULD950, M2 Pro와 Windows HDMI 깜빡임, USB-C에도 증상 유지 일치. USB-C 비교 호스트 미상을 유지. 타인의 환불 댓글은 작성자의 실패 결론으로 사용하지 않음 |
| PUR-006 | [원문](https://quasarzone.com/bbs/qc_user/views/133467). 27ULD950 번들 C-C, Mac 클램쉘 화면·충전 확인. 칩·신호Hz·실측W 미상. 구매 권유 맥락을 사용자 관측과 구분 |
| PUR-014 | [원문](https://seook.tistory.com/m/entry/맥북-4K-모니터-추천-MSI-MD271UL-4K-듀얼-모니터-실제-사용-후기). M2 Air/M4 mini 언급, 케이블 교체 후 증상 해소와 PD 설정 관측 일치. 교체 당시 호스트·케이블 세대 미상. Thunderbolt 케이블 사용을 모니터 Thunderbolt 지원으로 해석하지 않음 |

공식 공급65W와 후기의 충전 인식은 별도 객체다. 후기의 일반 권유·제조사 설명·판매 맥락은 호환 승인 근거가 아니다. 원문 개인정보나 긴 본문은 감사 문서에 복제하지 않았다.

## 실제 실행 결과

- `python3 -m unittest discover -s tests -q`: **319 tests, 2.711초, OK**. v1 CSV·영어 예시·v2 JSONL 검증도 PASS. 로그 `/tmp/connectable-audit-python.log`.
- `npm run test:e2e -- --workers=2 --output=/tmp/connectable-audit-e2e-results`: **62 passed, 28.3초**, 실패·삭제·skip 없음. 로그 `/tmp/connectable-audit-e2e.log`.
- `python3 scripts/build_site_content_v2.py --check`: 생성 일치 PASS. 파생 JS 헤더의 기준 JSON SHA-256도 일치.
- `git diff --check`: PASS. 보호 17파일 SHA-256과 두 화면 archive 8·16파일 manifest 일치. 추적된 data/official·data/rules·data/research·schemas 15파일은 HEAD 바이트와 일치. 미추적 review 원본도 보호 manifest로 확인했다.
- 별도 읽기 전용 Chromium 점검: 6종의 15개 비교 조합 열림, 필터 결과와 3개 가이드 관계 확인. 이는 모든 셀 내용의 정답 검증을 뜻하지 않는다. 초기 점검 스크립트가 선택 전 숨겨진 ‘선택 비우기’를 클릭해 실패했고, 첫 선택 전 클릭을 생략한 점검으로 재실행했다. 제품 테스트 실패로 숨기거나 제품 코드를 수정하지 않았다.

## 발견 문제와 권장 순서

치명적 P0 및 현재 잘못된 공개 호환 판정 P1은 발견하지 않았다. 아래 P2는 배포 전 보강 권고다.

1. **P2 — batch 검증기 근거와 payload 검증 공백.** `scripts/build_site_content_v2.py:validate_monitor_batch`는 빈 fact.source_refs를 허용한다. 같은 함수는 VIDEO_PROFILE payload를 `{watts:-1}`로 바꾼 잘못된 입력도 허용했다. 메모리 복사에서 재현했으며 파일 변경 없음. 현재 사실은 정상이고 전체 테스트가 통과하지만 미래 잘못된 데이터가 같은 경로로 들어올 수 있다. nonempty 근거·property별 payload·단위·범위·날짜/URL 형식 검증과 부정 회귀 테스트를 우선 권고한다.
2. **P2 — 공개 파생 참조 무결성 손실.** `web/derive-site-content.py`는 features.fact_id를 제거하지만 capabilities.feature_refs는 유지한다. 브라우저 실제 객체에서 신규 3종의 참조 ID에 해당하는 fact ID가 모두 누락된 것을 확인했다. 원본 JSON 참조는 정상이며 현재 화면은 요약을 읽어 작동한다. 공개 projection에서 참조를 유지할지 제거할지 계약을 확정하고 대상 존재 테스트가 필요하다.
3. **P2 — 비교 검증이 요약문에 의존.** `web/site-v2.js:comparisonRows/openComparison`은 payload에서 값을 렌더링하지 않고 summary를 출력한다. 따라서 잘못된 단위·값의 요약이 payload와 달라도 통과할 수 있다. Dell의 90W upstream과15W downstream은 문구로 구분되지만 같은 PD 행에 있으며, 공급 전력/포트 역할별 정규화 비교는 없다. 자동 우열 계산은 없으므로 현재 단위가 다른 값을 계산한 오류는 발견하지 않았다. 요약-payload 일치·서로 다른 포트/조건·Cross PD65 미상·MSI 입력별 값의 셀별 독립 oracle 검사를 권고한다.
4. **P2 — 공식 원문 재확인 미완료.** U2723QE와 LG 상세 사양은 이번 직접 대조가 완료되지 않았다. 접근이 정상인 시점의 수동 재검토를 권고하며 현재 데이터 변경은 하지 않는다.
5. **P3 — 가이드 관련성 약함.** build()가 세 가이드 모두에 6개 모니터와 PUR-001/008/013을 동일하게 넣는다. 없는 ID는 아니지만 USB-C 가이드의 G2724D 링크 등은 왜 관련됐는지 설명이 없다. 주제별 관계와 포함 사유를 편집하고 의미 검사를 추가하는 것이 좋다.
6. **P3 — 필터가 제품의 완전한 사양 목록은 아님.** 높이 조절 필터는 저장 자료상 Cross 한 모델만 표시한다. G2724D의 공식 높이 조절 사양은 수집되지 않아 결과에서 빠진다. 기존 ‘공식 자료에서 확인하지 못함’은 이번 감사 시점의 직접 발견과 별개로 과거 수집 범위 표현이다. ‘현재 수집한 기능’ 범위 고지와 별도 승인된 결측 보강을 권고한다.
7. **P3 — 재현 기준은 미커밋 작업 트리.** commit SHA만으로 결과 재현 불가. 승인 후 논리적 커밋과 lockfile·브라우저 환경·자료 해시를 함께 고정해야 한다. 실제 기기·스크린리더·광고·제휴·공개 SEO·사진 권리는 이 감사의 검증 범위 밖이다.

## 테스트 범위 평가

319개 전체는 기존 코퍼스·공식 자료·경로 모델 회귀를 포함한 총합이며 모니터 기능 전용 319개가 아니다. E2E 62개는 새 홈 14개 시나리오×desktop/mobile 28개, 내부 검토22개, legacy12개다. desktop/mobile은 Chromium 환경이며 실제 Safari/iPhone 검증을 뜻하지 않는다.

출처/원본 보존, 잘못된 모델 연결 거부, 사용자 근거의 공식 사양 사용 거부, 두 개 비교 제한, UNKNOWN 문구, 키보드·axe·CSP·안전 링크·악성 데이터·그룹화·뒤로가기·목차 초점 이동은 포함된다. 반면 현재 기대값 상당수가 같은 content JSON에서 계산되므로 원문과 데이터가 함께 잘못됐을 때 잡지 못한다. 이번 직접 원문 감사가 이를 보완했지만, 모든 feature/filter 조합·15쌍 모든 셀·가이드의 의미적 관련성·빈 근거/잘못된 payload·projection 참조는 기존 회귀 테스트로 충분히 검증되지 않는다.

다음 순서는 **검증기/참조 계약 보강 승인 → 회귀 테스트 보강 → 공식 출처 재확인·편집 관련성 검토 → 로컬 재감사**를 권고한다. 새 기능 확장이나 공개 운영 전에 이 항목들을 먼저 처리한다. 감사에서 발견한 문제는 승인 없이 수정하지 않았다.

## Audited working-tree SHA-256

| File | SHA-256 |
| --- | --- |
| `data/site/content-v2.json` | `edec539d4a58ea5c01a20b81f334e5d64dcd93fc6ec42c061c2e2fd11ba8f2c7` |
| `data/site/monitor-batch-1-sources.json` | `a0f942da7cf765b8075cf5002ab43f7e9f72d23d4c09f0aa3b2eea534642ede7` |
| `scripts/build_site_content_v2.py` | `c2fece6d45936736968ef936365624765505ac94935dbdb926d6243265e7c92b` |
| `web/derive-site-content.py` | `5e404a17ff8f5d72b1dcb5e45784a19afcd965e9755301c4fd6d8166ffe6f65b` |
| `web/site-v2.js` | `1be5d4d1acdff29a455f9625af7edee8d24946e0fbcbcfd7bad39799173c4398` |
| `web/site-content-v2.js` | `e1a63961fd95258b70057a1dd155bd8a0bb28fa2871f6e2db061fdd67f89ca3d` |
| `tests/test_site_content_v2.py` | `80193f6fd61f1c53ce05b644871e73e85810fa2b927b706e83d4baaf4ef27ab0` |
| `tests/e2e/site-v2.spec.js` | `1b7c70e45304ae61bc8acbd1dc8bf69533a586a15512e56dc459cdf76f092614` |
