# P1 데이터 신뢰성 결함 수정

확인일: 2026-10-09. 기준: `codex/official-spec-manual-review`의 `57dbf2c0a9aed2da85c5f64d674fd737189ee09e` 및 로컬 CONNECTABLE_INTEGRATION_READINESS_REPORT.md.
작업 브랜치: `codex/p1-data-trust-fix`. 수정 커밋: `07197a0`, 공식 사이트 내부 사용자 게시판 제외 보강: `53004d1`. 최종 보고서 커밋은 이 파일을 추가한 커밋이며 완료 응답에 SHA를 기록한다.

## 결함별 원인과 수정 전 재현

| 결함 | 원인 | 수정 전 입력 및 결과 |
|---|---|---|
| 후기 모델 연결 | node.display_model과 link.reported_model만 비교하고 연결 대상 제품 모델과의 대응을 검사하지 않음 | 두 값을 동시에 OTHER-MODEL로 변경해도 기존 대상 제품으로 연결됨. 거부를 기대하는 테스트 FAIL |
| 공식 출처 분류 | source_type=MANUFACTURER_*와 HTTPS 자기 선언만 검사 | 제조사 URL을 example.com으로 변경해도 승인 경로 통과. 거부를 기대하는 테스트 FAIL |

먼저 [회귀 테스트](../tests/test_p1_data_trust.py) 5개를 작성하고 기존 코드에서 실행했다. **잘못된 입력 거부 테스트 4개 FAIL, 정상 데이터 테스트 1개 PASS**였다. 핵심 두 결함 외에 같은 결함을 파생 콘텐츠 검증 경로에서도 재현했다. 실패 원인은 모두 `ValueError not raised`다. 임시 로그: `/tmp/connectable-p1-red.log`. 원본에 가짜 값을 쓰지 않고 메모리 복사만 변형했다.

## 수정 1: 후기와 제품 모델 연결

[공통 신뢰성 검사](../scripts/data_trust.py)의 `linked_model_identity`를 batch 및 full/public 콘텐츠 검사에 적용했다.

- 후기 DISPLAY node, 연결 기록의 reported_model, 연결 대상 제품 모델을 함께 대조한다.
- monitor_ids 자체도 해당 모델의 DISPLAY node로 뒷받침돼야 한다.
- `주연테크 V32UE`, `크로스오버 27ULD950`, `MSI MD271UL`은 기존 직접 확인된 네 후기의 표기다. 이 세 표기와 제품의 기본 모델명 대응만 명시적 대응표로 인정한다. 제조사 접두어를 모든 문자열에서 자동 제거하는 규칙은 만들지 않았다.
- 등록되지 않은 별칭, 대소문자·공백 차이, SKU 접미사, V32UE-E 같은 변형, UNKNOWN은 동일 모델로 추정하지 않는다. `MANUAL_REVIEW` 오류로 자동 연결·생성을 중단한다.
- 수동 검토 대상이라는 진단만 반환하며 원본 데이터의 상태나 결론을 자동 수정하지 않는다. 별도 검토 후 근거가 있는 대응표만 추가할 수 있다.
- 모델 표기 대응은 실물 SKU·리비전 동일성 승인과 다르다. MODEL_ONLY / variant_match UNKNOWN은 그대로 유지한다.

초기 수정에서는 모든 문자열의 원시 일치를 요구해 정상 후기의 제조사 포함 표기를 거부했다. 정상 회귀 검사가 이를 발견했고, 원본을 변경하거나 기준을 느슨하게 풀지 않고 기존에 확인된 세 대응을 명시적으로 등록했다. 이후 정상·비정상 테스트를 다시 실행했다.

## 수정 2: 공식 URL 권위 검증

`official_url_status`는 URL 파서로 추출한 **정확한 hostname**과 제조사별 명시적 제품·지원 경로를 대조한다. 문자열 포함이나 도메인 suffix만으로 임의 하위 도메인을 인정하지 않는다. 반환값 `OFFICIAL_URL_SCOPE`는 URL 권위 범위 확인이며 제품 사양·호환성 승인 상태가 아니다.

허용 범위:

| 제조사 | 등록 호스트 및 경로 |
|---|---|
| Dell | www.dell.com 지역 shop/지원 경로, dl.dell.com/content/ 공식 문서 |
| LG | www.lg.com 지역 monitors/monitori/monitores/support 경로 |
| 주연테크 | www.jooyon.co.kr 보도자료 board.php, bo_table=press와 게시물 ID |
| 크로스오버 | www.crosslcd.co.kr 또는 crosslcd.co.kr의 shop/item.php와 상품 ID |
| MSI | www.msi.com의 Business-Productivity-Monitor/ 또는 support/ |

