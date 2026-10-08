# 공식 사양 및 수동 검토 배치

확인일: 2026-10-09. 브랜치: `codex/official-spec-manual-review`.
기준 커밋: `90136e84056bade3a48e1e57f442f96f9924f5da`.
데이터·검증 코드 커밋: `90a2d65`. 최종 커밋은 이 보고서를 추가한 커밋이며 `git log -1`로 확인한다.

## 처리 방식

기존 [의미 검증 보고서](PRODUCT_SEMANTIC_VALIDATION_REPORT.md)의 수동 검토 두 항목과 Dell/LG 사실을 재검토했다. 확인 결과는 [별도 검토 데이터](../data/official/spec_manual_review_2026-10-09.json)에 저장했다. 원본 fact의 정렬 JSON SHA-256을 연결하여 원본과의 대응을 검증한다. 원본 catalog, 사이트 요약, 질문 코퍼스는 수정하지 않았다.

`VERIFIED_MODEL_SCOPE`는 공식 페이지에 해당 모델의 사실이 명시됐다는 뜻이다. 지역별 SKU 동일성, 연결 호환성, 한국 판매 제품의 동일 사양을 승인하는 상태가 아니다. 모든 항목은 `variant_match=UNKNOWN`, `public_status=UNKNOWN`, `usable_for_compatibility=NO`이며 catalog 적용 상태는 `NOT_APPLIED`다.

## 수동 검토 2건

| 원본 fact | 원본 요약·typed 값 | 직접 확인 결과 | 미확인 필드 및 처리 |
|---|---|---|---|
| `jooyon-v32ue:site-1` | 32형 IPS, 4K UHD 표기; PANEL, resolution_label=4K UHD; 수치 UNKNOWN | 공식 보도자료의 4K UHD 표기와 일치 | width, height, refresh_hz는 문서의 숫자 명시를 확보하지 못함. PARTIALLY_VERIFIED 유지 |
| `crossover-27uld950:site-2` | USB PD 지원; PD65는 상품명; OFFER, watts/interface UNKNOWN, PRODUCT_LABEL_ONLY | 공식 상품명 PD65와 USB PD 지원 표기를 확인 | watts, interface 및 OFFER 방향은 이 근거만으로 확정하지 못함. PARTIALLY_VERIFIED 유지 |

