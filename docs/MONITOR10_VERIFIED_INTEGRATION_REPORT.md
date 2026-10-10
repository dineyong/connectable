# Monitor10 전달 자료 검토 및 확인 항목 통합 보고

확인일: 2026-10-11. 브랜치: `codex/monitor10-verified-integration`. 시작 커밋: `e01638f3f710d46d082bec6b59aeb00d1e756579`. main 병합·공개 배포·호환성 승인 대상이 아니다.

## 입력과 검증 범위

사용자 전달 파일은 `connectable_monitor10_verified_20261010.json`이다. SHA-256은 `ea6ba0de4a31fb128e7c1672630ae6dd467a2262baaf887523e18b6e148d28af`다. 함께 전달된 요약 파일 SHA-256은 `83fe12793b6d89a20969c00b1c9a45d2dc85d0cafc2b2cda5b6665bc65261433`이며 상위 작업자가 확인했다. 원본을 수정하지 않고 읽었다.

- 모델 10개, official_identity + official_specs 객체 **340개**, 사용자 관측 **19건**을 실제 구조에서 집계했다.
- 세 조사 작업이 모델마다 8개씩 **80개 선택 필드 묶음**을 공식 원문과 다시 대조했다. 이 수는 340개 전체 검증 완료나 80개 신규 사양이라는 뜻이 아니다. 복합 값·지원 페이지 연결·별도 모델 구분도 포함한다.
- 재확인 목록에 없는 전달 사실, 후기, 문서의 DIRECT 표기는 자동 승계하지 않는다. 공식 사양과 사용자 경험을 별도 계층으로 유지한다.
- 사용자 관측 19건은 공개 승인·구매 인증·독립 사용자 19명·긍정 후기 19개가 아니다. 기존 저장 후기와 중복된 원문도 포함한다. 이 검토자의 직접 본문 재확인 3건과 상위 작업자의 27GP850 재확인 1건은 신규 후기 수입 건수와 구분한다.
- 기존 30종 공식 원본 및 기존 사이트 자료를 덮어쓰지 않는 추가 검토 페이지 방식으로 통합한다. 한국 공식 자료를 확보했어도 기존 해외 SKU와 자동 병합하지 않는다.

상세 조사 기록은 [LG·M27Q](MONITOR10_LG_GIGABYTE_REVIEW.md), [Dell·ASUS·M32U](MONITOR10_DELL_ASUS_M32U_REVIEW.md), [MSI·BenQ·Crossover](MONITOR10_MSI_BENQ_CROSSOVER_REVIEW.md)를 따른다. 각 문서에 실제 URL·문서 위치·재접근 실패가 있다.

## 모델별 기존 자료 연결과 범위