기존 정상 URL은 모두 통과한다. 미등록 공식 호스트·CDN도 자동 추정하지 않고 UNKNOWN으로 남긴다. 제조사 사용자 게시판이 공식 도메인에 있다는 이유로 제조사 사양 근거가 되지 않도록, 주연테크의 다른 board와 크로스오버 사용자 board는 허용하지 않는다. 미등록 제조사는 자동 승인하지 않는다.

검사하는 위험:

- evil.example 내 제조사 이름, dell.com.evil.example, 유사 철자, 미등록 하위 도메인.
- userinfo를 사용한 위장, 비HTTPS, 비표준 포트, hostname 뒤 점, 역슬래시·공백·C0 제어문자.
- 리다이렉트 경로, 미등록 query key, 중복 query key, query 속 외부 URL 및 중첩 URL 인코딩.
- 인코딩된 경로 구분자·dot segment. 정상 비ASCII 제품명 URL 인코딩은 허용한다. Dell 폴란드 원본 URL도 정상 회귀로 검사했다.
- 선택적으로 기록된 redirect_chain/final_url의 모든 목적지. 외부로 나갔다가 공식 호스트로 돌아오는 체인도 UNKNOWN으로 거부한다.

검사는 원본·파생 모니터 출처와 batch 제품 근거에 적용했고, [공식 재검토 검증기](../scripts/validate_official_spec_review.py)도 동일한 URL 권위 규칙을 사용하도록 했다. 기존 typed 검증, 출처 record/URL 참조, 원본 hash 및 공개 승격 금지는 유지했다. 후기 원문 사이트를 제조사 도메인으로 제한하지 않는다.

### 공식 사이트 관계 확인

이번에는 다음 공개 공식 페이지의 도메인·브랜드·제품/문서 관계를 직접 확인했다. 제품 숫자 사양이나 모델 별칭을 새로 수집해 원본에 추가하지 않았다.