주연테크 공식 자료: [제품 출시 보도자료](https://www.jooyon.co.kr/bbs/board.php?bo_table=press&page=16&wr_id=227)의 V32UE 본문. 4K UHD라는 명칭을 자동으로 숫자 해상도·주사율로 확장하지 않았다.

크로스오버 공식 자료: [27ULD950 제품 페이지](https://www.crosslcd.co.kr/shop/item.php?it_id=1716533757)의 상품명·요약정보. 상세 이미지 확인은 실패했다. PD65라는 이름을 65W 전력 제공의 독립 근거로 사용하지 않았다. 기존 OFFER 값도 검증 완료 필드로 승격하지 않았다.

## Dell U2723QE

공식 근거: [Dell 폴란드 제품 페이지](https://www.dell.com/pl-pl/shop/monitor-dell-ultrasharp-27-4k-z-koncentratorem-usb-c-u2723qe/apd/210-bcxk/monitory-i-akcesoria-do-monitor%C3%B3w).

문서 위치: `Rozdzielczość / częstotliwość odświeżania`, `Interfejsy` / `Złącza`.

기존 4개 fact에 대응하는 다음 사실을 모델 범위에서 재확인했다.

- 기본 해상도·주사율 3840×2160, 60Hz.
- USB-C upstream의 DP 1.4 Alt Mode.
- 해당 upstream 전력 공급 최대 90W.
- 별도 USB-C downstream 전력 공급 최대 15W.

90W와 15W는 서로 다른 포트 역할이다. USB-C라는 커넥터 이름만으로 모든 USB-C 포트를 영상 입력으로 취급하지 않았다. 별도 데이터 upstream의 영상 기능은 UNKNOWN으로 남긴다. 포트별 영상 타이밍, DSC·lane 조건, DP 출력의 routing, PD 전압·전류 profile도 미확인이다. PL 주문 코드와 기존 GB 또는 한국 SKU의 동일성은 확보하지 못했다.

## LG 27UP850-W

주 근거: [LG 라트비아 제품 페이지](https://www.lg.com/lv/monitori/lg-27up850-w)의 `SAVIENOJAMĪBA` 및 USB-C 소개 문단.

6개 검토 fact를 기록했다. 기존 USB-C DP Alt Mode 사실을 재확인했고, 최대 96W 공급, HDMI·DP·USB-C 각각의 최대 3840×2160/60Hz, DP 입력 버전 1.4를 별도 typed 자료로 추가했다. 소개 문단은 최대 전력을 명시하므로 새 검토 자료는 `UP_TO`로 표현했다. 기존 MY 자료의 `RATED` 원본을 덮어쓰거나 두 표현을 자동 충돌 판정하지 않았다. 실제 협상 전력이나 호스트 충전 보장은 아니다.

보조 확인: [LG 포르투갈 제품 페이지](https://www.lg.com/pt/monitores/uhd-4k-5k/27up850-w/)의 `CONECTIVIDADE` 표는 같은 수치를 보여준다. 다만 소개 본문에 **27UP850N** 모델명이 섞여 있다. 출처의 모델 표기 불일치로 기록했고, 이번 typed assertion의 근거에는 PT 페이지를 사용하지 않았다. 수치 충돌이 확인됐다는 뜻은 아니다.

LV 모델 페이지와 기존 MY 또는 한국 SKU 동일성, PD 전압·전류, DSC·lane 조건은 미확인으로 유지한다.

## 접근 실패와 확인 범위

- 기존 Dell GB 페이지는 이번 도구에서 본문 재확인이 되지 않았다.
- 기존 LG MY 페이지는 timeout으로 재확인하지 못했다.
- [Dell 공식 지원 목록](https://www.dell.com/support/product-details/en-nz/product/u2723qe-monitor/resources/manuals)에서 사용자 설명서 위치는 확인했다. [설명서 PDF](https://dl.dell.com/content/manual12109242-dell-u2723qe-monitor-user-s-guide.pdf?language=en-us)는 웹 도구 크기 제한 이후 일반 다운로드에서도 HTTP 403을 반환했다. 본문을 읽지 못했으며 검증 근거로 쓰지 않았다.
- Dell 공식 es-mx 데이터시트도 HTTP 403으로 제외했다.
- LG UK/US 지원 페이지에서는 설명서 본문이나 다운로드 자료를 확보하지 못했다.

접근 제한은 우회하지 않았다. 검색 결과 요약, 비공식 설명서 사본, 제품명 추론으로 누락값을 채우지 않았다. 원본 출처의 확인일도 소급 갱신하지 않았다.

## 변경 파일과 검증

- [검토 데이터](../data/official/spec_manual_review_2026-10-09.json): 출처 8개, 모델 범위 assertion 10개, 부분 수동 검토 2개, 남은 미확인 항목.
- [검증기](../scripts/validate_official_spec_review.py): 공식 제조사 도메인·모델·직접 확인 상태, typed payload, 확인 필드, 원본 fact hash, 참조·ID·날짜·URL 검사. 공개 판정 및 catalog 적용 승격 거부.
- [회귀 테스트](../tests/test_official_spec_review.py): 8개. 접근 실패 자료의 근거 사용, 다른 모델·비공식 출처, UNKNOWN 승격, 원본 hash 변조, 공개 호환성 승격을 거부한다.
- 본 보고서.

실행 결과:

- `python3 -m unittest discover -s tests -q`: **356개 PASS**, 3.517초. 기존 348개와 새 8개 모두 통과. v1 CSV 및 v2 JSONL 검증도 통과.
- `python3 scripts/validate_official_spec_review.py`: **PASS**, assertion 10개와 부분 검토 2개.
- `npm run test:e2e`: 결과는 아래 최종 검증 기록 참조. 추적 이미지 덮어쓰기를 피하기 위해 커밋 스냅샷의 별도 임시 폴더에서 실행했다.
- 원본 데이터·스키마·archive·web 64개 SHA-256: 작업 전후 모두 동일.
- 개인정보·비밀값 및 내부 링크 검사, JSON 파싱, `git diff --check`: 아래 최종 검증 기록 참조.

테스트는 근거 참조 계약과 회귀를 검사하며 공식 문장 자체의 진실이나 지역 SKU 동일성을 자동으로 승인하지 않는다. 새 원본 자료가 UI에 적용되지 않았으므로 브라우저 테스트는 기존 화면 보존을 검증한다.

## 남은 위험과 다음 권장 작업

1. 한국 판매 SKU와 지역별 공식 자료를 명시적으로 바인딩한 뒤에만 사이트 데이터 반영을 검토한다.
2. 주연테크 숫자 해상도·주사율, 크로스오버 실제 PD 전력·방향을 명시한 공식 설명서를 확보한다. 상품명만으로 해결하지 않는다.
3. LG 기존 RATED와 새 UP_TO 표현의 출처 의미를 검토하고 별도의 승인된 수정으로 처리한다.
4. 공식 문서의 모델 혼입은 제조사 페이지라도 발생할 수 있다. 자료 위치와 적용 모델을 함께 검토한다.

근거가 확보된 모델 범위 사실은 기록했지만 수동 검토 두 건은 부분 해결이다. 공개 호환성 판정, 엔진 확대, 광고·제휴 활성화, 배포, main 병합은 수행하지 않았다. 작업 시작 당시 README·DECISIONS와 별도 미추적 문서는 사용자 변경으로 보존하고 커밋에서 제외했다.

## 최종 검증 기록

- 브라우저: **66개 PASS**, 24.0초.
- JSON 파싱·문서 내부 경로 5개: PASS.
- 새 데이터·보고서의 이메일, 전화번호, GitHub/AWS 토큰, private key 패턴 검사: PASS. 사실 요약을 수동으로 검토했으며 작성자명이나 원문 전체를 저장하지 않았다. 패턴 검사는 모든 개인정보 형태를 포괄하는 보증은 아니다.
- `git diff --check`: PASS. 새 자료와 검증 코드의 커밋 diff 및 보고서를 직접 검토했다.
- 원본 64개 파일 hash 일치: PASS. README·DECISIONS의 기존 사용자 변경은 이번 커밋에 포함하지 않았다.