| 전달 선정명 | 기존 자료 | 이번 재확인 범위·식별 관계 | 병합하지 않는 경계 |
|---|---|---|---|
| 27GP850 | `monitor:lg-27gp850-b`, ES | 한국 27GP850 제품 + 27GP850-BB 지원 페이지의 제품 링크 | 한국 BB 지원 연결은 해외 -B 및 전체 한국 공장 SKU 동치가 아님 |
| 27GS95QE | `monitor:lg-27gs95qe-b`, GB | 한국 27GS95QE 제품 + 27GS95QE-BB 지원 연결 | 해외 -B·한국 유통 SKU·하드웨어 리비전 미확인 |
| 32GS95UE | `monitor:lg-32gs95ue-b`, CA | 한국 32GS95UE 제품 + 32GS95UE-BB 지원 연결 | 해외 -B 동치 미확인; UHD240/FHD480은 대체 모드 |
| M27Q 2.0 | `monitor:gigabyte-m27q-rev-1-0`, Global은 **다른 리비전** | 한국 제조사 M27Q Rev.2.0 표 | Rev.1.0을 수정하지 않음. 유통명 제이씨현과 정확 Rev.2 SKU 연결 미확인 |
| M32U | `monitor:gigabyte-m32u`, Global | 한국 제조사 페이지·한국어 설명서 | Global 원본을 한국 유통 SKU 승인으로 바꾸지 않음 |
| U2724D | `monitor:dell-u2724d`, US | 현재 한국 판매 페이지 PTXMV/g5jtmg/u2724d_monitor + 공식 설명서 | 과거 주문·US SKU 동일성 미확인. U2724DE와 별개 |
| XG27AQDMG | `monitor:asus-xg27aqdmg`, US | 한국 모델 페이지·한국어 설명서 | XG27AQDMGR Gen2 별개. 한국 유통 SKU·하드웨어 리비전 미확인 |
| MPG 274URF-QD | 기존 30종 및 6종 목록에 없음 | 글로벌 MPG 274URF QD 사양 + 한국어 모델3CC2 설명서 | MAG/QD-OLED 제품과 별개. 문서 V1.1은 하드웨어 리비전 아님 |
| BenQ MOBIUZ EX2710Q | `monitor:benq-ex2710q`, CA | 이번에도 캐나다 공식 표. 한국 URL 상세 재접근 실패 | 한국 SKU로 승격 금지. Nano IPS라고 확대하지 않음 |
| Crossover 27ULD950 | 30종에는 없음. 구 사이트 `product:crossover-27uld950`, KR | 한국 공식 HTML 요약 | 별도 유통 SKU/하드웨어 리비전 미확인. 이미지 전용 값 재확인 대기 |

기존 근거 파일은 [official_specs.json](../data/research/monitor-expansion/official_specs.json), [content-v2.json](../data/site/content-v2.json)이다. 동일 해상도·주사율이라는 이유로 접미사나 국가가 다른 제품의 결측을 메우지 않는다.

## 주요 확인 내용과 보류

| 대상 | 이번 확인한 대표 내용 | 반드시 남길 제한 |
|---|---|---|
| LG 27GP850 | QHD Nano IPS, DP165/OC180 및 HDMI144 | OC의 DP1.4 GPU 조건. cm 원문을 임의 인치 반올림하지 않음 |
| LG 27GS95QE | QHD OLED240, HDR peak1300/800 | 3% APL 및 typical/minimum 의미 보존 |
| LG 32GS95UE | UHD240 또는 FHD480, HDR peak1300/1040 | 1.5% APL. 두 모드를 동시 출력으로 해석 금지 |
| M27Q Rev.2 | 165/OC170, USB-C Alternate Mode upstream, PD up to10W | 설명서의 대기15W는 이번 표 시각 확인 실패. 웹10W만 해당 출처 범위로 표시 |
| M32U | HDMI4K144의 DSC4:4:4 또는4:2:0, DP4K144, USB-C 입력 선택, 전원 프로파일 | 프로파일과 별도 전원 권고를 명시적 `max_w=18`로 승격하지 않음 |
| Dell U2724D | QHD120 IPS Black, USB-C upstream data-only, downstream15W | HDMI FRL/DSC 미지원 각주를 DP 전체 주장으로 확대 금지. USB-C host충전과 구분 |
| ASUS XG27AQDMG | 26.5인치 WOLED, 패널240, QHD HDMI144/DP240 | 웹 HDMI주파수40–144와 설명서 FHD240 행의 범위 검토. 해상도 없는 HDMI최대144 주장 금지 |
| MSI MPG 274URF QD | 27 Rapid IPS4K160, DP1.4a/HDMI2.1, USB-C DP Alt Mode 최대65W | 높이130/110 충돌. USB-C 데이터 미지원/KVM Type-C 입력 설명 충돌 |
| BenQ EX2710Q | 27 IPS QHD165, 일반250/HDR peak400, HDMI2.0/DP1.4 | CA 근거 유지. 일반250을 SDR전용으로 바꾸지 않음. 타이밍 표 열 시각 검증 미완료 |
| Crossover 27ULD950 | HTML의27 IPS4K60, VESA75, 스탠드기능, USB PD지원 | PD65 상품명만으로 실제65W 확정 금지. 400cd의 SDR/HDR/typical/peak 미확인 |