- [주연테크 보도자료](https://www.jooyon.co.kr/bbs/board.php?bo_table=press&page=16&wr_id=227): 사이트 회사 표시 및 V32UE 출시 제목/본문.
- [크로스오버 상품 페이지](https://www.crosslcd.co.kr/shop/item.php?it_id=1716533757): 브랜드·제품 제목·회사 안내.
- [MSI 사양 페이지](https://www.msi.com/Business-Productivity-Monitor/Modern-MD271UL/Specification): 공식 제품 제목/사양 경로.
- [LG 모델 페이지](https://www.lg.com/lv/monitori/lg-27up850-w): LG 모델 페이지와 지역 경로.
- [Dell 공식 지원 문서 목록](https://www.dell.com/support/product-details/de-ch/product/u2723qe-monitor/resources/manuals): www.dell.com 내 지역 리다이렉트와 dl.dell.com 공식 설명서 링크를 확인했다. PDF 본문을 재확인했다고 기록하지 않았다.

**리다이렉트 한계:** 검증기는 오프라인·읽기 전용이다. 실시간 HTTP 요청이나 DNS 소유권 확인, 모든 endpoint의 open redirect 탐색을 수행하지 않는다. legacy DIRECT_CHECK에는 실제 체인 메타데이터가 없으므로 체인을 만들어 넣거나 최신 HTTP 목적지 검증 완료로 표시하지 않는다. 알려진 우회 형태와 기록된 목적지의 권위는 검사하지만, 향후 수집 시 실제 요청/최종 URL 기록과 사람 확인이 필요하다. 공식 URL 범위 통과만으로 출처 내용을 참이라고 승인하지 않는다.

## 정상/비정상 입력과 회귀 결과

새 테스트 **14개**를 추가했다. subTest로 다음 여러 입력을 함께 검사한다.

- 정상 batch·full 콘텐츠와 실제 public projection: PASS, 입력 변경 없음.
- 공동 변경된 후기 모델/대상 불일치: 거부.
- 미등록 별칭·SKU·모델 변형·UNKNOWN: MANUAL_REVIEW로 거부.
- 비제조사·유사/위장 도메인·다른 제조사 URL: UNKNOWN으로 거부.
- 미등록 redirect 경로/query·중첩 외부 URL·기록된 외부 최종 목적지/체인: 거부.
- 등록된 제품/지원 URL과 공식 문서 목적지: URL 범위 검사 PASS.
- 공식 도메인 내 미등록 사용자 게시판: UNKNOWN.
- 별도 공식 재검토 데이터: 기존 정상 자료 PASS, 임의 하위 도메인 거부.

현재 정상 데이터 6모니터·38연구기록·3가이드와 공식 검토 assertion 10개·부분 검토 2개가 거부되지 않는다. 문장·수치·현재 UI 출력은 변경하지 않았다.

## 전체 테스트 및 보존

최종 코드 커밋 `53004d1`을 `git archive`로 임시 폴더에 풀고 전체 검사를 수행했다. 기존 스크린샷이 E2E에 의해 덮어써지지 않도록 테스트를 저장소 밖에서 실행했다. 동일 package-lock 설치 의존성과 Chromium을 사용했다.

- `python3 -m unittest discover -s tests -q`: **370 PASS**, 4.427초(기존356 + 신규14). v1 한국어 CSV·영어 예시·v2 JSONL 검사도 PASS.
- `npm run test:e2e`: 최종 결과는 아래 기록 참조.
- `python3 scripts/build_site_content_v2.py --check`: PASS, 기존 JSON 바이트 재현 일치.
- `python3 scripts/validate_official_spec_review.py`: PASS, 모델 범위 assertion 10개·부분 검토2개.
- 작업 시작 hash manifest와 비교해 기존 변경 파일은 검증 코드 3개뿐이다. catalog·코퍼스·rules·schemas·site JSON·web·archive·사용자 문서/미추적 파일은 보존했다.
- `git diff --check`, 보고서 내부 경로 및 개인정보·비밀값 검사: 아래 기록 참조.

## 변경 파일

- [data_trust.py](../scripts/data_trust.py): 명시적 모델명 대응 및 공식 URL 권위 정책.
- [build_site_content_v2.py](../scripts/build_site_content_v2.py): batch의 대상 모델 및 제품 출처 검사.
- [site_content_validation.py](../scripts/site_content_validation.py): 원본/공개 projection의 제품 연결·출처 검사.
- [validate_official_spec_review.py](../scripts/validate_official_spec_review.py): 같은 공식 URL 정책 적용.
- [test_p1_data_trust.py](../tests/test_p1_data_trust.py): 수정 전 재현 및 정상/악성 입력 회귀.
- 본 보고서.

로컬의 기존 통합 감사 보고서와 README·DECISIONS·GP 관련 사용자 변경은 이번 커밋에 포함하지 않는다. 감사 보고서는 아직 원격에 기록되지 않은 상태여서 이 보고서에는 해당 로컬 문서의 파일명만 기록한다.

## 남은 위험

- P1 두 검증 결함은 해결했다. source_status, 모델 원문 내용 및 직접 확인의 진실성까지 형식 검사로 증명할 수는 없다. 알려진 공식 호스트/경로와 모델명 대응표의 추가는 근거 검토가 필요하다.
- 공식 문서 경로가 바뀌면 자동 통과시키지 않고 수동 검토한다. 보수적 제한으로 정상 새 URL이 UNKNOWN이 될 수 있다.
- 지역 SKU·리비전 미확인, LG RATED/UP_TO, Cross 전력·방향의 부분 검토, 수동 문장 승인 gate, site public_status/protocol 계약, CI push 범위 등 직전 감사의 P2는 이번 범위 밖이므로 변경하지 않았다.
- 브라우저 테스트는 Chromium desktop/mobile 회귀이며 제품의 실물 연결 정확성·공개 호환 승인 검사가 아니다. 공개 UNKNOWN·골든 승인0 정책을 유지한다.

main 병합·공개 배포·광고/제휴·새 화면 기능·원본 수정·강제 push는 수행하지 않았다.

## 최종 검증 기록

- 브라우저 **66 PASS**, 38.2초.
- 기존 hash manifest 161개 중 승인된 검증 코드 3개만 변경; 나머지 158개는 바이트 일치.
- 문서 로컬 링크·개인정보/비밀값 패턴·git diff 검사 PASS. 실제 원문 전체나 사용자명을 저장하지 않았다. 패턴 검사는 모든 자유문장 개인정보를 증명하는 검사는 아니다.
- 보고서 commit 후 `codex/p1-data-trust-fix`만 원격에 push한다. main ref는 변경하지 않는다.