### 충돌의 상태도 구분한다

- **직접 재확인한 충돌:** MSI 높이 설명서130mm/글로벌110mm, USB-C 데이터와 KVM 설명. 하나를 선택해 덮어쓰지 않는다.
- **정리 전 채택 보류:** Dell RJ45는 한국 일반필드 ‘있음’과 상세 포트 목록 간 범위 문제다. 목록 미기재로 false도 만들지 않는다.
- **범위 검토:** ASUS HDMI는 해상도 조건에 따라 달라진다. 설명서450nits의 모드 미지정과 웹 HDR1300도 같은 시험 조건으로 간주하지 않는다.
- **전달 자료상 충돌·이번 재확인 실패:** Crossover 이미지 DP1.4/1.2, 스위블 ±30/±90, 높이 `0~110m`. 직접 본 충돌인 것처럼 기록하지 않고 pending 상태를 유지한다. PD qualifier도 UNKNOWN이다.

Crossover 이미지는 약16MB로 해당 조사 도구의 크기 제한 오류를 반환했고, 담당 조사 세션에서 브라우저를 사용할 수 없어 픽셀을 재확인하지 못했다. BenQ 한국 상세는404, 일부 PDF screenshot은 픽셀이 반환되지 않았다. 접근 실패를 자료 없음·미지원·원문 오류로 판정하지 않는다. 로그인·CAPTCHA·차단을 우회하지 않았다.

## 사용자 관측의 처리

이번에 실제 본문을 재확인한 것은 [LG 27GP850 후기 이벤트 글](https://quasarzone.com/bbs/qc_user/views/131513), [BenQ 후기](https://quasarzone.com/bbs/qf_dp/views/522348), [Crossover 맥북 사용 후기](https://quasarzone.com/bbs/qc_user/views/133467), [Crossover 3주 후기](https://quasarzone.com/bbs/qf_photo/views/919113) 4개다. LG 글은 DP 165Hz 설정에서 개인 사용 만족을 보고하며 후기 이벤트 제목을 명시한다. 전달 요약의 주요 맥락과 일치하나 공식 사양·PD 실측·독립 구매 인증·협찬 없음으로 승격하지 않는다. 기존 URL과 중복 여부를 확인하기 전 신규 후기 수로 세지 않는다.

상위 작업자는 별도로 [27GP850 후기](https://quasarzone.com/bbs/qc_user/views/131513)의 DP165 사용 만족 문단과 후기 이벤트 제목을 직접 확인했다. 해당 관측의 적용 범위만 기록하며 이번 신규 후기 수입은 **0건**이다. 전체19건의 본문을 모두 확인했다는 뜻이 아니다. MSI DPG는 페이지 틀만 확보됐으며, 다른 작업들은 제출 내용을 검토했어도 공식 사양 조사와 후기 승인을 섞지 않았다. 후기 이벤트, 해외 SKU, 다른 모델 글의 이전 사용 회고를 유지한다. 작성자명·연락처·본문 전문·이미지는 저장하지 않는다.

## 통합 전 교차 품질 검토

10개 임시 재확인 JSON을 교차 확인했다. 모델별8개/전체80개, 확인일2026-10-11, 원문 URL·위치·범위가 있는 구조다. 다음 주의점을 발견했다.

1. LG 3종의 input_profiles 메모에 다른 LG 모델의 조건이 공통 복사되어 있었다. 값 자체의 모델 연결은 올바르지만 표시 메모에 혼동을 만들 수 있어 해당 모델 조건으로 한정하도록 상위 작업자에게 전달했다. 최종 JSON에서 모델별 조건으로 수정됐음을 확인했다.
2. support_product_link와 distinct_related_model은 제품 성능 수치가 아니다. 80개를 모두 신규 사양이나 검증 완료 제품80개로 홍보하지 않는다.
3. 일부 scope는 PANEL/HDMI처럼 기능 범위만 표기한다. 화면은 URL 국가와 record의 원본 지역 메모도 함께 보존해야 하며, scope만 보고 KR 승인으로 요약하지 않는다.
4. 명시된 공식 사실 확인과 공개 검토 승인은 별개다. 공개 상태 UNKNOWN·검토 보류·호환성 사용 불가 계약을 유지한다.

## 구현 및 검증 결과

아래 결과는 이번 작업에서 실제 실행한 결과다. 구현 전 기준선과 최종 검증을 구분했다.

- 추가 검토 데이터: `data/research/monitor-expansion/monitor10_verified_supplement.json`. 검증기: `scripts/validate_monitor10_supplement.py`.
- 추가 검토 페이지: `web/monitor10-review.html` 및 별도 CSS. 생성기: `scripts/build_monitor10_review.py`. 홈과 해당 모델 상세에는 문맥 링크만 연결하고 기존 사양값은 덮어쓰지 않는다.
- 회귀 테스트: `tests/test_monitor10_supplement.py`, `tests/test_monitor10_review.py`, `tests/e2e/monitor10-review.spec.js`.
- 구현 전 Python 기준선: 상위 작업자가 전체490개 통과, 22.322초를 확인했다. 최종 `python3 -m unittest discover -s tests -q`는 **520개 통과 (33.459초)**. 보강 검증기 및 기존 조사 데이터·30종 파생 데이터·30개 정적 페이지 검사 모두 통과. 테스트 중 출력되는 의도적인 stale 입력 실패 문구는 음성 회귀 테스트이며 전체 결과는 OK다.
- 데스크톱·모바일: `npm run test:e2e` **124개 통과 (47.7초)**. 마지막 충돌 설명 라벨 수정 후 `npx playwright test tests/e2e/monitor10-review.spec.js` **6개 재통과 (8.7초)**. 로컬 기존 미커밋 테스트 14개는 보존하되 이번 push에는 포함하지 않으므로 GitHub에서는 110개가 대상이다.
- 보존: 시작 시 273개 파일의 SHA-256과 비교. 기존 파일 중 의도한 변경은 CI, v3 HTML·JS 3개뿐이다. 원본30종·기존6종·질문 코퍼스·사용자 미커밋 변경은 바이트 보존. 테스트가 갱신한 기존 스크린샷 3개는 시작 해시와 HEAD 일치를 확인한 후 시작 내용으로 복원했다.
- 새 문서 내부 경로·로컬 HTML 링크/앵커, 민감 문자열·비밀값 패턴 검사와 `git diff --check` 통과. 작성자명·연락처·원문 전문을 수입하지 않았다. 화면을 직접 확인하고 [데스크톱](screenshots/monitor10-review-desktop.jpg)·[모바일](screenshots/monitor10-review-mobile.jpg) 기록을 남겼다.
- Git: 현재 작업 브랜치에 데이터 검토와 사이트 연결을 나누어 커밋·push한다. 보고서 포함 최종 커밋은 `git log -1 -- docs/MONITOR10_VERIFIED_INTEGRATION_REPORT.md`로 식별한다. GitHub CI에도 보강 데이터 검증과 생성물 일치 검사를 추가했다. CI 실행 결과는 push 후 최종 응답에 기록하며, main 병합·공개 배포는 하지 않는다.

## 남은 작업

한국 SKU와 해외 접미사 관계, Crossover 공식 이미지 직접 검토, MSI/Dell/ASUS 충돌 범위 정리, 미열람 후기 원문 확인은 후속 검토다. 지금 확인된 부분을 보이는 별도 검토 페이지는 가능하지만, 미해결 정보를 확정 사양 필터나 호환성 판정에 넣는 것은 보류한다. 추가 조사 없이 전달 파일 전체340개와 후기19개를 일괄 승인하지 않는다.
